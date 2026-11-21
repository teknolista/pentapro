"""Check/sync PentaPRO plugin metadata or export a self-contained local bundle.

No host installation, config edits, hooks, registry publishing or network calls.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HOSTS = ('codex', 'copilot', 'opencode', 'antigravity-cli')


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def expected(root):
    import yaml  # Maintenance-only metadata generation; not an OpenCode dependency.
    manifest = json.loads((root / 'plugin.json').read_text())
    if manifest['name'] != 'pentapro' or manifest['repository'] != 'https://github.com/teknolista/skills':
        raise ValueError('PentaPRO identity/repository changed')
    if not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', manifest['version']) or manifest.get('license') != 'MIT':
        raise ValueError('Invalid plugin version or license')
    names = sorted(p.parent.name for p in root.glob('*/SKILL.md'))
    if not names or manifest['skills'] != ['./' + n for n in names]:
        raise ValueError('plugin.json must list every source skill exactly once')
    catalog = []
    for name in names:
        source = (root / name / 'SKILL.md').read_text()
        data = yaml.safe_load(source.split('---', 2)[1])
        if data['name'] != name:
            raise ValueError('Skill name mismatch: ' + name)
        catalog.append({'id': name, 'description': data['description'], 'path': name + '/SKILL.md', 'autoinvoke': not data.get('disable-model-invocation', False)})
    codex = manifest | {'interface': {'displayName': 'PentaPRO', 'shortDescription': 'Software engineering skills and factory agents', 'developerName': 'Teknolista'}}
    anti = manifest | {'$schema': 'https://antigravity.google/schemas/v1/plugin.json', 'displayName': 'PentaPRO'}
    marketplace = {'name': 'teknolista', 'owner': {'name': 'Teknolista'}, 'plugins': [{'name': 'pentapro', 'source': './', 'description': manifest['description']}]}
    package = {'name': 'pentapro', 'version': manifest['version'], 'private': True, 'type': 'module', 'description': manifest['description'], 'license': 'MIT', 'repository': {'type': 'git', 'url': 'https://github.com/teknolista/skills.git'}, 'exports': {'.': './plugin/opencode.mjs'}, 'files': ['plugin', 'plugin.json', '.codex-plugin', '.antigravity-plugin', '.github/plugin', '.claude-plugin', 'LICENSE', 'THIRD-PARTY-NOTICES.md', *names]}
    return {'.codex-plugin/plugin.json': codex, '.antigravity-plugin/plugin.json': anti,
            '.github/plugin/marketplace.json': marketplace, '.claude-plugin/marketplace.json': marketplace,
            'package.json': package, 'plugin/catalog.json': catalog}


def synchronize(root, check=False):
    stale = []
    for name, value in expected(root).items():
        path = root / name
        if path.is_symlink() or path.resolve() != path.absolute():
            raise ValueError('Refusing generated metadata symlink: ' + name)
        if not path.is_file() or path.read_text() != encoded(value):
            stale.append(name)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(encoded(value))
    if check and stale:
        raise ValueError('Stale plugin metadata: ' + ', '.join(stale))


def regular_source(root, relative):
    path = root / relative
    if path.is_symlink() or path.resolve() != path or not path.is_file():
        raise ValueError('Refusing missing, symlink or non-regular package input: ' + str(relative))
    return path


def export(root, output, host):
    if host not in HOSTS:
        raise ValueError('Unsupported plugin host')
    root = root.resolve()
    destination = Path(os.path.abspath(output))
    if destination.resolve() != destination or destination.exists():
        raise ValueError('Output must be a new directory with no symlink parents; preserve existing installations')
    if destination.is_relative_to(root):
        raise ValueError('Export outside the source checkout to avoid duplicate skill discovery')
    synchronize(root, check=True)
    manifest = json.loads((root / 'plugin.json').read_text())
    allowed = {Path(p[2:]) for p in manifest['skills']}
    inventory = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root)
    files = []
    for raw in inventory.split(b'\0'):
        if not raw:
            continue
        relative = Path(os.fsdecode(raw))
        if len(relative.parts) < 2 or Path(relative.parts[0]) not in allowed:
            continue
        path = root / relative
        if path.is_symlink() or path.resolve() != path:
            raise ValueError('Refusing package symlink: ' + str(relative))
        if not path.exists():  # Deleted tracked files are not distribution content.
            continue
        if not path.is_file():
            raise ValueError('Refusing non-regular package file: ' + str(relative))
        files.append(relative)
    required = {Path(name) / filename for name in allowed for filename in ('SKILL.md', 'LICENSE')}
    if missing := required - set(files):
        raise ValueError('Distribution inventory excludes required resources: ' + ', '.join(sorted(map(str, missing))))
    auxiliary = ['LICENSE', 'THIRD-PARTY-NOTICES.md']
    auxiliary.append('.codex-plugin/plugin.json' if host == 'codex' else '.antigravity-plugin/plugin.json' if host == 'antigravity-cli' else 'plugin.json')
    if host == 'opencode':
        auxiliary.extend(['package.json', 'plugin/opencode.mjs', 'plugin/catalog.json'])
    for relative in auxiliary:
        regular_source(root, relative)
    # Preflight every input before creating the output; stage for atomic rename.
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.pentapro-build-', dir=destination.parent) as temp:
        staged = Path(temp) / 'plugin'
        staged.mkdir()
        for relative in files:
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / relative, target)
        for name in ('LICENSE', 'THIRD-PARTY-NOTICES.md'):
            shutil.copy2(root / name, staged / name)
        (staged / 'README.md').write_text(f"PentaPRO {manifest['version']}\n\nUse the packaged setup-pentapro skill in the target project. Source and instructions: https://github.com/teknolista/skills\n")
        if host == 'codex':
            (staged / '.codex-plugin').mkdir()
            shutil.copy2(root / '.codex-plugin/plugin.json', staged / '.codex-plugin/plugin.json')
        elif host == 'antigravity-cli':
            shutil.copy2(root / '.antigravity-plugin/plugin.json', staged / 'plugin.json')
        else:
            shutil.copy2(root / 'plugin.json', staged / 'plugin.json')
        if host == 'opencode':
            (staged / 'plugin').mkdir()
            for name in ('opencode.mjs', 'catalog.json'):
                shutil.copy2(root / 'plugin' / name, staged / 'plugin' / name)
            shutil.copy2(root / 'package.json', staged / 'package.json')
        hashes = {str(p.relative_to(staged)): hashlib.sha256(p.read_bytes()).hexdigest() for p in staged.rglob('*') if p.is_file()}
        (staged / 'bundle-files.json').write_text(encoded({'host': host, 'version': manifest['version'], 'files': hashes}))
        # Refuse late destinations too, including an empty directory.
        if destination.exists() or destination.is_symlink():
            raise ValueError('Output appeared during export')
        staged.rename(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--sync', action='store_true')
    group.add_argument('--output', type=Path)
    parser.add_argument('--host', choices=HOSTS)
    args = parser.parse_args()
    try:
        if args.output:
            if not args.host:
                parser.error('--output requires --host')
            print(export(ROOT, args.output, args.host))
        else:
            synchronize(ROOT, check=args.check)
            print('PentaPRO plugin metadata checked' if args.check else 'PentaPRO plugin metadata synchronized')
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'error: {error}\n')


if __name__ == '__main__':
    main()
