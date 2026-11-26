# Durable execution records

Use one record for each factory run or substantial dependent multi-agent change, including a standalone shipping operation when recovery evidence warrants it. Ordinary bounded single-agent edits can use the existing task/handoff. Reuse an approved equivalent tracker/ledger with the same identity, ownership and revision checks; do not create competing records. A project policy that prohibits persistence leaves resumability unavailable: report the gap and keep dependent recovery pending rather than presenting conversation memory as durable state.

## Ownership and placement

Default: `docs/agents/runs/<run-id>/run.json`. Setup creates only a README describing this location, not a fictional active run. The software-factory package owns the [helper](../scripts/run_state.py) and this format; the optional setup-pentapro companion owns the directory guide installed at project initialization. A standalone software-factory installation needs only its packaged helper and this reference. Resolve the installed helper path through the host registry. Run commands against the actual target Git root, never the skill/plugin cache.

The orchestrator alone writes the record. Agents receive run ID, path, record version, input fingerprint, contract references, scope and expected checks. They return evidence and resulting snapshot; they do not update shared state. Record documents and fields are in English; specifications may use the project's chosen language. Persist summaries and references, not raw prompts, credentials or full tool traces. The record indexes PentaPRO baseline/change artifacts, issues and checks; their owning records retain their authority. Never store permission-bearing secrets or treat an authorization reference as a new grant.

The existing helper is optional bookkeeping for record integrity. The native SDD lifecycle can be executed by agents with ordinary file tools and a reviewed equivalent record; it does not depend on an SDD CLI or schema engine. Its check cannot validate the truth of referenced evidence.

## Invocation events and run reuse

Keep one execution identity for the same ongoing assignment across prompts, sessions, role calls and retries. A fresh independent assignment can start a new run; a new prompt alone cannot. Each explicitly invoked factory role, including a standalone role, uses that identity or a minimal real assignment run maintained by its invoking main session. This does not impose a full factory lifecycle on ordinary skill calls or bounded edits.

Keep append-only `events.jsonl` alongside `run.json` under the same existing run directory. [Invocation events](invocation-events.md) owns that separate versioned format, recording/recovery procedure and summary helper. The state/checkpoint format below remains version 1; never add event fields to its strict envelope or rewrite completed historical records. Events describe dispatches and observed outcomes; `run.json` still owns execution state, and lessons retain long-lived learning. Both helpers are optional conveniences; an approved equivalent must preserve the same guarantees and disclose missing automatic checks.

## Start, checkpoint and resume

1. Initialize before the first delegation. Use a unique lowercase hyphenated ID. Confirm scope, required gates, owners, pending tasks and separately authorized operations. Add a gate for each required check/review; an empty initial record cannot enter SHIP or DONE.
2. Save before dispatch, after validating a returned result, before an external effect and after observing its outcome. Persist only at these boundaries or when blocked; do not record every interaction. Serialize overlapping integrations. Use a separate candidate JSON and compare-and-save version to detect outdated writers.
3. On any source change, capture the new snapshot. Recheck affected gates; conservatively reset previously passed gates to pending if their fingerprint differs. Retain old evidence and its old fingerprint on pending gates or link historical evidence separately. The helper rejects a passed gate associated with a different fingerprint.
4. Before resuming, reread the latest record and inspect actual source, branch, checks and operation effects. `check` compares local identity; it does not query remotes, read evidence targets or certify reviews. Unknown push/archive/deploy outcomes remain `uncertain` until inspected under actual authority. A successful effect followed by a failed record write must be reconciled before any retry.
5. Before SHIP or DONE, inspect the current record/identity and required owning-skill gates; when using the optional helper, also run `check`; required checks must pass against the current fingerprint. DONE also requires completed tasks and confirmed requested operations. A confirmed push needs the exact expected revision and a reference to a remote query showing that revision. Compare remote identity in git-ship; this local helper cannot verify it. Record completion and publication separately.

Example (replace installed paths and placeholders; never execute placeholders):

```sh
python3 /installed/software-factory/scripts/run_state.py init --project /project --run-id checkout-fix --objective "Repair checkout retries" --contract "issues/42"
python3 /installed/software-factory/scripts/run_state.py snapshot --project /project
# Copy the saved record to a separate candidate; edit facts and references there.
# Keep record_version and history unchanged: save advances both.
python3 /installed/software-factory/scripts/run_state.py save --project /project --run-id checkout-fix --input /temporary/candidate.json --expect-version 1
python3 /installed/software-factory/scripts/run_state.py check --project /project --run-id checkout-fix
```

Exit 0 means local validation succeeded; exit 1 reports an error without replacing the previous record on rejected saves. Python 3.12+ and Git are prerequisites. Without them, preserve the record through an equivalent reviewed mechanism and report the missing automatic checks. The helper executes only fixed read-only Git queries; it never executes record strings, installs hooks or changes Git/host configuration.

## Completed records and later maintenance

A completed run remains evidence for its recorded source and publication, not a claim about every later worktree. After a new maintenance edit, `check` may correctly report snapshot drift against that completed run. Do not reopen it, rewrite its passing fingerprints or repeat its confirmed effects merely to obtain a green check. Inspect its recorded structure/history without asserting current-source equivalence, and use a new run or proportionate task record for new work. A genuinely resumed unfinished operation still follows the actual-state reconciliation above.

## Format version 1

`init` emits the complete envelope and initial history. `save` preserves schema, run/repository/orchestrator identity and earlier history, increments `record_version` and appends a checkpoint (state, fingerprint and owner). Field sets are strict so misspellings fail. History is a checkpoint index, not a full audit log or a replay of every former task/gate value. Keep historical detail in the referenced evidence.

| Field | Contents |
| --- | --- |
| `schema_version`, `run_id`, `record_version` | Format 1, unique execution ID, monotonically increasing record version. |
| `objective`, `contracts`, `repository`, `orchestrator` | English objective, canonical references, Git root/branch/base commit, sole writer identity. A clone/move or branch switch needs explicit identity reconciliation; do not silently repoint a run. |
| `state` | Existing execution states, from INTAKE through DONE/BLOCKED; phase order follows project requirements. The helper validates gates at SHIP/DONE, not every workflow-specific transition. |
| `snapshot` | `fingerprint` of inventoried source and `head` observed at capture. Re-capture HEAD after commit; unchanged source retains its fingerprint and matching check evidence. |
| `gates` | `id`, `kind` (`check`, `review`, `spec-review`), boolean `required`, `status` (`pending`, `passed`, `failed`, `unavailable`, `not-applicable`), `snapshot`, `evidence`, `reason`. Snapshot/evidence/reason can initially be null. Passing requires a matching fingerprint and nonempty evidence reference. Only optional gates can be not applicable, with a reason. |
| `tasks` | `id`, `owner`, `status` (`pending`, `running`, `done`, `blocked`), `evidence` (null until available). Completed tasks require evidence. Link canonical task lists instead of reproducing them wholesale. |
| `operations` | `id`, `kind` (`commit`, `push`, `pr`, `merge`, `archive`, `release`, `deploy`), `authorization` reference, `status` (`planned`, `uncertain`, `confirmed`, `failed`), `expected_revision`, `observation`. Last two can initially be null; Git confirmation requires a revision and all confirmations need observation evidence. |
| `blockers`, `next_action`, `history` | Concrete blockers, next authorized action (or completion handoff), helper-maintained checkpoint history. |

Example gate and operation values:

```json
{
  "gate": {
    "id": "independent-review", "kind": "review", "required": true,
    "status": "pending", "snapshot": null, "evidence": null, "reason": null
  },
  "operation": {
    "id": "publish-main", "kind": "push", "authorization": "issue 42 delivery approval",
    "status": "planned", "expected_revision": null, "observation": null
  }
}
```

Changing requirements, gate applicability or authority needs an owning decision and review; editing JSON alone cannot waive a gate. The helper cannot prove that a referenced check ran, detect a fabricated review, infer missing requirements or enforce agent honesty. It validates structure, identity and specified conditions. Prefer an existing deterministic CI check for actual product acceptance.

## Source identity and safe persistence

The SHA-256 fingerprint covers Git-inventoried tracked and unignored untracked files, their relative paths, executable bit and bytes (or symlink target without following it). Deleted files are absent so committing a deletion preserves identity. Gitignored untracked outputs, submodule contents, external services, environment variables and model context are outside it; capture those identities in evidence or stop if required inputs cannot be established. Unsupported inventory entries fail explicitly. A whole-project fingerprint is deliberately conservative and may invalidate checks after unrelated documentation changes. An affected-scope analysis can inform which checks need rerunning, but cannot re-stamp an old passing gate: the current helper still requires a current fingerprint and fresh qualifying gate evidence. Preserve the original receipt and provenance; optimize the guard only through a separately evaluated helper change.

Only `docs/agents/runs/` and root `AGENTS.log`/`AGENTS.log.*` are excluded from the fingerprint. Keep executable source or acceptance criteria out of that record directory. Record integrity changes do not demonstrate source changes. An `AGENTS.log` tracked/staged privacy conflict still blocks the project under its prompt policy; hashing exclusion is not permission to publish it.

Initialization refuses an existing run. Save acquires an exclusive per-run `.run.lock`, checks the expected version, validates and replaces JSON atomically after flushing the file. Failed validations preserve the saved bytes and release the lock. A crash can leave a lock or temporary file; inspect ownership and actual process/effect state before separately authorized recovery. Do not automatically delete a lock or start a replacement run to bypass a conflict. Atomic replacement protects readers from partial JSON; it is not distributed locking, power-loss durability or a security boundary against another writer ignoring this protocol. Symlinked paths and hard-linked/non-regular record files are refused.

Choose the project's versioning policy for sanitized summaries; no helper stages or publishes records. Keep sensitive/transient evidence local. A checkpoint written after commit/push may remain local for the next authorized commit. Do not chase a self-referential commit hash with repeated commits: the record describes observed product snapshots and remote refs, and record files are excluded from the source fingerprint. A new session first reconciles those observations. Lessons remain in their separate long-lived record and can link back to the run.

## Optional command receipts

For a trusted, explicitly authorized argv command on POSIX, the package-local [command evidence helper](../scripts/command_evidence.py) records the actual input Git snapshot, UTC start time, elapsed duration, exit code and timeout. Use `python3 /installed/software-factory/scripts/command_evidence.py --repo /actual/git/root --receipt /existing/parent/new-receipt.json --timeout 60 -- command arg...`. It does not accept a shell program from a record, does not store stdout/stderr/environment or raw arguments, and does not overwrite an existing receipt. Nonzero status propagates; timeouts kill the process group. SIGINT/SIGTERM cancel the owned group, reap the command, record interruption where possible and preserve the wrapper signal status. SIGKILL, host failure and descendants that deliberately create new sessions escape this best-effort process-group cleanup; inspect effects before retrying. Signals arriving during atomic publication may leave an already-completed receipt without an interruption field; the caller signal still matters. Inspect command effects before use.

The argv hash and argument count identify the invocation without exposing raw arguments; hashes are guessable and are not anonymization. Keep a reviewed sanitized command description and receipt locator in PROOF when needed. An intentionally invoked shell can still run arbitrary code: trusted argv and user authority remain required. Receipts prove only the observed subprocess outcome, not acceptance truth, environment completeness, live service state or absence of side effects. Fingerprints exclude ignored/external inputs; record material dependencies separately. Windows cleanup is unvalidated. Evidence reuse keeps the original receipt and snapshot plus delta justification; the helper never updates gates.
