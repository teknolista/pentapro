# Lessons learned

The main session/orchestrator maintains this project record. Factory agents return candidates and evidence; they do not write here. Write every persisted lesson entry in English, including its title and all fields, even when project specifications or conversations use another language. Translate and summarize relevant observations into English; retain technical identifiers and source quotes only when needed, with an English explanation. This applies to the project's lessons record in `docs/` or its approved equivalent and keeps lessons reusable for improving the PentaPRO skills. Keep proposed prevention separate from validated results. Lessons added after publication may remain local until the next authorized commit.

## LL-001 — Distinguish host sandbox failures from helper regressions

- Date: 2026-11-21.
- Source: main-session maintenance review; legacy logger CLI test execution.
- Context: Linux host sandbox, Python 3.12.6 and Node 27 alpha; synthetic temporary files only.
- Observation/evidence: Node `spawnSync` reported EPERM; three CLI tests failed while the same synthetic CLI launched by Python passed. A separately authorized retry outside that restriction passed all original 15 tests. See [maintenance evidence](../maintenance-review-2026-11-21.md).
- Cause/confidence: confirmed environment restriction for that execution; not proof that every CLI error has this cause.
- Correction/result: inspect subprocess error/status and repeat only within an authorized boundary. Preserve real failing assertions; a later attachment-redaction regression was independent and needed a code fix.
- Prevention hypothesis: report process-launch errors separately from helper exits so environment restrictions are visible before modifying code.
- Status: validated in context; proposed general prevention.
- Next check: reproduce on the intended CI runtime and retain an ordinary invalid-input control. Never bypass required project gates or broaden permissions merely to turn tests green.


## LL-002 — Review every consumer of a changed specification owner

- Date: 2026-11-22.
- Source: native-sdd-process integrated review, NATIVE-01 and NATIVE-02.
- Context: collection migration from direct root drafting to active-change authorship; published implementation a012b2b76453d6736ad474eebf8f72d8e274895d.
- Evidence: [integrated review](runs/native-sdd-process/integrated-evidence.md) and [retrospective](runs/native-sdd-process/retrospective.md). UI/discovery/generic routes and mandatory-helper wording conflicted with the new contract; corrections and focused independent re-review passed.
- Cause/confidence: incomplete propagation across callers is plausible, medium confidence; a broad source audit is not proof of every model path.
- Proposed prevention: inventory callers and output destinations before an ownership migration; inspect companion prompts/examples as well as primary entrypoints. Owner: migration implementer/reviewer.
- Status: proposed; correction validated in this context, broader prevention unmeasured.
- Next check: use the caller inventory in a later migration and retain independent review for conflicting destinations/helper requirements.
- Persistence/publication: this entry is local post-publication bookkeeping, not part of a012b2b.

## LL-003 — Check closure state separately from link validity

- Date: 2026-11-22.
- Source: native-sdd-process closure review, NATIVE-CLOSE-01.
- Evidence: [closure check](runs/native-sdd-process/closure-evidence.md). Links/preservation checks passed while archive index and preserved PRODUCT still described pending acceptance/implementation; corrected states passed separate re-review.
- Cause/confidence: stale workflow text across moved records, confirmed for this closure; not evidence that publication failed.
- Proposed prevention: compare archive disposition, approval and current execution receipts separately from path/anchor checks. Preserve historical instructions as contextual snapshots instead of rewriting immutable history. Owner: orchestrator.
- Status: proposed; local correction observed, repeated prevention effectiveness unmeasured.
- Next check: exercise a future completed/cancelled archive and inspect wording against authoritative receipts.
- Persistence/publication: local post-publication entry, pending a future authorized commit; do not republish merely to add it.

## Entry format

- ID and date:
- Source role and task:
- Project, environment and snapshot:
- Trigger and observation:
- Evidence reference and gaps:
- Cause and confidence (confirmed or hypothesis):
- Correction and observed result:
- Proposed prevention and applicability limits:
- Status: proposed / in test / validated in context / superseded / discarded
- Next verification or supersession reference:
