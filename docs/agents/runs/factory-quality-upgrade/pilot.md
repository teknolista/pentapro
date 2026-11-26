# Bounded qualitative pilot

Task: the same synthetic ledger-port case, plus typo-only and shared-library negative/control requests. Two fresh host subagents were requested as factory_verifier with gpt-6.1-terra/high; baseline received HEAD 6eaf9b9 mixed UI instructions, candidate received the current terminal and journey/execution references. The host confirmed dispatch/returns. Actual selected model/effort, token totals and cost were not exposed. Both tasks were read-only; no external Codex process, app implementation or consumer rollout was used.

## Observed results

Both returns preserved downloader scope, required exact values/currency checks, selected-row visibility at 80x24/40x12, actual worker cancellation, alternatives before custom parsing, authorized repair and separate developer acceptance. Both kept typo work local and checked both shared-library consumers. Baseline proposed import→JSON first then terminal; candidate proposed input→import→interactive view→failure/cancellation as the initial slice and explicitly added redirected stdout/stderr/exit/ANSI isolation, resize and keyboard help.

Both correctly said that no product/PTY/browser/device execution or user acceptance was available. The candidate acknowledged reading inputs before the private prompt append; this instruction-compliance gap was not silently repaired retroactively. Both provide useful plans; the baseline's strong response is counter-evidence to any claim that old guidance could never work.

## Assessment and limits

Main-session qualitative assessment used scope preservation, evidence/property fit, authorized continuation, proportionality and cross-consumer coverage. This rubric was applied after returns, not a preregistered or blinded benchmark. Both satisfy the core task; candidate enumerates more terminal-specific observables. A single task/attempt per arm, unequal instruction context, unavailable runtime/usage attribution and nonblinded assessment prevent causal savings or universal quality claims. This is an exploratory comparison of returned plans, not proof of actual product equivalence, enforced TDD or six-host behavior. A later controlled task implementation with repeated runs and independent grading remains useful research, not a fabricated pass.

Task inputs: `evals/fixtures/factory-port/README.md`; invocation IDs pilot-baseline and pilot-candidate in the current events ledger. Both agents preserved product source and shared records.

## Executed scripted vertical slice

The separate [synthetic terminal fixture](../../../../evals/fixtures/terminal-journey/app.py) exercises input preparation→exact-decimal JSON report→real PTY render→malformed input rejection→restored valid input. The [independent checker](../../../../evals/check_factory_journey.py) sets actual PTY dimensions with ioctl and verifies emitted row bounds, selected Gamma row/value, labels and actual size at 80x24 and 40x12. Clean invocation exited 0. `--seed-defect` deliberately places selection outside the clipped viewport and exited 1 with the expected visibility finding. Six semantic tests exercise clean/seeded outcomes, incorrect report/status/decimal/control sequences, malformed input recovery and bounded hung-process/descendant cleanup.

The new PTY checker originally had a blocking read before its subprocess timeout; main-session inspection found it, and the implementer corrected it with a monotonic/select deadline and a process-group regression. This is actual scripted input/output and static PTY evidence. It does not establish interactive keyboard navigation, resizing during execution, terminal-emulator fidelity, visual attractiveness, human task satisfaction, full application equivalence or a causal process improvement. It closes the deliberately bounded scripted-slice criterion and complements the two qualitative role returns.
