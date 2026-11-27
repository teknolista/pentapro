# Focused I2 specification rereview — spec-i2-05

- Run: `engine-openspec-read`, record v15.
- Snapshot independently checked: `09f59c1940f0eb08f658c9b02a99054afa5a85b153bb644830a8bfd089385d47`; HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`.
- Outcome: **PASS for the focused composed-symlink contract correction**. No remaining blocking finding in this assigned specification scope. Implementation, differential coverage, independent verification/review and developer result acceptance remain separate pending gates.

## Disposition of SPEC-LINK-01

Resolved. PRODUCT I2-005 (`product.md:28`) now states the missing canonical parent-containment prerequisite for the project-file fallback, explicitly rejects an external capability directory whose `spec.md` links back into project/docs, and requires the pinned capability-directory diagnostic and text/JSON error behavior. PROJECT (`project.md:5`) preserves the ordered `assertDiscoveredSpecFile` / `assertLinkedSpecFileInProject` source contract, including checking the file-link parent within the specs root before the project-target fallback. This matches pinned `src/utils/spec-path-containment.ts:83–88,113–130`.

PROOF (`proof.md:11,25`) now requires the two-link negative fixture, text and JSON stdout/stderr/exit comparison, capability-directory error path, and no writes to project or outside target. It retains ordinary external-directory/regular-file success and internal/contained/dangling/traversal controls. PROCESS (`process.md:20`) records the finding and independently reviewed correction requirement rather than claiming acceptance.

The reconstructed read journey is coherent: select a supported lexical capability ID, apply the pinned ordered physical containment checks, allow a file within the explicitly selected capability trust root (including an external directory), apply the narrower project-file-link fallback only when its parent satisfies the source prerequisite, then output content without writing. The separate external-read disclosure and absence of a sandbox guarantee remain explicit. The correction preserves the user-requested upstream compatibility and does not authorize writes or weaken native Engine boundaries.

## Checks, limitations and PDSA

Read the four corrected documents, the previous focused report, the pinned containment owner and current run identity; independently recaptured the source fingerprint, which matches record v15. This was a read-only specification rereview, not a new full-suite or runtime verification. The prior synthetic reproduction remains evidence for why the correction was needed; it is not restamped as a post-fix run. Other agents must prove the actual implementation now produces the documented result. No project source, index, run/events or lessons edits; only required prompt logging and this requested `/tmp` report.

PDSA: planned a focused follow-up against SPEC-LINK-01, compared the saved correction with the exact source ordering and observable scenario, confirmed the missing prerequisite and negative control are now present, and returned the scoped readiness result. **No new lesson identified.** Configured model/effort do not independently establish runtime attribution; usage/cost unknown.
