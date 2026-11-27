# Independent focused I2 rereview — review-i2-04

- Run: `engine-openspec-read`, record v15.
- Tested source fingerprint: `09f59c1940f0eb08f658c9b02a99054afa5a85b153bb644830a8bfd089385d47`; HEAD/base remains `d17b923bf0c274334f0fbe1812ecefd567367fa2`.
- Verdict: **No blocking findings in the focused corrected I2 scope.** This review is not developer acceptance or full OpenSpec parity certification.

## Resolution and direct evidence

I2-REVIEW-03 is fixed. `src/compat.rs` now first accepts a canonical final file within canonical specs or its selected capability directory. The project-local final-file-symlink fallback checks that its canonical containing directory is within canonical specs. If the capability directory itself resolves outside specs and its final file links back into project/docs, the command now returns the pinned capability-directory diagnostic rather than a successful read.

Built the actual corrected source with `CARGO_TARGET_DIR=/tmp/i2-review-final-target cargo build --locked --offline` (passed). Independently replayed `/tmp/i2-review-link-probe.py` against that fresh binary: Engine and pinned OpenSpec both returned exit 1, identical stdout `show_error` JSON and empty stderr for the composed-link case. Captured output: `/tmp/i2-review-last-link-output.json`.

Ran the current repository differential runner against the fresh Engine and pinned built OpenSpec with stable Node 26.10.0:

`python3 test/differential.py /tmp/i2-review-final-target/debug/pentapro /tmp/pentapro-openspec-reference/bin/openspec.js /home/dever/.nvm/versions/node/v26.10.0/bin/node`

Result: **43 exact reference comparisons plus one intentional mixed-depth refusal passed**, receipt `/tmp/i2-review-last-differential.log`. This directly covers composed-link text/JSON denial and positive controls for external capability regular files, internal directory links, contained file links and project-doc file links; list exclusion of directory links, lexical traversal, dangling/external-file errors, parser Unicode corrections, nested ID/CWD and malformed parser errors also passed. Positive link controls assert status and sentinel content, not merely equality.

Prior parser and identity-harness findings remain resolved in examined code. U+2028/U+2029 capture handling and regression tests are retained. The runner verifies the source SHA and clean checkout, emits Node/build/binary identities, and clearly states measured build hashes do not authenticate build-from-source provenance. Wrong-SHA refusal was independently observed in review-i2-03 and its preflight code is unchanged; that observation was not rerun in this pass.

## Harness isolation and scope

Reference and Engine now run in separate equivalent temporary project/home trees; each invocation uses its own HOME/XDG and closed stdin. Snapshots check both fixture trees before/after each process without following directory links; external fixture targets are inside the monitored temporary side. Only each side's randomized temporary base path is normalized in stdout/stderr, preserving project/home/outside suffixes, channels, status and other output bytes. No download/build/model call is introduced by the runner, which requires explicit already-built reference paths. Directory-only/transient changes and unmonitored external effects remain outside snapshot proof.

The clarified PRODUCT I2-005 and PROJECT explicitly state the external capability-directory trust exception and its composed-link restriction; the regression and implementation now agree with the pinned source. Static checks do not provide an adversarial race-free sandbox, and untrusted projects may direct explicit reads to external capability files as documented. No new source mutation or process/network execution was found in the production reader.

Read-only review: no source/index/run/events/lesson edits. Only the mandatory local prompt-log append and requested /tmp fixtures/reports were written. The parallel verifier owns full Cargo/collection suites; this pass did not repeat them. Whole-tree fingerprint was recaptured after tests and is unchanged.

## PDSA / limits

Plan: recheck the composed trust-boundary correction, its allowed controls and harness isolation. Do: inspect source/contract/tests, build fresh binary, replay the exact former failure and expanded differential suite. Study: prior mismatch now matches the oracle; controls continue succeeding and intentional unsupported behavior remains distinct. Act: return the corrected snapshot for orchestration; no source fix required.

No additional new lesson identified beyond the previously returned composition-of-links candidate. Linux/Node 26 observations only; exhaustive parser, other OS/locale, permission combinations, hostile concurrent replacement and full upstream functional parity remain unverified. Requested role model/effort are configuration; independent runtime attribution, token usage and cost remain unknown.
