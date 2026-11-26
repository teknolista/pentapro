# PentaPRO future plan — proposals requiring deeper compatibility study

Date: 2026-11-25 (America/Sao_Paulo). Status: **study backlog; no implementation approval or efficacy claim**.

## Purpose and relationship to the current plan

The developer requested that potentially conflicting additions be persisted separately for future investigation. This artifact retains 12 of the 20 proposals discussed after the external-material review. The eight bounded compatible refinements are in [section 13 of the current improvement plan](pentapro-improvement-plan-2026-11-25.md#13-compatible-additions-from-the-external-material-review), which also contains the complete 20-item disposition table, source provenance and strategy constraints.

This file is not a second execution workflow, requirement baseline or replacement plan. Reading it does not authorize implementing it. The original P01–P12 commitments, including required TDD, independent review, continuation/recovery, evidence reuse, safe concurrency, usage observation and comparable process experiments, remain intact. A future item may refine one of those themes without making its proposed mechanism part of the approved approach.

The split is conservative: the items below introduce enforcement, policy, resource isolation, benchmarking or new operation modes whose interactions need decisions. They are not rejected, and a risk is not a proven defect. Retained items are also not guaranteed harmless: they have explicit bounds and acceptance checks. Cross-links in either direction are navigation, not automatic promotion.

## Non-negotiable study constraints

- Preserve PRODUCT, PROJECT, PRODUCTION, PROOF and PROCESS, the principal orchestrator, six factory roles and the current three-UI-skill migration decision. Do not add supervisors, permanent specialist roles or a second orchestrator by default.
- Build toward excellent automated engineering for all software types. GitHub/PR/browser/cloud examples must not become universal requirements. Domain-specific evidence can differ; required correctness and authority do not disappear.
- Preserve the project's actual authority, configured models/effort, permissions, required independent gates and result acceptance. An automation, label, model judgment or template does not confer authority; already granted authority must not be needlessly requested again.
- Keep one canonical record per fact and preserve customizations, logs, histories and effect reconciliation. Do not replay confirmed writes/pushes to repair missing bookkeeping.
- Study in isolated fixtures or an explicitly authorized pilot. ChuteGo, ChuteGPT, other consumer projects and global host settings are not write targets for this backlog. No hooks, schedulers, external orchestrators, issue/PR messages, installs or publication are authorized by creating this document.
- Preserve the original P0 order: scope/acceptance, authorized continuation and observable product journeys. New infrastructure must not become a prerequisite for implementing that work.
- Verify original licenses and attribution before any incorporation; use independently written designs for the MIT collection. Attachment claims about licenses, external costs and past executions are not newly verified facts.

## Evidence available and uncertainty

This list comes from `software-factory-review.md`, `legacy-openspec-config.yaml`, two attached video frames and the ensuing compatibility discussion, compared with current source contracts. External inputs are listed in the current plan's section 13. The review contains multiple assessments; agreement between them is not an independent behavioral trial. No external factory, full video, queue, dashboard or provider-diversity trial was executed for this persistence task.

Expected cost/quality benefits are hypotheses. The historical ChuteGo invocation counts are not token or cost measurements. Where host metadata, usage, readiness or an operation outcome cannot be reliably observed, preserve unknowns rather than zero or success. A planning checklist is not an executed check.

## F01 — Guide adoption depth without creating competing factory modes

- **Origin / related plan:** Discussion 2; P12.02, P12.06 and proportionate workflow selection.
- **Potential value:** Help developers choose a useful degree of assistance or automation based on repository readiness, risk, recovery, verification and authority.
- **Potential conflict:** A maturity ladder can imply that autonomy is inherently superior, create multiple workflows or let a lower mode skip required reviews. It may also exclude non-PR or hardware-dependent projects.
- **Questions to resolve:** Are capability descriptions sufficient? Which invariant gates apply regardless of mode? How are an exploration-only request and an authorized full delivery distinguished? Who selects scope without making the user manage every stage?
- **Likely owner / bounded approach:** Existing README/factory guide and lifecycle entry, not a new skill. Describe capabilities of one workflow rather than ranked organizational levels. Do not introduce auto-merge as a maturity requirement.
- **Study acceptance and counter-controls:** Compare small maintenance, greenfield, integration and constrained-runtime cases. Confirm narrower authority is honored, a full delivery still uses required agents/gates, and no request is silently rescoped. Measure selection errors and added ceremony.
- **Promotion condition / fallback:** Promote only a short evidence-backed guide that preserves current contracts. Otherwise retain existing proportionality guidance. Dependency: F02 may inform readiness but must not block the original plan.

## F02 — Add a scoped readiness verdict without blocking legitimate preparation

- **Origin / related plan:** Discussion 10; P06.04, P08.05, P09.05. Existing shared preflight remains in the current plan.
- **Potential value:** Distinguish readiness for specification, implementation, runtime verification and publication before costly downstream work.
- **Potential conflict:** A blanket green-baseline/clean-worktree rule blocks greenfield work, preserves inherited failures indefinitely or discards legitimate local changes. Rechecking the environment per agent wastes context. Setup must not invent a successful execution.
- **Questions to resolve:** Which facts are needed for each activity? How do expected TDD failures differ from inherited failures? When do environment facts expire? What may proceed with limitations? Can repairs proceed within current authority?
- **Likely owner / bounded approach:** Existing setup/factory entry and PROOF/run records. Reuse one preflight and attach evidence to the affected activity. No new mandatory standalone file or global environment installer.
- **Study acceptance and counter-controls:** Exercise existing green baseline, unrelated dirty worktree, new repository without tests, expected red TDD case, genuine regression, inherited failure and denied runtime access. Missing runtime evidence must block the claim that needs it, not all independent work. Preserve index and environment.
- **Promotion condition / fallback:** Require no weakening of tests, no repetitive diagnosis and a recoverable scoped decision. If unresolved, retain factual preflight plus honest unavailable checks. Run-related bookkeeping must not become a new SDD coordinator.

## F03 — Operationalize risk routing without waiving required roles or settings

- **Origin / related plan:** Discussion 11; P06.01, P07.08, P07.07.
- **Potential value:** Select relevant expertise and evidence depth for consequences, uncertainty, reversibility and affected surfaces.
- **Potential conflict:** A low-risk label may skip mandatory spec/review/verification; model tiers may override custom settings; a universal always-human list may recreate approval loops. A table based on diff size may miss serious effects.
- **Questions to resolve:** Which roles are invariant for the selected workflow? What is advisory versus enforced? How are mixed/unknown risk and runtime-unavailable expertise handled? What evidence would justify changing a classification?
- **Likely owner / bounded approach:** Existing factory role packets and PROCESS. Keep project-owned policy portable; preserve configured models/effort. Route additional skills through existing agents before considering new roles.
- **Study acceptance and counter-controls:** Small high-impact security/data change, large low-impact documentation change, mixed UI/API change, unsupported host capability and already-authorized sensitive operation. Verify no mandatory gate disappears and no model/config change is implicit.
- **Promotion condition / fallback:** Adopt only if routing is explainable, false positives/misses are evaluated and cost does not merely shift to repeated classification. Otherwise preserve explicit scoped role/skill selection. Depend on clarified F02/F04 where needed, not on a new agent.

## F04 — Protect acceptance integrity while preserving TDD and legitimate test changes

- **Origin / related plan:** Discussion 12; PROOF integrity, P04.02, P05.03 and P07.04.
- **Potential value:** Detect a branch weakening/removing the independent harness, CI or acceptance oracle that judges it.
- **Potential conflict:** Protecting every test makes TDD, regression repair and intentional behavior changes impossible. A fixed baseline harness may be incompatible with a legitimate API change. A model's edited record alone is not tamper-proof enforcement.
- **Questions to resolve:** Which oracles are independent? Who may change them under the existing contract? How are authorized test changes reviewed without extra routine approvals? What is the trusted base and what actually enforces it?
- **Likely owner / bounded approach:** Existing verifier/peer-review contracts and runner. Prefer a small manifest/diff check only if a genuine boundary and portability can be established. Do not install hooks or change host permissions as an incidental fix.
- **Study acceptance and counter-controls:** Legitimate new red/green test, changed public contract with updated tests, unauthorized deletion/skipping/assertion weakening, runner bypass, renamed harness and incompatible old fixture. Detect genuine weakening without blocking valid tests. Demonstrate the checker rejects the bad case and accepts the control.
- **Promotion condition / fallback:** Require meaningful adversarial and legitimate-change cases plus a reviewed exception path. Otherwise keep independent oracle review and existing prohibition on evading checks. Protected paths are integrity evidence, not proof of product correctness or a filesystem security boundary.

## F05 — Enforce selected transitions without preventing correction and recovery

- **Origin / related plan:** Discussion 13; P05.08, P08.03, P08.07, P10.01. Existing run-state validation remains authoritative.
- **Potential value:** Reject dependent advancement without the required contract review, current evidence or authority.
- **Potential conflict:** A rigid graph may prevent a return to design, strand work after reboot, require rerunning completed effects or conflict with legitimate archive/publication ordering. Another state store would duplicate the current run.
- **Questions to resolve:** Which transitions have objective enforceable conditions? What does resumed or partially completed mean? How are changed contracts and unaffected inherited checks represented? Is a policy advisory or mechanically enforceable?
- **Likely owner / bounded approach:** Existing factory lifecycle and `skills/software-factory/scripts/run_state.py`, not an imported `job` system. Preserve run identity, history, versions and uncertain-operation reconciliation. Prototype against the current schema before deciding on a migration.
- **Study acceptance and counter-controls:** Missing spec review, failed gate followed by repair, changed contract, stale write, interrupted push with remote success, cancelled work and metadata-only follow-up after publication. No automatic reopening/relabeling of historic passing evidence; do not chase a self-referential final commit hash.
- **Promotion condition / fallback:** Legal recovery paths and current contracts must remain possible; test both accepted and rejected transitions with preservation checks. Otherwise retain current instructions/helper validation and improve clear returns only.

## F06 — Check generated-artifact drift without unstable or excessive gates

- **Origin / related plan:** Discussion 14; P05.02, P06.08, P11.09 and current distribution consistency checks.
- **Potential value:** Detect divergence between canonical schemas/templates/metadata and their derived consumers.
- **Potential conflict:** Non-reproducible timestamps, network generators or destructive output paths create noisy gates and unwanted effects. A new generic mechanism may duplicate existing plugin/package validators.
- **Questions to resolve:** Which files are genuinely derived? Is generation stable and authoritative? What scopes need regeneration after a change? How are tool versions, unsupported generators and customized outputs handled?
- **Likely owner / bounded approach:** Existing `scripts/package_plugin.py`, collection validation and affected generator owners, only where a coverage gap is demonstrated. Preserve current validation; do not defer existing generation checks just because this generic extension is future work.
- **Study acceptance and counter-controls:** Reproducible generated drift, unchanged rerun, changed source with valid regeneration, intentional customization, irrelevant source edit, denied generator and failure midway. No deletion of custom data, hidden network writes or misleading green output.
- **Promotion condition / fallback:** Require deterministic safe output and a demonstrated missing check; reuse existing validators where sufficient. Otherwise document the actual generation/check procedure and limitations rather than add a new universal gate.

## F07 — Isolate parallel resources proportionately and verify the real boundary

- **Origin / related plan:** Discussion 15; existing concurrency contract, P08.05, P09.05.
- **Potential value:** Prevent interference through ports, databases, fixtures, processes, caches and scratch directories beyond source ownership.
- **Potential conflict:** Mandatory containers/worktrees can be costly or unavailable; worktrees alone do not isolate databases/network/processes. Cleanup may destroy another task's state. A resource allocator can become an unauthorized second orchestrator.
- **Questions to resolve:** Which resources are actually shared? What isolation does each host support? How is ownership assigned/recovered after a crash? When is serial execution safer and cheaper?
- **Likely owner / bounded approach:** Existing software-delivery/factory execution packet and reproducible recipes. First propagate resource ownership facts; prototype allocation/cleanup only on disposable fixtures. Preserve current prohibition on overlapping concurrent writes immediately.
- **Study acceptance and counter-controls:** Conflicting ports, shared test database, cache mutation, interrupted process, failed teardown and serial fallback. Check that cleanup affects owned resources only and does not follow unsafe paths. Report unavailable isolation explicitly.
- **Promotion condition / fallback:** Demonstrate an actual reduction in interference with acceptable setup cost and preserved evidence. Otherwise execute conflicting work serially. No host settings or container infrastructure installation is implied.

## F08 — Derive operational summaries without a second ledger or guessed metrics

- **Origin / related plan:** Discussion 16; P09.10, P10.13, P11.02. Existing optional usage observation remains planned.
- **Potential value:** Expose active work, waits requiring a decision, retries, elapsed time and observed usage from current runs/events.
- **Potential conflict:** A dashboard adds maintenance and context cost, conflates agent-duration sums with wall time, guesses billing or requires fragile transcript scraping. A reporting cache can become a competing source of truth.
- **Questions to resolve:** Which user decision needs this view? What metric definitions and observation boundaries apply? How are parallel work, missing results, event replay, clock differences and privacy handled?
- **Likely owner / bounded approach:** Existing event summarizer and retrospective/reporting owner; prefer a read-only command before any UI. Use current records, explicit provenance and unknowns. Do not call all proposed measures DORA metrics or create a new project-wide log.
- **Study acceptance and counter-controls:** Concurrent invocations, incomplete events, duplicate event attempt, unavailable usage, inherited checks and a completed historical run. Aggregate exactly once where meaningful; keep costs unknown without a reliable source. Protect prompts/secrets and avoid scanning all runs during ordinary tasks.
- **Promotion condition / fallback:** A measured operational need and trustworthy small summary must precede a dashboard. Otherwise retain bounded existing summaries. A lower invocation count alone is not an efficiency result.

## F09 — Replay historical tasks with independent grading and representative scope

- **Origin / related plan:** Discussion 17; P10.14, P11.12. Comparable process experiments are already in scope; this replay method is deferred.
- **Potential value:** Evaluate realistic changes against their pre-change state alongside synthetic controls.
- **Potential conflict:** Solution leakage, known public PRs, grader access, selection bias and unequal environments can produce misleading comparisons. A few web PRs cannot support all-software claims.
- **Questions to resolve:** What is available to the task model versus the grader? How is the task reconstructed without giving away the accepted implementation? Which cases represent the decision and how are failures/skips retained?
- **Likely owner / bounded approach:** Existing `docs/SKILL-EVALUATION.md`, package evaluation procedure and isolated `evals/`. Do not start external Codex instances for ordinary work or model trials without a later explicit evaluation scope consistent with host/user constraints.
- **Study acceptance and counter-controls:** Behavioral grading accepts a different correct architecture, rejects a seeded regression and includes actual access/isolation checks. Keep tools, permissions, budgets and starting state comparable. Private/recent examples do not prove absence of contamination.
- **Promotion condition / fallback:** Define isolation and grading before a small diverse pilot; expand only on evidence. Otherwise retain the original matched synthetic/vertical experiment. Report uncertainty and maintain original independent evaluation requirements.

## F10 — Test model diversity without overriding configurations or inventing independence

- **Origin / related plan:** Discussion 18; P02.04, P04.04, P07.03, P09.11.
- **Potential value:** Determine whether a different reviewer model catches material defects at acceptable incremental cost.
- **Potential conflict:** More providers may increase cost, expose source to another service, violate configured choices or create false security confidence. Different names/providers do not establish independent knowledge or failure modes.
- **Questions to resolve:** Is there a demonstrated miss attributable to correlated reasoning? What actual runtime is available and authorized? What controls would distinguish model effect from prompt/context/tool differences?
- **Likely owner / bounded approach:** Existing reviewer packets and evaluation procedure, not a new permanent role or default tier substitution. Preserve configured model/effort unless separately authorized. Runtime-unobservable attribution remains unknown.
- **Study acceptance and counter-controls:** Blind defect-seeded and clean cases under matched conditions; measure material misses, invented findings, time and observed cost. Include unavailable second-model behavior without waiving mandatory independent review.
- **Promotion condition / fallback:** Require a justified quality/cost result and authorized data/host use. Otherwise use the existing fresh review context with its honest limitations. No universal requirement for a second provider.

## F11 — Define recurring authority without granting it through configuration

- **Origin / related plan:** Discussion 19; existing authority, stop-condition and recovery contracts.
- **Potential value:** Bound scheduled/event-driven work by purpose, inputs, actions, evidence, resource limits, duration, revocation and result destination.
- **Potential conflict:** A scheduler, policy file or past approval may be misread as broad authority. Persistent credentials, untrusted PR content and repeated effects can widen exposure. Automatic edits to factory instructions would bypass reviewed maintenance.
- **Questions to resolve:** Who grants/revokes which operations? Where is trusted policy anchored? What happens after expiry, interrupted effects or changed project instructions? Can the host actually enforce limits and deliver results?
- **Likely owner / bounded approach:** An optional reference under the existing factory/setup owner after the boundary is agreed. Distinguish a policy template, an explicit grant and a live scheduler. No global hooks, scheduled jobs or external messages are installed by this plan.
- **Study acceptance and counter-controls:** Expired/revoked grant, malicious task text, unavailable scheduler, repeated event and crash after an external write. Preserve user's checkout and reconcile effects before retry. A permitted report does not authorize edits, merge, deploy or permissions changes.
- **Promotion condition / fallback:** Explicit host-supported bounded authority and audited disposable pilot. Otherwise retain session-triggered work and the normal acceptance gate. F03/F05 may support analysis but do not themselves confer authority.

## F12 — Add queue intake without making labels or PRs universal authority

- **Origin / related plan:** Discussion 20 and the Bergholz frame; optional tracker integration.
- **Potential value:** Triage queued work with an explicit ready/needs-information/rejected disposition and resumable handoff to the existing lifecycle.
- **Potential conflict:** Anyone able to apply a label might trigger privileged work; issue comments may inject instructions. One-PR-per-issue or auto-merge assumptions can narrow support to a specific host and bypass developer acceptance. Concurrent consumers may process the same issue twice.
- **Questions to resolve:** What verified policy/identity authorizes intake and effects? How are duplicate claims, changed labels, scope changes and stale comments handled? How do local requests and non-GitHub trackers remain first-class?
- **Likely owner / bounded approach:** Existing tracker templates and an optional factory adapter; preserve native changes/runs as canonical records. Start with read-only classification in a disposable repository. External issue/PR writes or messages require actual separate user authority.
- **Study acceptance and counter-controls:** Untrusted commenter/label, missing information, duplicate event, changed scope, legitimate resumed task and no-tracker/local use. Model merge is not human acceptance; a human merge is evidence only within the project's actual acceptance policy. No label alone grants merge/deploy permissions.
- **Promotion condition / fallback:** Verified trust/claim/recovery boundaries and an authorized pilot with bounded effects. Otherwise retain current request-driven orchestration. Consider F11 only if work becomes recurring; no dependency may block the original plan.

## Promotion protocol and study order

No item moves automatically into the current plan. A later explicit study should select one bounded question, refresh current source and relevant lessons, preserve fixed requirements, define a baseline and adversarial/legitimate controls, and identify actual host/data/resource authority. Record the result in existing study/run evidence as appropriate; do not create an execution directory for merely reading this file.

Promotion requires all of the following:

1. Map the selected F ID to original P IDs, owners, consumers, new observable behavior and the exact conflict being resolved. Show that no existing proposal is silently removed or deferred.
2. Describe invariants, supported domains/hosts, unsupported or unavailable evidence, privacy/license implications and maintenance/context cost.
3. Evaluate both the failure the mechanism should prevent and valid work it must allow. Use relevant TDD for executable behavior, required independent review and honest observed metadata. Structural checks alone do not establish behavioral improvement.
4. Demonstrate preserved scope completeness, correction/continuation, evidence integrity and actual acceptance authority. Compare quality and efficiency; reject regression even if token counts fall.
5. Present a concrete recommendation to promote, revise or defer, with remaining uncertainty. Obtain the developer's explicit scope decision before adding this deferred mechanism to implementation. That decision is distinct from later acceptance/publication authority.
6. Integrate into the existing owner, reconcile affected consumers/metadata/evals and provide migration/disable/recovery behavior. Avoid a second source of truth. Retain this item's study history and link the chosen replacement; do not rewrite it as an already successful result.

Suggested order for a future study, not an implementation commitment: investigate F02–F05 entry/integrity/routing/transition interactions first; assess F06–F07 only for demonstrated generation/concurrency gaps; derive F08 only from a real reporting need; use F09–F10 for explicit comparative questions; consider F11–F12 only after authority and recovery boundaries are understood. F01 is optional adoption documentation, not a prerequisite for the factory. Dependencies must never turn this backlog into a blocker of current P0 work.

## Resumption prompt for study only

```text
Study selected items from docs/pentapro-future-plan.md and their links to
section 13 and the original P01–P12 proposals in
docs/pentapro-improvement-plan-2026-11-25.md. Inspect current AGENTS.md and
current owners first. Preserve all five pillars, current mandatory roles/gates,
TDD policy, model settings, actual authority, and all-software applicability.
Do not implement the backlog or modify application/consumer projects or global
configuration. Select a bounded compatibility question, distinguish established
facts from hypotheses, propose a reproducible evaluation with positive and
negative controls, and report what would justify promotion. Model executions,
external operations, installation and publication require their actual scope
and authorization; do not infer them from this document.
```

## Persistence checkpoint

- Status: 12 deferred proposals documented with origin, conflicts, questions, owners, candidate approaches, controls and promotion conditions; eight compatible additions remain in the current plan.
- Artifacts: this file and the appended section 13 of the current plan. All 20 discussion items have one primary destination and retain their original mapping.
- Evidence: document/source inspection and compatibility assessment, not runtime proof or measured cost/quality improvement. No full-video or external-factory execution was performed.
- Verification: documentation and preservation/accounting results are recorded in the accompanying persistence result after execution.
- Pending: explicit future study scope, resolution of conflicts, authorized trials, independent review and promotion decision for each selected item. No implementation is requested by this artifact.
- Git baseline observed: `2647a8696c19eb28c1a1bfedf7eccc5a429602c3`. No commit or push requested or performed. Private prompt logging remains separate from published planning artifacts.

The executed documentation checks, environment limits and original-content/disposition preservation results are recorded in the [current plan verification checkpoint](pentapro-improvement-plan-2026-11-25.md#documentation-persistence-verification--2026-11-25). They do not establish that any F item is safe, implemented or effective.
