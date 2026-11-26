# Bounded delivery closeout

A direct `factory_shipper` request includes the reviewed source delivery and one optional administrative commit/push by its invoking orchestrator. Explicit local-only, source-only or narrower authority prevails. This policy supplies no merge, release, deploy, force-push or history-rewrite authority. The orchestrator owns records; the shipper owns its git-ship task.

## Two stages, one invocation

1. Before source delivery, record current evidence, necessary lessons, required gates and the shipper dispatch in the selected existing run. Include the sanitized record files in the reviewed primary commit. Before that commit, the shipper returns its local check results/snapshot to the orchestrator if record gates need updating; the orchestrator saves the ready source gates and acknowledges internally, without another user approval. The shipper rechecks/stages those updated bytes before committing. Final remote/CI observations belong in operations evidence; changes to governing gates require ordinary checked reconciliation outside the light exception. The shipper reviews/publishes the source and confirms its exact remote ref and applicable CI, then returns the primary SHA, ref, checks, invocation ID and outcome. If the source is already published and unchanged, verify that state instead of creating an empty primary commit.
2. After the return, the orchestrator appends the actual terminal event and updates `run.json` with the confirmed primary commit/push and observations. Preserve the original gates/source fingerprint and history. Finish all record updates before freezing this run for closeout. Keep late lesson candidates in that return/event or conversation; a new long-lived lesson or other source change belongs to separately scoped work, not this receipt-only commit.
3. Review and stage only the changed `run.json` and/or `events.jsonl` in that same selected run. Preserve unrelated edits and index selections using git-ship's safeguards. Use the installed [receipt checker](../scripts/check_delivery_receipts.py) on the **index**, with the actual primary commit SHA: `python3 /installed/software-factory/scripts/check_delivery_receipts.py --project /actual/project --base <primary-sha> --staged --validate`. Existing regular files, valid schema, append-only events/history, unchanged governing contract/gates and source fingerprint, completed invocations, and a primary commit/push recorded as confirmed are required. Use logical `factory_shipper` in the role field (the standard hyphenated `factory-shipper` is also accepted); store custom/discovered host identity in `agent_id`. The checker inspects recorded claims; it cannot authenticate a remote observation. The orchestrator must actually query the primary ref/CI.
4. If eligible residual files exist, the orchestrator uses git-ship directly for **one** descriptive administrative commit and normal branch-only push, without dispatching another shipper, opening a new run or asking again for the same authority. The subject/body explain why a follow-up exists, identify the primary SHA and run ID, and list its record paths. Inspect the exact staged bytes and whitespace. No residual diff means no follow-up commit. Out-of-scope additions, deletions, executable bits, other records or source edits require normal review/checks; never widen the light exception or silently sweep them in.
5. Confirm the administrative remote SHA and its applicable lightweight check, then report both published SHAs and remaining unrelated work in the conversation. **Freeze tracked delivery records after this push.** The administrative commit does not record its own future SHA, push result or CI in those files. Git refs, the commit and CI are the authoritative external receipt for that final publication. This explicit boundary prevents a third commit or recursive factory invocation. Return the final PDSA in the conversation; do not create another tracked lesson/event for this administrative bookkeeping.

Example message:

```text
docs: record final delivery receipts

Record the factory outcome, confirmed remote SHA and CI observations
for primary commit <source-sha> in run <run-id>.

Contains: docs/agents/runs/<run-id>/run.json and events.jsonl.
This follow-up publishes observations obtained after the source push.
```

## Lightweight validation and consumer policy

The source collection retains its `validate` check. A deterministic Git diff classifier selects the lightweight steps only for modifications of existing non-executable `run.json`/`events.jsonl` in one run. It reads the actual staged or committed blobs, not message markers or unstaged content. Changes elsewhere, new/deleted/renamed files, mode changes, multiple runs, empty comparisons and unknown history keep the full lane. Malformed eligible receipts fail the lightweight check; they do not become an exemption. In CI use `--base <before-sha> --head HEAD --validate`; source/mixed pushes run the complete existing suite.

Required branch checks remain in force. A consumer project must deliberately integrate equivalent classification before claiming a lighter CI; obey its existing CI and branch policy otherwise. This skill does not edit consumer workflows automatically or authorize `[skip ci]`. Conditional steps keep the workflow/check present; path/message filtering can leave required checks pending ([GitHub workflow filtering](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)). The collection has local tests for classification and receipt semantics; actual hosted workflow execution is separate evidence.

## Recovery and a finite ending

If primary publication fails, preserve the local commit and report/reconcile the actual ref before retrying; the receipt-only stage does not manufacture primary success. If administrative commit/push or its check fails, preserve the frozen files and any local commit, inspect the actual destination, and retry/fix **that same unfinished closeout** within authority. Do not repeat the successful primary delivery, create an empty commit or launch another shipper just to repair bookkeeping. An existing committed closeout with an uncertain push is queried and pushed by its exact SHA, without changing its contents. A genuinely invalid administrative commit needs scoped recovery and honest reporting; no amend or force push is implied.

On cancellation, new source changes or a resource/permission blocker, retain an explicit unresolved outcome in the conversation and actual local state rather than claiming a clean delivery. Successful closeout leaves no delivery-owned tracked modifications; unrelated developer work remains intact. A human can later authorize a separate historical correction; routine success never reopens frozen records merely to record that they were frozen.
