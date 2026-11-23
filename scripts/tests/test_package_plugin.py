"""Isolated export controls and optional read-only native discovery probes."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('package_plugin', ROOT / 'scripts/package_plugin.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PluginPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns('.git', 'AGENTS.log*', '__pycache__', 'node_modules'))
        subprocess.run(['git', 'init', '-q', str(self.source)], check=True)

    def test_all_four_exports_are_complete_and_contained(self):
        names = [p[2:] for p in json.loads((self.source / 'plugin.json').read_text())['skills']]
        for host in package.HOSTS:
            output = package.export(self.source, self.root / host, host)
            self.assertEqual(sorted(p.parent.name for p in output.glob('*/SKILL.md')), sorted(names))
            for name in names:
                self.assertEqual((output / name / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())
                self.assertEqual((output / name / 'SKILL.md').read_bytes(), (ROOT / name / 'SKILL.md').read_bytes())
            self.assertFalse((output / 'AGENTS.md').exists())
            self.assertFalse((output / 'AGENTS.log').exists())
            self.assertFalse((output / 'docs/agents/lessons-learned.md').exists())
            manifest = output / ('.codex-plugin/plugin.json' if host == 'codex' else 'plugin.json')
            self.assertEqual(json.loads(manifest.read_text())['name'], 'pentapro')
            self.assertTrue((output / 'setup-pentapro/assets/agents/factory-shipper/codex.toml').is_file())
            for host_profile in ('claude-code.md', 'cursor.md'):
                for role in ('spec', 'implementer', 'verifier', 'reviewer', 'retrospective', 'shipper'):
                    self.assertTrue((output / 'setup-pentapro/assets/agents' / ('factory-' + role) / host_profile).is_file())
            self.assertTrue((output / 'setup-pentapro/assets/lessons-learned.md').is_file())
            self.assertTrue((output / 'bundle-files.json').is_file())
            self.assertEqual((output / 'software-factory/scripts/run_state.py').read_bytes(), (ROOT / 'software-factory/scripts/run_state.py').read_bytes())
            self.assertTrue((output / 'software-factory/references/run-records.md').is_file())
            self.assertEqual((output / 'software-factory/scripts/run_events.py').read_bytes(), (ROOT / 'software-factory/scripts/run_events.py').read_bytes())
            self.assertTrue((output / 'software-factory/references/invocation-events.md').is_file())
            self.assertTrue((output / 'setup-pentapro/assets/runs-readme.md').is_file())
            self.assertFalse((output / 'docs/agents/runs').exists())

    def test_refuses_existing_destination_without_modifying_it(self):
        output = self.root / 'existing'
        output.mkdir()
        (output / 'custom').write_text('keep')
        with self.assertRaises(ValueError):
            package.export(self.source, output, 'codex')
        self.assertEqual((output / 'custom').read_text(), 'keep')

    def test_refuses_internal_export_and_unknown_host(self):
        for output, host in [(self.source / 'out', 'codex'), (self.root / 'out', 'unknown')]:
            with self.assertRaises(ValueError):
                package.export(self.source, output, host)
            self.assertFalse(output.exists())

    def test_rejects_source_symlink_and_does_not_copy_ignored_secrets(self):
        (self.source / 'git-ship/private.md').symlink_to('/etc/hosts')
        with self.assertRaises(ValueError):
            package.export(self.source, self.root / 'unsafe', 'codex')
        self.assertFalse((self.root / 'unsafe').exists())
        (self.source / 'git-ship/private.md').unlink()
        (self.source / 'git-ship/.env').write_text('synthetic private fixture')
        output = package.export(self.source, self.root / 'safe', 'codex')
        self.assertFalse((output / 'git-ship/.env').exists())

    def test_stale_catalog_blocks_export_until_synchronized(self):
        catalog = self.source / 'plugin/catalog.json'
        catalog.write_text('[]\n')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            package.export(self.source, self.root / 'stale', 'opencode')
        package.synchronize(self.source)
        self.assertTrue(package.export(self.source, self.root / 'fresh', 'opencode').exists())

    def test_metadata_check_is_read_only_and_rejects_missing_skill(self):
        manifest = self.source / 'plugin.json'
        before = manifest.read_bytes()
        package.synchronize(self.source, check=True)
        self.assertEqual(manifest.read_bytes(), before)
        data = json.loads(before)
        data['skills'].pop()
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'every source skill'):
            package.synchronize(self.source, check=True)

    def test_exports_are_reproducible(self):
        a = package.export(self.source, self.root / 'a', 'copilot')
        b = package.export(self.source, self.root / 'b', 'copilot')
        self.assertEqual((a / 'bundle-files.json').read_bytes(), (b / 'bundle-files.json').read_bytes())

    def test_refuses_destination_symlink(self):
        output = self.root / 'linked'
        output.symlink_to(self.root / 'not-created')
        with self.assertRaises(ValueError):
            package.export(self.source, output, 'codex')
        self.assertFalse((self.root / 'not-created').exists())

    def test_rejects_auxiliary_symlink_before_creating_output(self):
        license = self.source / 'LICENSE'
        license.unlink()
        license.symlink_to(ROOT / 'LICENSE')
        output = self.root / 'unsafe-root'
        with self.assertRaisesRegex(ValueError, 'package input'):
            package.export(self.source, output, 'opencode')
        self.assertFalse(output.exists())

    def test_refuses_required_skill_resource_excluded_from_inventory(self):
        with (self.source / '.gitignore').open('a') as ignored:
            ignored.write('\n/git-ship/LICENSE\n')
        output = self.root / 'incomplete'
        with self.assertRaisesRegex(ValueError, 'required resources'):
            package.export(self.source, output, 'copilot')
        self.assertFalse(output.exists())

    @unittest.skipUnless(shutil.which('agy'), 'optional Antigravity CLI')
    def test_native_antigravity_strict_discovery(self):
        output = package.export(self.source, self.root / 'native-agy', 'antigravity-cli')
        result = subprocess.run(['agy', 'plugin', 'validate', '--strict', '--json', str(output)], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['components']['skills'], 24)
        self.assertEqual(data['components']['hooks'], 0)

    @unittest.skipUnless(shutil.which('codex'), 'optional Codex CLI')
    def test_native_codex_marketplace_discovery(self):
        result = subprocess.run(['codex', '-c', 'marketplaces.teknolista.source_type="local"',
                                 '-c', 'marketplaces.teknolista.source=' + json.dumps(str(self.source)),
                                 'plugin', 'list', '--available', '--marketplace', 'teknolista', '--json'],
                                cwd=self.source, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        available = json.loads(result.stdout)['available']
        self.assertTrue(any(p['name'] == 'pentapro' and p['version'] == json.loads((self.source / 'plugin.json').read_text())['version'] for p in available), available)
