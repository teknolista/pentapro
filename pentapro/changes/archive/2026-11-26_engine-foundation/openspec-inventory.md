# OpenSpec 2.2.0 parity inventory

Research snapshot: 2026-11-26. Source checkout HEAD `f1cd852f4edce22b8df9548a4df889172ca8ff25`, tags `v2.2.0` and `@fission-ai/openspec@2.2.0`. This is exactly the reference already cited in the initial PentaPRO Engine document. Source inspection only; no OpenSpec installation or tests executed. Mutable `main` was cloned once, then identified by SHA.

## Observable command families

| ID | Surface | Required behavior and principal source |
|---|---|---|
| OS-001 | Global/version | `--help`, `--version`, `--no-color`; `version --json --check`, install/update-channel reporting and explicit registry check (`src/cli/index.ts:145–260`, `src/core/version-check.ts`). |
| OS-002 | init/update | Interactive/noninteractive path setup, tools selection, language, profiles, project/global scope, legacy cleanup, Copilot cloud opt-in; update preservation, drift detection and JSON dry-run; optional self-update. `src/core/init.ts`, `update.ts`, `update-plan.ts`, `migration.ts`, `legacy-cleanup.ts`, `src/cli/index.ts:261–454`. |
| OS-003 | install | `install [version]` standalone binary installation, without Node requirement after install (`src/commands/install-standalone.ts`). Network/download and shell/profile effects must be explicitly tested and safe. |
| OS-004 | browse | `list` active/archived/all changes/specs, sorting and nested-change warnings; `show` change/spec disambiguation, requirement/scenario filtering and deltas/diff; interactive `view` dashboard. `src/core/list.ts`, `view.ts`, `file-view.ts`, `src/commands/show.ts`. |
| OS-005 | legacy aliases | `change show/list/validate` and `spec show/list/validate`; deprecated `--requirements-only` alias. Compatibility includes warnings/diagnostics, not merely the modern commands. `src/cli/index.ts:547–610`, `src/cli/commands/spec.ts`. |
| OS-006 | validation | Single/bulk/all/spec/change/archived validation, strict warnings-as-failure, concurrency, full/findings reports; Markdown headings/fences, scenarios, normative statements, task numbering and checkboxes, scenario loss and delta coherence. `src/commands/validate.ts`, `src/core/validation/*`, `src/core/parsers/*`. |
| OS-007 | archive | Preflight/validation, confirmation and JSON noninteractive diagnostics; spec merge and change archival; skip specs/no-validate; ADDED/MODIFIED/REMOVED/RENAMED, already-synced detection, purpose inheritance, scenario preservation, capability retirement opt-in and recovery after partial effects. `src/core/archive.ts`, `specs-apply.ts`. |
| OS-008 | workflow | `new change` metadata, goal/description/schema; `status` one/all change artifact DAG; `instructions` artifact/apply/archive; skipped specs, ready/blocked/done and transitive prerequisites, context/rules/guidance and reference indices. `src/commands/workflow/*`, `src/core/artifact-graph/*`, `change-metadata/schema.ts`. |
| OS-009 | schemas | `schemas`, `templates`; `schema init/fork/validate/which`; schema resolution precedence, custom artifacts/generates/requires/templates/apply, cycle/path validation and overrides. `src/commands/schema.ts`, `src/core/artifact-graph/resolver.ts`, `schema.ts`, `graph.ts`. |
| OS-010 | config | Global `path/list/get/set/unset/reset/edit/profile`, typed values/string/allow-unknown, preset or interactive profile; project config context/rules/schema/references/store/operation guidance and language/scope preferences. `src/commands/config.ts`, `src/core/global-config.ts`, `project-config.ts`, `config-schema.ts`, `profiles.ts`. |
| OS-011 | stores | `store setup/register/unregister/remove/list/doctor`; canonical store identity, Git backend, id/path conflicts, optional init-git/remote, registry atomicity and locks, guarded deletion and relationships. `src/cli/commands/store.ts`, `src/core/store/*`. |
| OS-012 | doctor/context | Nearest/store/declared/default/implicit root selection; relationship health across declarations, refs and known projects; assembled working set, brief, and optional VS Code workspace write with overwrite control. `src/core/root-selection.ts`, `working-set.ts`, `relationship-health.ts`, `references.ts`, `known-projects.ts`; `src/commands/context.ts`, `doctor.ts`. |
| OS-013 | worksets | Personal manually composed views: `create` repeated ordered members, optional tool; `list`/`ls`; `open` chosen tool; `remove` saved metadata only. Member directories never mutated; open rejects JSON rather than implying a machine launch receipt. `src/core/worksets.ts`, `openers.ts`; `src/commands/workset.ts`. |
| OS-014 | completions | Generate/install/uninstall Bash/Zsh/Fish/PowerShell; dynamic hidden `__complete`; managed profile blocks, platform profile handling, opt-in tip; no silent profile mutation. `src/core/completions/*`, `src/commands/completion.ts`. |
| OS-015 | feedback | Explicit GitHub issue via authenticated `gh`, title shortening and full summary/body retention; repository identity adaptation required for PentaPRO. `src/commands/feedback.ts`. |
| OS-016 | host assets | Generated skills and command formats, profiles/core/custom workflows, skills/commands/both delivery, project/global scopes, managed-content fingerprints, legacy migration and customized-content preservation, Copilot cloud workflow/agent. `src/core/config.ts`, `command-generation/*`, `shared/*`, `github-copilot/cloud-agent.ts`. |
| OS-017 | operating behavior | One JSON document on stdout, prose/spinners stderr, diagnostic envelopes/codes, exit codes 0/1, optional-key omissions, mixed casing compatibility, TTY prompts and noninteractive failures. `docs/agent-contract.md`, `src/commands/shared-output.ts`, `src/cli/index.ts`. |
| OS-018 | release/telemetry | npm and standalone packaging/self-install/update reports, telemetry preference/DNT, update-check controls. PentaPRO may deliberately disable telemetry but must declare/test this compatibility divergence rather than silently copy it. `src/telemetry/*`, `src/core/version-check.ts`, `src/commands/install-standalone.ts`, `package.json`, `build.js`. |

## Exact source registration inventory

The following source-derived list captures every `.command`, `.option`, `.alias`, `.addOption`, `new Option`, `.version` registration. Continuation lines are retained for multi-line registrations. Group context: `index.ts` contains root commands plus legacy `change`, `completion`, `new` subgroups; files in `src/cli/commands/` register the named subgroup, except `spec.ts` for legacy spec aliases and context/doctor root commands. This is a discovery inventory, not proof every flag combination has been behaviorally recovered.

### src/cli/index.ts

```text
36: return new Option(
37: '--store-path <path>',
38: 'Not supported; register the path with "openspec store register <path>" and use --store <id>'
39: ).hideHelp();
40: }
149: .version(version);
152: program.option('--no-color', 'Disable color output');
155: .command('version')
157: .option('--json', 'Output as JSON')
158: .option('--check', 'Check the registry for a newer version')
261: .command('init [path]')
263: .option('--tools <tools>', 'Configure all, none, or a comma-separated list of tool IDs')
265: .option('--language <language>', 'Write new OpenSpec artifacts in this language')
266: .option('--force', 'Auto-cleanup legacy files without prompting')
267: .option('--profile <profile>', 'Override global config profile (core or custom)')
268: .option('--no-animation', 'Show a static welcome screen instead of the animated one')
269: .option('--copilot-cloud', 'Set up GitHub Copilot cloud coding-agent files without prompting')
270: .option('--no-copilot-cloud', 'Skip GitHub Copilot cloud coding-agent files without prompting')
271: .option('--scope <scope>', 'Where the skills go: global (this machine, for every project) or project')
312: .command('experimental', { hidden: true })
314: .option('--tool <tool-id>', 'Target AI tool (maps to --tools)')
315: .option('--no-interactive', 'Disable interactive prompts')
332: .command('update [path]')
334: .option('--force', 'Force update even when tools are up to date')
335: .option('--dry-run', 'Report what the update would change without writing anything')
336: .option('--json', 'With --dry-run, print the planned changes as JSON')
457: .command('install [version]')
470: .command('list')
472: .option('--specs', 'List specs instead of changes')
473: .option('--changes', 'List changes explicitly (default)')
474: .option('--archived', 'Show only archived changes')
475: .option('--all', 'Show both active and archived changes')
476: .option('--sort <order>', 'Sort order: "recent" (default) or "name"', 'recent')
477: .option('--json', 'Output as JSON (for programmatic use)')
478: .option('--store <id>', STORE_OPTION_DESCRIPTION)
479: .addOption(hiddenStorePathOption())
520: .command('view')
522: .option('--store <id>', STORE_OPTION_DESCRIPTION)
523: .addOption(hiddenStorePathOption())
547: .command('change')
556: .command('show [change-name]')
558: .option('--json', 'Output as JSON')
559: .option('--deltas-only', 'Show only deltas (JSON only)')
560: .option('--requirements-only', 'Alias for --deltas-only (deprecated)')
561: .option('--diff', 'Show per-requirement diffs for delta specs')
562: .option('--no-interactive', 'Disable interactive prompts')
575: .command('list')
577: .option('--json', 'Output as JSON')
578: .option('--long', 'Show id and title with counts')
592: .command('validate [change-name]')
594: .option('--strict', 'Enable strict validation mode')
595: .option('--json', 'Output validation report as JSON')
596: .option('--no-interactive', 'Disable interactive prompts')
614: .command('archive [change-name]')
616: .option('-y, --yes', 'Skip confirmation prompts')
617: .option('--skip-specs', 'Skip spec update operations (useful for infrastructure, tooling, or doc-only changes)')
618: .option('--no-validate', 'Skip validation (not recommended, requires confirmation)')
619: .option('--json', 'Output as JSON (non-interactive)')
620: .option('--store <id>', STORE_OPTION_DESCRIPTION)
621: .addOption(hiddenStorePathOption())
643: .command('validate [item-name]')
645: .option('--all', 'Validate all changes and specs')
646: .option('--changes', 'Validate all changes')
647: .option('--specs', 'Validate all specs')
648: .option('--archived', 'Validate that archived changes have all tasks completed (for pre-commit linting)')
649: .option('--report <full|findings>', 'Select bulk report content: full|findings; combine with --json for JSON')
650: .option('--type <type>', 'Specify item type when ambiguous: change|spec')
651: .option('--strict', 'Enable strict validation mode')
652: .option('--json', 'Output validation results as JSON')
653: .option('--concurrency <n>', 'Max concurrent validations (defaults to env OPENSPEC_CONCURRENCY or 6)')
654: .option('--no-interactive', 'Disable interactive prompts')
655: .option('--store <id>', STORE_OPTION_DESCRIPTION)
656: .addOption(hiddenStorePathOption())
670: .command('show [item-name]')
672: .option('--json', 'Output as JSON')
673: .option('--type <type>', 'Specify item type when ambiguous: change|spec')
674: .option('--no-interactive', 'Disable interactive prompts')
676: .option('--deltas-only', 'Show only deltas (JSON only, change)')
677: .option('--requirements-only', 'Alias for --deltas-only (deprecated, change)')
678: .option('--diff', 'Show per-requirement diffs for delta specs (change)')
680: .option('--requirements', 'JSON only: Show only requirements (exclude scenarios)')
681: .option('--no-scenarios', 'JSON only: Exclude scenario content')
682: .option('-r, --requirement <id>', 'JSON only: Show specific requirement by ID (1-based)')
683: .option('--store <id>', STORE_OPTION_DESCRIPTION)
686: .addOption(hiddenStorePathOption())
702: .command('feedback <message>')
704: .option('--body <text>', 'Detailed description for the feedback')
718: .command('completion')
722: .command('generate [shell]')
736: .command('install [shell]')
738: .option('--verbose', 'Show detailed installation output')
751: .command('uninstall [shell]')
753: .option('-y, --yes', 'Skip confirmation prompts')
767: .command('__complete <type>', { hidden: true })
786: .command('status')
788: .option('--change <id>', 'Change name to show status for')
789: .option('--all', 'Show status for all active changes')
790: .option('--schema <name>', 'Schema override (auto-detected from config.yaml)')
791: .option('--json', 'Output as JSON')
792: .option('--store <id>', STORE_OPTION_DESCRIPTION)
793: .addOption(hiddenStorePathOption())
814: .command('instructions [artifact]')
816: .option('--change <id>', 'Change name')
817: .option('--schema <name>', 'Schema override (auto-detected from config.yaml)')
818: .option('--json', 'Output as JSON')
819: .option('--store <id>', STORE_OPTION_DESCRIPTION)
820: .addOption(hiddenStorePathOption())
841: .command('templates')
843: .option('--schema <name>', `Schema to use (default: ${DEFAULT_SCHEMA})`)
844: .option('--json', 'Output as JSON mapping artifact IDs to template paths')
857: .command('schemas')
859: .option('--json', 'Output as JSON (for agent use)')
860: .option('--store <id>', STORE_OPTION_DESCRIPTION)
861: .addOption(hiddenStorePathOption())
877: const newCmd = program.command('new').description('Create new items');
880: .command('change <name>')
882: .option('--description <text>', 'Description to add to README.md')
883: .option('--goal <text>', 'Optional goal metadata to store with the change')
884: .option('--schema <name>', `Workflow schema to use (default: ${DEFAULT_SCHEMA})`)
885: .option('--json', 'Output as JSON')
886: .option('--store <id>', STORE_OPTION_DESCRIPTION)
887: .addOption(hiddenStorePathOption())
890: .addOption(new Option('--initiative <id>', 'No longer supported').hideHelp())
891: .addOption(new Option('--areas <names>', 'No longer supported').hideHelp())
```

### src/cli/commands/config.ts

```text
10: .command('config')
12: .option('--scope <scope>', 'Config scope (only "global" supported currently)')
23: .command('path')
32: .command('list')
34: .option('--json', 'Output as JSON')
42: .command('get <key>')
51: .command('set <key> <value>')
53: .option('--string', 'Force value to be stored as string')
54: .option('--allow-unknown', 'Allow setting unknown keys')
62: .command('unset <key>')
71: .command('reset')
73: .option('--all', 'Reset all configuration (required)')
74: .option('-y, --yes', 'Skip confirmation prompts')
82: .command('edit')
91: .command('profile [preset]')
```

### src/cli/commands/context.ts

```text
12: .command('context')
14: .option('--store <id>', COMMON_FLAGS.store.description)
15: .addOption(
16: new Option('--store-path <path>', 'Removed; register the store and use --store').hideHelp()
17: )
18: .option('--json', 'Output the agent brief as JSON')
19: .option('--code-workspace <path>', 'Also write a VS Code workspace file for the set')
16: new Option('--store-path <path>', 'Removed; register the store and use --store').hideHelp()
18: .option('--json', 'Output the agent brief as JSON')
19: .option('--code-workspace <path>', 'Also write a VS Code workspace file for the set')
20: .option('--force', 'Overwrite an existing --code-workspace file')
```

### src/cli/commands/doctor.ts

```text
12: .command('doctor')
14: .option('--store <id>', COMMON_FLAGS.store.description)
15: .addOption(
16: new Option('--store-path <path>', 'Removed; register the store and use --store').hideHelp()
17: )
18: .option('--json', 'Output as JSON')
19: .action(async (options: DoctorOptions) => {
16: new Option('--store-path <path>', 'Removed; register the store and use --store').hideHelp()
18: .option('--json', 'Output as JSON')
```

### src/cli/commands/schema.ts

```text
8: .command('schema')
18: .command('which [name]')
20: .option('--json', 'Output as JSON')
21: .option('--all', 'List all schemas with their resolution sources')
29: .command('validate [name]')
31: .option('--json', 'Output as JSON')
32: .option('--verbose', 'Show detailed validation steps')
40: .command('fork <source> [name]')
42: .option('--json', 'Output as JSON')
43: .option('--force', 'Overwrite existing destination')
51: .command('init <name>')
53: .option('--json', 'Output as JSON')
54: .option('--description <text>', 'Schema description')
55: .option('--artifacts <list>', 'Comma-separated artifact IDs (proposal,specs,design,tasks)')
56: .option('--default', 'Set as project default schema')
57: .option('--no-default', 'Do not prompt to set as default')
58: .option('--force', 'Overwrite existing schema')
```

### src/cli/commands/spec.ts

```text
6: .command('spec')
15: .command('show [spec-id]')
17: .option('--json', 'Output as JSON')
18: .option('--requirements', 'JSON only: Show only requirements (exclude scenarios)')
19: .option('--no-scenarios', 'JSON only: Exclude scenario content')
20: .option('-r, --requirement <id>', 'JSON only: Show specific requirement by ID (1-based)')
21: .option('--no-interactive', 'Disable interactive prompts')
28: .command('list')
30: .option('--json', 'Output as JSON')
31: .option('--long', 'Show id and title with counts')
38: .command('validate [spec-id]')
40: .option('--strict', 'Enable strict validation mode')
41: .option('--json', 'Output validation report as JSON')
42: .option('--no-interactive', 'Disable interactive prompts')
```

### src/cli/commands/store.ts

```text
23: const store = program.command('store').description(storeGroupDescription);
26: .command('setup [id]')
28: .option('--path <path>', 'Folder where the store should live (for example ~/openspec/<id>)')
29: .option('--init-git', 'Initialize a Git repository with an initial commit (default)')
30: .option('--no-init-git', 'Skip every Git action: no init, no initial commit')
31: .option('--remote <url>', 'Canonical clone source recorded in store.yaml')
32: .option('--json', 'Output as JSON')
39: .command('register [path]')
41: .option('--id <id>', 'Store id; defaults to metadata or folder name')
42: .option('--yes', 'Confirm creating store identity metadata for a healthy OpenSpec root')
43: .option('--json', 'Output as JSON')
50: .command('unregister <id>')
52: .option('--json', 'Output as JSON')
59: .command('remove <id>')
61: .option('--yes', 'Confirm local store folder deletion')
62: .option('--json', 'Output as JSON')
69: .command('list')
70: .alias('ls')
72: .option('--json', 'Output as JSON')
79: .command('doctor [id]')
81: .option('--json', 'Output as JSON')
```

### src/cli/commands/workset.ts

```text
25: const workset = program.command('workset').description(groupDescription);
29: workset.addOption(new Option('--json', 'Output as JSON').hideHelp());
32: .command('create [name]')
34: .option(
35: '--member <member>',
36: 'Member folder as <path> or <name>=<path>; repeatable, first is the primary',
37: collectMember,
38: [] as string[]
40: .option('--tool <id>', 'Preferred tool to open this workset with')
41: .option('--json', 'Output as JSON')
48: .command('list')
49: .alias('ls')
51: .option('--json', 'Output as JSON')
58: .command('open <name>')
60: .option('--tool <id>', 'Open with this tool just this once')
61: .addOption(
62: // Parsed so Commander never owns the error; rejected in the
63: // action with one JSON document. Hidden because help should not
64: // advertise a mode that only rejects.
65: new Option('--json', 'Not supported for open').hideHelp()
65: new Option('--json', 'Not supported for open').hideHelp()
73: .command('remove <name>')
75: .option('--yes', 'Confirm removal non-interactively')
76: .option('--json', 'Output as JSON')
```

## Formats and compatibility obligations

- Root layout: `openspec/specs/<capability-path>/spec.md`, `openspec/changes/<name>/`, `openspec/changes/archive/<YYYY-MM-DD-name>/`, root `openspec/config.yaml`, per-change `.openspec.yaml`, project-local `openspec/schemas/<name>/schema.yaml` and templates. Schema lookup order is project-local, user override under global data dir, then package built-in (`src/core/artifact-graph/resolver.ts:135`); do not assume a PentaPRO profile can overwrite custom schemas.
- Default schema `schemas/spec-driven/schema.yaml`: proposal → specs/design → tasks; `apply.requires: [tasks]`, task tracking `tasks.md`; specs glob `specs/**/*.md`. An artifact beneath `specs/` is satisfied/skipped when `skip_specs: true`, regardless of its custom ID. Declaration order breaks topological ties.
- Change metadata recognizes `schema`, `created`, `goal`, `affected_areas`, `initiative`, `skip_specs`, `retire_capabilities`; legacy/removed command options can still be parsed to deliver explicit diagnostics. Scope metadata parsing separately from removed CLI workflows.
- Markdown spec grammar includes purpose, requirement and scenario blocks, exact matching of normalized requirement names, closing hash removal, code-fence exclusion, ADDED/MODIFIED/REMOVED/RENAMED deltas and plain task checkboxes. `[x]`, `[X]`, and spacing with only x are completed; other marks are unfinished. Must preserve arbitrary source text and unknown content through controlled edits.
- Project config: schema/context/rules; apply/archive advisory operation guidance; references manually normalized as ID strings or `{id, remote}` maps; default store pointer used only for config-only roots; Copilot cloud preference. Context/reference index caps include 50KB behavior. See `src/core/project-config.ts`, `references.ts`.
- Stores: `.openspec-store/store.yaml` `{version:1,id,remote?}`; `<globalDataDir>/stores/registry.yaml` `{version:1,stores:{id:{backend:{type:"git",local_path,remote?,branch?}}}}`. Git working tree and registry are distinct; unregister preserves folder, remove is destructive and requires confirmation. `src/core/store/foundation.ts`.
- Worksets: `<globalDataDir>/worksets/worksets.yaml` `{version:1,worksets:{name:{tool?,members:[{name,path}]}}}`; generated `<name>.code-workspace`, first member is primary cwd. No project writes; no inferred multi-repository authority. `src/core/worksets.ts`.
- Global data location: explicit XDG_DATA_HOME wins on all platforms; Unix/macOS fallback `~/.local/share/openspec/`, Windows `%LOCALAPPDATA%/openspec/`. Global config is a separate resolution path in `src/core/global-config.ts`; isolate it with environment fixtures.
- Root selection: explicit `--store`; nearest ancestor planning root; config-only declared store; global defaultStore; no-root errors when registered stores exist; implicit cwd only for commands that permit it. `list`, `doctor`, `context`, bulk validation have stricter no-root cases; list retains legacy project.md fallback.
- JSON: preserve actual upstream shape per command, mixed camelCase/snake_case, `root.store_id`, omitted optional keys, diagnostic arrays and command-specific null shapes. `schemas --json` is intentionally a bare array. `archive:null` does NOT establish no mutation; recovery diagnostics require effect inspection.
- Environment: OPENSPEC_TELEMETRY=0, DO_NOT_TRACK=1, OPENSPEC_CONCURRENCY, EDITOR/VISUAL, NO_COLOR, OPENSPEC_NO_ANIMATION, OPENSPEC_NO_COMPLETIONS, OPENSPEC_NO_UPDATE_CHECK, CI, NODE_ENV=test, npm_config_registry; plus XDG/platform home paths and shell/profile vars. Distinguish CLI/JSON functional parity from branded network endpoints and privacy defaults.

## Host integration inventory

Observed tool definitions from `src/core/config.ts` (source is authoritative for actual availability, global-only exceptions, restart notes and aliases):

- `amp`: Amp
- `antigravity`: Antigravity
- `atomcode`: AtomCode
- `auggie`: Auggie (Augment CLI)
- `bob`: IBM Bob
- `claude`: Claude Code
- `cline`: Cline
- `command-code`: Command Code
- `codeartsagent`: CodeArts
- `codex`: Codex
- `dsh`: DeepSeek Harness
- `devin`: Devin Desktop (formerly Windsurf)
- `forgecode`: ForgeCode
- `codebuddy`: CodeBuddy Code (CLI)
- `codestudio`: Code Studio
- `continue`: Continue
- `costrict`: CoStrict
- `crush`: Crush
- `cursor`: Cursor
- `easycode`: EasyCode
- `factory`: Factory Droid
- `gemini`: Gemini CLI
- `github-copilot`: GitHub Copilot
- `gigacode`: GigaCode
- `grok`: Grok Build
- `gsd`: GSD
- `hermes`: Hermes Agent
- `iflow`: iFlow
- `junie`: Junie
- `kilocode`: Kilo Code
- `kimi`: Kimi Code
- `kiro`: Kiro
- `lingma`: Lingma
- `minimax-code`: MiniMax Code
- `vibe`: Mistral Vibe
- `oh-my-pi`: Oh My Pi
- `opencode`: OpenCode
- `pi`: Pi
- `codeassistant`: SourceCraft Code Assistant
- `qoder`: Qoder
- `qwen`: Qwen Code
- `rovodev`: Rovo Dev CLI
- `roocode`: Zoo Code
- `trae`: Trae
- `veai`: Veai
- `warp`: Warp
- `zed`: Zed Agent
- `zcode`: ZCode
- `agents`: Other / Universal (shared .agents skills)

Generated skill names: `openspec-explore`, `openspec-new-change`, `openspec-continue-change`, `openspec-apply-change`, `openspec-update-change`, `openspec-ff-change`, `openspec-sync-specs`, `openspec-archive-change`, `openspec-bulk-archive-change`, `openspec-verify-change`, `openspec-onboard`, `openspec-propose`, `openspec`. Template workflows and skill generation do not execute an AI host. Host rendering must be golden-tested separately from live host loading/model behavior.

Notable host cases: MiniMax Code global-only skills; shared `.agents` target; Devin alias `windsurf` and legacy migration; Copilot IDE prompt files versus cloud coding-agent generation versus CLI; Hermes trust/external directories; skill-only hosts have no slash-command adapter. See `docs/supported-tools.md` and adapter registry.

## Upstream technology and proposed Rust alternatives

| TypeScript role/dependency | Rust proposal | Evidence and selection limits |
|---|---|---|
| commander 14 | clap derive/builder + clap_complete | Primary docs https://docs.rs/clap/latest/clap/ (observed 4.6.10) document help/completions, parser features and maintenance policy. Port flags/diagnostics explicitly; default clap exit/help behavior may differ. |
| zod 4 | serde + typed validation / thiserror; optionally schemars | Serde primary docs https://docs.rs/serde/latest/serde/ (observed 1.0.229) describe typed, reflection-free formats. Serde alone does not implement Zod refinements or preserve unknown YAML comments. |
| yaml 2.8 | maintained serde-compatible YAML implementation after maintenance/security check | Do not casually choose deprecated serde_yaml; loss-aware text edits and source preservation are separate requirements. No candidate selected in this research. |
| @inquirer/core/prompts | dialoguer + console; Ratatui only if dashboard needs it | https://docs.rs/dialoguer/latest/dialoguer/ observed 0.12.0 covers input/confirm/select/multiselect/editor. TTY behavior and Windows must be exercised. |
| chalk / ora | anstream/anstyle or console / indicatif | Common CLI ecosystem candidates; current release cadence/download popularity not measured here. |
| diff 9 | similar | https://docs.rs/similar/latest/similar/ observed 3.2.1 supports diff and merge primitives; semantic spec merging remains custom domain code. |
| tinyglobby / picomatch / brace-expansion | globset + walkdir/ignore | Candidate only; glob semantics, braces, **, separators and dotfiles require differential fixtures. |
| cross-spawn | std::process::Command | Standard library avoids extra shell layer; process cancellation, quoting, PATH and Windows behavior remain explicit controls. |
| skills 1.8.1 | native generated assets/host adapters + controlled package integration | No equivalent general Rust host installer was established. Do not silently depend on Node runtime to claim a standalone Rust binary. |
| Vitest | cargo test + assert_cmd/predicates/tempfile; proptest as needed | Use integration fixture/differential CLI subprocess tests. Cargo built-in harness handles unit tests. Popularity/cadence ranking was not measured, so these are candidates rather than benchmark winners. |
| pnpm/changesets/eslint/TypeScript | Cargo/lockfile/rustfmt/clippy + release CI | Distribution/signing/target smoke tests are separate deliverables. Preserve npm/standalone upgrade compatibility decisions explicitly. |

The chosen minimum foundation should favor the standard library, clap and serde, adding crates only when the next verified capability requires them. Framework popularity, update frequency and performance are three different criteria: this research verified primary documentation for four candidates but did not measure download rankings, execute benchmarks, or select a complete stack.

## Test recovery and parity evidence plan

Observed 250 `*.test.ts` files under `test/`, including unit/component/CLI E2E fixtures. This is a file count, not a test-case count or proof they pass. Relevant suites: `test/cli-e2e/capstone-journeys.test.ts`, `store-lifecycle.test.ts`, `workset-journey.test.ts`, `update-dry-run.test.ts`, `upgrade-from-releases.test.ts`, `validate-*`, `view-store-resolution.test.ts`, `startup-modules.test.ts`; `test/core/artifact-graph`, `parsers`, `store`, `completions`, `command-generation`, `templates`, `shared`; `test/specs`, `test/ui`, `test/telemetry`.

For each OS ID above expand a case matrix from upstream tests: success, empty, invalid arguments/config, malformed metadata, TTY/non-TTY, Unicode, symlink/path traversal, collisions, stale/partial effects, permission failures and recovery, platform paths. Differential test runs must use independent temporary roots and isolated home/XDG directories, compare exit/stdout/stderr plus file trees, and normalize only declared nondeterminism (timestamps, absolute temp roots, own binary/version branding). Do not normalize errors, missing fields or semantic content to make results pass. Compare optional omitted keys and ordering where contractual. Upstream golden/generated assets carry MIT attribution if reused.

The feature table and exact registration inventory recover the full command surface but do not yet constitute an exhaustive atomic behavior-to-fixture catalog. Completing that catalog requires reading each handler and all applicable tests, then running the pinned upstream CLI as oracle. No executed behavioral parity, Rust speed benefit, all-host interoperability or cross-platform guarantee is claimed.
