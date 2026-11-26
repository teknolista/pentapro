#!/usr/bin/env python3
"""Classify real Git changes and validate a bounded receipt closeout, without writes."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

import run_events
import run_state

SHA = re.compile(r'(?:[0-9a-f]{40}|[0-9a-f]{64})\Z')
RECORD = re.compile(r'docs/agents/runs/([a-z0-9]+(?:-[a-z0-9]+)*)/(run\.json|events\.jsonl)\Z')


def git(repo, *args):
    return subprocess.check_output(['git', *args], cwd=repo, stderr=subprocess.PIPE)


def revision(repo, value):
    if value == 'HEAD':
        value = git(repo, 'rev-parse', '--verify', 'HEAD').decode().strip()
    if not value or not SHA.fullmatch(value):
        raise ValueError('Expected a complete commit SHA')
    git(repo, 'cat-file', '-e', value + '^{commit}')
    return value


def strict_json(data):
    def invalid(_value):
        raise ValueError('Non-finite JSON number')
    return json.loads(data, object_pairs_hook=run_state.unique_object, parse_constant=invalid)


def event_list(data, run_id):
    run_state.require(not data or data.endswith(b'\n'), 'Truncated event history')
    rows = data.splitlines()
    run_state.require(all(rows), 'Blank event history row')
    events = [strict_json(row) for row in rows]
    _, invocations = run_events.validate_history(events, run_id)
    run_state.require(all(v[-1]['event_type'] not in {'dispatch_requested', 'dispatched'}
                          for v in invocations.values()), 'Unfinished invocation in closeout')
    run_state.require(any(v[0].get('role') in {'factory_shipper', 'factory-shipper'} for v in invocations.values()),
                      'Missing finished primary shipper invocation')
    return events


def check(repo, base, head='HEAD', *, staged=False, validate=False):
    repo = Path(repo)
    full = lambda reason: {'mode': 'full', 'reason': reason, 'paths': []}
    try:
        base = revision(repo, base)
        target = None if staged else revision(repo, head)
        args = ['diff'] + (['--cached'] if staged else []) + ['--raw', '-z', '--no-renames', base]
        if not staged:
            args.append(target)
        raw = git(repo, *args, '--').split(b'\0')
    except (ValueError, OSError, subprocess.CalledProcessError):
        return full('Unknown comparison history; run full checks')
    rows = [x for x in raw if x]
    if not rows or len(rows) % 2:
        return full('Empty or unrecognized comparison; run full checks')
    paths, run_ids = [], set()
    for meta, name in zip(rows[::2], rows[1::2]):
        fields = meta.split()
        path = name.decode('utf-8', errors='replace')
        match = RECORD.fullmatch(path)
        if len(fields) != 5 or fields[0] != b':100644' or fields[1] != b'100644' or fields[4] != b'M' or not match:
            return full('Changes include source, unknown records, additions, removals or mode changes')
        paths.append(path)
        run_ids.add(match[1])
    if len(run_ids) != 1:
        return full('Closeout must concern exactly one run')
    run_id = next(iter(run_ids))
    result = {'mode': 'receipts', 'reason': 'Only existing regular records of one run changed',
              'run_id': run_id, 'paths': paths, 'base': base}
    if not validate:
        return result

    def blob(path, previous=False):
        return git(repo, 'show', f'{base}:{path}' if previous else (f':{path}' if staged else f'{target}:{path}'))

    directory = f'docs/agents/runs/{run_id}'
    try:
        # Even an unchanged companion must be a regular tracked blob.
        for filename in ('run.json', 'events.jsonl'):
            path = directory + '/' + filename
            for rev in (base, target):
                entry = git(repo, 'ls-files', '--stage', '--', path) if rev is None else git(repo, 'ls-tree', rev, '--', path)
                run_state.require(entry.startswith(b'100644 '), 'Expected both regular tracked record files')
        old = strict_json(blob(directory + '/run.json', True))
        current = strict_json(blob(directory + '/run.json'))
        run_state.validate(old)
        run_state.validate(current)
        run_state.require(current['run_id'] == old['run_id'] == run_id, 'Run identity changed')
        for field in ('repository', 'objective', 'orchestrator', 'contracts', 'gates'):
            run_state.require(current[field] == old[field], f'Closeout changed governing {field}')
        run_state.require(current['snapshot']['fingerprint'] == old['snapshot']['fingerprint'], 'Source fingerprint changed')
        run_state.require(current['snapshot']['head'] == base, 'Receipt does not identify the published primary commit')
        run_state.require(current['record_version'] >= old['record_version'], 'Record version regressed')
        run_state.require(current == old or current['record_version'] > old['record_version'], 'Changed run requires a new checkpoint version')
        run_state.require(bool(current['gates']), 'Closeout needs recorded source gates')
        for operation in old['operations']:
            if operation['status'] == 'confirmed':
                run_state.require(operation in current['operations'], 'Confirmed operation history was removed or changed')
        run_state.require(current['history'][:len(old['history'])] == old['history'], 'Checkpoint history was rewritten')
        run_state.require(all(g['status'] == 'passed' for g in current['gates'] if g['required']), 'Required gate incomplete')
        for kind in ('commit', 'push'):
            run_state.require(any(o['kind'] == kind and o['status'] == 'confirmed' and o['expected_revision'] == base
                                  for o in current['operations']), 'Primary commit and push must be confirmed')
        previous = blob(directory + '/events.jsonl', True)
        latest = blob(directory + '/events.jsonl')
        run_state.require(latest.startswith(previous), 'Event history was rewritten')
        # Previous history may legitimately contain the now-completed shipper.
        rows = previous.splitlines()
        run_state.require(not previous or previous.endswith(b'\n'), 'Truncated previous event history')
        run_events.validate_history([strict_json(row) for row in rows], run_id)
        event_list(latest, run_id)
        git(repo, 'diff', '--check', *(['--cached', base] if staged else [base, target]), '--')
    except subprocess.CalledProcessError as error:
        raise ValueError('Required record blob or whitespace validation failed') from error
    return result | {'validated': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', default='HEAD')
    parser.add_argument('--staged', action='store_true')
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--github-output', action='store_true', help='emit only the deterministic step output')
    args = parser.parse_args()
    try:
        result = check(args.project, args.base, args.head, staged=args.staged, validate=args.validate)
        if args.validate and result['mode'] != 'receipts':
            raise ValueError('Not a receipt-only closeout; run full checks')
        if args.github_output:
            print('receipts_only=' + str(result['mode'] == 'receipts').lower())
        else:
            print(json.dumps(result, indent=2))
    except (ValueError, OSError, UnicodeError, subprocess.CalledProcessError) as error:
        print(f'receipt validation: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
