#!/usr/bin/env python3
"""Run a bounded synthetic report-to-PTY journey and a seeded negative control."""
import argparse
import errno
import fcntl
import json
import os
from pathlib import Path
import pty
import re
import select
import signal
import shutil
import struct
import subprocess
import sys
import tempfile
import termios
import time

FIXTURE = Path(__file__).resolve().parent / 'fixtures' / 'terminal-journey'
APP = FIXTURE / 'app.py'
EXPECTED = {'selected': 'Gamma', 'amount': '2.35', 'total': '3.65'}
ANSI = re.compile(rb'\x1b(?:\[[0-?]*[ -/]*[@-~]|.)')


def check_report(result):
    if result.returncode != 0 or result.stderr or ANSI.search(result.stdout):
        raise AssertionError('report must succeed with clean stdout and empty stderr')
    try:
        value = json.loads(result.stdout)
    except (ValueError, UnicodeDecodeError) as exc:
        raise AssertionError('report is not valid JSON') from exc
    if value != EXPECTED:
        raise AssertionError(f'incorrect report: {value!r}')


def check_view(output, columns, lines):
    if ANSI.search(output):
        raise AssertionError('unexpected terminal controls')
    text = output.decode('ascii').replace('\r\n', '\n')
    rows = text.splitlines()
    if len(rows) > lines or any(len(row) > columns for row in rows):
        raise AssertionError('output exceeds viewport bounds')
    if not rows or rows[0] != f'Report {columns}x{lines}':
        raise AssertionError('program did not observe the expected PTY size')
    if rows.count('> Gamma: 2.35 USD') != 1:
        raise AssertionError('selected Gamma row and its amount are not visible together')
    if 'Name / amount (USD)' not in rows:
        raise AssertionError('amount context is missing')


def render(path, columns, lines, seeded=False, timeout=5):
    master, slave = pty.openpty()
    try:
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', lines, columns, 0, 0))
        command = [sys.executable, str(APP), 'view', str(path)]
        if seeded:
            command.append('--seed-defect')
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=slave, stderr=subprocess.PIPE, start_new_session=True)
        os.close(slave)
        slave = -1
        chunks = []
        deadline = time.monotonic() + timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not select.select([master], [], [], remaining)[0]:
                    raise TimeoutError('view timed out')
                try:
                    block = os.read(master, 4096)
                except OSError as exc:
                    if exc.errno == errno.EIO:  # Linux PTY closes with EIO.
                        break
                    raise
                if not block:
                    break
                chunks.append(block)
                if sum(map(len, chunks)) > 65536:
                    raise AssertionError('view output exceeds limit')
            _, stderr = process.communicate(timeout=max(0.01, deadline - time.monotonic()))
        except BaseException:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate(timeout=5)
            raise
        if process.returncode != 0 or stderr:
            raise AssertionError(f'view failed: status={process.returncode}, stderr={stderr!r}')
        return b''.join(chunks)
    finally:
        os.close(master)
        if slave != -1:
            os.close(slave)


def run(seeded=False):
    with tempfile.TemporaryDirectory(prefix='factory-journey-') as temp:
        path = Path(temp) / 'input.json'
        shutil.copyfile(FIXTURE / 'input.json', path)
        command = [sys.executable, str(APP), 'report', str(path)]
        result = subprocess.run(command, capture_output=True, timeout=5)
        check_report(result)
        for columns, lines in ((80, 24), (40, 12)):
            check_view(render(path, columns, lines, seeded), columns, lines)
        path.write_text('{"items":[{"name":"Gamma","amount":"not-a-number"}]}', encoding='utf-8')
        invalid = subprocess.run(command, capture_output=True, timeout=5)
        if invalid.returncode == 0 or invalid.stdout or not invalid.stderr.startswith(b'invalid input:') or ANSI.search(invalid.stderr):
            raise AssertionError('malformed input must fail cleanly on stderr')
        shutil.copyfile(FIXTURE / 'input.json', path)
        check_report(subprocess.run(command, capture_output=True, timeout=5))
        check_view(render(path, 40, 12), 40, 12)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed-defect', action='store_true', help='expect this negative control to fail')
    args = parser.parse_args()
    try:
        run(args.seed_defect)
    except (AssertionError, OSError, subprocess.SubprocessError, UnicodeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print('PASS: report, PTY views, malformed input and recovery')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
