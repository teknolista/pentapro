# I2 final reconciliation verification — verify-i2-06

Outcome: PASS for checks exercised on the current integrated snapshot; developer acceptance is separate. Run `engine-openspec-read`, invocation `verify-i2-06`, source fingerprint `bcc12d2a4fefc6fa009286f9acdb1bc58d7caa45c7bdaa17413d65dd8369f3ad`, HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`. Source snapshot and index were unchanged across checks. Host model/effort and usage were not independently observed.

## Direct checks — Linux, Rust/Cargo 1.100.0

- `cargo fmt --check`: passed.
- `CARGO_TARGET_DIR=/tmp/i2-verify-resume3 cargo clippy --locked --offline --all-targets -- -D warnings`: passed.
- `CARGO_TARGET_DIR=/tmp/i2-verify-resume3 cargo test --locked --offline`: passed, 23 binary integration tests (12 CLI/native, 11 compatibility).
- `CARGO_TARGET_DIR=/tmp/i2-verify-resume3 cargo build --locked --offline`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 test/differential.py /tmp/i2-verify-resume3/debug/pentapro /tmp/pentapro-openspec-reference/bin/openspec.js /home/dever/.nvm/versions/node/v26.10.0/bin/node`: passed 43 reference comparisons and one intentional mixed-depth refusal. The runner confirmed pinned clean upstream SHA `f1cd852f4edce22b8df9548a4df889172ca8ff25`, Node 26.10.0, and measured Engine SHA-256 `26ff46897f381c644dee58bc8ae3b07cc9af8c12c1dc829d74f0aece117cd5d3`. It uses separate temp project/HOME trees. Identity hashes measure bytes, not authenticated build provenance.
- Collection checks: validator 383 Markdown files, 1457 local links/anchors, 26 version checks, zero issues; 20 evaluation cases; package metadata check; `git diff --check`: all passed.
- `sha256sum --check /tmp/i2-reconciled-source-hashes.txt`: all ten Rust source, test, Cargo manifest/lock entries passed. The freshly built Engine binary hash also matches previous independent verification. This supports reuse of prior report and mode-0111 evidence for unchanged code, not a proof that unrelated environment inputs stayed identical.
- `git diff --cached --name-only` returned empty; the three additional untracked `docs/1-...`, `docs/2-...`, `docs/3-...` files are outside this task and remain untouched. Their presence is included in the whole-tree fingerprint and collection validation but their contents were not evaluated as I2 requirements.

## Existing evidence and scope

[verification-final.md](verification-final.md) and [eacces-followup.md](eacces-followup.md) are inherited evidence for previous snapshot `09f59c1940f0eb08f658c9b02a99054afa5a85b153bb644830a8bfd089385d47`: earlier independently executed mode-0111 EACCES matched OpenSpec in text/JSON for list/show on Linux UID 1000. I inspected the receipts, the reconciliation text, and unchanged code/test checksums; I did not rerun the permission-specific fixture in this invocation. Current product and process records reference that evidence and do not present it as new execution.

This establishes only exercised I2 Linux behaviors, not complete OpenSpec parity, exhaustive parser equivalence, other OS or permission scenarios, hostile concurrent path replacement safety, absence of transient or out-of-fixture writes, Node 24 behavior, hosted CI, acceptance, or publication. The user-visible external-directory symlink behavior remains explicitly documented.

PDSA: planned focused snapshot/evidence checks using LL-009/010/011; ran isolated Rust, collection, and executable differential checks; compared outputs and recorded bounded limitations. No corrective source edits and no new lesson identified.
