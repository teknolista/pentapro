"""Exercise installed-profile diagnostics without touching a real project's settings."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'setup-pentapro/scripts/check_agent_profiles.py'
spec = importlib.util.spec_from_file_location('profiles', SCRIPT)
profiles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(profiles)


class ProfileCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def install(self, host):
        directory, template, suffix = profiles.HOSTS[host]
        for role in profiles.ROLES:
            p = self.project / directory / (role + suffix)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((profiles.TEMPLATES / role / template).read_bytes())
        return self.project / directory / ('factory-shipper' + suffix)

    def test_all_six_hosts_match_without_writes(self):
        for host in profiles.HOSTS:
            self.install(host)
        before = {p: p.read_bytes() for p in self.project.rglob('*') if p.is_file()}
        result, code = profiles.check(self.project)
        self.assertEqual(code, 0)
        self.assertEqual(len(result['profiles']), 36)
        self.assertTrue(all(x['status'] == 'current' for x in result['profiles']))
        self.assertEqual(before, {p: p.read_bytes() for p in self.project.rglob('*') if p.is_file()})

    def test_custom_model_metadata_is_preserved_and_not_workflow_drift(self):
        p = self.install('codex')
        p.write_text(p.read_text().replace('gpt-6-luna', 'project-selected-model').replace('"high"', '"medium"'))
        original = p.read_bytes()
        result, code = profiles.check(self.project)
        self.assertEqual(code, 0)
        shipper = next(x for x in result['profiles'] if x['role'] == 'factory-shipper')
        self.assertTrue(shipper['metadata_customized'])
        self.assertEqual(p.read_bytes(), original)

    def test_legacy_workflow_and_custom_runtime_guard_both_require_review(self):
        p = self.install('opencode')
        original = p.read_text()
        for extra in ('OpenSpec apply workflow', 'Project-specific runtime model guard'):
            with self.subTest(extra=extra):
                p.write_text(original + '\n' + extra + '\n')
                result, code = profiles.check(self.project)
                self.assertEqual(code, 1)
                row = next(x for x in result['profiles'] if x['role'] == 'factory-shipper')
                self.assertEqual(row['status'], 'review-required')
                self.assertNotIn(extra, json.dumps(result))
                self.assertTrue(p.read_text().endswith(extra + '\n'))

    def test_explicit_host_missing_roles_and_no_host_are_incomplete(self):
        result, code = profiles.check(self.project)
        self.assertEqual((result['status'], code), ('unconfigured', 2))
        result, code = profiles.check(self.project, ['cursor'])
        self.assertEqual(code, 1)
        self.assertEqual([x['status'] for x in result['profiles']], ['missing'] * 6)

    def test_invalid_toml_empty_body_and_missing_frontmatter(self):
        for host, data in [('codex', 'not = [valid'), ('opencode', 'no frontmatter'),
                           ('cursor', '---\nname: fixture\n---\n')]:
            with self.subTest(host=host):
                p = self.install(host)
                p.write_text(data)
                result, code = profiles.check(self.project, [host])
                self.assertEqual(code, 1)
                self.assertEqual(result['profiles'][-1]['status'], 'invalid')

    def test_symlinked_profile_or_host_parent_is_refused(self):
        p = self.install('codex')
        outside = self.project / 'private-profile'
        p.rename(outside)
        p.symlink_to(outside)
        result, code = profiles.check(self.project)
        self.assertEqual(code, 1)
        self.assertEqual(result['profiles'][-1]['status'], 'invalid')
        self.assertNotIn('Act only on', json.dumps(result))
        host = self.project / '.opencode/agents'
        host.parent.mkdir()
        host.symlink_to(self.project / '.codex/agents', target_is_directory=True)
        result, code = profiles.check(self.project, ['opencode'])
        self.assertEqual(code, 1)
        self.assertTrue(all(x['status'] == 'invalid' for x in result['profiles']))

    def test_hardlinked_or_oversized_profile_is_refused(self):
        import os
        p = self.install('codex')
        os.link(p, self.project / 'linked-profile')
        result, code = profiles.check(self.project)
        self.assertEqual(code, 1)
        self.assertEqual(result['profiles'][-1]['status'], 'invalid')
        p.unlink()
        p.write_bytes(b'x' * (profiles.MAX_BYTES + 1))
        result, code = profiles.check(self.project)
        self.assertEqual(code, 1)
        self.assertEqual(result['profiles'][-1]['status'], 'invalid')

    def test_invalid_project_and_symlink_root_are_not_success(self):
        with self.assertRaisesRegex(ValueError, 'real directory'):
            profiles.check(self.project / 'missing')
        link = self.project / 'alias'
        link.symlink_to(self.project, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'real directory'):
            profiles.check(link)
        proc = subprocess.run([sys.executable, str(SCRIPT), '--project', str(link)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)['status'], 'invalid')

    def test_cli_exit_and_json_and_argument_validation(self):
        p = self.install('codex')
        proc = subprocess.run([sys.executable, str(SCRIPT), '--project', str(self.project)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['status'], 'current')
        p.write_text(p.read_text() + '\ncustom guard\n')
        proc = subprocess.run([sys.executable, str(SCRIPT), '--project', str(self.project)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(json.loads(proc.stdout)['status'], 'review-required')
        self.assertEqual(profiles.check(self.project, ['codex', 'codex'])[0]['hosts'], ['codex'])
        with self.assertRaisesRegex(ValueError, 'unknown host'):
            profiles.check(self.project, ['unknown'])

    def test_tracked_checkout_roles_match_the_packaged_body_and_settings(self):
        for host in ('codex', 'github-copilot'):
            result, code = profiles.check(ROOT, [host])
            self.assertEqual(code, 0, result)
            self.assertFalse(any(x['metadata_customized'] for x in result['profiles']))


if __name__ == '__main__':
    unittest.main()
