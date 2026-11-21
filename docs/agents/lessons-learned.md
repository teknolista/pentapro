# Lessons learned

The main session/orchestrator maintains this project record. Factory agents return candidates and evidence; they do not write here. Keep proposed prevention separate from validated results. Lessons added after publication may remain local until the next authorized commit.

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
