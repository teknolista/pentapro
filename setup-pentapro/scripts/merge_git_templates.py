"""Merge bundled Git defaults into an explicitly selected repository root.

Only .gitignore and .gitattributes are written. Existing bytes and rule order
are preserved after missing defaults, so project-specific rules keep precedence.
No Git index changes, renormalization, installation, or network operations.
"""
import argparse
from pathlib import Path
import stat
import subprocess
import tempfile


ASSETS = Path(__file__).resolve().parents[1] / "assets"


def merged_content(template: bytes, existing: bytes | None) -> bytes:
    if existing is None:
        return template
    # Decode strictly rather than corrupting an unknown encoding. Preserve a BOM
    # and existing CRLF/LF bytes; compare complete lines without their terminators.
    bom = b"\xef\xbb\xbf" if existing.startswith(b"\xef\xbb\xbf") else b""
    body = existing[len(bom):]
    seen = set(body.decode("utf-8").splitlines())
    missing = []
    for line in template.decode("utf-8").splitlines():
        if line and line not in seen:
            missing.append(line)
            seen.add(line)
    if not missing:
        return existing
    newline = b"\r\n" if b"\r\n" in body else b"\n"
    prefix = newline.join(line.encode("utf-8") for line in missing) + newline
    return bom + prefix + (newline if body else b"") + body


def snapshot(path: Path) -> bytes | None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError(f"Refusing symlink, hard-linked or non-regular target: {path}")
    return path.read_bytes()


def merge_templates(root: Path) -> list[str]:
    root = root.resolve(strict=True)
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"], text=True
    ).strip()
    if Path(actual).resolve() != root:
        raise ValueError("Select the repository root, not a subdirectory")
    changes = []
    for name in ("gitignore", "gitattributes"):
        target = root / ("." + name)
        before = snapshot(target)
        after = merged_content((ASSETS / name).read_bytes(), before)
        changes.append((target, before, after))
    outcomes = []
    for target, before, after in changes:
        if snapshot(target) != before:
            raise ValueError(f"Target changed during merge; inspect and rerun: {target}")
        if after == before:
            outcomes.append(f"unchanged {target.name}")
            continue
        if before is None:
            with target.open("xb") as output:
                output.write(after)
        else:
            # Stage the complete replacement before touching the existing file.
            # A failed write must not truncate the project's current rules.
            staged = None
            try:
                with tempfile.NamedTemporaryFile(dir=root, delete=False) as output:
                    staged = Path(output.name)
                    output.write(after)
                staged.chmod(stat.S_IMODE(target.stat().st_mode))
                if snapshot(target) != before:
                    raise ValueError(f"Target changed during merge; inspect and rerun: {target}")
                staged.replace(target)
            finally:
                if staged is not None:
                    staged.unlink(missing_ok=True)
        outcomes.append(f"{'created' if before is None else 'merged'} {target.name}")
    return outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Actual target Git repository root")
    args = parser.parse_args()
    try:
        for result in merge_templates(args.root):
            print(result)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
