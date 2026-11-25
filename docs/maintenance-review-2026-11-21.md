# Closing maintenance review — 2026-11-21

This report describes an earlier snapshot. The [final follow-up](maintenance-final-follow-up-2026-11-21.md) supersedes its shipper model restriction and records the later inventory and checks; historical observations below remain unchanged.

## Scope and verdict

Maintainer self-review of the current working tree, including the pending cross-host roles and PDSA changes. This is not an independent review or a release certification. All 24 skill entrypoints were read for declared purpose, action authority, ownership, evidence, failure handling and companion fallback. Supporting references/templates were inspected by risk and dependency; all distribution Markdown files and local links are subject to the structural validator. Historical reports, research drafts and exported PDFs retain their snapshot; their content inventory and provenance were checked, without regenerating PDFs or claiming page-by-page visual QA. The review did not re-execute every external technical example or revalidate every remote link/API.

Verdict: the scoped maintenance fixes and available offline checks are complete, with the adoption limitations below. No universal “100% ready for any developer” conclusion follows. Project tools, privileges, models and required checks must still be established during setup and actual use. Changes remain local until separately authorized Git delivery.

## Skill assessment

| Owner | Purpose and contract assessment |
| --- | --- |
| agent-instructions | Instruction/package maintenance; canonical owner, standalone packaging and evidence boundaries retained. |
| setup-pentapro | Non-destructive project setup, complete prompt rule, selected-host role installation and PDSA pointers; repaired role identity mapping and clarified legacy logger limits. |
| penta-pro | Five-pillar specification, source/status distinction and readiness separate from implementation authority; initializer has preservation and unsafe-path regressions. |
| peer-review | Read-only defect/test-effectiveness assessment, fixed snapshot and honest independence; fixes follow actual authority. |
| cybersec | Scoped threat/control assessment and authorized hardening; cannot establish invulnerability or live configuration from source. |
| ui-design | Screen contract, platform-specific references and scoped implementation; local concepts remain separate from native/runtime validation. |
| diagnose-defect | Evidence-driven diagnosis, causal hypotheses, bounded reassessment and authorized fix verification. |
| behavior-testing | Observable assertions, correct failing baseline and meaningful boundaries; test-only mode preserves product source. |
| http-api | Caller-facing compatibility, effect-boundary authorization, idempotency/recovery and representative real-handler checks. |
| mcp-server | Version/transport/tool contract, authorization and client checks; current SDK smoke remains a separate optional dependency. |
| software-delivery | Incremental authorized implementation, canonical contracts, preservation and revision-matched completion evidence. |
| software-factory | Proportional orchestration, six role contracts, exact host identity, PDSA handoffs and orchestrator-only lesson writes. |
| production-operations | Target identity, deployment/data authority, uncertain effects and verified recovery remain explicit. |
| technical-research | Primary evidence, counterexamples and bounded experiments; research grants no production effects. |
| git-ship | Exact reviewed scope/index, branch-only authorized publication, outgoing secrets review and actual remote-ref confirmation. |
| pr-quiz | Explicitly requested comprehension aid; public answer key and informational status cannot become security/review approval. |
| android-module-structure | Existing project/toolchain first; examples are conditional, no forced architecture or toolchain migration. |
| android-di-koin | Composition/lifetime/worker ownership and installed-version checks; preserve other DI stacks. |
| android-data-layer | Storage/transport ownership, account-partitioned commits, cancellation and replay/restore constraints. |
| android-error-handling | Typed expected outcomes, cancellation preserved, unknown/programming defects visible and deadline/retry ownership. |
| android-background | Durable scheduling, idempotency, startup ownership, session fencing and bounded work. |
| android-unit-testing | Deterministic scheduling, authentic fakes, meaningful state/cancellation assertions and explicit runtime limits. |
| android-integration-testing | Actual selected boundaries, positive/denied controls and migration/data preservation evidence. |
| android-ui-testing | Real input/lifecycle/selectors and device-aware accessibility evidence, not mocked callbacks or arbitrary sleeps. |

No justified behavioral rewrite was identified for the unchanged entrypoints in this review. This assessment is an instruction-contract review, not a benchmark showing equal effectiveness on all hosts or models.

## Repairs and evidence

- Host identity: OpenCode identifies a profile by its filename/path, whereas the workflow uses logical underscore names. Setup and packets now require resolving the discovered identity (for example `factory_shipper` to `factory-shipper`). Other hosts retain their documented identity behavior; no implicit alias is claimed.
- Added host metadata, canonical instruction parity and unknown-field checks across all 30 adapters, including the existing mandatory shipper model/skill and every PDSA handoff. These checks can catch malformed/drifting distributed files; they cannot prove discovery or tool execution.
- Reproduced credential-like text leaking through a synthetic attachment label in the legacy logger's formatter. A new regression failed before correction; attachment labels now receive the same best-effort redaction as body text. No real credential was used. Current setup still installs no hooks.
- Clarified that legacy hook recipes and helpers do not implement all current prompt-capture requirements on their own; historical rotation recipes are not authority to reset the active append-only log.
- Updated the operational factory guide from five to six roles and added cross-host identity, mandatory shipper model limits and PDSA/lesson recording. README versions and maintenance pointers are synchronized. Historical evidence was not relabeled as current validation.

## Executable inventory and test judgment

A distinct test file for every module is not necessary; observable contract coverage can be indirect. Test count is not line/branch coverage. Fixture source is intentionally seeded and must not be “fixed” as production code.

| Executable/helper | Coverage and judgment |
| --- | --- |
| `skills/penta-pro/scripts/init_pentapro.py` | Dedicated `test_init_pentapro.py`; initialization, rerun, existing content and unsafe-path cases. Appropriate offline regression coverage for the maintained contract, with live project workflows still separate. |
| `skills/ui-design/scripts/prototype_tools.py` | Dedicated `test_prototype_tools.py`; inputs, contrast, fragments, injection boundaries and export behavior. Appropriate bounded-helper coverage, not browser/native accessibility certification. |
| `skills/pr-quiz/scripts/publish_quiz.py` | Dedicated `test_publish_quiz.py`; invalid JSON/options, rendering and mocked publication/freshness controls. No live GitHub write performed. |
| `skills/pr-quiz/assets/pr-quiz.yml` | Actual embedded handler exercised by `skills/pr-quiz/scripts/tests/workflow.cjs` with offline API doubles; hosted events/token permissions remain separate. |
| `scripts/validate_collection.py` | Dedicated `test_validate_collection.py`; metadata/link/portability defects and valid controls. Also runs against the complete candidate inventory. |
| `scripts/run_skill_evals.py` | `test_run_skill_evals.py` exercises candidate export, lifecycle, status, manifests, grading and controls; model execution is not part of default offline checks. |
| `scripts/eval_outcomes.py` | Indirect tests in the same runner suite cover actual scoring and clean/seeded fixtures; separate filename not required. |
| `scripts/eval_isolation.py` | Real mount/socket/resource probes plus grader/control tests exercise its boundary. Linux/Bubblewrap/libseccomp requirements are intentional and must not be weakened when unavailable. |
| `evals/check_receipts.py` | Used by actual clean, seeded, hard-coded and false-success tests in runner suite. It is an independent grader, not application code. |
| `evals/check_mcp_sdk.py` | Self-checking in-process SDK smoke with assertions, not another production helper. Not run here because MCP SDK/HTTP dependencies are absent; acceptable as optional validation only while that gap is explicit. |
| Legacy `core.mjs`, `log-prompt.mjs` | `test_agents_log.mjs` tests formatter/redaction/safe append and real CLI in temporary directories; attachment regression added. No current host hook installed or certified. |
| Legacy `opencode.ts` | Core logic tested indirectly; no installed-host API integration test. Acceptable only as historical, separately reviewed adapter material; not ready for unqualified installation. |
| Test harnesses and `evals/fixtures`/`overlays` | Exercised as tests or positive/negative inputs; recursive “tests of tests” are not required, but sensitivity controls are required for grading claims. |

## Executed checks and environment

Python 3.12.6, PyYAML 6.0.1, Node v27.0.0-alpha.0.0.0 and installed OpenSpec CLI. CI specifies Python 3.12, PyYAML 6.0.3 and Node 24; the exact CI runtime was not recreated locally. No dependencies were installed globally.

- `python3 -m unittest discover -s scripts/tests`: 42 passed after the additional adapter test.
- `python3 -m unittest discover -s skills/penta-pro/scripts/tests`: 11 passed.
- `python3 -m unittest discover -s skills/ui-design/scripts/tests`: 26 passed.
- `python3 -m unittest discover -s skills/pr-quiz/scripts/tests`: 15 passed.
- `node skills/pr-quiz/scripts/tests/workflow.cjs`: 27 passed.
- `node --test scripts/tests/test_agents_log.mjs`: 16 passed after the attachment fix, outside the host sandbox restriction on Node `spawnSync`. The original 15 tests failed inside that restriction and passed after the scoped retry; Python execution of the same synthetic CLI also succeeded.
- `python3 scripts/run_skill_evals.py --check-isolation --grade`: mount, socket and resource probes passed, without a model call.
- `python3 scripts/run_skill_evals.py --check-cases`: case definitions checked; this does not execute model trials.
- `python3 scripts/validate_collection.py` and `git diff --check`: final inventory, local links, versions and whitespace checked. Python commands used `PYTHONDONTWRITEBYTECODE=1`.

## Remaining adoption checks

No fresh cross-model trial, live setup/rerun in all five clients, full PDSA behavioral comparison, real GitHub grading workflow, consuming Android build/device session, deployed service or production security scan was executed. Host tools, skill discovery, permissions and required model/effort need runtime evidence. In particular, `factory_shipper` remains blocked wherever GPT-6 Luna/high cannot be selected and verified; file creation is not proof of readiness. Read-only role instructions are behavioral constraints, not a separate sandbox.

The PDF exports and prior reports are historical snapshots, not synchronized generated copies of today's README or role templates. Use current entrypoints, the operational guide and project-owned contracts for runtime work. Remote documentation can change; verify the installed SDK/host version at adoption. Do not claim exhaustive software quality, security, measured savings or readiness across every developer environment from this audit.
