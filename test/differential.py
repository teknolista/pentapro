#!/usr/bin/env python3
"""Compare a restricted Engine reader with a built, pinned OpenSpec CLI.

Usage: python3 test/differential.py ENGINE_BIN OPENSPEC_BIN NODE_BIN
All fixtures and environment state are temporary; no network is intended.
"""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PINNED_SHA = "f1cd852f4edce22b8df9548a4df889172ca8ff25"


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_hash(root):
    """Measure every relative path and regular file; reject ambiguous links."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlink in oracle build: {path}")
        if path.is_file():
            digest.update(str(path.relative_to(root)).encode("utf-8"))
            digest.update(b"\0")
            digest.update(bytes.fromhex(file_hash(path)))
        elif not path.is_dir():
            raise ValueError(f"non-regular oracle build path: {path}")
    return digest.hexdigest()


def preflight(argv, identity_env):
    if len(argv) != 4:
        raise ValueError("usage: differential.py ENGINE_BIN OPENSPEC_BIN NODE_BIN")
    engine_path, upstream_path, node_path = (Path(x).resolve(strict=True) for x in argv[1:])
    for path in (engine_path, upstream_path, node_path):
        if not path.is_file():
            raise ValueError(f"expected regular executable/file: {path}")
    # Resolve from the CLI itself, not the caller's cwd. Never fetch or rebuild.
    checkout = Path(subprocess.run(["git", "-C", str(upstream_path.parent), "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True, timeout=10, env=identity_env).stdout.strip()).resolve(strict=True)
    if upstream_path != checkout / "bin" / "openspec.js":
        raise ValueError("oracle must be the pinned checkout's bin/openspec.js")
    sha = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"], check=True, capture_output=True, text=True, timeout=10, env=identity_env).stdout.strip()
    if sha != PINNED_SHA:
        raise ValueError(f"upstream SHA mismatch: {sha}")
    dirty = subprocess.run(["git", "-C", str(checkout), "status", "--porcelain=v1", "--untracked-files=all"], check=True, capture_output=True, text=True, timeout=20, env=identity_env).stdout
    if dirty:
        raise ValueError("upstream tracked or untracked source changes present")
    build = checkout / "dist"
    if build.is_symlink() or not build.is_dir() or not (build / "cli" / "index.js").is_file():
        raise ValueError("built oracle dist/cli/index.js is missing or unsafe")
    node_version = subprocess.run([str(node_path), "--version"], check=True, capture_output=True, text=True, timeout=10, env=identity_env).stdout.strip()
    print(f"IDENTITY upstream_commit={sha} upstream_cli_sha256={file_hash(upstream_path)} dist_tree_sha256={tree_hash(build)} lock_sha256={file_hash(checkout / 'pnpm-lock.yaml')}", flush=True)
    print(f"IDENTITY node_path={node_path} node_version={node_version} node_sha256={file_hash(node_path)} engine_path={engine_path} engine_sha256={file_hash(engine_path)}", flush=True)
    print("NOTE: build hash measures bytes, not proof that dist was built from the checkout; runtime dependencies and environment are not authenticated.", flush=True)
    return str(engine_path), str(upstream_path), str(node_path)


try:
    with tempfile.TemporaryDirectory(prefix="pentapro-identity-") as identity_home:
        identity_env = dict(os.environ, HOME=identity_home,
                            XDG_CONFIG_HOME=str(Path(identity_home) / "config"),
                            XDG_DATA_HOME=str(Path(identity_home) / "data"),
                            GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        engine, upstream, node = preflight(sys.argv, identity_env)
except (ValueError, OSError, subprocess.SubprocessError) as exc:
    print(f"oracle identity preflight failed: {exc}", file=sys.stderr)
    sys.exit(2)
with tempfile.TemporaryDirectory(prefix="pentapro-diff-") as tmp:
    import shutil

    root = Path(tmp)
    sides = []
    for name in ("reference", "engine"):
        base = root / name
        project = base / "project"
        home = base / "home"
        project.mkdir(parents=True)
        home.mkdir()
        sides.append((base, project, home))

    def env_for(home):
        return dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(home / "config"),
                    XDG_DATA_HOME=str(home / "data"), XDG_CACHE_HOME=str(home / "cache"),
                    DO_NOT_TRACK="1", OPENSPEC_TELEMETRY="0", OPENSPEC_NO_UPDATE_CHECK="1",
                    NO_COLOR="1", CI="1", TERM="dumb")

    def snapshot(base):
        # Include file bytes and link targets, but do not follow directory links.
        return {str(p.relative_to(base)): ("link:" + os.readlink(p) if p.is_symlink()
                else hashlib.sha256(p.read_bytes()).hexdigest())
                for p in base.rglob("*") if p.is_symlink() or p.is_file()}

    def compare(args, cwd="."):
        observations = []
        for idx, (base, project, home) in enumerate(sides):
            before = [snapshot(side[0]) for side in sides]
            prefix = [node, upstream] if idx == 0 else [engine, "compat", "openspec"]
            result = subprocess.run([*prefix, *args], cwd=project / cwd,
                                    env=env_for(home), capture_output=True, timeout=20,
                                    stdin=subprocess.DEVNULL)
            assert [snapshot(side[0]) for side in sides] == before, (args, "persistent file changes")
            # The two fixture trees are equivalent but have different parent paths.
            # Normalize only the containing temporary fixture root, retaining the
            # project/home/outside suffixes and all other exact bytes.
            observations.append((result.returncode,
                                 result.stdout.replace(os.fsencode(base), b"<ROOT>"),
                                 result.stderr.replace(os.fsencode(base), b"<ROOT>")))
        assert observations[0] == observations[1], (args, *observations)
        print("PASS", " ".join(args))
        return observations[1]

    def reset():
        for base, project, home in sides:
            shutil.rmtree(project)
            project.mkdir()
            shutil.rmtree(home)
            home.mkdir()
            for child in (base / "external-dir", base / "outside.md"):
                if child.is_dir():
                    shutil.rmtree(child)
                elif child.exists() or child.is_symlink():
                    child.unlink()

    def each(fn):
        for base, project, home in sides:
            fn(base, project, home)

    def put(project, name, data):
        folder = project / "openspec" / "specs" / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "spec.md").write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))

    compare(["list", "--specs", "--json"])
    compare(["show", "missing", "--type", "spec", "--json"])
    doc = b'\xef\xbb\xbf# X\r\n## Purpose\r\nInvalid \xff text\r\n## Requirements\r\n```\r\n### Fake\r\n```\r\n### Requirement: Real ###\r\n**ID**: A\r\nText\r\n#### Scenario: Here ###\r\nBody\r\n'
    each(lambda b, p, h: put(p, "alpha", doc))
    each(lambda b, p, h: (p / "nested").mkdir())
    for args in (["list", "--specs"], ["list", "--specs", "--json"], ["show", "alpha", "--type", "spec"], ["show", "alpha", "--type", "spec", "--json"], ["show", "missing", "--type", "spec", "--json"], ["show", "../alpha", "--type", "spec", "--json"]):
        compare(args)
    compare(["list", "--specs", "--json"], cwd="nested")
    for text in ("\ufeffHello\ufeff", "\u0085Hello\u0085"):
        each(lambda b, p, h: put(p, "alpha", "# X\n## Purpose\n" + text + "\n## Requirements\n### Requirement: A\nBody\n"))
        compare(["show", "alpha", "--type", "spec", "--json"])
    prefix = "# Alpha\n\n## Purpose\n\nPurpose text\n\n## Requirements\n\n"
    for sep in ("\u2028", "\u2029"):
        for suffix in ("### Requirement: A" + sep + "B\nBody\n", "### Requirement: A" + sep + "\nBody\n", "```foo" + sep + "`\n### Requirement: Hidden\nBody\n```\n"):
            each(lambda b, p, h: put(p, "alpha", prefix + suffix))
            compare(["show", "alpha", "--type", "spec", "--json"])
    each(lambda b, p, h: put(p, "alpha", prefix + "### Requirement: Normal\nBody\n"))
    compare(["show", "alpha", "--type", "spec", "--json"])
    each(lambda b, p, h: put(p, "alpha", b"# Missing purpose\n"))
    compare(["list", "--specs", "--json"])
    compare(["show", "alpha", "--type", "spec", "--json"])
    for malformed in ("# X\n## Purpose\n\n## Requirements\n", "# X\n## Purpose\nHere\n"):
        each(lambda b, p, h: put(p, "alpha", malformed))
        listed = compare(["list", "--specs", "--json"])
        shown = compare(["show", "alpha", "--type", "spec", "--json"])
        assert listed[0] == 0 and b'"requirementCount": 0' in listed[1] and shown[0] == 1

    reset()
    each(lambda b, p, h: put(p, "platform/session", prefix + "### Requirement: Nested\nBody\n"))
    listed = compare(["list", "--specs", "--json"])
    assert listed[0] == 0 and b'"id": "platform/session"' in listed[1]
    shown = compare(["show", "platform/session", "--type", "spec", "--json"])
    assert shown[0] == 0 and b"Nested" in shown[1]

    if hasattr(os, "symlink"):
        reset()
        def external_regular(base, project, home):
            specs = project / "openspec/specs"
            specs.mkdir(parents=True)
            external = base / "external-dir"
            external.mkdir()
            (external / "spec.md").write_text(prefix + "### Requirement: External\nBody\n", encoding="utf-8")
            (specs / "linked").symlink_to(external, target_is_directory=True)
        each(external_regular)
        listed = compare(["list", "--specs", "--json"])
        assert listed[0] == 0 and b'"id": "linked"' not in listed[1]
        for args in (["show", "linked", "--type", "spec"], ["show", "linked", "--type", "spec", "--json"]):
            result = compare(args)
            assert result[0] == 0 and b"External" in result[1]

        # External capability directory with final file link back to project docs:
        # upstream denies it because the file link's parent is outside specs.
        def external_backlink(base, project, home):
            external = base / "external-dir"
            (external / "spec.md").unlink()
            docs = project / "docs"
            docs.mkdir()
            (docs / "spec.md").write_text(prefix + "### Requirement: Docs\nBody\n", encoding="utf-8")
            (external / "spec.md").symlink_to(docs / "spec.md")
        each(external_backlink)
        for args in (["show", "linked", "--type", "spec"], ["show", "linked", "--type", "spec", "--json"]):
            result = compare(args)
            assert result[0] == 1 and b"Path is outside the allowed directory: <ROOT>/project/openspec/specs/linked" in result[1] + result[2]

        reset()
        def internal_links(base, project, home):
            put(project, "real", prefix + "### Requirement: Internal\nBody\n")
            specs = project / "openspec/specs"
            (specs / "alias").symlink_to("real", target_is_directory=True)
            (specs / "filelink").mkdir()
            (specs / "filelink/spec.md").symlink_to("../real/spec.md")
            docs = project / "docs"
            docs.mkdir()
            (docs / "spec.md").write_text(prefix + "### Requirement: Docs\nBody\n", encoding="utf-8")
            (specs / "doclink").mkdir()
            (specs / "doclink/spec.md").symlink_to("../../../docs/spec.md")
        each(internal_links)
        # Same-depth IDs are supported; linked directory is excluded from list.
        listed = compare(["list", "--specs", "--json"])
        assert listed[0] == 0 and b'"id": "alias"' not in listed[1]
        for ident in ("real", "alias", "filelink", "doclink"):
            for args in (["show", ident, "--type", "spec"], ["show", ident, "--type", "spec", "--json"]):
                result = compare(args)
                assert result[0] == 0 and (b"Internal" in result[1] or b"Docs" in result[1])

        reset()
        def dangling(base, project, home):
            put(project, "alpha", prefix + "### Requirement: Normal\nBody\n")
            broken = project / "openspec/specs/broken"
            broken.mkdir()
            (broken / "spec.md").symlink_to("missing.md")
        each(dangling)
        compare(["show", "broken", "--type", "spec", "--json"])
        def external_file(base, project, home):
            outside = base / "outside.md"
            outside.write_text("external")
            folder = project / "openspec/specs/outside"
            folder.mkdir()
            (folder / "spec.md").symlink_to(outside)
        each(external_file)
        compare(["list", "--specs", "--json"])
        compare(["show", "alpha", "--type", "spec", "--json"])

    # Mixed-depth IDs are a documented conservative Engine refusal, not parity.
    reset()
    def mixed_depth(base, project, home):
        put(project, "alpha", prefix + "### Requirement: A\nBody\n")
        put(project, "nested/session", prefix + "### Requirement: B\nBody\n")
    each(mixed_depth)
    base, project, home = sides[1]
    before = [snapshot(side[0]) for side in sides]
    result = subprocess.run([engine, "compat", "openspec", "list", "--specs", "--json"],
                            cwd=project, env=env_for(home), capture_output=True, timeout=20,
                            stdin=subprocess.DEVNULL)
    assert result.returncode == 2 and not result.stdout and b"unsupported spec identifier ordering" in result.stderr
    assert [snapshot(side[0]) for side in sides] == before
    print("PASS intentional mixed-depth refusal")
