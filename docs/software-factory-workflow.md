# Software factory workflow

Historical design/evaluation record. It describes its original snapshot, not the current runtime contract. Use the [native workflow guide](guia-fabrica-changes.md) and the maintained skill entrypoints for current work.

Status: **historical proposal**. Its portable first version is now the [Software Factory skill](../skills/software-factory/SKILL.md); the gates, pilot and rollout below remain proposed design material, not evidence of an executed factory run. For day-to-day use, follow the [operational checklist](guia-fabrica-changes.md).

Date: 2026-11-19.

This document proposes a sequential, gate-based agent and subagent workflow for taking a prompt or an accepted change from specification review to implementation, verification, code review, records, publication and, only when separately authorized, release. It is based on the Castas project history and on the maintenance history of this skill collection.

The proposal does not replace the existing owners. It composes them. [PentaPRO](../skills/penta-pro/SKILL.md) still owns the specification, [Software Delivery](../skills/software-delivery/SKILL.md) still owns implementation coordination, [Peer Review](../skills/peer-review/SKILL.md) still owns read-only code assessment, [Git Ship](../skills/git-ship/SKILL.md) still owns Git publication, and [Production Operations](../skills/production-operations/SKILL.md) still owns deployment and runtime evidence.

## Why this layer is missing

At the time of this proposal, the collection answered **what to do** in each domain but lacked a packaged answer to **who acts next, with which inputs, and what evidence authorizes the next stage**. In practice, a long agent session can mix intake, specification, implementation, review and shipping in one context. That works for small changes. It breaks down when:

- the specification and the implementation disagree;
- the same context both writes and approves the change;
- a test passes but the runtime target was never exercised;
- documentation, links or OpenSpec tasks drift from the code;
- a commit is treated as a release;
- a subagent is asked to review without a clean packet of requirements and evidence.

The factory layer makes those boundaries explicit and repeatable.

## Evidence base

| Source | What it contributes |
| --- | --- |
| [Castas Android retrospective](relatorio-retrospectiva-castas-android.pdf) | Seven journeys, environment failures, parity defects, review findings, release limits and a first seven-gate model. Historical snapshot: Android `9ce150a`, web `791ef01`, collection `95abba6`, 2026-11-09. |
| Castas Codex history | 24 recorded sessions across the Castas working directories, including 9 primary user sessions and their review/guardian subagents. Shows task shape, model changes, compaction and repeated publication prompts. |
| [Castas repository](https://github.com/55area/castas) | Monorepo consolidation, GitHub Flow, CI repair, JDK 25/Gradle 9 migration, API 36 device test, current `main` at `6e3ef53`. |
| This collection's history at proposal time | Setup PentaPRO iterations, a project-scoped logging hook followed by a temporary narrow rule-only version, 23 skills, version and link maintenance. The full repository setup was restored later; the current catalog has 24 skills. |
| [SDD walkthrough notes](SDD_step-by-step.md) and the [engineering guide](guia-consolidado-desenvolvimento-com-agentes.pdf) | Existing guidance for discovery, change contracts, implementation gates, verification and release. |

The retrospective is a historical record. Later Castas commits changed the build, documentation, CI and PentaPRO structure. Reuse its lessons, not its exact revision claims.

## What the evidence shows

### 1. Environment preflight must precede implementation

The Castas Android bootstrap failed on an unconfigured SDK and on Gradle loading `libnative-platform.so`. The OpenSpec integration also hit `EROFS` while writing under `.agents/skills`. Device installation later exposed an app-icon/launcher problem on an Android 8 phone. These are not coding defects. They are target-availability defects that were discovered after implementation had started.

**Control:** gate 0 must prove that the intended build, test and runtime path works before the first feature slice.

### 2. The executable contract must name its owner

The web scorer used `3/2/1/0`, while the Android "About" wireframe said `4/3/2/1`. The code was consistent with the scorer, but the copied document was not. The Android README also inherited a `localStorage` claim and a license path that did not apply to Android. A later Android release still lacked signed production packaging and physical-device installation/update evidence.

**Control:** specification review must identify the canonical source for each material rule and mark copied claims as unverified until checked on the destination platform.

### 3. A broad prompt still needs vertical slices

The first Android implementation reached 6 of 12 tasks before the first real-device audit. The audit then found rotation state loss, contrast problems and an API-level lint issue. The work was technically substantial, but the first runnable journey had not been exercised early enough.

**Control:** planning must produce slices with an observable outcome, a real entry point and a check. The first slice must run on the target, not only compile.

### 4. Verification and review are different jobs

The Castas history records two review axes: specification review and standards review. The closing audit also used a separate model and fresh context. That separation found issues that the implementation context had accepted as done. The retrospective is careful not to attribute quality to the model change alone, because the closing round also had more precise acceptance criteria, prepared tools and reproduced findings.

**Control:** verification answers "did the required checks run on this snapshot?" Review answers "is this change correct against the contract and likely to fail in a way the checks miss?" Keep both, and keep the reviewer independent of the implementer.

### 5. Publication, release and deployment are separate states

Castas had a green CI run, a local AAB, and still no signed production artifact or verified store installation. CI itself failed once at `sdkmanager` before Gradle started. A commit or a green build is not a release.

**Control:** Git publication, artifact signing, store publication and live deployment each get their own gate and their own evidence.

### 6. Skills must be selected and observed, not just installed

The retrospective compared 13 tracked `SKILL.md` files byte-for-byte with the collection and found them identical. That proves installation, not activation. It also records that the host integration failed at first, so direct reading substituted for native skill activation. The observed effects came from specific methods: five pillars, UI contract, Gradle/DataStore, tests, security and review.

**Control:** each task packet names the owner skill and the artifact or check that proves its effect. "The skill is installed" is not evidence of use.

### 7. Simplicity is a gate, not a taste

At the time of this proposal, Setup PentaPRO had been narrowed to the portable `AGENTS.md` rule after adding a project-scoped capture core, command-line adapter and per-host recipes. Its broader repository setup was subsequently restored in version 1.5.0, while hook installation remains outside the active setup workflow. The intermediate changes illustrate the cost of changing scope without reconciling every dependent artifact.

**Control:** specification review must challenge scope and maintenance cost. A capability that is optional must not become a second mandatory path. Remove or archive superseded assets in the records gate.

### 8. Long sessions accumulate context debt

One recorded Castas Android session reached about 107.6 million input tokens, mostly cache reads, with two compactions. Other primary sessions reached roughly 30 million and 39 million input tokens. A single context carried discovery, implementation, audit, release and Git work across many turns.

**Control:** keep the orchestrator's state compact, give each subagent only its packet, and start review/verification in a fresh context.

### 9. Authorization must be explicit at each irreversible step

The Castas and collection histories show repeated, careful distinctions between implementation, commit, push, deploy and release. They also show what happens when a user says "do everything": the agent must still stop at actions the project has not authorized, such as signing credentials, store submission or production traffic.

**Control:** the run manifest records authorization as a set of explicit capabilities, not as a general "done" flag.

### 10. The branch and release model is project-owned

Castas moved from a `develop` branch to GitHub Flow with `main` as the source of truth, integrated the old branch, and removed it. A later CI repair used a short-lived branch and a pull request. The agent followed the project's decision; it did not invent a permanent integration branch.

**Control:** G0 records the branch, worktree and merge policy. G8 publishes only the authorized ref and does not merge, rebase or force-push by habit.

## Design principles

1. **One run, one state machine.** Every request becomes a run with an ID, a manifest and an ordered set of gates.
2. **Canonical records stay in the project.** OpenSpec, PentaPRO, issues, ADRs and the UI contract remain authoritative. The run folder is an index and evidence ledger, not a second specification.
3. **One role per subagent.** A subagent gets a narrow packet, a write scope and an output contract. It does not inherit the whole conversation.
4. **Read-only review and verification.** The reviewer and verifier do not edit source. Fixes return to an implementation role.
5. **Fresh context for independent judgment.** The reviewer sees the contract, the diff and the evidence, not the implementer's rationale.
6. **Evidence before claims.** A check is `executed`, `inherited`, `unavailable` or `not applicable`. It is never "assumed".
7. **Vertical slices.** Every implementation task leaves a usable behavior or a named prerequisite whose dependent behavior and check are identified.
8. **Stop on a material gate.** Missing authority, a failed required check, a contradictory contract or an unavailable target keeps the gate open. Independent work may continue.
9. **Bounded autonomy.** Retries, loops and delegation are capped. The orchestrator escalates instead of spinning.
10. **Measure the process.** Gate pass rate, rework, escaped defects, runtime coverage and cost decide whether this workflow is worth keeping.

## Pipeline at a glance

The pipeline is sequential at the gate level. Some gates fan out and rejoin.

| Gate | Name | Primary owner | Main output | Exit criterion |
| --- | --- | --- | --- | --- |
| G0 | Intake and preflight | Orchestrator + preflight subagent | Run manifest, environment report | Scope, authority, repository and target path are known; baseline checks run |
| G1 | Specification review | Spec panel | `spec-review.md`, reconciled contract | No blocking ambiguity; every acceptance criterion has an owner and a feasible check |
| G2 | Plan and slice | Planner | `plan.md`, task packets | Every task has an outcome, paths, dependencies, check and stop condition |
| G3 | Build | Implementer | Task diff, local check result | The task's check passes on the task snapshot; no out-of-scope change |
| G4 | Verify | Verifier | Evidence ledger, coverage matrix | Required checks executed on the final snapshot, or explicitly waived |
| G5 | Code review | Reviewer | Review report with findings | `No blocking findings`, or a bounded fix loop |
| G6 | Fix and re-review | Fixer + verifier + reviewer | Resolution record | Every blocker closed and rechecked |
| G7 | Records and consolidation | Records owner | Reconciled specs, tasks, docs and links | Records match the code; no stale claim or broken link |
| G8 | Ship | Shipper | Commit, push or PR, remote confirmation | Reviewed revision is published to the intended ref; CI state reported |
| G9 | Release and deploy | Release owner | Signed artifact, rollout record, live evidence | Only when separately authorized; served revision and recovery verified |
| G10 | Retrospective | Retro subagent | Metrics and lessons | Findings are recorded; skill changes require evidence |

`BLOCKED`, `WAITING_FOR_HUMAN`, `DONE` and `FAILED` are terminal or paused states, not gates. A run can stop at any gate without losing prior evidence.

## Gate contracts

### G0 — Intake and preflight

**Purpose:** turn a prompt into an authorized, executable run.

**Subagent:** `factory-intake` (read-only) plus an optional `factory-preflight` for commands.

**Inputs:** the user prompt, repository instructions, current branch and worktree, issue or change reference, and any stated authorization.

**Actions:**

- Identify the repository root, base revision, branch, remote and active Git operation.
- Record the project's branch, worktree and merge policy, including protected branches and the role of `main`.
- Read the project instructions and the relevant app guides.
- Inventory the skills that could own the work; select the smallest set.
- Record what is authorized: specify, implement, test, commit, push, open a PR, merge, sign, deploy, publish.
- Run safe baseline checks that distinguish inherited failures from new ones.
- Prove one real path through the target: build, test runner, emulator/device, browser, API sandbox or package tool.
- Capture unavailable prerequisites explicitly.

**Output:** `run.json` with intent, scope, non-goals, risk, authorization, baseline evidence and gate status.

**Stop conditions:** ambiguous repository or scope; conflicting instructions; detached HEAD or an in-progress merge/rebase/cherry-pick; missing authority for a requested irreversible action; no executable target path for work that requires one.

**Skills:** [Agent Instructions](../skills/agent-instructions/SKILL.md) for project guidance; [Software Delivery](../skills/software-delivery/SKILL.md) for baseline and execution controls.

### G1 — Specification review

**Purpose:** make the contract reviewable before code.

**Subagents (parallel, read-only):**

| Lens | Question | Output |
| --- | --- | --- |
| Product and scope | What user outcome, non-goals and observable acceptance criteria govern this change? | Criteria with stable IDs and sources |
| Contract and architecture | Which schemas, APIs, data, compatibility or platform-parity decisions change? | Contract delta and affected consumers |
| Verification | How will each criterion be checked, on which target, with what failure case? | Check matrix and evidence plan |
| Risk and security | Which permissions, private data, destructive effects or release risks are material? | Risk register and required controls |
| Change-record validation | Is the OpenSpec change or project-native record complete and internally consistent? | Validation result and missing scenarios |

**Inputs:** run manifest, existing PentaPRO pillars, OpenSpec change or spec, UI contract, issue and baseline code.

**Rules:**

- Identify the owner of each material rule. A copied README, mock or test is evidence, not automatic authority.
- Mark copied or platform-specific claims as unverified until checked on the destination.
- Every acceptance criterion needs an observable result and a feasible check; negative and boundary cases are included where the contract depends on them.
- A proposal is not an acceptance. The review can recommend, but the responsible human accepts consequential product decisions.
- If the change is underspecified, use exploration or create the missing change record rather than coding around the gap.

**Output:** `spec-review.md` with blocking findings, accepted criteria, open decisions and the check matrix.

**Exit criterion:** no blocking ambiguity; the contract is accepted or explicitly scoped for incremental specification; every criterion maps to at least one planned check.

**Skills:** [PentaPRO](../skills/penta-pro/SKILL.md), OpenSpec `explore`/`propose`, [UI Design](../skills/ui-design/SKILL.md) when the interface contract changes, [Cybersecurity](../skills/cybersec/SKILL.md) when risk is material.

### G2 — Plan and slice

**Purpose:** convert the accepted contract into executable tasks.

**Subagent:** `factory-planner`.

**Inputs:** accepted spec review, baseline code map, environment report.

**Rules:**

- Split by observable result, not by file or layer.
- Start with a useful path through the real entry point.
- Shared schema or interface changes come before dependents.
- Each task packet names its outcome, owning paths, consumed and produced contracts, prerequisites, acceptance check, evidence required, rollback and stop conditions.
- Mark tasks that can run in parallel without write conflicts.
- Do not create a task without a check or a named dependent check.

**Output:** `plan.md` and one packet per task in `tasks/`.

**Exit criterion:** every acceptance criterion is covered; the dependency graph has no cycles; the first slice is runnable on the target.

**Skills:** [Software Delivery](../skills/software-delivery/SKILL.md), OpenSpec `apply-change` task list when applicable.

### G3 — Build

**Purpose:** implement one coherent task.

**Subagent:** `factory-implementer`, one per task or per independent slice.

**Inputs:** task packet, relevant spec excerpt, affected source and callers, baseline evidence. It does not receive the reviewer's notes or the full conversation.

**Rules:**

- Make the smallest complete change that satisfies the task.
- Preserve existing work and meaningful tests.
- If a test-first workflow is required, observe the intended failure before the fix.
- Run the task's targeted check on the resulting snapshot.
- Stop and report if the task exposes a material contract conflict.
- Do not fix unrelated findings, reformat adjacent code or expand scope.

**Output:** diff, commands run, results, open questions and the task status.

**Exit criterion:** the task check passes; the diff is within the packet's scope; no new behavior is left without a check or a named follow-up.

**Skills:** [Software Delivery](../skills/software-delivery/SKILL.md) plus the domain owner: [UI Design](../skills/ui-design/SKILL.md), [HTTP API](../skills/http-api/SKILL.md), [MCP Server](../skills/mcp-server/SKILL.md), or the relevant native Android helper.

### G4 — Verify

**Purpose:** establish what actually ran, on which snapshot, in which environment.

**Subagent:** `factory-verifier` (read-only, independent of the implementer).

**Inputs:** task packets, final diff, spec criteria, check matrix, environment report.

**Rules:**

- Record command, revision, environment, result, duration and artifact hash.
- Distinguish executed, inherited, unavailable and not applicable.
- Exercise the real entry point, not only a unit seam, when the contract depends on it.
- Include a meaningful failure or boundary case.
- Reuse prior evidence only for the same snapshot, command, configuration and environment.
- A green build does not prove runtime behavior; a screenshot does not prove persistence; a test does not prove the packaged artifact.

**Output:** `evidence.jsonl` plus a coverage matrix mapping each criterion to evidence or a gap.

**Exit criterion:** all required checks have evidence or an authorized waiver; no acceptance criterion is silently unverified.

**Skills:** [Behavior Testing](../skills/behavior-testing/SKILL.md), native Android test helpers, [Peer Review](../skills/peer-review/SKILL.md) verification reference, [Production Operations](../skills/production-operations/SKILL.md) for deployment checks.

### G5 — Code review

**Purpose:** find consequential defects that the checks may miss.

**Subagent:** `factory-reviewer` (read-only, fresh context).

**Inputs:** accepted contract, final diff, changed-file map, evidence ledger and applicable policy. It does not receive the implementer's justification.

**Rules:**

- Follow each changed behavior through entry points, guards, effects and consumers.
- Substantiate every finding with a trigger, expected/actual behavior, impact and evidence.
- Separate blockers from questions and optional suggestions.
- Do not edit source, tests, index or configuration.
- Disclose self-review if a truly independent context is unavailable.
- A resolved thread is not a fix; re-review the new snapshot.

**Output:** `review.md` with stable finding IDs, P0–P3 severity, blocking disposition and a verdict: `No blocking findings`, `Changes requested` or `Incomplete`.

**Exit criterion:** no P0/P1 blockers; P2 findings have an explicit disposition; coverage is stated.

**Skills:** [Peer Review](../skills/peer-review/SKILL.md) with the relevant backend, frontend, Android or verification reference.

### G6 — Fix and re-review

**Purpose:** close review findings without reopening the whole change.

**Subagents:** `factory-fixer`, then the verifier and reviewer on the delta.

**Rules:**

- Each fix links to a finding ID and stays within the authorized scope.
- Re-run the affected checks and any check that could regress.
- Re-review the new snapshot, not the old thread.
- If a finding reveals a contract problem, return to G1 instead of coding around it.
- Cap the loop (for example, two rounds) and escalate a repeated or disputed finding.

**Output:** resolution record, updated evidence, updated review verdict.

**Exit criterion:** every blocker is closed and rechecked; no new blocker is introduced.

### G7 — Records and consolidation

**Purpose:** leave the project's canonical records true after the code changes.

**Subagent:** `factory-records`.

**Actions:**

- Reconcile OpenSpec tasks, scenarios and archive state.
- Update affected PentaPRO pillars, decisions, checks and revision history.
- Update README, app guides, UI contract, changelog and ADRs where they make claims about the changed behavior.
- Validate links, anchors, versions, generated files and ignored paths.
- Record actual checks and remaining gaps in PROOF or the project's evidence owner.
- Remove or archive superseded assets and instructions.

**Output:** `records.md` with changed records, validation commands and remaining gaps.

**Exit criterion:** no stale claim, broken link, unreconciled task or orphaned asset remains in the changed scope.

**Skills:** [PentaPRO](../skills/penta-pro/SKILL.md), OpenSpec `archive-change`/`sync-specs`, [Agent Instructions](../skills/agent-instructions/SKILL.md).

### G8 — Ship

**Purpose:** publish the reviewed Git snapshot without widening authorization.

**Subagent:** `factory-shipper`.

**Inputs:** reviewed snapshot, target branch and remote, commit/push/PR authorization, required checks.

**Rules:**

- Recheck HEAD, index and worktree against what was reviewed.
- Stage only explicit publishable paths; preserve unrelated work.
- Inspect the candidate diff for secrets, private data and generated noise.
- Run required checks and `git diff --check`; validate moved links.
- Commit once with a concise English message unless the project requires otherwise.
- Push only the intended ref; verify the remote object ID.
- Do not merge, deploy, force-push or rewrite history without separate authority.

**Output:** commit hash, branch and destination, verified push state, CI run reference, PR URL if requested.

**Exit criterion:** the remote ref matches the reviewed commit; CI is reported as pending, passing or failing; any failure is retained and explained.

**Skills:** [Git Ship](../skills/git-ship/SKILL.md).

### G9 — Release and deploy

**Purpose:** turn a published revision into a verified artifact or running service.

**Subagent:** `factory-release` with the project's release authority.

**Rules:**

- Require explicit authorization for signing, store submission, production traffic, paid resources and data changes.
- Pin the artifact to a commit and immutable version.
- Verify the packaged artifact, not only the source build.
- Exercise install, upgrade, first run, failure and recovery on the target channel.
- Record the served revision, health signals, rollout window and rollback path.
- A successful pipeline job only proves what that job observed.

**Output:** release record with artifact hash, target, checks, observed behavior, rollback status and remaining risks.

**Exit criterion:** the intended artifact is served or installed and verified; recovery is understood; unresolved risks have an owner.

**Skills:** [Production Operations](../skills/production-operations/SKILL.md) for hosted services; project release procedures for mobile and desktop packages.

### G10 — Retrospective

**Purpose:** turn one run into reusable evidence without inventing certainty.

**Subagent:** `factory-retro` (read-only analysis).

**Actions:**

- Compare planned and actual outcomes, gate times, rework, review findings, escaped defects and unavailable checks.
- Identify the smallest process or skill change that would have prevented a confirmed failure.
- Attribute causes to missing evidence, unclear ownership, tool limits or scope, not to model reputation.
- Add a regression check or a concrete instruction change only when the evidence supports it.

**Output:** `retro.md` with metrics, confirmed lessons, proposed changes and owners.

**Exit criterion:** lessons are recorded; any skill or workflow change is scoped and evaluated separately.

## Subagent contracts

| Role | Default context | Write scope | Output | Model tier |
| --- | --- | --- | --- | --- |
| `factory-orchestrator` | Run manifest and gate summaries | Run state only | Gate transitions, escalations | Strong coordinator |
| `factory-intake` | Prompt, instructions, repository state | None | Run manifest draft | Fast, reliable |
| `factory-preflight` | Manifest, target commands | None (commands may write caches) | Environment report | Fast with tools |
| `factory-spec-product` | Manifest, product records, request | None | Criteria and scope findings | Strong |
| `factory-spec-contract` | Manifest, architecture, schemas, code map | None | Contract delta | Strong |
| `factory-spec-verification` | Manifest, criteria, test inventory | None | Check matrix | Strong |
| `factory-risk` | Manifest, data flows, permissions, release context | None | Risk register | Strong |
| `factory-planner` | Accepted spec, code map | Plan artifacts only | Task packets | Strong |
| `factory-implementer` | One task packet and relevant source | Task paths | Diff and local evidence | Capable implementer |
| `factory-verifier` | Spec, diff, environment | None | Evidence ledger | Strong with tools |
| `factory-reviewer` | Spec, diff, evidence, policy | None | Review report | Strong reviewer |
| `factory-fixer` | Findings and relevant source | Authorized fix paths | Fix diff and recheck | Capable implementer |
| `factory-records` | Accepted change and docs | Record paths | Reconciled records | Fast to capable |
| `factory-shipper` | Reviewed snapshot and Git authority | Git index and ref | Commit and push record | Fast with Git tools |
| `factory-release` | Released revision and target authority | Release environment | Release record | Strong with target access |
| `factory-retro` | Run artifacts and metrics | None | Retrospective | Strong analyst |

Model names are intentionally omitted. Assign the smallest model that passes the role's evaluation. A bigger model is not a substitute for a missing check, a clean packet or an independent context.

## Handoff artifacts

Keep the run folder small. The canonical specification stays in the project; the run folder links to it. The current runtime contract is [durable run persistence](../skills/software-factory/references/run-records.md), which supersedes the earlier `.factory/runs/` proposal. Only `run.json` is required for the default persisted format; the other files below are optional evidence locations, reused from existing project records where available.

```text
docs/agents/runs/<run-id>/
├── run.json            # state, scope, authorization, gate status
├── preflight.md        # environment and baseline evidence
├── spec-review.md      # accepted criteria, findings, open decisions
├── plan.md             # slices, dependency graph, coverage map
├── tasks/
│   ├── T-001.md        # one task packet
│   └── T-002.md
├── evidence.jsonl      # one record per executed check
├── review.md           # findings and verdict
├── records.md          # reconciliation and validation
├── release.md          # only when G9 is authorized
└── retro.md            # metrics and lessons
```

If the project already has a run record or tracker, use it and link the artifacts instead of creating a parallel structure. The run folder must not become a second source of truth for requirements.

### Run manifest

The [packaged helper](../skills/software-factory/scripts/run_state.py) initializes the complete versioned envelope and validates compare-and-save checkpoints. Use its [format version 1](../skills/software-factory/references/run-records.md#format-version-1) rather than the former design-only intent/repo/G0-G10 JSON shape. Record state, repository/branch/base commit, source fingerprint, canonical references, gates, tasks, authorized operations, blockers, next action and checkpoint history. Only the orchestrator writes; agents return evidence against the supplied record version and input snapshot. This is a local record contract with deterministic structural checks, not a general distributed workflow engine.

### Task packet

```json
{
  "task_id": "T-002",
  "run_id": "result-deletion",
  "record_path": "docs/agents/runs/result-deletion/run.json",
  "record_version": 2,
  "input_fingerprint": "<captured source fingerprint>",
  "outcome": "A saved result can be deleted and does not reappear after restart",
  "owner_skill": "android-data-layer",
  "paths": ["android/app/src/main/java/...", "android/app/src/androidTest/..."],
  "contracts": ["SPEC-3.2", "DEC-7"],
  "depends_on": ["T-001"],
  "check": "./gradlew :app:connectedDebugAndroidTest",
  "evidence_required": ["test output", "device API level", "tested revision"],
  "stop_if": ["schema conflict", "no device available"]
}
```

### Evidence record

```json
{
  "id": "E-014",
  "task_id": "T-002",
  "run_id": "result-deletion",
  "record_path": "docs/agents/runs/result-deletion/run.json",
  "record_version": 2,
  "input_fingerprint": "<captured source fingerprint>",
  "criterion": "SPEC-3.2",
  "command": "./gradlew :app:connectedDebugAndroidTest",
  "revision": "abc1234",
  "environment": "AVD API 35, Android 15",
  "result": "pass",
  "artifacts": ["android/app/build/reports/..."],
  "timestamp": "2026-11-19T14:02:00-03:00"
}
```

## Context and handoff rules

1. **The orchestrator never forwards the full conversation.** It sends a packet: intent, accepted criteria, task scope, relevant paths and evidence.
2. **The implementer does not see the reviewer's notes.** It sees the contract and the task, not a pre-judgment.
3. **The reviewer does not see the implementer's rationale.** It sees the contract, the diff and the evidence. This reduces anchoring.
4. **The verifier does not trust a claim.** It runs the command or records why it cannot.
5. **A gate handoff is explicit.** The output names what passed, what is missing, what is blocked and who owns the next action.
6. **A new session is acceptable.** If context is compacted or the host loses state, resume from the run manifest and the last gate output, not from memory.
7. **No hidden scope.** A subagent that discovers a wider effect reports it to the orchestrator instead of editing outside its packet.

## Automation mechanics

The workflow is host-agnostic. Use the strongest mechanism the host provides, and fall back to separate sessions plus files.

| Host capability | Mapping |
| --- | --- |
| Native subagents or task tool | One subagent per role; pass the packet in the prompt; require the output schema. |
| Fresh session / new chat | Use for review, verification and retro when subagents are unavailable. |
| Worktrees | One isolated worktree per independent implementation slice; never two writers in the same worktree. |
| CI | Enforce G4/G7 checks that can fail independently; attach evidence artifacts. |
| Git hooks | Run formatting, link and secret checks; do not hide a failing gate. |
| Project tracker | Link the run ID, task IDs and evidence; do not duplicate the canon. |

Recommended orchestration loop:

```text
load run manifest
while state not terminal:
  choose the next gate
  build the packet for that gate
  dispatch the owner (subagent, session, or human)
  validate the output against the gate contract
  if pass: record evidence, advance
  if blocking: record the gap, pause dependent work, continue independent work
  if authority missing: set WAITING_FOR_HUMAN and stop
```

The orchestrator should be deterministic where possible: the same manifest and gate output should produce the same next action. It should not "decide" that a check passed; it should read the evidence.

## Human decision points

Keep these explicit. Automating them away is a process defect.

- Accepting product scope, non-goals and consequential trade-offs.
- Accepting a specification when the project requires full prior specification.
- Authorizing destructive, irreversible or externally visible actions.
- Approving a security exception or a waived required check.
- Merging a PR, signing an artifact, submitting to a store, enabling production traffic.
- Accepting residual risk when evidence is unavailable.

The orchestrator may recommend, but it must not manufacture approval.

## Metrics

Measure the workflow, not only the output.

| Metric | Definition | Target direction |
| --- | --- | --- |
| First-pass gate rate | Gates that pass without a fix loop | Up |
| Rework ratio | Fix rounds per completed task | Down |
| Escaped defects | Confirmed defects found after the gate that should have caught them | Down |
| Runtime coverage | Acceptance criteria with executed target evidence | Up |
| Evidence freshness | Evidence tied to the final reviewed revision | Up |
| Cycle time | Time from G0 to G8 | Down, without hiding gates |
| Human interventions | Approvals and unblocks per run | Stable or down |
| CI flake rate | Failures unrelated to the change | Down |
| Cost per completed task | Tokens, tools and human time | Down |
| Spec churn | Accepted criteria changed after G3 starts | Down |

Do not compare models without fixing the task, tools, permissions, starting state and acceptance checks. The Castas history shows why: the closing round had better evidence and a clearer contract, so a model comparison would be confounded.

## Pilot: Castas result deletion

Use the next small Castas change as the pilot. The retrospective already suggests "delete a saved result" as a user problem with a clear before/after state.

**G0:** confirm the Castas root, `main` at the current revision, web build, Android Gradle build, an available emulator or device, and OpenSpec validation. Record which checks are unavailable.

**G1:** review the existing affective-polarization spec and PentaPRO records. Define the deletion contract for web and Android: what is deleted, what confirmation is required, what happens to the current result, how restart behaves, and which translations and result formatting are affected.

**G2:** create separate web and Android tasks with a shared domain contract. The first slice should be one platform's complete deletion journey, not a shared abstraction.

**G3:** implement the first slice with the domain owner. Keep the other platform pending until the contract is stable.

**G4:** exercise the real path: delete, restart, reopen, confirm absence; test cancel, empty state and storage failure. Record device/emulator API and browser.

**G5:** review the diff against the contract and the evidence. Look for data-loss, race, stale-state and cross-platform parity defects.

**G6:** fix only confirmed findings and recheck.

**G7:** update the OpenSpec change, PentaPRO records, UI contract and README claims. Validate links and translations.

**G8:** ship only when the user authorizes commit/push. Report CI.

**G9:** not requested unless the user explicitly asks for release.

**G10:** measure the pilot and decide whether the factory layer earned its overhead.

## Rollout

1. **Write the contract, not the platform.** Start with this document, a run-manifest template and task/evidence templates. Do not build a scheduler or database.
2. **Pilot on one change.** Use Castas or a disposable repository. Run the gates manually with subagents where available.
3. **Measure.** Record gate pass rate, rework, evidence gaps and human interventions.
4. **Package only what repeated.** This proposal led to a first `software-factory` instruction package. A real pilot must still establish whether its orchestration contract improves outcomes; avoid duplicating existing procedures.
5. **Add host adapters.** Provide OpenCode, Claude Code and Codex invocation examples only after the host-agnostic contract is stable.
6. **Add CI enforcement.** Encode the checks that can fail independently: spec validation, tests, link checks, secret scanning, artifact verification.
7. **Review the review.** After two or more pilots, compare outcomes with and without the workflow. Remove gates that do not change a decision.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Orchestration overhead exceeds the change | Scale gates to risk; a one-line copy fix does not need a full spec panel. |
| Agents agree with each other | Fresh context for review; reviewer sees evidence, not rationale; require disconfirming checks. |
| Handoff packets drift from the canon | Link canonical IDs; re-read the source on resumption; records gate reconciles. |
| Gate theater | Every gate must be able to fail and must name the decision it protects. |
| False confidence from green CI | Keep runtime, packaging and release evidence separate. |
| Secret or private-data leakage | Packets exclude secrets; shipper scans the outgoing range; use references, not values. |
| Cost and latency | Small models for mechanical roles; parallel only independent work; cap retries. |
| Host differences | Keep the contract host-agnostic; adapt invocation, not the gates. |
| Unreviewed concurrent work | Worktrees, explicit paths, snapshot checks and a clean handoff. |
| A subagent expands scope | Explicit write scope and a stop-and-report rule. |

## Recommendation

Adopt the **gates and handoffs** before adopting any orchestration product. The highest-value changes are:

1. A preflight gate that proves the target path before code.
2. A specification review that names the canonical rule and its check.
3. Vertical task packets with evidence requirements.
4. Independent verification and review in fresh contexts.
5. A records gate that keeps OpenSpec, PentaPRO, README and links true.
6. A ship gate that distinguishes commit, push, release and deploy.

The first [software-factory skill](../skills/software-factory/SKILL.md) now owns the portable sequence, packets, gates and evidence ledger. A pilot should test its value before claiming an efficiency gain. It does not reimplement [PentaPRO](../skills/penta-pro/SKILL.md), [Peer Review](../skills/peer-review/SKILL.md), [Git Ship](../skills/git-ship/SKILL.md) or [Production Operations](../skills/production-operations/SKILL.md); those skills remain the source of their methods.

## Related records

- [Castas Android retrospective](relatorio-retrospectiva-castas-android.pdf)
- [Engineering guide](guia-consolidado-desenvolvimento-com-agentes.pdf)
- [SDD walkthrough notes](SDD_step-by-step.md)
- [Skill routing](SKILL-ROUTING.md)
- [Evaluation procedure](SKILL-EVALUATION.md)
- [Maintenance review](FINAL-SKILL-REVIEW.md)
