# Engine I1 final independent re-review

- Invocation returned: `review-03`, resuming the same run/assignment after the parent reported a usage-limit boundary; preceding focused work was received as `review-02`.
- Run `engine-foundation`, saved record v7.
- HEAD/base: `5b39b1bd2c760a4d1c96bd9d05bd28f72dcec6ad`.
- Reviewed and recaptured working-tree fingerprint: `4e1d6e2b83dcee29bdcc6f4964ba7c80b616010df423117325dd430c8ed49ebc`.
- Verdict: **No blocking findings for I1 in the reviewed scope.** Both initial blockers are resolved. This is technical review, not developer acceptance or release authorization.

## Finding resolution

**REVIEW-01 resolved.** `src/native.rs:85–112` inspects each supplied root component before canonicalization. The corrected release binary rejected all four independently exercised variants: absolute intermediate symlink, absolute symlink-plus-parent traversal, relative intermediate symlink, relative symlink-plus-parent traversal. Each returned exit 1 with JSON `unsafe-path`, empty stdout, no outside specification files and no root lock effects. A real `real/../real` directory control succeeded and returned the contracted init envelope with 22 created files. The new regression test observes these properties through the actual binary, not a mocked guard.

**REVIEW-02 resolved.** `src/native.rs:122–133` separates ancestor-marker discovery from selected-directory validation. A nested ordinary `pentapro` file now permits successful ancestor discovery/list output; replacing the marker with a symlink still returns `unsafe-path`. The regression tests additionally retain explicit-root collision rejection. The fix does not relax the selected managed-directory or symlink-marker guards.

## Checks, coverage and evidence accounting

Source-inspected the correction to root resolution and three added real-binary regression tests, the implementation correction report, final PRODUCT/PROJECT/PRODUCTION/PROOF/PROCESS records and LL-009. Focused runtime checks used the rebuilt `target/release/pentapro` in disposable `/tmp` roots and passed the seven cases above. Fingerprint recapture matched the v7 input after these checks. This focused work began under review-02 and is retained at the identical current fingerprint for review-03; it is not represented as a second full-suite execution.

The prior review's coverage of unchanged command dispatch, exact native JSON ABI, ID grammar, preservation/preflight, lock/staging, archive identity guard, listing/show/validation, manifests/dependency footprint, README and CI remains applicable: the changed runtime path is root resolution, and this pass traced its effects on every command. Native compatibility commands remain explicitly unimplemented rather than successful stubs. Full Rust/collection suites are owned by the independent verifier and were not redundantly executed here. The final proof correctly separates implementer test evidence, correction RED/GREEN, first-review failures and pending final independent gates; PROCESS records execution without claiming developer acceptance. LL-009 states its local evidence, proposed generalization and hostile-writer limit. No source, index, events, run checkpoint or shared lessons were changed by this reviewer.

Limitations: Linux-only focused execution. No Windows/UNC/macOS native run, hostile simultaneous path replacement, fault-injected power-loss recovery, dependency advisory audit, hosted CI or full OpenSpec parity was established by this review. The component checks are static safeguards and cooperating locks, not race-free descriptor-relative filesystem containment. Earlier stale verifier-binary evidence is correctly excluded from corrected-code proof.

PDSA: targeted the two concrete counterexamples; inspected the narrow correction and new assertions; reran the actual failure/clean controls; confirmed no blocking regression in the affected scope. The initial review's proposed path-component lesson has been incorporated as LL-009; no additional new lesson identified. Actual model/effort attribution and usage are unavailable rather than inferred from configured profile values.
