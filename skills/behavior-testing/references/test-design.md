# Choose tests that distinguish wrong behavior

Read when numeric values cross parsing, calculation or presentation boundaries, the existing suite substitutes a material boundary, many inputs share the same rule, or a test sometimes fails.

- Start with the externally observable result and a plausible incorrect implementation. A calculation can use unit-level equivalence classes and values on either side of a threshold. A permission policy with several roles and resource states can use a decision table. An operation with a lifecycle can use valid and invalid transitions, with assertions on what remains unchanged after denial.
- Use a fake or stub for deterministic timing and fault injection. Exercise the real boundary when transaction isolation, serialization, middleware, scheduling, or provider behavior determines the result. Consumer-driven contract checks can exercise consumer assumptions against a provider. They leave environment-specific delivery and authorization to integration checks at those boundaries.
- Use generated inputs when a stable invariant covers many cases, such as a parser round trip or conservation across a state transition. Record seeds for failures, retain a minimized counterexample, and cover known edge cases explicitly. For a test-sensitivity check, exercise one plausible reversible fault in a disposable snapshot and inspect the intended assertion. Use the project's mutation tooling when broader systematic sampling is useful.

For example, an export endpoint may return `403` while still enqueuing a job. Use the real handler and queue boundary or an isolated adapter with observable effects. Check an allowed export and its job, then deny a different tenant and assert unchanged job state. An assertion on the response alone can pass with the defect present.

## Follow numeric values across boundaries

When a changed contract involves money, measurements or bounded numeric values, trace representative inputs through parsing/conversion, calculation, rounding and public formatting. Establish the expected unit, precision, accepted range, rounding rule and unavailable/overflow behavior from the owning contract; report consequential gaps instead of deriving expected values from the implementation. Exercise the real adapter and output boundary where pure arithmetic tests could hide rejection or misrepresentation.

For example, if the contract accepts decimal currency `0.29` and `0.57`, verify exact conversion to 29 and 57 minor units and the agreed displayed result. Include an accepted maximum, a value outside the accepted range, and a rounding tie when the operation can produce fractions. A plausible fault might reject `0.29` through floating-point equality or turn an accepted large positive average negative through narrowing. The regression must reject that fault and retain valid input/output controls. Use independent expected values; choose cases and boundaries relevant to the actual contract rather than requiring a monetary suite for every project. If the fix already exists, label new coverage as regression evidence, not a retroactive red phase.

## Investigate an intermittent result

Preserve the first failure, revision, environment, attempt count, and relevant traces. Reproduce with the test alone and with its neighbors when order or shared state could matter. Control the clock, inputs, seed, and external events. Wait for the actual state under test and inspect scheduled work, connection lifetime, cleanup, and fixture ownership. A retry may collect evidence. Record the original failure and any attempt that passes. If a required test remains unreliable, report the effect on its gate. Follow project policy for temporary quarantine, with an owner, follow-up, and a statement of the coverage it removes.
