# Independent verification — engine-foundation / verify-01

Snapshot: run.json v5 fingerprint `b763856543d87f0e306b909719218a90d64eacc4535c16939e1f5d58d4e12809`, HEAD `5b39b1bd2c760a4d1c96bd9d05bd28f72dcec6ad`. Fingerprint independently measured before and after checks. Linux, rustc 1.100.0, cargo 1.100.0. Requested role factory_verifier; observed model/effort/usage unknown.

## Result: FAIL — ENG-027/S05

`--root /tmp/<case>/alias/child --json init`, where `alias` is a symlink to a different existing directory containing `child`, returns 0 and creates `pentapro` below the symlink target. `src/native.rs` root() tests only the final root path using `symlink_metadata` and then canonicalizes it; an intermediate symlink is followed. This violates the contract's root symlink prohibition and permits initialization outside the path as presented to the user. Reproduced with an isolated temp directory, no external data affected. Coordinate with REVIEW01; no source fix made. Test all relevant root components and rerun affected/full checks on the new snapshot.

## Executed now

- `cargo fmt --check`: passed.
- `CARGO_TARGET_DIR=/tmp/pentapro-verify-target cargo clippy --locked --offline --all-targets -- -D warnings`: passed.
- `CARGO_TARGET_DIR=/tmp/pentapro-verify-target cargo test --locked --offline`: 8 integration tests passed, 0 unit tests, 0 failed; these are actual executable invocations in isolated roots.
- `cargo build --release --locked --offline`: passed; `target/release/pentapro --version` reports `pentapro 0.1.0`; `--help` displayed 5 subcommands and options. Build output only under ignored target/.
- Independent temp-root real CLI task: `init` created 22 files, `new`, `list`, `show`, `validate`, whitespace corruption produced `empty-file` and exit 1, restoration passed; sentinel AGENTS.md preserved; `../escape` was rejected with `invalid-name`. Script `/tmp/verify-engine-journey.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_collection.py`: 348 Markdown files, 1388 links/anchors, 26 version checks, 0 issues.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_skill_evals.py --check-cases`: 20 cases passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/package_plugin.py --check`: passed.
- `git diff --check`: passed; checked unstaged tracked diff, does not cover untracked source.
- 269 source/plugin files listed in `/tmp/engine-protected-hashes.json` were unchanged. No Git index mutation was performed by verifier.

## Criteria and coverage

ENG-001 real help/version, JSON, exit handling exercised by tests; no comparison with OpenSpec implied. ENG-002 S01 init/repeat/preservation exercised. ENG-003 S02 success, concurrent same-name, duplicate/archived IDs exercised. ENG-004 S03 nested and explicit root, sorting and show exercised in suite. ENG-005 S04 empty/missing, diagnostics and recovery exercised; structural check cannot assert semantic readiness. ENG-027 S05 invalid IDs/direct symlink/collision tests passed but intermediate symlink root fails as above. ENG-028 S06 no model/network invocation observed in tested flows; source inspection supports no subprocess/network in native.rs but does not prove a security property. Collection preservation source hashes passed; no full plugin discovery or actual model execution performed.

Not exercised: Windows/macOS, power-loss, hostile concurrent file replacement, actual upstream differential parity, multi-user filesystem privileges, full accessibility/interactive UX, source/performance/security certification. Checks reflect the pre-correction snapshot only.

## PDSA

Plan: test fixed snapshot, real entry point, invalid and preservation paths. Do: executed listed checks independently. Study: routine suite passed but exploratory ancestor symlink boundary exposed a substantive contract violation independently confirming reviewer. Act: reported to orchestrator; no unauthorized source edits. Relevant LL-001: use offline cached dependencies and temp target; no sandbox failure occurred. Candidate lesson (proposed, not persisted): use a nested symlink component fixture in path containment tests; final-component symlink checks alone do not establish containment. Applicability: local CLI paths; not proof against adversarial racing. Next verify after fix on exact new fingerprint.
