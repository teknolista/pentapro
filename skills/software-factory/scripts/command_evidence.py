#!/usr/bin/env python3
"""Explicitly run argv once and publish a minimal, private evidence receipt.

Only invoke with a trusted command. Receipts contain hashes, not command arguments,
output, environment, or file names. An existing destination is never replaced.
"""
import argparse
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time

import run_state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--receipt', required=True, type=Path)
    parser.add_argument('--timeout', required=True, type=float)
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv[:1] == ['--'] else args.argv
    if not argv or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('provide a command and a finite positive timeout')
    repo = args.repo.resolve(strict=True)
    target = args.receipt.absolute()
    if target.name in ('', '.', '..') or not target.parent.is_dir():
        raise ValueError('receipt parent must be an existing directory')
    # Avoid redirecting a receipt through a symlinked directory.
    if target.parent.resolve(strict=True) != target.parent:
        raise ValueError('receipt parent must not contain symlinks')
    if os.path.lexists(target):
        raise FileExistsError('receipt already exists')
    snapshot = run_state.snapshot(repo)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    begin = time.monotonic()
    timed_out = False
    interrupted = None
    process = None
    signals = {signal.SIGINT, signal.SIGTERM}
    previous_handlers = {sig: signal.getsignal(sig) for sig in signals}

    def kill_group():
        if process is not None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    def cancel(signum, _frame):
        nonlocal interrupted
        if interrupted is None:
            interrupted = signum
        kill_group()

    for sig in signals:
        signal.signal(sig, cancel)
    try:
        # A signal during Popen is remembered even before its PID is available.
        try:
            process = subprocess.Popen(argv, cwd=repo, stdin=subprocess.DEVNULL,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                       start_new_session=True)
        except FileNotFoundError:
            code = 127
        except PermissionError:
            code = 126
        if interrupted is not None:
            kill_group()
        if process is not None:
            try:
                code = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                kill_group()
                process.wait()
                code = 124
            except BaseException:
                kill_group()
                process.wait()
                raise
        # After normal exit a cancellation can still reach surviving group members.
        if interrupted is not None:
            kill_group()
        # Complete one atomic publication before handling any newly pending signal.
        publication_mask = signal.pthread_sigmask(signal.SIG_BLOCK, signals)
        try:
            receipt = {'version': 1, 'started_at': started,
                       'duration_seconds': round(time.monotonic() - begin, 6),
                       'command': {'argument_count': len(argv),
                                   'argv_sha256': hashlib.sha256(json.dumps(argv, ensure_ascii=True, separators=(',', ':')).encode()).hexdigest()},
                       'exit_code': code, 'timed_out': timed_out,
                       'interruption_signal': interrupted, 'git': snapshot}
            fd, temp = tempfile.mkstemp(prefix='.command-evidence-', dir=target.parent)
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as out:
                    json.dump(receipt, out, indent=2)
                    out.write('\n')
                    out.flush()
                    os.fsync(out.fileno())
                os.link(temp, target, follow_symlinks=False)
            finally:
                os.unlink(temp)
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, publication_mask)
    except BaseException:
        kill_group()
        if process is not None:
            process.wait()
        raise
    finally:
        if process is not None and process.poll() is None:
            kill_group()
            process.wait()
        for sig, previous in previous_handlers.items():
            signal.signal(sig, previous)
        if interrupted is not None:
            # Preserve the wrapper's signal termination status for its caller.
            signal.signal(interrupted, signal.SIG_DFL)
            os.kill(os.getpid(), interrupted)
    return 128 - code if code < 0 else code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'command evidence: {error}', file=sys.stderr)
        sys.exit(2)
