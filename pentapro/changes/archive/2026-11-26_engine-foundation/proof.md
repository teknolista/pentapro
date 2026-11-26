# PROOF · Acceptance and evidence

## Before-code traceability

| Criteria | Scenarios | Responsible role | Observable check |
|---|---|---|---|
| ENG-001 | S03, S06 | implementer/verifier | real binary help/version, valid JSON, exit codes, unknown command |
| ENG-002 | S01 | implementer/verifier | empty and populated project init, repeat byte preservation |
| ENG-003 | S02, S05 | implementer/verifier | six-file creation, duplicate and concurrent creation, invalid IDs |
| ENG-004 | S03 | implementer/verifier | sorted list, archive ignored, nested root, explicit root, show content |
| ENG-005 | S04 | implementer/verifier | missing/empty artifacts and structural-only success diagnostics |
| ENG-027/028 | S05, S06 | reviewer/verifier | symlinks/collisions/no out-of-root effects, no subprocess/network source inspection |
| Collection coexistence | S06 | orchestrator/verifier | collection validator, case checker, metadata freshness, git diff --check; compare protected source hashes/index |
| ENG-006–026 | full target inventory | future increments | pinned differential fixtures, actual upstream test cases and native boundary scenarios; Pending |

I1 must demonstrate a complete temporary-project journey: init → new → list → show → validate → corrupt required file → diagnostic → repair → validate. Preserve a sentinel AGENTS.md, plugin metadata and existing Markdown bytes. Negative tests cover missing roots, invalid names, empty files, duplicate/concurrent mutation, unsafe paths and JSON error contract. Tests must call the compiled executable with isolated roots, not just mirror internal functions.

I0 recovery is source-inspected evidence, not executed OpenSpec parity. I1 does not pass the full product gate. Future differential harness normalizes only temporary paths, timestamps and explicitly justified nondeterminism; compare stdout/stderr, exit, files, Markdown preservation and prompt decisions. Every inventory row needs positive, negative, existing-data and interrupted-operation cases where applicable. Stable seed fixtures and license provenance remain in test/fixtures/ when introduced.

Performance: baseline release-build startup/list/validate on documented fixtures; report sample count, sizes, environment and percentiles before choosing budgets. No Rust-vs-TypeScript or token savings claim without controlled comparison. Cross-platform, PTY, SIGINT/process cleanup and recovery fault injection are separate gates. I1 is structural validation, not security certification or semantic readiness proof.

## Executed evidence

Specification review passed for I1 after exact scaffold/JSON clarification; see [rereview](spec-rereview.md). Native I1 implementation and correction evidence is persisted in [implementation](../../../../docs/agents/runs/engine-foundation/implementation.md) and [correction](../../../../docs/agents/runs/engine-foundation/correction.md). The first independent [review](../../../../docs/agents/runs/engine-foundation/review-first.md) and [verification](../../../../docs/agents/runs/engine-foundation/verification-first.md) reproduced intermediate symlink traversal and ordinary marker-file discovery defects. Both were corrected with genuine failing assertions before the fix and passing assertions afterward.

Implementer observed on corrected code snapshot `9c222bdeb1e1ccaaac9503613e0c79d7156361634ef68bc07cff9505b7190a37`: fmt, Clippy, 11 actual-binary integration tests, release build and fresh-root success/failure/repair journey passed. This is implementer evidence, not the final independent gate. Final verifier/reviewer returns are stored under the selected run and its invocation ledger; current gate state is owned by run.json. Initial eight tests were authored alongside implementation; only correction regressions have observed RED/GREEN evidence. Collection baseline checks passed and 269 protected source bytes were inventoried for later comparison.

All results are local Linux observations. Hosted CI, Windows/macOS, adversarial concurrent path replacement, power-loss recovery, full upstream tests/parity and measured comparative performance remain unverified. A stale verifier script call identified in correction was excluded from post-fix evidence. No source or skill/plugin release was published.
