# I2 focused independent rereview — review-i2-03

- Run: engine-openspec-read, record v13. Tested fingerprint `08a7c16af990d2a0d60d1a318f09c7d77e0720b5994124bde76c37dc08a1a015`; HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`.
- Verdict: **Changes requested** for the newly confirmed composed-symlink case below. Prior two findings are resolved within tested scope.

## Resolved prior findings

I2-REVIEW-01: source now reproduces ECMAScript U+2028/U+2029 heading and fence-info capture boundaries. Fresh binary built directly from reviewed source with `CARGO_TARGET_DIR=/tmp/i2-review-final-target cargo build --locked --offline` passed. Replayed three earlier counterexamples plus ASCII control: exact exit/stdout/stderr matched pinned OpenSpec/Node 26.10.0. The committed integration regression covers both separators at interior/trailing heading positions and fence info; the differential runner includes these controls.

I2-REVIEW-02: runner now checks exact pinned commit, checkout entrypoint, clean source and existing built output; prints measured CLI/dist/lock/Engine/Node identities and Node version. Ran full current differential runner: 23 calls passed with identity receipt `/tmp/i2-review-final-differential.log`. A fresh unrelated Git oracle fixture was refused with exit 2, empty stdout and `upstream SHA mismatch` before any comparisons. This establishes the requested reference preflight; its explicit note correctly avoids claiming build bytes are authenticated as derived from source.

## I2-REVIEW-03 — P2, blocking: project fallback incorrectly authorizes a file escaping an external capability-directory trust root

- Location: `src/compat.rs:381–385`, especially `&& !file_real.starts_with(project)`.
- Trigger: `<project>/openspec/specs/alpha` is a directory link to `<temporary>/external`; that external directory's `spec.md` is itself a file link back to `<project>/docs/spec.md`. All content is synthetic; project root/config meet the supported preflight.
- Expected: pinned OpenSpec refuses the composed path with exit 1 and JSON `show_error`, message `Path is outside the allowed directory: <project>/openspec/specs/alpha` (or equivalent human error). The external capability directory is a distinct trust root; a file link leaving it does not get unconditional access to the original project.
- Actual: Engine returns exit 0 and the project/docs document as a parsed successful spec. The boolean permits any final file inside the project even when the capability-directory parent canonicalizes outside the specs root.
- Evidence: independently replayed the spec reviewer's fixture against this rereview's fresh binary: `/tmp/i2-review-link-probe.py`, outputs `/tmp/i2-review-link-results.json`; original repro `/tmp/i2-spec-link-probe.py`. Reference and Engine used the same isolated temporary project/home, stable Node 26 and pinned OpenSpec.
- Source rationale: `assertDiscoveredSpecFile()` in pinned `src/utils/spec-path-containment.ts` first tries the specs root, then a lexically-addressed capability directory as its own trust root. Its fallback `assertLinkedSpecFileInProject()` additionally asserts that the file's containing directory is reached from within the specs root before allowing a project-local file target. Rust's single `parent_real OR project` condition omits that parent-containment guard and produces a success forbidden by the reviewed exact-link contract (PRODUCT I2-005).
- Correction: port the complete containment/fallback sequencing, including checking the capability directory before permitting a project-local linked spec. Preserve ordinary internal spec-file links, direct external capability-directory files and lexical-ID rejection. Regression: the composed directory-link + file-link case must fail with exact channel/status/diagnostic while all three allowed controls continue matching upstream. Include text and JSON forms.

## Coverage / PDSA

Reviewed corrected parser and identity harness, added tests and clarified directory-link trust contract; inspected pinned containment source. No blocker is asserted against direct external directory-link reads now explicitly allowed in PRODUCT/PROJECT; they are not a physical-root sandbox. Static TOCTOU defense and non-Linux remain outside proof.

Only the mandatory local prompt log and requested /tmp reports/fixtures were written. No source/index/run/event changes. Parallel verifier owns full suite checks, which this review did not repeat. Fresh build plus full 23-case differential and focused identity/Unicode/link probes ran directly. Snapshot rechecked unchanged before report.

Plan/Do/Study/Act: rereview prior corrections, replay exact regressions, inspect composed trust boundaries, reproduce the new mismatch and route it to the orchestrator. No new persisted lesson; candidate prevention: test compositions of individually permitted link types rather than only each type independently. Local cause confirmed; broader prevention remains proposed. Requested role model/effort are host configuration; independent runtime attribution and usage remain unknown.
