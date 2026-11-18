---
name: setup-pentapro
description: "Configure this repository for the teknolista skills: choose the issue tracker and domain documentation layout, initialize the root instruction file from the packaged template, enable mandatory prompt logging (optionally with a project-scoped capture hook for the developer's coding agent), and decide which project facts belong in the PentaPRO specification. Recommended once per new project before the collection's coordinated workflows."
license: MIT
metadata:
  version: "1.2.0"
---

# Setup PentaPRO

Scaffold the per-repository configuration that the teknolista skills expect. This is the **first skill to run in a new project**. It records the issue tracker and the domain documentation layout, initializes the root agent instruction file, enables mandatory prompt logging (with an optional project-scoped capture hook for the developer's coding agent), and — when the developer approves — records the project facts that belong in the `pentapro/` specification. Skills that coordinate through the tracker read this configuration.

Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repository to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Which sections does it already carry? Is the packaged template's `Setup status: temporary` marker or an `## Agent skills` block present?
- Prompt-logging state: `AGENTS.log`, `docs/agents/prompt-logging.md`, existing `AGENTS.log*` ignore rules, and any project-scoped hook that already logs prompts (`scripts/agents-log/`, `.opencode/`, `.claude/`, `.codex/`, `.cursor/`, `.github/hooks/`).
- Coding-agent hosts: repository markers (`opencode.json`, `.opencode/`, `CLAUDE.md`, `.claude/`, `.codex/`, `.cursor/`, `.github/hooks/`, `.github/copilot-instructions.md`), installed CLIs (`opencode`, `claude`, `codex`, `cursor-agent`, `copilot`), and the user's configuration directories. A global capture for the same host is a duplicate risk, not a project mechanism. Check `node --version` for the optional hook.
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

Run the initializer in step 4, once the user authorizes it; it never overwrites existing files and fills the pillar topic files with `Pending` markers. If the installed `penta-pro` package is not available, recommend installing it or defer, and record the deferred facts as described in Section D. If the user prefers to defer, say that domain terms and other setup facts stay unrecorded until the first `$penta-pro` pass.

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

The root instruction file is the durable guide every agent reads. Build it from the packaged [agents.md](assets/agents.md) template: fill what repository evidence supports, keep unresolved template content visibly temporary, and never present generic guidance as a project fact.

- **Choose the file:** edit `CLAUDE.md` when it exists, otherwise `AGENTS.md`. If neither exists, ask which one to create. Never create a competing file.
- **New file:** seed it from the template. Fill the rows and commands exploration proved — purpose, stack, repository map, installed skill locations, verification commands — remove rows the evidence proves inapplicable, and leave the genuinely unknown ones as `[FILL IN]`.
- **Existing file:** preserve the user's content. Add a template section only when the file has no equivalent guidance, and update the skill-owned `## Prompt Logging` and `## Agent skills` blocks in place. Never duplicate a heading or replace project-specific rules with template prose.
- **Temporary status:** keep the template's setup marker while any material `[FILL IN]` or unverified template section remains. `$penta-pro` reconciles the file after the specification exists.

Prompt logging is mandatory in every repository configured by this skill; only the capture mechanism is a choice. The rule is the portable contract; a project hook is the optional mechanical guarantee.

- Write the operational rule into the root instruction file's `## Prompt Logging` section from the packaged template. Every agent appends each prompt to `AGENTS.log` before acting, including prompts sent to subagents.
- Copy [prompt-logging.md](assets/prompt-logging.md) to `docs/agents/prompt-logging.md` for the entry format, security, concurrency, host behavior, and limits.
- Ensure `.gitignore` ignores `AGENTS.log` and `AGENTS.log.*`; the log is local and never committed.
- Detect the coding-agent host(s) from exploration and present the list. Ask one question: keep the instruction rule alone, or add a project-scoped hook for the detected host(s)? Recommend the instruction alone for a solo repository whose host already has a working personal capture, and the project hook for a team repository or when mechanical enforcement is required. Do not ask per host; confirm the list once.
- The hook is always project-scoped: a shared `scripts/agents-log/` core plus the host's documented project configuration. Never write the user's global configuration, and never make the repository depend on a personal global capture. If the same host already captures globally, keep one mechanism or make the personal capture defer to the project hook.
- If the developer declines the hook, say that capture then depends on instruction compliance. Node.js 18+ is required for a hook; without it, do not offer the hook.
- If a project hook already logs prompts, keep one mechanism per host: verify its entry and do not add a duplicate rule or hook.

### 3. Confirm and edit

Show the user a draft of:

- the `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- the root instruction change: which template sections will be added, which fields exploration can already fill, and where the temporary marker stays
- `docs/agents/prompt-logging.md`, the `AGENTS.log*` ignore entries, and — when a hook was chosen — the exact host(s), files copied, configuration entries to merge, and whether those paths are ignored by Git
- the contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/triage-labels.md` (the last only when Section B ran), and `docs/agents/setup-notes.md` (only when facts were gathered and `pentapro/` was declined)
- the exact facts proposed for `pentapro/`, grouped by target pillar file, so nothing is written before the user approves the list

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create; don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa); always edit the one that's already there.

**Merge the root instruction template.** For a new file, start from [assets/agents.md](assets/agents.md), adjust the title to the chosen filename, and fill the fields exploration confirmed. For an existing file, add only the template sections it lacks, and add or update the `## Prompt Logging` and `## Agent skills` blocks in place. Keep the temporary setup marker while material fields remain unfilled. Do not overwrite, reorder, or replace user-authored sections with template prose.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

~~~
## Agent skills

### Issue tracker

Issues for this project live in [one-line summary, for example: GitHub Issues in this repository]. Read `docs/agents/issue-tracker.md` before creating, reading, labeling, or closing a ticket.

### Domain docs

[one-line summary: "single-context PRODUCT glossary" or "multi-context with a PRODUCT context map"]. See `docs/agents/domain.md`. The glossary lives in `pentapro/product/domain.md`; decision records live in `pentapro/project/decisions.md`.

### Repository setup

Agent setup is complete. The other collection skills read `docs/agents/*.md`; `$penta-pro` creates or resumes the `pentapro/` specification. Next step: run `$penta-pro` to introduce the software. `$setup-pentapro` (already run once for this repository) is not needed again unless the issue tracker or the domain layout changes.
~~~

Include the `### Triage labels` sub-block, linking to `docs/agents/triage-labels.md`, only when Section B ran; otherwise both are omitted.

Then write the files, using the seed templates in this skill folder as a starting point:

- [assets/issue-tracker-github.md](assets/issue-tracker-github.md): GitHub issue tracker
- [assets/issue-tracker-gitlab.md](assets/issue-tracker-gitlab.md): GitLab issue tracker
- [assets/issue-tracker-local.md](assets/issue-tracker-local.md): local-markdown issue tracker
- [assets/triage-labels.md](assets/triage-labels.md): label mapping (only if Section B ran)
- [assets/domain.md](assets/domain.md): domain documentation consumer rules and layout
- [assets/prompt-logging.md](assets/prompt-logging.md): prompt-logging policy copied to `docs/agents/prompt-logging.md`
- [assets/prompt-logging/core.mjs](assets/prompt-logging/core.mjs): shared entry, redaction and append core copied into the project when a hook is chosen
- [assets/prompt-logging/log-prompt.mjs](assets/prompt-logging/log-prompt.mjs): stdin adapter for command hooks
- [assets/prompt-logging/opencode.ts](assets/prompt-logging/opencode.ts): OpenCode project plugin adapter
- [assets/prompt-logging/hosts.md](assets/prompt-logging/hosts.md): host configuration, merge, trust and verification recipes
- [assets/agents.md](assets/agents.md): root instruction template

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

**Enable prompt logging.** Immediately after the root instruction file is written, write `docs/agents/prompt-logging.md` from [assets/prompt-logging.md](assets/prompt-logging.md). Ensure `.gitignore` lists `AGENTS.log` and `AGENTS.log.*`, preserving existing entries.

If the developer chose a project hook:

1. Copy `core.mjs` and `log-prompt.mjs` from [assets/prompt-logging/](assets/prompt-logging/) to `scripts/agents-log/`; copy `opencode.ts` too when OpenCode is one of the chosen hosts.
2. Merge the selected host entry from [hosts.md](assets/prompt-logging/hosts.md) into the project configuration the host already uses. Preserve every existing hook and key, validate the JSON afterwards, and show the user the exact entry before writing. Never overwrite a configuration file.
3. Run `git check-ignore -v` on each configuration path and tell the user whether the hook will be committed or remain local. Do not change the project's ignore policy without asking.
4. If a personal global capture exists for the same host, keep one mechanism or make the personal capture defer to the project hook (the OpenCode adapter sets `globalThis.__agentsLogProjectCapture`). Never install or edit the user's global configuration.
5. Run the smoke test from [hosts.md](assets/prompt-logging/hosts.md), then ask the user to send one real prompt; confirm exactly one new entry, check redaction with a fake secret, and record the host and version in `docs/agents/prompt-logging.md`.

If no hook was chosen, state that capture depends on the instruction rule. Never modify global agent configuration.

If Section B ran on GitHub or GitLab, create each configured label the tracker lacks (`gh label create` / `glab label create`).

If the user authorized initializing the PentaPRO skeleton, run the initializer now, before writing approved Section D facts into pillar files:

```sh
python3 <installed penta-pro path>/scripts/init_pentapro.py <repository root>
# For example, in a project using .agents/skills:
python3 .agents/skills/penta-pro/scripts/init_pentapro.py .
```

The initializer never overwrites existing files. If it is missing or fails, report the exact failure and continue with the remaining setup steps; do not create the pillar files by hand as a substitute.

Write the approved Section D facts into their pillar files. Preserve existing content, stable IDs and prior provenance; merge the new entries with their `Confirmed` / `Proposed` / `Pending` labels and sources. Rewrite the initializer's `Pending` guidance only where a fact replaced it; leave the rest for the first `$penta-pro` pass.

### 5. Done

Tell the user the setup is complete:

- what was written under `docs/agents/` and what was written into `pentapro/` (or where deferred facts were noted)
- which root instruction file was created or updated, which fields remain `[FILL IN]`, and that `$penta-pro` reconciles the temporary template content after the specification exists
- that prompt logging is active, that `AGENTS.log` is local and ignored by Git, which hosts have a project hook (or that the rule alone is the mechanism), whether a personal global capture already covers a host, and whether the hook configuration is committed or local according to the ignore check
- which collection skills read this configuration (Software Delivery, Git Ship, Peer Review and PR Quiz when they create or update tickets or PRs; `$penta-pro` and the review skills use the glossary and decision records)

Then present the next step explicitly:

> **Next step: run `$penta-pro`.** Introduce the software now — what it is, who it is for, the problem it solves, what the first usable version must do, and the terms your team already uses for the domain. `$penta-pro` turns that introduction into the five-pillar specification under `pentapro/` and tells you which decisions are still open.

Offer a ready-to-use opening prompt the user can paste and fill in:

~~~text
Use $penta-pro to start the specification for this project. Here is what we are building: <describe the software, who uses it, and the problem it solves>. The first usable version should <describe the smallest outcome worth delivering>. Record the domain terms we agree on in pentapro/product/domain.md, draft the five pillars, and list the decisions that are still open before any implementation starts.
~~~

Say that a plain description of the software and the intended outcome is enough; `$penta-pro` asks about consequential gaps, keeps the user's answers as the source, and marks inferred items as proposed. Glossary terms and decisions agreed during that conversation belong to PRODUCT and PROJECT, not to the repository root.

Finish with the maintenance note: `docs/agents/*.md`, the root instruction file, and `pentapro/` can be edited directly later; re-running this skill is only necessary to switch issue trackers, change the domain layout, or restart from scratch.
