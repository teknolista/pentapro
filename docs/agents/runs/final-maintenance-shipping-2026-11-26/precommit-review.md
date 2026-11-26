# Pre-commit shipping review

Run: `final-maintenance-shipping-2026-11-26`
Invocation: `final-maintenance-factory-shipper`
Repository: `/home/dever/workspace/teknolista/pentapro` (`origin/main`)
Base: `7be471763b322bec91399e8929c36c47fccd69d0`
Reviewed source fingerprint: `5dd490db6ff0736522763940ad7daeedf5b27ab24ba422fa01392714a3c34765`

The selected run already existed and contained exactly one `dispatch_requested` event, so no run or dispatch record was duplicated. The target path provided in the task (`/home/dever/workspace/teknolista/skills`) does not exist; this checkout and the run record both identify the repository root as `/home/dever/workspace/teknolista/pentapro`.

Reviewed all pending intended tracked and untracked files, including the ChuteGo lesson adoption follow-up, the final maintenance report, behavior-testing numeric-boundary guidance and authored briefs, the setup section planner correction and regression tests, Git Ship full-SHA guidance, generated manifests, README/notices/navigation, and the specified concurrent receipt/document updates. Confirmed the index was empty and the branch had no local commits ahead of its upstream at review. Excluded private `AGENTS.log` and ignored `.codex/` and `.opencode/` profiles; no other ignored/local data was selected. The review found no blocker. The scope includes concurrent edits in historical records as explicitly directed; their exact contents are preserved.

Fresh checks passed: plugin metadata generation check; collection validation (336 Markdown files, 1,378 local links/anchors, 26 package versions, zero issues); 20 evaluation definitions; bounded factory journey; whitespace check; 159 root Python tests; 14 PentaPRO tests; 26 UI helper tests; 15 quiz Python tests; 27 quiz Node workflow tests; 16 prompt-log Node tests; and four OpenCode adapter tests. The prompt-log test first failed when subprocess launches were restricted by the sandbox; the same suite passed completely when rerun with subprocess execution permission. The source receipt classifier correctly selected the full check lane. This is a shipper self-review, not a new independent review. Hosted CI and remote publication remain pending.

Requested model/effort: `gpt-6-luna` / `high`; host-observed runtime metadata is unavailable.
