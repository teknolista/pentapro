#!/usr/bin/env python3
"""Read-only comparison of installed factory workflows with this package's templates."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import tomllib

TEMPLATES = Path(__file__).resolve().parents[1] / 'assets/agents'
HOSTS = {
    'codex': ('.codex/agents', 'codex.toml', '.toml'),
    'claude-code': ('.claude/agents', 'claude-code.md', '.md'),
    'cursor': ('.cursor/agents', 'cursor.md', '.md'),
    'github-copilot': ('.github/agents', 'github-copilot.md', '.agent.md'),
    'opencode': ('.opencode/agents', 'opencode.md', '.md'),
    'antigravity': ('.agents/agents', 'antigravity.md', '.md'),
}
ROLES = ('factory-spec', 'factory-implementer', 'factory-verifier',
         'factory-reviewer', 'factory-retrospective', 'factory-shipper')
MAX_BYTES = 256 * 1024


def safe_read(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('symbolic-link path refused')
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > MAX_BYTES:
        raise ValueError('expected a regular single-link profile within 256 KiB')
    return path.read_text(encoding='utf-8')


def split_profile(text, host):
    if host == 'codex':
        metadata = tomllib.loads(text)
        body = metadata.pop('developer_instructions', None)
    else:
        match = re.fullmatch(r'---\r?\n(.*?)\r?\n---\r?\n(.*)', text, re.DOTALL)
        if not match or not match[1].strip():
            raise ValueError('expected Markdown frontmatter and workflow body')
        metadata, body = match[1].strip(), match[2]
    if not isinstance(body, str) or not body.strip():
        raise ValueError('expected nonempty workflow instructions')
    return metadata, body.strip()


def check(project, hosts=None, templates=TEMPLATES):
    project = Path(project).absolute()
    if not project.is_dir() or any(p.is_symlink() for p in (project, *project.parents)):
        raise ValueError('project must be a real directory without symlink parents')
    selected = list(dict.fromkeys(hosts)) if hosts else [
        h for h, (directory, _, _) in HOSTS.items()
        if (project / directory).exists() or (project / directory).is_symlink()
    ]
    if any(h not in HOSTS for h in selected):
        raise ValueError('unknown host')
    profiles = []
    for host in selected:
        directory, template_name, suffix = HOSTS[host]
        for role in ROLES:
            relative = Path(directory) / (role + suffix)
            path = project / relative
            item = {'host': host, 'role': role, 'path': str(relative)}
            try:
                expected_meta, expected = split_profile(safe_read(templates / role / template_name), host)
                actual_meta, actual = split_profile(safe_read(path), host)
                item['metadata_customized'] = actual_meta != expected_meta
                if actual == expected:
                    item['status'] = 'current'
                else:
                    item.update(status='review-required',
                                expected_body_sha256=hashlib.sha256(expected.encode()).hexdigest(),
                                actual_body_sha256=hashlib.sha256(actual.encode()).hexdigest())
            except FileNotFoundError:
                item['status'] = 'missing'
            except (OSError, ValueError, UnicodeError) as error:
                item.update(status='invalid', reason=str(error))
            profiles.append(item)
    code = 2 if not selected else int(any(x['status'] != 'current' for x in profiles))
    return {'project': str(project), 'hosts': selected, 'profiles': profiles,
            'status': 'unconfigured' if not selected else ('current' if code == 0 else 'review-required')}, code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--host', action='append', choices=HOSTS,
                        help='Check all six roles for this host; repeat for multiple hosts. Default: existing host directories.')
    args = parser.parse_args()
    try:
        result, code = check(args.project, args.host)
    except (ValueError, OSError) as error:
        result, code = {'status': 'invalid', 'reason': str(error)}, 2
    print(json.dumps(result, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
