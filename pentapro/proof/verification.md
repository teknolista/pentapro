# PROOF — accepted migration evidence

Status: the owner accepted the reviewed migration result on 2026-11-22. Acceptance does not transform unavailable evidence into a passing check.

The [maintenance review](../../docs/native-sdd-review.md) maps maintained helpers to direct/indirect tests and optional/legacy limits. [Integrated evidence](../../docs/agents/runs/native-sdd-process/integrated-evidence.md) records the pre-closure snapshot, findings/corrections and scoped rechecks. The [execution record](../../docs/agents/runs/native-sdd-process/run.json) records later closure/publication observations separately.

The integrated migration passed 130 Python tests, 47 Node controls, isolated grader probes, package metadata/export checks, 15 case-definition checks, and collection link/version/whitespace checks. Independent review identified and rechecked baseline-authoring and mandatory-helper wording defects, then reported no blocking findings. Closure documentation receives its own structural/preservation checks and focused review.

Three agent-constructed synthetic artifact walkthroughs exercised specification-only, cancellation with partial effects, and local consolidation/archive. A separate verifier inspected their saved effects and reran two fixture tests; their provenance and limits are recorded. The first closure attempt without implementation tests remains incomplete evidence, not a passing gate. These are not all-host benchmarks, controlled model comparisons or real developer approvals.

Exact CI Node 24 execution, native inference in all six clients, optional MCP SDK smoke, consuming Android/browser/accessibility journeys and live deployed security/PR-workflow behavior were not established. Historical evidence retains its tested scope. No universal correctness, security, reliability or savings claim follows.


## Engine I1 verification

The independent [verification](../../docs/agents/runs/engine-foundation/verification-final.md) and [review](../../docs/agents/runs/engine-foundation/review-final.md) passed on fingerprint `4e1d6e2b83dcee29bdcc6f4964ba7c80b616010df423117325dd430c8ed49ebc`: 11 CLI integration tests, fmt, clippy, release build, native journey and collection controls. Two earlier path-resolution defects were corrected with observed failing and passing regression assertions. This evidence does not establish OpenSpec parity, other OS support, hostile-race safety or hosted CI.


## OpenSpec read compatibility I2 verification

The independent [verification](../../docs/agents/runs/engine-openspec-read/verification-reconciled.md) and [review](../../docs/agents/runs/engine-openspec-read/review-reconciled.md) cover the verified candidate snapshot `bcc12d2a4fefc6fa009286f9acdb1bc58d7caa45c7bdaa17413d65dd8369f3ad`: 23 Rust integration tests, 43 executable differential comparisons plus an intentional refusal, formatting, Clippy and collection checks on Linux. The [permission follow-up](../../docs/agents/runs/engine-openspec-read/eacces-followup.md) was inherited as recorded. This does not establish full parser equivalence, OpenSpec parity, all permission cases or non-Linux behavior.
