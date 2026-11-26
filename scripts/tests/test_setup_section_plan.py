import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(os.environ.get('SECTION_HELPER', Path(__file__).resolve().parents[2] / 'skills/setup-pentapro/scripts/plan_instruction_sections.py'))
spec = importlib.util.spec_from_file_location('section_plan', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SectionPlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.path = self.root / 'AGENTS.md'

    def plan(self, expected=None):
        return module.plan(self.root, expected)

    def test_fresh_custom_intro_and_adjacent_content_are_preserved(self):
        fresh = self.plan()
        self.assertIn(module.MANIFESTO.encode(), fresh)
        self.assertIn(module.LOGGING.encode(), fresh)
        original = b'Unheaded introduction.\n\n## Project\nKeep this.\n'
        self.path.write_bytes(original)
        proposed = self.plan()
        self.assertTrue(proposed.endswith(original))
        self.path.write_bytes(proposed + b'Unheaded adjacent custom guidance.\n')
        self.assertEqual(self.plan(), self.path.read_bytes())

    def test_idempotent_and_no_write(self):
        result = self.plan()
        self.assertFalse(self.path.exists())
        self.path.write_bytes(result)
        before = self.path.stat().st_mtime_ns
        self.assertEqual(self.plan(), result)
        self.assertEqual(before, self.path.stat().st_mtime_ns)

    def test_duplicate_and_modified_sections_refused(self):
        canonical = self.plan()
        for payload in (canonical + b'\n' + module.MANIFESTO.encode() + b'\n', canonical.replace(b'Our mission is', b'Changed mission is')):
            self.path.write_bytes(payload)
            with self.assertRaises(ValueError): self.plan()
            self.assertEqual(self.path.read_bytes(), payload)

    def test_links_and_stale_before_hash_refused(self):
        other = self.root / 'other'
        other.write_bytes(b'keep')
        self.path.symlink_to(other)
        with self.assertRaises(ValueError): self.plan()
        self.path.unlink()
        os.link(other, self.path)
        with self.assertRaises(ValueError): self.plan()
        self.path.unlink()
        self.path.write_bytes(b'changed')
        with self.assertRaises(ValueError): self.plan(hashlib.sha256(b'old').hexdigest())
        self.assertEqual(self.path.read_bytes(), b'changed')

    def test_non_root_rejected(self):
        child = self.root / 'child'
        child.mkdir()
        with self.assertRaises(ValueError): module.plan(child)

if __name__ == '__main__': unittest.main()
