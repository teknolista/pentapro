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

The full setup again includes issue-tracker selection, optional triage mappings, domain-document guidance, the project instruction template, project-fact assessment and an appropriate PentaPRO handoff. The complete prompt rule remains inline in the entrypoint. Repository setup details are in [repository-setup.md](repository-setup.md). Existing authoritative domain records are preserved unless migration is authorized; external tracker writes require actual authorization. A narrower user request remains narrow. The original hook implementation and host recipes are retained as legacy assets and are not installed by setup.

The change reverses the entrypoint narrowing in commit `5fe20c9` while adapting upstream behavior to current project authority, existing records and the collection's owners. It does not copy the upstream mandatory confirmation workflow, or assume all consumer skills are installed. The upstream MIT notice is included in [the package's third-party notices](../THIRD-PARTY-NOTICES.md).

Version 1.6 adds original project-local factory role templates and the [factory setup procedure](factory-setup.md). Their Codex format follows the [custom agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents); OpenSpec setup follows its [project setup documentation](https://openspec.dev/docs/setup), with version-specific checks before execution. Model choices are editable project defaults, not availability guarantees. The repository's pilot record documents failed custom-role invocation and the manual-capture correction in 1.6.1; neither templates nor schema tests prove runtime discovery.
