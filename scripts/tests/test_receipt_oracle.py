"""Pure oracle controls complement, rather than replace, real isolated grader tests."""
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('receipt_oracle', ROOT / 'evals/check_receipts.py')
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class ReceiptOracleTests(unittest.TestCase):
    def test_opaque_receipt_replay_conflict_and_tenant_separation(self):
        body = {'request_id': 'x', 'payload': 'payload'}
        calls = [('a', body), ('a', body), ('a', dict(body, payload='changed')), ('b', body)]
        a = ['a', 'payload']; b = ['b', 'payload']
        observations = [
            [[202, {'receipt': 'opaque-A'}], [a]],
            [[202, {'receipt': 'opaque-A'}], [a]],
            [[409, {'error': 'idempotency_conflict'}], [a]],
            [[202, {'receipt': 'opaque-B'}], [a, b]],
        ]
        self.assertTrue(oracle.follows_contract(calls, observations))
        observations[-1][0][1]['receipt'] = 'opaque-A'
        self.assertFalse(oracle.follows_contract(calls, observations))

    def test_forged_status_wrong_shape_and_unauthorized_effect_are_rejected(self):
        call = [('a', {'request_id': 'x', 'payload': 'payload'})]
        for forged in ({'status': 'pass'}, [], [[['202', {'receipt': 'x'}], [['a', 'payload']]]],
                       [[[202, {'receipt': 'x'}], [['a', 'payload'], ['other', 'payload']]]]):
            with self.subTest(forged=forged):
                self.assertFalse(oracle.follows_contract(call, forged))
        self.assertFalse(oracle.follows_contract([(None, {})], [[[401, {'error': 'unauthenticated'}], [['a', 'payload']]]]))

    def test_rejected_inputs_preserve_effects_and_randomized_cases_are_reproducible(self):
        calls = [(None, {}), ('a', None), ('a', {'request_id': [], 'payload': 'x'})]
        observations = [[[401, {'error': 'unauthenticated'}], []],
                        [[400, {'error': 'invalid_request'}], []],
                        [[400, {'error': 'invalid_request'}], []]]
        self.assertTrue(oracle.follows_contract(calls, observations))
        self.assertEqual(oracle.build_scenarios(53), oracle.build_scenarios(53))
        self.assertNotEqual(oracle.build_scenarios(53), oracle.build_scenarios(54))


if __name__ == '__main__':
    unittest.main()
