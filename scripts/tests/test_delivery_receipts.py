"""Exercise actual staged/committed receipt blobs in disposable Git histories."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'skills/software-factory/scripts'
sys.path.insert(0, str(PACKAGE))
import run_state
import run_events
SPEC = importlib.util.spec_from_file_location('delivery_receipts', PACKAGE / 'check_delivery_receipts.py')
receipts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(receipts)


class DeliveryReceiptsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q', '-b', 'main')
        (self.root / 'app.py').write_text('value = 1\n')
        self.commit()
        self.path = run_state.initialize(self.root, 'sample-run', 'Fixture delivery', ['issue/42'])
        value = self.load()
        value['state'] = 'RECORDS'
        value['gates'] = [dict(id='tests', kind='check', required=True, status='passed',
                               snapshot=value['snapshot']['fingerprint'], evidence='fixture', reason=None)]
        run_state.save(self.root, 'sample-run', value, 1)
        self.events = self.path.parent / 'events.jsonl'
        self.event('dispatch_requested', 0, role='factory_shipper', task_id='ship', attempt=1,
                   reason='Fixture', expected_outcome='Fixture', input_snapshot=value['snapshot']['fingerprint'])
        self.event('dispatched', 1, agent_id='fixture-agent')
        other = self.path.parent.parent / 'other-run/run.json'
        other.parent.mkdir()
        other.write_text('{}\n')
        self.base = self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.PIPE)

    def commit(self):
        self.git('add', '-A')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture')
        return self.git('rev-parse', 'HEAD').decode().strip()

    def load(self):
        return json.loads(self.path.read_text())

    def event(self, kind, second, **fields):
        value = dict(schema_version=1, event_id='fixture-' + kind.replace('_', '-'),
                     invocation_id='fixture-ship', run_id='sample-run', event_type=kind,
                     occurred_at=f'2026-11-26T12:00:{second:02d}+00:00') | fields
        run_events.append(self.root, 'sample-run', value)

    def closeout(self):
        value = self.load()
        value['snapshot'] = run_state.snapshot(self.root)
        value['operations'] = [dict(id=kind, kind=kind, authorization='Synthetic fixture authority',
                                    status='confirmed', expected_revision=self.base,
                                    observation='Synthetic fixture observation, not an actual remote push')
                               for kind in ('commit', 'push')]
        run_state.save(self.root, 'sample-run', value, value['record_version'])
        self.event('completed', 2, outcome='Fixture delivery confirmed')

    def checked(self):
        head = self.commit()
        return receipts.check(self.root, self.base, head, validate=True)

    def corrupt(self, edit):
        value = self.load()
        edit(value)
        self.path.write_text(json.dumps(value) + '\n')

    def test_committed_closeout_validates_and_has_no_self_reference(self):
        self.closeout()
        result = self.checked()
        self.assertEqual(result['mode'], 'receipts')
        self.assertEqual(result['run_id'], 'sample-run')
        self.assertEqual(len(result['paths']), 2)
        self.assertEqual(self.load()['snapshot']['head'], self.base)

    def test_staged_blobs_are_validated_instead_of_unstaged_bytes(self):
        self.closeout()
        self.git('add', '--', str(self.path.relative_to(self.root)), str(self.events.relative_to(self.root)))
        self.path.write_text('invalid unstaged content')
        result = receipts.check(self.root, self.base, staged=True, validate=True)
        self.assertEqual(result['mode'], 'receipts')

    def test_source_mixed_with_receipts_requires_full_checks(self):
        self.closeout()
        (self.root / 'app.py').write_text('value = 2\n')
        self.assertEqual(self.checked()['mode'], 'full')

    def test_new_record_or_arbitrary_document_requires_full_checks(self):
        self.closeout()
        (self.path.parent / 'note.md').write_text('not a closeout record\n')
        self.assertEqual(self.checked()['mode'], 'full')

    def test_two_runs_require_full_checks(self):
        self.closeout()
        (self.path.parent.parent / 'other-run/run.json').write_text('{"changed":true}\n')
        self.assertEqual(self.checked()['mode'], 'full')

    def test_deleted_record_requires_full_checks(self):
        self.closeout()
        self.events.unlink()
        self.assertEqual(self.checked()['mode'], 'full')

    def test_executable_mode_change_requires_full_checks(self):
        self.closeout()
        self.path.chmod(0o755)
        self.assertEqual(self.checked()['mode'], 'full')

    def test_renamed_record_requires_full_checks(self):
        self.closeout()
        self.events.rename(self.events.with_name('renamed.jsonl'))
        self.assertEqual(self.checked()['mode'], 'full')

    def test_unknown_base_and_empty_diff_require_full_checks(self):
        self.assertEqual(receipts.check(self.root, '0' * 40, self.base)['mode'], 'full')
        self.assertEqual(receipts.check(self.root, self.base, self.base)['mode'], 'full')

    def test_bad_json_is_rejected(self):
        self.closeout()
        self.path.write_text('{"duplicate":1,"duplicate":2}')
        with self.assertRaises(ValueError):
            self.checked()

    def test_truncated_events_are_rejected(self):
        self.closeout()
        self.events.write_bytes(self.events.read_bytes().rstrip(b'\n'))
        with self.assertRaises(ValueError):
            self.checked()

    def test_event_rewrite_is_rejected(self):
        self.closeout()
        self.events.write_text(self.events.read_text().replace('"reason":"Fixture"', '"reason":"Changed"'))
        with self.assertRaises(ValueError):
            self.checked()

    def test_missing_primary_publication_is_rejected(self):
        self.closeout()
        self.corrupt(lambda v: v.update(operations=[]))
        with self.assertRaises(ValueError):
            self.checked()

    def test_source_identity_cannot_be_restamped(self):
        self.closeout()
        self.corrupt(lambda v: v['snapshot'].update(fingerprint='a' * 64))
        with self.assertRaises(ValueError):
            self.checked()

    def test_gate_changes_are_not_receipt_only(self):
        self.closeout()
        self.corrupt(lambda v: v['gates'][0].update(status='pending'))
        with self.assertRaises(ValueError):
            self.checked()

    def test_history_rewrite_is_rejected(self):
        self.closeout()
        self.corrupt(lambda v: v['history'][0].update(state='BUILD'))
        with self.assertRaises(ValueError):
            self.checked()

    def test_run_identity_cannot_change(self):
        self.closeout()
        self.corrupt(lambda v: v.update(run_id='other-run'))
        with self.assertRaises(ValueError):
            self.checked()

    def test_primary_revision_must_be_actual_base(self):
        self.closeout()
        self.corrupt(lambda v: v['snapshot'].update(head='a' * 40))
        with self.assertRaises(ValueError):
            self.checked()

    def test_record_mutation_requires_a_new_checkpoint_version(self):
        self.closeout()
        old = json.loads(self.git('show', self.base + ':' + str(self.path.relative_to(self.root))))
        self.corrupt(lambda v: v.update(record_version=old['record_version'], history=old['history']))
        with self.assertRaises(ValueError):
            self.checked()

    def test_validating_final_commit_does_not_create_another_tracked_change(self):
        self.closeout()
        head = self.commit()
        for _ in range(2):
            result = receipts.check(self.root, self.base, head, validate=True)
            self.assertTrue(result['validated'])
        self.assertEqual(self.git('status', '--porcelain'), b'')
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), head)

    def test_ci_outputs_come_from_actual_paths_and_unknown_history_is_full(self):
        self.closeout()
        head = self.commit()
        command = [sys.executable, str(PACKAGE / 'check_delivery_receipts.py'), '--project', str(self.root),
                   '--base', self.base, '--head', head, '--github-output']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout, 'receipts_only=true\n')
        command[command.index('--base') + 1] = '0' * 40
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout, 'receipts_only=false\n')

    def test_symlink_record_requires_full_checks(self):
        self.closeout()
        self.events.unlink()
        self.events.symlink_to('run.json')
        self.assertEqual(self.checked()['mode'], 'full')

    def test_unfinished_invocations_cannot_be_closed(self):
        self.closeout()
        self.events.write_bytes(self.git('show', self.base + ':' + str(self.events.relative_to(self.root))))
        with self.assertRaises(ValueError):
            self.checked()

    def test_hyphenated_host_shipper_role_is_supported(self):
        self.events.write_text(self.events.read_text().replace('factory_shipper', 'factory-shipper'))
        self.base = self.commit()
        self.closeout()
        self.assertTrue(self.checked()['validated'])

    def test_primary_shipper_invocation_must_be_present(self):
        self.events.write_text(self.events.read_text().replace('factory_shipper', 'factory_verifier'))
        self.base = self.commit()
        self.closeout()
        with self.assertRaises(ValueError):
            self.checked()

    def test_prior_confirmed_operations_are_preserved(self):
        value = self.load()
        value['operations'] = [dict(id='older-commit', kind='commit', authorization='Fixture',
                                   status='confirmed', expected_revision=self.base, observation='Fixture')]
        self.path.write_text(json.dumps(value) + '\n')
        self.base = self.commit()
        self.closeout()  # Deliberately overwrites the older operation: validator must reject it.
        with self.assertRaises(ValueError):
            self.checked()

    def test_lightweight_cli_rejects_full_scope_without_weakening_gate(self):
        self.closeout()
        (self.root / 'app.py').write_text('value = 3\n')
        head = self.commit()
        result = subprocess.run([sys.executable, str(PACKAGE / 'check_delivery_receipts.py'),
                                 '--project', str(self.root), '--base', self.base, '--head', head, '--validate'],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
