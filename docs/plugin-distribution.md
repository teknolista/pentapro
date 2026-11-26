# PentaPRO plugin distribution

PentaPRO is the collection/plugin brand and `pentapro` its machine ID. the repository is `teknolista/pentapro`; existing skill IDs (including `penta-pro`) remain unchanged; source directories are now under `skills/`. The aggregate plugin started at version 1.0.0; bundle 1.1.0 added execution-state resources and bundle 1.1.1 reconciled role invocation and model-choice guidance, and bundle 1.2.0 added Cursor role templates and bundle 2.0.0 adopted native PentaPRO SDD and bundle 2.0.1 corrects setup/closure guidance, and bundle 2.1.0 adds Git defaults and the permanent motivational manifesto, and bundle 2.2.0 added per-run factory invocation history and the current 2.3.0 candidate adds read-only installed-profile diagnostics and safe refresh guidance; each skill retains its own version. Plugin versioning describes a bundle release, not a claim that every skill changed.

## Ownership and formats

`plugin.json` owns package identity, version and the explicit list of all source skill directories. `scripts/package_plugin.py --sync` generates the Codex compatibility manifest, Antigravity overlay, Copilot/compatibility marketplace catalogs, OpenCode package metadata and skill catalog. `--check` fails on drift and is a CI gate. The explicit compatibility paths avoid moving the established packages or committing duplicate `SKILL.md` trees. The root manifest intentionally uses the supported legacy path-based format, not the fixed `skills/` semantics of Agent Plugins 1.0. Do not add the portable schema URL without deliberately migrating the layout and discovery checks.

| Host | Source entrypoint | Project-local adoption |
| --- | --- | --- |
| Codex | `.codex-plugin/plugin.json`, compatibility marketplace `.claude-plugin/marketplace.json` | Export bundle, merge repo marketplace and trusted-project config, then install through the host; inspect user enable choices and cache scope. |
| GitHub Copilot CLI | Legacy root `plugin.json`, `.github/plugin/marketplace.json` | Export bundle and launch with `--plugin-dir`; user-wide `plugin install` is optional. |
| OpenCode V2 | `package.json` default export `plugin/opencode.mjs` | Project `plugins` entry; adapter adds skills through `skill.transform`, preserving existing IDs and disposing its own registration. |
| Antigravity CLI | `.antigravity-plugin/plugin.json` in source; root manifest in clean export | Export to the target project's `.agents/plugins/pentapro`; no global installation required. |

The OpenCode adapter is dependency-free JavaScript in the documented `{ id, setup }` module shape. Its only effect is registration of the installed skill catalog. It performs no model request, hook registration, credential access or filesystem write. Skills keep their real source paths for loading adjacent resources. The adapter preserves an already registered skill with the same ID; mixed installations should still be reconciled explicitly instead of relying on that priority.

Agent definitions remain template assets within setup-pentapro. Plugins do not auto-register the six agents globally or impose their model choices on every project. Running setup in the target checkout creates only missing selected-host agents, protocol and lessons files, with current checks and preservation rules. Plugin cache, source checkout and target project are separate locations. Use the actually registered namespaced skill IDs where required; do not create forwarding copies to hide a namespace.

## Export, update and removal

Use the README's [installation recipes](../README.md#install-pentapro). Export uses Git's eligible working-tree inventory inside skill packages, includes their resources and licenses, and excludes ignored files, local prompt logs, project lesson history and root maintainer instructions. It refuses package symlinks, non-regular sources, existing destinations, substituted output parents and output inside the source checkout. Inputs are preflighted before a staged export is renamed into place. A `bundle-files.json` SHA-256 inventory binds the output to exact contents. It is integrity evidence, not a publisher signature or proof of safe behavior.

For a local update, export to a new versioned directory, inspect the diff/checks and switch the project's plugin path or marketplace entry deliberately. Keep customized project agents/lessons and index selections. No blanket force overwrite is provided. A bundle cannot update project-generated documents by overwriting them; rerun setup and reconcile conflicts when appropriate. Removing/deactivating a plugin affects future skill availability; it does not delete project guidance, agents or lessons. Preserve those or remove them under a separate explicit cleanup request.

User-wide installation requires no changes to skill procedures: resources resolve from the installed package, while project facts remain in the checkout. It can affect many repositories after an update, shadow project copies or expose duplicate names. Choose the smallest scope, pin/review updates as appropriate, and confirm registered paths. Do not share lesson or prompt data globally merely because skills are globally available. Hosts may cache plugin bytes in user storage even with project-only activation. The skills CLI's default project copy route is the alternative when local file placement is required.

Never install both routes for the same host without inspecting effective discovery. No npm publication, release upload, global config mutation or official marketplace submission is performed by the package/export helpers. The root npm metadata is private; OpenCode uses a Git/local package source. Publishing to a registry or store is a separate task.

## Validation record — 2026-11-21

- Cached `skills` CLI 1.9.0 discovered exactly 24 skills and installed all 24 as project-local copies for `codex`, `github-copilot`, `opencode` and `antigravity-cli` in separate disposable projects. Telemetry was disabled. This exercised the same CLI entrypoint used by npx, without downloading or installing dependencies globally.
- Ten offline packaging controls cover all four exports, byte/resource/license retention, preservation of existing destinations, path containment, ignored synthetic secrets, required-resource inventory, auxiliary symlink refusal, stale catalog rejection and reproducibility. Two optional native tests additionally validate Antigravity and Codex discovery when their CLIs are present.
- Antigravity CLI 1.5.13 strict native validation passed for the clean export with 24 skills and zero hooks. The full multi-tool source checkout has expected warnings about the inactive root maintainer AGENTS.md and overlay precedence; export provides the clean validation target.
- Codex CLI 0.160.0 discovered `pentapro@teknolista` from the source marketplace and the exported bundle from an explicitly configured temporary local marketplace. It was not installed into the developer's user cache and no model was invoked. Explicit marketplace configuration was necessary for this installed client; a catalog file alone did not make it available.
- Four Node adapter tests exercise real skill loading, preservation/disposal, an unsupported API and invalid/duplicate paths. No external SDK is needed for these offline tests.
- OpenCode 2.0.31's runtime registry stayed empty for both PentaPRO and a minimal JavaScript control, using explicit project config and automatic `.opencode/plugins` discovery. An empty session and an explicit deep-object `location[directory]` API query did not change that result. The scoped private server was terminated after each attempt. Native runtime success is not claimed; use the skills CLI fallback until the target client's plugin API/discovery is validated.
- The Copilot command on this host is a launcher without an installed Copilot CLI. Copilot native install remains unexecuted; the shipped manifest follows its documented legacy format. No user-wide installation or automatic update was performed for any host.

The maintenance run passed 106 Python tests (including the two native probes) and 47 Node tests, the 24-skill collection/link validator, metadata freshness and 15 evaluation-case checks. These ran with Python 3.12.6 and Node.js 27.0.0-alpha.0.0.0 rather than the CI Node.js 24 runtime; CI execution remains pending publication. No live model-based setup or shipping trial was run.

Run the full README/CI offline suite after source/package changes. `package_plugin.py --check` guards metadata freshness; existing collection checks guard links, versions and standalone skill portability. Optional native probes are not a six-host workflow trial, a PDSA effectiveness benchmark, or a security certification.

## Primary format references

- [Codex packaging and marketplaces](https://developers.openai.com/plugins/build/plugins), [configuration keys](https://learn.chatgpt.com/docs/config-file/config-reference).
- [Copilot plugin manifest, commands and locations](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).
- [OpenCode plugin packaging](https://opencode.ai/docs/build/plugins/), [skill transforms](https://opencode.ai/docs/build/plugins/server/#skills).
- [Antigravity build and validation](https://antigravity.google/docs/build-plugins), [installation scopes](https://antigravity.google/docs/plugins).
- [Skills installer reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

Documentation and client versions can diverge. Check the installed version and actual discovery at adoption; report gaps instead of substituting an unsupported manifest, skill or model.


## Execution-state resources in bundle 1.1.0

Software Factory 0.5.0 includes its package-local run helper and format reference; Setup PentaPRO 1.10.0 includes the run directory guide and host pointers. These are ordinary skill resources, distributed through each existing route without host API changes. No active execution is created at install time. Existing customized projects need reviewed reconciliation rather than automatic replacement. The [persistence validation record](factory-run-persistence.md) covers the new offline controls; the native installation observations above retain their original snapshot and limitations.

## Native SDD bundle 2.0.0

The bundle keeps 24 source skills and six specialist roles for six hosts. The host main session guides exploration and delegates the native change lifecycle. Setup PentaPRO 2.0.0, PentaPRO 4.0.0, Software Delivery 2.0.0 Software Factory 1.0.0 and UI Design 2.0.0 use fixed five-dimensional change records and the default single result-approval gate. No additional SDD executable, schema installation, global agent configuration or automatic project migration is part of packaging. Existing customized projects need reviewed reconciliation and preservation of their historical records; plugin updates do not overwrite them. See the [migration guide](native-sdd-migration.md).

## Guidance follow-up 2.0.1

The pre-existing local setup-reference heading typo was removed; the published heading was already correct, so Setup PentaPRO remains 2.0.0. Software Factory 1.0.1 clarifies current resume guidance versus historical archive checkpoint instructions. The README specification-only example writes the six active-change files and preserves the baseline until result approval. No agent model, effort, package inventory or helper runtime changes. Earlier versioned observations above retain their original scope.

## Initialization defaults 2.1.0

Setup PentaPRO 2.1.0 merges bundled Git defaults into root `.gitignore` and `.gitattributes`, preserving existing rules and avoiding duplicate additions. Full setup requires the complete permanent motivational manifesto near the beginning of root `AGENTS.md`, including existing instruction files. Editable READMEs receive an experiment note. PentaPRO 4.0.1 preserves the manifesto during template reconciliation. Narrowly scoped requests keep their scope. Updating the plugin alone does not rewrite existing projects; rerun full setup to adopt these outputs. Package inventory and factory role settings are unchanged. Offline helper checks do not measure the motivational experiment's effect on model decisions.

## Invocation history 2.2.0

Software Factory 1.1.0 adds a separate versioned invocation-event ledger and per-run summary helper alongside unchanged run.json schema 1. Setup PentaPRO 2.2.0 and all six-host role assets carry run reuse, invocation identity and orchestrator-only event guidance. Existing projects reconcile guidance while preserving histories and custom role settings; plugin installation/update alone does not rewrite projects. Git defaults and the permanent manifesto remain part of full setup. No hooks, global settings, automatic deletion or model-selection change is included. Native capture completeness and efficiency improvements require separate evidence.

## Installed-profile diagnostics 2.3.0

Setup PentaPRO 2.3.0 adds an optional package-local read-only checker and a reviewed refresh procedure. Matching workflow bodies and custom host metadata are separate outcomes; custom bodies require review and are never deleted or automatically overwritten. Current host syntax/discovery and actual model selection remain separate checks. The bundle also improves sampled scenario coverage and optional SDK smoke diagnostics. No new host, runtime permission or model policy is introduced. These source changes are not published merely by regenerating metadata.

## Receipt closeout bundle 3.1.0

Git Ship 2.2.0, Software Factory 1.3.0 and Setup PentaPRO 2.5.0 coordinate one optional administrative receipt commit after primary delivery. The parent orchestrator owns this stage and freezes its tracked records afterward, using external refs/CI/conversation for the final confirmation. The source validate job has an actual-diff receipt lane; source/mixed changes retain full checks. The packaged checker supports staged local validation and committed CI validation without installing dependencies or executing record text. Read the [bounded procedure](../skills/software-factory/references/delivery-closeout.md). No consumer workflow, global setting or customized local role is updated automatically. Hosted adoption and publication remain separately observed effects.
