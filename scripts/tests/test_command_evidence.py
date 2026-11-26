import json
import os
import signal
import time
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(os.environ.get('EVIDENCE_HELPER', Path(__file__).resolve().parents[2] / 'skills/software-factory/scripts/command_evidence.py'))

class CommandEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-qm', 'initial'], check=True)
        self.receipt = self.root / 'receipt.json'

    def call(self, *command, timeout='2', receipt=None):
        return subprocess.run([sys.executable, str(HELPER), '--repo', str(self.root), '--receipt', str(receipt or self.receipt), '--timeout', timeout, '--', *command], capture_output=True, text=True)

    def test_nonzero_and_secrets_not_recorded(self):
        result = self.call(sys.executable, '-c', 'import sys; print("private-output"); sys.exit(7)', 'private-argument')
        self.assertEqual(result.returncode, 7, result.stderr)
        raw = self.receipt.read_text()
        data = json.loads(raw)
        self.assertEqual(data['exit_code'], 7)
        self.assertFalse(data['timed_out'])
        self.assertIn('argv_sha256', data['command'])
        self.assertNotIn('private-', raw)
        self.assertIn('fingerprint', data['git'])
        self.assertGreaterEqual(data['duration_seconds'], 0)

    def test_timeout_returns_124_and_records_timeout(self):
        result = self.call(sys.executable, '-c', 'import time; time.sleep(5)', timeout='0.1')
        self.assertEqual(result.returncode, 124, result.stderr)
        self.assertTrue(json.loads(self.receipt.read_text())['timed_out'])

    def test_timeout_kills_child_process_group(self):
        marker = self.root / 'late-marker'
        child = f'import time; time.sleep(0.8); open({str(marker)!r}, "w").write("bad")'
        parent = f'import subprocess,sys,time; subprocess.Popen([sys.executable, "-c", {child!r}]); time.sleep(5)'
        result = self.call(sys.executable, '-c', parent, timeout='0.2')
        self.assertEqual(result.returncode, 124, result.stderr)
        import time
        time.sleep(1)
        self.assertFalse(marker.exists())

    def test_signal_cancellation_kills_descendants_and_records_interruption(self):
        for sig in (signal.SIGTERM, signal.SIGINT):
            with self.subTest(signal=sig):
                ready = self.root / 'ready'
                marker = self.root / 'cancelled-marker'
                receipt = self.root / f'receipt-{sig}.json'
                child = f'import time; time.sleep(1); open({str(marker)!r}, "w").write("bad")'
                parent = (f'import subprocess,sys,time; '
                          f'subprocess.Popen([sys.executable, "-c", {child!r}]); '
                          f'open({str(ready)!r}, "w").write("ready"); time.sleep(10)')
                wrapper = subprocess.Popen([sys.executable, str(HELPER), '--repo', str(self.root),
                    '--receipt', str(receipt), '--timeout', '8', '--', sys.executable, '-c', parent],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
                try:
                    deadline = time.monotonic() + 4
                    while not ready.exists() and wrapper.poll() is None and time.monotonic() < deadline:
                        time.sleep(0.01)
                    self.assertTrue(ready.exists(), 'command did not start')
                    os.killpg(wrapper.pid, sig)
                    wrapper.communicate(timeout=3)
                    self.assertEqual(wrapper.returncode, -sig)
                    self.assertEqual(json.loads(receipt.read_text())['interruption_signal'], sig)
                    time.sleep(1.1)
                    self.assertFalse(marker.exists(), 'descendant survived cancellation')
                finally:
                    if wrapper.poll() is None:
                        wrapper.kill()
                        wrapper.communicate(timeout=3)
                    ready.unlink(missing_ok=True)
                    marker.unlink(missing_ok=True)

    def test_snapshot_includes_dirty_source_content(self):
        source = self.root / 'source'
        source.write_text('first')
        self.assertEqual(self.call(sys.executable, '-c', 'pass').returncode, 0)
        first = json.loads(self.receipt.read_text())['git']['fingerprint']
        self.receipt.unlink()
        source.write_text('second')
        self.assertEqual(self.call(sys.executable, '-c', 'pass').returncode, 0)
        self.assertNotEqual(first, json.loads(self.receipt.read_text())['git']['fingerprint'])

    def test_existing_receipt_and_links_are_not_modified_or_executed(self):
        marker = self.root / 'marker'
        target = self.root / 'existing'
        target.write_text('keep')
        for path in (target, self.root / 'symlink', self.root / 'hardlink'):
            if path.name == 'symlink': path.symlink_to(target)
            if path.name == 'hardlink': os.link(target, path)
            result = self.call(sys.executable, '-c', f'open({str(marker)!r}, "w").write("bad")', receipt=path)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists())
            self.assertEqual(target.read_text(), 'keep')

    def test_index_unchanged_and_receipt_has_private_permissions(self):
        (self.root / 'a').write_text('staged')
        subprocess.run(['git', '-C', str(self.root), 'add', 'a'], check=True)
        index = (self.root / '.git/index').read_bytes()
        result = self.call(sys.executable, '-c', 'pass')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(index, (self.root / '.git/index').read_bytes())
        self.assertEqual(self.receipt.stat().st_mode & 0o777, 0o600)

if __name__ == '__main__': unittest.main()
