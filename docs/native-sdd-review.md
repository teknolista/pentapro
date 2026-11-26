# Native SDD maintenance review — 2026-11-22

## Result and reviewed scope

The native migration is implemented locally and accepted by the developer on 2026-11-22 and locally consolidated/archived. Independent review reported no blocking findings after rechecking the corrections; final handoff freshness is recorded in the checkpoint. Local archive is complete; the separate run record owns commit/push receipts. Under the new default, explicit acceptance of this reviewed result will authorize consolidation, archival, commit and normal push for this change, unless the developer asks for separate/local-only steps. Approval of that policy was not acceptance of the implementation.

Source change: [native-sdd-process](../pentapro/changes/archive/2026-11-22_native-sdd-process/change.md). Decision provenance: [transition contract](native-sdd-contract.md). Execution record: [checkpoint](agents/runs/native-sdd-process/run.json). The record is bookkeeping, not proof that referenced checks ran.

The review covers the 24-skill source inventory, changed specification/delivery/setup/orchestration/UI contracts, six required change files, six-host specialist adapters, local project copies, package generation/export, evaluation runner/fixtures, maintenance helpers and current adoption instructions. The 19 unchanged domain skills retain their existing scoped behavior; they were not rewritten to claim higher quality without a concrete defect. References were inspected by dependency/risk; historical Markdown/PDF evidence was retained rather than represented as current runtime guidance. This is not a page-by-page new PDF audit or a full external API revalidation.

## Changed behavior and defects corrected

- Active work lives in pentapro/changes/name using change.md and the five dimension files; root pillars are the consolidated baseline, not a draft destination.
- The host main session guides exploration and delegates the existing six specialists. No new model tier, command surface or configurable schema is introduced.
- One explicit reviewed-result approval covers closure/publication by default. Explicit separate approvals and narrower authority prevail; cancelled intent, unresolved partial effects and archival location are not collapsed into accepted software.
- Closure compares baseline, accepted change and actual effects, preserves unaffected IDs/scenarios, fixes links after the extra archive level and handles collisions/interruption without overwrites or blind replay.
- Setup and installed role copies use native contracts, preserve prompt rules/PDSA/models and customized work, and require no external SDD executable. Retired local workflow packages were moved outside active discovery into a temporary backup; prior empty planning scaffolds remain dated history. No global tools were uninstalled.
- Native evaluator fixtures replace the command-dependent case, preserve independent receipt/grader isolation and test correct/incorrect task/evidence changes. Historical trial results retain their original meaning.
- The collection validator now excludes deleted tracked files from the working-tree candidate while still reporting links to them and dangling symlinks. Two regressions distinguish a valid retirement from a broken incoming link.
- Independent review found baseline destination drift in UI authoring/example/prompt and generic project guidance, plus discovery resume paths; these were corrected to active-change ownership. Verification also found mandatory-initializer wording; creation now has a safe ordinary-file fallback and the existing helper remains optional.

## Executable inventory and test judgment

Separate test files per module are not required when observable coverage is indirect. Counts are not line/branch coverage; fixtures and tests do not need recursive tests of tests. No new SDD runtime utility or archive script was introduced.

| Maintained executable | Coverage and remaining boundary |
| --- | --- |
| scripts/validate_collection.py | Dedicated invalid/valid metadata, portability, links and candidate-deletion tests; all current candidate resources validated. |
| scripts/package_plugin.py | Dedicated four-host exports, resource/license retention, metadata drift, preservation/unsafe paths and reproducibility controls; optional local native discovery checks where installed. |
| scripts/run_skill_evals.py, eval_outcomes.py, eval_isolation.py | Runner suite covers native fixture/task/proof/source-scope controls and actual independent graders; separate mount/socket/resource probe passes. |
| evals/check_receipts.py | Clean/seeded/misleading-result controls in runner tests; synthetic application grading, not a production guarantee. |
| evals/check_mcp_sdk.py | Optional assertion-based in-process protocol smoke, itself a check; not run because SDK dependencies are absent. No extra unit file is required, but SDK compatibility remains unverified here. |
| skills/software-factory/scripts/run_state.py | Dedicated record identity, stale evidence/writer, locks, interrupted effects and preservation controls. Optional bookkeeping, not semantic specification validation. |
| skills/penta-pro/scripts/init_pentapro.py | 14 tests cover output structure, rerun preservation and unsafe path controls. Optional bootstrap only; does not archive, accept or implement a change. |
| skills/ui-design-web/scripts/prototype_tools.py | 26 dedicated regressions for bounded inputs, fragment/contrast handling and exports; browser/native accessibility remains separate. |
| skills/pr-quiz/scripts/publish_quiz.py and assets/pr-quiz.yml | 15 Python tests and 27 actual embedded-handler scenarios with API doubles; live permission/event behavior remains separate. |
| Legacy prompt logger core/CLI | 16 Node tests for formatting/redaction/safe append and CLI; legacy opt-in material is not current mechanical capture enforcement. |
| Legacy prompt logger host adapter | Core behavior covered indirectly; actual installed-host API remains untested and explicitly legacy. |
| plugin/opencode.mjs | Four offline loading/registration/disposal/API/path controls; native runtime success is not inferred from them. |

No maintained runtime helper lacking either direct/indirect coverage or an explicit optional/legacy boundary was identified. Test effectiveness was assessed through existing negative controls; no exhaustive coverage claim follows.

## Executed checks

Environment: Python 3.12.6, Node 27.0.0-alpha.0.0.0; CI specifies Python 3.12 and Node 24. No global dependencies, hooks or permission policies were installed.

- 75 root Python tests, 14 initializer tests, 26 UI helper tests and 15 quiz publisher tests passed: 130 total.
- 27 quiz-handler scenarios, 16 logger tests and four adapter controls passed: 47 Node controls. Logger CLI tests used scoped permission escalation to avoid the known host subprocess restriction.
- Package metadata freshness, four export/resource checks, 15 evaluation-case definitions and whitespace checks passed.
- Independent mount/socket/resource isolation probes passed without inference or real services.
- Collection validation: 242 Markdown files, 1010 local links/anchors, 24 version checks, zero issues at the pre-handoff documentation snapshot. Final checkpoint records any later relevant rerun.

Python commands used PYTHONDONTWRITEBYTECODE=1. After the instruction-only review fixes, affected package/validator/role/prompt-rule and UI tests are rerun; unchanged helper runtime results above retain their exact command/environment and are not claimed as new application behavior.

## Bounded agent trials and review

The orchestrator delegated three synthetic artifact walkthroughs to `/root/native_behavior_trial` (factory_implementer) under `/tmp/pentapro-agent-smoke-wqrwrh6h`; no hidden grader/sibling outcomes or real developer approval was supplied. This attribution is inherited from the host delegation/result record, not independently inferred from fixture files. The outputs are local synthetic artifacts, not shipped project behavior; no complete inference transcript is stored inside them.

- Greenfield specification-only work produced six files and no accepted baseline or product implementation; review/clarifications remained pending.
- Brownfield feedback/cancellation preserved the two-scenario baseline byte-for-byte and retained partial code; unresolved effects prevented archival/rollback.
- A later synthetic accepted-result trial ran two local tests, changed one scenario while preserving another, consolidated and moved six files to an archive with the local date, and checked link targets. No Git publication occurred.
- The first closure attempt lacked implementation tests and is retained as incomplete evidence, not a passing gate; the later checked fixture is separate.

These are agent-constructed synthetic artifact walkthroughs, not independent proof of end-to-end autonomous orchestration, a matched baseline comparison, an all-host benchmark or proof of perfect determinism. The trial executor reported runtime gpt-6.1-terra; effective effort was not exposed. A fresh verifier independently inspected saved artifacts and reran the two closure-fixture tests, confirming preserved baseline/scenario content and moved link targets. That artifact-only verification cannot identify the producing model or prove how the files were authored. A separate reviewer reported no blocking findings after the corrections at snapshot `415f1ecee98c34efb4cba492164ca50e1dfaf88f270f80b0007c43dd70252631`; subsequent edits only qualify evidence claims and update completed review tasks.

## Adoption and handoff limits

Actual discovery/inference in all six clients, consuming Android/browser/accessibility journeys, deployed security/operations and live quiz permissions were not established. Exact CI Node 24 execution was not reproduced locally. Use bounded project adoption checks and the [migration guide](native-sdd-migration.md); old historical evidence and source attribution do not impose current runtime dependencies.

Configured role models/effort, explicit user authority and host permissions remain in force. An agent profile is not an isolation boundary. The harness is ready only to the extent demonstrated by the reviewed scope and observed checks; no universal 100% readiness, infallible model behavior, exhaustive security or measured cost advantage is claimed. Developer result acceptance and local consolidation/archive are complete. Verified publication is recorded separately by the shipper/run receipts.
