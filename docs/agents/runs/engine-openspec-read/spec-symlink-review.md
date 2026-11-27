# Focused I2 specification review — spec-i2-04

- Run: `engine-openspec-read`, input record v13.
- Snapshot independently checked: `08a7c16af990d2a0d60d1a318f09c7d77e0720b5994124bde76c37dc08a1a015`; HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`.
- Outcome: **BLOCK for one residual normative link-rule mismatch**. The earlier broad ambiguity about an explicitly selected external capability directory is now resolved: PRODUCT I2-005 clearly permits the outside read, states stdout/context confidentiality consequences, distinguishes it from a sandbox, and links a meaningful no-write test. The user's requested upstream compatibility supports that declared read-only behavior; the rule does not authorize writes or waive host permissions. Its project-root fallback detail is still too broad.

## SPEC-LINK-01 — project fallback requires a contained parent

`pentapro/changes/openspec-reading/product.md:28` says that for an external linked capability directory the final file may resolve within that directory **or within the project** under the pinned file-link rule. That second alternative omits the parent containment prerequisite in pinned `src/utils/spec-path-containment.ts:83–88`: the directory holding the final file link must itself resolve within the specs root before project fallback is allowed.

Concrete synthetic fixture: `<project>/openspec/specs/alpha` is a directory symlink to `<outside>/`; `<outside>/spec.md` is a file symlink back to `<project>/docs/spec.md`. The final file is in the project, but it is not within the selected external capability trust root, and its parent is outside the specs root.

Executed `/tmp/i2-spec-link-probe.py` with Node 26.10.0 and pinned OpenSpec v2.2.0, and `/tmp/i2-correct-target/debug/pentapro` from the corrected candidate. Captured exact results in `/tmp/i2-spec-link-probe-results.json`:

- OpenSpec: exit 1, empty stderr, JSON stdout `status[0].code = show_error`, message `Path is outside the allowed directory: <PROJECT>/openspec/specs/alpha`.
- Engine: exit 0 and JSON with the synthetic project document's contents.

The expected Engine success is consistent with the overbroad sentence, but contradicts the stated pinned reference behavior. This is a real contract error and associated implementation mismatch, not a hypothetical confidentiality warning.

### Minimal correction and verification

Clarify I2-005: an explicitly selected capability directory may be an external link, and a final file resolving inside that canonical capability root is permitted. The fallback allowing a final file link elsewhere within the project is permitted only when the file-link parent is canonically within the specs root, as required by the pinned helper. Thus an external capability link whose file links back to project/docs must be rejected with the upstream capability-directory path diagnostic. Preserve the ordinary external-directory/regular-file success case and contained project-file-link controls.

Add this two-link composition to PROOF alongside the existing sentinel test. Run both text and JSON for the composed denial and existing success controls, compare stdout/stderr/exit and no-write snapshots; align implementation rather than silently declare a new divergence. No new developer decision or broad additional research is needed for this source-backed correction.

## Review coverage and limits

Read PRODUCT, PROJECT, PROOF, PROCESS, prior verification V2, PentaPRO review procedure, PDSA protocol and relevant LL-009. Compared the exact pinned containment helpers and current Rust behavior. Reconstructed journey: trusted project selection → explicit lexical ID → capability trust root → final file-link containment → read-only output, with external regular-file success and composed-link denial. No product-source, index, run/events or shared lessons changes; only mandatory prompt logging and this requested /tmp report. No full suite, full parser review, Windows or hostile concurrent path replacement assessment performed in this focused specification role. Other independent gates still own implementation evidence.

PDSA: planned a narrow consistency check; inspected the documented trust chain and pinned owner; found and reproduced the missing prerequisite with synthetic data; routed the minimal correction and regression scenario to the orchestrator. **No new lesson identified.** Requested role settings are configured values; independently observed model/effort, usage and cost are unknown.
