# Delegation packets

Roles are task packets for the host's actual subagent tools, not a promise of configured agent types. Prefer a fresh context and relevant skills; select only roles needed. Send an explicit bounded assignment and wait for its result. Do not ask a child to recursively create agents unless explicitly authorized and supported. A parent integrates and checks results. Independent reviews may run in parallel on a fixed snapshot; implementation writes must not overlap.

## Specification reviewer — read-only
Input: request, applicable policy, OpenSpec/PentaPRO source of truth, existing behavior and proposed acceptance checks. Inspect ambiguities, traceable criteria, data/contract changes, risk, feasibility, scope and alternative simpler solutions. Output blocking issues with evidence and concrete correction, unresolved decisions, checks and coverage. Do not invent product acceptance. Use penta-pro and applicable OpenSpec skill when available.

## Planner — read-only

The orchestrator performs planning by default. The packet can be delegated if the host and scope support it.
Input: accepted contract and baseline. Return vertical slices with outcomes, ownership paths, dependencies, skill, acceptance checks, evidence and stop conditions. Identify safe parallelism; resolve shared interfaces first. Use software-delivery where available.

## Implementer — scoped writes
Input: one slice, relevant contracts, permitted paths and checks. Follow OpenSpec apply and applicable platform skills. Return changed files, actual check outcomes, contract conflicts and resulting snapshot. Preserve unrelated edits; do not publish.

## Verifier — read-only source
Input: integrated snapshot, criteria, test plan and target. Execute safe checks, report exact commands, environment, status, tested snapshot and coverage gaps. Classify inherited failure versus introduced or unknown. Avoid commands that mutate external systems unless authorized. Skill selection follows the affected boundaries.

## Reviewer — read-only, fresh context
Input: fixed base and final snapshot, governing requirements, policy, diff, tests and evidence. Use peer-review; inspect relevant callers, integration, tests, boundaries, error paths and actual behavior. Report findings with IDs, severity, concrete trigger and evidence, or no blocking findings with coverage and limitations. Independent means a distinct review context, not proof of an independent human or different model. If unavailable, record self-review.

## Records and ship
The integrator reconciles canonical records after accepted corrections. The orchestrator handles shipping by default and uses git-ship (or the project's actual successor) within recorded authority, checks exact staged contents, publishes only the permitted ref, verifies remote identity and follows CI. A changed snapshot after review requires appropriate recheck. Archive with the OpenSpec archive skill only when authorized and ready; track its subsequent commit/push separately.

## Retrospective reviewer — read-only
Input: prompt, ledger, stage outcomes and evidence, authorized history and final revision. Follow retrospective.md. Prefer a context separate from the orchestrator; if unavailable disclose that fact. Recommendations are proposals; modifying skills is a separate authorized task.
