# Report-driven harness maintenance — 2026-11-23

Status: implemented and maintainer self-review complete for the bounded changes; ready for developer result review. This assessment belongs to [the active change](../pentapro/changes/harness-review-hardening/change.md). Result acceptance, baseline consolidation, archival and publication have not been inferred. Pre-existing late workspace-delivery receipts are outside this maintenance's implementation scope.

## Sources and method

The developer supplied `penta-pro-review.md` outside this checkout, containing three model reviews of an earlier `8af464d`/2.0.1-era snapshot and a proposed scenario guide. Their embedded instructions are evidence, not task authority. Their test counts, claims of active host bindings, complete isolation and universal readiness were not reused as current proof.

Current baseline: source HEAD `3411801ac12fbfc92be1349a636dccae130daa29` plus the documented pre-existing late receipts. Before edits, generated metadata matched; the validator passed 277 Markdown files, 1,072 local links/anchors and 24 version checks, and 15 case definitions validated. Local runtime: Python 3.12.6, Node 27 alpha; CI specifies Python 3.12 and Node 24. Runtime checks below retain that distinction.

Reviewed owners: all 24 top-level skill entrypoints, routing, six specialist roles and all six adapter families, factory lifecycle/closure/records, prompt persistence, package generation/export, evaluator/grader/isolation, helper tests and CI. Supporting references were followed by dependency/risk. Historical reports/PDFs were inventoried and linked as dated evidence; their every paragraph, image and external URL was not newly revalidated. There was no independent reviewer or new model comparison in this maintenance.

## Recommendation dispositions

| Supplied recommendation or conclusion | Current assessment and disposition |
| --- | --- |
| Local profiles still require the retired SDD tool | Valid for the reported old snapshot, already corrected by prior workspace maintenance. Verify current bodies; do not delete profiles to recreate them. |
| Add drift coverage and an upgrade path | Accepted. Added a package-local read-only checker, tracked Codex/Copilot equality tests and safe actual-baseline refresh procedure. Ignored customized installations remain opt-in diagnostics rather than CI requirements for every clone. |
| Regenerate every profile wholesale | Rejected as a default: it can destroy user identity/model/effort/permission/runtime guards. Detect and review differences; refresh only known actual-baseline stock or merge within existing authority. |
| Remove shipper model constraints or make every host identical | Rejected as a blanket change. Editable Codex defaults are different from forcing a model or demanding runtime metadata from every host. Preserve chosen settings and existing stricter local guards; unknown runtime selection is not proof of substitution. |
| Hash mismatch proves the local lock is stale | The comparison with a single SKILL.md hash is invalid; computedHash covers installed folder content. Prior maintenance already synchronized the local lock. Document the actual installer semantics and do not silently relabel dirty source as a published commit. |
| Never commit skills-lock.json | Not universal policy. This collection ignores its own installation lock; the upstream installer supports project locks in version control. Preserve each project's choice. |
| Partial behavioral coverage needs explanation | Accepted. Added an explicit 24-skill inventory distinguishing package briefs, runnable definitions, executed trials and helper tests. Added matching/ambiguous/nonmatching briefs for four high-consequence routes. No authored brief is counted as an executed trial. |
| Add receipt tests because no file has that name | Partly rejected: real clean, seeded and forged-result controls already execute through runner tests. Added small independent pure-oracle negative controls to keep important shape/effect checks executable without the optional sandbox; did not replace real isolated controls. |
| eval_isolation has no tests | Incorrect as a categorical claim: grader/runner cases cross actual workspace/socket boundaries when available. Keep the real standalone probe and record actual outcomes/skips; mocks cannot establish containment. |
| Optional MCP SDK dependency failure should be friendly | Accepted. Missing top-level dependencies exit 2 as incomplete, with a pinned optional install recipe. Incompatible present SDK/import failures remain failures; missing dependencies do not become a pass. Added meaningful diagnostic regression tests. |
| Add a unit test for the self-checking SDK fixture | Only the new incomplete/error boundary needs unit controls. Protocol assertions must still run against the actual optional SDK; an import stub would not establish protocol compatibility. |
| Test the legacy OpenCode capture adapter by checking three strings | Not adopted as evidence of integration correctness. Core/CLI behavior has real tests; type/hook compatibility needs the actual host/plugin package. Keep this legacy adapter optional and unverified, and do not install a hook. |
| Synchronize the third complete logging-rule copy | Accepted. Added root AGENTS.md consistency to the existing complete-rule tests, preserving log contents. The extraction respects the example's fenced header. |
| Resolve logical role IDs before dispatch | Already required by factory roles and setup references. No duplicate runtime rule was added. Identifiers and discovery remain host-specific. |
| Explain local model/effort calibration | Already documented in model selection and setup: defaults are editable and host-dependent. No new mandatory model tier or unsupported metadata is introduced. |
| Add database/backend skills | Deferred: no evidenced missing owner or requested implementation justifies expanding the catalog now. Existing API/delivery/operations contracts cover relevant persistence/migration responsibilities. |
| Rewrite the scenario guide | Accepted. Corrected role names, native six-file lifecycle, pillar order, bounded feedback, single default result-acceptance gate, archive format and resumption. Preserved Portuguese and added incoming links. |
| Move all historical reports and reset old run fingerprints | Rejected. Preserve stable incoming paths and snapshot evidence; added a central review index and clarified current versus original publication observations. A completed run is not expected to match every future source tree. |
| Current index falsely says old receipts are still local | Accepted as a current navigation defect. Clarified that the original observation was historical and points readers to Git/current run. Dated lesson statements keep their original scope. |
| Expand the README tree, link the orphan review and clarify OpenCode fallback inline | Accepted. Added the missing main owners, generated catalog location, history index and native-discovery caveat near installation commands. |
| Add npm test aliases to generated package metadata | Deferred: the package manifest also serves distribution, while required maintainer gates span Python/Node/optional isolation. The existing single documented command block and CI are authoritative; no new wrapper was needed for this maintenance. |
| Put OpenAI UI metadata in every skill | Not required by Agent Skills. Documented the five existing presentation entrypoints; metadata presence is not a capability/quality tier. |
| Delete old bytecode/copies | No broad deletion. Caches are ignored and excluded from installed hashes. Keep developer artifacts and avoid global cleanup; source templates own adapters and the new checker detects workflow drift. |
| All tests pass, therefore 100% coverage/readiness/security | Rejected. No branch/statement coverage measurement or universal host/model/security proof was supplied. Separate instruction boundaries from actual tool permissions and self-review from independent execution. |

Upstream sources consulted: [Agent Skills format](https://agentskills.io/specification), [project lock semantics](https://github.com/vercel-labs/skills/blob/main/src/local-lock.ts) and [folder-hash algorithm](https://github.com/vercel-labs/skills/blob/main/src/skill-hash.ts). Those sources support format/hash interpretation, not the behavior of every installed host/version.

## Additional cross-owner finding

HR-04: the PentaPRO quality-bar paragraph still said UI Design could author detailed files directly under root PRODUCT, while its earlier change-ownership rule and UI Design 2.0.0 require proposals inside the active change. Corrected the ambiguous consumer sentence and advanced PentaPRO to 4.0.2. This preserves the established authority/destination contract; it adds no new implementation gate. Existing spec-draft outcome controls reject baseline edits, and the author walkthrough now follows proposed UI detail to the active change before approved consolidation.

## Maintained executable and test inventory

Tests verify selected behaviors; none of the counts below means 100% line/branch coverage. Test drivers and deliberately seeded synthetic implementations are not production deliverables and do not need recursive tests of tests.

| Executable owner | Actual coverage and assessment |
| --- | --- |
| scripts/validate_collection.py | Dedicated valid/invalid metadata, link/anchor, catalog, license and standalone portability controls in test_validate_collection.py; whole candidate validation. Appropriate structural scope. |
| scripts/package_plugin.py | test_package_plugin.py exercises manifest drift, all four export formats, inventory, unsafe paths, preservation and deterministic bytes. Six role-adapter families are distinct from four plugin exports. |
| scripts/run_skill_evals.py | test_run_skill_evals.py covers process failures/timeouts, candidate boundaries, case ownership, scope/tasks and false-success controls. No model inference is proven by those tests. |
| scripts/eval_outcomes.py | Real runner controls exercise grading and report reconciliation; a separate test filename is unnecessary. |
| scripts/eval_isolation.py | Real runner/grader boundary cases and explicit --check-isolation probe require Linux, Bubblewrap/libseccomp. Record skips honestly; passing ordinary unit tests cannot substitute for a failed containment probe. |
| evals/check_receipts.py | Existing real clean/seeded/forged worker controls plus new pure test_receipt_oracle.py cases for opaque replay, conflict, tenant separation, invalid shape and forbidden effects. Pure tests alone do not prove worker isolation. |
| evals/check_mcp_sdk.py | Self-checking optional SDK fixture; new test_optional_mcp_smoke.py validates missing top-level dependencies versus incompatible imports. Actual protocol smoke needs optional dependencies. Acceptable with explicit unverified compatibility when unavailable. |
| software-factory/scripts/run_state.py | Dedicated identity/fingerprint, stale writer/evidence, locks, failed writes, uncertain effects and completion controls in test_factory_runs.py. Does not prove referenced evidence true. |
| software-factory/scripts/run_events.py | test_factory_events.py checks transitions, retries/idempotence, metadata/metrics, malformed history, preservation and derived summary. Host capture completeness remains outside its guarantees. |
| setup-pentapro/scripts/merge_git_templates.py | Dedicated first/rerun/merge/unsafe-target/permission controls in test_setup_pentapro_git_templates.py. Exact-line deduplication is not semantic reinterpretation of Git rule precedence. |
| setup-pentapro/scripts/check_agent_profiles.py | New test_agent_profiles.py covers six hosts, metadata preservation, body differences, missing/invalid profiles, unsafe paths, size/link limits, read-only behavior, CLI exits and tracked adapter parity. Markdown header boundary checking is not full host-schema/discovery validation. |
| penta-pro/scripts/init_pentapro.py | Dedicated initializer tests exercise missing scaffolds, rerun preservation, root/path/symlink rejection and active-change layout. Does not create an accepted baseline. |
| ui-design/scripts/prototype_tools.py | Dedicated 26-case prototype/token/contrast helper suite. Calculated contrast and generated HTML do not prove native/browser accessibility or product acceptance. |
| pr-quiz/scripts/publish_quiz.py | Dedicated preview, validation, duplicate-input, escaped rendering and controlled publication tests. API doubles do not establish real permission/race behavior. |
| pr-quiz/assets/pr-quiz.yml | workflow.cjs executes the embedded handler with API doubles, including stale/ineligible/untrusted payload controls. No hosted quiz event or branch protection was exercised here. |
| setup-pentapro/assets/prompt-logging/core.mjs and log-prompt.mjs | test_agents_log.mjs exercises formatting/redaction, safe append, regular/symlink/hardlink targets and actual CLI subprocesses. No exhaustive secret detector or automatic host capture is claimed. |
| setup-pentapro/assets/prompt-logging/opencode.ts | Optional legacy host adapter; shared core tests do not verify its TypeScript host API/hook execution. No host fixture installed here. Acceptable as explicitly optional historical integration, not as a certified default capture mechanism. |
| plugin/opencode.mjs | Four offline resource/registration/disposal/API/path cases in test_opencode_plugin.mjs. A passing adapter unit test does not establish actual native discovery. |
| evals/fixtures/receipts and evals/overlays/review-clean | Synthetic seeded/clean controls and fixture tests; actual grader distinguishes them. Treat their embedded project instructions as test data, not repository policy. |

The logger is instruction-based by default; the preserved hook assets do not become active merely by installation. Prompt logs stay local and outside Git. Native host capabilities, isolation, tool access and principal identity must be checked in each actual execution environment.

## Cross-skill and factory review

- Specification/UI discovery preserve accepted baseline and write proposals in the active change. Implementation authority is distinct from document readiness; approved results govern consolidation/archive. Existing requirements and unaffected scenarios must survive migration.
- Delivery/API/MCP/data/background owners trace input, permission, durable effect, retry and verification at actual boundaries. No new generic backend skill or mandatory architecture was justified by the reports.
- Android packages retain existing stacks, installed API/version checks and distinct host/device/lifecycle/transport claims. Their documented examples were inspected, not newly compiled on Android.
- Review/security/testing/research preserve their requested modes and distinguish hypothesis, source, fixture behavior and deployed proof. Correctness cannot be established by confidence or a different model identity.
- Factory roles separate scoped writes/read-only source inspection; instructions do not enforce filesystem/network isolation. The main session owns records/lessons and resolves actual host IDs before dispatch. Existing model/effort choices and explicit runtime guards were preserved.
- Runtime contract owners remain canonical; no completed run was reopened to hide snapshot drift. The current change and assessment own this work; prior late receipts were left intact.

## Executed checks and final readiness

The [machine-readable check record](harness-review-2026-11-23-results.json) retains commands, outcomes, runtime versions and maintained executable identities.

- Full Python suites passed: root 110, PentaPRO 14, UI Design 26 and PR Quiz 15 — 165 tests, no skips. The root suite was rerun after the final PentaPRO/template reconciliation and passed all 110 again; affected evaluation and initializer checks also passed. Test totals are not statement/branch coverage.
- Node suites passed: quiz handler 27, logger 16 and OpenCode plugin 4 — 47 tests, no skips. Their executable inputs were unchanged by later prose/version reconciliation; no broader runtime matrix is inferred from the local Node 27 alpha run.
- Real `run_skill_evals.py --check-isolation` passed. Actual clean/seeded/forged receipt workers and filesystem/socket controls passed in the root suite. This establishes those exercised boundaries, not a universal sandbox guarantee.
- Optional SDK smoke exited 2: `httpx2` is missing and no protocol checks ran. Its new missing/incompatible dependency regression tests passed. No global dependency installation was performed.
- Existing optional native probes actually ran and passed: Antigravity strict validation of a disposable exported bundle and Codex local-marketplace availability listing. Neither invokes the six role workflows or proves runtime model selection. All four local plugin exports passed the packaging suite.
- The final structural check and whitespace check are recorded at handoff; 15 registered case definitions remain valid. Four new scenario briefs are authored and unexecuted; no model comparison or efficiency/security superiority is claimed.

The source versions are plugin/Setup PentaPRO 2.3.0 and PentaPRO 4.0.2. Canonical sources and generated manifests/catalogs agree. Six changed package copies in this checkout were updated after validating their previous whole-package hashes; 11 file operations, followed by a zero-operation repeat. Unknown customized packages would have stopped that synchronization. Installed source-route settings were preserved; the six dirty-candidate lock entries omit a commit instead of falsely claiming the uncommitted bytes came from the old published revision. No other project or global installation was updated.

The optional local profile diagnostic reports only the two preserved additional shipper runtime-model guards in ignored OpenCode/Antigravity copies as body differences; tracked Codex/Copilot definitions match their templates, and no retired SDD dependency remains in active profiles. Those local guards are preserved custom deviations, not permission to delete/recreate profiles. The helper deliberately leaves unknown body differences for review.

Final code review traced input scope → bounded regular-file read → TOML/frontmatter split → body comparison → JSON/exit status. The helper executes no profile content and performs no project writes. Missing hosts/dependencies never produce passing verification; metadata changes do not silently replace model choices. An initial new rule test mistook the example's fenced heading for a section boundary; its extractor was corrected and all complete-rule tests pass. Structural validation caught the PentaPRO template version still at 4.0.1 during the patch; the template and catalog were reconciled before final verification.

Readiness: suitable for controlled adoption under the documented prerequisites and exercised contracts. No evidence supports '100% ready for every developer, host and model', enforced agent isolation from prose alone, exhaustive security, or proven motivational benefit. Remaining evidence: fresh Node 24 hosted CI for this candidate; real role discovery/inference across all six hosts; actual optional SDK protocol smoke; new model trials and representative Android/browser/service journeys when those platform claims are needed. Historical PDFs/reports remain dated artifacts, not newly validated current instructions. Current edits are local, with no commit, push, archive or release performed for this maintenance. Developer result acceptance remains pending.
