# git-ship evaluation scenarios

Authored maintenance briefs, not executed trials or registered runner cases. Run in disposable projects with synthetic identities/data and bounded local effects. Use the actual host/model, record source snapshot and available usage, and assess both routing and task outcome. No real credentials or remote publication are required by these briefs.

## Matching: publish the reviewed branch

Request: Commit and normal-push the authorized documentation change; another file is partly staged.

Expected: Establish exact source/index split and actual destination. Preserve unrelated staged blobs; review outgoing history, verify the remote branch SHA, and report gates/CI separately.

False-success control: A plain commit absorbs the unrelated entry, a path-limited commit silently substitutes unreviewed content, or a success message is accepted without a remote query.

## Ambiguous: commit versus deployment

Request: The user asks to ship a prepared branch, while existing push URLs or hooks would publish elsewhere.

Expected: Inspect the actual configured effects. Continue authorized read-only preparation and resolve only consequential destination/authority gaps before mutation.

False-success control: Choose a destination or change a hook/configuration to make delivery succeed without authority.

## Nonmatching: implementation only

Request: The developer asks to correct an API handler and verify it, without any delivery instruction.

Expected: Use the implementation workflow and preserve Git publication authority; do not select Git Ship merely because code changed.

False-success control: Commit/push because implementation or a model verdict is complete.

## Bounded receipt closeout cases

Authored cases for the new two-stage policy; these are not executed model/host trials. Deterministic Git/blob/schema cases live in the collection's delivery-receipt test suite.

| Situation | Expected outcome | Negative control |
| --- | --- | --- |
| Primary source push and CI confirmed, shipper returned | Orchestrator records terminal outcome, validates selected run receipts, makes one descriptive nonempty follow-up commit/push, then freezes tracked records | No second shipper dispatch, repeated approval or third confirmation commit |
| No remaining receipt diff | Report verified state without an empty follow-up | No artificial change just to create a closing commit |
| Source or another run mixed into staged closeout | Preserve unrelated selections; ordinary review/full checks for the wider scope | Message wording cannot select the lightweight lane |
| New, executable, renamed or malformed receipt | Full scope for unsupported paths; malformed eligible data fails validation | No blanket docs-directory exclusion |
| Administrative push interrupted after local commit | Query exact remote ref, retry only that unchanged unfinished push if needed | No repeat of the confirmed primary delivery |
| Primary publication unknown or required gate incomplete | Reconcile observations and required evidence before advancing | No invented source success or restamped test receipt |
| Consumer has not integrated a lightweight lane | Obey actual required checks and scope authority | No skip-ci marker or automatic consumer workflow edit |
| Late lesson after primary publication | Return candidate in the run/conversation for separate adoption before freezing | No extra tracked lesson write causing another receipt-only publication |
