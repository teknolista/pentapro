# Factory invocation events

Use this contract for factory-role dispatches, including isolated role assignments. It adds evidence for retrospective analysis without replacing execution state, product acceptance checks or long-lived lessons.

## Identity, ownership and scope

The invoking main session/orchestrator alone writes `docs/agents/runs/<run-id>/events.jsonl` beside the existing `run.json`. Roles receive and return their invocation ID and actual evidence; they do not write shared events. The event format is version 1, separate from unchanged run.json schema 1. The [run-record contract](run-records.md) owns root identity, checkpoints and recovery. Lessons remain in the project's existing lessons record and link to events as evidence.

Reuse the same ongoing execution across prompts, sessions, role calls and retries. A new prompt, agent, attempt or session does not create a directory. For a directly invoked standalone factory role with no applicable run, the main session creates one minimal real assignment run through the existing record procedure; this does not start a full specification/factory lifecycle. Ordinary skill use and bounded edits without a factory role remain outside this telemetry. A genuinely independent assignment can have a new run.

Do not generate historical events, terminal outcomes or runtime metadata that were not observed. If a role runs without a recording owner/capability, return an event candidate and mark capture pending. This is a declared coverage gap, not successful capture. An instruction-based record cannot prove complete host capture; compare host/tool receipts when available. Host instrumentation would require separately authorized integration; no hooks, global settings or telemetry services are installed here.

## Event lifecycle

Use lowercase hyphenated event, invocation and run IDs. Give each event a unique event_id and each actual invocation a unique invocation_id. Task attempts start at one and increment for a real retry. A resubmission of identical event_id/content is idempotent; conflicting reuse fails. A real retry of an assignment gets a fresh invocation_id and incremented task attempt, preserving the previous invocation.

| Current observation | Allowed next event |
| --- | --- |
| No invocation yet | dispatch_requested |
| dispatch_requested | dispatched, dispatch_failed, cancelled |
| dispatched | completed, failed, cancelled, interrupted |
| completed | result_accepted, result_rejected |
| dispatch_failed, failed, cancelled, interrupted, result_accepted, result_rejected | No further event for this invocation; a real retry has a new identity |

A request records the intent before the dispatch tool is called. `dispatched` requires the concrete agent identity returned by the host. Failed dispatch is distinct from an agent that ran and failed. Completion means a returned task outcome, not a passed product gate. `result_accepted` means the orchestrator accepted an agent return; it never means developer result acceptance, source consolidation authority or publication permission. An invocation with no observed terminal event remains open. After a crash inspect actual host/effect state before labeling it interrupted or retrying.

## Payload and measurements

All events carry schema_version=1, event_id, invocation_id, run_id, event_type and occurred_at as a timezone-aware ISO 8601 observed timestamp. Each dispatch_requested also carries role, task_id, positive attempt, concise reason, expected_outcome and input_snapshot (the source fingerprint). dispatched includes the observed agent_id. Terminal events include outcome. Optional evidence locators, output_snapshot, parent_invocation_id, model_requested/effort_requested and model_observed/effort_observed preserve their distinct meanings. Optional usage contains input_tokens, output_tokens and cost_usd; unknown values are null, never invented zeros. See the helper's validation errors for malformed or unsupported payloads; use only this version's documented fields.

Use English summaries and stable task/role/invocation IDs. Keep reasons short and specific: what expertise or required independence is needed, what input is handed off and what observable result is expected. Store sanitized references rather than raw prompts, full tool traces, credentials or unnecessary personal data. Redaction depends on the recording owner; the helper is not a secret detector or authenticity verifier.

Within an invocation, timestamps must not go backward. Parallel invocations may append in a different chronological order. Record actual observed model/effort and usage only when the host exposes them; configured/requested values do not prove runtime selection. Invocation elapsed time is available only with suitable observed dispatch/terminal timestamps. Sums of overlapping invocation durations are not project wall time, CPU time or proof of savings. Waiting, rework and cost comparisons require comparable tasks and evidence.

## Append and summary

The package-local [event helper](../scripts/run_events.py) requires Python 3.12+ and Git, uses the existing run identity and does not create a run implicitly. Resolve the installed package path; the target is the actual project checkout, never the plugin cache. Inspect event contents before submission.

```sh
python3 /installed/software-factory/scripts/run_events.py append --project /actual/project --run-id actual-run --input /temporary/sanitized-event.json
python3 /installed/software-factory/scripts/run_events.py summary --project /actual/project --run-id actual-run
```

Replace all placeholders. The helper validates only the selected run/history, never enumerates other runs. It serializes recording using per-run locking, rejects unsafe paths/files and malformed/truncated histories without truncation or automatic repair, and detects invalid ordering or conflicting identities. A successful local append proves only local persistence of the submitted observation. It does not prove that the described agent/check actually ran. No Git index/configuration changes, source renormalization, network access or execution of event text is performed.

Append-only events preserve prior facts. The summary is derived, not another authoritative record; it exposes counts, open/terminal status, attempts and available measurements. Read only the current run during ordinary work. Cross-run aggregation is a separate explicit audit and must be bounded to the requested scope. A large current-run ledger may eventually warrant an indexed design, but do not add compaction/sharding without observed need and a compatible migration.

## Recording failures and retention

Before managed dispatch, failed recording holds that dispatch: repair/reconcile persistence before starting the agent. After dispatch or an external effect has occurred, preserve the observed outcome and stable event identity in the current durable handoff, reconcile actual state, then retry only the recording. Never redispatch an agent, re-push, re-archive or repeat another effect to make its log appear complete. If the record itself is damaged, report the failure and preserve bytes for explicitly scoped recovery; do not truncate, overwrite, delete it or create a replacement run to bypass the conflict. A failed terminal append leaves capture pending, not an invented failure/success.

Choose the project's retention and sanitized Git versioning policy explicitly. No automatic rotation, movement, deletion or expiry is installed. Keep existing histories and lesson IDs during setup/update; finished historical records need not be backfilled. Any future archive/move must preserve incoming references. This directory remains execution metadata excluded from source fingerprints, not a place to hide executable source or acceptance criteria.

## Using the evidence

At change completion, the retrospective can inspect repeated assignments, rework, handoff waits, overlapping scope and available cost per verified result. Required independent checks retain their purpose even with no findings; fewer calls alone is not greater efficiency. Link useful observations into proposed lessons with context, cause confidence, correction, limits and a next experiment. A successful helper test or synthetic pilot does not establish a motivational effect, all-host capture completeness or a universal process improvement.

## Final receipt boundary

A completed primary shipper invocation is recorded by its orchestrator before the [single administrative closeout](delivery-closeout.md). Administrative commit/push is direct bookkeeping, not another role invocation or event that requires another tracked confirmation. Finish all requested role returns first; freeze tracked records at the administrative push and use Git refs/CI plus the conversation to confirm that final publication. Preserve unknown/failed outcomes and resume only the unfinished operation. This exception never suppresses a real new role invocation or permits fabricated success.
