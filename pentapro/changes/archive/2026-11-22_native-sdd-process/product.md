# PRODUCT — native change behavior

Status: preserved specification of the accepted, completed change, approved on 2026-11-22. The consolidated current baseline is maintained separately in root PRODUCT.

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

Other 19 domain skills retain their prior scoped behavior. No numerical quality, cost or universal-readiness guarantee is introduced.
