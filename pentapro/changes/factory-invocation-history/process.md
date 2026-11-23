# PROCESS — tasks and authority

- [x] T1 Orchestrator: save contract/run record; specification review before implementation.
- [x] T2 Implementer: event helper and behavior tests (software-factory/scripts/run_events.py, scripts/tests/test_factory_events.py).
- [x] T3 Orchestrator: reconcile workflow/setup/project guidance, scenarios, versions and catalogs.
- [x] T4 Verifier/reviewer: independent fixed-snapshot verification and code review; route corrections.
- [ ] T5 factory_shipper: review intended changes, commit and normal push; preserve unrelated staged document. Verify exact remote revision and CI where available.
- [ ] T6 Orchestrator: after confirmed push, reconcile eligible local PentaPRO consumers and verify preservation/idempotence.
- [ ] T7 Orchestrator: record retrospective/lessons and report completed/local/published states.

Developer request explicitly authorizes T1–T7 and source commit/normal push. User asked factory_ship; actual exposed identity is factory_shipper, with configured GPT-6 Luna/high settings. This direct delivery instruction is separate from factory result acceptance: do not claim acceptance/consolidate/archive the change until the developer actually accepts the completed result. No consumer commits/pushes, force push, merges, deployment, global settings or hooks are authorized.

Protocol: docs/agents/continuous-improvement.md; consult LL-001 (environment failures), LL-002 (consumer propagation), LL-003 (closure state). Main session alone writes shared state/lessons; roles return evidence and candidates. Bound corrections to two attempts for the same cause. Current reconciliation: In progress. Preserve the original staged blob and index entry of docs/pentapro-simulacao.md. All implementation and publication gates remain pending until observed.

Implementation handoff: run_events.py and focused event tests implemented by factory_implementer; 10 focused tests passed after preserving split usage metrics. Workflow, role adapters, setup guidance and plugin versions integrated by main session. Independent verification/review pending on the resulting fixed snapshot. Bootstrap role calls predated helper availability; see the explicit capture-gap receipt, not invented events.

Independent verification/review complete. REV-INV-01 corrected and rereviewed; source behavior tests pass within documented environment limits. User explicitly requested factory_shipper next and normal source push; consumer rollout remains conditional on exact remote confirmation. Finished-result acceptance and baseline consolidation/archive remain pending, not fabricated.
