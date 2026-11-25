"""Local factory execution records. No model, network, Git mutation or command execution from records."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

STATES = {'INTAKE', 'CONTRACT', 'PLAN', 'BUILD', 'VERIFY', 'REVIEW', 'RECORDS',
          'SHIP', 'ARCHIVE', 'RETROSPECTIVE', 'DONE', 'BLOCKED'}
RUNS = Path('docs/agents/runs')
HASH = re.compile(r'^[0-9a-f]{64}$')
IDENTIFIER = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def git(project, *args):
    return subprocess.check_output(['git', *args], cwd=project, stderr=subprocess.PIPE)


def project_root(project):
    project = Path(project).resolve(strict=True)
    actual = Path(os.fsdecode(git(project, 'rev-parse', '--show-toplevel')).strip()).resolve()
    if actual != project:
        raise ValueError('--project must identify the target Git root')
    for operation in ('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply'):
        path = Path(os.fsdecode(git(project, 'rev-parse', '--git-path', operation)).strip())
        if not path.is_absolute():
            path = project / path
        if path.exists():
            raise ValueError('Reconcile active Git operation before recording: ' + operation)
    return project


def branch(project):
    name = os.fsdecode(git(project, 'symbolic-ref', '--quiet', '--short', 'HEAD')).strip()
    if not name:
        raise ValueError('Detached HEAD is not a factory execution branch')
    return name


def snapshot(project):
    """Hash path, kind, mode and bytes of every Git-inventoried source file.

    Excludes only factory records and root prompt logs. Ignored untracked files
    are outside this identity; owners must record external/generated inputs separately.
    """
    project = project_root(project)
    paths = sorted(set(git(project, 'ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0')) - {b''})
    digest = hashlib.sha256()
    for raw in paths:
        relative = Path(os.fsdecode(raw))
        if relative.is_relative_to(RUNS) or (len(relative.parts) == 1 and (relative.name == 'AGENTS.log' or relative.name.startswith('AGENTS.log.'))):
            continue
        path = project / relative
        # A symlink is hashed as a link, never dereferenced (also for symlinked parents).
        for parent in path.parents:
            if parent == project:
                break
            if parent.is_symlink():
                raise ValueError('Source inventory contains symlink parent: ' + str(relative))
        if path.is_symlink():
            kind, payload, mode = 'symlink', os.fsencode(os.readlink(path)), 'link'
        elif not path.exists():
            continue  # Absence must hash identically before and after committing a deletion.
        elif path.is_file():
            before = path.stat()
            payload = path.read_bytes()
            after = path.stat()
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                raise ValueError('Source changed during snapshot capture')
            kind, mode = 'file', 'executable' if before.st_mode & 0o111 else 'regular'
        else:
            raise ValueError('Unsupported source input: ' + str(relative))
        item = [os.fsdecode(raw), kind, mode, hashlib.sha256(payload).hexdigest()]
        digest.update(json.dumps(item, ensure_ascii=True, separators=(',', ':')).encode() + b'\n')
    return {'fingerprint': digest.hexdigest(), 'head': os.fsdecode(git(project, 'rev-parse', 'HEAD')).strip()}


def unique_object(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('Duplicate JSON field: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, required, label):
    require(isinstance(value, dict) and set(value) == set(required.split()), 'Invalid fields: ' + label)


def validate(record, current=None):
    fields(record, 'schema_version run_id record_version objective contracts repository orchestrator state snapshot gates tasks operations blockers next_action history', 'run')
    require(type(record['schema_version']) is int and record['schema_version'] == 1, 'Unsupported schema')
    require(type(record['record_version']) is int and record['record_version'] >= 1, 'Invalid record version')
    require(isinstance(record['run_id'], str) and IDENTIFIER.fullmatch(record['run_id']), 'Invalid run ID')
    require(text(record['objective']) and text(record['orchestrator']) and text(record['next_action']), 'Objective, orchestrator and next action required')
    require(record['state'] in STATES, 'Invalid state')
    for key in ('contracts', 'blockers'):
        require(isinstance(record[key], list) and all(text(v) for v in record[key]), 'Invalid ' + key)
    fields(record['repository'], 'root branch base_commit', 'repository')
    require(all(text(v) for v in record['repository'].values()), 'Repository identity required')
    fields(record['snapshot'], 'fingerprint head', 'snapshot')
    require(isinstance(record['snapshot']['fingerprint'], str) and HASH.fullmatch(record['snapshot']['fingerprint']), 'Invalid fingerprint')
    require(isinstance(record['snapshot']['head'], str) and re.fullmatch(r'[0-9a-f]{40,64}', record['snapshot']['head']), 'Invalid HEAD')
    if current is not None:
        require(record['snapshot'] == current, 'Record snapshot differs from actual project; reconcile before continuing')
    for group in ('gates', 'tasks', 'operations'):
        require(isinstance(record[group], list), 'Invalid ' + group)
        seen = set()
        for item in record[group]:
            require(isinstance(item, dict) and text(item.get('id')), 'Missing ' + group + ' ID')
            require(item['id'] not in seen, 'Duplicate ' + group + ' ID')
            seen.add(item['id'])
    for gate in record['gates']:
        fields(gate, 'id kind required status snapshot evidence reason', 'gate')
        require(gate['kind'] in {'check', 'review', 'spec-review'}, 'Invalid gate kind')
        require(type(gate['required']) is bool, 'Gate required must be boolean')
        require(gate['status'] in {'pending', 'passed', 'failed', 'unavailable', 'not-applicable'}, 'Invalid gate status')
        require(gate['snapshot'] is None or (isinstance(gate['snapshot'], str) and HASH.fullmatch(gate['snapshot'])), 'Invalid gate snapshot')
        require(gate['evidence'] is None or text(gate['evidence']), 'Invalid evidence reference')
        require(gate['reason'] is None or text(gate['reason']), 'Invalid gate reason')
        if gate['status'] == 'passed':
            require(gate['snapshot'] == record['snapshot']['fingerprint'] and text(gate['evidence']), 'Passed gate has stale snapshot or missing evidence: ' + gate['id'])
        if gate['status'] == 'not-applicable':
            require(not gate['required'] and text(gate['reason']), 'Required gate cannot be marked not applicable')
    for task in record['tasks']:
        fields(task, 'id owner status evidence', 'task')
        require(text(task['owner']) and task['status'] in {'pending', 'running', 'done', 'blocked'}, 'Invalid task')
        require(task['evidence'] is None or text(task['evidence']), 'Invalid task evidence')
        if task['status'] == 'done':
            require(text(task['evidence']), 'Completed task needs evidence reference')
    for operation in record['operations']:
        fields(operation, 'id kind authorization status expected_revision observation', 'operation')
        require(operation['kind'] in {'commit', 'push', 'pr', 'merge', 'archive', 'release', 'deploy'}, 'Invalid operation kind')
        require(text(operation['authorization']), 'Operation needs authority reference')
        require(operation['status'] in {'planned', 'uncertain', 'confirmed', 'failed'}, 'Invalid operation status')
        require(operation['expected_revision'] is None or (isinstance(operation['expected_revision'], str) and re.fullmatch(r'[0-9a-f]{40,64}', operation['expected_revision'])), 'Invalid expected revision')
        require(operation['observation'] is None or text(operation['observation']), 'Invalid operation observation')
        if operation['status'] == 'confirmed':
            require(text(operation['observation']), 'Confirmed operation needs observed evidence')
            if operation['kind'] in {'commit', 'push'}:
                require(operation['expected_revision'] is not None, 'Git confirmation needs revision')
    require(isinstance(record['history'], list), 'Invalid history')
    for entry in record['history']:
        fields(entry, 'record_version state snapshot orchestrator', 'history')
        require(type(entry['record_version']) is int and entry['state'] in STATES and text(entry['orchestrator']), 'Invalid history entry')
        require(isinstance(entry['snapshot'], str) and HASH.fullmatch(entry['snapshot']), 'Invalid history snapshot')
    require([e['record_version'] for e in record['history']] == list(range(1, record['record_version'] + 1)), 'Incomplete history')
    last = record['history'][-1]
    require(last == history_entry(record), 'History does not match current record')
    if record['state'] in {'SHIP', 'DONE'}:
        require(not record['blockers'], 'Resolve blockers before shipping or completion')
        require(bool(record['contracts']) and bool(record['gates']), 'Define contract references and gates before shipping or completion')
        require(all(o['status'] != 'uncertain' for o in record['operations']), 'Reconcile uncertain effects before dependent shipping')
        require(all(g['status'] == 'passed' for g in record['gates'] if g['required']), 'Required gates pending or failed')
    if record['state'] == 'DONE':
        require(all(t['status'] == 'done' for t in record['tasks']), 'Unfinished tasks')
        require(all(o['status'] == 'confirmed' for o in record['operations']), 'Unconfirmed operations; inspect actual effects before retrying')


def history_entry(record):
    return {k: record[k] for k in ('record_version', 'state', 'orchestrator')} | {'snapshot': record['snapshot']['fingerprint']}


def record_path(project, run_id):
    require(isinstance(run_id, str) and IDENTIFIER.fullmatch(run_id), 'Invalid run ID')
    target = project / RUNS / run_id / 'run.json'
    for path in [target, *target.parents]:
        if path == project.parent:
            break
        require(not path.is_symlink(), 'Refusing symlink record path')
        if path.exists():
            if path == target:
                info = path.stat()
                require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'Refusing non-regular or hard-linked record')
            else:
                require(path.is_dir(), 'Record parent must be directory')
    return target


@contextmanager
def locked(target):
    lock = target.parent / '.run.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try:
        yield
    finally:
        lock.unlink()


def atomic_write(target, record):
    fd, name = tempfile.mkstemp(prefix='.run-', dir=target.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def initialize(project, run_id, objective, contracts, orchestrator='main-session'):
    project = project_root(project)
    target = record_path(project, run_id)
    identity = snapshot(project)
    record = dict(schema_version=1, run_id=run_id, record_version=1, objective=objective,
                  contracts=contracts, repository={'root': str(project), 'branch': branch(project), 'base_commit': identity['head']},
                  orchestrator=orchestrator, state='INTAKE', snapshot=identity,
                  gates=[], tasks=[], operations=[], blockers=[], next_action='Define scope, required gates and role packets.', history=[])
    record['history'] = [history_entry(record)]
    validate(record, identity)
    # mkdir is exclusive for each run: reruns never replace an existing record.
    target.parent.parent.mkdir(parents=True, exist_ok=True)
    target.parent.mkdir()
    with locked(target):
        atomic_write(target, record)
    return target


def verify(project, run_id):
    project = project_root(project)
    record = read_json(record_path(project, run_id))
    validate(record, snapshot(project))
    require(record['run_id'] == run_id and record['repository']['root'] == str(project), 'Record project/run identity mismatch')
    require(record['repository']['branch'] == branch(project), 'Branch changed; reconcile execution identity')
    return record


def save(project, run_id, candidate, expected_version):
    project = project_root(project)
    target = record_path(project, run_id)
    with locked(target):
        old = read_json(target)
        validate(old)  # Old source may legitimately be stale after authorized work.
        require(old['record_version'] == expected_version, 'Concurrent record update; reread latest state')
        for key in ('schema_version', 'run_id', 'repository', 'orchestrator'):
            require(candidate[key] == old[key], 'Immutable execution identity changed: ' + key)
        require(old['run_id'] == run_id and old['repository']['root'] == str(project) and old['repository']['branch'] == branch(project), 'Project/run identity changed')
        require(candidate['record_version'] == expected_version and candidate['history'] == old['history'], 'Candidate must preserve version and history; helper advances them')
        candidate = json.loads(json.dumps(candidate))
        candidate['record_version'] += 1
        candidate['history'].append(history_entry(candidate))
        validate(candidate, snapshot(project))
        atomic_write(target, candidate)
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'snapshot', 'check', 'save'])
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--run-id')
    parser.add_argument('--objective')
    parser.add_argument('--contract', action='append', default=[])
    parser.add_argument('--input', type=Path)
    parser.add_argument('--expect-version', type=int)
    args = parser.parse_args()
    try:
        if args.command == 'snapshot':
            result = snapshot(args.project)
        else:
            require(args.run_id is not None, '--run-id required')
            if args.command == 'init':
                require(text(args.objective), '--objective required')
                result = str(initialize(args.project, args.run_id, args.objective, args.contract))
            elif args.command == 'check':
                result = verify(args.project, args.run_id)
            else:
                require(args.input is not None and args.expect_version is not None, '--input and --expect-version required')
                require(args.input.resolve() != record_path(project_root(args.project), args.run_id), 'Use a separate candidate file; preserve the saved record')
                result = save(args.project, args.run_id, read_json(args.input), args.expect_version)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError, IndexError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'run-state error: {error}\n')


if __name__ == '__main__':
    main()
