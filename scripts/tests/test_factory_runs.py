"""Behavioral controls for local execution records in disposable Git projects."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('run_state', ROOT / 'software-factory/scripts/run_state.py')
runs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runs)


class FactoryRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.git('init', '-q', '-b', 'main')
        (self.root / '.gitignore').write_text('build/\nAGENTS.log\n')
        (self.root / 'app.py').write_text('value = 1\n')
        self.commit()
        self.path = runs.initialize(self.root, 'sample-run', 'Fix a bounded behavior', ['issue/42'])

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.PIPE)

    def commit(self):
        self.git('add', '-A')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture')

    def load(self):
        return json.loads(self.path.read_text())

    def gate(self, status='passed'):
        return dict(id='check', kind='check', required=True, status=status,
                    snapshot=runs.snapshot(self.root)['fingerprint'], evidence='evidence/check.txt', reason=None)

    def ready(self):
        record = self.load()
        record['state'] = 'SHIP'
        record['gates'] = [self.gate()]
        return record

    def test_init_and_safe_rerun_preserve_record(self):
        self.assertEqual(runs.verify(self.root, 'sample-run')['state'], 'INTAKE')
        before = self.path.read_bytes()
        with self.assertRaises(FileExistsError):
            runs.initialize(self.root, 'sample-run', 'Replacement', [])
        self.assertEqual(self.path.read_bytes(), before)

    def test_snapshot_ignores_only_records_logs_and_untracked_gitignored_outputs(self):
        before = runs.snapshot(self.root)
        (self.path.parent / 'note.md').write_text('Checkpoint detail')
        (self.root / 'AGENTS.log').write_text('Synthetic local fixture')
        (self.root / 'build').mkdir()
        (self.root / 'build/output').write_text('generated')
        self.assertEqual(before, runs.snapshot(self.root))
        (self.root / 'new.py').write_text('value = 2')
        self.assertNotEqual(before, runs.snapshot(self.root))

    def test_snapshot_is_stable_across_commit_and_deletion(self):
        (self.root / 'app.py').unlink()
        before = runs.snapshot(self.root)
        self.commit()
        after = runs.snapshot(self.root)
        self.assertEqual(before['fingerprint'], after['fingerprint'])
        self.assertNotEqual(before['head'], after['head'])

    def test_executable_mode_changes_source_identity(self):
        before = runs.snapshot(self.root)
        (self.root / 'app.py').chmod(0o755)
        self.assertNotEqual(before, runs.snapshot(self.root))

    def test_resume_detects_changed_source_then_accepts_rechecked_candidate(self):
        runs.save(self.root, 'sample-run', self.ready(), 1)
        (self.root / 'app.py').write_text('value = 2\n')
        with self.assertRaisesRegex(ValueError, 'snapshot differs'):
            runs.verify(self.root, 'sample-run')
        stale = self.load()
        stale['snapshot'] = runs.snapshot(self.root)
        with self.assertRaisesRegex(ValueError, 'stale snapshot'):
            runs.save(self.root, 'sample-run', stale, 2)
        stale['gates'][0]['status'] = 'pending'
        stale['state'] = 'VERIFY'
        fresh = runs.save(self.root, 'sample-run', stale, 2)
        self.assertEqual(fresh['record_version'], 3)
        self.assertEqual(fresh['gates'][0]['evidence'], 'evidence/check.txt')
        fresh['gates'][0] = self.gate()
        fresh['state'] = 'SHIP'
        runs.save(self.root, 'sample-run', fresh, 3)
        self.assertEqual(runs.verify(self.root, 'sample-run')['state'], 'SHIP')

    def test_old_writer_and_existing_lock_cannot_replace_record(self):
        old = self.ready()
        runs.save(self.root, 'sample-run', old, 1)
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Concurrent'):
            runs.save(self.root, 'sample-run', old, 1)
        lock = self.path.parent / '.run.lock'
        lock.write_text('another writer')
        with self.assertRaises(FileExistsError):
            runs.save(self.root, 'sample-run', self.load(), 2)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(lock.read_text(), 'another writer')

    def test_failed_gate_blocks_ship_and_preserves_saved_bytes(self):
        for status in ('pending', 'failed', 'unavailable', 'not-applicable'):
            with self.subTest(status=status):
                record = self.ready()
                record['gates'][0]['status'] = status
                before = self.path.read_bytes()
                with self.assertRaises(ValueError):
                    runs.save(self.root, 'sample-run', record, 1)
                self.assertEqual(before, self.path.read_bytes())
                self.assertFalse((self.path.parent / '.run.lock').exists())

    def test_done_requires_task_and_operation_completion(self):
        record = self.ready()
        record['state'] = 'DONE'
        record['tasks'] = [dict(id='T1', owner='factory_implementer', status='running', evidence=None)]
        with self.assertRaisesRegex(ValueError, 'Unfinished tasks'):
            runs.save(self.root, 'sample-run', record, 1)
        record['tasks'][0].update(status='done', evidence='issue/42')
        record['operations'] = [dict(id='P1', kind='push', authorization='issue/42 approval',
                                     status='uncertain', expected_revision=self.git('rev-parse', 'HEAD').decode().strip(), observation=None)]
        with self.assertRaisesRegex(ValueError, 'uncertain'):
            runs.save(self.root, 'sample-run', record, 1)
        # Reconciliation observes the effect; do not issue another push from a record.
        record['operations'][0].update(status='confirmed', observation='reference to remote query receipt')
        runs.save(self.root, 'sample-run', record, 1)
        self.assertEqual(runs.verify(self.root, 'sample-run')['state'], 'DONE')

    def test_confirmation_cannot_omit_observation_or_git_revision(self):
        record = self.ready()
        record['operations'] = [dict(id='P1', kind='push', authorization='issue/42', status='confirmed', expected_revision=None, observation=None)]
        with self.assertRaisesRegex(ValueError, 'observed evidence'):
            runs.save(self.root, 'sample-run', record, 1)
        record['operations'][0]['observation'] = 'receipt'
        with self.assertRaisesRegex(ValueError, 'revision'):
            runs.save(self.root, 'sample-run', record, 1)

    def test_identity_and_history_are_preserved(self):
        for field in ('repository', 'run_id', 'orchestrator', 'history'):
            record = self.ready()
            if field == 'repository':
                record[field]['branch'] = 'other'
            elif field == 'history':
                record[field][0]['state'] = 'DONE'
            else:
                record[field] = 'other'
            with self.assertRaises(ValueError):
                runs.save(self.root, 'sample-run', record, 1)
        self.assertEqual(self.load()['record_version'], 1)

    def test_branch_switch_and_active_git_operation_block_resume(self):
        self.git('checkout', '-qb', 'other')
        with self.assertRaisesRegex(ValueError, 'Branch changed'):
            runs.verify(self.root, 'sample-run')
        self.git('checkout', '-q', 'main')
        (self.root / '.git/MERGE_HEAD').write_text(self.git('rev-parse', 'HEAD').decode())
        with self.assertRaisesRegex(ValueError, 'active Git'):
            runs.verify(self.root, 'sample-run')

    def test_symlink_and_hardlinked_record_are_refused(self):
        backup = self.path.parent / 'original.json'
        self.path.rename(backup)
        self.path.symlink_to(backup)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            runs.verify(self.root, 'sample-run')
        self.path.unlink()
        self.path.hardlink_to(backup)
        with self.assertRaisesRegex(ValueError, 'hard-linked'):
            runs.verify(self.root, 'sample-run')

    def test_invalid_destination_cannot_escape_run_root(self):
        for run_id in ('../outside', '/tmp/run', 'A B', ''):
            with self.assertRaises(ValueError):
                runs.initialize(self.root, run_id, 'Objective', [])
        directory = self.root / runs.RUNS / 'linked'
        directory.symlink_to(self.path.parent, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            runs.initialize(self.root, 'linked', 'Objective', [])

    def test_duplicate_json_and_incomplete_or_misspelled_fields_fail(self):
        bad = self.root / 'candidate.json'
        bad.write_text('{"state":"BUILD","state":"DONE"}')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON'):
            runs.read_json(bad)
        record = self.ready()
        record['nextAction'] = record.pop('next_action')
        with self.assertRaisesRegex(ValueError, 'Invalid fields'):
            runs.save(self.root, 'sample-run', record, 1)

    def test_failed_atomic_replacement_preserves_previous_bytes(self):
        before = self.path.read_bytes()
        with patch.object(runs.os, 'replace', side_effect=OSError('synthetic disk error')):
            with self.assertRaisesRegex(OSError, 'disk error'):
                runs.save(self.root, 'sample-run', self.ready(), 1)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse((self.path.parent / '.run.lock').exists())
        self.assertEqual(sorted(p.name for p in self.path.parent.iterdir()), ['run.json'])

    def test_source_symlink_hashes_target_text_without_reading_external_bytes(self):
        external = Path(self.temp.name) / 'external'
        external.write_text('synthetic private input')
        (self.root / 'external-link').symlink_to(external)
        before = runs.snapshot(self.root)
        external.write_text('changed external contents')
        self.assertEqual(before, runs.snapshot(self.root))
        (self.root / 'external-link').unlink()
        self.assertNotEqual(before, runs.snapshot(self.root))

    def test_tracked_ignored_input_is_included_in_fingerprint(self):
        (self.root / 'build').mkdir()
        tracked = self.root / 'build/tracked.txt'
        tracked.write_text('first')
        self.git('add', '-f', 'build/tracked.txt')
        before = runs.snapshot(self.root)
        tracked.write_text('second')
        self.assertNotEqual(before, runs.snapshot(self.root))

    def test_cli_creates_checks_and_saves_without_model_or_external_effects(self):
        script = ROOT / 'software-factory/scripts/run_state.py'
        args = ['python3', str(script)]
        created = subprocess.run(args + ['init', '--project', str(self.root), '--run-id', 'cli-run', '--objective', 'CLI initialization', '--contract', 'issue/43'], capture_output=True, text=True)
        self.assertEqual(created.returncode, 0, created.stderr)
        captured = subprocess.run(args + ['snapshot', '--project', str(self.root)], capture_output=True, text=True)
        self.assertEqual(captured.returncode, 0, captured.stderr)
        self.assertEqual(json.loads(captured.stdout), runs.snapshot(self.root))
        result = subprocess.run(args + ['check', '--project', str(self.root), '--run-id', 'sample-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        candidate = Path(self.temp.name) / 'candidate.json'
        candidate.write_text(json.dumps(self.ready()))
        result = subprocess.run(args + ['save', '--project', str(self.root), '--run-id', 'sample-run', '--input', str(candidate), '--expect-version', '1'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['record_version'], 2)
        self.assertEqual(self.git('rev-list', '--count', 'HEAD').decode().strip(), '1')
        self.assertEqual(self.git('remote').decode().strip(), '')


if __name__ == '__main__':
    unittest.main()
