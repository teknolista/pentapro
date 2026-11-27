# PRODUCT — native SDD behavior

Status: accepted scoped collection baseline, 2026-11-22. Source acceptance: the owner approved the reviewed migration result with “sim, prossiga” after the consolidation/archive/commit/normal-push scope was presented.

The collection supports a five-dimensional specification and an agent-guided change lifecycle. The 24 skill packages remain reusable independently; the native factory coordinates requested end-to-end work without requiring a prompt for every stage. Exploration-only and narrower requests retain their scope.

## Requirements and scenarios

| ID | Change intent | Observable contract and acceptance scenario |
| --- | --- | --- |
| REQ-SDD-1 / SC-SDD-1 | Add | Given a new or existing project, when setup prepares native tooling, active changes belong under pentapro/changes and archive is a separate subdirectory; no fake active change or accepted baseline is created. |
| REQ-SDD-2 / SC-SDD-2 | Modify | Given an outcome request, the host main session clarifies scope and dispatches specification review, implementation, verification and review without requiring a prompt for each skill; exploration-only requests stop within scope. |
| REQ-SDD-3 / SC-SDD-3 | Add | Every active change has change.md and product/project/production/proof/process.md, explicit stable IDs and baseline/unchanged links; names use two or three lowercase hyphen-separated words and do not collide with history. |
| REQ-SDD-4 / SC-SDD-4 | Modify | Before final result approval, root pillar scaffolds stay Pending and existing baseline facts stay unchanged; tasks and evidence record current work inside the change. |
| REQ-SDD-5 / SC-SDD-5 | Add | When the developer explicitly accepts the reviewed result after its scope is presented, consolidation/archive/commit/normal push proceed by default; silence and process-policy approval do not count. Separate/local-only directions prevail. |
| REQ-SDD-6 / SC-SDD-6 | Add | On negative feedback or changed baseline, affected contract/review/test evidence is re-evaluated before closure; prior passing evidence is not relabeled for changed software. |
| REQ-SDD-7 / SC-SDD-7 | Add | After accepted reconciliation across affected dimensions, the change moves to archive/YYYY-MM-DD_name with local date, preserved unaffected requirements/scenarios and repaired links; a collision never overwrites content. |
| REQ-SDD-8 / SC-SDD-8 | Add | On cancellation, record partial effects and recovery; do not promote abandoned intent or automatically revert source; unresolved effects keep archival pending and archived disposition remains cancelled. |
| REQ-SDD-9 / SC-SDD-9 | Remove | Active setup, role instructions, runner and current guides require no separate SDD executable or configurable schema; historical records and permitted attribution remain identifiable as such. |
| REQ-SDD-10 / SC-SDD-10 | Preserve | Host model/effort choices, read-only review boundaries, privacy/prompt rules, independent grading and safe package export continue; a template/model label is not runtime evidence. |

The [completed change](../changes/archive/2026-11-22_native-sdd-process/product.md) retains the original change-intent context. The requirements/scenario IDs above are preserved as the accepted scoped baseline; later work must preserve unaffected behavior.


## Engine I1 — accepted 2026-11-26

Requirements ENG-001–005, ENG-027 and ENG-028 for the bounded first increment are implemented by the local Rust `pentapro` CLI: native initialization, change creation/list/show and structural validation with human/JSON output. See the [accepted contract](../changes/archive/2026-11-26_engine-foundation/product.md) for exact behavior and scenarios. Validation is structural, not human acceptance. Full OpenSpec compatibility and additional deterministic factory capabilities remain pending future increments; the linked inventories are research, not evidence of delivered behavior.


## OpenSpec read compatibility I2 — accepted 2026-11-27

The Engine provides the limited read-only `compat openspec list --specs [--json]` and `compat openspec show ID --type spec [--json]` forms, with explicit refusals for unsupported commands, root configurations, identifier ordering and operating systems as defined in the [accepted contract](../changes/archive/2026-11-27_openspec-reading/product.md). It does not implement OpenSpec validation or full parity. In the explicitly documented compatibility behavior, a selected capability directory symlink may expose an external `spec.md`; the composed final-file link fallback has additional containment requirements.
