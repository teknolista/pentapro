# Post-run retrospective

Run after the requested implementation, review, publication and archival stages finish. If any requested stage remains incomplete, label the assessment provisional, identify the missing evidence and record the follow-up retrospective as the next action after completion. Inspect the reconciled durable run record (including version, snapshots, incomplete operations and checkpoint history), original request and later changes, review findings, check output, revision/remote evidence, archived change and actual session records when available. Do not assume all conversations or cost data exist.

Produce a concise report:

1. Scope, sources and gaps; identify reviewed and published revisions, archive revision and reviewer independence.
2. Timeline of stages, handoffs, failure/retry and meaningful user interventions, with available timestamps.
3. Outcomes against each acceptance criterion, checks and runtime targets; distinguish facts, inference and unknowns.
4. Escaped defects, repeated failures, authorization mistakes, unnecessary waiting, conflicting instructions, skill use and whether each had observable effects.
5. Quantitative measures only when actually observable: stage duration, rework count, review loops, CI failures, interventions, and available token/cost usage. Mark unavailable values unknown; compare only with a sufficiently similar baseline.
6. Prioritized improvement proposals: evidence, root-cause hypothesis, expected benefit and risk, owner, verification experiment and success/failure criteria. Do not automatically rewrite skills or assume causation from a single run.
7. Pending work and decision: keep, modify or retire each proposed process control; identify what can be automated and its authority boundary.

Keep report in a project-approved durable location when requested or required. Separate retrospective state from archived change content unless the project explicitly requires it. Avoid storing sensitive prompts and tool outputs; use minimal references and redact secrets.

Collect PDSA summaries and lesson candidates from every role, including failed stages. Review relevant existing lesson IDs, repeated failures, contradictory evidence and whether proposed prevention was actually tested. Return consolidated candidates and status recommendations to the orchestrator; the retrospective role remains read-only and does not persist them. The orchestrator records useful findings in the existing project lessons record in English, regardless of the project specification language, preserving hypotheses, context and next checks. A late entry may remain local until the next authorized commit; report it without reopening publication.
