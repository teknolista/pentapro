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
| [../assets/agents.md](../assets/agents.md) | The project root instruction template formerly maintained at the repository root as `AGENTS-template.md`. Retained for earlier installations that seeded broad project guidance and temporary fields; current setup does not read or copy it. It contains the complete prompt-persistence rule, which is also present in the skill entrypoint so setup does not depend on a separate policy document. |

The files under `../assets/prompt-logging/` and `../assets/prompt-logging.md` are legacy hook implementation materials. The current setup flow does not reference, install, or require them; current setup uses only the self-contained rule in `SKILL.md`.

## Current scope (1.4.0)

The active entrypoint configures only the current project's root `AGENTS.md`, using its own inline prompt-persistence rule. It preserves unrelated instructions, merges one complete logging section, and leaves other files unchanged. It no longer imports instructions through Claude, configures trackers, creates domain documentation, seeds the broad instruction template, interviews for project facts or initializes a specification. The historical templates and logger assets remain for earlier installations and regression checks; they are not setup dependencies.

The prompt rule is original to this collection. It includes timing, prompt and subagent scope, entry format, attribution, attachments, redaction, duplicate verification, append-only local storage, unsafe-target and tracked-log checks, and failure handling. Both setup and the resulting instruction section are self-contained.
