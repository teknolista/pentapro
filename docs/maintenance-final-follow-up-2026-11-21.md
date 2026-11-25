# Final maintenance follow-up — 2026-11-21

## Result and scope

Maintainer self-review starting from `0bdaf3ea8c19d91efa7017df4d9208c1da1bbf4e`, initially clean. This review covers the 24 source skill entrypoints, six local Codex roles, corresponding Copilot profiles, 30 distributed host adapters, factory execution/record/lesson contracts, package generation, CI and maintenance instructions. All distributed Markdown paths and anchors receive structural validation. Supporting references and script implementations were inspected by risk and dependency; this is not a line-by-line semantic audit of every reference, fixture, external technical example or historical PDF page. No new independent agent review or comparative model trial was run.

The collection has a usable installation/setup path and passed the available local checks below. These results do not establish universal readiness, invulnerability, optimal cost or identical activation on every developer's host. The README's development-status notice remains accurate. No substantiated executable defect requiring a code change was found in this pass.

## Skill contracts

The declared outcomes, ownership, authority and failure/evidence handling of all 24 entrypoints were screened. The following boundaries remain deliberate; no rewrite was justified merely to enlarge an instruction set.

| Skills | Outcome and important boundary |
| --- | --- |
| agent-instructions, setup-pentapro | Portable instruction maintenance versus non-destructive project initialization; preserve customized files and prompt logs. |
| penta-pro, ui-design | Canonical five-pillar and screen contracts; specification, accepted decisions and observed runtime evidence remain distinct. |
| peer-review, cybersec | Substantiated implementation findings versus threat/control assessment; reviewed content cannot authorize privileged effects. |
| diagnose-defect, technical-research | Causal investigation versus evidence-backed technical decisions; uncertainty stays visible. |
| behavior-testing | Observable contract checks, meaningful failing controls and explicit test-only boundaries. |
| http-api, mcp-server | Real interface/effect authorization, compatibility and replay semantics; client descriptions do not enforce server permissions. |
| software-delivery, software-factory | Dependent implementation versus multi-agent coordination; current evidence, disjoint writes and recovery records retain owners. |
| git-ship, production-operations | Exact Git publication versus deployment/runtime effects; uncertain effects require reconciliation before retry. |
| pr-quiz | Requested educational aid; public answers and informational status do not certify review or security. |
| android-module-structure, android-di-koin | Existing build/DI choices and lifetimes; no unsolicited toolchain or container migration. |
| android-data-layer, android-error-handling, android-background | Transactions, account fencing, cancellation, typed expected failures and bounded durable retries. |
| android-unit-testing, android-integration-testing, android-ui-testing | Deterministic logic versus actual storage/transport/device boundaries; fake-backed success cannot establish live behavior. |

The portable package shape was also compared with the [Agent Skills specification](https://agentskills.io/specification). Source-name, metadata, catalog, version, license, local-link and standalone-resource checks remain deterministic collection gates, not behavioral certification.

## Repairs and synchronization

- Corrected the active Portuguese factory adoption guide: it still required runtime proof of Luna/high as a shipping prerequisite after that rule had been removed from the templates. The guide now preserves configured/default/customized parameters and default role execution, while retaining real permission and Git gates.
- Bumped Setup PentaPRO to 1.10.1 and Software Factory to 0.5.1 to identify the changed role-invocation/model-choice contract. Bumped the aggregate bundle to 1.1.1 and regenerated host metadata. All configured role model/effort values are retained.
- Added matching, ambiguous and non-matching authored cases for invocation, narrower review-only scope, customized parameters and absent runtime metadata. These are scenario definitions, not new executed model evidence.
- Marked the earlier same-day report as a historical snapshot and linked this follow-up from maintenance navigation. Historical test counts, design proposals, retrospectives and PDF exports keep their original evidence; they are not regenerated copies of the current README.

## Executables and tests

A separate test file per source file is unnecessary when another suite exercises its observable contract. Test counts below are not line/branch coverage. Test harnesses, deliberately faulty fixtures and policy overlays are test data rather than production modules needing recursive test suites.

| Source/helper | Automated coverage and judgment |
| --- | --- |
| `scripts/validate_collection.py` | `scripts/tests/test_validate_collection.py`; invalid and valid metadata/link/portability controls plus the real inventory. Appropriate regression coverage for these structural guarantees. |
| `scripts/package_plugin.py` | `test_package_plugin.py`; four complete exports, destination preservation, unsafe paths, ignored inputs, metadata freshness and reproducibility, plus optional native discovery probes. Real host invocation remains separate. |
| `scripts/run_skill_evals.py`, `eval_outcomes.py`, `eval_isolation.py` | `test_run_skill_evals.py`; lifecycle/grading/controls with the actual grader; the separate isolation probe exercises mount/socket/resource boundaries. Module splitting does not require duplicate test files. |
| `evals/check_receipts.py` | Runner suite exercises clean, seeded-defect and misleading-result cases. Independent synthetic grading is covered; it does not prove application correctness. |
| `evals/check_mcp_sdk.py` | Assertion-based in-process SDK smoke, itself a verification script. No separate unit suite is required for this fixture, but its SDK compatibility must be exercised before relying on it. Not run: `mcp` and `httpx2` are absent; no dependencies installed. |
| `skills/software-factory/scripts/run_state.py` | `test_factory_runs.py`; stale source/gates/writers, identity, locks, uncertain effects, forbidden paths and preservation. The helper validates local records, never the truth of referenced remote evidence. |
| `skills/penta-pro/scripts/init_pentapro.py` | 11 dedicated tests for initialization, existing content and unsafe paths. Live interviews and migration acceptance remain separate. |
| `skills/ui-design/scripts/prototype_tools.py` | 26 dedicated tests for inputs, contrast/fragments, injection bounds and exports. No browser/native accessibility certification follows. |
| `skills/pr-quiz/scripts/publish_quiz.py` | 15 dedicated tests with controlled publication/freshness behavior. Live GitHub permissions and concurrent editors remain adoption concerns. |
| `skills/pr-quiz/assets/pr-quiz.yml` | 27 offline scenarios execute the embedded handler with API doubles, including stale events, eligibility and reflected markers. No hosted workflow executed. |
| `skills/setup-pentapro/assets/prompt-logging/{core,log-prompt}.mjs` | 16 Node tests for redaction, formatting, safe append and CLI paths. Legacy adapters remain historical opt-in material, not current setup enforcement. |
| Legacy `prompt-logging/opencode.ts` | Core behavior covered indirectly; actual host API integration is untested. Acceptable only with its existing legacy/adoption limitations, not as a certified current integration. |
| `plugin/opencode.mjs` | Four offline tests for actual resource loading, registration/disposal, conflicts and rejected API/paths. Native OpenCode success remains unestablished; use the documented skills installation fallback. |
| Distributed role adapters | Six factory-agent tests parse metadata and check canonical instruction parity, role schema and PDSA clauses. These cannot prove that a host selects or obeys a role. |

No untested maintained production helper was identified without either indirect coverage or an explicit optional/legacy limitation. This does not mean every branch or environment has been exercised.

## Executed evidence

Python 3.12.6 and Node 27.0.0-alpha.0.0.0 were available; CI targets Python 3.12 and Node 24. No global dependencies, hooks or host settings were installed or changed.

- `python3 -m unittest discover -s scripts/tests`: 72 passed, including local package/discovery and factory-record controls.
- `python3 -m unittest discover -s skills/penta-pro/scripts/tests`: 11 passed.
- `python3 -m unittest discover -s skills/ui-design/scripts/tests`: 26 passed.
- `python3 -m unittest discover -s skills/pr-quiz/scripts/tests`: 15 passed.
- `node skills/pr-quiz/scripts/tests/workflow.cjs`: 27 passed.
- `node --test scripts/tests/test_opencode_plugin.mjs`: four adapter controls passed.
- `node --test scripts/tests/test_agents_log.mjs`: 16 passed outside the host subprocess restriction. The first restricted attempt failed; that failure is retained as an environment limit, not silently counted as passing.
- `python3 scripts/run_skill_evals.py --check-isolation --grade`: mount, socket and resource probes passed without model calls.
- `python3 scripts/run_skill_evals.py --check-cases`: 15 case definitions validated; no inference trial implied.
- `python3 scripts/package_plugin.py --check`, `python3 scripts/validate_collection.py` and `git diff --check`: final freshness, inventory/link/version and whitespace gates.

Python maintenance commands used `PYTHONDONTWRITEBYTECODE=1`. Matching earlier suite results are reused only for unchanged helper implementations; package/collection checks are repeated after documentation/version reconciliation.

## Adoption limits

Before relying on a new host/model combination, exercise actual skill discovery, a bounded role invocation, project setup/rerun preservation and the target project's checks. The prior successful Git deliveries in this session are bounded observations, not an all-host workflow benchmark. Copilot native installation and OpenCode plugin runtime success remain gaps in the earlier distribution record. Current configured model choices are respected without requiring unavailable runtime metadata; configuration still is not proof of actual selection or measured savings.

No consuming Android app/device, browser accessibility journey, deployed service/security test, live PR quiz workflow, fresh cross-model comparison or page-by-page PDF visual review was executed. External examples and remote links were not all revalidated. Historical PDFs remain explicitly historical; current skill entrypoints and maintained guides govern use. Local edits from this follow-up are not committed or published by this review request.
