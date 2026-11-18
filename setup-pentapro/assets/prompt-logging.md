# Prompt Logging

Mandatory rule for every AI agent and model working in this repository. The root instruction file carries the short operational version; this document defines the entry format, the capture mechanisms, security, concurrency, and limits.

## Rule

Every prompt sent to an AI agent working in this repository must be appended to `AGENTS.log` at the repository root **before any work is done on it**, including prompts sent to subagents. With a project hook the append happens before the model request; with instruction-based capture it is the agent's first action. A prompt must never be acted on unlogged. If the append fails, stop the work, fix the write, backfill the missing prompts, and only then continue.

- **Scope:** every interaction, with no exception.
- **Integrity:** append only. Never rewrite, reorder, or delete entries.
- **Privacy:** keep secrets and unnecessary personal data out of prompts. When they arrive anyway, replace them with `[REDACTED]` before logging.
- **Silence:** logging produces no confirmation in the conversation; report failures only.
- **Versioning:** the log is local. It is listed in `.gitignore`, is never committed, and must not be published.
- **Repository scope:** this rule applies to this repository only. Setup never writes it into the user's global agent configuration, and the repository must never depend on one developer's global capture.
- **One mechanism per host:** a project hook and a personal global capture for the same host must not both write entries. Pick one, or make the personal capture yield to the project hook.

## Entry format

Each entry is a header followed by the prompt text:

```markdown
## Wed, 18 Nov 2026 09:14:05 -0300 | provider/model (agent build, host opencode)
The full prompt, with its spacing and line breaks preserved.

```

- **Date and time:** RFC 5322 local time with the UTC offset, for example `Wed, 18 Nov 2026 09:14:05 -0300`.
- **Attribution:** `provider/model`, then the receiving agent and the host in parentheses. The provider removes ambiguity between same-named models. When the host does not expose a model, use `<host>/unknown`; when the host is the provider, `host` may be omitted.
- **Body:** the prompt exactly as sent. Do not rewrite, summarize, or reformat it. An empty prompt is recorded as `[empty prompt]` so the event is still visible.
- **Separator:** one blank line after the body; consecutive entries are separated by that line.
- **Attachments:** record them as `[attachment: <name>]` where they were sent, because binary content is not text.

## How logging happens

### Primary: project instructions

The root instruction file (`AGENTS.md`, or `CLAUDE.md` when that is the file this project uses) states the rule, so every agent sees it on every request. The agent appends the entry as its first action. This path depends on the model following instructions and has no mechanical guarantee.

### Optional: project hook

A project-scoped hook enforces the rule mechanically. It is optional, versioned with the repository, and installed only with the developer's approval. The shipped implementation is one shared core plus thin host adapters:

```text
scripts/agents-log/core.mjs        entry format, redaction, safe append contract
scripts/agents-log/log-prompt.mjs  stdin adapter for command hooks
.opencode/plugins/agents-log.ts    OpenCode project plugin adapter
```

The core reads the host payload, extracts the prompt, formats the entry, applies best-effort redaction, and appends synchronously with owner-only permissions. It produces no output on success. On failure it writes the reason to stderr and exits non-zero; the OpenCode adapter throws instead.

| Host | Project configuration | Event | Can block an unlogged prompt? |
| --- | --- | --- | --- |
| OpenCode | `.opencode/plugins/agents-log.ts` | `session.hook("context")` | Yes, the request is aborted |
| Claude Code | `.claude/settings.json` | `UserPromptSubmit` | Yes, exit 2 |
| Codex CLI | `.codex/hooks.json` | `UserPromptSubmit` | Yes, exit 2 or `decision: block` |
| Cursor | `.cursor/hooks.json` | `beforeSubmitPrompt` | Yes, exit 2 or `continue: false` |
| GitHub Copilot CLI | `.github/hooks/<name>.json` | `userPromptSubmitted` | No, hook output is ignored |

The exact configuration entries, merge rules, trust requirements, and verification steps are in the skill's `assets/prompt-logging/hosts.md`. A hook requires Node.js 18 or newer; without it, keep the instruction rule and do not install a hook.

A command hook must reject a payload that has no recognized prompt field; only an explicitly empty prompt is recorded as `[empty prompt]`. The logger must also refuse a symlink or non-regular log path so a repository-local hook cannot redirect prompt text outside the repository.

A hook must:

1. select only real user prompts, excluding messages injected by the harness (system reminders, environment context, conversation checkpoints, plan-mode notices);
2. append synchronously before the request continues, and signal failure so the host can block;
3. preserve the prompt text and redact known secret patterns;
4. avoid duplicating an entry already written by another mechanism for the same host.

Verify a new hook with a test payload and a real prompt, and confirm that exactly one entry was written. Record the host and version tested, because plugin and hook APIs change between releases.

### Personal global capture

A developer may keep a personal capture in the agent's global configuration, outside this repository. It is a convenience for projects that do not ship a hook, not part of this repository's setup, and never a requirement. It must not duplicate a project hook: the OpenCode personal plugin, for example, should check `globalThis.__agentsLogProjectCapture` and skip logging when the project adapter is loaded. The repository's rule and any committed hook must stand on their own.

### Existing hook

If the repository already logs prompts, verify its entry instead of creating a second one. One mechanism per host is enough; a duplicate rule or hook produces duplicate entries.

## Security

Redaction is best effort. It covers common patterns — PEM private keys, `sk-`/`rk-`/`pk-` keys, `ghp_`/`github_pat_` tokens, `AKIA` keys, `AIza` keys, `xox*` tokens, JWTs, `Bearer` values, and values after `password`, `secret`, `token`, `senha`, or `api_key` — but it does not identify personal data or unknown formats. Pasting secrets into prompts remains prohibited. A secret that reached the log must be revoked, not merely deleted: the file is local, but the value has already circulated.

The core creates the log with owner-only permissions (`0600`) when it creates the file and refuses symlink, hard-linked, or non-regular log paths. Treat the log as local audit data, restrict access, and keep it out of Git.

## Concurrency

The log is opened in append mode (`O_APPEND`), so simultaneous agents do not overwrite each other's write position. The order of concurrent entries is not guaranteed, and a very large entry can interleave with another. For audit, read the set of entries, not their absolute order.

## Limits

- Prompts that never reach a model request (for example, cancelled before sending) are not logged.
- Manual capture depends on model compliance; only a hook can enforce it mechanically, and only where the host lets a hook block.
- GitHub Copilot CLI ignores the output of `userPromptSubmitted`: the hook records but cannot stop an unlogged prompt. The instruction rule remains the enforcement layer there.
- A hook depends on the host continuing to offer the event it uses; a host update may require adjustment and revalidation. Record the tested host and version.
- A project hook requires Node.js 18 or newer on the machine that runs it.
- If the host's configuration directory is ignored by Git, the hook is local to that machine. The rule still applies, but the team does not get mechanical capture until the configuration is committed or installed another way.
- Deduplication is in memory only in some implementations: restarting the host and resuming a session may log earlier prompts again. Accept duplicates rather than editing the log.
- There is no automatic rotation. Rotate manually by copying the file and starting a new one; never edit existing entries.
- The log can contain sensitive operational text. Keep it out of Git, restrict access, and treat it as local audit data.

## Maintenance

- Keep `AGENTS.log` and `AGENTS.log.*` in `.gitignore`.
- Rotate by copying the current file to a dated name (also ignored) and starting a fresh `AGENTS.log`.
- Never change the rule to make a failing write look successful.
- When a host updates its hook API, re-run the smoke test, confirm one entry, and update the recorded version.
