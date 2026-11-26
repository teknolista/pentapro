# Engine I1 independent code review

- Invocation: `review-01`; run `engine-foundation`, record v5.
- Base/HEAD: `5b39b1bd2c760a4d1c96bd9d05bd28f72dcec6ad`.
- Reviewed working-tree fingerprint: `b763856543d87f0e306b909719218a90d64eacc4535c16939e1f5d58d4e12809`, recaptured unchanged after review.
- Verdict: **Changes requested**. Two confirmed I1 root-resolution defects; no publication or result acceptance implied.

## REVIEW-01 · P1 · Reject intermediate symlinks before canonicalizing an explicit root

Location: `src/native.rs:80–91` (`root`); introduced in new Engine code.

Trigger: an existing `/tmp/example/alias` symlink points to `/tmp/example/outside`, which has real child directory `child`. Run `pentapro --root /tmp/example/alias/child --json init`.

Expected: fail with `unsafe-path` before creating specification files, per PRODUCT S05 and the explicit contract that canonicalization must not silently authorize a symlink root, and PROJECT ADR-006 (reject unsafe components before resolution).

Observed against the actual `target/debug/pentapro`: exit 0 and all 22 artifacts were created in `outside/child/pentapro`. `safe_dir` applies symlink_metadata only to the final `child` path component; canonicalize then erases the intermediate symlink. No adversarial concurrent filesystem writer is required, so the documented hostile-concurrent-writer limitation does not cover this case.

Impact: the declared static root safety boundary is bypassed for every command, including mutations. The existing test covers only an explicit root whose final component itself is a symlink and misses this case.

Correction: resolve the requested path component by component from an established absolute anchor, inspecting symlink metadata before following each component (including relative and `..` paths); fail on any forbidden component before canonicalize/lock/mutation. Keep Windows prefixes/roots correctly represented rather than assuming POSIX-only syntax.

Regression: intermediate symlink roots in absolute and relative paths must produce `unsafe-path` and leave both target and selected workspace unchanged; retain clean real-directory controls and existing final-component tests. Native Windows/UNC behavior needs a separate platform test, not an unsupported claim.

## REVIEW-02 · P2 · Skip ordinary files while looking for an ancestor specification directory

Location: `src/native.rs:101–103` (`root`); introduced in new Engine code.

Trigger: initialize a real root, then create `root/nested/pentapro` as an ordinary file. From `root/nested`, run `pentapro --json list` without --root. An especially relevant instance is running the repository's executable from `target/debug`, which itself contains an ordinary file named `pentapro`.

Expected: find the nearest ancestor containing a `pentapro/` directory, as PRODUCT ENG-004/S03 promises. An ordinary file is not that directory marker.

Observed with a fresh temporary root and real CLI: exit 1 and `unsafe-path`, `Expected a real directory: .../nested/pentapro`; the valid ancestor is never examined. `safe_dir` intentionally treats non-directories as errors, so it cannot also serve as the marker-discovery predicate.

Impact: the promised nested-directory journey fails in otherwise valid projects with an ordinary file named after the executable, including an ordinary build directory. Current nested-root tests only use `pentapro/product` and do not exercise marker collisions.

Correction: distinguish candidate-marker discovery from validation of a selected managed directory: ignore ordinary non-directory candidate markers and keep walking ancestors; retain explicit unsafe handling for symlink markers and validation of the selected root.

Regression: nested ordinary `pentapro` file plus a valid ancestor must discover/list that ancestor; no-marker roots still return project-not-found, and explicit root/managed-path collision rejection must remain intact.

## Coverage and actual checks

Read new main/native/manifest code, all eight integration tests, Cargo manifest and lock metadata, Rust CI workflow, additive README/.gitignore edits, governing change PRODUCT/PROJECT/PRODUCTION/PROOF/PROCESS and related review policies/lessons. Assessed command dispatch, JSON/error handling, ID grammar, init preservation/preflight, staged creation/cooperating lock, archived-name guard, listing/show/validation, dependency footprint and CI coexistence. No other substantiated blocker found in this coverage.

Executed only two focused real-binary reproducers in disposable `/tmp` roots, plus source fingerprint recapture; no full Rust/collection suite repeated because the independent verifier owns those checks. Did not modify repository source/index, run/event records or lessons; only mandatory append-only prompt logging and this requested `/tmp` report. No Windows/macOS execution, hostile-writer sandbox validation, fault-injected power-loss recovery, full OpenSpec parity, dependency advisory audit or hosted CI run established by this review.

PDSA: planned against the reviewed I1 contract; traced root/path and filesystem effects; tested concrete static counterexamples; returned two bounded corrections and regression expectations to the owning implementer. No source fix performed. Relevant lesson principle: LL-008 distinguishes individually promised failure properties; current safety tests verify final symlink components but not traversal through an intermediate component.

Lesson candidate (English, proposed): Validate the whole user-supplied filesystem path before canonicalization when the contract forbids symlinks. Evidence is REVIEW-01 on this exact fingerprint; cause confirmed locally (leaf-only metadata check), correction untested until implemented. Pair a final-component symlink test with intermediate, relative and clean-path controls. Applicability: statically symlink-rejecting project writers; it does not establish race-free hostile filesystem containment. Next check: rerun the reproducer and focused regression tests after the fix.

Requested model/effort are configured by factory_reviewer profile; observed attribution/usage unavailable, not inferred. Return retains invocation ID review-01.
