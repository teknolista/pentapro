# PRODUCT

- RC-01: direct factory_shipper shipping authority includes one optional receipt-only closeout commit/push, with source SHA, reason and file inventory in its message; no new shipper invocation or approval.
- RC-02: only existing non-executable run.json/events.jsonl in the same selected run qualify; unrelated paths, additions, deletions, mode changes and uncertain history use full CI.
- RC-03: validate actual staged/committed blobs, run schema/identity, unchanged source fingerprint and gates, confirmed primary publication, append-only history/events. Invalid receipts fail validation.
- RC-04: orchestrator serializes records, freezes them before the single follow-up commit, verifies its remote SHA and reports it externally without another tracked write. Failures preserve uncertain effects and resume the same unfinished closeout.
- RC-05: keep required validate status, full checks for source/mixed changes and lightweight local/CI checks for receipts; never skip by message alone.
