#!/usr/bin/env python3
"""Small synthetic report/view fixture; not a full terminal application."""
import argparse
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
import re
import sys


def load_items(path):
    try:
        raw = Path(path).read_bytes()
        if len(raw) > 65536:
            raise ValueError('input exceeds 65536 bytes')
        payload = json.loads(raw)
        if not isinstance(payload, dict) or set(payload) != {'items'} or not isinstance(payload['items'], list):
            raise ValueError('expected an items list')
        if not 1 <= len(payload['items']) <= 100:
            raise ValueError('expected 1 to 100 items')
        items = []
        seen = set()
        for row in payload['items']:
            if not isinstance(row, dict) or set(row) != {'name', 'amount'}:
                raise ValueError('each item requires name and amount')
            name, amount = row['name'], row['amount']
            if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9 -]{0,19}', name) or name in seen:
                raise ValueError('invalid or duplicate item name')
            if not isinstance(amount, str) or not re.fullmatch(r'(?:0|[1-9][0-9]{0,7})\.[0-9]{2}', amount):
                raise ValueError('amount must be a nonnegative decimal with two places')
            seen.add(name)
            items.append((name, Decimal(amount)))
        return items
    except OSError as exc:
        raise ValueError('invalid input: cannot read file') from exc
    except (UnicodeError, json.JSONDecodeError, InvalidOperation, ValueError, RecursionError) as exc:
        raise ValueError('invalid input: malformed data or values') from exc


def main():
    parser = argparse.ArgumentParser(description='Synthetic terminal report')
    parser.add_argument('mode', choices=['report', 'view'])
    parser.add_argument('input')
    parser.add_argument('--selected', default='Gamma')
    parser.add_argument('--seed-defect', action='store_true', help='intentionally clip the selected row')
    args = parser.parse_args()
    try:
        items = load_items(args.input)
        selected = next((row for row in items if row[0] == args.selected), None)
        if selected is None:
            raise ValueError('selected item not found')
        if args.mode == 'report':
            print(json.dumps({'selected': selected[0], 'amount': str(selected[1]),
                              'total': str(sum((v for _, v in items), Decimal('0.00')))}, separators=(',', ':')))
        else:
            if not sys.stdout.isatty():
                raise ValueError('view requires a terminal')
            size = os.get_terminal_size(sys.stdout.fileno())
            if size.columns < 20 or size.lines < 4:
                raise ValueError('terminal too small (minimum 20x4)')
            lines = [f'Report {size.columns}x{size.lines}', 'Name / amount (USD)']
            rows = [f'{">" if name == selected[0] else " "} {name}: {amount} USD' for name, amount in items]
            if args.seed_defect:
                # Mimics a selected item placed below the clipped content viewport.
                rows = [line for line in rows if not line.startswith('>')]
                rows += [' filler'] * size.lines + [f'> {selected[0]}: {selected[1]} USD']
            lines.extend(rows)
            for line in lines[:size.lines]:
                print(line[:size.columns])
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
