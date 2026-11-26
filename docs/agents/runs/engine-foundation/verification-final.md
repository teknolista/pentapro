# Independent final verification — engine-foundation / verify-03

Result: PASS for the bounded I1 criteria exercised; complete OpenSpec parity remains pending. Snapshot independently measured `4e1d6e2b83dcee29bdcc6f4964ba7c80b616010df423117325dd430c8ed49ebc`, HEAD `5b39b1bd2c760a4d1c96bd9d05bd28f72dcec6ad`; run v8 at resumption. Linux, Rust/Cargo 1.100.0. Runtime model/effort/usage observations unavailable.

## Direct checks on this snapshot

- `cargo fmt --check`: passed.
- `CARGO_TARGET_DIR=/tmp/pentapro-verify-final cargo clippy --locked --offline --all-targets -- -D warnings`: passed.
- `CARGO_TARGET_DIR=/tmp/pentapro-verify-final cargo test --locked --offline`: 11 binary integration tests passed, 0 failed; no unit tests defined.
- `cargo build --release --locked --offline`: passed; repository `target/release/pentapro --version` reported `pentapro 0.1.0`.
- Real release binary, isolated projects: init/new/list/show/validate succeeded; empty required file produced `empty-file` and exit 1, restoration succeeded, sentinel AGENTS.md preserved, invalid `../escape` rejected. `/tmp/engine-corrected-journey.py`.
- Independently invoked real release binary on absolute and relative `alias/child` and `alias/../alias/child` roots: all rejected with `unsafe-path` and no external `pentapro` creation. REVIEW01 reproduced before fix, corrected now for these static cases.
- Ancestor discovery with an ordinary file named `pentapro` in a nested directory correctly found the initialized ancestor; REVIEW02 corrected. Suite also checks symlink-marker refusal.
- Collection `validate_collection.py`: 352 Markdown files, 1395 links/anchors, 26 version checks, 0 issues; `run_skill_evals.py --check-cases`: 20 cases passed; `package_plugin.py --check`: passed; `git diff --check`: passed (tracked diff only).
- Compared 269 tracked collection/plugin source files against `/tmp/engine-protected-hashes.json`: no differences. Verifier made no source/index changes. Release target was built as requested.

## Coverage and limitations

ENG-001–005, ENG-027/028 mapped to S01–S06 through real binary integration tests and the independent temporary-root journey; checks cover structure and specified failure cases, not semantic readiness. Path controls were verified against static symlinks; adversarial simultaneous replacement and power-loss behavior are not established. No Windows/macOS tests, hosted CI, full OpenSpec differential/parity validation, interactive accessibility, security certification or controlled performance comparison was performed. The collection hashes do not prove live host discovery. Git diff --check excludes untracked file contents. Earlier report `/tmp/engine-verification.md` applies solely to the earlier failing snapshot.

PDSA: planned targeted regression and full local checks; executed against fixed snapshot; studied actual outputs and verified prior observed defects no longer reproduce in tested scenarios; no source corrections required. Relevant LL-009 is supported only within the local static-path scope. No new lesson identified.
