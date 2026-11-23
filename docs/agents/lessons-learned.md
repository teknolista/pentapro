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


## LL-004 — Validate permanent instruction sections in their destination context

- Date: 2026-11-23.
- Source role/task: factory_retrospective, retrospective-1; factory-invocation-history implementation and consumer adoption.
- Context: Setup PentaPRO 2.2.0 / Software Factory 1.1.0; source publication 24f83cc1ac0cda9ea2f9b8a9ca9cc508c7e90448 and local adoption in eight projects.
- Evidence: [independent correction review](runs/factory-invocation-history/review-final.md), [adoption review](runs/factory-invocation-history/rollout-review.md), [consumer checks](runs/factory-invocation-history/consumer-update.md).
- Observation/cause/confidence: confirmed locally. An H2 extraction initially absorbed temporary template guidance; insertion into an existing instruction file could also absorb its unheaded introduction.
- Correction/result: explicit boundaries for generic setup and existing project context; source-template and destination-insertion regressions passed. All eight planned and installed manifesto sections matched the intended permanent content; reruns changed nothing.
- Proposed prevention: validate exact extracted section content after insertion into fresh and customized destinations, including an unheaded introduction, while preserving unrelated guidance.
- Limits/status: local correction validated; prevention across future templates remains proposed. No model-compliance or motivational benefit measured.
- Next verification: apply these destination-context controls to the next template insertion and compare the resulting section before delivery.
- Persistence/publication: local post-publication lesson; do not recommit/push solely to include it.


## LL-005 — Establish installation provenance before replacing package files

- Date: 2026-11-23.
- Source role/task: factory_retrospective, retrospective-1; reviewed eight-project PentaPRO adoption.
- Evidence: [adoption review](runs/factory-invocation-history/rollout-review.md), [actual consumer results](runs/factory-invocation-history/consumer-update.md) and six disposable updater controls recorded there.
- Observation/cause/confidence: confirmed design risk in the draft updater. Matching arbitrary old upstream blobs can classify an intentional local reversion as stock; no real-project loss occurred because the draft was corrected before application.
- Correction/result: use the actual installed baseline or an exact whole-package match to the identified pre-change published baseline; preserve unknown differences as conflicts. Stale-lock and intentional-reversion controls passed; all eight actual adoptions had no unresolved conflicts and matched the published source afterward.
- Proposed prevention: retain accurate installed revision/hash metadata and review a concrete preservation plan before bulk updates.
- Limits/status: fixture behavior and this adoption validated in context; future upgrades and general prevention remain unmeasured/proposed.
- Next verification: rerun both stale-lock and intentional-local-reversion controls on the next package update; verify hashes and preserved local decisions.
- Persistence/publication: local post-publication lesson; no additional publication merely to include it.

## LL-006 — Compare host role bodies as well as installed skill packages

- Date: 2026-11-23. Source: main-session eight-project documentation/tooling review.
- Evidence: [maintenance evidence](runs/workspace-git-delivery/maintenance-evidence.md). All 192 installed skill packages matched current source while several local host role profiles still required the retired workflow; 84 profiles needed reconciliation.
- Cause/confidence: confirmed propagation gap in the inspected files. Prior package equality and invocation-paragraph updates did not establish whole-role workflow consistency. This does not establish which profiles a host actually selected.
- Correction/result: compare the complete workflow body for each selected host against its packaged owner; preserve model/effort metadata and explicit custom runtime requirements. Updated known paragraphs and verified matching bodies plus a zero-operation second plan.
- Proposed prevention: inventory each configured host adapter during collection updates, classify custom differences before writes, and check both package bytes and role-body semantics.
- Status: correction validated locally; generalized prevention and runtime impact remain unmeasured. Next check: repeat during a later upgrade and inspect real host discovery separately.
