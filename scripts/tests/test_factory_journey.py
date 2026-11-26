import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / 'evals' / 'check_factory_journey.py'
spec = importlib.util.spec_from_file_location('factory_journey', CHECKER)
journey = importlib.util.module_from_spec(spec)
spec.loader.exec_module(journey)


class FactoryJourneyTests(unittest.TestCase):
    def test_clean_journey_and_seeded_viewport_control(self):
        good = subprocess.run([sys.executable, str(CHECKER)], capture_output=True, text=True, timeout=15)
        bad = subprocess.run([sys.executable, str(CHECKER), '--seed-defect'], capture_output=True, text=True, timeout=15)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertIn('PASS:', good.stdout)
        self.assertEqual(bad.returncode, 1, bad.stderr)
        self.assertIn('selected Gamma row and its amount are not visible together', bad.stderr)

    def test_report_checker_rejects_nonzero_malformed_and_wrong_decimal(self):
        for status, stdout, stderr in [(2, b'{"selected":"Gamma","amount":"2.35","total":"3.65"}', b''),
                                        (0, b'not json', b''),
                                        (0, b'{"selected":"Gamma","amount":"2.35","total":"3.64"}', b''),
                                        (0, b'\x1b[31m{}', b''),
                                        (0, b'{}', b'warning')]:
            with self.subTest(status=status, stdout=stdout):
                with self.assertRaises(AssertionError):
                    journey.check_report(subprocess.CompletedProcess([], status, stdout, stderr))

    def test_fixture_rejects_invalid_values_without_stdout(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'input.json'
            for value in ('NaN', '-1.00', '1.234', '1e3', '\u001b[31m'):
                with self.subTest(value=value):
                    path.write_text(json.dumps({'items': [{'name': 'Gamma', 'amount': value}]}))
                    result = subprocess.run([sys.executable, str(journey.APP), 'report', str(path)], capture_output=True, timeout=5)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, b'')
                    self.assertIn(b'invalid input:', result.stderr)
                    self.assertNotIn(b'\x1b', result.stderr)

    def test_both_viewports_detect_seeded_defect(self):
        for width, height in ((80, 24), (40, 12)):
            with self.subTest(width=width, height=height):
                capture = journey.render(journey.FIXTURE / 'input.json', width, height, seeded=True)
                with self.assertRaisesRegex(AssertionError, 'selected Gamma row'):
                    journey.check_view(capture, width, height)

    def test_hanging_process_group_is_terminated(self):
        with tempfile.TemporaryDirectory() as temp:
            tmp = Path(temp)
            marker = tmp / 'late-write'
            app = tmp / 'slow.py'
            app.write_text(
                'import subprocess, sys, time\n'
                'subprocess.Popen([sys.executable, "-c", '
                + repr('import time; from pathlib import Path; time.sleep(0.8); Path(' + repr(str(marker)) + ').write_text("late")')
                + '])\n'
                'time.sleep(10)\n'
            )
            original = journey.APP
            journey.APP = app
            try:
                started = time.monotonic()
                with self.assertRaises(TimeoutError):
                    journey.render(tmp / 'unused', 40, 12, timeout=0.3)
                self.assertLess(time.monotonic() - started, 3)
                time.sleep(1)
                self.assertFalse(marker.exists(), 'descendant survived timeout')
            finally:
                journey.APP = original

    def test_view_checker_rejects_missing_value_and_bad_dimensions(self):
        with self.assertRaises(AssertionError):
            journey.check_view(b'Report 40x12\r\nName / amount (USD)\r\n> Gamma\r\n', 40, 12)
        with self.assertRaises(AssertionError):
            journey.check_view(b'Report 80x24\r\nName / amount (USD)\r\n> Gamma: 2.35 USD\r\n', 40, 12)


if __name__ == '__main__':
    unittest.main()
