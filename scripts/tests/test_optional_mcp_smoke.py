"""Only missing optional top-level packages produce an incomplete SDK smoke result."""
from pathlib import Path
import runpy
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'evals/check_mcp_sdk.py'


class OptionalMcpSmokeTests(unittest.TestCase):
    def invoke_with_blocked_import(self, name):
        code = """
import importlib.abc, runpy, sys
class Missing(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in {'httpx2', 'mcp'}:
            raise ModuleNotFoundError('synthetic missing module', name=sys.argv[1])
sys.meta_path.insert(0, Missing())
runpy.run_path(sys.argv[2], run_name='__main__')
"""
        return subprocess.run([sys.executable, '-I', '-B', '-c', code, name, str(SCRIPT)], capture_output=True, text=True)

    def test_missing_optional_dependencies_never_report_success(self):
        for name in ('httpx2', 'mcp'):
            with self.subTest(name=name):
                proc = self.invoke_with_blocked_import(name)
                self.assertEqual(proc.returncode, 2, proc.stderr)
                self.assertIn('No protocol checks ran', proc.stderr)
                self.assertIn('requirements-mcp.txt', proc.stderr)
                self.assertNotIn('Traceback', proc.stderr)
                self.assertEqual(proc.stdout, '')

    def test_incompatible_present_sdk_is_not_disguised_as_missing_dependency(self):
        proc = self.invoke_with_blocked_import('mcp.internal_incompatible_module')
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotEqual(proc.returncode, 2)
        self.assertIn('Traceback', proc.stderr)
        self.assertNotIn('smoke incomplete', proc.stderr)


if __name__ == '__main__':
    unittest.main()
