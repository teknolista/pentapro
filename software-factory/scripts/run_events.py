"""Append and summarize sanitized factory invocation events for one existing run.

No host integration, telemetry, Git mutation, or execution of event content.
Capture and privacy depend on the invoking orchestrator and host.
"""
import argparse
from collections import Counter
from datetime import datetime
import json
import math
import os
from pathlib import Path
import stat
import subprocess

import run_state as state

BASE = {'schema_version', 'event_id', 'invocation_id', 'run_id', 'event_type', 'occurred_at'}
REQUEST = {'role', 'task_id', 'attempt', 'reason', 'expected_outcome', 'input_snapshot'}
OPTIONAL = {'model_requested', 'effort_requested', 'model_observed', 'effort_observed',
            'output_snapshot', 'parent_invocation_id', 'usage', 'evidence'}
TRANSITIONS = {
    'dispatch_requested': {'dispatched', 'dispatch_failed', 'cancelled'},
    'dispatched': {'completed', 'failed', 'cancelled', 'interrupted'},
    'completed': {'result_accepted', 'result_rejected'},
    'dispatch_failed': set(), 'cancelled': set(), 'failed': set(),
    'interrupted': set(), 'result_accepted': set(), 'result_rejected': set(),
}
OUTCOMES = {'dispatch_failed', 'completed', 'failed', 'cancelled', 'interrupted',
            'result_accepted', 'result_rejected'}
USAGE = {'input_tokens', 'output_tokens', 'cost_usd'}


def timestamp(value):
    state.require(isinstance(value, str), 'Timestamp must be a string')
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('Invalid ISO 8601 timestamp') from exc
    state.require(parsed.tzinfo is not None and parsed.utcoffset() is not None,
                  'Timestamp must include a UTC offset')
    return parsed


def identifier(value, name):
    state.require(isinstance(value, str) and state.IDENTIFIER.fullmatch(value),
                  'Invalid ' + name)


def validate_shape(event, run_id):
    state.require(isinstance(event, dict), 'Event must be an object')
    kind = event.get('event_type')
    state.require(kind in TRANSITIONS, 'Invalid event type')
    required = BASE | (REQUEST if kind == 'dispatch_requested' else set())
    if kind == 'dispatched':
        required |= {'agent_id'}
    if kind in OUTCOMES:
        required |= {'outcome'}
    state.require(required <= set(event) and set(event) <= required | OPTIONAL,
                  'Invalid event fields')
    state.require(type(event['schema_version']) is int and event['schema_version'] == 1,
                  'Unsupported event schema')
    state.require(event['run_id'] == run_id, 'Event run identity mismatch')
    for name in ('event_id', 'invocation_id', 'run_id'):
        identifier(event[name], name)
    timestamp(event['occurred_at'])
    if kind == 'dispatch_requested':
        for name in ('role', 'task_id', 'reason', 'expected_outcome'):
            state.require(state.text(event[name]), 'Invalid ' + name)
        state.require(type(event['attempt']) is int and event['attempt'] > 0, 'Invalid attempt')
        state.require(isinstance(event['input_snapshot'], str) and state.HASH.fullmatch(event['input_snapshot']),
                      'Invalid input snapshot')
    if kind == 'dispatched':
        state.require(state.text(event['agent_id']), 'Invalid observed agent identity')
    if kind in OUTCOMES:
        state.require(state.text(event['outcome']), 'Invalid outcome')
    if 'evidence' in event:
        state.require(isinstance(event['evidence'], list) and all(state.text(x) for x in event['evidence']),
                      'Evidence must be a list of locators')
    for name in ('model_requested', 'effort_requested', 'model_observed', 'effort_observed'):
        if name in event:
            state.require(event[name] is None or state.text(event[name]), 'Invalid ' + name)
    if 'parent_invocation_id' in event and event['parent_invocation_id'] is not None:
        identifier(event['parent_invocation_id'], 'parent invocation')
    if 'output_snapshot' in event and event['output_snapshot'] is not None:
        state.require(isinstance(event['output_snapshot'], str) and state.HASH.fullmatch(event['output_snapshot']),
                      'Invalid output snapshot')
    if 'usage' in event and event['usage'] is not None:
        usage = event['usage']
        state.require(isinstance(usage, dict) and set(usage) <= USAGE, 'Invalid usage fields')
        for key, value in usage.items():
            if value is not None:
                state.require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                              'Invalid usage value')
                if key != 'cost_usd':
                    state.require(type(value) is int, 'Token counts must be integers')


def validate_history(events, run_id):
    ids, invocations, attempts = {}, {}, {}
    for event in events:
        validate_shape(event, run_id)
        event_id, invocation = event['event_id'], event['invocation_id']
        state.require(event_id not in ids, 'Duplicate event ID in history')
        ids[event_id] = event
        kind = event['event_type']
        if invocation not in invocations:
            state.require(kind == 'dispatch_requested', 'Invocation must begin with dispatch_requested')
            task, attempt = event['task_id'], event['attempt']
            state.require(attempt == attempts.get(task, 0) + 1,
                          'Task attempts must increment from one for each new invocation')
            attempts[task] = attempt
            invocations[invocation] = []
        else:
            last = invocations[invocation][-1]
            state.require(kind in TRANSITIONS[last['event_type']], 'Invalid invocation transition')
            state.require(timestamp(event['occurred_at']) >= timestamp(last['occurred_at']),
                          'Invocation timestamps must not go backwards')
        invocations[invocation].append(event)
    return ids, invocations


def run_target(project, run_id):
    project = state.project_root(project)
    run_path = state.record_path(project, run_id)
    record = state.read_json(run_path)
    state.validate(record)  # A completed or in-progress record may have source drift.
    state.require(record['run_id'] == run_id and record['repository']['root'] == str(project),
                  'Record project/run identity mismatch')
    state.require(record['repository']['branch'] == state.branch(project),
                  'Branch changed; reconcile execution identity')
    return run_path


def read_events(path, run_id):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return []
    state.require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                  'Refusing symlink, hard-linked or non-regular event file')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        state.require(stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1 and
                      (opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino),
                      'Event file changed during inspection')
        data = stream.read()
    state.require(not data or data.endswith(b'\n'), 'Truncated event history; preserve and reconcile')
    events = []
    for line in data.splitlines():
        state.require(bool(line), 'Empty event history line')
        events.append(json.loads(line.decode('utf-8'), object_pairs_hook=state.unique_object,
                                 parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Invalid JSON number'))))
    validate_history(events, run_id)
    return events


def append(project, run_id, event):
    run_path = run_target(project, run_id)
    path = run_path.parent / 'events.jsonl'
    with state.locked(run_path):
        # Recheck identity after obtaining the lock.
        run_target(project, run_id)
        events = read_events(path, run_id)
        validate_shape(event, run_id)
        ids, _ = validate_history(events, run_id)
        if event['event_id'] in ids:
            state.require(ids[event['event_id']] == event, 'Conflicting duplicate event ID')
            return {'status': 'unchanged', 'event_id': event['event_id']}
        validate_history(events + [event], run_id)
        payload = (json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                              allow_nan=False) + '\n').encode('utf-8')
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, 'O_NOFOLLOW', 0)
        fd = os.open(path, flags, 0o600)
        try:
            info = os.fstat(fd)
            state.require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                          'Refusing non-regular or hard-linked event file')
            written = os.write(fd, payload)
            if written != len(payload):
                raise OSError('Partial append; preserve history and reconcile before retry')
            os.fsync(fd)
        finally:
            os.close(fd)
    return {'status': 'appended', 'event_id': event['event_id']}


def summary(project, run_id):
    run_path = run_target(project, run_id)
    with state.locked(run_path):
        events = read_events(run_path.parent / 'events.jsonl', run_id)
    _, invocations = validate_history(events, run_id)
    roles, outcomes = Counter(), Counter()
    items = []
    for invocation, series in invocations.items():
        request, last = series[0], series[-1]
        roles[request['role']] += 1
        status = last['event_type']
        outcomes[status] += 1
        dispatched = next((e for e in series if e['event_type'] == 'dispatched'), None)
        terminal = next((e for e in series if e['event_type'] in {'completed', 'failed', 'cancelled', 'interrupted'}), None)
        elapsed = ((timestamp(terminal['occurred_at']) - timestamp(dispatched['occurred_at'])).total_seconds()
                   if dispatched is not None and terminal is not None else None)
        usage_records = [e['usage'] for e in series if e.get('usage') is not None]
        usage = ({key: next((record[key] for record in reversed(usage_records)
                             if record.get(key) is not None), None)
                  for key in sorted(USAGE)} if usage_records else None)
        observed_model = next((e['model_observed'] for e in reversed(series) if e.get('model_observed') is not None), None)
        observed_effort = next((e['effort_observed'] for e in reversed(series) if e.get('effort_observed') is not None), None)
        items.append({'invocation_id': invocation, 'task_id': request['task_id'], 'role': request['role'],
                      'attempt': request['attempt'], 'status': status,
                      'open': status in {'dispatch_requested', 'dispatched'},
                      'agent_id': dispatched.get('agent_id') if dispatched else None,
                      'model_requested': request.get('model_requested'), 'effort_requested': request.get('effort_requested'),
                      'model_observed': observed_model, 'effort_observed': observed_effort,
                      'duration_seconds': elapsed, 'usage': usage})
    return {'run_id': run_id, 'invocation_count': len(items), 'roles': dict(roles),
            'outcomes': dict(outcomes), 'open_count': sum(item['open'] for item in items),
            'retry_count': sum(item['attempt'] > 1 for item in items),
            'project_wall_time_seconds': None, 'invocations': items}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['append', 'summary'])
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--input', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'append':
            state.require(args.input is not None, '--input required for append')
            event = state.read_json(args.input)
            result = append(args.project, args.run_id, event)
        else:
            state.require(args.input is None, '--input is only for append')
            result = summary(args.project, args.run_id)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, OSError, KeyError, TypeError, IndexError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'run-events error: {error}\n')


if __name__ == '__main__':
    main()
