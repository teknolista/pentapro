---
name: setup-pentapro
description: "Configure this repository for the teknolista skills: choose the issue tracker and domain documentation layout, initialize AGENTS.md with the complete prompt-persistence rule, and decide which project facts belong in the PentaPRO specification. Recommended once per new project before the collection's coordinated workflows."
license: MIT
metadata:
  version: "1.3.0"
---

# Setup PentaPRO

Scaffold the per-repository configuration that the teknolista skills expect. This is the **first skill to run in a new project**. It records the issue tracker and the domain documentation layout, configures the complete prompt-persistence rule in the root `AGENTS.md`, and — when the developer approves — records the project facts that belong in the `pentapro/` specification. Skills that coordinate through the tracker read this configuration.

Explore, present what you found, confirm with the user, then write.

The agent running this skill must apply the prompt-persistence rule in Section E immediately, starting with the prompt that invoked setup. Make logging or verification the first tool operation, allowing only the repository-location and log-safety checks needed for it; defer general exploration. If automatic capture already recorded it, verify the current entry instead of duplicating it. Stop and report if the append fails.

## Process

### 1. Explore

Look at the current repository to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Which sections does it already carry? Does `CLAUDE.md` already import `AGENTS.md`? Is the packaged template's `Setup status: temporary` marker or an `## Agent skills` block present?
- Prompt-logging state: whether `AGENTS.log` exists and whether `.gitignore` already excludes `AGENTS.log` and `AGENTS.log.*`, and whether `git ls-files -- AGENTS.log 'AGENTS.log.*'` reports tracked logs. Preserve its existing entries; access only the current entry when needed to verify automatic capture under Section E.
- Root `GLOSSARY.md`, `GLOSSARY-MAP.md`, `CONTEXT.md`, and `CONTEXT-MAP.md`: glossary/context-file conventions used by other collections. If any exist, note them; Section C offers to migrate them into the PentaPRO specification.
- `pentapro/` and `pentapro/product/domain.md`: does a five-pillar specification exist, and are domain terms already recorded in PRODUCT?
- `docs/adr/` and any `src/*/docs/adr/` directories (legacy architecture decision records)
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: a sign that a local-markdown issue-tracker convention is already in use
- Is a `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Their absence means single-context, which is almost every repo.
- Project facts for Section D: the root `README`, package/build manifests and lockfiles, CI workflows, existing docs, and the build/test commands the project already uses.

### 2. Present findings and ask

Summarise what's present and what's missing. If `docs/agents/` already exists, this is a re-run: show the current configuration and change only what the user asks for. Otherwise, take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip a section entirely when exploration already settled it (Section B when no `triage` skill is installed), and take Section C's single-context default without a question when no monorepo signal or legacy glossary/ADR tree exists.

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. The collection's coordination skills (Software Delivery, Git Ship, Peer Review, PR Quiz) need to know whether to call `gh issue create`, `glab issue create`, write a markdown file under `.scratch/`, or follow another workflow. Pick the place you actually track work for this repo.

Default posture: propose GitHub when a `git remote` points at GitHub, GitLab (`gitlab.com` or a self-hosted host) when it points at GitLab. Otherwise, or if the user prefers, offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`, using the matching seed template from this skill folder. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

A GitHub or GitLab tracker needs a reachable repo. When the user picks one and no `git remote` points at that host, get the repo URL from them and wire it up (`git init` if needed, `git remote add origin <url>`) before going further. Done when `gh repo view` / `glab repo view` prints the project from inside this directory; if it can't, stop and tell the user what's missing.

**Section B: Triage label vocabulary.** Skip this section entirely unless the `triage` skill is installed; without one, omit this section and the `### Triage labels` block of the root instruction file.

When a `triage` skill is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is into `docs/agents/triage-labels.md` (the seed template ships in this skill folder). Only if the user says no, usually because the tracker already uses other names (for example `bug:triage` for `needs-triage`), collect the overrides so the installed `triage` skill applies existing labels instead of creating duplicates.

When Section B runs on GitHub or GitLab, create each configured label the tracker lacks (`gh label create` / `glab label create`).

**Section C: Domain docs.** The collection keeps the domain glossary and decision records inside the PentaPRO specification — never loose at the repository root. The glossary is PRODUCT material; decision records are PROJECT material. Do not create root-level `GLOSSARY.md`, `GLOSSARY-MAP.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, or a parallel `docs/adr/` tree; if they already exist, decide their disposition with the user in this section.

If no `pentapro/` directory exists yet, ask whether to initialize it now:

> Initialize the PentaPRO specification skeleton now? (recommended: **yes** — `$penta-pro` fills and maintains it later)

Run the initializer in step 4, once the user authorizes it; it never overwrites existing files and fills the pillar topic files with `Pending` markers. If the installed `penta-pro` package is not available, recommend installing it or defer, and record the deferred facts as described in Section D. If the user prefers to defer, record the approved setup facts in `docs/agents/setup-notes.md` during Section D; the first `$penta-pro` pass should absorb them into the five pillars.

Then decide the domain-document layout:

- **Single-context** (most repositories): the glossary lives at `pentapro/product/domain.md`; decision records live at `pentapro/project/decisions.md`. Write `docs/agents/domain.md` from the seed template in this skill folder without further questions.
- **Multi-context** (monorepo signals found): one PentaPRO specification covers the repository. `pentapro/product/domain.md` carries a context map linking per-context term files under `pentapro/product/` (for example `domain-<context>.md`), one per bounded context. Decisions stay in `pentapro/project/decisions.md` with context-scoped IDs. Confirm the layout with the user after presenting the monorepo signals; do not fork into per-package spec trees.
- **Legacy migration**: if exploration found root `GLOSSARY.md`, `GLOSSARY-MAP.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, or similar, propose moving the content to its five-pillar home with `git mv` plus a link to the new location — never a silent deletion and never two copies. Keep decision IDs and inbound links; merge records into `pentapro/project/decisions.md`, or keep one file per record under `pentapro/project/decisions/` indexed from it, when the project already works that way. Show the exact list of files to move and ask for confirmation, then update links in the root instruction file and affected records. When two files describe the same term differently, surface the conflict and ask which wins; record the resolution with provenance.

**Section D: Other project facts.**

Everything else exploration raised — stack and toolchain, build and test commands, repository conventions, constraints, known decisions — must be assessed individually: either it belongs in the PentaPRO specification (saved under `pentapro/`), or it belongs in the root instruction file or `docs/agents/`, or it is not worth recording. Do not write project facts into the root instruction file just because they were convenient, and never dump unassessed notes into the specification.

For each candidate fact, decide by pillar ownership:

| Finding | Specification home | If not specification material |
| --- | --- | --- |
| Domain terms, users, journeys, value, scope boundaries, acceptance criteria | PRODUCT (`pentapro/product/`, normally `domain.md` for terms) | Root instruction file only if every agent must read it |
| Stack, architecture, dependencies, contracts, architecture decisions | PROJECT (`pentapro/project/`) | Same |
| Environments, deployment, migration, operations, support | PRODUCTION (`pentapro/production/`) | Same, plus command notes in the root instruction file |
| Verification commands, checks, acceptance evidence plans | PROOF (`pentapro/proof/`) | Environment and commands table in the root instruction file (concrete commands agents can actually run) |
| Tasks, processes, authority, ownership, escalation | PROCESS (`pentapro/process/`) | Root instruction file authority sections |
| Repository mission, short navigation notes | Not specification by itself | Root instruction file |

Rules:

- When in doubt about whether a fact belongs in `pentapro/`, **ask the developer and let them decide**. Do not pre-fill the specification with assumptions. The user's answers are the source; record items you inferred as `Proposed`, not `Confirmed`, marked with the evidence used.
- Never overwrite existing specification content. When writing into a pillar file, preserve stable IDs and prior entries, merge new entries in labelled `Confirmed` / `Proposed` / `Pending` states, and add a source locator (file, command, date, or the answer in this interview).
- Domain terms go to `pentapro/product/domain.md` even when the rest of the specification is not drafted yet, once the user approves them.
- If `pentapro/` was declined in this setup, record the gathered facts in `docs/agents/setup-notes.md` (short, factual, with sources and dates) and state that the first `$penta-pro` run should absorb them into the five pillars. Never leave gathered facts only in the conversation.
- Record configuration names only, never secret values.

**Section E: Root instructions and prompt logging.**

`AGENTS.md` is the canonical, self-contained instruction for prompt persistence. The entire operational rule must be in that file; do not make it depend on another policy document, a hook, or a global agent configuration.

- **Choose the file:** edit `AGENTS.md` when it exists; otherwise create it from [agents.md](assets/agents.md). Do this even when `CLAUDE.md` already exists. If `CLAUDE.md` exists, preserve its content and add `@AGENTS.md` on its own line unless it already imports `AGENTS.md`, so Claude Code loads the complete rule without duplicating it.
- **Existing `AGENTS.md`:** preserve the user's content. Add or update one `## Prompt Logging` section in place; do not duplicate the heading or replace project-specific rules with template prose. The final section must be complete and self-contained as specified below.
- **New file:** fill the rows and commands repository exploration proved — purpose, stack, repository map, installed skill locations, verification commands — remove rows the evidence proves inapplicable, and leave genuinely unknown ones as `[FILL IN]`.
- **Temporary status:** keep the template's setup marker while any material `[FILL IN]` or unverified template section remains. `$penta-pro` reconciles the file after the specification exists.

Prompt logging is mandatory. Put the complete rule below in `AGENTS.md`; it is also the source text for the `## Prompt Logging` section in the packaged root template. Do not replace it with a link or a summary.

~~~markdown
## Prompt Logging

Before analyzing, responding to, or taking any action on a prompt for this repository, append one entry containing that prompt to `AGENTS.log` at the repository root. The first tool operation may locate the repository, check the log target, and append this entry or verify capture; defer other tool use and delegation until logging succeeds. This applies to every prompt, including prompts sent to subagents. Record each received prompt once, including repeated identical submissions; verify automatic capture using the current event identity or other reliable capture evidence, not text equality alone. If verification requires log access, inspect only the relevant current entry without exposing prior prompts. If capture cannot be verified, stop and report the uncertainty before risking a duplicate or an omitted entry.

Use RFC 5322 local time with a numeric UTC offset, the provider/model, and the receiving agent and host. Use `unknown` for unavailable attribution; if the host is known but the model is not, use `<host>/unknown`. Keep one blank line between entries:

```text
## <RFC 5322 local date and time with numeric UTC offset> | <provider>/<model> (agent <agent name>, host <host>)
<prompt text, preserving its wording, spacing, and line breaks; use [empty prompt] if empty>
[attachment: <filename, at its position in the prompt>]
```

Include attachment names at their position in the prompt; do not copy binary contents. Preserve the prompt text except that secrets and unnecessary personal data must be replaced with `[REDACTED]` before writing. Never put credentials in prompts. Redact common patterns such as PEM private keys, `sk-`/`rk-`/`pk-` keys, `ghp_`/`github_pat_` tokens, `AKIA` and `AIza` keys, `xox*` tokens, JWTs, `Bearer` values, and values after `password`, `passwd`, `senha`, `token`, `secret`, or `api_key`. Redaction is best-effort; it does not identify every secret or personal-data format. If a secret reaches the log, revoke it; deleting the local copy is not sufficient.

Before appending, check the Git index for `AGENTS.log` and `AGENTS.log.*`; if any are tracked or staged, stop and report the privacy conflict. Ignore patterns alone do not untrack files; preserve local data and existing index selections until authorized remediation. Create the log with owner-only permissions where supported. Refuse symlink, hard-linked, or non-regular log targets; stop rather than redirecting prompt text. Append only. Never rewrite, reorder, or delete existing entries. Concurrent entries may not be in chronological order; do not reorder them. The log has no automatic rotation; never truncate it. Keep it local; never commit or publish it. Do not send a success message just for logging. If appending fails, stop, report the failure, fix the write, and record the pending prompt before continuing. Never proceed as if logging succeeded when it did not. This instruction depends on agent compliance and is not mechanical enforcement.
~~~

- Ensure `.gitignore` excludes `AGENTS.log` and `AGENTS.log.*`, preserving existing entries; the log must not be committed.
- Do not install or configure hooks, plugins, slash commands, or global agent settings as part of this skill. The rule is enforced by the instruction every agent receives; do not claim that it provides mechanical enforcement.

### 3. Confirm and edit

Show the user a draft of:

- the `## Agent skills` block to add to `AGENTS.md`
- the root instruction change: which template sections will be added, which fields exploration can already fill, and where the temporary marker stays
- the complete `## Prompt Logging` section to add to `AGENTS.md`, the `@AGENTS.md` import to add to an existing `CLAUDE.md`, and the `AGENTS.log*` ignore entries
- the contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/triage-labels.md` (the last only when Section B ran), and `docs/agents/setup-notes.md` (only when facts were gathered and `pentapro/` was declined)
- the exact facts proposed for `pentapro/`, grouped by target pillar file, so nothing is written before the user approves the list

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- Edit the root `AGENTS.md` if it exists; otherwise create it from [assets/agents.md](assets/agents.md).
- If a root `CLAUDE.md` exists, preserve its content and add `@AGENTS.md` on its own line unless it already imports `AGENTS.md`.
- Do not create or replace `CLAUDE.md` as part of this setup.

**Merge the root instruction template.** For a new `AGENTS.md`, start from [assets/agents.md](assets/agents.md) and fill the fields exploration confirmed. For an existing file, add only the template sections it lacks, and add or update the `## Prompt Logging` and `## Agent skills` blocks in place. Keep the temporary setup marker while material fields remain unfilled. Do not overwrite, reorder, or replace user-authored sections with template prose. The `## Prompt Logging` section must contain the complete rule above, without references to other policy files.

If an `## Agent skills` block already exists in `AGENTS.md`, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

~~~
## Agent skills

### Issue tracker

Issues for this project live in [one-line summary, for example: GitHub Issues in this repository]. Read `docs/agents/issue-tracker.md` before creating, reading, labeling, or closing a ticket.

### Domain docs

[one-line summary: "single-context PRODUCT glossary" or "multi-context with a PRODUCT context map"]. See `docs/agents/domain.md`. The glossary lives in `pentapro/product/domain.md`; decision records live in `pentapro/project/decisions.md`.

### Repository setup

Agent setup is complete. The other collection skills read `docs/agents/*.md`; `$penta-pro` creates or resumes the `pentapro/` specification. Next step: run `$penta-pro` to introduce the software; when `docs/agents/setup-notes.md` exists, read and reconcile its deferred facts first. `$setup-pentapro` (already run once for this repository) is not needed again unless the issue tracker or the domain layout changes.
~~~

Include the `### Triage labels` sub-block, linking to `docs/agents/triage-labels.md`, only when Section B ran; otherwise both are omitted.

Then write the files, using the seed templates in this skill folder as a starting point:

- [assets/issue-tracker-github.md](assets/issue-tracker-github.md): GitHub issue tracker
- [assets/issue-tracker-gitlab.md](assets/issue-tracker-gitlab.md): GitLab issue tracker
- [assets/issue-tracker-local.md](assets/issue-tracker-local.md): local-markdown issue tracker
- [assets/triage-labels.md](assets/triage-labels.md): label mapping (only if Section B ran)
- [assets/domain.md](assets/domain.md): domain documentation consumer rules and layout
- [assets/agents.md](assets/agents.md): root instruction template

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

**Enable prompt logging.** Immediately after writing `AGENTS.md`, ensure its `## Prompt Logging` section contains the full rule above, and ensure `.gitignore` lists `AGENTS.log` and `AGENTS.log.*`, preserving existing entries. If `CLAUDE.md` exists, verify that it imports `AGENTS.md`. Do not create a policy document elsewhere or configure any hook, plugin, slash command, or global agent setting.

If Section B ran on GitHub or GitLab, create each configured label the tracker lacks (`gh label create` / `glab label create`).

If the user authorized initializing the PentaPRO skeleton, run the initializer now, before writing approved Section D facts into pillar files:

```sh
python3 <installed penta-pro path>/scripts/init_pentapro.py <repository root>
# For example, in a project using .agents/skills:
python3 .agents/skills/penta-pro/scripts/init_pentapro.py .
```

The initializer never overwrites existing files. If it is missing or fails, report the exact failure, preserve any partial output, and defer approved facts to `docs/agents/setup-notes.md` with their status, sources and dates; do not create the pillar files by hand as a substitute. Continue independent setup steps and report initialization as incomplete.

Only after successful initialization, or when using a pre-existing specification with the required pillar files, write the approved Section D facts into their pillar files. If initialization was declined or failed in this run, keep those facts in `docs/agents/setup-notes.md` instead, even if partial pillar files exist. Preserve existing content, stable IDs and prior provenance; merge the new entries with their `Confirmed` / `Proposed` / `Pending` labels and sources. Rewrite the initializer's `Pending` guidance only where a fact replaced it; leave the rest for the first `$penta-pro` pass.

### 5. Done

Report completed steps and any incomplete initialization, tracker or logging prerequisite; claim setup complete only when required steps succeeded:

- what was written under `docs/agents/` and what was written into `pentapro/` (or where deferred facts were noted)
- that `AGENTS.md` was created or updated with the complete, self-contained prompt rule, which fields remain `[FILL IN]`, whether `CLAUDE.md` imports it, and that `$penta-pro` reconciles the temporary template content after the specification exists
- that prompts must be appended to `AGENTS.log` and that the log is ignored by Git; do not claim mechanical enforcement
- which collection skills read this configuration (Software Delivery, Git Ship, Peer Review and PR Quiz when they create or update tickets or PRs; `$penta-pro` and the review skills use the glossary and decision records)

Then present the next step explicitly:

> **Next step: run `$penta-pro`.** Introduce the software now — what it is, who it is for, the problem it solves, what the first usable version must do, and the terms your team already uses for the domain. `$penta-pro` turns that introduction into the five-pillar specification under `pentapro/` and tells you which decisions are still open.

Offer a ready-to-use opening prompt the user can paste and fill in:

~~~text
Use $penta-pro to start the specification for this project. Here is what we are building: <describe the software, who uses it, and the problem it solves>. The first usable version should <describe the smallest outcome worth delivering>. Record the domain terms we agree on in pentapro/product/domain.md, draft the five pillars, and list the decisions that are still open before any implementation starts.
~~~

Say that a plain description of the software and the intended outcome is enough; `$penta-pro` asks about consequential gaps, keeps the user's answers as the source, and marks inferred items as proposed. Glossary terms and decisions agreed during that conversation belong to PRODUCT and PROJECT, not to the repository root.

Finish with the maintenance note: `docs/agents/*.md`, the root instruction file, and `pentapro/` can be edited directly later; re-running this skill is only necessary to switch issue trackers, change the domain layout, or restart from scratch.
