# Delegation packets

Roles are task packets for the host's actual subagent tools, not a promise of configured agent types. Prefer a fresh context and relevant skills; select only roles needed. Resolve logical role names against the actual host catalog and include that identity in the packet. Send an explicit bounded assignment and wait for its result. Do not ask a child to recursively create agents unless explicitly authorized and supported. A parent integrates and checks results. Include run ID, record path/version and input fingerprint in each packet when a durable run exists; agents return the tested/resulting fingerprint and evidence references. Only the orchestrator updates the record after reconciling those results. Independent reviews may run in parallel on a fixed snapshot; implementation writes must not overlap.

Every factory-role packet also carries its invocation ID and expected outcome. The orchestrator records dispatch requests, observed dispatch identities and returned/failed/interrupted results in the run's event history; roles return the invocation ID, evidence and observed metadata without writing that shared history. Distinguish requested model/effort from host-observed values and report unavailable timestamps/usage as unknown. Follow [invocation events](invocation-events.md), including minimal real runs for standalone roles and preservation after logging failures. Ordinary skill selection is not an agent dispatch.

## Compact packet and return

Carry the objective, exact authority, stop condition, owned paths, contract and relevant criterion/scenario locators, snapshot and checks; link canonical records instead of copying entire histories. Include only relevant prior findings, evidence and verified environment preflight (working commands, versions, caches or permissions where relevant); refresh them when their conditions change. Return changed paths or inspected scope, outcome, actual checks with coverage and gaps, resulting snapshot, next action, invocation ID and available observed runtime/usage. Label configured values separately from host-observed values; unavailable attribution, token and cost data remain unknown. A dispatch or modified file is not a completed result. State facts, hypotheses and unknowns distinctly.

When a genuine decision or missing authority blocks progress, return a concise question, evidence and consequences, viable alternatives (one is sufficient if only one exists), recommendation where supported, exact missing authority and safe independent work. Routine choices and already authorized repairs do not need another approval.

## Specification reviewer — read-only
Input: request, applicable policy, PentaPRO baseline and active-change source of truth, existing behavior and proposed acceptance checks. Inspect ambiguities, traceable criteria, data/contract changes, risk, feasibility, scope and alternative simpler solutions. Output blocking issues with evidence and concrete correction, unresolved decisions, checks and coverage. Do not invent product acceptance. Use penta-pro when available.

## Planner — read-only

The host main session is the principal exploration/orchestration agent; it drafts with penta-pro, guides clarification and dispatches the existing specialists without a prompt for each stage. It performs planning by default. The packet can be delegated if the host and scope support it.
Input: accepted contract and baseline. Return vertical slices with outcomes, ownership paths, dependencies, skill, acceptance checks, evidence and stop conditions. Identify safe parallelism; resolve shared interfaces first. Use software-delivery where available.

## Implementer — scoped writes
Input: one slice, relevant contracts, permitted paths and checks. Follow the reviewed native change, software-delivery and applicable platform skills. Return changed files, actual check outcomes, contract conflicts and resulting snapshot. Preserve unrelated edits; do not publish.

## Verifier — read-only source
Input: integrated snapshot, criteria, test plan and target. Execute safe checks, report exact commands, environment, status, tested snapshot and coverage gaps. Classify inherited failure versus introduced or unknown. Avoid commands that mutate external systems unless authorized. Skill selection follows the affected boundaries.

## Reviewer — read-only, fresh context
Input: fixed base and final snapshot, governing requirements, policy, diff, tests and evidence. Use peer-review; inspect relevant callers, integration, tests, boundaries, error paths and actual behavior. Report findings with IDs, severity, concrete trigger and evidence, or no blocking findings with coverage and limitations. Independent means a distinct review context, not proof of an independent human or different model. If unavailable, record self-review.

## Records and ship
The integrator reconciles canonical records after accepted corrections. When shipping is authorized and `factory_shipper` is available, use its configured model and effort and delegate to it; wait for its result. A direct request to invoke a role with no narrower task requests its defined workflow in the current project and session; preserve that scope and authority in the packet. For the shipper this includes git-ship review, commit and normal push, subject to applicable permissions and stop conditions. Do not restrict such a request to review by default. Otherwise report the limitation; the orchestrator may use git-ship for separately authorized shipping when the user has not required that specific agent. The shipper must use git-ship within recorded authority, check exact staged contents, publish only the permitted ref, verify remote identity and follow applicable CI. A changed snapshot after review requires appropriate recheck. Consolidate and archive through the native closure contract after explicit result acceptance; one approval covers normal commit/push by default unless the developer narrowed it. Track actual closure and publication revisions separately.

## Retrospective reviewer — read-only
Input: prompt, ledger, stage outcomes and evidence, authorized history and final revision. Follow retrospective.md. Prefer a context separate from the orchestrator; if unavailable disclose that fact. Recommendations are proposals; modifying skills is a separate authorized task.

## PDSA handoff for every packet

Include project protocol/lessons paths, relevant lesson IDs, brief contextual plan, expected checks and corrective-attempt limit. Require an outcome, actual evidence and gaps, PDSA summary and optional lesson candidates at completion or blockage. Agents return candidates without editing the shared record. The orchestrator is the sole recording owner, including after an isolated invocation, and reports saved versus pending lessons and publication status separately. Persist every lesson in English regardless of the project specification language. Read-only roles route source corrections to the implementer.
