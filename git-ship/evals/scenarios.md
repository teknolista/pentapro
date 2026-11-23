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
