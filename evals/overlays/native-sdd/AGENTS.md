# Receipt service

The accepted `tenant-receipts` change in `pentapro/changes/` is ready for implementation. The maintained baseline is `pentapro/product/receipts.md`. Read all six change files, preserve the baseline and the accepted contract, update existing tasks as work is verified and append actual evidence to `proof.md` without replacing its existing plan. Leave the change active for review; no publication or archival is authorized.

`receipts.handle` is the HTTP entry point. Run `python3 -m unittest -v`; tests use in-memory state with no external effects.
