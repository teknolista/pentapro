# PentaPRO improvement plan and resumption context

Date: 2026-11-25 (America/Sao_Paulo). Status: **proposals consolidated; implementation deferred**.

This document preserves the complete substance of the improvement proposals discussed after the ChuteGo retrospective, including their descriptions and the subsequent cross-project lessons review. It is a consolidated plan, not a verbatim conversation transcript or evidence that the changes already work. It is intended to support a new session without requiring the old chat to fit in context.

## Authority, scope, and decisions to preserve

The current request authorizes saving this document for later work. It does not request implementation now. The user's intent is to execute the proposed PentaPRO improvements after credits renew.

- Future implementation concerns **PentaPRO source packages, agent assets, process definitions, templates, helper scripts, catalogs, and evaluations in the `skills` repository**.
- **Do not change ChuteGo or ChuteGPT.** They remain read-only case studies, including their application code, specifications, installed skills, agent profiles, configuration, data, and historical records. Their corrective product changes have been removed from this plan.
- Do not bulk-update other project installations, change global host configuration, install hooks, or start external AI orchestrators as a side effect. Consumer rollout requires separate authority.
- Preserve PentaPRO's five pillars: PRODUCT, PROJECT, PRODUCTION, PROOF, and PROCESS. Preserve useful existing workflows, permanent instruction sections, histories, prompt logs, custom model/effort settings, permissions, and unrelated work.
- Keep the current principal orchestrator and six factory roles. Improve their contracts before adding roles. There is no evidence-based recommendation to create more permanent agents or supervisory agents.
- Replace `ui-design` with **`ui-design-web`, `ui-design-android`, and `ui-design-terminal`**. Technology selection belongs in the existing agent/workflow that needs UI expertise. Do not retain a fourth forwarding skill solely to route between them. Retirement must be coordinated with consumers and packaging.
- Use existing canonical records and owners. This planning document does not replace a native change specification, a run record, the lessons record, or the collection routing map.
- Write maintained collection artifacts in English; converse with the user in Brazilian Portuguese. Keep future work in the current authorized Codex session, with only the agents required by the applicable official workflow or a specifically authorized quality need.
- Commit, push, deployment, consumer adoption, and destructive operations are not authorized by this document's existence. Resolve authority from the future user request and applicable workflow; do not repeatedly request authority already granted in that execution.

## Context needed to resume

The user wanted a Go implementation of ChuteGPT and an evaluation of the PentaPRO factory, including initial delivery and a separate guess-generation change. ChuteGo was delivered, but the user found missing development tooling and inferior terminal organization. The user also reported excessive token consumption and unexplained interruptions. Subsequent discussion shifted from application repair to improving PentaPRO itself.

The original retrospective (`/home/dever/workspace/teknolista/chutego/docs/agents/relatorio-retrospectiva-chutego-pentapro-2026-11-25.md`) has 12 topics. Sections 1–12 below retain their order. Proposals within each topic progress approximately from simpler/local changes to more involved changes. Complexity order is not priority order. Repeated themes deliberately appear under their explanatory topic and their implementation/experiment topic; **implement the underlying capability once**, linking the relevant proposal IDs rather than creating duplicate rules or checks.

### Evidence already available and its limits

- Historical delivery commits: initial implementation `24bcf78957498c8d246d009e64ede5d35d8ecb35`; guess-generation change `0a0e55a42db4b4a50dcfac4e9adbc955195f9f18`. Their pushes were verified during those executions. This document does not repeat remote verification.
- The two delivery ledgers recorded 52 role invocations and 199 events: 8 specification, 20 implementation, 12 verification, 10 review, and 2 shipping invocations. Recorded outcomes were 45 completed, 4 interrupted, 1 usage-limit failure, and 2 unknown. A subsequent audit used the retrospective role. Counts describe those ledgers, not token totals, effort quality, or all service interruptions.
- Go checks, scoped PTY tests, and 50 reference Rust tests were recorded. Differential checks on deterministic synthetic history matched exercised components of 12 strategies. They did not prove complete product equivalence or visual quality.
- There is evidence of genuine red/green cycles for part of the work and of tests added after implementation for other parts. **Integral TDD was not established.**
- The reference specification did include a development results-download script. The Go scope explicitly excluded the updater. Its absence was therefore also a scope-transfer/orchestration failure, not simply a missing source requirement.
- Both specifications described a user data directory by default. The reference development workflow also used an explicit workbook under `docs/`. Installed use and repository development were not reproduced as a complete journey.
- The Go terminal used custom ANSI rendering; the Rust terminal used Ratatui regions/borders. Correct values and keyboard reachability did not establish equivalent readability. This is not an inevitable limitation of Go.
- Source use of all applicable skills at the right time was not demonstrated. UI expertise and early technical alternatives were particularly weakly evidenced. Reading a skill now cannot repair that historical evidence gap.
- An avoidable orchestration stop occurred while authorized corrective work remained. Reboots and usage limits were also reported; these causes must not be conflated. One slow agent's internal cause remains unknown.
- No reliable token/cost totals were available for these runs. Claims that a proposed change will save a particular percentage remain hypotheses until measured.
- The `skills` repository was clean before creating this document; its observed HEAD was `b6a9a96137a7ee996d16bf6eefe7a22648c82703`. Refresh state on resumption rather than assuming this snapshot remains current.

## 1. Executive conclusion

Source topic: “Conclusão executiva”.

- **P01.01 — Define success in terms of use.** Completion criteria must cover the intended user/developer task, operation, and experience alongside numerical or technical correctness. A collection of passing internal tests is insufficient when it does not exercise the promised outcome.
- **P01.02 — Make role inputs and outputs explicit.** Every assignment needs a bounded objective, relevant contracts, ownership, an observable return, and a stop condition. Delegation should reduce uncertainty or produce a deliverable, rather than merely demonstrate that an agent was invoked.
- **P01.03 — Inventory the whole product.** For reproduction/porting work, include utilities, development workflow, data acquisition, startup, configuration, error recovery, and presentation. Classify each relevant component as preserve, adapt, or exclude, with rationale and impact.
- **P01.04 — Build a criterion-to-evidence matrix before implementation.** Link stable requirement IDs to scenarios, the responsible role, an observable acceptance condition, and the check that can establish it. Keep the matrix proportionate and use existing canonical artifacts.
- **P01.05 — Validate an early vertical slice.** Exercise one representative end-to-end journey before expanding the feature surface. The slice must expose operational and presentation risks early enough to change an approach cheaply.
- **P01.06 — Control continuation and context cost.** Specify when to repair, continue, wait, resume, or stop, and bound repeated context transfer and rechecking. Efficiency must preserve checks that found real defects.

## 2. Evidence and limits

Source topic: “Evidência e limites deste relatório”.

- **P02.01 — Label facts, hypotheses, and unknowns.** Use these distinctions in role returns, lessons, and final reports. A plausible cause or prevention measure must not be written as a measured result.
- **P02.02 — State what each check covers.** Record relevant inputs, environment, snapshot, and omissions. A partial differential comparison, source inspection, or one terminal size must remain a scoped result.
- **P02.03 — Preserve unknown invocation outcomes.** Missing returns, interrupted work, and unavailable model or usage attribution remain unknown until reconciled from reliable evidence. Do not infer success from a dispatch or a changed file alone.
- **P02.04 — Separate configured from observed runtime.** Record configured model/effort separately from any independently observed runtime. Token and cost fields may remain unknown; invocation counts are not substitutes.
- **P02.05 — Include user feedback as evidence of product gaps.** Record the task and observed dissatisfaction without turning a single observation into a universal measurement. Do not record delegated decisions as human satisfaction or acceptance.
- **P02.06 — Distinguish source, rendered, and task evidence.** Source code can establish that rendering logic exists; a capture can establish what appeared; a completed task can establish usable interaction. None alone proves every other layer.
- **P02.07 — Record evidence origin and valid reuse.** Mark checks as executed now, inherited from an earlier receipt, or source-inspected. Reused evidence must point to its original execution and explain why the intervening changes do not invalidate it. This avoids both invented reruns and needless reruns.

Cross-project addition: `skills` closure/retrospective evidence showed the value of explicit inherited results and the danger of treating updated receipts as new execution. See the [native-SDD retrospective](agents/runs/native-sdd-process/retrospective.md).

## 3. Lessons from the four user-reported product problems

Source topic: “Os quatro problemas apresentados pelo usuário”. These are generalized process changes, **not an application repair backlog**.

- **P03.01 — Distinguish execution contexts.** Specifications and acceptance scenarios should name repository development, installed use, automated use, and any other materially different context. Paths and data locations must be evaluated against the intended context.
- **P03.02 — Inventory supporting tools and data lifecycle.** Include import/download/update scripts, fixtures, startup commands, configuration, and recovery steps where they are part of the promised journey. A support script can be product scope even when written in a different language.
- **P03.03 — Challenge exclusions against the original objective.** A locally coherent change can still contradict a reproduction request. The specification reviewer and orchestrator must surface that mismatch before implementation.
- **P03.04 — Define readability criteria.** Specify grouping, labels, alignment, units, ordering, density, and representative task questions for displayed statistics. Test the properties that make information understandable, rather than merely checking that a number exists.
- **P03.05 — Establish reference presentation samples.** For equivalence work, identify representative normal, dense, error, and constrained-size views with comparable inputs. Record intentional adaptations without requiring identical source structure or a shared UI library.
- **P03.06 — Validate the operational and visual journey.** Acceptance must connect obtaining/preparing input, launching the program, executing a task, reading its result, and recovering from failure where relevant. Use source, rendered, and task evidence appropriate to each claim.

Excluded work: adding a downloader to ChuteGo, changing its workbook default, redesigning either application's terminal, reformatting its statistics, or changing application dependencies. Those require separate future product work.

## 4. What worked and should be retained

Source topic: “Onde acertamos”.

- **P04.01 — Preserve language-independent domain contracts.** Reuse explicit business rules and independent examples rather than translating source structure. Equivalent behavior may legitimately use different Go and Rust architectures.
- **P04.02 — Report TDD honestly.** Preserve demonstrated red/green sequences, compilation status, command results, and later regression tests. Never relabel a retrospective test as test-first development.
- **P04.03 — Preserve recovery and effect reconciliation.** Before retrying a write, dispatch, commit, or push after interruption, inspect what actually happened. Retain confirmed effects and pending steps without replaying completed actions.
- **P04.04 — Keep independent verification and technical review.** Verification proves acceptance claims; review looks for defects and risks beyond the implementer's assertions. Improve focus and evidence reuse instead of removing controls that found real problems.
- **P04.05 — Keep increments bounded and comparable.** Prefer a coherent slice with explicit interfaces and acceptance. Do not attribute the lower cost of a much smaller change to process improvements without controlling for complexity.

## 5. What failed and how to prevent recurrence

Source topic: “Onde erramos e por que houve tantos erros”.

- **P05.01 — Make exclusions and adaptations visible.** Record their origin and impact in the owning specification. Autonomy to choose implementation details is not authority to silently reduce the user's intended product.
- **P05.02 — Preserve requirement identity and meaning.** During scope reconciliation or specification migration, check stable IDs, business meaning, scenarios, and acceptance semantics. Link correctness alone does not detect a reused identifier or lost behavior.
- **P05.03 — Define the property before writing the assertion.** Cancellation needs evidence of worker cancellation; progress needs monotonicity across the real operation; visibility needs a real viewport. Choose tests from the claim, not from the easiest observable.
- **P05.04 — Generate deterministic metadata with tools.** Obtain timestamps, SHAs, exit status, and file boundaries from reliable tools instead of manually retyping them. Preserve the final reviewed target and verify it where the workflow requires.
- **P05.05 — Inventory the full journey before coding.** Make operating tools, input preparation, startup, error paths, and experience part of early scope work. Avoid allowing final review to become the primary product-discovery phase.
- **P05.06 — Discover material criteria before feature expansion.** Use the acceptance matrix and early slice to expose missing charts, series, progress, preflight, and interaction requirements in analogous projects. Keep independent review capable of finding genuinely new defects.
- **P05.07 — Compare total cost of technical alternatives.** For substantial infrastructure, assess mature libraries, existing tools, and custom implementation for maintenance, license, platform fit, integration, and validation cost. Dependency count is not a sufficient complexity metric.
- **P05.08 — Automate repetitive administration proportionately.** Extend existing deterministic helpers for events, state, fingerprints, and evidence rather than asking models to assemble many fragile commands. Do not build a separate external orchestration system.
- **P05.09 — Make snapshot and gate provenance explicit.** Model what changed, which acceptance claims it affects, and why earlier evidence remains valid. Do not simply relabel a previous green result with a new full-tree fingerprint.

Additional evidence: ChuteGo LL-001 demonstrated an ID collision; Castas specification migration retained requirement/scenario meaning and original archived bytes. General prevention is proposed, not yet measured across future projects.

## 6. Skill use, boundaries, and UI specialization

Source topic: “Skills: foram todas usadas corretamente?”.

- **P06.01 — Select skills by outcome, platform, and risk.** Installed availability is not a reason to load every package. Use the capability appropriate to the current step and explain its expected contribution when that matters to the run.
- **P06.02 — Load only the necessary references.** Keep essential rules in concise entrypoints and read conditional material when the current task needs it. Avoid repeated full-package reading across assignments.
- **P06.03 — Record useful application, not a reading ritual.** Evidence should identify what a skill contributed to the contract, decision, implementation, or check. Opening `SKILL.md` alone is not successful application.
- **P06.04 — Make setup evidence precise.** Distinguish a completed setup execution from an inspection that finds expected files. A structural check cannot retroactively prove every initialization step ran.
- **P06.05 — Use bounded technical research before costly commitments.** Consult the existing research capability for material library, parser, renderer, or runtime decisions. Do not add research for obvious routine choices merely to satisfy a checklist.
- **P06.06 — Apply UI expertise before the interface is fixed.** Use the appropriate UI skill during experience definition and the early slice, then carry its criteria into implementation and acceptance. Late screenshots alone do not repair missing early design decisions.
- **P06.07 — Connect specification, construction, and verification.** Carry stable criteria, relevant design decisions, and evidence expectations through existing handoffs so each skill works from the same promise.
- **P06.08 — Inventory all skill consumers before changing ownership.** Search agents, companion skills, templates, examples, routing, catalogs, metadata, scripts, and evaluations. Update affected destinations and activation instructions coherently.
- **P06.09 — Check host role instructions as well as package bytes.** A current installed package does not prove its host role stopped requiring a retired workflow. In source maintenance, reconcile packaged adapters while preserving model/effort metadata and explicit custom guards; do not update live consumer projects without authority.
- **P06.10 — Split `ui-design` into three distinct packages.** Move web content to `ui-design-web`, Android content to `ui-design-android`, and introduce practical terminal guidance in `ui-design-terminal`. Small initial packages are acceptable if each has a clear activation boundary, usable procedure, evidence expectations, and honest limitations.
- **P06.11 — Complete the split as a supported migration.** Update technology selection, references, agent assets, exports, metadata, catalogs, licensing/attribution, tests, and representative evaluations before retiring the old package. Preserve standalone usability and known customizations; verify an idempotent repeat plan.

### UI split design decisions to carry forward

Benefits: clearer activation, less irrelevant context, stronger platform-specific acceptance, and separate future growth. Risks: duplicated common guidance, content drift, stale consumers, incomplete terminal expertise, and a larger packaging/evaluation surface. Savings are plausible, not measured.

- Put technology/scope selection in the existing role that owns the task. Mixed-platform work can use more than one specialized skill for distinct deliverables; avoid an artificial forced single choice.
- Preserve generic design principles without introducing a mandatory hidden cross-package filesystem dependency. Prefer concise, intentional local common guidance or an explicitly supported dependency strategy. Each standalone package must remain usable after installation by itself.
- Keep web-specific browser/layout behavior in the web package and Android-specific navigation, components, architecture, and accessibility material in the Android package. Inspect existing references and tools before moving or copying them.
- Give the terminal package concrete initial guidance: CLI versus interactive TUI choice, sections and hierarchy, alignment and units, terminal dimensions and resize, selection visibility, keyboard/help, non-color cues, progress/cancellation, error states, output modes where relevant, and rendered/PTY checks. Scope requirements to the actual product; do not make every terminal task implement every feature.
- Preserve useful helpers, assets, tests, licenses, and source notices in their rightful package. Do not mechanically copy web prototype tools into Android or terminal packages.
- Add matching, ambiguous, and non-matching activation cases. Test representative web, native Android, and terminal outcomes separately. Static package validation is not proof of real-host discovery or useful generated UI.
- Retire `ui-design` only after all supported source consumers are reconciled. Document how future installations handle the old name safely; do not silently remove customized installed copies.

## 7. Agent quantity, timing, and responsibilities

Source topic: “Agentes: quantidade, momentos e papéis”. Keep the existing six factory roles plus the host principal orchestrator.

- **P07.01 — Focus shipping on the reviewed revision.** `factory_shipper` must obtain target SHAs from tools, preserve scope and index selections, reuse compatible evidence, run the remaining delivery checks, and verify normal publication when authorized. Shipping success is not a substitute for product acceptance.
- **P07.02 — Bound retrospectives.** `factory_retrospective` receives a compact evidence packet, separates observations from hypotheses, and returns prioritized experiments. It must not trigger another unlimited audit or write competing lessons records.
- **P07.03 — Focus review on technical risks and deltas.** `factory_reviewer` receives requirements, relevant interfaces, changes, prior findings, and verification limits. Re-review coherent fixes and affected boundaries; avoid repeating all earlier verification without a new reason.
- **P07.04 — Give implementers vertical ownership and honest TDD returns.** `factory_implementer` owns an explicit slice/files/interfaces, works test-first where required, and returns changes, actual checks, limitations, and remaining integration needs. It does not declare the entire product accepted.
- **P07.05 — Broaden specification review to the promised journey.** `factory_spec` checks operating tools, startup, data, experience, exclusions, acceptance observables, and preserved reference meaning before code. Internal consistency of a narrowed change is necessary but insufficient.
- **P07.06 — Make product verification observable.** `factory_verifier` maps criteria to evidence and covers relevant operational/visual journeys. Distinguish text presence, rendered organization, task completion, and actual user evaluation; do not claim authority reserved for the developer acceptance gate.
- **P07.07 — Give the orchestrator explicit end-to-end responsibility.** The main session owns scope, dependencies, criteria, decisions, interfaces, integration, context budget, progress, effect reconciliation, and real stop conditions. It must continue authorized repair without creating extra supervisors.
- **P07.08 — Use specialist assignments selectively.** A bounded UI/UX assessment may be justified for interface-heavy work, using the appropriate existing capability. Do not create permanent roles for each quality dimension; demonstrate a recurring capability gap before adding a role.

## 8. Orchestration, pauses, and resumption

Source topic: “Avaliação do orquestrador e das paradas”.

- **P08.01 — Explain material pauses.** Distinguish active waiting, external failure, missing required information, exhausted usage, deliberate user pause, and a workflow gate failure. Do not present ordinary pending authorized repairs as a final stop.
- **P08.02 — Keep a compact resumption state.** Persist the active phase, last confirmed effect, relevant snapshot, pending work, and next action in the existing owning record. Do not create a new run for every prompt, reboot, or retry.
- **P08.03 — Repair within the current phase after a failed gate.** A failed gate blocks advancement, not authorized corrective work. Continue correction and relevant rechecking unless a real blocker, resource limit, explicit stop, or role-specific condition prevents it.
- **P08.04 — Classify failures before editing code.** Separate process launch/permission/sandbox/transport failures from returned assertion failures. Inspect subprocess errors and status; do not weaken tests or broaden permissions merely to obtain green output.
- **P08.05 — Propagate verified environment facts.** Reuse a bounded preflight covering relevant permissions, caches, versions, and working commands. Include facts in downstream packets so each agent does not rediscover the same diagnosed failure.
- **P08.06 — Bound unproductive waiting and retries.** Define useful timeout/check-in behavior and recovery for agents or tools that produce no progress. A timeout is not proof of the agent's internal cause; interrupt or reassign only with effect reconciliation.
- **P08.07 — Inspect effects before repeating actions.** After interruption, verify actual files, index, run state, commits, and remote state where relevant. Retry only the unfinished action; repair recording after confirmed effects rather than replaying them.
- **P08.08 — Align state transitions with user authority and resources.** Preserve authorization across continuation, make consequential missing information explicit, and avoid redundant approval loops. Honest resource exhaustion or a genuine blocker must leave a useful checkpoint rather than a false completion.

Cross-project support: `skills` LL-001 distinguished a real launch restriction from an independent redaction regression. The lesson does not justify dismissing all failures as environmental.

## 9. Token and execution efficiency

Source topic: “Como reduzir consumo de tokens”.

- **P09.01 — Bound tool output and read the relevant delta.** Use focused searches, selected sections, and appropriate output budgets. Avoid repeatedly returning entire files, histories, or unchanged logs.
- **P09.02 — Reuse proved facts within their validity.** Carry reliable findings and evidence references forward. Refresh cheap, drift-sensitive facts when needed; do not repeat expensive verification without a change or unresolved concern.
- **P09.03 — Reduce empty polling and repetitive narration.** Use host-appropriate waits and concise updates when there is progress, a blocker, a meaningful decision, or completion. Preserve user responsiveness without identical messages after every timeout.
- **P09.04 — Default to compact assignment packets.** Include objective, bounded files, IDs/contracts, interfaces, constraints, snapshot, prior findings, and expected return. Give full history only when the task requires it, and measure context insufficiency as a counter-metric.
- **P09.05 — Share one relevant environment preflight.** Propagate tested commands/cache/permission facts rather than repeatedly diagnosing the same host. Do not impose a full environment audit on trivial work.
- **P09.06 — Batch deterministic administrative operations.** Use conventional scripts and tools for metadata, records, and validation. Batch independent reads/checks where safe; keep dependent writes and checks sequential and inspect every result.
- **P09.07 — Fix coherent finding groups before focused re-review.** Consolidate related findings, address the underlying cause, and recheck impacted criteria. Preserve independent judgment; do not hide unrelated defects to reduce round counts.
- **P09.08 — Spend early context on the right criteria.** A complete relevant scope map and vertical slice should reduce costly late discovery. This is a hypothesis to measure, not a reason to expand initial documentation indefinitely.
- **P09.09 — Invalidate gates by affected scope with traceability.** Separate relevant product, documentation, and evidence changes while retaining a reproducible path from checked snapshot to delivered snapshot. Test the replacement contract before weakening current fingerprint safeguards.
- **P09.10 — Capture actual usage only when available.** Prefer host-reported token/cost data with clear attribution and unknowns. Use counts of reads, calls, rounds, and output volume as separate operational metrics, not billing proxies.
- **P09.11 — Evaluate efficiency together with correctness.** Compare similar work for observed cost, elapsed time, escaped defects, late requirements, and user-task outcomes. No percentage savings target or model-tier change is justified by the current evidence alone.

## 10. Corrective and evolutionary maintenance plan

Source topic: “Plano corretivo e evolutivo proposto”. These work items consolidate earlier proposals rather than adding a second implementation for each theme. Local complexity generally increases down the list; priority is explicit.

- **P10.01 [P0] — Clarify execution states and continuation rules.** Update the owning factory/orchestrator instructions with progress, repair, pause, block, completion, and recovery semantics. Completion requires demonstrable outputs, not simply the end of a role's turn.
- **P10.02 [P0] — Add a reusable equivalence inventory.** Provide a proportionate preserve/adapt/exclude structure for ports/reproductions, covering tooling, operation, data, presentation, and business behavior. Keep technology-specific structure optional.
- **P10.03 [P0] — Add criterion ownership and acceptance observables.** Integrate the matrix into existing specification/readiness/handoff artifacts. Avoid creating another canonical requirement list.
- **P10.04 [P1] — Standardize compact handoffs.** Improve existing role packets and returns so they carry sufficient contracts, verified environment, prior evidence, and changed risks without default full-history transfer.
- **P10.05 [P1] — Require proportionate alternatives analysis.** Route consequential infrastructure decisions to bounded research and record maintenance plus proof costs. Do not require comparative research for routine local implementation choices.
- **P10.06 [P1] — Test templates after insertion.** Exercise fresh and customized destinations, exact permanent-section boundaries, unheaded introductions, and preservation of adjacent guidance. Testing the source template alone misses destination-context failures.
- **P10.07 [P1] — Require installation provenance and preservation plans.** Base replacement decisions on the actual installed revision/hash or a justified exact known baseline. Preserve unknown/custom differences as conflicts; arbitrary matching historical blobs must not overwrite intentional local reversions.
- **P10.08 [P1] — Deliver the three UI skills and migrate source consumers.** Implement P06.08–P06.11 together with focused activation and behavior cases. Keep any eventual external consumer rollout separate.
- **P10.09 [P0] — Establish representative rendered acceptance.** Give the verifier/UI capability practical ways to connect reference samples and task criteria to observed presentation. Do not impose screenshot-heavy evaluation on tasks without visual outcomes.
- **P10.10 [P1] — Implement safe evidence reuse and focused re-review.** Define scope-aware validity, original receipt links, and changed-risk justification. Add positive and negative controls so a behavior change cannot inherit an unrelated green gate.
- **P10.11 [P1] — Automate deterministic evidence capture.** Extend existing helpers, where needed, to capture command, real exit status, timestamp, and relevant snapshot without huge logs. Test failure paths and preservation; a pipeline formatter's exit code must not mask a failing test.
- **P10.12 [P1] — Run a representative vertical pilot.** Validate a small authorized workflow with the revised contracts and real observable outcomes before broad adoption. Use isolated fixtures or an explicitly authorized pilot; do not turn ChuteGo/ChuteGPT into write targets.
- **P10.13 [P2] — Add optional, privacy-respecting usage observation.** Only where supported, record actual usage without copying prompts or credentials. Leave unavailable data unknown and avoid mandatory global hooks or a duplicate telemetry system.
- **P10.14 [P2] — Run a comparable process experiment.** Establish a baseline and similar tasks, maintain independent grading and fixed controls, and evaluate quality alongside efficiency. A single successful smoke trial is not a causal proof of savings.

## 11. Acceptance criteria for the next experiment

Source topic: “Critérios sugeridos para o próximo experimento”. These criteria evaluate the revised process; they are not claims that it already meets them.

- **P11.01 — Explicit completion output.** Final handoff separates delivered behavior, unresolved differences, checks, publication state, and local-only artifacts.
- **P11.02 — Honest metrics and uncertainty.** Every reported result has the right evidence class; unavailable costs, runtime attribution, and missing returns are not guessed.
- **P11.03 — Explain each additional round.** Record what changed, the risk/criterion affected, and the focused check needed. Avoid requiring a new full audit merely because another round occurred.
- **P11.04 — Do not repeat a diagnosed setup failure unchanged.** Later assignments receive the verified workaround/configuration within authorized boundaries. A genuinely changed environment can justify a fresh diagnosis.
- **P11.05 — Inventory relevant product components before code.** The exercise includes operational tools and experience, with explicit preserve/adapt/exclude decisions and no silent loss of promised scope.
- **P11.06 — Tie approval to the claimed observable.** Source inspection, passing tests, rendered samples, task execution, and user evaluation remain distinct. A gate can pass only the claim its evidence supports.
- **P11.07 — Evaluate an early end-to-end journey.** Exercise relevant input preparation, launch, a representative task, presentation, and error recovery. Delegated decisions must not be recorded as observed user satisfaction.
- **P11.08 — Diagnose repeated non-progress.** Repeated similar failures trigger investigation of the underlying cause instead of indefinite identical attempts. Preserve actual retry limits and stop conditions of the current workflow.
- **P11.09 — Verify semantic closure separately from links.** Compare acceptance, disposition, execution receipts, and archive/current status. Preserve historical statements as historical rather than rewriting old records to make them look current.
- **P11.10 — Prove idempotent, non-destructive setup/upgrade planning.** An already applied plan produces no changes. Tests cover accurate baselines, intentional local reversions, unknown customizations, safe targets/concurrency, index/history/log preservation, and template boundaries.
- **P11.11 — Exercise both ends of important boundaries.** Follow realistic inputs through parsing, transformation, and presentation; follow interaction state into the actual viewport. Retain relevant negative controls without claiming one fixture proves every platform.
- **P11.12 — Establish a baseline before savings targets.** Compare sufficiently similar tasks with known measurement limits. Report counter-evidence and quality regressions even if context or tool-call counts fall.

## 12. Recommended decision

Source topic: “Decisão recomendada”.

- **P12.01 — Keep the framework and current roles.** Preserve useful technical discipline and independent controls; adjust demonstrated weak contracts rather than expanding the organization by default.
- **P12.02 — Validate a smaller complete journey first.** Prefer an observable vertical outcome over premature expansion across the entire feature catalog.
- **P12.03 — Correct orchestration behavior.** Make continuation, recovery, dependencies, bounded handoffs, and genuine stop conditions explicit in the existing owner.
- **P12.04 — Treat functional and experiential equivalence together.** Preserve language independence while making operational and presentation acceptance concrete when the product requires it.
- **P12.05 — Reduce context and manual administration deliberately.** Remove duplication and repeated diagnosis; preserve the evidence and checks needed to detect real defects.
- **P12.06 — Measure before scaling.** Demonstrate useful outcomes in a controlled pilot and then compare quality and observed cost. Do not claim that the revised factory is efficient or universally reliable before evaluation.

## Cross-project lessons incorporated

The last discussion-stage inspection identified seven projects under `/home/dever/workspace/teknolista` with `docs/agents`: `castas`, `chutego`, `chutegpt`, `skills`, `softheca`, `teknolista`, and `teknolista.github.io`. ChuteGo and skills contained populated lessons records. The other five lessons files were templates without substantive entries; useful migration reviews also existed in Castas and ChuteGPT. Empty templates are not evidence of successful learning or missing execution. Historical references to `yo-fi` in adoption receipts do not establish that it was present in the inspected root.

| Source lesson/record | Observed finding and limitation | Incorporated proposals |
| --- | --- | --- |
| ChuteGo LL-001 | Reused requirement ID had conflicting meaning; corrected locally. Broader prevention remains proposed. | P05.02 |
| ChuteGo LL-002 | Decimal parsing and large monetary presentation boundaries failed despite other tests; targeted corrections/re-review passed. | P03.04, P05.03, P11.11 |
| ChuteGo LL-003 | State tests passed while selected content/chart was missing in a real viewport; focused PTY reproduction found it. | P02.06, P06.10, P11.11 |
| ChuteGo LL-004 | Progress/charts/keyboard/preflight criteria emerged late. The acceptance-matrix efficiency benefit has no controlled comparison yet. | P01.04, P05.06, P09.08 |
| Skills LL-001 | Restricted process launch was distinguishable from a separate real redaction regression. Do not generalize an environment excuse. | P08.04, P08.05 |
| Skills LL-002 | Owner migration left callers/routing/examples inconsistent until corrected. General model behavior was not exhaustively tested. | P06.08, P06.11 |
| Skills LL-003 | Valid paths coexisted with stale acceptance/archive status. Corrected locally; historical publication was not thereby disproved. | P11.09 |
| Skills LL-004 | Permanent-section extraction/insertion could absorb temporary or unheaded neighboring content. Destination regressions were added. | P10.06, P11.10 |
| Skills LL-005 | A draft updater could misclassify an intentional old-content reversion as stock. Corrected before actual adoption; no real loss observed. | P10.07, P11.10 |
| Skills LL-006 | All 192 packages matched source while 84 host profiles needed workflow reconciliation. Package equality did not establish selected runtime behavior. | P06.09, P06.11 |
| Castas/ChuteGPT migration reviews | Requirements/scenarios and original historical content were preserved while links/status needed separate attention. | P05.02, P11.09 |
| Native-SDD/consumer receipts | Evidence inheritance, confirmed-effect recovery, preservation and zero-change reruns were useful controls; not a proof of all-host operation. | P02.07, P04.03, P11.10 |

### Evidence references

Read only what is needed for the active work item. Do not restart an audit of every project merely because these links are available.

- ChuteGo critical retrospective, 2026-11-25 (`/home/dever/workspace/teknolista/chutego/docs/agents/relatorio-retrospectiva-chutego-pentapro-2026-11-25.md`).
- Earlier consolidated product/process report (`/home/dever/workspace/teknolista/chutego/docs/agents/relatorio-consolidado-pentapro.md`).
- ChuteGo lessons (`/home/dever/workspace/teknolista/chutego/docs/agents/lessons-learned.md`).
- Initial delivery ledger (`/home/dever/workspace/teknolista/chutego/docs/agents/runs/historical-analysis/events.jsonl`) and change ledger (`/home/dever/workspace/teknolista/chutego/docs/agents/runs/uniform-picks/events.jsonl`).
- [Skills lessons](agents/lessons-learned.md).
- [Native-SDD retrospective](agents/runs/native-sdd-process/retrospective.md) and [closure evidence](agents/runs/native-sdd-process/closure-evidence.md).
- [Invocation-history retrospective](agents/runs/factory-invocation-history/retrospective.md), [correction review](agents/runs/factory-invocation-history/review-final.md), [rollout review](agents/runs/factory-invocation-history/rollout-review.md), and [consumer receipt](agents/runs/factory-invocation-history/consumer-update.md).
- [Role/profile maintenance evidence](agents/runs/workspace-git-delivery/maintenance-evidence.md).
- Castas migration review (`/home/dever/workspace/teknolista/castas/docs/agents/runs/specification-migration/review.md`) and ChuteGPT migration review (`/home/dever/workspace/teknolista/chutegpt/docs/agents/runs/specification-migration/review.md`).

Application evidence is referenced by absolute path, not copied or edited. Cross-repository sources are plain paths because collection validation requires Markdown links to stay within the collection. This plan can be read independently; inspecting those sources requires the corresponding sibling repositories. Collection-local evidence retains navigable relative links.

## Likely implementation owners and affected surfaces

These are starting points, not an authorization to change every listed file. Inspect current source and callers for each increment. Some safeguards already exist; tighten or evaluate them rather than duplicating them.

| Capability | Canonical starting owner | Other surfaces to inspect when affected |
| --- | --- | --- |
| Lifecycle, continuation, role packets, evidence reuse | `skills/software-factory/SKILL.md`, its references and existing record helper | `skills/software-factory/agents/`, supported host profiles, `docs/software-factory-workflow.md` |
| Acceptance, equivalence, requirement identity | `skills/penta-pro/SKILL.md` and its templates/references | native change artifacts, readiness/spec-review guidance; preserve five pillars |
| Bounded slices and shared environment | `skills/software-delivery/SKILL.md` | implementer packets and interfaces |
| Test-first evidence and meaningful assertions | `skills/behavior-testing/SKILL.md` | platform testing skills when applicable, verifier guidance |
| Risk/delta review and exact delivery | `skills/peer-review/SKILL.md`, `skills/git-ship/SKILL.md` | reviewer and shipper assets; retain independent checks and actual action authority |
| Alternatives and context discipline | `skills/technical-research/SKILL.md`, `skills/agent-instructions/SKILL.md` | relevant decision templates and assignment contracts |
| Setup and safe installation updates | `skills/setup-pentapro/SKILL.md`, existing package/update helpers | permanent-section templates, installed baseline/lock handling, preservation tests |
| Three UI packages | current `skills/ui-design/` source, then the three replacements | all skill/role consumers, package-local references/assets/tools/tests and notices |
| Routing, distribution, and evaluation | `SKILL-ROUTING.md`, `README.md`, `plugin.json`, `SKILL-EVALUATION.md` | `scripts/package_plugin.py`, collection validation, eval cases, generated host metadata, CI |

Do not silently impose new model tiers. Preserve configured role identities/model/effort by host; a role template is not evidence of host availability or actual selection. Use one record per real execution and the current invocation-event contract, not a new project-wide parallel log.

## Suggested implementation sequence after credits renew

1. **Resume and reconcile.** Read this plan and the current `skills/AGENTS.md`; inspect Git status, current workflow and relevant lessons. Confirm the concrete execution authority from the new user prompt. Do not reread all historical evidence. Identify already-implemented safeguards and remaining deltas.
2. **Specify the bounded maintenance change(s).** Use the current official native PentaPRO workflow when implementation is requested. Map proposal IDs to acceptance, owners, and affected source consumers. Document deliberate consolidation or a conflict that needs resolution; do not silently drop proposals.
3. **Implement the foundational contracts.** Address P0 scope/acceptance, continuation, evidence classes, and role responsibilities, with compact handoffs and proportionate supporting changes. Establish relevant evaluation cases before revising substantive instructions. For executable helpers, show a meaningful failing case before the fix and a passing case after it.
4. **Migrate UI skills coherently.** Inventory consumers first; implement the three packages and selection rules; reconcile exports/catalogs/evals/agent assets; then retire the old source package. Test standalone installation and preservation behavior without changing live application projects.
5. **Complete deterministic helpers and validity rules.** Extend existing recording/update helpers only where needed. Exercise exit-code handling, stale/custom provenance, template destinations, idempotence, safe-target/concurrent-change refusal, and evidence invalidation controls.
6. **Verify and independently review the integrated source.** Follow the current official roles and gates, using compact packets and focused rechecks. State which evaluations actually ran and which remain unavailable. Do not substitute structural checks for behavioral validation.
7. **Run the pilot and report.** Use an authorized isolated fixture or pilot, compare observable quality and available cost, and record bounded lessons. Broader comparative measurement or host discovery that cannot run remains explicit pending evidence, not a fabricated pass.
8. **Deliver only as authorized.** At the applicable acceptance point, report source changes, unresolved limits and checks. Commit/push only within authority granted for that future execution, preserving unrelated work and verifying actual publication when performed. Keep external consumer rollout separate.

### Validation to refresh from current repository instructions

For instruction, metadata, and link changes, the current root instructions require:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_collection.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_skill_evals.py --check-cases
git diff --check
```

Run affected helper tests for executable changes and the package/export tests for the UI split. Obtain exact commands from the current README/CI rather than copying a stale guessed suite. Use existing suitable runtimes; do not install global dependencies merely for documentation. Distinguish static validation, authored cases, actual model trials, native-host integration, and controlled comparisons. Record unavailable trials honestly and preserve mandatory gates.

### Checkpoint discipline

At meaningful phase boundaries in the future execution, update the existing canonical record with status, changed artifacts, evidence origins/snapshots, pending work, and relevant commits. Use deterministic tools for timestamps/SHAs/exit codes. After interruption inspect confirmed effects first; do not create redundant runs or repeat confirmed pushes just to update an old note.

### Copy-ready resumption prompt

```text
Retome a manutenção do PentaPRO no repositório /home/dever/workspace/teknolista/pentapro.
Leia docs/pentapro-improvement-plan-2026-11-25.md e o AGENTS.md atual.
Implemente as propostas consolidadas desse plano no PentaPRO, seguindo o fluxo oficial
atual, os agentes obrigatórios, os testes e os quality gates aplicáveis. Antes de editar,
confronte o plano com o estado atual para não duplicar melhorias já existentes.
Não altere ChuteGo, ChuteGPT, outros projetos consumidores nem configurações globais.
Substitua ui-design por ui-design-web, ui-design-android e ui-design-terminal com migração
coerente dos consumidores no código-fonte da coleção. Preserve customizações e históricos.
Trabalhe na sessão atual; não inicie outro Codex ou orquestrador externo. Use contextos
compactos, ferramentas determinísticas e somente as referências necessárias à etapa.
Registre evidência real, checkpoints e pendências; diferencie resultados executados,
herdados, hipóteses e informações indisponíveis. Continue as correções autorizadas até
a conclusão ou um bloqueio real/limite de uso. Não faça commit ou push neste pedido;
apresente o resultado revisável e os limites para decidirmos a publicação depois.
```

The prompt deliberately requests local implementation and leaves publication for a later decision. The user may explicitly change that authority when resuming.

## Checkpoint at document creation

- Status: proposal/context persistence completed; PentaPRO implementation not started by this request.
- Artifact: `docs/pentapro-improvement-plan-2026-11-25.md` in the `skills` repository.
- Content: full descriptive proposal inventory in the original 12-topic order, later lessons additions, UI split decisions, source references, likely owners, validation expectations, execution sequence, and resumption prompt.
- Changes to operational PentaPRO source or application products: none from this persistence task. Required local prompt-log appends are separate, private administrative records.
- Commit/push: none requested or performed. The document remains a local artifact until a later authorized delivery.
- Pending: implementation, relevant new tests/evaluations, official technical review, pilot, usage measurement if available, and any separately authorized publication/consumer rollout.
