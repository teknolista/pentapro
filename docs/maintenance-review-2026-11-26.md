# Final maintenance review — 2026-11-26

## Verdict and snapshot

The source collection is suitable for scoped developer use within its documented host/runtime limits after the corrections below. Universal readiness for every developer, model, software domain or host is not established. This review includes 26 skill entrypoints, six logical factory roles and 36 packaged host adapters; ownership, authority, setup/preservation, execution/closure/recovery, packaging, automated evidence and documentation were assessed. Supporting references and assertions were traced by risk; this is not line-by-line semantic certification of every historical document or compilation of every example.

Base: `7be471763b322bec91399e8929c36c47fccd69d0`, plus the pending ChuteGo lesson follow-ups. Final maintenance source bundle: 3.1.2. The main session integrated corrections; two distinct-context, read-only reviewers assessed harness behavior and collection contracts using Peer Review. They did not supply independent human certification or new product acceptance. No source commit, push, consumer rollout or global installation was performed by this review.

## Findings and corrections

| ID | Finding and correction | Evidence / disposition |
| --- | --- | --- |
| HR-01, P2 | The section planner accepted canonical mandatory sections hidden inside Markdown examples as already installed. It now rejects exact mandatory headings in backtick/tilde fences or HTML comments, checks canonical text at the live heading, and preserves destination bytes. | Three meaningful assertion failures before the fix; all seven planner tests passed afterward, including valid active-section/idempotence and unrelated-example controls. Independent re-review confirmed four-backtick/short-closing-fence/unclosed-comment controls. Resolved within documented scope. |
| D1, P2 | README told contributors to put new skills at repository root, although discovery uses `skills/`. | New-skill procedure now names `skills/<name>/`; manifest/validator owners agree. Resolved. |
| D2, P2 | Current navigation still described previously shipped quality/closeout work as unpublished. | Added dated publication dispositions and this review's navigation while retaining original evaluated counts, acceptance distinctions and immutable completed ledgers. Resolved. |
| D3, P3 | Execution reference requested separate publication authority for every tracked postpublication retrospective, overlooking the bounded run-receipt exception. | Selected existing run.json/events.jsonl observations now link to bounded closeout; new reports/lessons/source changes retain ordinary scope/checks and authority. Resolved. |
| Local integration | Six ignored project Codex workflow bodies lacked inspected canonical additions; metadata matched. | Refreshed only developer_instructions, preserving metadata and project scope. Checker subsequently reported six Codex and six tracked Copilot profiles current. Local ignored configuration is not distributable source or proof an already-running agent reloaded its profile. |

The planner is intentionally conservative, not a complete Markdown parser. A literal HTML comment opener in inline code can cause a safe review-required refusal. This is documented; no automatic write or deletion follows a refusal. Full Markdown interpretation would require its own evaluated change.

## Coverage and script assessment

Every one of the 48 tracked Python/JavaScript/TypeScript/shell source and test artifacts is accounted for in the [script inventory](factory-script-inventory.md). Production helpers have behavioral or integration tests; tests themselves need meaningful assertions, not recursive tests of tests. Synthetic fixtures deliberately include wrong behavior and are judged by independent controls. Review covered subprocess cancellation/timeouts, Git blob/index scope, append-only histories, safe target handling, export preservation and prompt privacy, not just filename matches.

Two exceptions are appropriate only with explicit limits:

- The optional MCP smoke harness has diagnostic tests, but actual protocol execution requires the optional SDK dependencies. A new direct attempt returned exit 2 because `httpx2` was absent and correctly reported that no protocol checks ran. Protocol integration remains unverified.
- The legacy optional OpenCode prompt hook has no executed host/type integration. Retaining a clearly labeled optional example is acceptable; treating it as reliable automatic prompt capture would not be. It is not installed automatically. Offline tests cover the separate current OpenCode catalog adapter.

No superficial test was added for prose/version edits. HR-01 warranted a real negative regression and valid controls because the script otherwise gave a false installed-state result. The script inventory now identifies that coverage.

## Executed verification

The complete documented offline command set was executed successfully: package metadata freshness, collection links/versions, 20 evaluation definitions, the real bounded synthetic PTY journey, Python suites and Node suites, and whitespace. Initial full run: 157 root + 14 PentaPRO + 26 web helper + 15 quiz Python tests, plus 27 quiz + 16 logging + 4 adapter Node tests (259 total). After HR-01, the changed root suite passed all 159 tests (46.488 seconds), giving 261 passing tests across the final affected-root result and the unchanged package/Node results. Unchanged package/Node evidence retains its original execution and is not relabeled as a new run. Final structural check: 336 Markdown files, 1,378 local links/anchors, 26 versions, zero issues; all 20 evaluation definitions valid. Logs and command/status receipts are in `/tmp/pentapro-final-review-20261126/`; temporary logs are local evidence, not durable content promised to future clones.

Independent harness execution additionally passed 96 focused tests before the defect correction and seven planner tests afterward. Those original green tests did not detect the missing context control. The documentation reviewer confirmed the 26 package names, MIT notices and manifest paths and assessed current generic/Android/UI ownership; supporting-reference semantics were sampled. The new numeric/Git SHA scenarios remain authored briefs, not executed model trials.

Environment: Python 3.12.6 and Node 27 alpha; CI targets Python 3.12 and Node 24. The earlier primary/administrative hosted deliveries passed, but the present local corrections have no new hosted CI observation. Metadata/exports are checked locally through their actual helpers and tests. Source/adapters for six hosts do not establish live six-host role execution, Android device/browser accessibility, Windows cleanup or causal efficiency/quality improvements.

## Documentation, provenance and remaining boundaries

README catalog, generated plugin/package manifests, workflow instructions, current review navigation and maintained documentation were reconciled. Historical reports retain their original source/versions and explicitly link current dispositions instead of rewriting old passing fingerprints. The prior ChuteGo-specific corrections remain documented in the [adoption review](chutego-lessons-adoption-2026-11-26.md). The five pillars, native lifecycle, developer acceptance and Git operation authority stay distinct.

One review subagent initially logged a summarized assignment, then appended the complete text as a correction. Historical fidelity was not retroactively repaired, and perfect prompt-capture compliance is not claimed. Instructional logging and configured models are distinct from host-enforced capture and observed runtime metadata.

Concurrent user edits appeared in `docs/pentapro-engine-especificacao-inicial-rust.md`, `docs/pentapro-future-plan.md`, `THIRD-PARTY-NOTICES.md`, earlier run-summary Markdown files and the factory-quality change during review. Another concurrent edit also changed the historical scope sentence in `docs/factory-quality-maintenance.md`, overlapping our dated navigation insertion; that unowned change was preserved rather than silently restored. They were preserved, not overwritten or accepted as implementation by this maintenance; final structural checks include their on-disk links. They do not invalidate unchanged executable test inputs, but later edits require fresh affected-scope reconciliation. Existing ignored prompt logs remain private and outside Git.
