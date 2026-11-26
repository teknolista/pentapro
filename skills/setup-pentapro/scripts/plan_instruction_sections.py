#!/usr/bin/env python3
"""Plan canonical instruction sections to stdout; never write a project file."""
import argparse
import hashlib
import os
import re
from pathlib import Path
import stat
import subprocess
import sys

MANIFESTO = '## Software Excellence Manifesto — Powered by PentaPRO'
LOGGING = '## Prompt Logging'
TEMPLATE = Path(__file__).resolve().parent.parent / 'assets/agents.md'


def template_section(text, start, end):
    return text[text.index(start + '\n'):text.index(end + '\n')].rstrip('\n')


def instruction_headings(text):
    """Locate exact mandatory headings and reject fenced/commented examples."""
    positions = {}
    fence = None
    comment = False
    offset = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip('\r\n')
        if content in (MANIFESTO, LOGGING):
            if fence is not None or comment:
                raise ValueError('mandatory section appears in example/comment context; review required')
            positions.setdefault(content, []).append(offset)
        if fence is not None:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(fence[1]) + r',}[ \t]*', content):
                fence = None
        elif not comment and (match := re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', content)) and (match[1][0] != '`' or '`' not in match[2]):
            fence = (match[1][0], len(match[1]))
        else:
            remaining = content
            while remaining:
                if comment:
                    _, end, remaining = remaining.partition('-->')
                    if not end:
                        break
                    comment = False
                else:
                    _, start, remaining = remaining.partition('<!--')
                    if not start:
                        break
                    comment = True
        offset += len(line)
    return positions


def plan(root, expected=None):
    root = Path(os.path.abspath(root))
    if root.resolve(strict=True) != root or not root.is_dir():
        raise ValueError('root must be an existing directory without symlink components')
    result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                            capture_output=True, check=False)
    if result.returncode or Path(os.fsdecode(result.stdout).strip()).resolve() != root:
        raise ValueError('root must be the Git repository root')
    target = root / 'AGENTS.md'
    try:
        fd = os.open(target, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        old = b''
    except OSError as error:
        raise ValueError('unsafe instruction target') from error
    else:
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise ValueError('unsafe instruction target')
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                old = stream.read()
            after = os.fstat(fd)
            if (info.st_ino, info.st_size, info.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
                raise ValueError('instruction target changed while reading')
        finally:
            os.close(fd)
    if expected is not None and hashlib.sha256(old).hexdigest() != expected:
        raise ValueError('instruction target does not match expected SHA-256')
    current = old.decode('utf-8')
    template = TEMPLATE.read_text(encoding='utf-8')
    sections = [template_section(template, MANIFESTO, '## Instruction setup and scope'),
                template_section(template, LOGGING, '## Project Facts and Navigation')]
    headings = instruction_headings(current)
    missing = []
    for heading, section in zip((MANIFESTO, LOGGING), sections):
        locations = headings.get(heading, [])
        count = len(locations)
        if count > 1:
            raise ValueError('duplicate mandatory section')
        if count == 1:
            if not current.startswith(section, locations[0]):
                raise ValueError('customized mandatory section needs review')
        else:
            missing.append(section)
    if not missing:
        return old
    prefix = '\n\n'.join(missing) + '\n\n'
    return prefix.encode('utf-8') + old


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--expected-sha256', help='reject a changed original; SHA-256 of empty bytes for a missing file')
    args = parser.parse_args()
    try:
        sys.stdout.buffer.write(plan(args.root, args.expected_sha256))
    except (OSError, UnicodeError, ValueError) as error:
        print(f'section plan: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
