# PentaPRO Engine: deterministic factory inventory

Date: 2026-11-26. Research snapshot: PentaPRO HEAD `5b39b1bd2c760a4d1c96bd9d05bd28f72dcec6ad` (bundle 3.1.2). Read-only source investigation; no helper tests, live host trials or performance measurements were executed. This document is an input to the five-pillar specification, not a second canonical specification. Paths below are relative to the PentaPRO repository root; package paths abbreviated as `software-factory/`, `setup-pentapro/` or `penta-pro/` resolve under `skills/`.

## Governing decisions and reconciliation

The current user request authorizes specification followed by Rust implementation in this same repository (`src/`, `test/`, `target/`), binary `pentapro`. This supersedes the initial Engine document's proposed separate repository and `pentapro-engine` executable, and its copy-ready exploration-only prompt. Preserve skills, role profiles, plugin metadata, logs and existing specification history. The historical native SDD statement that no CLI/schema engine is introduced describes the previous migration: the new request deliberately adds an optional Engine. It does not authorize making existing skills depend on that Engine.

Sources: `docs/native-sdd-contract.md`; `docs/pentapro-engine-especificacao-inicial-rust.md` §§1,4–11; `skills/software-factory/SKILL.md`; `skills/penta-pro/SKILL.md`; `docs/SKILL-ROUTING.md`; current helpers listed below. The initial Engine document already proposes PP-01–PP-26; retain those IDs or provide an explicit mapping rather than creating competing requirement identities.

Full OpenSpec parity remains a final-product requirement. A first increment is a vertical slice, not permission to silently remove stores/worksets/schemas/host integrations or any other upstream surface. A separate upstream inventory is needed for exact parity details.

## Boundary rule

Engine owns deterministic checks, serialization, plans, discovery, process execution and reliable observation. Agents own discovery, design, implementation reasoning, test design, evidence sufficiency, review and exception diagnosis. Humans own product choices, acceptance and missing/consequential authority. Engine may verify an approval receipt's structure, identity and snapshot; it cannot prove the human genuinely approved merely because a local JSON field says so. Host sandbox and approval enforcement remain external controls. No filesystem tool is a security boundary against a process with equivalent write permissions.

## Complete capability-family inventory

Each row gives a concrete acceptance scenario. “Existing” means source exists, not that it was executed in this investigation. Dxx are research item IDs; map to final PP IDs in the owning specification.

| ID / PP mapping | Deterministic responsibility | Existing source / owner | Acceptance scenario / dependency |
| --- | --- | --- | --- |
| D01 / PP01,20 | Resolve actual repository root, branch, active Git operations and path containment; reject unsupported/symlink substitutions | `software-factory/scripts/run_state.py:project_root`, `record_path`; setup helpers | Nested root resolves explicitly; wrong root, rebase/merge and escaping write reject without mutation. Foundational for every writer. |
| D02 / PP01,23 | Safe append-only prompt capture at Engine-controlled entry points, redaction, restrictive creation, ignored/index conflict checks | root `AGENTS.md`; `setup-pentapro/SKILL.md`; optional logging examples are not automatically installed | Unsafe/tracked log refuses; repeated identical user events are not incorrectly deduplicated by text; prior log bytes preserved. Capture outside Engine remains unknown. |
| D03 / PP01 | Non-destructive Git ignore/attributes merge | `setup-pentapro/scripts/merge_git_templates.py` | First merge adds missing lines; rerun no-op; existing bytes and index remain preserved. |
| D04 / PP01 | Plan instruction-section reconciliation with content precondition, exact section boundaries and example/comment refusal | `setup-pentapro/scripts/plan_instruction_sections.py` | Fenced canonical heading is review-required, valid live sections idempotent, changed SHA rejects; plan cannot overwrite custom content. D01. |
| D05 / PP01,02 | Detect six-host role profiles, split workflow body from host/model/effort metadata, compare provenance and classify custom changes | `setup-pentapro/scripts/check_agent_profiles.py`; `setup-pentapro/references/factory-setup.md` | Current workflow/custom model separately reported; unknown custom body preserved; installed profile is not evidence of actual model execution. |
| D06 / PP02,24 | Discover skill paths, version, package resources/licenses, install hash/origin/scope and duplicate/retired IDs | `plugin.json`, `scripts/package_plugin.py`, `scripts/validate_collection.py`, `docs/plugin-distribution.md` | Missing resource/hash drift/duplicate ID diagnosed; no global configuration mutation. Source installation and runtime discovery distinguished. |
| D07 / PP01,02,21 | Upgrade planning from exact known baseline and CAS apply, with conflict detection and preservation manifest | setup refresh reference and checker; no generalized safe apply helper currently observed | Intentional local reversion and unknown custom copy produce conflict, not overwrite; repeated accepted plan no-op. D01,D05,D06. |
| D08 / PP03 | Initialize pillar directory/topic scaffolds and change/archive directories | `penta-pro/scripts/init_pentapro.py`; `penta-pro/assets/` | Fresh safe initialization; existing destination never overwritten; scaffolds remain Pending. |
| D09 / PP03,11 | Validate pillar coverage states, required six change files, stable requirement/scenario IDs, local references and traceability shape | `penta-pro/SKILL.md`, `references/coverage-map.md`, `assets/change/`; root link validator | Missing dimension, duplicate ID and unresolved scenario reported; text presence never implies semantic completeness. D08. |
| D10 / PP04 | Create/list/show/validate native changes, enforce unique two/three-word names and lifecycle transitions | `docs/native-sdd-contract.md`; `software-factory/references/change-records.md` | Duplicate/colliding name refuses; required checks absent blocks advancement; unaffected baseline preserved. D09,D16. |
| D11 / PP04,21 | Plan semantic baseline consolidation with explicit add/modify/retire/rename intent and agent-reviewed patch | native SDD contract; `penta-pro/references/document-maintenance.md` | Unknown or conflicting ID cannot be silently reused; unaffected scenarios remain; Engine checks identities/diff but agent evaluates meaning. D09,D10. |
| D12 / PP04 | Transactional archive/cancel operation, local-date naming, collision guard and incoming/outgoing link repair | `software-factory/references/closure.md` | Collision preserves both trees; cancellation never promotes abandoned intent; partial retained code recorded. D10,D11,D23,D27. |
| D13 / PP05 | Task graph, dependency cycle detection, readiness, path-overlap guards, owners/input/output/check declarations | `software-delivery/SKILL.md`; `software-factory/references/roles.md` | Cycle or overlapping concurrent writers reject; independent tasks ready together; serial default. Needs explicit machine-readable task representation alongside Markdown. |
| D14 / PP06 | Lightweight Vibe workflow and explicit promotion to SDD without waiver of policy | initial Engine document §6; extension proposal, not implemented native format | Promotion preserves evidence and identity; no synthetic filled requirements. Needs product decision on minimal state. |
| D15 / PP07 | Resolve declared policy/capabilities/operation authority and expose missing authority | role packets; `git-ship/SKILL.md`; host controls external | Push/merge/deploy capabilities separately identified; approval scope persists across continuation; file data cannot grant authority. D01,D24. |
| D16 / PP10,11 | Gate model bound to exact snapshot; reject missing/stale evidence, required not-applicable and unavailable gates | `software-factory/scripts/run_state.py:validate`; `references/run-records.md` | Changed source invalidates pass; missing evidence blocks SHIP/DONE; unsupported not-applicable cannot waive required gate. |
| D17 / PP11 | Deterministic source fingerprint of Git inventory, mode, file bytes and symlink target, race checks | `software-factory/scripts/run_state.py:snapshot` | Same deletion hashes before/after commit; symlink never dereferenced; ignored/external inputs explicitly outside identity. Preserve algorithm/version compatibility. D01. |
| D18 / PP11,19 | Scope-aware evidence reuse plan with original receipt, delta, dependency closure and invalidation reasons | `software-factory/references/execution.md`; improvement P09.09 | Related behavior change rejects old green gate; irrelevant docs delta may be proposed for reuse, never silently restamped. Current helper intentionally requires current whole-tree fingerprint; new contract needs negative controls. |
| D19 / PP12 | Strict run.json v1 parsing/validation, one run per assignment, CAS version, lock and atomic checkpoint/history | `software-factory/scripts/run_state.py` | Duplicate JSON keys/stale version/unsafe target rejects without damage; stopped writer recovery never deletes lock automatically. D01,D17. |
| D20 / PP08,12 | Append-only invocation event ledger, ordering/identity/idempotent append, requested vs observed metadata | `software-factory/scripts/run_events.py`; `references/invocation-events.md` | Duplicate identical event no-op; duplicate conflicting event/truncated history refuses preserving bytes; attempt progression validated. D19. |
| D21 / PP08,09 | Capability negotiation and compact role packet construction; preserve configured model/effort and scopes | six role templates under `setup-pentapro/assets/`; `software-factory/references/roles.md` | Missing role/capability reported; unsupported model never replaced without authority; no dispatch from a role template alone. D05,D13,D15,D20. |
| D22 / PP08 | Host-driven dispatch integration, observed dispatch receipts, cancellation/wait/retry and effect reconciliation | factory execution reference; host adapters currently templates, not executable engine adapters | Dispatch failure differs from role failure; interrupted operation reconciled before retry; one orchestrator at a time. Engine-driven later adapter work, not default hidden supervisor. D21,D23. |
| D23 / PP12,20 | Operation journal/plan/observe/reconcile for partial effects, single writer, crash recovery and dry run | existing run operations/locks; initial Engine §5 | Crash between effect and receipt detects actual state before replay; never repeat push/archive just to repair bookkeeping. Multi-file transactions need new design; atomic single-file writes alone insufficient. |
| D24 / PP07,10 | Snapshot-bound result-acceptance receipt and distinct authority for consolidation/archive/commit/normal push versus release/merge/deploy | `software-factory/SKILL.md` steps 6–8 | Silence, elapsed time, tool success or model approval cannot satisfy human gate. Local-only restriction retained. D15,D16. |
| D25 / PP13 | RED/GREEN/refactor evidence timeline with relevant failure classification and executed check provenance | `behavior-testing/SKILL.md`; `software-factory/scripts/command_evidence.py` | Compile/setup failure not RED; later test not mislabeled test-first; TDD requirement only when selected. Test relevance remains judgment. |
| D26 / PP11,13,18 | Trusted argv subprocess runner: observed exit, start/end duration, timeout/cancel and receipt hashing | `software-factory/scripts/command_evidence.py` | Test fails through formatter pipeline without masked success; timeout kills owned process group; interrupted outcome preserved; stdout/env/secrets not copied by default. POSIX current, Windows gap. D17. |
| D27 / PP14 | Git plan, exact path/index guard, commit full SHA verification, normal push and remote/CI observation | `git-ship/SKILL.md`; `references/resumable-operations.md` | Hook-produced commit identity resolved after commit; wrong/ref-expanded SHA never used; unrelated staged changes preserved; remote uncertainty reconciled. D15,D16,D23,D24. |
| D28 / PP14,15 | Bounded one-administrative-commit receipt closeout classification/checking | `software-factory/scripts/check_delivery_receipts.py`; `references/delivery-closeout.md` | Source/mixed patch cannot enter receipt-only lane; existing history/gates preserved; no third confirmation commit or recursive role call. D19,D20,D27. |
| D29 / PP15,16 | Per-run/bounded-set summary of statuses, outcomes, retries, durations and real supported usage with unknowns | `run_events.py:summary`; PDSA protocol | Unknown tokens remain unknown, not zero; counts do not imply billed usage or effectiveness. Cross-run reading explicit/bounded. D20,D26. |
| D30 / PP16,19 | Resource/time/context budget checks, compact relevant context packing and content/version/policy cache keys | role packet reference; initial Engine §§6.7,9.3 | Cache invalidates changed contract/policy; packet includes relevant preflight, stale results not reused; budget exhaustion checkpoints. No promised token-saving percentage. D13,D17,D21. |
| D31 / PP17 | Lesson-candidate structure, duplicate suggestions and English persistence plan | `docs/agents/continuous-improvement.md`; lessons record; factory skill | Candidate vs validated lesson distinguished; orchestrator-only writes; no skill change/publication automatically granted. Semantic dedup/lesson validity remains agent review. |
| D32 / PP18 | Stable JSON/exit diagnostics, non-TTY/headless behavior, report export and shell completion | initial Engine §7; CLI contract still to specify | JSON stdout parseable, stderr diagnostics separate; headless command never waits for hidden input; selected defaults explicit. All commands depend on this envelope. |
| D33 / PP20 | Secrets/log/privacy export policy, no-follow paths, least privilege and indirect-instruction handling | logging rule; cybersec skill; helper safety guards | Export excludes prompts/keys; embedded record text never executed as shell or policy; arbitrary external links grant no repo authority. Test concrete trust crossings, not claim blanket injection prevention. |
| D34 / PP21 | OpenSpec/legacy import preview, conflict manifest, backup/rollback, exact baseline attribution and ID mapping | initial Engine §§3,5; no generalized importer exists | Existing docs and IDs preserved; unsupported semantic construct explicit; migration no dual canonical owner. Depends on upstream inventory. |
| D35 / PP22 | Multi-repository selection, dependency/workset/store context and shared contracts | initial Engine PP22; upstream parity inventory needed | Referencing a repository does not authorize writes/dispatch/push in it; conflicts and source revision explicit. D01,D15,D34. |
| D36 / PP24 | Collection validation, package export/hash inventory, standalone resource/metadata checks, eval-case validation | `scripts/validate_collection.py`, `package_plugin.py`, `run_skill_evals.py` | Ignored synthetic secret excluded; existing export refused; no package source symlink; authored case vs executed trial explicit. Keep helper compatibility rather than rewrite all evaluation machinery at once. |
| D37 / PP24 | Controlled process/quality experiment runner and metric comparison | `docs/SKILL-EVALUATION.md`; plan P10.12–14 | Comparable baseline/control tasks, fixed grading, escapes and counter-evidence alongside cost; one smoke trial never proves causal savings. D26,D29. |
| D38 / PP25 | Explicit operational gate/runner hooks and deployment observation/rollback receipts | `production-operations/SKILL.md` | Commit success does not imply runtime deployment; deploy requires own authority and target/revision evidence. D15,D23,D26. |
| D39 / PP26 | Versioned adapter/runner/plugin contracts, schema validation and capability discovery | initial Engine §§5,7; existing plugin formats separate | Unsupported contract versions refuse safely; no record/plugin text executed implicitly; optional adapter absence explicit. |
| D40 / PP03,11,15 | Requirement/component preserve-adapt-exclude inventory, evidence-class and decision discoverability checks | `software-factory/references/journey-evidence.md`; penta-pro references | Missing promised supporting tool flagged; source/rendered/task/user evidence distinctly labeled; semantic completeness still reviewer responsibility. D09. |

## Responsibilities retained by skills, agents and developer

- Principal host session: intent clarification, consequential choices, scope arbitration, principal orchestration and recording ownership. Engine can suggest next permitted action from state; it cannot invent acceptance or expand authority.
- `factory_spec` / PentaPRO: semantics, feasibility, complete promised journeys, criterion quality and alternatives; Engine checks structure/links/IDs and records review snapshot.
- `factory_implementer` / delivery/platform skills: code, behavior, tests and design judgment; Engine owns trusted execution/readiness/receipts, not arbitrary automatic “fixes”.
- `factory_verifier`: claim-to-evidence sufficiency, realistic journeys and actual UI/host behavior. Engine can execute tests, preserve status and detect stale input; it cannot infer correctness or visual usability from a green exit alone.
- `factory_reviewer` / Peer Review and Cybersecurity: substantiated defect/threat traces, unexpected cross-boundary risks, test effectiveness and independence disclosure. Engine provides fixed snapshot and coverage matrix.
- `factory_shipper` / Git Ship: review the scoped candidate under authority; Engine can enforce bounded deterministic Git operations and observe refs. Required result acceptance precedes closure as policy dictates.
- `factory_retrospective`: interpret causes, counter-evidence and useful proposals; Engine calculates summaries without inventing cause/confidence, cost or outcome.
- Technical Research: evaluate practical alternatives, source trust, maintenance/performance/license trade-offs; Engine can fetch/cache/index pinned inputs only with permitted network use.
- UI Design Terminal/Web/Android: product interaction/readability/platform judgments; Engine can capture dimensions/screenshots/test output where supported, not infer human usability.
- Android/API/MCP/background/DI/data/testing specialists remain selected by actual product platform; their presence does not imply every skill must be invoked to build this Rust CLI.
- PR Quiz remains an explicit-request feature; an Engine should not generate/publish quizzes automatically after every PR.
- Developer: product acceptance, unresolved material scope/authority choices, release/merge/deploy approval where required. All six roles occur at their applicable lifecycle points; shipping role invocation is not authority for premature publication.

## Improvement-plan reconciliation against current source

The improvement plan is dated 2026-11-25; use its IDs rather than the old Engine document's assumption that it was inaccessible. It is now accessible and was inspected. All proposals are policy/design inputs; historical reports are scoped evidence, not proof current runtime automation exists.

| Plan family | Current source disposition | Engine translation |
| --- | --- | --- |
| P01.01–06 | Journey/equivalence reference, criterion matrices, early-slice and compact-packet requirements now present in factory/delivery/penta-pro | D09,D13,D30,D40; test real end-to-end use, not task count |
| P02.01–07 | Evidence classes, requested/observed metadata, unknown outcomes and reuse provenance explicit in execution/roles/events | D16–20,D26,D29; typed unknowns and scoped receipts |
| P03.01–06 | Development/installed/automated contexts, support tools and presentation examples explicit in journey evidence and terminal skill | D32,D40; validate operation + presentation with host-specific evidence |
| P04.01–05 | Language-independent requirements, honest TDD, recovery and independent roles retained | D23,D25,D26; no TDD/independence claim from metadata alone |
| P05.01–09 | Exclusions/identities/observables/alternatives/administration/freshness now covered by source contracts and helpers | D09,D17–19,D26,D40; new scope-aware reuse requires separate tested contract |
| P06.01–11 | 26 skills and three UI owners present; routing/role guidance selects by outcome, not all-package ritual | D05,D06,D21,D40; package inventory != observed skill use |
| P07.01–08 | Existing six roles and principal orchestrator preserved; compact bounded assignment and independent checks explicit | D13,D21,D22; no new permanent supervisors |
| P08.01–08 | Execution reference now describes pause/failure/recovery/retry/continuation and missing authority | D19,D22–24,D30; implement honest state machine, not auto-retry loops |
| P09.01–11 | Compact reads/packets, reuse provenance, batching, actual usage and controlled efficiency comparison instructed | D18,D29,D30,D37; current full-tree gate fingerprint remains conservative |
| P10.01 | Current `software-factory/references/execution.md` and role contracts include continuation semantics | D22,D23 |
| P10.02–03 | `journey-evidence.md` and penta-pro templates carry equivalence/components/criterion-to-evidence ownership | D09,D40 |
| P10.04–05 | `references/roles.md`, technical-research and penta-pro alternatives guidance present | D21,D30 plus agent judgment |
| P10.06 | `plan_instruction_sections.py` checks fenced/commented headings, expected SHA and conservative boundaries | D04; no blanket Markdown-parser completeness |
| P10.07 | Profile checker and refresh procedure distinguish workflow, metadata and custom baselines | D05,D07; a generalized apply engine is new |
| P10.08 | `ui-design-web`, `ui-design-android`, `ui-design-terminal` in current manifest | D06,D21; source/runtime adoption remain distinct |
| P10.09 | Terminal skill and journey evidence specify representative rendering/task evidence | D32,D40; automated capture is platform dependent |
| P10.10 | Safe reuse is instructed but run helper still checks full fingerprint | D18; do not weaken current safeguard without negative controls |
| P10.11 | `command_evidence.py` captures actual process status/snapshot and bounded cleanup | D26; OS-specific gaps remain |
| P10.12 | Historical maintenance review reports a synthetic PTY journey; no new trial executed here | D37; Engine pilot still required |
| P10.13 | Optional usage fields exist in events; no host telemetry hook automatically installed | D29; real host adapters/coverage still needed |
| P10.14 | Controlled comparison is prescribed; no causal efficiency result established by source | D37 |
| P11.01–12 | Acceptance observables echoed in current evidence/closure/recovery/upgrade contracts | Corresponding D04,D07,D16,D18,D23,D25,D29,D37,D40; carry original IDs into proof |
| P12.01–06 | Current six roles, early slice, compact records and measured claims preserved | Roadmap ordering constraint, not six additional Engine commands |
| P13.01 | `references/roles.md` actionable missing-authority packet | D15,D21,D32 |
| P13.02 | Relevant preventive control vs detection distinguished by risk/criterion guidance | D16,D40; meaningful threat/criterion interpretation remains cognitive |
| P13.03 | Behavior-testing regression/negative controls and recurring-defect guidance | D25,D26; exact numeric-boundary follow-up recorded in 3.1.1 |
| P13.04 | Journey evidence carries multi-consumer shared rule/adaptations/exclusions | D35,D40 |
| P13.05 | Penta-pro decision maintenance and closure discoverability | D09,D11,D12 |
| P13.06 | Simplicity/total-cost review guidance in Peer Review | Agent judgment; D40 can require a decision reference |
| P13.07 | Penta-pro material-behavior triggers include errors, partial effects, duplicate operations, recovery/resource criteria | D09,D23,D40 |
| P13.08 | Technical-research/penta-pro alternatives assess proof, safety, performance and maintenance | Agent decision; record measurements/ADR through D26,D40 |

This mapping is a source-level reconciliation. No automatic claim is made that every prose proposal is behaviorally effective. `docs/maintenance-review-2026-11-26.md` and `docs/chutego-lessons-adoption-2026-11-26.md` preserve the previous checks and explicit gaps; do not label those executions as new Engine proof.

## Suggested dependency order and first vertical journey

1. Root/path safety, stable CLI JSON/errors, read-only metadata/doctor, safe native six-file change initialization and validation. Exercise create → list → show/status → validate from nested directory and headless context; reject traversal/collision without altering collection files.
2. Snapshot, strict v1 run/event compatibility, check receipts and gated transitions; compare Rust bytes/semantics against Python fixtures, including negative controls. This turns a large existing deterministic administrative cost into software without waiting for hosted AI integration.
3. Task readiness/DAG and compact host-driven packets; select configured roles and preserve unknown observed metadata. No new dispatcher until host integration is actually proven.
4. Closure/archive/consolidation plans, authority receipts and operation journal before any Git delivery writes. Distinguish schema validation from authenticity and semantic approval.
5. Full OpenSpec parity families per frozen upstream inventory; import/migration, custom schemas, stores/worksets, integrations, interactive terminal and completion are required final scope, not optional untracked exclusions.
6. Proven host adapters, optional engine-driven orchestration, budget/metrics/experiment support and operational extensions, each with its own tested observable and no promises of inferred cost savings.

Ordering of items 1–5 can be adjusted to the specification's architecture, but full parity must have a complete matrix before it can be claimed. Preserve no-Engine skill use throughout. Do not bulk-update projects or global host configuration as a side effect of developing Engine.

## Material gaps and questions for the owning specification

- Human approval receipt authenticity/channel and CLI UX need a concrete threat model; a writable file cannot enforce provenance by itself.
- Typed machine metadata alongside Markdown must be defined without creating duplicate sources of truth or damaging hand-authored formats.
- Atomic multi-file mutations, Windows lock/process cleanup and adversarial path races need actual implementation and tests; existing Python helper behavior is not universal OS proof.
- Host-driven actual runtime integration, configured vs observed models/effort, cancellation, optional usage coverage and capability fallback need per-host probes. Existing six-host templates are not runtime adapters.
- Full OpenSpec source/CLI/test inventory and pinned stable revision are a separate prerequisite for exact parity; do not infer that all old document command names still exist.
- Research did not benchmark crates or run either upstream CLI; performance/commonness/maintenance comparisons require primary-source data and local measurement as appropriate.
- The user requests development start, not immediate final-product acceptance/publication. Keep active change/baseline and normal result gate distinct, following current policy.
