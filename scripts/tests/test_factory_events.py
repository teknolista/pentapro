"""Exercise invocation history against disposable Git repositories and real CLI."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'skills/software-factory/scripts'
sys.path.insert(0, str(SCRIPTS))
import run_state as runs
import run_events as events


class FactoryEventsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.git('init', '-q', '-b', 'main')
        (self.root / 'app.py').write_text('value = 1\n')
        self.git('add', 'app.py')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture')
        self.record = runs.initialize(self.root, 'sample-run', 'Fixture', ['issue/1'])
        self.path = self.record.parent / 'events.jsonl'
        self.snapshot = runs.snapshot(self.root)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.PIPE)

    def request(self, event_id='request-1', invocation='invocation-1', task='task-1', attempt=1, at='2026-11-23T12:00:00+00:00'):
        return dict(schema_version=1, event_id=event_id, invocation_id=invocation, run_id='sample-run',
                    event_type='dispatch_requested', occurred_at=at, role='factory_implementer',
                    task_id=task, attempt=attempt, reason='Implement criterion',
                    expected_outcome='Verified behavior', input_snapshot=self.snapshot['fingerprint'],
                    model_requested='model-a', effort_requested='high')

    def transition(self, event_id, kind, invocation='invocation-1', at='2026-11-23T12:01:00+00:00', **kwargs):
        result = dict(schema_version=1, event_id=event_id, invocation_id=invocation, run_id='sample-run',
                      event_type=kind, occurred_at=at)
        if kind == 'dispatched': result['agent_id'] = 'host-agent-1'
        elif kind in events.OUTCOMES: result.update(outcome='Observed', evidence=['checks/result'])
        return result | kwargs

    def append(self, event):
        return events.append(self.root, 'sample-run', event)

    def test_append_lifecycle_idempotence_and_state_isolation(self):
        original = self.record.read_bytes()
        index = self.git('diff', '--cached', '--name-only')
        request = self.request()
        self.assertEqual(self.append(request)['status'], 'appended')
        before = self.path.read_bytes()
        self.assertEqual(self.append(request)['status'], 'unchanged')
        self.assertEqual(self.path.read_bytes(), before)
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            self.append(request | {'reason': 'Changed'})
        self.assertEqual(self.path.read_bytes(), before)
        self.append(self.transition('dispatch-1', 'dispatched', model_observed='observed-model'))
        self.append(self.transition('completion-1', 'completed', at='2026-11-23T12:02:00+00:00', effort_observed='medium', usage={'input_tokens': 42, 'output_tokens': None, 'cost_usd': None}))
        self.append(self.transition('accept-1', 'result_accepted', at='2026-11-23T12:03:00+00:00'))
        info = events.summary(self.root, 'sample-run')
        item = info['invocations'][0]
        self.assertEqual(item['duration_seconds'], 60)
        self.assertEqual(item['usage'], {'input_tokens': 42, 'output_tokens': None, 'cost_usd': None})
        self.assertEqual(item['model_requested'], 'model-a')
        self.assertEqual(item['model_observed'], 'observed-model')
        self.assertEqual(item['effort_observed'], 'medium')
        self.assertEqual(info['open_count'], 0)
        self.assertIsNone(info['project_wall_time_seconds'])
        self.assertEqual(self.record.read_bytes(), original)
        self.assertEqual(runs.snapshot(self.root), self.snapshot)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), index)
        self.assertEqual([p.name for p in self.record.parent.parent.iterdir()], ['sample-run'])

    def test_retry_and_interrupted_or_open_invocations(self):
        self.append(self.request())
        self.append(self.transition('dispatch-1', 'dispatched'))
        self.append(self.transition('interrupted-1', 'interrupted', at='2026-11-23T12:03:00+00:00'))
        self.append(self.request('request-2', 'invocation-2', attempt=2, at='2026-11-23T12:02:00+00:00'))
        info = events.summary(self.root, 'sample-run')
        self.assertEqual(info['invocation_count'], 2)
        self.assertEqual(info['retry_count'], 1)
        self.assertEqual(info['open_count'], 1)
        self.assertEqual(info['outcomes'], {'interrupted': 1, 'dispatch_requested': 1})
        self.assertIsNone(info['invocations'][1]['duration_seconds'])
        self.assertIsNone(info['invocations'][1]['usage'])
        self.assertIsNone(info['invocations'][1]['model_observed'])
        with self.assertRaisesRegex(ValueError, 'increment'):
            self.append(self.request('request-3', 'invocation-3', attempt=2))

    def test_partial_usage_observations_merge_by_metric(self):
        self.append(self.request())
        self.append(self.transition('dispatch-1', 'dispatched', usage={'input_tokens': 42}))
        self.append(self.transition('completion-1', 'completed', at='2026-11-23T12:02:00+00:00',
                                    usage={'input_tokens': None, 'output_tokens': 11}))
        usage = events.summary(self.root, 'sample-run')['invocations'][0]['usage']
        self.assertEqual(usage, {'input_tokens': 42, 'output_tokens': 11, 'cost_usd': None})

    def test_parallel_durations_are_per_invocation_only(self):
        for number in (1, 2):
            invocation = f'invocation-{number}'
            self.append(self.request(f'request-{number}', invocation, f'task-{number}'))
            self.append(self.transition(f'dispatch-{number}', 'dispatched', invocation))
            self.append(self.transition(f'complete-{number}', 'completed', invocation, at='2026-11-23T12:02:00+00:00'))
        info = events.summary(self.root, 'sample-run')
        self.assertEqual([x['duration_seconds'] for x in info['invocations']], [60, 60])
        self.assertIsNone(info['project_wall_time_seconds'])

    def test_terminal_evidence_is_optional_but_validated_when_present(self):
        self.append(self.request())
        event = self.transition('cancel-1', 'cancelled')
        del event['evidence']
        self.append(event)
        self.assertEqual(events.summary(self.root, 'sample-run')['outcomes'], {'cancelled': 1})

    def test_invalid_transition_timestamp_fields_and_usage_leave_history_untouched(self):
        self.append(self.request())
        before = self.path.read_bytes()
        bad = [self.transition('x-1', 'completed'), self.request('x-2', 'invocation-2', 'task-2') | {'occurred_at': '2026-11-23T12:00:00'},
               self.request('x-3', 'invocation-2', 'task-2') | {'extra': 'bad'},
               self.request('x-4', 'invocation-2', 'task-2') | {'usage': {'cost_usd': float('nan')}},
               self.transition('x-5', 'dispatched', at='2026-11-23T11:59:59+00:00')]
        for item in bad:
            with self.subTest(item=item):
                with self.assertRaises(ValueError): self.append(item)
                self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_and_truncated_history_are_not_repaired_or_overwritten(self):
        for content in (b'{bad}\n', b'{"schema_version":1}', b'\n', b'{"x":1,"x":2}\n'):
            self.path.write_bytes(content)
            with self.assertRaises((ValueError, UnicodeError)):
                self.append(self.request())
            self.assertEqual(self.path.read_bytes(), content)

    def test_refuses_symlink_hard_link_and_missing_or_mismatched_runs(self):
        external = Path(self.temp.name) / 'external'
        external.write_bytes(b'keep')
        self.path.symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'Refusing'): self.append(self.request())
        self.path.unlink()
        self.path.hardlink_to(external)
        with self.assertRaisesRegex(ValueError, 'Refusing'): self.append(self.request())
        self.assertEqual(external.read_bytes(), b'keep')
        self.path.unlink()
        with self.assertRaises((ValueError, OSError)): events.append(self.root, '../escape', self.request())
        with self.assertRaises((ValueError, OSError)): events.append(self.root, 'missing-run', self.request())
        record = json.loads(self.record.read_text())
        record['run_id'] = 'another-run'
        self.record.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'identity mismatch'): self.append(self.request())
        self.assertFalse(self.path.exists())

    def test_existing_lock_or_failed_append_never_loses_existing_history(self):
        self.append(self.request())
        before = self.path.read_bytes()
        lock = self.record.parent / '.run.lock'
        lock.write_text('other writer')
        with self.assertRaises(FileExistsError): self.append(self.transition('dispatch-1', 'dispatched'))
        self.assertEqual(lock.read_text(), 'other writer')
        self.assertEqual(self.path.read_bytes(), before)
        lock.unlink()
        with patch.object(events.os, 'write', side_effect=OSError('disk error')):
            with self.assertRaisesRegex(OSError, 'disk error'):
                self.append(self.transition('dispatch-1', 'dispatched'))
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse(lock.exists())

    def test_cli_standalone_installed_copy(self):
        installed = Path(self.temp.name) / 'installed' / 'scripts'
        installed.mkdir(parents=True)
        for name in ('run_state.py', 'run_events.py'):
            shutil.copy2(SCRIPTS / name, installed / name)
        source = Path(self.temp.name) / 'event.json'
        source.write_text(json.dumps(self.request()))
        args = [sys.executable, '-B', str(installed / 'run_events.py')]
        result = subprocess.run(args + ['append', '--project', str(self.root), '--run-id', 'sample-run', '--input', str(source)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'appended')
        result = subprocess.run(args + ['summary', '--project', str(self.root), '--run-id', 'sample-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['open_count'], 1)


if __name__ == '__main__':
    unittest.main()
