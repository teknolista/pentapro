# PROOF — verification plan

INV-01/03/04/05: disposable Git repository tests for multiple invocations/retries within one run, append preservation, idempotent retries/conflicts, open/interrupted histories, summaries and unknown/parallel metrics.
INV-02/06: actual CLI smoke, missing/mismatched runs, malformed JSON/ordering, symlink/hard-link/path checks, existing state compatibility and standalone installation. Failed operations preserve previous bytes.
INV-07: collection metadata/link/version/case checks, affected setup/template tests, package export checks and independently reviewed preservation behavior.
INV-08: exact source commit/ref receipt before rollout; per-project before/after inventory, customized-file disposition, prompt-log and lessons preservation, Git-index invariance and idempotent rerun.

Evidence pending execution. Run-level records: docs/agents/runs/factory-invocation-history/. No controlled model comparison, universal completeness or efficiency benefit is established by structural/helper checks. Existing staged docs/pentapro-simulacao.md has an unrelated broken external link; validate intended publication snapshot separately and preserve the staged file.

INV-09: authored standalone-role/no-owner/ordinary-skill controls plus helper checks for missing run, explicit lifecycle transitions, event retry vs invocation retry, and failed append preserving prior bytes. Model-level capture compliance remains unmeasured.

Executed focused checks: 10 event-helper tests passed by factory_implementer; 7 role-adapter checks and 12 setup/prompt-rule tests passed by the orchestrator. Available environment: Python 3.12.6; local Node 27 alpha (CI targets Node 24). Full intended-publication verification remains pending. Source metadata/case/whitespace checks passed except the known unrelated staged-document link in whole-checkout validation.

Final evidence: docs/agents/runs/factory-invocation-history/verification.md and verification-final.md, review.md and review-final.md. Full direct suites passed in the intended-publication snapshot: Python 93 root +14 PentaPRO +26 UI +15 PR quiz; Node 27 quiz +16 logger +1 OpenCode suite. One additional manifesto-boundary regression and affected setup/export gates passed afterward; unchanged-code evidence reused explicitly. Local Node27 alpha differs from CI Node24. Three disposable one-off updater controls passed. Source commit/push/CI and real consumer adoption remain pending actual receipts.
