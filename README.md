# PentaPRO — AI software development collection

**PentaPRO** is a collection of reusable skills for developers building software with AI coding agents. Its `penta-pro` specification skill turns intent into an actionable specification; Peer Review checks implementation against requirements and concrete evidence; Cybersecurity assesses security risks and controls across software, DevOps, and IT systems. The three UI Design skills turn requirements into web, Android and terminal interaction contracts, with authorized implementation and verification. The collection covers specification, implementation, research, testing, review, security, Git publication, production operations and agent guidance. Optional native Android implementation/test helpers and a generic PR quiz complement them; see [skill ownership](docs/SKILL-ROUTING.md). Each skill can be used independently.

The collection's skill instructions and reusable artifacts are written in English. Conversation uses the developer's preferred language. For a project README, Setup PentaPRO uses the language the developer selects.

> [!IMPORTANT]
> These skills are still in development. They are based on my personal experience developing my own applications and may need adjustments for other projects, teams, models, and workflows.
>
> All 26 skills are distributed under the [MIT License](LICENSE), with source attribution in the [third-party notices](THIRD-PARTY-NOTICES.md).
>
> Feedback from actual use, constructive criticism, and suggestions are very welcome through [GitHub Issues](https://github.com/teknolista/pentapro/issues).

## Install PentaPRO

PentaPRO is the collection/package name; the repository is `teknolista/pentapro` and the specification skill remains `penta-pro`. Choose **one installation method per host/project**. Installing both the plugin and copied skills can advertise duplicates. The bundle contains all 26 current skills and the six factory-agent templates; setup creates the actual selected-host agents in each project. Installing the plugin does not run setup, enable prompt hooks, select a model, or publish Git changes.

### 1. Choose the installation scope

**Recommended: project-scoped skills.** Run one command from the target repository (choose your agent):

```sh
npx skills@latest add teknolista/pentapro --skill '*' -a codex
npx skills@latest add teknolista/pentapro --skill '*' -a github-copilot
npx skills@latest add teknolista/pentapro --skill '*' -a opencode
npx skills@latest add teknolista/pentapro --skill '*' -a antigravity-cli
```

These are alternatives. No `-g` means project scope. Omit `-a` to select interactively; omit `--skill '*'` to choose individual skills. For editable independent copies, select copy in the installer or add `--copy`. Use `npx skills@latest check` and `npx skills@latest update` for installer-managed skills; review changes before adoption. [Installer reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)

`skills-lock.json` is installation provenance, not a hash of `SKILL.md` alone: its installer-defined `computedHash` covers the skill folder. This collection ignores its own local installation lock; that repository policy is not a rule for consuming projects. The upstream skills CLI supports versioning project locks for reproducibility. Use the installer corresponding to the existing route, preserve custom copies, and update provenance only after checking the installed content. A lock pointing to a newer commit does not prove that the bytes were updated. [Installer lock semantics](https://github.com/vercel-labs/skills/blob/main/src/local-lock.ts)

**Native plugin, project-scoped:** use the local bundle recipes below. They configure the project/session. Codex also requires installation through the host and an effective-scope check. Some hosts still cache package bytes in a user directory; project activation and cache storage are different. Use the skills CLI route when you require skill files to live entirely in the project and no plugin cache installation.

**Native plugin, user-wide:** these commands change the host's user installation/configuration and are optional:

```sh
# Codex
codex plugin marketplace add teknolista/pentapro
codex plugin add pentapro@teknolista

# GitHub Copilot CLI
copilot plugin marketplace add teknolista/pentapro
copilot plugin install pentapro@teknolista

# OpenCode V2
opencode plugin add github:teknolista/pentapro

# Antigravity CLI
agy plugin install https://github.com/teknolista/pentapro
```

OpenCode native discovery was not established in the recorded V2 probe; use the project-scoped skills CLI fallback when the plugin is absent from its registry. See [discovery evidence and limitations](docs/plugin-distribution.md).

Check the installed CLI's help before using these commands on older versions. These use a repository source, not a published npm package or an official marketplace listing. Remote installation requires the committed manifests to be available on GitHub. Updating local files in this checkout does not publish them. Host update/removal commands and policy vary; see [plugin operations](docs/plugin-distribution.md).

To install only skills globally, add `-g` to the selected skills CLI command. Global availability affects multiple repositories; a shared update can change behavior in all of them. Project copies can diverge or shadow global skills. Keep one active copy per skill/host and inspect the effective registered path before removing duplicates. No global setup or background action is required.

### 2. Run setup once in each target project

Open your host in the actual target repository and invoke the installed `setup-pentapro` skill, selecting its plugin-qualified name if the host namespaces it:

```text
Use the installed setup-pentapro skill to configure this project for PentaPRO.
Use project-local settings only and preserve existing files and decisions.
The project purpose is: [describe your project].
```

Setup preserves existing instructions, asks for unresolved README/license choices, prepares relevant project guidance and available tools, installs the selected-host agent templates and initializes the PDSA protocol and empty lessons record. It never writes into the plugin cache or turns a user-wide installation into global project configuration. Repeat per repository even when the plugin is installed globally. Existing customized agents/records are preserved on rerun; plugin updates do not silently replace them. Use the [safe profile refresh and read-only checker](skills/setup-pentapro/references/factory-setup.md#review-existing-role-updates) to identify outdated workflow bodies without discarding project choices. See [Setup PentaPRO](#setup-pentapro).

### Project-local native plugin recipes

From a separate source checkout of `teknolista/pentapro`, use Python 3.12+ with [maintenance dependencies](scripts/requirements-validation.txt) in an existing suitable environment. Export to a **new** directory in the target project. Replace the absolute example paths; never overwrite an existing plugin or host config. The exporter only copies distribution-eligible skill files and writes the selected-host manifest; it does not install anything or edit host settings.

| Host | Export command | Activate only in the target project |
| --- | --- | --- |
| Codex | `python3 /path/to/pentapro/scripts/package_plugin.py --host codex --output /path/to/project/plugins/pentapro` | Merge the repository marketplace and trusted-project config below; install from the local Plugins Directory, then verify effective scope. |
| Copilot CLI | `python3 /path/to/pentapro/scripts/package_plugin.py --host copilot --output /path/to/project/plugins/pentapro` | From that project run `copilot --plugin-dir ./plugins/pentapro`; this mounts for that session without a user-wide install. |
| OpenCode V2 | `python3 /path/to/pentapro/scripts/package_plugin.py --host opencode --output /path/to/project/plugins/pentapro` | Merge `"plugins": ["./plugins/pentapro"]` into project `opencode.json(c)` and restart; preserve other entries. Requires V2 `skill.transform`. |
| Antigravity CLI | `python3 /path/to/pentapro/scripts/package_plugin.py --host antigravity-cli --output /path/to/project/.agents/plugins/pentapro` | Start `agy` in the project; inspect `/plugin` and `/skills`. Optionally validate first with `agy plugin validate --strict /path/to/project/.agents/plugins/pentapro`. |

For Codex, merge this catalog into `.agents/plugins/marketplace.json` in the target project (retain other plugins):

```json
{
  "name": "pentapro-project",
  "plugins": [{
    "name": "pentapro",
    "source": {"source": "local", "path": "./plugins/pentapro"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Productivity"
  }]
}
```

Merge into the target project's `.codex/config.toml`, using its actual absolute path and keeping existing settings:

```toml
[marketplaces.pentapro-project]
source_type = "local"
source = "/absolute/path/to/project"

[plugins."pentapro@pentapro-project"]
enabled = true
```

The Codex catalog advertises a plugin; availability alone does not establish installation. Restart the app and install PentaPRO from the local Plugins Directory. The host uses its user cache and can save user-level enable choices; inspect those choices before claiming project-only activation. For installation wholly contained in the project, use the recommended skills CLI route. Codex loads project configuration only in trusted projects, subject to managed policy. Inspect availability with `codex plugin list --marketplace pentapro-project --available --json`. This establishes discovery, not agent/model execution. [Codex packaging](https://developers.openai.com/plugins/build/plugins) · [Copilot CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) · [OpenCode plugins](https://opencode.ai/docs/plugins/) · [Antigravity plugins](https://antigravity.google/docs/plugins)

**Validation status:** exported Antigravity bundles passed native strict validation with 24 skills; Codex discovered the root marketplace and exported local bundle. Copilot CLI is unavailable in the maintenance environment. The installed OpenCode 2.0.31 returned an empty plugin/skill registry even for a minimal control plugin; its runtime discovery is not established here. Use the skills CLI fallback until your client's plugin discovery is confirmed. Offline adapter/export tests do not certify all host versions. See [distribution design and checks](docs/plugin-distribution.md).

## Contents

- [PentaPRO — AI software development collection](#pentapro--ai-software-development-collection)
  - [Contents](#contents)
  - [Install PentaPRO](#install-pentapro)
  - [Available skills](#available-skills)
  - [Quick start](#quick-start)
  - [Choose a workflow](#choose-a-workflow)
  - [Start a pilot](#start-a-pilot)
  - [Installation and activation](#installation-and-activation)
    - [Install with the skills CLI](#install-with-the-skills-cli)
    - [Manual installation](#manual-installation)
    - [Activation](#activation)
    - [First task and adoption checks](#first-task-and-adoption-checks)
  - [Agent and model compatibility](#agent-and-model-compatibility)
    - [Native skill locations](#native-skill-locations)
    - [Required capabilities](#required-capabilities)
    - [Model selection and validation](#model-selection-and-validation)
  - [Setup PentaPRO](#setup-pentapro)
    - [Example requests](#example-requests)
    - [Output and working boundaries](#output-and-working-boundaries)
    - [Next step](#next-step)
    - [Provenance](#provenance)
    - [Resources](#resources)
  - [PentaPRO](#pentapro)
    - [The five pillars](#the-five-pillars)
    - [Example requests](#example-requests-1)
    - [Output and working boundaries](#output-and-working-boundaries-1)
    - [Resources](#resources-1)
  - [Peer Review](#peer-review)
    - [Example requests](#example-requests-2)
    - [Findings, verdicts, and boundaries](#findings-verdicts-and-boundaries)
    - [Test effectiveness](#test-effectiveness)
    - [Independent review and models](#independent-review-and-models)
    - [Hosted review environments](#hosted-review-environments)
    - [Resources](#resources-2)
  - [Cybersecurity](#cybersecurity)
    - [Modes and limits](#modes-and-limits)
    - [Example requests](#example-requests-3)
    - [Coverage and findings](#coverage-and-findings)
    - [Resources](#resources-3)
  - [UI Design Web](#ui-design-web)
  - [UI Design Android](#ui-design-android)
  - [UI Design Terminal](#ui-design-terminal)
  - [Diagnose Defect](#diagnose-defect)
  - [Behavior Testing](#behavior-testing)
  - [HTTP API](#http-api)
  - [MCP Server](#mcp-server)
  - [Software Delivery](#software-delivery)
  - [Software Factory](#software-factory)
    - [Durable execution records](#durable-execution-records)
    - [Continuous improvement with PDSA](#continuous-improvement-with-pdsa)
  - [Production Operations](#production-operations)
  - [Technical Research](#technical-research)
  - [Git Ship](#git-ship)
  - [Agent Instructions](#agent-instructions)
  - [Native Android implementation and testing](#native-android-implementation-and-testing)
  - [PR Quiz](#pr-quiz)
  - [Project agent instructions template](#project-agent-instructions-template)
  - [Guides and case studies](#guides-and-case-studies)
  - [Repository structure](#repository-structure)
  - [Maintenance and new skills](#maintenance-and-new-skills)
    - [Validation and improvement](#validation-and-improvement)
    - [Adding a new skill](#adding-a-new-skill)
  - [License and attribution](#license-and-attribution)
  - [Data privacy](#data-privacy)

## Available skills

| Skill | Version | Purpose |
| --- | --- | --- |
| [Setup PentaPRO](#setup-pentapro) | 2.4.0 | Set up prompt persistence, README and license choices, tracker and domain guidance, project-local factory agents, native change records and a PentaPRO handoff. |
| [PentaPRO](#pentapro) | 4.1.0 | Explore, create, resume, update, or review software specifications across PRODUCT, PROJECT, PRODUCTION, PROOF, and PROCESS. |
| [Peer Review](#peer-review) | 1.11.0 | Review backend, frontend, Android, and test code for substantiated defects and meaningful regression protection. |
| [Cybersecurity](#cybersecurity) | 1.6.1 | Model threats, assess security controls, and verify authorized hardening across web/API, desktop/mobile, DevOps, cloud, and IT projects. |
| [UI Design Web](#ui-design-web) | 1.0.0 | Design, review and implement browser screens and flows. |
| [UI Design Android](#ui-design-android) | 1.0.0 | Design, review and implement native Android screens and flows. |
| [UI Design Terminal](#ui-design-terminal) | 1.0.0 | Design, review and implement CLI/TUI interaction and readable output. |
| [Diagnose Defect](#diagnose-defect) | 1.1.1 | Reproduce unclear failures, distinguish causes, and verify authorized fixes. |
| [Behavior Testing](#behavior-testing) | 1.3.0 | Author behavior and regression tests or use a requested test-first workflow outside native Android. |
| [HTTP API](#http-api) | 1.2.0 | Implement HTTP API changes and verify compatibility, authorization, and write effects. |
| [MCP Server](#mcp-server) | 1.2.1 | Implement and verify Model Context Protocol server capabilities and transport boundaries. |
| [Software Delivery](#software-delivery) | 2.1.0 | Coordinate dependent implementation tasks and verify their integrated result against the agreed change. |
| [Software Factory](skills/software-factory/SKILL.md) | 1.2.0 | Coordinate an explicitly requested multi-agent run across specification, implementation, independent review, authorized delivery and retrospective. |
| [Production Operations](#production-operations) | 1.0.2 | Plan and configure hosted backends, deploy verified artifacts, and operate or recover the service. |
| [Technical Research](#technical-research) | 1.2.0 | Resolve technical uncertainty with traceable evidence. |
| [Git Ship](#git-ship) | 2.1.1 | Review, commit, publish or prepare the PR for the authorized Git snapshot. |
| [Agent Instructions](#agent-instructions) | 1.2.0 | Maintain portable software-development agent guidance. |
| [Android modules](skills/android-module-structure/SKILL.md) | 1.4.1 | Implement native Gradle/module configuration; specification belongs to PentaPRO. |
| [Android data](skills/android-data-layer/SKILL.md) | 1.3.0 | Implement repositories, Ktor/OkHttp, Room, DataStore and sync. |
| [Android errors](skills/android-error-handling/SKILL.md) | 1.2.5 | Implement typed domain/HTTP/storage error handling. |
| [Android Koin](skills/android-di-koin/SKILL.md) | 1.2.5 | Implement dependency bindings and Android lifetimes. |
| [Android background](skills/android-background/SKILL.md) | 1.2.4 | Implement durable WorkManager jobs and retries. |
| [Android unit testing](skills/android-unit-testing/SKILL.md) | 1.2.5 | Author/run/debug isolated logic tests. |
| [Android integration testing](skills/android-integration-testing/SKILL.md) | 1.3.0 | Author/run/debug non-UI integration tests. |
| [Android UI testing](skills/android-ui-testing/SKILL.md) | 1.3.1 | Author/run/debug native device/emulator Compose tests. |
| [PR Quiz](skills/pr-quiz/SKILL.md) | 2.0.0 | Explicitly requested PR decision-comprehension aid, separate from review approval. |

The [routing and consolidation map](docs/SKILL-ROUTING.md) records the 14 Android/quiz source skills. The [closure review](docs/COLLECTION-REVIEW.md) maps all 54 entrypoints in the two requested upstream repositories. Four Android UI skills are internal UI Design Android procedures; Android security is a Cybersecurity reference. Those five overlapping names are deliberately not separate installable skills.

The current collection contains **26 skills**. It is a curated adaptation, not a mirror of upstream packages. Matt Pocock or Superpowers are not required as separate installations.

## Quick start

In a new project, use the [installation prerequisites](#install-with-the-skills-cli), install `setup-pentapro` first, then the working skills you need. This example installs the setup skill and PentaPRO for Codex from the published collection.

```sh
npx skills@latest add teknolista/pentapro --skill setup-pentapro -a codex
npx skills@latest add teknolista/pentapro --skill penta-pro -a codex
```

Open a Codex session in that project, select `$setup-pentapro`, and ask:

> Configure this repository for the PentaPRO collection. Its purpose is to provide a local task tracker.

Setup configures prompt persistence and the relevant tracker and domain guidance. It uses the supplied purpose or discovers it from the repository. Choose whether to replace, complement or skip an existing README, select the language for the generated README and choose a license when the project lacks one.

Full setup also prepares native change/archive directories and six factory roles for the selected host (Codex, Claude Code, Cursor, GitHub Copilot, Antigravity or OpenCode) in the project when the installed tools support a safe project-scoped setup. Codex templates use Terra for implementation and verification and Sol for specification review, code review and retrospective, with high effort except medium for retrospective. The shipper defaults to GPT-6 Luna with high effort. These role settings were chosen with developer costs in mind; they are defaults, not a guarantee of the lowest cost for every task. Respect the configured model and effort, and do not silently substitute them. Developers may change their project-local settings for their host. Claude Code and Cursor templates inherit the session model by default; role-level selection and actual support depend on the host. Other host templates inherit the available session model where role-level selection is unsupported. A direct request to invoke a factory role without further detail requests its defined workflow in the current project and session; for the shipper, that includes git-ship review, commit and normal push, subject to scope, checks and host permissions. The setup reports unavailable prerequisites and preserves existing role files. See [factory setup](skills/setup-pentapro/references/factory-setup.md). A new Codex session may be needed to discover roles and skills.

For specification work, introduce the software, its users, the problem and the first useful outcome.

> Use $penta-pro to start the specification for this project. Here is what we are building: an offline-first notes app for a single user, where notes stay usable without a connection and sync when one returns. The first usable version should let me create, edit and search notes locally. Create a uniquely named active change under `pentapro/changes/<name>/` with `change.md`, `product.md`, `project.md`, `production.md`, `proof.md` and `process.md`. Record agreed domain terms and scenarios in that change’s `product.md`, capture open decisions in the owning dimension, and keep the root baseline unchanged until explicit result approval permits consolidation. This request is specification-only; stop before implementation.

Read the saved specification and confirm the first increment's behavior. For an agreed multi-step implementation, install and select [Software Delivery](#software-delivery). For a known local fix, give the agent the expected behavior and a focused check. Native SDD changes use the standard PentaPRO workflow. Use the [workflow guide](#choose-a-workflow) to decide when a versioned change record helps.

## Choose a workflow

Use a short request for a clear, reversible, low-risk edit. Work from the existing behavior and run the checks that cover the change. For exploratory prompting or vibe coding, isolate the experiment and capture the question it answers. Before carrying experimental code into a maintained product, establish the intended behavior and apply the product's implementation and verification gates.

For consequential work or when the project requires spec-driven development (SDD), use the governing specification or change record before implementation. The agent can draft it from the developer's intent, repository evidence and examples, then ask for unresolved decisions that affect the outcome. Use [PentaPRO](#pentapro) for a broader specification and [Software Delivery](#software-delivery) for dependent implementation tasks. Preserve the project's authoritative tickets, schemas and acceptance checks, and link them from the specification where useful.

Follow the native change contract at `pentapro/changes/<name>/`. Review the six fixed artifacts before dependent implementation, preserve the maintained baseline while building, and map the accepted scenarios to real entry-point checks. The change remains active until result acceptance, consolidation and archival. [Delivery example](skills/software-delivery/references/change-contracts.md#worked-example-with-project-native-sdd) · [Specification ownership](skills/penta-pro/references/document-maintenance.md#change-ownership)

If you require the entire selected scope specified before coding, say so in the request or project policy. Otherwise settle each increment's behavior, constraints and checks before implementing that increment. Give the agent autonomy over routine implementation choices within the agreed scope. Keep verification and any release authority explicit. For a hosted backend, use [Production Operations](#production-operations) when planning environments, configuring the release pipeline or carrying out an authorized deployment and verifying the running service. The [routing guide](docs/SKILL-ROUTING.md#choose-the-depth-of-the-workflow) shows how to apply this to common tasks.

## Start a pilot

1. Choose one maintained repository or a new project's first useful slice. Record the intended user outcome, relevant boundary, and one check that exercises it. Run `$setup-pentapro` to configure prompt persistence and the applicable tracker and domain guidance.
2. Install the primary skill and any specialist the work needs. For direct work, start with the agreed behavior and focused check. For vibe coding, define what the isolated experiment should demonstrate. Use the [prototype promotion example](skills/software-delivery/references/change-contracts.md#worked-example-of-adopting-a-prototype) if it will become maintained code.
3. Open or resume a native change with the factory. Link its five-dimensional specification and acceptance scenarios to checks through the actual product entry point; retain revision-bound evidence and pending gates. Use the [delivery example](skills/software-delivery/references/change-contracts.md#worked-example-with-project-native-sdd).
4. Run a working control and a meaningful failure check where the risk warrants it. Record the command, revision, result and any required check still pending in the project's existing PR or verification record. For consequential changes, follow the project's review, security and release gates. Record what a new session would need to resume.
5. Use the [pilot measurement procedure](docs/SKILL-EVALUATION.md#score-the-outputs) to compare outcomes and record friction or failures. See the [adoption plan](docs/ANTHROPIC-ADOPTION-PLAN.md) for the rationale and sequence.

A pilot can begin with a local test and synthetic inputs. Hosted deployment, native device coverage, third-party integration, and comparative model runs need the corresponding target tools and access.

## Installation and activation

### Install with the skills CLI

Install [Node.js 22.20 or later](https://github.com/vercel-labs/skills#install-a-skill), with npm/npx available, and run the command from the project where you want to use the skills. The CLI installs from the published GitHub repository.

To set up a new project for the collection, install `setup-pentapro` first:

```bash
npx skills@latest add teknolista/pentapro --skill setup-pentapro -a codex
```

Then install the working skills you need. To install PentaPRO for Codex or list the available skills, use the corresponding command:

```bash
npx skills@latest add teknolista/pentapro --skill penta-pro -a codex
npx skills@latest add teknolista/pentapro --list
```

The wildcard command installs all 26 skills, including `setup-pentapro`. Quoting `'*'` passes the wildcard to the installer.

```bash
npx skills@latest add teknolista/pentapro --skill '*' -a codex -y
```

Replace `codex` with another [supported agent identifier](https://github.com/vercel-labs/skills/blob/main/docs/agents.md), such as `claude-code` or `cursor`. Installation defaults to the current project. Add `-g` for user-level installation across projects.

To pilot edits from a local checkout, run `npx skills@latest add /path/to/pentapro --skill '*' -a codex --copy -y` from the pilot project. Use an absolute path to the checkout whose files you want to test.

The installer installs the selected skill packages and can link agent directories to a canonical copy. Use `--copy` when independent copies are needed; see the [installation methods](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#installation-methods). The repository's root `evals/` and `scripts/` stay in the collection checkout, even when you install all 26 skills. For a manual installation, copy only the selected skill directories. See [what belongs to the collection and to each package](#repository-structure).

Use `npx skills@latest check` to check for updates and `npx skills@latest update` to update installed skills. See the [official CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) for installation options and update scopes.

### Manual installation

Copy each desired skill directory into the location supported by your agent. Preserve its internal paths and included `LICENSE`. The complete Codex path inventory is below.

```text
your-project/.agents/skills/agent-instructions/SKILL.md
your-project/.agents/skills/android-background/SKILL.md
your-project/.agents/skills/android-data-layer/SKILL.md
your-project/.agents/skills/android-di-koin/SKILL.md
your-project/.agents/skills/android-error-handling/SKILL.md
your-project/.agents/skills/android-integration-testing/SKILL.md
your-project/.agents/skills/android-module-structure/SKILL.md
your-project/.agents/skills/android-ui-testing/SKILL.md
your-project/.agents/skills/android-unit-testing/SKILL.md
your-project/.agents/skills/behavior-testing/SKILL.md
your-project/.agents/skills/cybersec/SKILL.md
your-project/.agents/skills/diagnose-defect/SKILL.md
your-project/.agents/skills/git-ship/SKILL.md
your-project/.agents/skills/http-api/SKILL.md
your-project/.agents/skills/mcp-server/SKILL.md
your-project/.agents/skills/peer-review/SKILL.md
your-project/.agents/skills/setup-pentapro/SKILL.md
your-project/.agents/skills/penta-pro/SKILL.md
your-project/.agents/skills/pr-quiz/SKILL.md
your-project/.agents/skills/production-operations/SKILL.md
your-project/.agents/skills/software-delivery/SKILL.md
your-project/.agents/skills/software-factory/SKILL.md
your-project/.agents/skills/technical-research/SKILL.md
your-project/.agents/skills/ui-design-web/SKILL.md
your-project/.agents/skills/ui-design-android/SKILL.md
your-project/.agents/skills/ui-design-terminal/SKILL.md
```

A skill stored in this repository is not automatically installed into other projects. Codex discovers repository skills from `.agents/skills/`; if a copied skill does not appear, restart the session. Other hosts use their own discovery locations and invocation syntax. See [agent and model compatibility](#agent-and-model-compatibility) for documented locations, capabilities, and integration limits.

### Activation

The skills support automatic selection for matching tasks. In Codex, mention a skill name such as `$penta-pro`, `$http-api`, or `$android-data-layer` to select it explicitly. PentaPRO, Peer Review, Cybersecurity, UI Design packages, and Production Operations ship optional `agents/openai.yaml` display metadata and default prompts. Those presentation entrypoints were selected for their existing display/prompt integration; metadata is not a capability or quality tier, and other packages do not require it for Agent Skills discovery. Select the model through the host controls. Use `$pr-quiz` for a requested comprehension quiz or quiz setup.

The core instructions use Markdown and package-local references and templates. Skills refer to optional companions by name. The optional prototype helper uses Python. Publishing a requested PR quiz requires Python, `gh` and actual GitHub access, and its optional grader uses GitHub Actions. Use the tools, access and writable destinations required by the task. Installing a skill supplies instructions and package assets.

### First task and adoption checks

1. Install the packages needed for your work and confirm that your agent can discover and read them, including their supporting files. Use a small task in a disposable project to check activation and tool access before relying on a new host/model combination.
2. Run `$setup-pentapro` to configure the project for the collection, including the complete prompt-persistence rule, README and license choices, tracker and domain guidance. Re-running preserves unrelated instructions and existing decisions. See [Setup PentaPRO](#setup-pentapro).
3. Open the software project's root and provide the intended outcome, relevant constraints and expected result. Reuse existing project instructions and preserve their prompt-persistence rule.
4. Choose the [workflow depth](#choose-a-workflow). For a new specification, ask `Use $penta-pro to specify an offline notes application. Save the specification and identify unresolved decisions before implementation.` For an existing accepted plan, ask `Use $software-delivery to implement the next ready increment and run the required checks.` For a clear copy edit, identify the exact text and intended replacement directly.
5. For a hosted backend, try a plan or staging configuration with `$production-operations`. Use the [deployment brief](skills/production-operations/assets/deployment-brief.md) to identify the exact target, access and permitted effects. Verify the running revision and a critical path if deployment is in scope.
6. Inspect the actual artifacts and verification evidence. Confirm that the result meets the requested behavior, preserves existing constraints and names untested boundaries. Review and release follow the project's own gates. Resume material work from its saved contracts and evidence.

The collection supplies reusable methods and selected platform procedures. Generic workflows apply across stacks, with implementation procedures for native Android, web UI, HTTP APIs and MCP, and deployment guides for AWS, Azure, Google Cloud, Cloudflare and VPS. Other stacks require their own tooling and applicable documentation. Installation, a generated specification and passing collection tests do not certify the software produced with these skills. Consult the [maintenance review](docs/FINAL-SKILL-REVIEW.md) and [evaluation results](evals/RESULTS.md) for the scope actually checked.

## Agent and model compatibility

Official host documentation checked on 2026-10-25. These packages use the Agent Skills format: Markdown instructions, relative references/assets, and optional OpenAI UI metadata. Native format support, execution access, and measured task quality are separate claims.

### Native skill locations

Copy the complete skill directory, retaining its internal paths. Use the location supported by the actual host and execution environment; installing locally does not install into every cloud agent.

| Host | Documented project locations | Documented user locations | Official guidance |
| --- | --- | --- | --- |
| Codex | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` | [Build skills](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | [Extend Claude with skills](https://code.claude.com/docs/en/skills) |
| Gemini CLI | `.gemini/skills/<name>/` or `.agents/skills/<name>/` | `~/.gemini/skills/<name>/` or `~/.agents/skills/<name>/` | [Agent skills](https://geminicli.com/docs/cli/skills/) |
| GitHub Copilot | `.github/skills/<name>/`, `.claude/skills/<name>/`, or `.agents/skills/<name>/` | `~/.copilot/skills/<name>/` or `~/.agents/skills/<name>/` | [Create agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) |
| Cursor | `.agents/skills/<name>/` or `.cursor/skills/<name>/` | `~/.agents/skills/<name>/` or `~/.cursor/skills/<name>/` | [Agent Skills](https://cursor.com/docs/skills) |

Invocation and consent differ by host. For example, Codex documents `$name`, Claude Code and Cursor support `/name`, and Gemini CLI exposes skill discovery/activation controls. Confirm discovery using the host's skill list or explicit invocation. Avoid installing duplicate copies with the same name just to cover several paths.

### Required capabilities

| Task | Necessary access | If unavailable |
| --- | --- | --- |
| Setup and factory | Writable project, applicable package assets and selected host tools | Resolve setup choices, keep unavailable capabilities pending and use a separate review context where required. See [factory setup](skills/setup-pentapro/references/factory-setup.md) and [role packets](skills/software-factory/references/roles.md). |
| PentaPRO creation/update | User intent, relevant existing context, package assets, and a writable requested destination | Ask only consequential missing questions; retain proposals and blockers. If writing is unavailable, return the draft and disclose that it was not saved. |
| PentaPRO review | The actual specification and relevant authoritative context | Report missing material rather than treating an absent document as ready. |
| UI Design specification and implementation | Relevant requirements/design context and a writable target project; source/toolchain for implementation, browser or Android environment for runtime checks | Save a partial specification and mark pending decisions/checks; never claim rendered, device, accessibility or user validation without evidence. |
| Code inspection | Actual selected source/snapshot, relevant requirements/contracts, and applicable references | Report material missing coverage; do not infer a clean review from a description alone. |
| Cybersecurity assessment | Authorized target/snapshot, relevant security requirements, applicable domain references, and evidence of the controls being claimed | Separate source/configuration from deployed/runtime evidence; mark inaccessible areas and avoid security or compliance guarantees. |
| Executed verification | The project's actual tools and isolated data/environment | Label unexecuted checks and distinguish static conclusions from runtime evidence. |
| Hosted backend deployment or recovery | Project pipeline or provider tooling, target and scoped identity, action authority, and applicable traffic, data and recovery checks | Complete accessible plan or configuration work and mark live effects or checks pending when the target is unavailable. |
| Independent review | A separate reviewer/session with actual source access | Disclose self-review or prepare a factual handoff; do not claim independence from a model label. |

Git, shell execution, browsers, Android SDKs, credentials, connectors, and additional agents are not supplied by installing a skill. Git is useful for comparisons, but an explicitly selected source snapshot can be reviewed without it. The skills can be used independently. Cybersecurity live testing and remediation require actual target/action authorization; capability does not imply permission.

Managed review services may load only instruction text. See [Hosted review environments](#hosted-review-environments) for supporting-file and execution limits.

### Model selection and validation

The skills include concrete behavior traces, failure examples, and evidence checks to reduce reliance on unstated engineering knowledge. For larger tasks, retain the target snapshot, reviewed and pending areas, evidence, unresolved questions, and next action. Reopen relevant source after context loss or a changed snapshot. Validate representative tasks on each intended model and host before relying on its results.

Portable workflows let the project and host choose models. The optional project-local Codex factory TOMLs supply editable model and reasoning defaults, subject to host availability. The package files named `agents/openai.yaml` provide display metadata and a default prompt.

Choose a currently available model with sufficient reasoning, domain competence, context capacity, and reliable tool use for the task. Escalate difficult requirements or review risks when evidence warrants it. The documented [OpenAI model options](https://learn.chatgpt.com/docs/models) include the repository's example implementation/review pairing; availability and suitability depend on the host/account and observed results. A model name is not a quality gate.

After changing host, model, or significant instructions, run the relevant [PentaPRO cases](skills/penta-pro/evals/scenarios.md), [Peer Review cases](skills/peer-review/evals/scenarios.md), [Cybersecurity cases](skills/cybersec/evals/scenarios.md), and [web cases](skills/ui-design-web/evals/scenarios.md), [Android UI cases](skills/ui-design-android/evals/scenarios.md) and [terminal UI cases](skills/ui-design-terminal/evals/scenarios.md). Check correct activation, preserved user decisions, meaningful defects versus false positives, honest evidence/coverage, and unintended edits. Compare matched tasks before claiming better accuracy, cost, or latency. Official format support does not establish a cross-vendor performance benchmark.

## Setup PentaPRO

**Entrypoint:** [skills/setup-pentapro/SKILL.md](skills/setup-pentapro/SKILL.md)

Set up the current repository for the collection: a template-based README in the chosen language, a missing project license selected by the developer, prompt persistence and a permanent motivational manifesto in `AGENTS.md`, merged Git defaults, appropriate issue-tracker and domain guidance, optional triage mappings, project facts and a PentaPRO handoff. The full prompt rule is embedded in the skill and written into `AGENTS.md` without requiring another policy file. Logging depends on agent compliance; no hook is installed.

### Example requests

```text
Use $setup-pentapro to configure this repository. Its purpose is to provide a CLI for tracking local tasks.
```

Supply a complementary description of the repository purpose; when omitted, setup inspects the repository to discover it. For an existing README, choose replace, complement, or skip; select the README language. When no project license exists, choose from GitHub license options before setup creates `LICENSE`. The bundled template comes from the developer-supplied README. See [README and license setup](skills/setup-pentapro/references/readme-and-license.md).

Full setup writes the bundled `assets/gitignore` and `assets/gitattributes` to root `.gitignore` and `.gitattributes`. Existing files receive only absent lines before their current content, preserving project-specific rule precedence. A repeat setup adds no duplicate lines and does not renormalize tracked files. The standalone [Git-template helper](skills/setup-pentapro/scripts/merge_git_templates.py) performs this merge with Python 3 and Git; manual setup follows the same contract.

Every fully initialized project must carry the complete **Software Excellence Manifesto — Powered by PentaPRO** near the beginning of `AGENTS.md`, including when instructions already exist. The section is mandatory and permanent: initialization must not skip it, and later maintenance, cleanup and specification reconciliation must never remove it. This developer-requested experiment studies motivational framing and autonomous model decisions; no improvement has been demonstrated. When README editing is authorized, setup adds a short explanation in the chosen language. Skipping README changes does not waive the manifesto. Plugin installation or an update alone does not modify project files; run full setup per project.

For prompt logging only, request that narrower scope explicitly.

### Output and working boundaries

A full setup may create or, after the selected treatment, update `README.md`, create a missing `LICENSE` after license selection, and update `AGENTS.md`, `.gitignore`, `.gitattributes`, relevant `docs/agents/` guidance, native change/archive directories and the selected host's agent directory; use the PentaPRO skill for an authorized specification. Preserve existing instructions, canonical domain records and tracker decisions. Remote labels, remotes and migrations require authority for those operations. Unavailable tools and unverified facts remain explicit.

### Next step

For specification work, invoke [PentaPRO](#pentapro) and describe the software, users, problem and first usable outcome.

### Provenance

Adapted from Matt Pocock's setup workflow (MIT). See [source notes](skills/setup-pentapro/references/sources.md) and [third-party notices](THIRD-PARTY-NOTICES.md#setup-pentapro).

### Resources

| Resource | Purpose |
| --- | --- |
| [Entrypoint](skills/setup-pentapro/SKILL.md) | Setup workflow and self-contained prompt-persistence rule. |
| [Repository setup](skills/setup-pentapro/references/repository-setup.md) | Tracker, triage, domain, project facts and handoff procedure. |
| [README and license](skills/setup-pentapro/references/readme-and-license.md) | Project purpose, template, language and licensing choices. |
| [Factory setup](skills/setup-pentapro/references/factory-setup.md) | Native changes, cross-host agents, PDSA records, models and verification. |
| [PDSA protocol template](skills/setup-pentapro/assets/continuous-improvement.md) | Contextual execution, bounded recovery and orchestrator-owned learning. |
| [Run directory guide](skills/setup-pentapro/assets/runs-readme.md) | Durable state location, ownership and recovery boundaries; no active run at setup. |
| [Lessons template](skills/setup-pentapro/assets/lessons-learned.md) | Empty project record with evidence and confidence fields. |
| [Evaluation scenarios](skills/setup-pentapro/evals/scenarios.md) | Authored cases for full and scoped setup. |
| [Root instruction template](skills/setup-pentapro/assets/agents.md) | Permanent manifesto and adaptable project guidance, preserving existing instructions. |
| [Git ignore template](skills/setup-pentapro/assets/gitignore) / [attributes template](skills/setup-pentapro/assets/gitattributes) | Defaults merged into dotted root Git files without duplicate additions. |


## PentaPRO

**Entrypoint:** [skills/penta-pro/SKILL.md](skills/penta-pro/SKILL.md)

For everyday software, PentaPRO is the canonical product record and the default starting point for specification work in a new project. [Setup PentaPRO](#setup-pentapro) can prepare the repository first but is not required. When setup has produced temporary root instruction fields, the first consolidated specification pass reconciles them with confirmed project facts and preserves unresolved fields.

Use PentaPRO when defining a product, specifying a substantial feature, maintaining an existing PentaPRO document, or checking whether the next increment is ready for development. It uses existing project information and asks about consequential gaps. Ordinary coding tasks and small, clear specification updates do not restart a full interview.

An exploration-only request stays in the conversation until the user asks to capture the findings. For a material change, PentaPRO compares the proposal with the current requirements and behavior, identifies compatibility commitments, and traces their effects across the pillars. Applicable project rules and amendments are linked from PROCESS.

### The five pillars

| Pillar | Focus |
| --- | --- |
| PRODUCT | Users, value, journeys, business rules, permissions, scope, and observable acceptance criteria. |
| PROJECT | Delivery constraints, resources, dependencies, risks, architecture, data, and contracts. |
| PRODUCTION | Installation, environments, updates, migration, support, monitoring, and recovery. |
| PROOF | Verification methods, concrete examples, failure cases, and acceptance evidence. |
| PROCESS | Tasks, responsibilities, execution authority, review, integration, and escalation. |

The preferred order for initial detail and document presentation is PRODUCT → PROJECT → PRODUCTION → PROOF → PROCESS. Establish behavior, acceptance criteria, and consequential conditions of real use in PRODUCT. Choose a feasible solution in PROJECT, detail its operation in PRODUCTION, then define complete checks and evidence in PROOF. Maintain PROCESS authority and resume state throughout. Reconcile affected pillars as decisions change; the order does not impose sequential development phases.

The template connects product strategy and stopping criteria to discovery evidence, outcomes, requirements, contracts, verification, and post-release learning. It includes a consolidated identifier and status model, increment readiness, decision and uncertainty records, privacy and accessibility considerations, delivery dependencies, documentation, launch and support readiness, and operational recovery evidence. Conditional profiles cover services, installed/offline apps, CLI tools, infrastructure, libraries, data/scientific workloads, AI features, embedded systems, interactive media, and commercial launch. For Android/KMP projects, an [additional overlay](skills/penta-pro/references/android-kmp.md) details cross-platform contracts, test boundaries, state retention, dependency lifetimes and release evidence within the five pillar directories. Combine profiles for hybrid products; they are not an exhaustive taxonomy.

Discovery resolves ambiguous domain terms with examples and counterexamples, compares material alternatives, and records the authority behind decisions. Binding principles become verifiable requirements. The selected increment includes a useful outcome and a check that can demonstrate it before later features exist. Detailed patterns address uncertain completion, retries, concurrent actions, access changes during queued work, and migration coexistence.

### Example requests

```text
Use $penta-pro to explore options for offline editing before we write the specification.
Use $penta-pro to interview me and create a specification for this project.
Use $penta-pro to resume the interview from pentapro/process/index.md.
Use $penta-pro to update the specification with these new requirements: ...
Use $penta-pro to review whether the first increment is ready for development.
```

### Output and working boundaries

A first specification is authored in `pentapro/changes/<name>/` using `change.md`, `product.md`, `project.md`, `production.md`, `proof.md` and `process.md`. Root topic files under the five pillars represent the consolidated baseline; initial scaffolds remain Pending until the implemented change is accepted and consolidated. The existing optional initializer prepares those directories without overwriting records. Use ordinary file tools if the helper is unavailable. See [change specification](skills/penta-pro/references/change-specification.md).

Existing PentaPRO specifications require an inventory and reconciliation before the new topic files become authoritative. Preserve legacy paths as redirects when callers need them.

PentaPRO owns both the maintained five-pillar baseline and the specification inside active changes. The factory coordinates their lifecycle; Software Delivery plans and implements tasks. A completed or cancelled change moves to `pentapro/changes/archive/YYYY-MM-DD_<name>/`, with disposition and publication recorded separately. [Ownership and reconciliation](skills/penta-pro/references/document-maintenance.md#change-ownership).

Creation saves the first draft in the selected format and location before pausing for answers. The initializer creates linked topic drafts across all five pillars. Later rounds update the affected records, with stable IDs or locators and links to authoritative definitions. PROCESS records `In progress` for material updates across files and `Consistent` after reconciliation. Resumption inspects actual contents and completes any interrupted update. Proposed changes retain their baseline, compatibility commitments, and separate status until settled.

For consequential ideas, PentaPRO records a working hypothesis and challenges it from the perspectives that could change the decision. Before handoff or authorized implementation, it reviews the consolidated specification by reconstructing a representative journey from the artifacts, comparing that reading with confirmed intent, and tracing material dependencies through the pillars. PROCESS holds the scoped review result, open items and next action. The author can run this review directly. Fresh independent review is available when authorized and supported by the host. [Specification review](skills/penta-pro/references/specification-review.md)

The skill distinguishes confirmed information, proposals, and pending decisions. Routine decisions made within explicit delegation are attributed to the agent and can be settled for readiness without being presented as user requirements or document acceptance. When the user is unavailable, retain consequential blockers and complete independent specification work. If saving is unavailable, return an explicitly unsaved draft.

PentaPRO drafts from accessible evidence and delegated choices with provenance. It identifies unresolved research, baselines, legal applicability, approvals, and test evidence. The interview targets consequential missing decisions. All five pillars remain, with coverage recorded as included, linked, pending, deferred, or not applicable. Larger specifications can link feature details, increment plans, and contracts from their owning pillar. The skill loads specialized forms and examples as needed.

Critical product rules should have concrete input/output examples independent of the implementation. PROOF identifies realistic regressions that planned assertions must detect and checks that reported execution actually exercises them. Planned checks remain `Unverified` until executed. Specification readiness, document acceptance, implementation verification, and release acceptance are separate states. Creating or updating a specification does not itself authorize implementation or release; existing authorization remains valid.

A sufficiently specified increment can be ready for implementation while its future software tests remain unverified. An unresolved product decision blocks the work that depends on it. When the request requires the entire selected scope specified first, readiness must cover that scope before coding. Acceptance records the responsible person's actual decision, scope, revision, and conditions. The handoff carries enough linked context for an implementer who did not attend the interview. Exploration and review preserve their next action in the conversation unless specification writing is authorized.

The workflow is model-neutral. Use a host that can load the complete skill folder and relevant project context. Disclose missing capabilities rather than inventing answers or verification results. Package compatibility does not establish identical quality across models.

### Resources

| Resource | Purpose |
| --- | --- |
| [Entrypoint](skills/penta-pro/SKILL.md) | Scope, interview workflow, document maintenance, readiness, and handoff. |
| [Template index](skills/penta-pro/assets/penta-pro-template.md) | Authoring guidance and links to the five pillar templates. |
| [Initializer](skills/penta-pro/scripts/init_pentapro.py) | Creates the five-pillar specification in a repository root, preserving existing files; offline tests live in the package's `scripts/tests/`. |
| [Document maintenance](skills/penta-pro/references/document-maintenance.md) | Canonical ownership, coordinated updates, resumption, and migration. |
| [Focused discovery](skills/penta-pro/references/discovery.md) | Conditional techniques for unclear intent, dependent questions, alternatives, and consequential missing information. |
| [Specification review](skills/penta-pro/references/specification-review.md) | Artifact-based comprehension, cross-pillar checks, finding resolution and readiness handoff. |
| [Software profiles](skills/penta-pro/references/software-profiles.md) | Coverage prompts for software types and cross-cutting concerns, including accessibility, privacy, and impacts on people and the environment. |
| [Specification patterns](skills/penta-pro/references/specification-patterns.md) | Conditional forms for data, interfaces, decisions, threats, evidence, and runbooks. |
| [Worked example](skills/penta-pro/references/worked-example.md) | Fictional example of linked requirements and planned evidence, with explicit uncertainty. |
| [Analyst review assessment](skills/penta-pro/references/analyst-review-assessment.md) | Assessment of the supplied reviews, adopted improvements, and recommendations adapted or not adopted. |
| [Source notes](skills/penta-pro/references/sources.md) | Discovery, proposal, project-rule, and operational research, with inspected revisions and adaptation decisions. |
| [Evaluation scenarios](skills/penta-pro/evals/scenarios.md) | Discovery, interview, update, delegation, and scope cases, with validation records. |
| [OpenAI metadata](skills/penta-pro/agents/openai.yaml) | Optional Codex display metadata and example invocation. |

For creation, read the template index and five pillar templates. For updates and reviews, consult relevant sections for structural gaps or readiness. Screen profiles for new specifications or material scope changes and read detailed patterns as needed. Source notes, the analyst assessment, and evaluation cases are maintainer resources.

## Peer Review

**Entrypoint:** [skills/peer-review/SKILL.md](skills/peer-review/SKILL.md)

Use Peer Review for backend services, frontend applications, Android software, and the effectiveness of their tests. It supports local edits, selected files or snippets, pull requests, commit comparisons, independent second opinions, and re-review after fixes. Reports separate substantiated defects, verification gaps, optional improvements, and remaining release requirements.

### Example requests

```text
Use $peer-review to review all my uncommitted changes, including new files.
Use $peer-review to review this branch against origin/main, including the local edits.
Use $peer-review to review the selected PR against the requirements and checks in pentapro/product/overview.md and pentapro/proof/traceability.md.
Use $peer-review to review the changed tests for assertions that would miss the regressions they claim to detect.
Use $peer-review to review the Android release changes, focusing on lifecycle and data migration.
Use $peer-review to re-review the fixes for CR-001 and CR-002 on the current revision.
Use $peer-review to prepare a handoff for an independent reviewer in another session.
```

`origin/main` is an example; use the actual intended base. A committed comparison and the current worktree are different scopes. With no named target, the skill starts with uncommitted work, including staged, unstaged, and relevant untracked files, and identifies comparisons that need clarification.

An explicitly selected file or source snippet can be reviewed without Git or an earlier version. The reviewer assesses current behavior and reports origin as `Unknown` when history is unavailable; it does not invent a regression claim or source location.

### Findings, verdicts, and boundaries

Findings include a real location or precise snippet label, reachable trigger, expected/actual behavior, impact, evidence, confidence, correction direction, and regression check. Severity uses P0–P3 with an explicit blocking disposition. Expected results come from authoritative product rules and examples, independently of the implementation and its tests. Zero findings is valid; there is no finding quota.

The report gives coverage, evidence, limitations, and one verdict:

- `Changes requested`: validated blocking findings remain.
- `No blocking findings`: the agreed review is complete without validated blockers.
- `Incomplete`: material context or coverage is missing.

The review preserves the selected source and Git state. Fixes, remote comments or approvals, merging, and releasing follow actual user authorization and project gates. Reports and filled handoffs belong to the reviewed project or requested output location, not the reusable skill folder. Existing `REVIEW.md` guidance is optional; the skill does not create or change project policy automatically.

The reviewer follows consequential behavior from its contract through entry points, guards, effects, and consumers. Concrete inputs and event order help investigate authorization, races, retries, and stale asynchronous results. Existing protections and unknown premises are checked before retaining a finding. Cross-file change maps and guided summaries are reconciled with the full in-scope diff. For related PRs, the skill checks shared behavior and distinguishes branch evidence from the actual integration state. [Conditional coordination guidance](skills/peer-review/references/independent-review.md#coordinate-related-changes) covers owners, dependencies, review capacity and workflow evaluation without imposing queue limits or authorizing Git integration.

The [automated-check layer](skills/peer-review/references/verification.md#establish-automated-check-evidence) separates formatting/static/build checks, security/secret scans and behavioral tests from semantic review. Evidence must match the snapshot; required gates retain their consequences. Migrations, authentication/configuration, dependencies and weakened test/CI protection trigger deeper tracing. Test retirement or replacement is assessed against the affected contract and remaining protection. For known escaped defects, the [learning loop](skills/peer-review/references/verification.md#learn-from-escaped-defects) connects the root cause to a meaningful regression check and proportionate process improvement under the existing authorization.

Follow-up reviews compare the current snapshot with the last reviewed one, check outstanding findings and trace affected paths. For consequential releases, the reviewer checks what the proposed recovery would actually restore. [Focused re-review](skills/peer-review/references/independent-review.md#focus-the-next-pass) · [Risk and recovery](skills/peer-review/references/review-method.md#choose-proportionate-depth)

### Test effectiveness

Peer Review examines the tests relied on for changed behavior, including their discovery, fixtures, real subject, assertions, and completion. It asks which realistic wrong behavior would still pass.

- Inspect tautologies, unused matchers, swallowed failures, unawaited assertions, and conditional or empty-case verification.
- Check whether mocks replace the behavior under review and whether shared fixtures, mock history, or automatic retries hide a failure.
- Derive expected results from the contract. Review skips, focus filters, weakened assertions, and regenerated snapshots against any authorized requirement change.
- Inspect helpers and framework semantics before judging a smoke test, snapshot, interaction check, or type assertion.

The verification guidance incorporates lessons from Hollowtest. Its CLI is optional and must support the actual language and runner. Static diagnostics and scores are review evidence to investigate. Mutation probes use a disposable copy and a passing baseline, then distinguish meaningful assertion failures from equivalent mutations, compilation errors, timeouts, and incorrect test selection. The [verification guide](skills/peer-review/references/verification.md) contains the detailed checks and execution boundaries.

### Independent review and models

A practical workflow is:

```text
Implementer -> project checks -> fresh reviewer -> validated findings
           <- focused fixes  <-                  |
           -> relevant checks -> re-review ------+
```

The reviewer receives requirements, actual source/snapshot access, contracts, and check evidence. It does not need the implementer's full conversation. A fresh session of the same capable model can provide independence; a different model may add diversity.

For example, use `gpt-6.1-terra` for implementation and `gpt-6.1-sol` for review when available in the host. Select the reviewer through model/session controls or authorized orchestration; installing this package does not select or change a model. Evaluate the arrangement on validated defects, material misses, false positives, time, and cost. No model-pair benchmark is claimed.

### Hosted review environments

Confirm how a managed reviewer receives instructions. Including only the body of `SKILL.md` does not transfer supporting references or execution capabilities. Claude's [managed Code Review customization](https://code.claude.com/docs/en/code-review-customize) can include skill text through its review policy but does not load supporting files. This differs from a local Claude Code session loading the complete directory. Supply needed guidance through that service's supported configuration and qualify coverage when references or execution are unavailable.

### Resources

| Resource | Purpose |
| --- | --- |
| [Entrypoint](skills/peer-review/SKILL.md) | Scope, routing, evidence requirements, independence, and follow-up. |
| [Review method](skills/peer-review/references/review-method.md) | Target selection, trusted policy, confidence, severity, coverage, and verdicts. |
| [Backend](skills/peer-review/references/backend.md) | APIs, authorization, data, concurrency, failure recovery, and operations. |
| [Frontend](skills/peer-review/references/frontend.md) | UI state, contracts, accessibility, browser boundaries, and performance. |
| [Android](skills/peer-review/references/android.md) | Lifecycle, coroutines, Flow, Compose/Views, platform security, and release variants. |
| [Android/KMP test effectiveness](skills/peer-review/references/android-testing.md) | Coroutine schedulers, Flow, Compose synchronization, restoration and target coverage. |
| [Verification](skills/peer-review/references/verification.md) | Test effectiveness, assertion execution, false-positive checks, isolated mutation probes, model correspondence, performance claims, and evidence reporting. |
| [Independent review](skills/peer-review/references/independent-review.md) | Fresh context, model selection, review lenses, and feedback loops. |
| [Report template](skills/peer-review/assets/review-report-template.md) | Optional structure for substantial or saved reviews. |
| [Handoff template](skills/peer-review/assets/review-handoff-template.md) | Factual packet for another reviewer or model. |
| [Source research](skills/peer-review/references/sources.md) | Original sources, official guidance, and synthesis decisions. |
| [Evaluation scenarios](skills/peer-review/evals/scenarios.md) | Calibration, scope, policy, host behavior, and validation records. |
| [OpenAI metadata](skills/peer-review/agents/openai.yaml) | Optional Codex display metadata and example invocation. |

Android/KMP guidance also examines typed-result fallback/decoding semantics, dependency lifetimes and shared-platform boundaries. Test review distinguishes scheduler/clock ownership, conflated Flow states, device execution and actual OS restoration.

Load the review method and applicable references. Source research and evaluation cases are maintainer resources, not required context for every review. The package is an original synthesis, not an installer or runtime wrapper around upstream skills.

## Cybersecurity

**Entrypoint:** [skills/cybersec/SKILL.md](skills/cybersec/SKILL.md)

Use Cybersecurity for explicit security assessments, threat modeling, secure implementation, hardening, and security readiness checks. It covers web/frontends, backend/APIs, desktop/native applications, Android/iOS, CI/CD, supply chains, cloud/IaC/containers, enterprise IT, and AI/agentic systems when present. It selects the relevant surfaces instead of running every checklist for every project.

### Modes and limits

Threat modeling produces assets, trust boundaries, credible abuse cases, controls, and planned verification. Repository audits inspect the current snapshot unless a narrower target is specified; they preserve reviewed files. Secure-build/hardening mode implements only security work already authorized and verifies affected controls. Readiness mode evaluates the requested gate, including detection, containment, recovery, and risk ownership.

No model or skill can predict every attack or establish invulnerability. Cybersecurity identifies supported vulnerabilities, credible threats, control gaps, and residual/unassessed risk. Source configuration, deployed controls, and runtime evidence are separate. Framework alignment or passing scans does not establish certification, compliance, or full release approval.

Live scans, exploitation, fuzzing, credential tests, shared-system testing, production changes, and external data transfers require authorization covering the specific actions, targets, methods, environment, and limits. Existing valid authorization is reused. An audit does not itself authorize fixes, installations, deployment, or secret/IAM changes.

### Example requests

```text
Use $cybersec to assess this repository's security controls and report findings and unreviewed areas. Keep the source unchanged.
Use $cybersec to threat-model the architecture in pentapro/project/architecture.md, including abuse cases and verification plans.
Use $cybersec to map this project's relevant threats to controls, tests, and gaps, including cross-component attack chains. Save the assessment to docs/security-assessment.md.
Use $cybersec to review this desktop app's IPC, local-file access, installer, and update boundaries.
Use $cybersec to review the Android and iOS release configuration and API trust boundaries.
Use $cybersec to assess CI/CD, dependencies, IaC, cloud IAM, and container isolation without live scans.
Use $cybersec to review IT identity, endpoint, network, and recovery policies; distinguish policy from operational evidence.
Use $cybersec to implement the approved fixes for SEC-001 and SEC-002 in this local test environment, then verify them.
Use $cybersec to re-assess the requested release-security gate and write docs/security-assessment.md.
```

### Coverage and findings

Substantial reports include the selected target/snapshot, relevant baseline/versions, credible threats, evidence-backed findings, and control coverage. Each relevant area is marked Assessed, Partially assessed, Not assessed, or Not applicable with a reason. Findings distinguish impact-based priority from confidence, test results, and treatment state; a changed but unverified fix is not a resolved vulnerability. Hypotheses remain investigation items rather than confirmed defects.

The coverage map connects material threats to controls, verification evidence, residual gaps, and responsible next actions. It considers attacks that combine weaknesses across components and tests whether fixes block unauthorized effects while preserving legitimate behavior. Reassess affected coverage after meaningful system or threat changes. Narrow reviews stay concise; the skill does not impose a full matrix on every change, assign an invented security score, or start continuous monitoring.

Mobile guidance also covers packaged configuration versus privileged secrets, credential storage/backups, HTTP logging, trusted destinations and refresh/logout races across actual platform implementations.

Concrete traces connect attacker-controlled input, the protected resource and rule, actual enforcement, effects, and counterevidence. Mechanism checks include queued work and caches after permission changes, concurrent one-use actions, resource limits before allocation, native length arithmetic, password hashing, token lifecycle, and cryptographic library use. Authorization checks pair an existing protected resource and an allowed actor with the prohibited case, then inspect data and side effects after denial.

The assessment can conclude `Action required`, `No blocking findings` within completed agreed coverage, or `Incomplete` when material evidence is missing. Zero findings is valid. Reports and filled templates belong in the target project or requested location; report files are written only when requested or required by the calling workflow. Without project artifacts, the output is a plan or scoped threat model rather than a fabricated audit.

The skill was informed by Silva97's [Bem-vindo ao ciberapocalipse](https://www.tabnews.com.br/Silva97/bem-vindo-ao-ciberapocalipse) and accessible related material, with technical guidance checked against primary NIST, OWASP, and platform sources. Opinionated article claims are not treated as standards. See [source notes](skills/cybersec/references/sources.md) for access limits and [third-party notices](THIRD-PARTY-NOTICES.md) for attribution.

### Resources

| Resource | Purpose |
| --- | --- |
| [Entrypoint](skills/cybersec/SKILL.md) | Modes, authority, target scope, routing, and working loop. |
| [Assessment method](skills/cybersec/references/assessment-method.md) | Threat reasoning, repository baseline, evidence, severity/status, coverage, and conclusions. |
| [Threat coverage and verification](skills/cybersec/references/threat-coverage.md) | Traceable coverage, combined attack paths, negative/positive checks, structural guarantees, security-model limits, and reassessment triggers. |
| [Web and API](skills/cybersec/references/web-api.md) | Browser/service trust, authorization, business logic, inputs, and data. |
| [Credential and cryptographic controls](skills/cybersec/references/web-api.md#credentials-and-cryptographic-controls) | Passwords, security tokens, encryption, and key handling across relevant platforms. |
| [Desktop and native](skills/cybersec/references/desktop-native.md) | IPC/bridges, file access, privileged helpers, distribution, updates, and native boundaries. |
| [Mobile](skills/cybersec/references/mobile.md) | Android/iOS release, platform, storage, network, and inter-app boundaries. |
| [DevOps and supply chain](skills/cybersec/references/devops-supply-chain.md) | Dependencies, CI/build/artifact trust, cloud, IaC, containers, and Kubernetes. |
| [IT operations](skills/cybersec/references/it-operations.md) | Assets, enterprise identities, endpoints, networks, incident readiness, and recovery. |
| [AI and agentic systems](skills/cybersec/references/ai-agentic.md) | Prompt/tool boundaries, retrieval/memory isolation, unsafe output, and action scope. |
| [Assessment template](skills/cybersec/assets/security-assessment-template.md) | Adaptable threat/control/finding/evidence report. |
| [Source notes](skills/cybersec/references/sources.md) | Article attribution, primary sources, adaptation decisions, and unavailable readings. |
| [Evaluation scenarios](skills/cybersec/evals/scenarios.md) | Discovery, platform/CI/IT risks, guard controls, authorization, evidence, and validation records. |
| [OpenAI metadata](skills/cybersec/agents/openai.yaml) | Optional host display metadata and invocation prompt; no model selection. |

## UI Design Web

Use [UI Design Web](skills/ui-design-web/SKILL.md) for browser screens, responsive layout, navigation, semantics and authorized implementation. Keep the existing design system and canonical screen contract. Its optional [prototype tools](skills/ui-design-web/scripts/prototype_tools.py) validate declared token pairs and build local HTML galleries; these checks do not establish full accessibility or production usability.

```text
Use $ui-design-web to specify the checkout's loading, failure and keyboard states in the active change, then implement the reviewed flow with existing components.
```

## UI Design Android

Use [UI Design Android](skills/ui-design-android/SKILL.md) for native Compose/Views interaction, lifecycle, navigation, accessibility and authorized implementation. It owns the screen contract; Android test-authoring packages implement checks, Peer Review assesses source defects and Cybersecurity owns security assessment. Browser concepts cannot establish native behavior.

```text
Use $ui-design-android to define and implement the offline-editing journey, preserving current app decisions; verify relevant native states and report unavailable device evidence.
```

## UI Design Terminal

Use [UI Design Terminal](skills/ui-design-terminal/SKILL.md) for CLI output and interactive TUIs: hierarchy, labels/units, real viewport and selection visibility, resize, keyboard/help, progress/cancellation and recovery. Choose CLI versus TUI for the task; redirected structured output needs a separate contract. Text presence, captured rendering, task execution and developer acceptance are separate claims.

```text
Use $ui-design-terminal to compare the reference's dense statistics journey with the proposed TUI at normal and constrained sizes before expanding the implementation.
```

All three packages are standalone. The owning task agent selects the relevant platform skill; mixed-platform work can select several for distinct outcomes. Proposed UI detail belongs in the active change, or the established project screen contract; update baseline PRODUCT only after result acceptance. [UI migration and preservation](docs/ui-skill-migration.md) explains the retired name, custom installations, resource destinations and safe repeat behavior.

## Diagnose Defect

Use for an ambiguous failure, intermittent regression, or slowdown that needs a discriminating reproduction. For example, “Diagnose why retries sometimes lose a queued job.” The result records the cause evidence and remaining uncertainty. A fix and its verification follow the requested scope. [Skill](skills/diagnose-defect/SKILL.md) · [Bisection and input reduction](skills/diagnose-defect/references/localization.md)

## Behavior Testing

Use when behavior tests are the primary deliverable or test-first implementation is requested. For example, “Add a regression test for submitting twice after a lost response.” Ordinary implementation includes its own regression checks. For native Android test authoring, select the applicable native helper. [Skill](skills/behavior-testing/SKILL.md) · [Test design and intermittent failures](skills/behavior-testing/references/test-design.md)

## HTTP API

Use for concrete server changes under an existing or authorized contract. For example, “Implement this endpoint with retry-safe writes and preserve current client errors.” The output includes contract and implementation changes, caller impact, and executed checks. [Skill](skills/http-api/SKILL.md) · [Limits, caching, and endpoint evolution](skills/http-api/references/lifecycle.md)

## MCP Server

Use to implement an MCP server or an exposed capability. For example, “Expose the existing document lookup through our supported MCP client.” Keep protocol revision, transport, permission enforcement, and downstream test effects explicit. The protocol reference covers modern and legacy clients, including shared endpoints. [Skill](skills/mcp-server/SKILL.md) · [Revision checks](skills/mcp-server/references/protocol-revisions.md) · [Remote authorization](skills/mcp-server/references/authorization.md) · [Tool contracts and task evaluation](skills/mcp-server/references/tool-contracts-and-evaluation.md)

## Software Factory

Describe the desired software outcome to the host main agent with `$software-factory`. It explores with you, creates or resumes a native change, dispatches specification review, plans and implements through specialists, and verifies/reviews the integrated result. You do not need a command or prompt for each stage. When the result is ready, one explicit approval authorizes consolidation, archival, commit and normal push by default; separate/local-only instructions prevail. Feedback returns to the affected specification/tasks and checks. No SDD CLI or configurable schema is required. See the [native lifecycle](skills/software-factory/references/execution.md), [fixed records](skills/software-factory/references/change-records.md) and [closure/recovery](skills/software-factory/references/closure.md).

The [first pilot](docs/retrospectiva-piloto-fabrica-2026-11-19.md) exercised local implementation, separate review, repeated setup verification and archival. Custom-role selection and configured models remain unverified in the tested host. Confirm those capabilities in your client before requiring them as delivery gates. Use the [change checklist](docs/guia-fabrica-changes.md) for adoption.

### Durable execution records

Factory runs and substantial dependent multi-agent changes use one `docs/agents/runs/<run-id>/run.json`, or an approved existing equivalent. The orchestrator alone checkpoints it before delegation, after checked results, before/after external effects and during recovery. It stores English summaries, canonical contract links, owners, pending work, required gates and snapshot-bound evidence. Small bounded single-agent edits can remain lightweight. Setup prepares the [directory guide](skills/setup-pentapro/assets/runs-readme.md) without creating a fictional active run or replacing existing records.

The optional bookkeeping [run-state helper](skills/software-factory/scripts/run_state.py) uses Python 3.12+ and Git for `init`, `snapshot`, `save` and `check`. It detects outdated record writers, stale fingerprints on passed gates, incomplete required gates and unfinished work at completion; saves use a per-run lock and atomic replacement. Follow the [record format and recovery procedure](skills/software-factory/references/run-records.md) for commands, prerequisites and limits. Check actual files and remote effects before replaying interrupted operations. A local record cannot certify a review or remote publication by itself.

The fingerprint excludes run metadata and local prompt logs; ignored untracked outputs and external inputs need separate evidence. Preserve historical evidence when invalidating a gate. Choose project policy for versioning sanitized checkpoints; helpers never stage, commit or publish them. Post-push records can remain local for the next authorized commit. Existing customized projects adopt this contract through reviewed reconciliation. See the [local directory guide](docs/agents/runs/README.md) and [executed recovery controls](docs/factory-run-persistence.md).

### Invocation history and efficiency

Factory-role calls use append-only `docs/agents/runs/<run-id>/events.jsonl` beside the existing state record. Reuse the execution across prompts, sessions and retries; a prompt or agent does not create a directory. Standalone factory roles use one minimal real assignment run; ordinary skill calls remain outside this history. Only the orchestrator records sanitized reasons, expected/actual outcomes, evidence and observed timing/usage. Unknown metrics remain unavailable. Requested models/effort are separate from observed values.

The [event contract and helper](skills/software-factory/references/invocation-events.md) support explicit appends and per-run summaries without scanning other runs. Failed capture before managed dispatch holds dispatch; after observed effects reconcile state and retry recording only. Events are not proof of complete host capture. Retrospectives can examine rework, repeated assignments, handoff waits and cost per verified outcome without treating fewer reviews as better. Lessons reference this evidence and remain separate long-lived knowledge. Choose retention/versioning explicitly; no automatic history deletion, hooks, global configuration or telemetry service is installed. Existing projects adopt the guidance through reviewed setup reconciliation.

### Continuous improvement with PDSA

All six factory roles (`factory_spec`, `factory_implementer`, `factory_verifier`, `factory_reviewer`, `factory_retrospective`, `factory_shipper`) use a short Plan-Do-Study-Act cycle, including isolated invocations. Plan against the current project, skills, relevant lessons and checks; execute the task; study results and unexpected conditions; then make authorized corrections and rerun affected checks. Read-only roles report source corrections to their authorized owner. Repeated correction is bounded to two attempts per failure, stopping sooner without progress.

Agents return the outcome, evidence/gaps, a concise PDSA summary and any useful lesson candidate; they do not write the shared lessons record. The orchestrator checks evidence, separates cause hypotheses from confirmed causes, consolidates duplicates and alone records lessons in `docs/agents/lessons-learned.md` or the project's established equivalent. For standalone agent calls, the invoking main session serves as orchestrator. Logical names must map to the discovered host IDs; for example OpenCode uses `factory-shipper` from its filename rather than an assumed `factory_shipper` alias. If a custom agent runs as the main session directly, it finishes its role before visibly taking the recording responsibility. If recording is unavailable, the candidate is returned with persistence pending. No new lesson is a valid outcome.

Full `setup-pentapro` installs the [PDSA protocol](skills/setup-pentapro/assets/continuous-improvement.md), an [empty lessons record](skills/setup-pentapro/assets/lessons-learned.md), and project instruction pointers while preserving existing customizations and lesson history. A logging-only setup leaves these artifacts untouched. Agents consult relevant lessons on the next task and revalidate their applicability. Lessons record context, evidence, confidence, correction, prevention hypothesis, status and next verification; every entry is written in English even when the developer keeps PentaPRO specifications in Portuguese, so the collection can reuse lessons for future skill improvements. Lessons never override project policy or grant permission.

Lessons persisted after commit or push may remain local until the next authorized commit. The orchestrator reports persistence and publication separately. This process does not automatically rewrite skills or retrain models. Structural validation and authored scenarios do not establish improved quality or lower cost; evaluate actual runs before making those claims.

## Software Delivery

Coordinate dependent tasks and verify the integrated result. For example, “Implement the accepted retry change across the API, worker and existing clients.” Use the governing baseline and applicable active change, or establish the intended behavior from the request and existing project contracts. Reconcile material changes with the owning records and keep verification tied to the resulting revision. A clear localized change can use its domain procedure directly. See [Software Delivery](skills/software-delivery/SKILL.md) and its [change contract guide](skills/software-delivery/references/change-contracts.md).

## Production Operations

Use [Production Operations](skills/production-operations/SKILL.md) to choose a deployment model, configure infrastructure and CI/CD, release an exact backend revision, or operate and recover a hosted service. It covers APIs, functions, containers, workers, scheduled and batch jobs, Kubernetes, VMs and stateful dependencies. Load the relevant [AWS](skills/production-operations/references/providers/aws.md), [Azure](skills/production-operations/references/providers/azure.md), [Google Cloud](skills/production-operations/references/providers/gcp.md), [Cloudflare](skills/production-operations/references/providers/cloudflare.md) or [VPS](skills/production-operations/references/providers/vps.md) guide.

Give the agent the repository and release ref, exact target environment and resource identifiers, approved login or runner, allowed changes and cost scope, and links to the relevant deployment and recovery procedures. Complete human login, MFA or consent directly with the provider. Supply references to secrets in the approved vault or CI store. The [access guide](skills/production-operations/references/access-and-mcp.md) separates bootstrap, pipeline, runtime and observation identities and explains when to use an official MCP server, CLI or the existing pipeline.

```text
Use $production-operations to compare AWS, Cloudflare, and a VPS for this API. Identify compatibility, cost assumptions, and what access staging needs.
Use $production-operations to prepare the Cloud Run staging pipeline with federated CI access. Validate the repository changes and provide the bootstrap handoff.
Use $production-operations to deploy this image digest to the authorized staging ECS service and verify the running revision and critical API flow.
```

The [deployment brief](skills/production-operations/assets/deployment-brief.md) captures inputs and authority. The [operations record](skills/production-operations/assets/operations-record.md) captures what ran, which revision served, observed checks and recovery evidence. See the [worked examples](skills/production-operations/references/worked-examples.md), [evaluation scenarios](skills/production-operations/evals/scenarios.md) and [source notes](skills/production-operations/references/sources.md). Cloud credentials and MCP tools are configured separately for the actual target.

## Technical Research

Resolve technical uncertainty with traceable evidence. Read [skills/technical-research/SKILL.md](skills/technical-research/SKILL.md) for scope and conditional resources. Invoke `$technical-research` for this outcome. Existing project tools, contracts and authorization remain authoritative.

## Git Ship

Review, commit and publish an authorized Git snapshot, and prepare a pull request when asked. Read [skills/git-ship/SKILL.md](skills/git-ship/SKILL.md) for scope and conditional resources. Existing project tools, contracts and authorization remain authoritative.

```text
Use $git-ship to review this branch, commit the intended fix and push it.
Use $git-ship to commit only docs/ and src/api/ and push the current branch.
Use $git-ship to draft the PR body for these commits against main.
```

A ship request covers review, the requested commit and a normal push of the reviewed branch; a PR request produces a draft body. Stated paths or a scope bound what is reviewed and committed, and unrelated staged or unstaged work is preserved rather than absorbed. Reviewing does not license opportunistic fixes: a blocker is reported and stopped, and correcting it is separate work.

The workflow keeps the safety boundaries visible: mutable Git state is established before anything changes, the candidate commit is inspected exactly, secrets are checked across the whole outgoing range including values added and later deleted, and the remote ref is confirmed at the effective push repository against the recorded reviewed commit ID. Environment failures are treated explicitly — an index lock, a network or credential failure, or a failing required hook stops or leaves publication `Unverified` instead of being bypassed. Merging, auto-merge, deployment, force-push, amend and history rewrite remain outside this authorization. Invoke `$git-ship` for this outcome.

## Agent Instructions

Maintain portable software-development agent guidance. Read [skills/agent-instructions/SKILL.md](skills/agent-instructions/SKILL.md) for scope and conditional resources. Invoke `$agent-instructions` for this outcome. Existing project tools, contracts and authorization remain authoritative.

## Native Android implementation and testing

These helpers implement concrete native Kotlin/JVM/Android changes. They do not create another specification or assessment workflow. Design and implement Android screens through UI Design Android's conditional Compose/presentation/navigation references; assess Android security through Cybersecurity's Android controls. Review source and test effectiveness through Peer Review. [Ownership and every source destination](docs/SKILL-ROUTING.md) explain the boundaries.

| Helper | Example request | Main supporting resources |
| --- | --- | --- |
| [android-module-structure](skills/android-module-structure/SKILL.md) | Add the approved notes data module using the existing Gradle conventions. | [Build logic](skills/android-module-structure/references/build-logic.md), [execution](skills/android-module-structure/references/execution.md), [maintenance cases](skills/android-module-structure/evals/scenarios.md) |
| [android-data-layer](skills/android-data-layer/SKILL.md) | Implement atomic refresh while retaining cached notes after failure. | Repository/storage/transport procedures and typed-domain examples in the entrypoint |
| [android-error-handling](skills/android-error-handling/SKILL.md) | Implement cancellation-preserving HTTP error mapping with TLS failures distinguished. | Typed Result and Ktor boundary examples in the entrypoint |
| [android-di-koin](skills/android-di-koin/SKILL.md) | Wire the existing repository and destination ViewModel with the correct owner. | Binding, startup and lifetime procedures in the entrypoint |
| [android-background](skills/android-background/SKILL.md) | Implement an account-scoped idempotent synchronization worker. | WorkManager retry/initialization and Koin procedures in the entrypoint |
| [android-unit-testing](skills/android-unit-testing/SKILL.md) | Write a deterministic test for a delayed refresh cancelled during logout. | [Case catalogue](skills/android-unit-testing/references/test-cases.md), [Notes fake](skills/android-unit-testing/references/notes-fake.md) |
| [android-integration-testing](skills/android-integration-testing/SKILL.md) | Write the Room migration/data-preservation test for this schema update. | Native boundary, storage and transport test procedures in the entrypoint |
| [android-ui-testing](skills/android-ui-testing/SKILL.md) | Write a device test for the retry button and retained content. | Native host, selectors, scheduling and cleanup procedures in the entrypoint |

Implementation results are source/configuration changes and proportionate executed checks, with missing SDK/device/service evidence disclosed. Existing stacks, versions, supported behavior and user authorization govern the work. Each package retains essential instructions for standalone use and names optional companions for distinct tasks. Use the project's existing commands and contracts when a companion is absent.

## PR Quiz

[pr-quiz](skills/pr-quiz/SKILL.md) creates an explicitly requested decision-comprehension quiz for a specific GitHub PR. It is generic across platforms and separate from Peer Review: passing questions does not establish defect freedom, security or independent approval. Creating a PR alone never activates it.

Example: `Use $pr-quiz to draft a quiz about the caching and retry decisions in PR 123.` Drafting stays local; publishing requires the requested PR-edit scope. The [Python helper](skills/pr-quiz/scripts/publish_quiz.py) previews with `--dry-run` without GitHub access, then can preserve surrounding PR text while publishing through `gh` when authorized. Resolve its installed path in the target repository. Publishing requires the intended repository in `--repo` and the reviewed commit in `--head`. Earlier helper versions accepted implicit targets. Update any publication scripts to pass both options. The helper checks the current head and body before the edit and confirms the result afterward.

The [optional workflow asset](skills/pr-quiz/assets/pr-quiz.yml) grades through trusted GitHub metadata events, without running PR-head code. It is not installed as an active workflow here. Authors are ineligible by default; passes bind to the quiz content, ID and head SHA. Comment answers use the current revision token shown in the pending status. Review team policy, the pinned action, and token permissions before enabling the template. Keep its commit status informational because PRs can share the same commit SHA. Use repository review requirements for merge authorization.

Offline maintainer checks: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/pr-quiz/scripts/tests -v` and `node skills/pr-quiz/scripts/tests/workflow.cjs`. They exercise rendering/body preservation and the actual embedded grader with API doubles; they do not validate a live GitHub deployment or branch rule.

## Project agent instructions template

[skills/setup-pentapro/assets/agents.md](skills/setup-pentapro/assets/agents.md) is an adaptable project instruction template. Setup preserves existing instructions, includes the permanent motivational manifesto and embeds its complete prompt rule directly in the target project’s `AGENTS.md`.

When `docs/agents/setup-notes.md` exists, PentaPRO reads its deferred facts on the next pass, preserves their status and provenance, and links them to the owning pillars.

The template supplies rules for native changes, scoped work, implementation, validation, review, security, collaboration, and handoff. It routes work by outcome and lets the project set when direct edits, exploration, or prior specification apply. It identifies the five pillar documents and the cumulative UI specification, and explains ownership, resumption, and evidence states. It also carries the mandatory repository-scoped prompt-logging rule in full, including safe local storage, capture verification, redaction and failure handling. Setup does not install hooks or plugins. Fill in the project's skill locations and commands; unknown fields stay `[FILL IN]` under a temporary marker until `$penta-pro` reconciles the file after the specification exists. The project chooses its stack, source layout, model, and test framework. Artifacts use English by default, with exceptions for required identifiers, literal data, and localization. Keep detailed specifications and runbooks in their authoritative documents and link them from the project guide.

## Guides and case studies

See the [factory quality maintenance assessment](docs/factory-quality-maintenance.md) and [script/test inventory](docs/factory-script-inventory.md) for the current changes and readiness limits. The [2026-11-25 harness review](docs/harness-review-2026-11-25.md) preserves its earlier checked snapshot.

The PDFs are Portuguese teaching editions dated November 2026. The development guide shows 22 skills and the Castas retrospective shows 21; their five-file PentaPRO examples predate the repository-root topic layout. Follow the current [catalog](#available-skills), [routing map](docs/SKILL-ROUTING.md) and [PentaPRO skill](skills/penta-pro/SKILL.md) for new projects and specification updates. The installed `SKILL.md`, this catalog, and the target tool's documentation govern current commands and versions. These PDFs are historical teaching material; use the native lifecycle and migration guide for current adoption.

- [Development with agents](docs/guia-consolidado-desenvolvimento-com-agentes.pdf) covers direct changes, vibe coding and prototype promotion, project-native SDD and OpenSpec, Android, web, desktop, HTTP APIs, MCP servers, workers, and deployment. The revised edition explains OpenSpec 2.0 discovery and distinguishes delta validation from verification of the consolidated capability.
- [Castas Android retrospective](docs/relatorio-retrospectiva-castas-android.pdf) shows how environment checks, cross-platform parity, device tests and release evidence changed during one project.
- [SDD walkthrough notes](docs/SDD_step-by-step.md) collect separate working drafts for product discovery and project constitutions using Spec Kit. Use the workflow above for current collection guidance.
- [Software factory v1 comparison](docs/software-factory-v1-comparison.md) explains the current portable package and remaining pilot evidence. The [original factory proposal](docs/software-factory-workflow.md) is a dated design record.
- [Greenfield and brownfield scenarios](docs/pentapro-cenarios-sdd.md) explain the native lifecycle in Portuguese, including authority, bounded correction and resumption.
- [Guia da fábrica para changes](docs/guia-fabrica-changes.md) is a Portuguese checklist for setting up a project, requesting a change, reviewing delivery and conducting the retrospective.
- [Adoption plan](docs/ANTHROPIC-ADOPTION-PLAN.md), [evaluation procedure](docs/SKILL-EVALUATION.md) and [maintenance review](docs/FINAL-SKILL-REVIEW.md) describe how to adopt or evaluate changes to the collection.

## Repository structure

Each skill lives in its own directory under `skills/` at the repository root and follows the [Agent Skills specification](https://agentskills.io/specification). Shared usage documentation and notices live at the root. Every skill carries the MIT notice inside its directory for standalone installation.

```text
pentapro/
├── README.md
├── AGENTS.md                  Repository instructions and local prompt-log policy
├── pentapro/                  Baseline, active changes and process status
├── .codex/agents/             Optional ignored local Codex role definitions
├── .github/agents/            Tracked Copilot role definitions
├── LICENSE
├── THIRD-PARTY-NOTICES.md
├── plugin.json                 PentaPRO package identity and source skill list
├── package.json                Generated OpenCode Git/local package metadata
├── plugin/                     OpenCode adapter and generated skill catalog
├── .codex-plugin/              Codex compatibility manifest
├── .antigravity-plugin/        Antigravity overlay
├── .claude-plugin/             Compatibility marketplace catalog
├── docs/                       Guides, routing, reviews and docs/agents/ records
├── .github/workflows/validate.yml
├── evals/
├── scripts/
└── skills/                   Canonical skill packages
    ├── software-delivery/
    ├── software-factory/
    ├── production-operations/
    │   ├── SKILL.md
    │   ├── agents/
    │   ├── assets/
    │   ├── evals/
    │   └── references/
    ├── technical-research/
    ├── setup-pentapro/
    │   ├── SKILL.md
    │   ├── assets/
    │   ├── evals/
    │   └── references/
    ├── git-ship/
    ├── agent-instructions/
    ├── diagnose-defect/
    ├── behavior-testing/
    ├── http-api/
    ├── mcp-server/
    ├── android-module-structure/
    ├── android-data-layer/
    ├── android-error-handling/
    ├── android-di-koin/
    ├── android-background/
    ├── android-unit-testing/
    ├── android-integration-testing/
    ├── android-ui-testing/
    ├── pr-quiz/
    ├── penta-pro/
    │   ├── SKILL.md
    │   ├── agents/
    │   ├── assets/
    │   │   ├── penta-pro-template.md
    │   │   ├── product.md
    │   │   ├── project.md
    │   │   ├── production.md
    │   │   ├── proof.md
    │   │   └── process.md
    │   ├── evals/
    │   ├── scripts/
    │   └── references/
    ├── peer-review/
    │   ├── SKILL.md
    │   ├── agents/
    │   ├── assets/
    │   ├── evals/
    │   └── references/
    ├── cybersec/
    │   ├── SKILL.md
    │   ├── agents/
    │   ├── assets/
    │   ├── evals/
    │   └── references/
    ├── ui-design-android/
    ├── ui-design-terminal/
    └── ui-design-web/
        ├── SKILL.md
        ├── agents/
        ├── assets/
        ├── evals/
        ├── references/
        └── scripts/
```

The tree is a navigation overview, not a complete inventory. `plugin/catalog.json` is generated by `scripts/package_plugin.py`; canonical agent templates live in `skills/setup-pentapro/assets/agents/`, not the installed host copies.

The documentation and maintenance directories serve different readers:

- `docs/` holds the [guides and case studies](#guides-and-case-studies) for developers and maintainers.
- `evals/` holds [evaluation cases](evals/cases.json), synthetic project fixtures, project-policy overlays, independent checks, and [trial results](evals/RESULTS.md). These let maintainers compare agent behavior on the same tasks and inspect the resulting artifacts.
- `scripts/` holds the [collection validator](scripts/validate_collection.py), its dependency list, the [evaluation runner](scripts/run_skill_evals.py), and offline validator/runner tests. Use the [validation instructions](#validation-and-improvement) and [evaluation procedure](docs/SKILL-EVALUATION.md) from a checkout of the collection. A full repository clone includes both directories.

Inside a skill package, `SKILL.md` contains metadata and runtime instructions. Optional `agents/` files adapt host presentation, `assets/` holds output templates, and `references/` holds conditional detail. Some packages also carry their own `evals/` maintenance cases or `scripts/` helpers and tests. These nested directories belong to the package and can accompany its installation. For example, UI Design Web carries its [local prototype helper](skills/ui-design-web/scripts/prototype_tools.py). Create only the directories a skill needs.

## Maintenance and new skills

Authoring was checked against [OpenAI's skill guide](https://learn.chatgpt.com/docs/build-skills) and [Anthropic's best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) on 2026-10-25. These are maintainer references, not runtime dependencies. Recheck relevant guidance when changing packaging, discovery, or model support; evaluate upstream changes deliberately rather than importing them automatically.

### Validation and improvement

The Linux/POSIX [synthetic terminal journey](evals/check_factory_journey.py) checks a small input/report/PTY/error-recovery path, with seeded failure controls in its tests. It is separate from live product, host-discovery and cost-effectiveness trials.

The [factory quality maintenance assessment](docs/factory-quality-maintenance.md) maps all 111 retained proposals, and the [script inventory](docs/factory-script-inventory.md) identifies tests and optional integration gaps. See the [UI migration](docs/ui-skill-migration.md) before replacing an older installation.

Install the maintainer dependency with `python3 -m pip install -r scripts/requirements-validation.txt` in a development environment. Run `python3 scripts/validate_collection.py` from this repository root. It checks frontmatter, local inline links and ATX-heading anchors outside fenced examples, catalog versions, licenses, installation coverage, and supported optional `agents/openai.yaml` fields. Relative links in shipped packages must resolve inside the package, including after a standalone install. Refer to optional companions by name and give maintainers upstream links for provenance. The [validation workflow](.github/workflows/validate.yml) runs the collection gate and offline Python and Node helper tests. Model trials and runtime compatibility checks use the [evaluation procedure](docs/SKILL-EVALUATION.md).

To reproduce the local collection checks, use a POSIX development environment with Git, Python 3.12+ and Node.js 24, matching the CI runtime family. After installing the dependency above, run these commands from the collection root. The validator tests use disposable Git inventories. The root suite also runs isolated execution-state recovery controls, with source-change, failed-write and uncertain-effect cases; see [persistence evidence](docs/factory-run-persistence.md). The evaluator isolation cases need Linux with Bubblewrap and libseccomp, and native SDD fixtures need only the documented local test prerequisites. Check the test summary for skips. The quiz tests use API doubles. [Evaluation prerequisites](docs/SKILL-EVALUATION.md)

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/package_plugin.py --check
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_collection.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_skill_evals.py --check-cases
PYTHONDONTWRITEBYTECODE=1 python3 evals/check_factory_journey.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/penta-pro/scripts/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/ui-design-web/scripts/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/pr-quiz/scripts/tests -v
node skills/pr-quiz/scripts/tests/workflow.cjs
node --test scripts/tests/test_agents_log.mjs
node --test scripts/tests/test_opencode_plugin.mjs
git diff --check
```

These are collection-maintenance prerequisites, not requirements for reading or installing each skill manually. Model trials and the optional MCP SDK smoke test have separate setup and evidence limits in the [evaluation procedure](docs/SKILL-EVALUATION.md).

See the [current source assessment](docs/factory-quality-maintenance.md), [script inventory](docs/factory-script-inventory.md) and [review history index](docs/reviews.md) for current evidence and historical report scope.

Use the [evaluation procedure and synthetic Codex trials](docs/SKILL-EVALUATION.md) to decide whether to add, revise, or retire a skill. The [review-report follow-up](docs/review-followup-2026-11-22.md) records the latest bounded corrections, fresh checks and limits. The [native SDD maintenance review](docs/native-sdd-review.md) preserves its migration checks and limits. The [earlier maintenance follow-up](docs/maintenance-final-follow-up-2026-11-21.md) preserves its evaluated snapshot. The [earlier closing maintenance audit](docs/maintenance-review-2026-11-21.md) records its evaluated snapshot; historical reports and exported PDFs retain their original snapshot and do not establish current behavior. The [software factory assessment](docs/SKILL-ASSESSMENT.md) and [collection review](docs/COLLECTION-REVIEW.md) retain earlier source decisions and validation limits. The [final maintenance review](docs/FINAL-SKILL-REVIEW.md) records the later per-package assessment and distribution review.

Git Ship was renamed from `git-delivery` in version 2.0.0. The package directory, frontmatter `name` and invocation are `git-ship`. The earlier name is not retained as a forwarding alias, because a second entrypoint would create duplicate discovery. Remove an older `git-delivery` copy when upgrading a project and update references that invoke it.

The Git Ship 2.1.0 maintenance pass strengthened the delivery contract: a stated path list bounds the reviewed set, delivery never silently fixes or refactors product code, documentation moves revalidate links and anchors, publication is confirmed by comparing `git ls-remote` with `git rev-parse HEAD`, and index, network and hook failures have explicit stop or `Unverified` outcomes. A disposable trial confirmed that a plain commit absorbs unrelated staged entries and that a path-limited commit substitutes working-tree content, while an isolated index preserves both the unrelated staged selection and a partially staged intended blob. These are single-repository structural and executed checks, not a model benchmark or a hosted-forge trial.

The pstack-informed update adds caller-facing contract sketches and verification recipes to PentaPRO, safety-premise and measurement checks to Peer Review, model/enforcement distinctions to Cybersecurity, and instance-aware journey evidence to UI Design. These additions are conditional; the skills keep their existing output contracts and introduce no pstack dependency. [Research attribution and limits](THIRD-PARTY-NOTICES.md#cursor-pstack-research) identify the pinned source and adaptations.

The Elephant & Goldfish Model informed PentaPRO's hypothesis challenge and review of the five pillar artifacts, Peer Review's checks of current documentation claims affected by a change, and UI Design's walkthrough from the documented entry to the result and recovery. [Research attribution and limits](THIRD-PARTY-NOTICES.md#elephant--goldfish-model-research)

Use each skill's evaluation cases before expanding its instructions. Compare matched tasks with and without the skill on the models and hosts actually used. Check activation, preserved decisions, invented facts, unnecessary questions, substantiated defects, false positives, material misses, coverage honesty, and unintended actions. Record actual time and usage when available, and retest after relevant model or instruction changes.

The collection review on 2026-11-06 strengthened handoffs across all 13 skills, retained project-owned contracts and made sample stacks conditional. Android corrections clarify Koin worker parameters, periodic-work termination, account-scoped commit races, pure StateFlow updates and version-sensitive build/test configuration. The optional PR quiz now separates reflected text from bot control markers, rejects ambiguous blocks/keys, renders question text literally and pins its action dependency to an official release commit with narrower permissions. Its grading remains an educational aid. Existing guidance covers safe test execution, staged versus working-file review, type/model limits, design fidelity and companion-document ownership. See the [validation scope and maintenance record](docs/SKILL-ROUTING.md#validation-scope) for actual results and remaining limits; these checks do not establish reliability on every model.

The closing audit additionally corrected external specification/task ownership, effective built-in Kotlin mode, literal-query and update/cascade semantics, final-write account isolation, conditional Android UI examples and strict JSON input handling in both helpers. Regression checks and a bounded PentaPRO forward trial are recorded in [the closure audit](docs/SKILL-ROUTING.md#closing-audit-after-sdd-and-layered-review-integration--2026-11-06). These changes clarify concrete decisions and failure modes without adding mandatory stages or another framework dependency.

Keep active versions in `SKILL.md`, this README, and any versioned output template aligned. When behavior changes, reconcile descriptions, UI metadata, templates, references, and evaluation cases. Validate local links and anchors from each file's location. Retain historical research dates and trial versions with their original scope; a package update does not rerun or broaden earlier evidence.

Where present, evaluation files and executable tests record the package's actual cases, audits/trials and limitations. A package without a recorded trial has no implied behavioral evaluation. Shorter documents and structural checks do not prove better task performance. No cross-model accuracy, cost, or efficiency benchmark is claimed. Prefer focused corrections supported by observed failures over universal rules for isolated cases.

### Adding a new skill

1. Create a root-level directory whose name matches the skill's `name`, using lowercase letters and hyphens.
2. Add `SKILL.md` with a clear description, focused instructions, and only the supporting resources the workflow needs.
3. Add an entry to [Available skills](#available-skills) and a dedicated section in this README covering purpose, example requests, output/boundaries, and resource links. Keep shared installation and maintenance guidance in their common sections.
4. Keep the shared README and canonical MIT notice at the repository root. Include a matching `LICENSE` inside each skill for standalone installation. Establish redistribution terms for any new import and preserve its applicable notices. Validate metadata and internal links, and run meaningful evaluation cases before claiming improvements.

## License and attribution

All 26 packages use the [MIT License](LICENSE) and include a copy of its notice. This covers the imported Android and PR Quiz material, including references embedded in UI Design and Cybersecurity, and the adapted Setup PentaPRO package, under the MIT redistribution permission confirmed by the repository maintainer. Retain the license and applicable attribution when redistributing a package. See [third-party notices](THIRD-PARTY-NOTICES.md) for the source mapping.

The source research for [PentaPRO](skills/penta-pro/references/sources.md), [Peer Review](skills/peer-review/references/sources.md), [Cybersecurity](skills/cybersec/references/sources.md), and [UI Design Web](skills/ui-design-web/references/sources.md) records their inputs and adaptation decisions. [Third-party notices](THIRD-PARTY-NOTICES.md) preserve upstream attribution; the repository license does not relicense external articles. Attribution does not imply affiliation, endorsement, or a runtime dependency.

## Data privacy

- Setup PentaPRO installs a project instruction to append prompts and attachment names to local `AGENTS.log`. The rule excludes log files from Git, uses best-effort redaction and relies on agent compliance. The log has no automatic rotation. Review access and retention under the project’s policy.

- The optional UI prototype helper reads local inputs and writes an HTML file. The bundled viewer runs locally and keeps the selected route, theme, and width in the URL fragment.
- PR Quiz preview runs locally. Publishing writes quiz questions and an encoded answer key to the GitHub PR body. If the optional grader is installed, answers and results can appear in PR checkboxes, comments, and commit statuses. Access and retention follow the repository and GitHub settings.
- The evaluation runner saves prompts, agent events, and outputs to a local temporary directory. Model trials send the supplied prompt and any context selected by the agent to the configured model service. Use synthetic fixtures for collection trials.
- The agent host, installer, and external tools have their own data policies. The optional Vercel installer documents telemetry settings. [Installer telemetry](https://github.com/vercel-labs/skills#telemetry)

---

<p align="center"><small>
Copyleft © 2026 <a href="https://x.com/teknolista">Raul Bras</a> 🇧🇷 Published under the MIT license. <br>
Made in Brazil, in the Land of Oz (SP) , with 🌭 🍕 and AI 🤖.
</small></p>


## AI development workflow

This repository uses project-local PentaPRO skills, factory profiles and the native five-dimensional change process. See [agent instructions](AGENTS.md), the [continuous improvement protocol](docs/agents/continuous-improvement.md), [lessons](docs/agents/lessons-learned.md) and [execution-record guide](docs/agents/runs/README.md). Lessons are recorded in English.

### Optional maintenance helpers

Setup's [instruction-section planner](skills/setup-pentapro/scripts/plan_instruction_sections.py) can propose canonical manifesto and prompt-policy insertion while preserving adjacent text and rejecting conflicts. It writes a proposal to stdout, never the project file: `python3 /installed/setup-pentapro/scripts/plan_instruction_sections.py --root /actual/project`. Review the proposal privately, recheck the original hash and target before separately applying it; never redirect stdout onto the original AGENTS.md. A plan is not proof of setup or an atomic upgrade.

Factory's [command receipt helper](skills/software-factory/scripts/command_evidence.py) is optional POSIX bookkeeping for explicitly trusted commands. It records actual failure/timeout/interruption and input snapshot without raw arguments/output; read the [receipt contract](skills/software-factory/references/run-records.md#optional-command-receipts) for authority, privacy, process-group and receipt limits.
