# Sources and adaptation notes

Earlier versions of `setup-pentapro` adapted Matt Pocock's [setup-matt-pocock-skills](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/setup-matt-pocock-skills/SKILL.md) at commit `59db609eb1e18aaf59b63284d0e52255aff0c63c` (2026-10-27), inspected on 2026-11-18 through the public repository. License: MIT, Copyright (c) 2026 Matt Pocock. The upstream source, copyright and permission notice are recorded in the repository [third-party notices](https://github.com/teknolista/skills/blob/main/THIRD-PARTY-NOTICES.md#setup-pentapro); the package ships under the repository [MIT license](../LICENSE).

## Historical adaptations

| Upstream file | Local file | Adaptation |
| --- | --- | --- |
| `SKILL.md` | [SKILL.md](../SKILL.md) | Reworked for this collection. Issue-tracker selection, exploration order, section numbering and the `## Agent skills` root-file block keep the upstream flow. The domain-documentation section is rewritten: glossary/context files move into the PentaPRO PRODUCT pillar (`pentapro/product/domain.md`), decisions into the PROJECT pillar (`pentapro/project/decisions.md`); no root `GLOSSARY.md` / `GLOSSARY-MAP.md` / `docs/adr/` is created. New Section D requires every other finding from setup to be weighed for inclusion in `pentapro/`, defaulting to a question to the developer when ownership is unclear. The collection context (this skill is the first skill run in a project, and it hands off to `$penta-pro`) is stated in the description and README. |
| `issue-tracker-github.md` | [../assets/issue-tracker-github.md](../assets/issue-tracker-github.md) | Retargeted attribution line from `mattpocock/skills` to `teknolista/skills`. The tracker conventions (GitHub issues, native dependencies, `wayfinder` operations) are kept; the `wayfinder` procedures are annotated for projects that also install the upstream `wayfinder` skill, since this collection does not ship one. |
| `issue-tracker-gitlab.md` | [../assets/issue-tracker-gitlab.md](../assets/issue-tracker-gitlab.md) | Same attribution retarget; `wayfinder` operations annotated the same way. |
| `issue-tracker-local.md` | [../assets/issue-tracker-local.md](../assets/issue-tracker-local.md) | Kept essentially as-is; `wayfinder` annotated the same way. |
| `triage-labels.md` | [../assets/triage-labels.md](../assets/triage-labels.md) | Header retargeted. This collection ships no `triage` skill, so the template is retained only for projects that install upstream `triage`; Section B of `SKILL.md` normally skips itself. |
| `domain.md` | [../assets/domain.md](../assets/domain.md) | Rewritten for the five-pillar layout. Glossary and decision records live in `pentapro/` (PRODUCT / PROJECT); multi-context keeps one specification with a PRODUCT context map pointing to per-context term files. The upstream "proceed silently", vocabulary-use and ADR-conflict rules are retained against the pillar paths. |

Not adaptable as-is: the upstream `disable-model-invocation: true` flag is not used; this collection selects skills by description and explicit invocation.

## Original assets

These files are original to this collection, not adaptations of the upstream package:

| Local file | Origin and purpose |
| --- | --- |
| [../assets/agents.md](../assets/agents.md) | The project root instruction template formerly maintained at the repository root as `AGENTS-template.md`. Used as an adaptable template for new project guidance or an explicitly requested broader setup; existing instructions remain authoritative. It contains the complete prompt-persistence rule, which is also present in the skill entrypoint so setup does not depend on a separate policy document. |

The files under `../assets/prompt-logging/` and `../assets/prompt-logging.md` are legacy hook implementation materials. The current setup flow does not reference, install, or require them; prompt logging uses the self-contained rule in `SKILL.md`.

## Current scope

Full setup includes purpose-driven README and license choices, issue-tracker selection, optional triage mappings, domain-document guidance, the project instruction template, project-fact assessment and an appropriate PentaPRO handoff. The complete prompt rule remains inline in the entrypoint. Repository setup details are in [repository-setup.md](repository-setup.md). Existing authoritative domain records are preserved unless migration is authorized; external tracker writes require actual authorization. A narrower user request remains narrow. The original hook implementation and host recipes are retained as legacy assets and are not installed by setup.

The change reverses the entrypoint narrowing in commit `5fe20c9` while adapting upstream behavior to current project authority, existing records and the collection's owners. It does not copy the upstream mandatory confirmation workflow, or assume all consumer skills are installed. The upstream MIT notice is included in [the package's third-party notices](../THIRD-PARTY-NOTICES.md).

Version 1.6 adds original project-local factory role templates and the [factory setup procedure](factory-setup.md). Their Codex format follows the [custom agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents); native setup now uses the PentaPRO-owned change lifecycle. Model choices are editable project defaults, not availability guarantees. The repository's pilot record documents failed custom-role invocation and the manual-capture correction in 1.6.1; neither templates nor schema tests prove runtime discovery.

## Native SDD transition — 2026-11-22

The native change workflow adapts ideas from [OpenSpec](https://github.com/Fission-AI/OpenSpec) and its workflow skills as implementation references. The earlier store-aware guidance is historical and no longer governs setup; no upstream utility is installed or required. Preserve attribution and applicable licensing.

## README and project licensing — 2026-11-20

The maintainer supplied `/home/dever/workspace/teknolista/readme.md` as the project README template. The packaged `assets/readme.md.template` preserved the original bytes at introduction (SHA-256 `f700c6520149fe5bf9ff73297c06ec6d2536b987ddf41192a92f373b942ea917`). The closing review removed one trailing space to pass the repository whitespace check (closing-review SHA-256 at that checkpoint `90968bf6eb7fc874f341e10675f6eb4d604f377b52d87211d3cefa97ef9aca58`); template examples are adapted to verified target-project facts. This is maintainer-supplied material, not attributed to the Matt Pocock adaptation. GitHub's [license API documentation](https://docs.github.com/en/rest/licenses/licenses) defines current choice discovery and canonical license-body retrieval. No external license text is bundled as a target-project default; the developer selects the license. README language and replace/complement/skip choices are required independently of the collection's English-artifact convention.

## Cross-host role identity and closing maintenance — 2026-11-21

The [OpenCode agent documentation](https://opencode.ai/docs/agents/) defines path-derived agent IDs. [Claude Code](https://code.claude.com/docs/en/sub-agents) uses `name` in frontmatter; [Copilot](https://docs.github.com/en/copilot/reference/custom-agents-configuration) documents profile identity and environment differences; [Antigravity](https://antigravity.google/docs/subagents) defines custom names, explicit tools and model tiers. Setup records the actual discovered mapping and missing capabilities rather than claiming universal alias or model support. Offline adapter validation is not an executed host integration test.

## PentaPRO plugin packaging — 2026-11-21

PentaPRO is the collection identity; setup remains project-scoped regardless of package scope. Resolve the plugin-qualified installed skill and the target checkout separately, preserving generated project records through package updates. Root package metadata and per-host adapters do not change the complete prompt rule or install hooks.

Setup PentaPRO 2.2.0 adds the maintainer-requested motivational experiment note to the README template and per-run invocation-history guidance to factory assets. Earlier template hashes above describe historical checkpoints, not the modified current file.

## Installed-profile diagnostics — 2.3.0

The developer-requested harness review added an optional read-only profile comparator, safe refresh guidance and explicit preservation of custom model/effort/host settings. Templates retain their existing role contracts. The helper does not establish native discovery, enforce permissions or overwrite installed profiles.
