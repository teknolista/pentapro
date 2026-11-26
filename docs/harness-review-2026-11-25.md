# PentaPRO harness maintenance review — 2026-11-25

## Verdict and scope

The local maintenance candidate passes the executed collection and helper gates. No additional blocking implementation defect was demonstrated in the inspected paths. It is **not certified as 100% ready for every developer, host, model, operating system or product**. Universal readiness cannot be inferred from these checks. Publication, the Codex desktop project binding, optional legacy hook integration and several platform/model trials remain separate concerns.

This is a main-session self-review, not an independent factory-role approval. No subagents or external AI orchestrator were started. The request is a harness review, not implementation of the 103 deferred improvement proposals. The existing improvement plan remains pending, including the proposed three-way UI skill split.

Reviewed checkout: `/home/dever/workspace/teknolista/pentapro`, HEAD `b6a9a96137a7ee996d16bf6eefe7a22648c82703`, with uncommitted maintenance changes and relevant untracked files. Checks exercised the working tree, not a new published revision or a hypothetical staged commit. The repository/folder rename and relocation of 24 canonical packages under `skills/` are included.

## Coverage and evidence boundaries

Inventoried all 24 skill entrypoints and their routing/metadata, six roles across six packaged host adapters, maintained executable helpers and fixtures, distribution manifests, CI commands, the evaluation registry and documentation navigation. Inspected factory lifecycle, delegation, result acceptance, run/event persistence, setup/profile preservation and the changed path/distribution consumers. Read relevant review/testing contracts and compared relocated packages against HEAD: 225 files were byte-identical and 14 differed, primarily repository URLs and directory-link normalization. This comparison supports preservation; it is not a fresh semantic audit of every sentence in every unchanged reference.

All collection Markdown links and anchors were checked automatically. Historical reports, PDFs, archived executions and previous model trials were inventoried/referenced as dated evidence, not exhaustively reread, re-rendered, externally link-checked or rerun. Instruction packages were not all exercised in newly generated application projects. The review focuses on current contracts, risk-bearing source and maintenance deltas; it does not claim exhaustive line-by-line analysis of every artifact or branch coverage.

## Executed checks

Environment observed: Python 3.12.6; Node `v27.0.0-alpha.0.0.0`. CI specifies Node 24, so this local Node execution is not a rerun on the exact CI family.

| Check | Current execution result |
| --- | --- |
| `python3 scripts/validate_collection.py` | 292 Markdown files, 1,132 local links/anchors, 24 version checks, zero issues before this report/navigation update; final documentation validation is reported at handoff. |
| `python3 scripts/run_skill_evals.py --check-cases` | 15 registered case definitions validated; no new model trial implied. |
| `python3 scripts/package_plugin.py --check` | Generated metadata matches its source owner. |
| `python3 -m unittest discover -s scripts/tests` | 111 tests passed, no skips reported. Includes preservation/failure controls, evaluator isolation controls and four-host exports. |
| `python3 -m unittest discover -s skills/penta-pro/scripts/tests` | 14 passed. |
| `python3 -m unittest discover -s skills/ui-design/scripts/tests` | 26 passed. |
| `python3 -m unittest discover -s skills/pr-quiz/scripts/tests` | 15 passed. |
| `node skills/pr-quiz/scripts/tests/workflow.cjs` | 27 passed. |
| `node --test scripts/tests/test_agents_log.mjs scripts/tests/test_opencode_plugin.mjs` | 20 passed in the authorized execution outside the known subprocess restriction. |
| `git diff --check` | Passed. Does not cover untracked files by itself. |
| `python3 skills/setup-pentapro/scripts/check_agent_profiles.py --project .` | 24 detected installed profiles: 22 current, two review-required custom shipper workflows; see below. |
| `python3 evals/check_mcp_sdk.py` | Exit 2: missing optional `httpx2`; no protocol checks ran. No global dependency installation performed. |

Totals: 166 Python tests and 47 Node tests passed. Test counts are not statement/branch coverage or evidence of universal model compliance. The packaging suite's read-only native Codex catalog and Antigravity strict-discovery probes ran without reported skips; these prove their limited local discovery assertions, not all-host installation and task execution. No new model-generation session, GitHub-hosted CI run, Android build/device run, cloud deployment or live PR publication was performed in this review.

## Script and test inventory

A script does not need its own similarly named test file if a meaningful integration test exercises its actual contract. Conversely, finding its name in a test is insufficient. The following map distinguishes executable tests, fixtures and unverified adapters. No percentage coverage was measured.

| Maintained executable | Protection inspected | Assessment |
| --- | --- | --- |
| `scripts/validate_collection.py` | `scripts/tests/test_validate_collection.py`; real candidate validation | Appropriate metadata, bad-link, portability and malformed-input controls; not a full Markdown parser or external-link checker. |
| `scripts/package_plugin.py` | `scripts/tests/test_package_plugin.py` | Four exports, resources/licenses, existing destinations, symlinks, ignored required files, stale metadata and reproducibility; appropriate for the relocation. |
| `scripts/run_skill_evals.py` | `scripts/tests/test_run_skill_evals.py` | Candidate copying, legacy/nested inventory, timeout/descendant effects, result grading and isolation; model trial execution remains distinct. |
| `scripts/eval_outcomes.py` | Runner tests and `scripts/tests/test_receipt_oracle.py` | Clean/defective/forged outputs and denied side effects; no need to add a duplicate file solely for naming symmetry. |
| `scripts/eval_isolation.py` | Runner containment probes and grading tests | Actual supported local isolation paths exercised; do not generalize containment to arbitrary hosts. |
| `skills/penta-pro/scripts/init_pentapro.py` | Package `scripts/tests/test_init_pentapro.py` | Initialization, preservation and invalid-root checks; appropriate. |
| `skills/software-factory/scripts/run_state.py` | `scripts/tests/test_factory_runs.py` | Versioned save, identity, snapshot drift, preservation and unsafe inputs; structure cannot prove evidence truth. |
| `skills/software-factory/scripts/run_events.py` | `scripts/tests/test_factory_events.py` | Invocation event lifecycle, invalid/unknown returns and persistence controls; actual host metadata still needs observation. |
| `skills/setup-pentapro/scripts/merge_git_templates.py` | `scripts/tests/test_setup_pentapro_git_templates.py` | Existing bytes/order, repeat merge and safe target checks; appropriate. |
| `skills/setup-pentapro/scripts/check_agent_profiles.py` | `scripts/tests/test_agent_profiles.py` | Six hosts, custom metadata, drift and unsafe profile inputs; does not prove runtime discovery. |
| `skills/setup-pentapro/assets/prompt-logging/core.mjs` | `scripts/tests/test_agents_log.mjs` | Extraction, redaction, append, owner-only file creation and unsafe log targets; best-effort redaction remains a limit. |
| `skills/setup-pentapro/assets/prompt-logging/log-prompt.mjs` | CLI cases in the same Node suite | Real CLI inputs, append/redaction and invalid JSON; appropriate. |
| `skills/setup-pentapro/assets/prompt-logging/opencode.ts` | No executed host/type/hook integration test | **Coverage gap.** Acceptable only as a clearly optional legacy adapter with unverified host integration. Do not advertise automatic reliable capture or install it by default. A string-presence test would not resolve this gap. |
| `plugin/opencode.mjs` | `scripts/tests/test_opencode_plugin.mjs` plus export tests | 24 real resources, preservation of customized skills, disposal, older-API error, duplicate/escaping paths; live V2 host integration still separate. |
| `skills/ui-design/scripts/prototype_tools.py` | Package `scripts/tests/test_prototype_tools.py` | 26 tests for supported local prototype contract; does not establish native Android behavior or complete accessibility. |
| `skills/pr-quiz/scripts/publish_quiz.py` | Package `scripts/tests/test_publish_quiz.py` | 15 tests with API doubles; live GitHub behavior not exercised here. |
| `skills/pr-quiz/scripts/tests/workflow.cjs` | Self-contained 27-case workflow suite | Test runner, not an untested production helper; permission, stale-event/head and quiz-binding negative controls matter. |
| `evals/check_receipts.py` | Pure oracle and runner tests | Seeded tenant/replay/conflict/effect controls; independent oracle remains distinct from generated tests. |
| `evals/check_mcp_sdk.py` | `scripts/tests/test_optional_mcp_smoke.py` plus its own real-SDK assertions | Missing/incompatible-import diagnostics tested. Real protocol smoke unavailable now; historical execution is inherited evidence only. |
| `evals/fixtures/receipts/receipts.py` and `evals/overlays/review-clean/receipts.py` | Fixture tests, runner and oracle controls | Intentionally defective/clean synthetic controls; do not fix a seeded defect as if it were production code. |
| `evals/fixtures/receipts/test_receipts.py` | Executed fixture/control tests | Test artifact, not a missing production-script test. |
| `evals/fixtures/test-effect/service.py` | Runner's authored-regression sensitivity controls | Seeded side-effect defect; retain the requirement that generated regression detects it. |

Tests themselves are excluded from recursive “every script needs another test” reasoning. Generated JSON metadata is validated against its generator, not treated as executable scripts.

## Skills, roles and process assessment

The current routing keeps specification, implementation coordination, test authoring, independent technical assessment, security, UI, research, operations and Git delivery under distinct owners. Package-local links/resources and the 24-package catalog pass structural validation after relocation. The optional native Android routes have narrower implementation/testing scopes than the general assessment skills. This is sound ownership design; its effectiveness for every supported task has not been established by the 15 registered cases. The existing [coverage inventory](evaluation-coverage.md) explicitly exposes routes without registered cases or local briefs. Their absence is a risk to prioritize, not evidence that every such instruction is broken.

The six roles have 36 packaged host adapters. Role tests check complete role coverage, allowed metadata, shipper guard, PDSA and workflow-body consistency. Codex/Copilot repository profiles are covered by synchronization tests. Four detected local host families yielded two custom body differences: OpenCode and Antigravity shippers require reliable evidence of Luna/high runtime before publication. These extra guards were preserved. The checker's exit 1 is expected for these differences; it must not be represented as a clean 24/24 match or repaired by deleting customization. Such a guard may prevent publishing on a host that cannot expose that metadata.

The factory separates contract review, implementation, verification, review, developer result acceptance, baseline consolidation, archival and authorized delivery. Main-session orchestration owns shared records and lessons; roles return candidates rather than racing to write shared history. Run helpers detect structural and identity errors, not fabricated evidence. Configured names/models and tests cannot prove host selection, permissions or actual isolation. No additional permanent agents or supervisor agents are justified by this review.

## Documentation, identity and remaining work

Active repository identity, generated manifests and source resources now use `teknolista/pentapro`; source packages live at `skills/<name>`. Installed `.agents/skills/<name>` paths remain valid. The README, routing, CI and commands agree on the new source layout. Remaining old URLs in immutable archives/PDFs/old receipts describe historical sources and must not be mechanically rewritten as current evidence.

Minor navigation improvements in this review: normalize README source-checkout placeholders to `/path/to/pentapro`, link this dated assessment from README and the review index, and retain older reports as historical. No production helper or workflow behavior was changed to manufacture additional green tests.

Outstanding items before broader readiness claims:

1. **Publication:** local maintenance has not been committed/pushed. The renamed GitHub repository still serves the earlier source snapshot until authorized delivery. New-clone readiness must be checked against the published revision, not inferred from this dirty checkout.
2. **Codex project binding:** the previous migration changed the project trust path but the desktop project entry still referenced the old folder when last inspected. It was not repaired or reverified in this review; resolve via supported app configuration before treating desktop migration as complete.
3. **Legacy prompt hook:** optional `opencode.ts` needs actual host/package typing and hook integration tests before capture guarantees. The collection does not install hooks by default.
4. **MCP:** provision optional dependencies in an isolated authorized environment and rerun the real SDK smoke if protocol compatibility is required for the release claim. Exit 2 is incomplete, not passed.
5. **Platform and behavior trials:** expand registered cases based on risk, then execute meaningful matching/ambiguous/nonmatching tasks. Real Android, browser accessibility, other host adapters and model behavior require their own environments; authored scenarios are not executed trials.
6. **Exact CI runtime and independence:** confirm GitHub CI on the delivered revision using Node 24 and obtain independent review if required for the eventual delivery workflow. This self-review does not satisfy a fresh-reviewer gate.
7. **Deferred evolution:** the 103-proposal plan, including terminal-specific UI skills, process efficiency experiments and usage measurement, remains pending. Do not describe it as delivered or promise token savings.

Recommendation: the current structure is suitable for controlled use within its documented limits, with strong local helper regression protection. Complete the publication/configuration handoff and validate each target host before wider adoption. Keep the explicit evidence limits; replacing them with “100% ready” would make the documentation less accurate.
