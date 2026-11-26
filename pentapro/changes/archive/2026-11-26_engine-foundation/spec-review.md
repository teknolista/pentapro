# Independent specification review · engine-foundation

Invocation: spec-01. Input record v2; supplied fingerprint c57af679dd4c08785add8f4db60165b159163935e8f2b4001b68ea59399d56f0. Read-only source review on 2026-11-26. Runtime/model/effort and usage independently observed: unknown. No product acceptance is granted.

Verdict: **BLOCK pending two bounded I1 contract corrections**. Scope division, fixed OpenSpec target, coexistence protections and first vertical slice are otherwise suitable for starting I1. Full product remains required; I1 is not a parity release.

## Required corrections before I1 code

1. **SPEC-01 — Define initialization artifact ownership and exact outputs.** `product.md:44` promises a generic native scaffold; `project.md` names only pillar directories. Existing canonical initializer `skills/penta-pro/scripts/init_pentapro.py:ARTIFACTS` creates topic files (5 product, 4 project, 3 production, 3 proof, 3 process), assets and indexes, and requires a Git repository root. Specify the exact I1 file manifest and template semantics (ideally reuse this canonical inventory), and state explicitly whether Engine accepts non-Git empty directories, as S01 currently implies. Otherwise the implementer must invent a different scaffold/Git policy while both are described as native. Tests must cover exact outputs plus existing-file preservation.

2. **SPEC-02 — Finish the promised version-1 JSON contract.** `product.md:42` defines only an outer envelope; `data`, error envelope and validation diagnostics remain undefined for init/new/list/show/validate. Before implementation define each command's keys/types, deterministic ordering, path representation, `show` content, validation-failure payload/stdout/stderr behavior and stable error identifiers. Keep the documented clap help/usage-error exception. Tests should assert these contracts against the actual CLI, including no project, duplicate/unsafe change and missing/empty artifact. This avoids publishing an arbitrary machine interface that the stated version implies is a contract.

Both can be settled by the orchestrator within existing authority; no new developer decision is required. Re-review the concrete additions, not the entire unchanged evidence inventory.

## Full-target traceability correction

3. **SPEC-03 — Preserve original PP IDs and elevate inventory-only capabilities.** The factory inventory asks to retain PP-01–PP-26 or map them explicitly. PRODUCT ENG-001–028 does not yet map those IDs. The input inventory is labeled evidence, not normative product requirements, so D25 (RED/GREEN timeline), D30 (resource/time/context budgets and content/policy/version cache invalidation), D35 (cross-project authority), D37 (controlled experiments), D38 (production runner/deploy/rollback authority), and D39 (versioned extension/runner contracts) are not clearly required by current ENG rows. Add explicit requirements or a normative adoption/traceability table from PP/D IDs to ENG IDs and roadmap increments. Similarly make configured model/effort/fallback constraints explicit rather than treating profile diagnostics as the whole PP-09 requirement. This affects later increments, not the native filesystem implementation algorithm.

## Scope/evidence limitation

OpenSpec inventory recovers the command surface but explicitly says it is not an exhaustive atomic behavior/fixture catalog. Describe this as complete target requirements and a source recovery inventory; do not claim that all detailed behavioral specification or parity proof has finished. Detailed later-increment specifications and oracle tests remain gates before their implementation. The developer's requested full final scope is retained; no exclusion can be inferred from first-increment delivery.

## Checks actually performed

Read six governing dimension/index files, technology assessment and linked inventories; inspected existing initializer ARTIFACTS and Git-root checks; compared original PP-09/13/16/18/19/22/25/26 with current ENG/D inventory; read PDSA and relevant LL-005/006/007/008. No executable Engine exists at review, so no runtime, benchmark, differential, cross-platform or security assertion was tested. Source/index unchanged except mandatory append-only prompt capture; this report is in /tmp only.

## PDSA

Plan: review user outcome, I1 observable contract and complete-target traceability. Do: compare saved contract with canonical initializer and prior requirements. Study: found two interface decisions an implementer would otherwise invent, plus inventory-to-requirement mapping gaps. Act: return scoped corrections to orchestrator and rereview additions. No new lesson identified beyond existing caller/owner and journey-completeness guidance.
