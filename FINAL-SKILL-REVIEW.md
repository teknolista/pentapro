# Final skill maintenance review

Latest assessment: see [review-report follow-up](docs/review-followup-2026-11-22.md). Earlier sections are dated maintenance records, not the current catalog.

This record contains successive reviews. Earlier dates, counts and versions describe their original snapshots. See the [current collection review](#current-collection-review) for the latest pass. The [README catalog](README.md#available-skills) owns current package versions.

Date: 2026-11-09. Scope: the current working collection of 21 packages, including the preceding maintenance changes on top of `95abba607180cda548749edb76034efe5dbcac32`. This is a maintainer self-review, not an independent approval or a claim of globally optimal skills.

## Assessment

Read every skill entrypoint and traced selected supporting procedures, technical examples, ownership boundaries and evaluation tooling. Checked activation, task scope, SDD and non-SDD contracts, safety, completion evidence and version-sensitive guidance. Supporting materials received targeted inspection; historical source notes, every template field and every platform/library combination were not independently revalidated in this pass.

The collection's division of responsibility is suitable for the stated development workflow. Keep requirements, implementation, tests, independent review, security and publication as distinct outcomes with explicit handoffs. More instructions are useful only when they change a relevant decision; a longer universal checklist would not establish higher quality.

| Package | Disposition and assessed contract |
| --- | --- |
| [PentaPRO](skills/penta-pro/SKILL.md) | Retain. Five pillars, accepted versus proposed changes, stable IDs and external SDD ownership remain coherent. Readiness does not authorize implementation. |
| [Software Delivery](skills/software-delivery/SKILL.md) | Retain. Executes dependent increments using accepted SDD records or ordinary contracts; verifies integrated results and preserves unfinished gates. |
| [Technical Research](skills/technical-research/SKILL.md) | Retain. Primary evidence, version applicability, bounded experiments and honest uncertainty; no automatic production promotion. |
| [Diagnose Defect](skills/diagnose-defect/SKILL.md) | Retain. Reproduction, working control, distinguishing hypotheses and scoped remediation; no unsupported cause claim. |
| [Behavior Testing](skills/behavior-testing/SKILL.md) | Retain. Independent expectations, meaningful red phase when applicable, runtime-specific boundaries and test-only scope. |
| [HTTP API](skills/http-api/SKILL.md) | Clarify outbound security. Preserve compatibility, authorization, durable effect/retry semantics and supported consumer behavior. |
| [MCP Server](skills/mcp-server/SKILL.md) | Retain. Separate protocol revision from SDK support, legacy/modern lifecycle, server enforcement and application idempotency. |
| [Peer Review](skills/peer-review/SKILL.md) | Retain. Source-backed findings, counterevidence, snapshot freshness and distinct verification/independence claims. |
| [Cybersecurity](skills/cybersec/SKILL.md) | Retain. Threat-to-control evidence, actual effect boundaries, allowed/denied controls, residual risk and authorization. |
| [UI Design](skills/ui-design/SKILL.md) | Correct documentation scope. Preserve platform-aware interaction/accessibility checks and distinguish specifications, concepts and runtime evidence. |
| [Git Ship](skills/git-ship/SKILL.md) | Retain. Reviewed snapshot, unrelated index preservation, explicit destinations and remote confirmation; no implicit merge/deploy. |
| [Agent Instructions](skills/agent-instructions/SKILL.md) | Strengthen evaluation integrity. Small useful owners, conditional references, verified isolation and honest comparison limits. |
| [Android Module Structure](skills/android-module-structure/SKILL.md) | Retain. Actual AGP/Kotlin mode, compatible conventions, explicit dependencies and release evidence. |
| [Android Data Layer](skills/android-data-layer/SKILL.md) | Retain. Atomic storage, migration and query semantics, account boundaries and uncertain remote outcomes. |
| [Android Error Handling](skills/android-error-handling/SKILL.md) | Retain. Typed expected failures, cancellation propagation, transport-specific mapping and visible programming defects. |
| [Android DI Koin](skills/android-di-koin/SKILL.md) | Retain. Actual API version, owner/lifetime, parameterized resolution and graph-check limits. |
| [Android Background](skills/android-background/SKILL.md) | Retain. Persistent work, bounded retries, stable operation identity, cancellation limits and account-switch enforcement. |
| [Android Unit Testing](skills/android-unit-testing/SKILL.md) | Retain. Shared scheduler, controlled suspension, meaningful assertions and correct restoration limits. |
| [Android Integration Testing](skills/android-integration-testing/SKILL.md) | Retain. Real storage/transport boundaries, historical migrations, negative-test reachability and legitimate controls. |
| [Android UI Testing](skills/android-ui-testing/SKILL.md) | Retain. Installed test APIs, real input, synchronization and device/assistive evidence limits. |
| [PR Quiz](skills/pr-quiz/SKILL.md) | Retain. Explicit educational scope, publication authority and revision-bound informational results; no security/review approval claim. |

## Corrections and evidence

1. **UI scope contradiction, corrected.** The document-maintenance reference said an invocation normally creates a document, while the entrypoint made documentation conditional. A localized UI implementation could therefore acquire an unnecessary specification deliverable. The reference and description now distinguish specification work from localized implementation and read-only review. Existing authoritative contracts still receive scoped updates when affected. Version: `1.5.6`.
2. **Outbound HTTP boundary, clarified.** Added conditional destination/credential enforcement for caller-controlled URLs and redirect hops, bounded response processing and allowed/denied endpoint checks. This puts a relevant implementation constraint in the API owner without requiring a full security audit for ordinary endpoint work. Basis: [OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html). Version: `1.1.1`. No live integration or new model-comparison gain is claimed.
3. **Evaluation isolation claims, qualified.** Evaluator files outside a task workspace may remain readable; directory separation is not confidentiality. The portable evaluation procedure now requires checking that boundary or disclosing it. Local trial documentation explicitly records that read isolation was not established. Prior measured results remain unchanged and exploratory. Agent Instructions version: `1.0.1`.
4. **Evaluation process lifetime, fixed.** A synthetic child wrote after `subprocess.run(timeout=...)` had terminated its parent. The runner now starts a POSIX process group and kills that group on timeout or an exception while waiting. A regression test confirms the child started and cannot perform the later write. The same test failed on the former behavior; success and nonzero-exit controls passed. The CI workflow includes these offline tests. Basis: [Python subprocess semantics](https://docs.python.org/3/library/subprocess.html). Process groups are cleanup, not a security sandbox for deliberately detached processes or external effects.

Current official documentation was also consulted for [AGP built-in Kotlin](https://developer.android.com/build/migrate-to-built-in-kotlin), [Koin verification](https://insert-koin.io/docs/reference/koin-test/verify/), [Compose v2 testing](https://developer.android.com/develop/ui/compose/testing/migrate-v2), and [MCP revision changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog). No conflicting rule requiring another change was established in those inspected paths. Consuming projects must still resolve their actual versions.

## Validation and limits

- All 21 packages passed the installed skill-creator `quick_validate.py`.
- Collection metadata, catalog versions and local links/anchors passed `scripts/validate_collection.py`.
- 64 offline checks passed: 3 evaluator lifecycle tests, 24 UI helper tests, 12 PR publisher tests and 25 Node grader scenarios.
- The lifecycle negative control failed for the intended late-write assertion under the old implementation, and passed with the correction.
- Whitespace validation passed. The CI workflow was parsed locally; hosted execution remains pending publication.

The previous [model trial results](evals/RESULTS.md) retain their original snapshots and limitations. The wording changes received source and contract review. Consuming Android builds, browser and assistive sessions, production security checks and the complete MCP client matrix remain project-specific verification.

No substantiated blocker remains in the inspected maintenance scope after these corrections. This supports using the collection with actual project checks; it does not establish exhaustive correctness, universal model efficacy or security certification. Changes remain local, with no commit, push or deployment performed.

## Distribution review

The maintenance snapshot was subsequently published as `bbd941da590e84c4594cd45d49e3aab9fd0d852e`. The [hosted validation run](https://github.com/teknolista/pentapro/actions/runs/42731202186) passed for that commit. This run is evidence for the published snapshot. The distribution corrections below were checked locally.

The README now uses one version catalog. The README, project template, routing guide and UI evaluation cases describe the same documentation scope and task ownership as the entrypoints. The seven synthetic case definitions still resolve to their intended fixtures and owners. The earlier trial count, routing observations and input-token figures were checked against the retained run summaries. The original trial scope and limitations remain in the [trial record](evals/RESULTS.md).

The local source comparison found matching material in five references embedded in UI Design and Cybersecurity, in addition to the nine standalone imports already recorded. The maintainer subsequently confirmed MIT redistribution permission for all imported material. All 21 packages declare MIT and carry a matching license notice with source attribution. See the [affected paths and provenance](THIRD-PARTY-NOTICES.md#pl-coding-android-and-pr-quiz-skills).

The local review passed collection and skill metadata validation, checked the four UI metadata files, and passed all 64 offline helper tests and the in-process MCP SDK smoke test. The current validator requires MIT metadata and the canonical notice in every package. After the license update, Skills CLI `1.7.6` installed all 21 packages from a local source into a disposable Codex project. Every installed file matched its source bytes, including all 21 license notices.

## Adaptive specification and delivery review

Reviewed on 2026-11-10 against `a910ca37f86ef48b6cb0a09b9569933249534346` and the supplied analyses. The collection already separated requirements, implementation, testing, review and release authority. It already supported persistent specifications, external change records, work without a formal SDD framework and isolated experiments. The gap was how to decide among these modes and how to handle a transition when implementation exposes a consequential ambiguity or an experiment becomes maintained software.

- [Software Delivery 1.2.0](skills/software-delivery/SKILL.md) keeps its dependent-task trigger. Its [change contract guide](skills/software-delivery/references/change-contracts.md) addresses readiness, escalation, experiment adoption, authoritative generation sources and reconciliation of implementation with the agreed contract.
- [PentaPRO 2.7.0](skills/penta-pro/SKILL.md) distinguishes readiness for an increment from a requirement to specify the entire selected scope before coding. The PROCESS template and document maintenance guidance make the handoff reconstructible from the saved artifacts and recognize governed schemas, policies and checks.
- The [README](README.md#choose-a-workflow), [routing guide](SKILL-ROUTING.md#choose-the-depth-of-the-workflow) and [project template](skills/setup-pentapro/assets/agents.md#skill-selection-and-coordination) expose the same decisions for direct edits, exploration and specified work. Existing domain skills continue to own their checks. The [evaluation procedure](SKILL-EVALUATION.md#score-the-outputs) includes cases for the new boundaries.

The review adopted the analyses' separation of agent authority, specification depth and verification. Numeric autonomy levels and a fixed risk score would not establish authority or cover cases where one consequence determines the workflow. Persistent contracts fit maintained behavior. Spec-as-source applies where the project already has a governing input and regeneration process. Automatic pipeline autonomy and universal code generation remain outside the demonstrated scope. [Berkeley position paper and overview](https://rdi.berkeley.edu/blog/auto-software-dev/) · [Böckeler's SDD taxonomy](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) · [NCSC guidance on oversight](https://www.ncsc.gov.uk/blogs/the-vibe-coding-spectrum-approach-to-ai-assisted-software-development)

The evidence favors testing specific practices. Practitioner reports describe selective use and additional review costs. The ESEM study analyzed mainly ticket references and did not evaluate adoption of SDD tools. Google's bug-detection gain concerns its contract-guided test generator on the studied tasks. The earlier local token observations compare skill snapshots on matched fixtures, with HTTP API as the localized implementation owner. They do not isolate the effect of adopting SDD. [Practitioner study](https://arxiv.org/abs/2608.25202v4) · [ESEM study](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.84) · [Google test generation study](https://research.google/pubs/grounding-ai-agents-in-contracts-an-empirical-evaluation-of-spec-driven-test-generation/) · [Local trial record](evals/RESULTS.md)

All 21 skill packages passed metadata validation. The collection validator checked local links, catalog versions and standalone notices. All 64 offline helper tests passed. The [adaptive workflow trial record](evals/RESULTS.md#adaptive-workflow-checks-2026-11-10) reports the exercised boundaries and remaining limits separately.

## Collection and installation verification

Reviewed on 2026-11-10 on the working snapshot over `a910ca3`. Read all 21 entrypoints against their intended tasks, routing, authority, and evidence requirements. Traced selected supporting contracts and executable paths, including Android version-sensitive guidance, MCP protocol revision handling, the UI gallery, and PR quiz publication and grading. The README now distinguishes [root maintenance directories](README.md#repository-structure) from packaged resources.

- [UI Design 1.5.7](skills/ui-design/SKILL.md) rejects malformed comment forms that the build-time parser and Chromium can interpret differently. A synthetic fragment passed the old builder and executed its script in Chromium. The new builder rejects that fragment without replacing the previous export. A separate Chromium control confirmed that the generated hash policy blocks the unexpected script while still running the bundled viewer. The regular gallery also opened the requested state, theme and width from a deep link. The helper remains intended for reviewed local inputs.
- [PR Quiz 1.2.3](skills/pr-quiz/SKILL.md) checks the current token and sender eligibility before answer comments can change a status or result comment. The former handler wrote state for some ineligible submissions, including malformed ones. Offline regressions cover authors, outsiders, malformed answers, and missing quiz metadata. PR lifecycle events still report missing or malformed quizzes, and eligible reviewers can still grade the current revision.
- Skills CLI 1.7.6 installed all 21 packages from a disposable copy of the working snapshot using `--copy`. The installed files matched their source bytes, including licenses and nested resources. Root `evals/` and `scripts/` stayed outside the target project.

Collection validation, all skill entrypoint checks, four host metadata checks, nine evaluation case definitions and whitespace validation passed. The 68 offline tests include 3 runner lifecycle tests, 26 UI helper tests, 12 PR publisher tests and 27 grader scenarios. The MCP Python SDK 2.2.0 in-process smoke test passed for the legacy and modern paths in the fixture. The browser and API doubles cover the stated reproductions. Live GitHub workflow execution, consuming Android builds and device tests, production services, and additional model comparisons were outside this pass.

## Final adoption review

Reviewed again on 2026-11-10 against the working collection over `a910ca3`. Read all 21 entrypoints and checked their task boundaries against routing, installation guidance, project instructions and the existing assessment. Supporting procedures and executable paths received targeted inspection, including specification ownership and readiness, Android storage/session boundaries, version-sensitive build/test/DI guidance, MCP revision handling, UI gallery output, PR publication/grading and evaluation-process cleanup. This is a maintainer self-review. It is not an independent approval or an exhaustive audit of every reference and platform combination.

No additional substantiated skill-instruction defect was found in this pass. Preserve the current instructions and versions instead of expanding them without a demonstrated need. The README now supplies a first-task adoption path, describes actual coverage and project-specific verification, and gives the complete offline maintenance commands and prerequisites. Its installation wording now accounts for symbolic links and explicit `--copy`, as documented by the [Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#installation-methods). Root maintenance directories remain outside installed skill packages.

Rechecked primary documentation for the [Agent Skills format](https://agentskills.io/specification), [AGP built-in Kotlin](https://developer.android.com/build/migrate-to-built-in-kotlin), [Koin verification](https://insert-koin.io/docs/reference/koin-test/verify/), [Compose v2 test environments](https://developer.android.com/develop/ui/compose/testing/migrate-v2), and [MCP revision changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog). The inspected guidance still requires matching a consuming project's actual versions. Historical source and evaluation records retain their original evidence; this review does not turn them into new trials.

Fresh local verification passed all 21 skill metadata checks, collection metadata/catalog/license/link validation, and all 68 offline tests (3 evaluator lifecycle, 26 UI helper, 12 PR publisher and 27 grader scenarios). The local runtimes were Python 3.12.6 and Node.js 26.10.0; hosted CI declares Python 3.12 and Node.js 24. The exact reproduction commands are in [README validation](README.md#validation-and-improvement). Whitespace checks passed. The root MIT notice and standalone notices remain aligned, using the maintainer's recorded redistribution authorization.

No blocking finding remains in the inspected collection scope. The collection is usable with the documented prerequisites and project checks. Universal correctness, security certification, effectiveness on every model and readiness of every generated application are not established. This pass did not repeat model comparisons, browser/device sessions, the MCP SDK smoke test, installation trials or hosted CI; their earlier results remain scoped to their recorded snapshots. Publication of the pending changes is a separate step; this pass created no commit or push.

## Production Operations addition

On 2026-11-10 the collection added [Production Operations](skills/production-operations/SKILL.md) as its 22nd package. It owns hosted backend planning, pipeline and infrastructure configuration, authorized deployment, runtime verification and recovery. PentaPRO retains specification, Software Delivery retains dependent application implementation, and Git Ship retains Git publication. The package ships five conditional provider guides, two adaptable templates, worked examples and [offline evaluation scenarios](skills/production-operations/evals/scenarios.md). Its [source notes](skills/production-operations/references/sources.md) record original synthesis and linked primary references. The earlier validation records refer to their own snapshots.

Local validation passed all 22 skill metadata checks, the collection catalog/license/link validator and all 68 offline helper tests. Skills CLI 1.7.6 installed only the new package into a disposable Codex project, where its 18 files matched the source byte for byte.

Two independent same-model forward scenarios exercised planning and safety decisions without cloud access. A Cloud Run runner context mismatch and partial backfill prompted explicit cross-project federation and job execution reconciliation guidance. A Cloudflare staging binding to production data and a Durable Object rename prompted exact lifecycle and rollback rules and checks of the prior revision's bindings. These runs exercised responses to fictional inputs. They supplied no live deployment, provider login, MCP connection, recovery or comparative model evidence.

### Integration follow-up

The adoption path and capability table now route hosted work to Production Operations. The [evaluation runner](SKILL-EVALUATION.md#score-the-outputs) registers a synthetic target mismatch and partial migration fixture. The follow-up verified fixture and owner paths. The new runner case has no model trial result yet.

The existing [GitHub validation workflow](.github/workflows/validate.yml) discovers root skill packages through the collection validator. A disposable Git snapshot passed, and separate controls rejected a missing AWS guide and a mismatched README version for Production Operations. All 22 packages, 768 local links and anchors, and 68 offline tests passed in the follow-up. Hosted CI and live cloud deployment were outside these checks.


## 22-package closing review

Date: 2026-11-10. Reviewed the local collection over `648fe9c`, preserving the pending Production Operations addition and integration changes. This was a maintainer self-review. Read all 22 entrypoints, checked their requested outcomes, authority, failure handling and evidence requirements, and traced selected security, Android, MCP, delivery and operations references. Checked the catalog, routing, project template, provenance, installation instructions and validation workflow. Supporting references received risk-directed inspection, not exhaustive re-execution of every example.

| Packages | Assessment |
| --- | --- |
| PentaPRO; Software Delivery; Agent Instructions | Keep the separation of accepted contracts, proposals, implementation authority and observed evidence. Existing SDD records remain canonical; ordinary scoped work does not need a new specification framework. |
| Technical Research; Diagnose Defect | Keep primary-source applicability, bounded experiments, controls and cause uncertainty. A plausible explanation is not a reproduced cause. |
| HTTP API; MCP Server | Keep tenant/resource authorization, compatibility, uncertain outcomes and durable idempotency. Protocol revision and actual SDK/client support remain separate checks. |
| Behavior Testing; Android Unit Testing; Android Integration Testing; Android UI Testing | Keep independent expectations, actual failure boundaries, deterministic scheduling and the distinction between mocked, host, device and live-service evidence. |
| Android Module Structure; Android Data Layer; Android Error Handling; Android DI Koin; Android Background | Keep version-aware examples, cancellation, account-bound commits, migration preservation, component ownership and effective startup/release checks. |
| UI Design; Peer Review; Cybersecurity | Keep observable interaction/accessibility contracts, substantiated findings, threat/control evidence, actual independence and scoped verdicts. No additional instruction defect was established in the inspected paths. |
| Git Ship; PR Quiz; Production Operations | Keep publication and deployment scoped to actual authorization, exact revision/target verification and recovery. The quiz remains an educational aid. Provider access and real deployment remain environment-specific. |

Rechecked the [Agent Skills specification](https://agentskills.io/specification), [AGP built-in Kotlin](https://developer.android.com/build/migrate-to-built-in-kotlin), [Koin verification](https://insert-koin.io/docs/reference/koin-test/verify/), [Compose v2 testing](https://developer.android.com/develop/ui/compose/testing/migrate-v2), and [MCP revision changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog). No new third-party skill implementation was incorporated. Existing notices and runtime package versions remain unchanged.

### Corrections to the collection gate

- The anchor validator previously counted headings inside fenced code. A link could therefore pass without a rendered heading, and an example could shift duplicate-heading numbering. Link and heading checks now share the same fenced-example filtering.
- Optional host metadata was not checked by the automated collection gate. It now checks YAML mapping shape and duplicate keys, supported UI fields, owner invocation in the default prompt, packaged icon paths, color syntax and boolean invocation policy. Files remain optional; this does not claim full host-schema or runtime-discovery validation.
- Added 12 offline validator regression/control tests. Six negative cases failed under the old gate because invalid fixtures were accepted; all now pass with the correction. The tests also cover valid collections, real duplicate headings, ignored targets, catalog drift and valid host metadata.
- Updated README validation scope and test descriptions. The existing GitHub Actions job already discovers `scripts/tests`, so it executes the new tests without a workflow edit. No cloud credentials or model calls are needed.

### Observed verification and readiness

All 22 installed skill-creator metadata checks passed. The collection gate passed catalog, license, installation, local-link/anchor and optional host-metadata checks. All 80 offline tests passed: 15 collection/evaluator tests, 26 UI helper tests, 12 PR publisher tests and 27 Node workflow scenarios. Whitespace checks passed. Local runtimes remain Python 3.12.6 and Node.js 26.10.0; hosted CI declares Python 3.12 and Node.js 24.

The collection is ready for use with its documented prerequisites and project-specific verification; no substantiated blocker remains in the inspected scope. This does not establish universal correctness, security certification, or best-in-class performance across models. This closing pass did not rerun model comparisons, live deployments, Android devices, browser/assistive sessions, installation trials or hosted CI. Their earlier evidence retains its original scope. Changes remain local; no commit, push or deployment was performed.

## Pilot readiness review

2026-11-11. Reviewed the 22 entrypoints in the working collection over `9405717` for discovery, responsibilities, authority, operational failure handling and evidence. Followed relevant templates and procedures, including risk-directed inspection of Android version and runtime assumptions, protected API/MCP effects, Git scopes, review independence, OpenSpec status, and production promotion. The [adoption plan](docs/ANTHROPIC-ADOPTION-PLAN.md) records rationale and the [pilot guide](README.md#start-a-pilot) is the project entry point.

| Package | Review and disposition |
| --- | --- |
| Software Delivery | Added OpenSpec and prototype adoption examples. The forward test exercised actual scenario, task and handler evidence. |
| PentaPRO | Added OpenSpec ownership and revision-aware resumption example. Synchronized PROCESS template and catalog. |
| Agent Instructions | Added scoped runner and external grader controls to the evaluation method. Kept evaluation conditional on significant instruction changes. |
| Behavior Testing | Retained test authoring scope, independent expected results and failure sensitivity. Receipt controls exercise those principles. |
| Peer Review | Retained read-only review and substantiated findings. Added a clean comparison fixture to the collection suite. |
| Cybersecurity | Retained threat/control ownership, scoped access and evaluation of the actual enforcement boundary. The runner enforces mount exclusion outside skill instructions. |
| Production Operations | Retained exact target, served revision and recovery boundaries after two offline forward tests. Added the stale-green fixture. |
| Diagnose Defect | Retained failing versus working comparison and authorization for fixes and probes. |
| HTTP API | Retained tenant-scoped retry, compatibility, transaction and external destination controls. |
| MCP Server | Retained revision-specific lifecycle, caller authorization and downstream effect checks. |
| Technical Research | Retained primary evidence, bounded experiments and explicit uncertainty. |
| Git Ship | Retained staged versus working-tree evidence and explicit publication scope. |
| UI Design | Retained conditional platform procedures and separation of visual, interaction and usability evidence. |
| Android Module Structure | Retained effective Gradle mode, module ownership and supported build/release variants. |
| Android Data Layer | Retained atomic writes, migration and session-bound storage behavior. |
| Android Error Handling | Retained typed failure classification, cancellation and bounded retry behavior. |
| Android DI Koin | Retained runtime argument and qualifier checks beyond graph inspection. |
| Android Background Work | Retained idempotency, WorkManager state and account-at-commit protections. |
| Android Unit Testing | Retained deterministic scheduling, cleanup and observable assertions. |
| Android Integration Testing | Retained actual migration, transport and application construction boundaries. |
| Android UI Testing | Retained native runtime, synchronization, selectors and platform evidence. |
| PR Quiz | Retained opt-in discovery boundary, safe publication and educational grading scope. |

All 22 packages passed the skill-creator validator and the collection catalog, license, link and installation checks. All 83 offline tests passed (18 collection/evaluator, 26 UI helper, 12 PR publisher and 27 Node grader scenarios). The installation comparison matched 144 files. The [pilot evidence](evals/RESULTS.md#anthropic-adoption-pilot-preparation) records the OpenSpec, isolation, grader and operations checks and their coverage. Review of entrypoints and selected references supports adoption for a scoped pilot. It does not establish exhaustive platform behavior, universal discovery, or superior model performance.


## Collection readiness verification

2026-11-11. Reviewed all 22 entrypoints in the candidate over `640d5ed`, their task boundaries and supporting resources, the installation and routing guides, project template, helper scripts, evaluation fixtures, notices and validation workflow. Rechecked version-sensitive instructions against the owning sources for the [Agent Skills format](https://agentskills.io/specification), [Android Gradle and Kotlin](https://developer.android.com/build/migrate-to-built-in-kotlin), [Compose test environments](https://developer.android.com/develop/ui/compose/testing/migrate-v2), [OpenSpec schema](https://openspec.dev/docs/schemas/spec-driven), [MCP revisions](https://modelcontextprotocol.io/specification/2026-07-28/changelog) and [GitHub CLI publishing](https://cli.github.com/manual/gh_pr_edit).

| Change | Reason and evidence |
| --- | --- |
| Software Delivery 1.4.0 and Android Module Structure 1.3.0 | The Castas retrospective showed a source/behavior mismatch and different device visibility in the agent sandbox and host. Porting now links a pinned source, the accepted rule and a comparison through the target entry point. Android setup now checks boot, device identity and a minimal user-visible assertion on uncertain runners. |
| PR Quiz 1.3.0 | The old publisher compared body text alone. A new head could receive questions drafted for an older diff. The supported invocation supplies the target repository and reviewed SHA. The helper pins the resolved PR URL and checks the head and body around the edit. Regression tests and an independent subprocess trial with a fake `gh` covered a matching revision, a stale draft, drift before the edit, and drift after submission. The last case reported the submitted edit and required inspection. GitHub does not provide an atomic compare-and-edit through this helper. |
| Evaluation runner | The candidate snapshot formerly copied whole directories, including ignored local files. It now follows the Git distribution inventory and refuses symlinks in selected package paths. The regression exercises changed tracked content, new files, deleted files, and an ignored control. |
| Documentation and validation | The adoption plan's relative links resolve after its move, and the prior root URL redirects readers. The README includes a first-task example and links the tutorial and case study as dated editions. Git attributes mark the PDFs as binary. A staged validation in a disposable checkout reproduced the original PDF whitespace failure and passed after the attribute was added. |

All 22 entrypoints passed the skill-creator validator. The collection gate found no issues across 135 Markdown files, 818 local link/anchor checks, 22 catalog versions, package licenses and optional host metadata. All 87 offline tests passed: 20 collection and evaluation tests, 26 UI helper tests, 14 quiz publisher tests, and 27 grader scenarios. The OpenSpec 1.16.0 fixture confirmed valid artifacts with unfinished work and detected a missing scenario. The Bubblewrap probe denied grader/sibling file access and confirmed private scratch writes.

Both the manual installation and Skills CLI 1.7.6 with `--copy` installed all 22 packages in disposable projects. All 144 installed package files matched the source. Collection-level guides, scripts and fixtures stayed outside the project installation. Codex CLI 0.160.0 reported all 22 project skills enabled through the local `skills/list` call. The [MCP fixture](evals/check_mcp_sdk.py) also passed in-process with Python SDK 2.2.0 for legacy sessions, modern direct calls, SDK discovery, replay after response loss, caller-bound handles, and version/header errors.

The candidate supports local adoption using the documented tools and prerequisites. Hosted CI, production providers, live GitHub grading, consuming Android builds, and quality comparisons across models and other hosts require their own evidence.

## Current collection review

2026-11-13. Reviewed all 22 installable entrypoints and their supporting assets and references relevant to the reviewed changes, using `2500753` as the starting revision. Checked canonical record ownership, task selection, permission boundaries, reproducible evidence, source currency, standalone installation and developer onboarding. This maintenance pass included targeted independent review, executed controls and a matched synthetic GPT-6.1 Sol pilot. The [evaluation record](evals/RESULTS.md#matched-gpt-61-sol-pilot) describes outcomes and limits.

| Package | Review disposition |
| --- | --- |
| PentaPRO | Resolve authority and output format before writing. Preserve local and external record identity, link verification to the tested revision, and distinguish priority, obligation and confirmation. |
| Software Delivery | Document OpenSpec defaults, version-specific skill invocation, strict post-archive validation, and a project-native SDD example. Preserve direct and exploratory paths. |
| Behavior Testing | Add focused examples for test boundary, denied side effects, input selection, fault sensitivity and intermittent failures. Preserve the existing test-first scope. |
| Diagnose Defect | Add reliable-reproducer prerequisites, bisection handling for unclassifiable revisions, and controlled input reduction. |
| Technical Research | Verify applicable versions and dependency provenance, examine counterevidence, and bound benchmark conclusions. |
| HTTP API | Add conditional guidance for throttling, shared cache isolation, atomic write preconditions and consumer migration. Retain the existing idempotency and SSRF procedure. |
| MCP Server | Make token audience and downstream credential separation operational and link both supported authorization revisions. Test denied requests at the actual downstream boundary. |
| Peer Review | Add a caller/installed API check and an example of a substitute hiding a protection failure. Retain evidence-based review and valid zero-finding outcomes. |
| Cybersecurity | Make detection and accountability visible in threat coverage, update MCP source links, and include the version-qualified Android encrypted storage option. |
| UI Design | Add a rendered accessibility journey spanning automated and manual checks, and make Android companion instructions optional when installed alone. |
| Production Operations | Connect an applicable error-budget policy to a promotion decision and add incident recovery and follow-up evidence to the existing record. |
| Git Ship | Respect project commit/signature policy and stop publication on credentials present anywhere in the outgoing range. |
| Agent Instructions | Distinguish explicit use from discovery and place generated-code execution and scoring in separate environments. |
| Android Module Structure | Describe effective built-in Kotlin configuration, conditional reference stacks, and Room 2/3 conventions. |
| Android Data Layer | Preserve existing clients and serialization policy, give Room 2/3 setup alternatives, and test actual data boundaries and migration. |
| Android Error Handling | Preserve cancellation, keep deadline ownership explicit, and carry server retry hints where the operation requires them. |
| Android DI Koin | Use compile-time checks where supported and exercise runtime parameters, module selection and platform startup where needed. |
| Android Background | Document current runtime coordinates, expedited quotas, foreground requirements and startup ownership. |
| Android Unit Testing | Clarify test scheduler scope and keep fixtures and cancellation checks deterministic. |
| Android Integration Testing | Describe version-matched Room tests, DataStore test-scope cleanup and optional process isolation. |
| Android UI Testing | Preserve resolved Compose factory/scheduler choices and use supported automated accessibility checks with device evidence when required. |
| PR Quiz | Reviewed the explicitly requested educational workflow, eligibility, revision binding, and the limits of its informational status. The current code and offline grader behavior meet that scope. |

The [routing guide](SKILL-ROUTING.md), [project template](skills/setup-pentapro/assets/agents.md), [maintenance procedure](SKILL-EVALUATION.md) and [Portuguese development guide](docs/guia-consolidado-desenvolvimento-com-agentes.pdf) share the same project-owned contract and verification workflow. The earlier [Castas case study](docs/relatorio-retrospectiva-castas-android.pdf) remains a dated record of that project.

The revised 112-page guide preserves the existing labs and adds OpenSpec 2.0 setup and troubleshooting, project-native SDD, vibe coding and prototype promotion, platform-specific verification, and a comparative pilot exercise. All nine extracted OpenSpec deltas validated and archived with simulated task completion, and all eight consolidated capability specs passed strict validation. The CLI lab passed six subprocess checks and rejected a deliberate negative-value regression. The current PDF's 22 catalog versions, page count, 165 internal destinations and 51 bookmarks were checked. The pages were rendered for inspection.

The Android review exercised five groups of JVM behavior with the extracted Kotlin Result, repository and fake snippets and the real coroutine library. Room, Compose and platform instructions were checked against primary sources. Builds of the updated variants against consuming Android dependencies and device behavior remain project checks. Hosted CI, live GitHub grading and production deployment were outside this local collection validation.

The closing run passed all 22 entrypoint validations and 99 offline checks: 32 collection/evaluator tests, 26 UI helper tests, 14 PR quiz publisher tests, and 27 quiz workflow scenarios. The case manifest and the standalone link and catalog checks passed. Local installation and discovery passed for the supported Codex workflow. Use the [installation guide](README.md#installation-and-activation) to adopt the collection and the [pilot procedure](SKILL-EVALUATION.md#reproduce-the-synthetic-codex-trials) to measure it on representative project work.

## Final maintenance review — 2026-11-14

The team-selected PentaPRO initial-detail order is PRODUCT → PROJECT → PRODUCTION → PROOF → PROCESS. The 2.9.0 update aligns the entrypoint, five templates, navigation, software profiles, Android/KMP overlay, worked example, project-instruction template, catalog, and preferred-order evaluation case. PRODUCT now explicitly holds consequential conditions of real use and observable acceptance before solution selection; PROJECT tests feasibility; PRODUCTION details the selected design; PROOF completes the check plan before implementation; PROCESS records authority and resumption throughout. Existing specifications retain their canonical layout and IDs unless a migration is requested. The earlier 2.3.0 evaluation note remains historical.

Reviewed the 22 current skill entrypoints for distinct activation, project-owned contracts, scoped authority, meaningful verification, failure handling, version-sensitive claims, and optional companion boundaries. The existing specialist skills already supply non-obvious implementation and review procedures; changing their instructions merely to restate the new PentaPRO order would add context and maintenance cost without changing their task behavior. Spot-checked the current [Agent Skills format](https://agentskills.io/specification) and Android primary documentation for [Compose test v2](https://developer.android.com/develop/ui/compose/testing/migrate-v2), [Room 3 testing](https://developer.android.com/reference/androidx/room3/testing/MigrationTestHelper), [WorkManager](https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/manage-work), and [AGP built-in Kotlin](https://developer.android.com/build/migrate-to-built-in-kotlin) claims. These checks found no additional correction supported by the evidence inspected.

For this revision, `scripts/validate_collection.py` checked 144 Markdown files, 790 local links/anchors, and 22 catalog versions with no issues; all 22 entrypoints passed skill-creator structural validation. The 99 existing offline tests passed: 32 collection/evaluator, 26 UI helper, 14 PR quiz publisher, and 27 quiz workflow cases. `git diff --check` passed. The order case is authored, not an executed multi-model PentaPRO trial. These checks do not establish identical behavior on other models, consuming-app correctness, live security, accessibility, deployment, or release readiness. The Portuguese PDF is a dated teaching edition; the current skill and catalog govern its superseded PentaPRO version label.

The 2.9.1 follow-up aligned additional active references found by a repository-wide search, including UI Design's PentaPRO ownership list and the OpenSpec adoption plan. The older evaluation record and Portuguese PDF remain dated artifacts. `docs/SDD_step-by-step.md` was added at the user's request as an existing SDD working document; it does not mention PentaPRO or replace the maintained skill and catalog. The follow-up validation and publication result should be reported separately from the checks above.

## Developer onboarding review

On 2026-11-14, reviewed the 22 entrypoints against their stated scope, the routing guide, referenced resources, the README catalog, and the project instruction template. Checked the adoption and evaluation instructions against the available commands, and the historical guides and reports against their role in the current documentation.

- Corrected the README privacy section to describe the actual local prototype, GitHub quiz, and model evaluation flows. Added the evaluation manifest check from CI to the local commands and linked the working SDD notes. The [Vercel installer documentation](https://github.com/vercel-labs/skills#install-a-skill) confirms the Node prerequisite and documents [installer telemetry](https://github.com/vercel-labs/skills#telemetry).
- PR Quiz now requires the target repository and reviewed SHA for publication. Existing integrations must supply both flags. Preview works locally with just the PR number, quiz file, and `--dry-run`. The regression test verifies that omitted flags stop publication before a GitHub request.
- Identified the earlier review report and the SDD drafts in their opening text. The Portuguese PDF editions retain their publication context. Use the README catalog and installed skill for current versions.

The collection validator reported 145 Markdown files, 795 local links and anchors, and 22 matching catalog versions. The 22 entrypoints passed the standalone metadata check, the 15 evaluation cases passed manifest validation, and all 100 local tests passed. Vercel Skills CLI 1.8.1 copied 22 packages into an isolated project and all 148 installed files matched their sources. Codex CLI 0.160.0 listed all 22 as enabled. The installed UI prototype sample built three states and checked six declared token pairs. The installed PR Quiz rendered its sample using dry-run.

This pass verifies the local installation and discovery path plus the declared helper checks. Behavior on other agent hosts and models, Android device results, and GitHub publication and grading with live permissions still depend on the target environment.


## PentaPRO directory transition

2026-11-15. Reviewed the five-pillar coverage against the supplied PentaPRO idea analysis. Kept the five dimensions and mapped domain knowledge, experience, protection, quality, cost, operations, verification and governance to topic files and links. PentaPRO 3.0.0 initializes repository-root pentapro/ with separate files in all five pillars and an assets index. UI Design 1.6.0 routes detailed screen records into PRODUCT when PentaPRO is selected. Document maintenance distinguishes the maintained specification from OpenSpec change artifacts and describes migration, revision-bound evidence and reconciliation after changes. The initializer preserves existing files and rejects a non-root destination or symlinked specification directory.

Castas and Yo-Fi received the initial directory structure and project-specific navigation. Castas still needs reconciliation of its existing pillar records and conflicting toolchain instructions; Yo-Fi still needs product decisions before its scaffold can be accepted as a complete specification. Their OpenSpec directories remain separate. Previous PDF guides are dated teaching editions, and the README points users to the current skill for the new layout.

The current collection validator, 22 entrypoint structural checks, evaluator isolation probe and offline suites passed locally. Structural and local execution checks do not establish that another agent, project or platform will recreate a software build identically. Projects must pin relevant inputs and verify their own outputs.

## Setup PentaPRO addition

2026-11-18. Added Setup PentaPRO 1.0.0 as the collection's first skill to run in a new project. It is adapted from Matt Pocock's `setup-matt-pocock-skills` at commit `59db609eb1e18aaf59b63284d0e52255aff0c63c`, with issue-tracker, triage-label and domain-documentation templates plus a separate root instruction template. The domain layout is rewritten for this collection: glossary and context terms are PRODUCT material in `pentapro/product/domain.md`, decisions are PROJECT material in `pentapro/project/decisions.md`, and no root `GLOSSARY.md`, `GLOSSARY-MAP.md` or parallel `docs/adr/` tree is created. A new findings section weighs every other setup fact against the five pillars and asks the developer when ownership is unclear. The skill ends with an explicit handoff to `$penta-pro` for the project introduction.

The README, routing map, project instruction template, third-party notices, collection disposition and validator label were updated. Provenance is recorded in the package [source notes](skills/setup-pentapro/references/sources.md) and the [third-party notices](THIRD-PARTY-NOTICES.md#setup-pentapro), which list the adapted files and deviations; the package keeps the repository's standard MIT `LICENSE`. The package ships authored evaluation scenarios, not executed model trials. Validation reported 155 Markdown files, 837 local links and anchors, 23 catalog versions and no issues. The 32 collection/evaluator, 11 PentaPRO initializer, 26 UI helper and 15 PR quiz publisher tests passed, as did the 27 Node quiz workflow scenarios, and `git diff --check` was clean.

These are structural and offline checks. The setup conversation was not executed against a fresh repository with a live GitHub or GitLab tracker, so activation, question quality and real project outcomes still depend on the host, model and target project.

## Final collection audit with the 23rd package — 2026-11-18

Read all 23 entrypoints, their descriptions, boundaries, authority statements, references and catalogs before closing the Setup PentaPRO work. The 22 existing skills needed no new behavioral change: their workflow, security, retry/idempotency, cancellation, release and evidence contracts remain aligned with their stated scope, and the earlier per-package findings are unchanged. The audit confirmed that tracker configuration is consumed through the generated root instruction block rather than duplicated inside each coordination skill.

Corrections made in this pass:

- Setup PentaPRO now distinguishes what the collection expects from what it guarantees: the tracker/domain configuration is the contract, while `pentapro/` initialization remains optional and is created or resumed by `$penta-pro`.
- The setup conversation now explores project facts (README, manifests, lockfiles, CI, commands) before Section D classifies them, handles a re-run over existing `docs/agents/`, stops rather than guessing when the tracker is unreachable, and states when the `penta-pro` initializer is not installed.
- Legacy glossary/ADR migration preserves decision IDs and inbound links, supports one-file or per-record decision layouts, and never leaves two canonical copies.
- The initializer reports repository failures as a clean `ValueError`, and its CLI prints `error: ...` with exit code 1 instead of a traceback and Git's stderr. Its 11 package-local tests cover creation, preservation, recreation, root enforcement, five symlink refusals and both CLI paths.
- README task numbering, installation sequencing, package tree and resource tables now match the 23-package collection; PentaPRO is 3.0.1 because its packaged initializer changed, with the template version updated in lockstep.
- Setup PentaPRO ships authored evaluation scenarios; they are maintainer cases, not executed model trials.

Verification: the collection validator reported 155 Markdown files, 837 local links and anchors, 23 catalog versions and no issues. The 15 evaluation cases, 32 collection/evaluator tests, 11 PentaPRO initializer tests, 26 UI helper tests, 15 PR publisher tests, 27 Node quiz scenarios and `git diff --check` passed. These remain structural and offline checks; no live tracker, fresh-repository interview, hosted CI run or model comparison was executed for this pass.

## Root instruction template and mandatory prompt logging — 2026-11-18

The project instruction template moved from the repository root (`AGENTS-template.md`) into the Setup PentaPRO package as `skills/setup-pentapro/assets/agents.md`; no root copy remains. Setup PentaPRO 1.1.0 now creates or merges the target project's root instruction file from that template. It uses repository evidence first, fills what it can verify, preserves existing project rules, and marks unresolved content with `[FILL IN]` and a `Setup status: temporary` note. PentaPRO 3.1.0 reconciles the file after the first consolidated specification: it fills remaining fields from confirmed pillar records, removes template sections that do not match the project, keeps the user's own instructions, and removes the marker only when the material fields are resolved or deliberately marked `Not applicable`. The packaged PROCESS template version moved in lockstep.

Prompt logging is now a mandatory Setup PentaPRO task, derived from the repository's former local prompt-policy document into harness-neutral English at `skills/setup-pentapro/assets/prompt-logging.md`. Setup writes the operational rule into the root instruction file, copies the detailed policy to `docs/agents/prompt-logging.md`, adds `AGENTS.log` and `AGENTS.log.*` to `.gitignore`, and can add a repository-scoped hook when the host documents one. The rule is append-only, covers subagent prompts, requires RFC 5322 headers and verbatim bodies, and is explicitly repository-scoped: it is never configured in the agent's global scope. An existing hook is verified rather than duplicated. Setup's authored evaluation cases now cover template merging, unknown facts, logging enablement, and an existing hook; PentaPRO adds a reconciliation case and validation record.

Verification: the collection validator reported 156 Markdown files, 846 local links and anchors, 23 catalog versions and no issues. The 15 evaluation cases, 32 collection/evaluator tests, 11 PentaPRO initializer tests, 26 UI helper tests, 15 PR publisher tests, 27 Node quiz scenarios and `git diff --check` passed. These are structural and offline checks. No live setup conversation, real project tracker, host hook execution or cross-model comparison was run for this pass.

## Final collection review — 2026-11-18

After the Setup PentaPRO additions, the collection was swept for stale routing references. The packaged project instruction template, the routing map and the closure record now describe setup as issue tracker, domain documentation layout, root instruction file and mandatory repository prompt logging; they previously named only the specification facts. Agent Instructions 1.1.2 states the boundary with setup-pentapro for a new repository's first root instruction file, avoiding two skills claiming that one-time task. The remaining skills were re-read against their proposed scopes; no further behavioral change was warranted.

Verification: the collection validator reported 156 Markdown files, 846 local links and anchors, 23 catalog versions and no issues. The 15 evaluation cases, 32 collection/evaluator tests, 11 PentaPRO initializer tests, 26 UI helper tests, 15 PR publisher tests and 27 Node quiz scenarios passed, as did `git diff --check`. These remain structural and offline checks; no live tracker, repository-hook execution, fresh-project interview, deployed environment or cross-model comparison was executed for this pass.

## Project-scoped prompt-logging hook — Setup PentaPRO 1.2.1 — 2026-11-18

Setup PentaPRO 1.2.1 adds optional mechanical prompt-capture to the mandatory logging rule. The rule is the portable contract and applies to every repository; the hook is an optional enforcement layer for the coding agent in use. The shipped hook implementation is a shared core plus thin host adapters:

- `skills/setup-pentapro/assets/prompt-logging/core.mjs` — entry format, redaction, and synchronous O_APPEND contract; exits non-zero on write failure so the host can block.
- `skills/setup-pentapro/assets/prompt-logging/log-prompt.mjs` — stdin adapter for command-based hooks (Claude Code, Codex, Cursor, Copilot).
- `skills/setup-pentapro/assets/prompt-logging/opencode.ts` — OpenCode project plugin adapter, installed under `.opencode/plugins/` for automatic discovery; sets `globalThis.__agentsLogProjectCapture` so a personal global plugin can yield.
- `skills/setup-pentapro/assets/prompt-logging/hosts.md` — per-host configuration merge instructions, trust requirements, smoke-test steps, and known limitations.

The skill's exploration step detects coding-agent markers and installed CLIs; Section E offers a hook only for detected hosts, verifies Node.js, preserves existing configuration, runs the smoke test, and asks the user to confirm one entry with a real prompt. OpenCode uses its documented `.opencode/plugins/` auto-discovery path. A personal global capture is surfaced and kept without duplication. The CI workflow (`validate.yml`) runs `node --test scripts/tests/test_agents_log.mjs`; its 15 cases cover redaction, missing/valid prompt payloads, entry formatting, append permissions, symlink/hard-link refusal, CLI failures, and Cursor attachments.

The final review of all 22 other skill entrypoints found no additional changes necessary. This pass also corrected OpenCode's invalid single-file plugin configuration (the adapter is now installed at its documented auto-discovery path and writes to `ctx.location.project.directory`), rejects prompt payloads that lack a recognized prompt field instead of logging a false empty prompt, and refuses symlink, hard-link, and non-regular log targets. The setup guidance now consistently records approved facts in `docs/agents/setup-notes.md` when PentaPRO initialization is deferred. Authored evaluation cases cover the OpenCode loading path, unsafe log paths, a global capture already present, an existing host configuration, the Copilot limitation, a missing Node runtime, a write failure, an ignored host configuration, and a configuration referencing credentials. The routing map, collection closure record and README resource table describe setup as including the optional capture hook. No other skill needed a behavioral change.

Verification: the collection validator reported 157 Markdown files, 859 local links and anchors, 23 catalog versions and no issues. The 15 agent-log tests, 15 evaluation cases, 32 collection/evaluator tests, 11 PentaPRO initializer tests, 26 UI helper tests, 15 PR publisher tests, 27 Node quiz scenarios and `git diff --check` passed. These are structural and offline checks; no live hook execution, real coding-agent session, repository-host integration, or cross-model comparison was run for this pass.

## Self-contained prompt rule — Setup PentaPRO 1.3.0 — 2026-11-18

Setup PentaPRO now configures prompt persistence through `AGENTS.md` only. The complete rule is embedded in the skill entrypoint and mirrored in `assets/agents.md`; the setup flow ensures `AGENTS.log` is ignored, does not create a separate policy document, and does not install or configure hooks, plugins, slash commands, or global agent settings. When `CLAUDE.md` exists, setup adds `@AGENTS.md` without replacing its content. Evaluation cases now cover the complete rule, first-action logging, safe merges, automatic-capture duplication, write failures and sensitive prompt content. Legacy hook assets remain in the package but are explicitly not part of the active setup flow.

Verification: the collection validator reported 157 Markdown files, 842 local links and anchors, 23 catalog versions and no issues. The 15 evaluation cases, all 35 collection tests (including the three prompt-rule consistency cases), and `git diff --check` passed. The Node runtime was unavailable, so the legacy Node logger test was not run; no source code in that logger was changed. The former local prompt-policy document was removed; historical maintenance entries retain its former path as provenance. Legacy packaged hook materials remain explicitly marked as historical and outside the active setup flow.


## Final collection maintenance audit — 2026-11-18

Scope: all 23 skill entrypoints, the existing uncommitted Setup PentaPRO 1.3.0 changes, recent setup/specification maintenance, catalog/routing, and supporting references, assets, helper scripts, tests and evaluation records. Two independent read-only reviewers assessed standards and specification consistency. Supporting resources were traced by risk and searched across the collection; this is not an exhaustive line-by-line audit of every reference, nor a claim of best-in-class effectiveness.

Standards review identified one substantive issue: ignore patterns do not protect a prompt log already tracked by Git. The self-contained rule now checks the index before appending, preserves local data and index selections, and reports the privacy conflict. It also specifies owner-only creation and rejection of unsafe log targets. The first tool operation explicitly permits the necessary root/index/path checks and logging; general work follows only after logging succeeds. Capture verification uses the current event rather than matching old prompt text, with narrowly scoped log access and explicit handling of unverifiable capture.

Specification review identified six issues: the same tracked-log gap; approved facts lost after initializer failure; no explicit PentaPRO consumer of deferred setup notes; obsolete discovery destinations; stale README guidance about CLAUDE-only setup and optional hooks; and a legacy evaluation that contradicted authorized migration. All were corrected. PentaPRO 3.1.1 preserves deferred fact status/provenance, links migrated notes to their canonical homes, and uses current pillar paths. UI Design 1.6.1 corrects its maintenance reference to identify PRODUCT experience files and five pillars. Catalog versions and the PentaPRO PROCESS template match. Setup's authored scenarios now include initialization failure, tracked/unsafe logs and repeated identical submissions. The prompt-rule consistency tests include the new invariants and the producer/consumer handoff. No other entrypoint required a behavioral change.

Verification: all 36 collection/evaluator tests, 11 PentaPRO initializer tests, 26 UI helper tests, 15 quiz publisher tests, 27 Node quiz scenarios and 15 legacy Node logger tests passed (130 checks). The logger initially failed because sandbox subprocess execution returned EPERM; the unchanged suite passed outside that restriction. The 15 executable evaluation case definitions validated; authored Markdown scenarios were reviewed, not executed as model trials. Collection metadata/link validation and whitespace checks passed on the final staged snapshot.

Limits: no new live-model comparison, full setup conversation, consuming application build, Android device test, live tracker/provider operation or end-to-end hook session was run. Passing helper tests and structural checks do not establish universal quality, exhaustive security coverage or production readiness. The checked Agent Skills specification supports the package structure/metadata, and Claude Code's documented imports support the existing-CLAUDE import path; target-host discovery and compliance still require their own verification.


## Setup PentaPRO scope reduction (2026-11-18)

Setup PentaPRO 1.4.0 now configures only the current project's `AGENTS.md`. Its entrypoint contains the complete prompt-persistence rule and writes that section directly, preserving unrelated instructions. Tracker selection, domain migration, broad template seeding, Claude imports, ignore-file changes and specification initialization are outside the active setup workflow. Historical assets remain for earlier installations. The catalog, routing guidance, related skill boundaries and authored scenarios reflect this scope; earlier entries above describe superseded versions.

Validation for this scope reduction: 156 Markdown files, 828 local links/anchors and 23 catalog version checks passed; all 35 Python collection tests and the skill frontmatter validator passed. `git diff --check` was clean. No model setup trial was executed.

## Setup workflow restoration and cross-skill alignment — 2026-11-19

The owner requested restoration of the broader setup workflow. Setup PentaPRO 1.5.0 again covers tracker and domain guidance, optional triage, project instructions and a PentaPRO handoff, alongside its self-contained prompt rule. PentaPRO 3.1.2 recognizes the restored handoff and keeps temporary instruction fields until their material facts are resolved. Agent Instructions 1.1.3 reflects the setup boundary. The earlier 1.4.0 scope reduction above remains a historical record, not a description of the current workflow. The producer/consumer structural check was restored; authored setup scenarios are not evidence of an executed model trial.

## Collection closing audit — 2026-11-19

This is a maintainer self-review of the working tree, including the new Software Factory 0.1.0 package and the restored Setup PentaPRO 1.5.0 workflow. It is not an independent approval or a claim that every host, stack, developer, model or project has been tested. All 24 entrypoints were checked for distinct purpose, project-owned authority, verification and evidence boundaries, failure handling, package metadata and portability. The existing specialist references and earlier review records supplied risk-directed coverage; examples were not all executed on real products. No further entrypoint expansion was justified by this audit. The factory now has [authored pilot scenarios](skills/software-factory/evals/scenarios.md), which remain unexecuted.

Documentation corrections made in this pass: the routing map now counts 24 skills; the earlier collection review identifies itself as historical; the factory proposal points to the local v1 instruction package and marks its old setup state as historical; the README exposes the factory records, distinguishes the dated PDF catalogs from the current catalog, and lists the Node logger test used in CI. The long Portuguese SDD notes and both PDFs remain dated educational records. Their historical counts and commands should not override the installed skills or current host documentation.

### Script coverage and execution

| Script surface | Available check | Result and limit |
| --- | --- | --- |
| Collection validator and evaluation runner/isolation/outcome modules | `scripts/tests/test_validate_collection.py`, `test_run_skill_evals.py`, `test_openspec_archive.py`, and the setup rule test | 36 Python tests passed with `python3`; manifest validation found 15 cases. Full model trials were not run. |
| PentaPRO initializer | `skills/penta-pro/scripts/tests/test_init_pentapro.py` | 11 tests passed, including repeat execution and unsafe paths. |
| UI prototype helper | `skills/ui-design/scripts/tests/test_prototype_tools.py` | 26 tests passed, including malformed input and output preservation. |
| PR quiz publisher and workflow | `skills/pr-quiz/scripts/tests/test_publish_quiz.py` and `workflow.cjs` | 15 Python tests and 27 Node scenarios passed with API doubles; live GitHub rules were not exercised. |
| Prompt logger core and CLI adapter | `scripts/tests/test_agents_log.mjs` | 15 Node tests passed outside the filesystem sandbox. The sandbox denied child-process creation with `EPERM`; CI runs these tests on its normal runner. |
| OpenCode prompt logger adapter | No automated host integration test | The adapter is retained as an optional legacy asset; Setup PentaPRO does not install it. Test with a supported OpenCode host before re-enabling the adapter as a setup action. |
| MCP SDK smoke fixture | `evals/check_mcp_sdk.py` is itself an assertion-based integration fixture | The earlier recorded SDK 2.2.0 run is in `evals/RESULTS.md`; it is optional and was not rerun in this pass. Its fixture services and receipt checks are test material, not production scripts. |

The collection validator reported 165 Markdown files, 889 local links/anchors and 24 version checks with zero issues. The skill-creator structural validator accepted all 24 packages. `git diff --check` was clean. These checks establish packaging and local script behavior, not full developer readiness. A real project pilot is still needed for Setup PentaPRO and Software Factory, especially host activation, OpenSpec handoffs, independent review, remote publication and archive ordering. The factory is a portable instruction workflow, not a deterministic scheduler or installed model-specific agent configuration. Publish or claim broad compatibility only after the relevant target environments have been exercised.

## Factory closing review — 2026-11-19

Reviewed current skill boundaries, agent templates, process contracts, script inventory, tests, README, routing, setup provenance and dated documentation against the pilot findings. Supporting resources received targeted inspection; this is a maintainer self-review and does not establish exhaustive correctness of every platform example. Preserved the preceding uncommitted work. Setup PentaPRO 1.6.2 adds trust and evidence boundaries to all five agent templates; Software Factory 0.2.2 explicitly requires the applicable specification review before dependent implementation is dispatched. Setup provenance now includes the factory assets, and README exposes the pilot's custom-role limitation.

Added two automated role-template tests under `scripts/tests/test_factory_agents.py`, covering required TOML fields, unique role names, filename consistency and exclusion of unsupported permission/provider overrides. They run through the existing CI discovery command. The current offline checks passed: 38 collection tests, 11 initializer tests, 26 UI helper tests, 15 quiz-publisher tests, 27 quiz-workflow cases and 15 logger tests (132 total). The logger suite needed execution outside the sandbox to permit its child processes. Manifest validation and all 24 package structural checks also passed.

Production helper scripts have direct tests. Evaluator modules and receipt grader are exercised by runner tests; fixture applications and the MCP smoke script are test material rather than production tools needing recursive tests. The optional MCP smoke script has its own assertions but was not rerun; prior evidence is in `evals/RESULTS.md`. The legacy OpenCode adapter still lacks a real host integration test. This is acceptable only while it remains outside the active setup path; do not enable it as a supported setup action without host verification. TOML schema tests establish configuration integrity, not agent discovery, model use or enforcement of read-only permissions.

The collection is ready for controlled adoption with explicit tool and model prerequisites. It cannot be certified as 100% ready for every developer or project: the tested Codex host did not demonstrate custom-role selection, full new-project bootstrap has not been repeated twice by independent CLI sessions, and remote delivery, deployment and broad host compatibility were not exercised by the local pilot. The Portuguese tutorials and PDFs remain dated educational records as identified in README; they are not current package/version authorities. The pilot retrospective and change checklist are the current adoption records. No publication was performed in this review.

## Approved targeted upstream refresh — 2026-11-20

Implemented the user's approved assessment over `3b62719` while preserving eight pre-existing modified skill entrypoints. Added store-aware OpenSpec root selection and removal/rename semantics; structured MCP results and agent-task usability guidance; individual reviewer candidate provenance and selective history investigation; initiating-path attribution; IME and forced-colors checks; and capture-control, pressure, snapshot and interrupted-effect evaluation briefs. Factory resumption now explicitly reconciles uncertain effects and keeps evidence separate from risk acceptance. Diagnosis retains its safeguards with conditional disposable mutation probes and reassessment after three unsuccessful fixes rather than automatic task termination.

Existing review snapshot rules, migration repair/restore, benchmarks, API boundaries, Git hygiene, semantic documentation drift and canonical contract guidance already cover the report's principal recommendations. Those procedures were preserved instead of duplicated. No new skill, fixed model, mandatory delegation, universal TDD, map toolchain, new document registry or automatic external action was introduced. Historical provenance remains intact; renamed upstream locations are recorded in notices and source notes. PL Coding's current bundle comparison remains pending.

Evaluation briefs describe future trials; they are not model executions or evidence of quality/token gains. Validation results for this working snapshot are recorded below when executed. No upstream code was run, no deployment or publication was performed, and historical test counts retain their original scope.

Validation executed for this working snapshot: collection validator passed **169 Markdown files, 907 local links/anchors and 24 version checks**; evaluation manifest validated **15 registered cases**; `git diff --check` passed. Existing offline suites passed **132 tests**: repository Python 38, PentaPRO Python 11, UI Python 26, PR publisher Python 15, embedded quiz Node 27 and logging Node 15. Logging subprocess tests initially failed under the sandbox with `spawnSync EPERM`; the unchanged suite passed when run with permitted escalation. Node execution used local v27.0.0-alpha.0.0.0 rather than CI's Node 24, so this is not a new hosted-CI/runtime-matrix result. No model comparison, browser/IME/forced-colors run, live OpenSpec store mutation or deployment was executed. The new briefs are not added to the executable manifest as if runners already existed.

## Setup README and license workflow — 2026-11-20

Setup PentaPRO 1.7.0 adds the requested purpose-driven README generation, existing README replace/complement/skip choice, explicit language selection and post-generation translation, and developer-selected GitHub licensing for projects without established licensing. The exact maintainer-supplied template is packaged as a portable output asset; its illustrative claims and stack commands do not become target-project facts. Existing license variants, narrow setup requests, skipped README bytes, concurrent edits and unresolved choices are preserved. License text remains canonical, independently of README language.

Executed checks: packaged template bytes matched the supplied original; skill metadata validator passed; collection validation passed 170 Markdown files, 910 local links/anchors and 24 version checks; four existing setup prompt-rule tests passed; `git diff --check` passed. Added authored choice, translation, inference, offline and rerun scenarios. No consuming-project generation/model trial or live license creation was executed, and no remote publication occurred.


## Final collection and factory readiness review — 2026-11-20

Reviewed all 24 skill entrypoints against their activation, ownership, expected outputs and verification requirements. Traced supporting references where they govern those outputs, with independent package-contract and documentation passes. Reviewed the five project-local Codex role templates and the factory contract from intake through retrospective, including interrupted effects, authorization, snapshot-specific evidence and optional OpenSpec paths. Cross-checked the root catalog, onboarding, ownership map, provenance, validation and evaluation guides, project docs, fixtures and resources. The dated PDFs and prior review results retain their original scope.

| Area | Correction and evidence |
| --- | --- |
| Setup PentaPRO | Scoped README-only and license-only requests activate only the selected branch. Complement mode applies the selected language to retained prose even when the selection is English. Existing README variants keep their renderer. Updated README, routing, guide and authored scenarios. One trailing space in the bundled template was removed so the file passes the repository whitespace gate. |
| Factory and OpenSpec | Aligned required-gate outcomes, planner/ship ownership, partial OpenSpec initialization and verification for archive paths that intentionally leave specs unchanged. Tightened implementer and verifier role handoffs. OpenSpec 2.1.0 first created the local root but failed to fetch skills under network restriction. An authorized retry installed six project-local Codex skills. In disposable projects, the CLI distinguished the checkout from a registered store and rejected an unavailable store. The archive integration test verified an actual archived delta and consolidated spec. |
| Delivery and PentaPRO | Evidence reuse now requires matching tested snapshot, relevant environment, configuration and checks. Affected checks run again after edits. PentaPRO points to the selected planning root when the project uses an OpenSpec store. |
| Git Ship | A disposable push with distinct fetch and push repositories showed that checking the named remote queried the wrong repository. The revised procedure pins the reviewed commit and checks the effective push endpoint before and after publication. The local bare-repository control confirmed the resulting branch ID. |
| Distribution and documentation | Updated package versions, README and route descriptions, the Portuguese factory guide, references, and setup logging disclosure. Skills CLI 1.9.0 installed 24 packages and 183 byte-identical files in a disposable Codex project. Codex CLI 0.160.0 listed all 24 collection skills and six OpenSpec skills in the local discovery probe. Five role TOMLs were installed in the probe and validated by the existing configuration tests. |

### Script assurance

| Executable material | Verification in this review |
| --- | --- |
| PentaPRO initializer, UI prototype helper, PR Quiz publisher | Direct Python suites passed 11, 26 and 15 tests respectively. These cover file generation and preservation, prototype behavior and input handling, and PR publisher behavior with local doubles. |
| PR Quiz GitHub Actions template | 27 Node scenarios exercised the embedded workflow with API doubles. GitHub-hosted execution remains a separate environment. |
| Prompt logging core and hook CLI | 15 Node tests passed with permitted escalation after the sandbox denied spawning Node subprocesses. The OpenCode adapter is historical, outside active setup, and has no host integration test. This gap is acceptable for archival use. Verify the adapter and host API before relying on it for capture. |
| Collection validator, eval runner, isolation and scoring, receipt grader | 38 collection tests passed, including fixture controls, process cleanup, input isolation, receipt scoring, factory TOML checks and real OpenSpec validation/archive. Fixture applications and test drivers are exercised as test material. Their independent controls provide coverage without recursive tests for the test code. |
| MCP SDK fixture | Existing integration assertions passed in process with MCP Python SDK 2.2.0, including legacy and modern requests, discovery, retry after response loss, principal-scoped handles and version/header errors. |

The **132 offline tests** above passed. The validator passed **170 Markdown files, 920 links/anchors and 24 version checks**. All 24 packages passed metadata validation and 15 registered evaluation cases passed manifest validation. Whitespace checks covered tracked changes and new files. The local Node runtime was v27.0.0-alpha.0.0.0. The workflow targets Node 24 in hosted CI.

The collection is ready for project-scoped adoption with the prerequisites in the README. The tests exercised local installation, discovery, role configuration and OpenSpec operations. Actual selection of custom roles and their configured models, an agent-driven setup from a blank project, hosted CI and publication, production deployment, and behavior across other hosts remain unverified for this snapshot. The evidence supports local readiness in the tested environment. Broader readiness depends on the target project, host, tools and required checks. No commit, push or deployment was performed on this repository.
