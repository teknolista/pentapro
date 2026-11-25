# Factory run persistence — implementation and validation

## Decision and scope

The recurring failure is lost or stale execution context between agents/sessions, especially source changes after review and uncertain external effects. Software Factory owns one small durable record and its local validation helper; Setup PentaPRO prepares only the directory guide and selected-host pointers. Reuse existing equivalent project trackers and keep bounded single-agent edits proportionate. Requirements, lessons and execution state retain separate owners.

Current locations and format are defined in [run persistence](../skills/software-factory/references/run-records.md). The former `.factory/runs/` proposal in the design guide is reconciled to `docs/agents/runs/<run-id>/run.json`. Record summaries and all persisted lessons are English even when specifications use Portuguese. Run records are not automatic sources of authority. Installation does not execute a run or register a new daemon/hook.

## Deterministic controls and limits

The original stdlib Python helper captures the inventoried source fingerprint, refuses stale passed gates and unfinished required work before SHIP/DONE, checks project/run/branch identity, and preserves previous checkpoints with version comparison and an exclusive writer lock. Saves use an atomic replacement after file flush; this is not distributed consensus or a guarantee against power loss. Only metadata and root prompt logs are excluded from source hashing; Gitignored untracked outputs and external inputs require separate evidence.

A local passing record does not verify that a review happened, establish agent isolation, query remote publication or certify semantic correctness. Owning skills still execute acceptance and Git/operations gates. The helper does not execute commands embedded in JSON, alter Git/index/host configuration or access the network. It cannot prevent a writer that ignores the contract from fabricating evidence. Preserve those verification limits in every handoff.

## Executed local controls

The candidate passed 18 new persistence tests, the complete 72-test root Python suite, 11 initializer tests, 26 prototype tests, 15 quiz publisher tests and 47 Node tests. In total: 124 Python tests (including two optional native discovery probes available on this host) and 47 Node tests. Metadata freshness, all 24 package versions, 981 local links/anchors across 204 Markdown files, the 15 evaluation-case definitions and whitespace checks passed. The runtime was Python 3.12.6 and Node.js 27 alpha; the CI Node.js 24 run remains pending publication. All four exported bundles were checked for the new helper/reference/directory-guide bytes and containment, alongside the existing optional Antigravity strict and Codex marketplace discovery probes. These probes do not extend the prior OpenCode/Copilot native runtime claims.

Disposable Git fixtures exercise initialization and preservation on rerun; ignored outputs versus inventoried source; executable bits and deletion/commit stability; stale-source resumption with gate invalidation and recheck; outdated record writers and existing locks; failed/unavailable gates preserving saved bytes; unfinished tasks and uncertain operations preventing completion; required Git observations and revisions; immutable execution identity/history; branch changes and active Git operations; symlink/hardlink refusal; path containment; duplicate/misspelled JSON fields; and CLI check/save with no remotes or model calls.

The recovery scenario marks a push uncertain, rejects premature completion, then accepts a supplied observation reference. It sends no push and does not prove any remote effect. The actual source-change case rejects the old review/check fingerprint, persists VERIFY with old evidence retained as pending, and accepts SHIP only after the updated gate matches current source.

Authored matching, ambiguous and non-matching agent/setup scenarios are maintained in the owning skills' evals. No new live multi-agent/host/model trial, cross-model comparison or measurement of quality/cost improvement is implied by these local tests. CI execution for this uncommitted snapshot remains pending publication. Use a real project pilot with interruptions and separate acceptance checks to measure transfer before claiming efficiency gains.

Maintainer commands are listed in the [README](../README.md#validation-and-improvement). The new tests are discovered by the existing root Python suite, so no additional CI job or network step is required. Host templates retain their models, action authority and PDSA boundaries.
