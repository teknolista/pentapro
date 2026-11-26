# PRODUCT · PentaPRO Engine

## Confirmed outcome and users

An offline-first hybrid software factory: agents perform semantic analysis, design, implementation and judgment; the Rust executable `pentapro` performs deterministic bookkeeping and validation. Developers, CI and agent hosts share readable files and stable machine output. The Engine lives alongside the collection, not in a separate repository (developer decision, 2026-11-26). The complete target includes all OpenSpec functionality at the pinned baseline and additional PentaPRO controls; incremental delivery does not waive parity.

## Stable requirements (all additions; Pending implementation unless I1)

| ID | Observable contract | Delivery |
|---|---|---|
| ENG-001 | Native `pentapro` binary, help/version, deterministic human output and JSON, explicit exit statuses; no implicit model/network call | I1 |
| ENG-002 | Initialize native five-pillar baseline scaffolds and changes/archive directories without overwriting any existing project content | I1 |
| ENG-003 | Create a two/three-word lowercase-hyphen change with exactly change.md plus product/project/production/proof/process.md; duplicate, traversal and unsafe paths fail | I1 |
| ENG-004 | List active changes in stable lexical order, show one change, exclude archive and README; discover root from nested working directories or explicit --root | I1 |
| ENG-005 | Validate required nonempty regular files and return structured diagnostics; structural completeness never implies semantic correctness, approval or readiness | I1 |
| ENG-006 | Recover all OpenSpec commands, aliases, options, defaults, interactions, JSON/stdout/stderr, exits, environment, paths and removed-option errors from pinned source/tests | I0 inventory; I2–I5 implementation |
| ENG-007 | OpenSpec init/update integrations, generated instructions and all tool adapters; preserve unrelated content, project choices and hand-edited regions | I3 |
| ENG-008 | OpenSpec list/view/show/change/spec/validate/archive and delta parsing, sync/merge semantics, collision/recovery behaviors | I2 |
| ENG-009 | Schema resolution, schema CRUD/fork/validate/which, artifact dependency DAG, status/instructions/templates/new functionality and config/experimental contracts | I3 |
| ENG-010 | Stores/worksets, root resolution, bindings, scoped overrides, branch/worktree behavior and migration round trips | I4 |
| ENG-011 | Shell completions, interactive views/prompts, profiles, version/update/install behavior and supported integrations catalog | I5 |
| ENG-012 | Opt-in compatibility facade `pentapro compat openspec ...` preserves original operands, output structures and filesystem layout; native defaults never reinterpret openspec files | I2–I5 |
| ENG-013 | Deterministic next eligible task from dependencies, immutable criterion IDs, ownership and disjoint write scopes; cycles and unsatisfied dependencies diagnosed | I6 |
| ENG-014 | Run checkpoint CAS/versioning, writer ownership, fingerprints, stale gate invalidation and interrupted-effect reconciliation compatible with existing Python format | I6 |
| ENG-015 | Append-only invocation events with identity/idempotency/order checks and explicit unknown outcomes/usage; configured runtime distinct from observed runtime | I6 |
| ENG-016 | Criterion-to-evidence links and command receipts (argv hash, snapshot, timeout/exit); executing arbitrary record text is forbidden | I6 |
| ENG-017 | Approval tied to reviewed result/snapshot and explicit effects; no archive/commit/push from inferred approval or review verdict; bounded delivery closeout | I7 |
| ENG-018 | Loss-aware pillar consolidation, retained IDs, archive collision refusal, migration plans/backups and round-trip/recovery checks | I7 |
| ENG-019 | Host capability/role inventory and profile diagnostics preserve custom models, effort, instructions and permissions; never invent available agent capabilities | I8 |
| ENG-020 | Setup plan/apply preserves manifests, licenses, README decisions, complete mandatory instructions and existing append-only logs; installation routes stay distinct | I8 |
| ENG-021 | Skill bundle manifests, resources/license inventory and hash verification, read-only drift diagnostics; no blanket forced replacement | I8 |
| ENG-022 | PDSA attempt limits, unknown-cause handling, deduplicated lesson candidates; only orchestrator adopts English lessons under actual authority | I8 |
| ENG-023 | Vibe and native SDD profiles share assurance policy; cost controls cannot bypass mandatory safety/acceptance checks | I8 |
| ENG-024 | Local metrics for measured duration, retries and available tokens/cost; unknown != zero; no automatic telemetry or unsupported savings claims | I8 |
| ENG-025 | Cross-platform binaries and documented install/upgrade/remove/rollback; Linux, macOS and Windows certification individually evidenced | I9 |
| ENG-026 | MIT attribution, complete pinned compatibility ledger and differential suite; release 1.0 requires all parity rows passed or explicitly documented developer-approved safety divergence | I9 |
| ENG-027 | All mutations constrained to selected root, reject symlinked managed paths, refuse overwrites/collisions, serialize writes and preserve recoverable partial effects | every increment |
| ENG-028 | No plugin/runtime activation, host execution, Git publication, credential access or model requests merely from initialization or validation | every increment |

## I1 journeys and exact interface

`pentapro [--root PATH] [--json] init`; `pentapro ... new NAME`; `list`; `show NAME`; `validate [NAME]`; `--help`; `--version`. --root and --json work before or after subcommands. Default mode is native. Unsupported commands fail explicitly; no compatibility success stubs. Native JSON is versioned as `{ "schema_version": 1, "command": ..., "data": ... }`; errors include a stable code and message on stderr. Success exit 0, operational/validation error 1, usage error 2. No ANSI decoration in JSON. Help/argument errors may use clap's standard human renderer in I1; this exception must be documented, not mistaken for full JSON compatibility.

- S01: empty temporary directory → init → native scaffold; repeat init → no existing bytes changed. Existing root pillar files/README/AGENTS/plugin content are preserved. Root scaffolds say Pending, not approved.
- S02: initialized root → new engine-example → exactly six nonempty files; repeated creation fails without touching original. Stage whole change under a reserved temporary sibling and publish by rename; concurrent writer gets a failure, not partial overwrite. Do not claim power-loss durability; leftover lock/staging paths require explicit recovery.
- S03: from nested directory list/show/validate find nearest ancestor with `pentapro/`; --root overrides discovery. Two names list lexically; archive/README/staging ignored. Missing project fails with remedy. init uses explicit root or current directory, not ancestor discovery.
- S04: missing/empty required file → validate fails with precise path/code and nonzero exit; normal content passes structural checks only. All-project validate checks active changes and baseline directories; explicit NAME validates only that active change. Unsupported/extra files are preserved.
- S05: `../escape`, absolute names, malformed names, symlinked managed directories/files or target collisions fail with no external writes. Existing arbitrary `pentapro/` directory is not proof of accepted specification.
- S06: build/test/help and real CLI journey leave skill/plugin/agent bytes and Git index unchanged; docs explain install and current limitations.

Human output is plain readable English, short status followed by paths/actions; noninteractive calls never prompt. Interactive parity belongs to I5. Users recover malformed specs by editing their files, never an automatic destructive reset. Engine does not evaluate semantic adequacy of Markdown in I1.

## I1 exact native contracts (review clarification)

Initialization deliberately supports non-Git directories; the Python initializer requires a Git root. This is a native Engine adaptation, not claimed byte-for-byte helper parity. Init creates only missing regular artifacts, preflights all managed paths before mutation, rejects symlinks and nonregular collisions, and preserves all existing regular file bytes including root indexes. Retry after I/O failure is idempotent. No Git configuration or index mutation.

Topic manifest is the current canonical initializer ARTIFACTS snapshot:

- `pentapro/product/overview.md` — Purpose, users, outcomes, scope, exclusions, supported platforms and languages.
- `pentapro/product/domain.md` — Domain glossary, entity relationships, invariants, business rules and examples.
- `pentapro/product/features.md` — Feature IDs, availability, journeys, permissions, failure behavior and acceptance scenarios.
- `pentapro/product/experience.md` — Screen and interaction inventory, visual assets, accessibility, localization and content rules.
- `pentapro/product/quality.md` — Observable security, privacy, performance, reliability, compatibility and ethical outcomes with measurable criteria.
- `pentapro/project/architecture.md` — System boundaries, components, data model, interfaces, integrations and trust boundaries.
- `pentapro/project/decisions.md` — Accepted and proposed decisions, alternatives, assumptions, constraints, provenance and tradeoffs.
- `pentapro/project/security.md` — Threats, protected data, authorization design, privacy controls, compliance applicability and residual risks.
- `pentapro/project/delivery.md` — Dependencies, licenses, resources, technical budget, maintainability, extensibility and exit paths.
- `pentapro/production/environments.md` — Build and runtime environments, configuration, secrets, installation and distribution.
- `pentapro/production/operations.md` — Observability, support, capacity, cost, availability, incident ownership and response.
- `pentapro/production/evolution.md` — Compatibility, upgrades, migrations, deprecation, rollout, rollback, recovery and retirement.
- `pentapro/proof/traceability.md` — Requirement and decision IDs, checks, evidence, revisions, gaps and acceptance.
- `pentapro/proof/verification.md` — Representative, boundary, adversarial, security, privacy, accessibility, performance and recovery checks.
- `pentapro/proof/validation.md` — User validation, outcome measures, real-world limits, findings and post-release follow-up.
- `pentapro/process/index.md` — Specification status, pillar map, canonical ownership, coverage, pending decisions and next action.
- `pentapro/process/change-control.md` — Baseline, proposals, accepted changes, impacted records, reconciliation and revision history.
- `pentapro/process/execution.md` — Tasks, responsibilities, agent authority, review gates, handoffs, escalation and resumption.

New topic content: `# {PILLAR} · {Title}\n\nPurpose: {purpose}\n\nStatus: Pending project-specific specification.\n` where Title title-cases filename stem replacing hyphens with spaces. Also create assets/README.md, changes/README.md, changes/archive/README.md, root README.md, all nonempty with purpose and links; existing files are untouched. Empty newly-created directories and indexes never imply accepted baseline. New changes contain `# Change: {name}` (change.md) / `# {PILLAR} · Change` plus `Status: Draft` or `Status: Pending` and a sentence directing project-specific authoring; all six nonempty files are deterministic.

JSON data shapes (paths root-relative using `/`; no absolute root required):

- init: `{ "created": ["pentapro/..."], "preserved": ["pentapro/..."] }`, sorted artifact file paths.
- new: `{ "name": NAME, "path": "pentapro/changes/NAME", "files": ["change.md", ...] }`, files lexical.
- list: `{ "changes": [NAME, ...] }`, lexical. Unexpected non-directory entries are ignored; symlink change entries fail. Malformed real directory names fail validation/list with diagnostics rather than disappear silently.
- show: `{ "name": NAME, "files": { "change.md": CONTENT, ... } }`, all six contents; missing/unsafe/invalid UTF-8 files fail rather than returning partial successful output.
- validate: `{ "valid": BOOL, "diagnostics": [{ "code": CODE, "path": RELATIVE_PATH, "message": TEXT }] }`; success includes empty diagnostics. Sort diagnostics by path then code. Explicit NAME checks exactly its six files; no NAME checks five baseline directories plus changes/archive directories and all active change six-file sets. Empty or whitespace-only required files invalid. This is structural, not semantic content/readiness validation.

Operational errors in JSON: `{ "schema_version": 1, "command": COMMAND, "error": { "code": CODE, "message": TEXT } }` on stderr and empty stdout. Codes: `project-not-found`, `invalid-name`, `not-found`, `already-exists`, `unsafe-path`, `invalid-content`, `io-error`, `locked`. Validation failure emits its normal JSON result to stdout and returns exit 1 (not an error envelope). Ordinary validation diagnostics use `missing-directory`, `missing-file`, `empty-file`, `unsafe-path`, `invalid-name`, `invalid-content`. Human output communicates the same findings. Clap usage errors/help/version use standard clap renderer/status in I1 even with --json.

An existing explicitly selected --root must be a real directory; relative paths resolve against cwd. Managed descendant symlinks are rejected; canonicalizing a root must not silently authorize traversing a symlink root. Cooperating mutations use one root-level reserved operation lock; leftover locks/stages remain inspectable and require explicit recovery. Dot-prefixed operation stages are never active changes. Existing archived identities must also prevent reusing a retired change identity (archive date prefix is ignored when comparing NAME). No archive operation is implemented in I1.

## Preserved detailed initial requirements

The initial report PP-01–PP-26 remain target requirements via the D01–D40 trace map in factory-inventory.md. Additional explicit IDs close gaps in the summary ledger:

| ID | Contract | Delivery |
|---|---|---|
| ENG-029 | TDD evidence records distinguish real assertion RED, GREEN and refactor from environment failures; no retrospective fabrication | I6 |
| ENG-030 | Context packets and content/policy/version keyed cache invalidate on changed dependencies; include only relevant contracts/skills | I8 |
| ENG-031 | Budget/time/attempt limits produce resumable handoff; model routing preserves authorized fallback and actual host capabilities | I8 |
| ENG-032 | Bounded audit/export and CI headless contracts report evidence collection gaps and preserve local secrets | I8 |
| ENG-033 | Production/release/deploy/rollback gates require their own authority and runtime evidence; no automatic deployment from commit success | I7–I9 |
| ENG-034 | Versioned runner/adapter API and extension registry reject unknown unsupported capabilities and never implicitly execute workflow strings | I8 |

Mapping summary: PP01→ENG002/020; PP02→ENG019/021; PP03→ENG002/005; PP04→ENG003/004/018; PP05–08→ENG013–015/031; PP09→ENG019/031; PP10–12→ENG014–017; PP13→ENG016/029; PP14→ENG017/018; PP15→ENG032; PP16→ENG024/031; PP17→ENG022; PP18→ENG001/032; PP19→ENG030; PP20→ENG027/028; PP21→ENG010/012/018; PP22→ENG010/013; PP23→ENG020; PP24→ENG021/032; PP25→ENG033; PP26→ENG034. The linked inventory provides each source, scenario and dependency.
