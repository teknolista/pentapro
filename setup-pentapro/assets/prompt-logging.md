# Prompt Logging

Mandatory rule for every AI agent and model working in this repository. The root instruction file carries the short operational version; this document defines the entry format, the capture mechanisms, security, concurrency, and limits.

## Rule

Every prompt sent to an AI agent working in this repository must be appended to `AGENTS.log` at the repository root **before any work is done on it**, including prompts sent to subagents. With a repository hook the append happens before the model request; with instruction-based capture it is the agent's first action. A prompt must never be acted on unlogged. If the append fails, stop the work, fix the write, backfill the missing prompts, and only then continue.

- **Scope:** every interaction, with no exception.
- **Integrity:** append only. Never rewrite, reorder, or delete entries.
- **Privacy:** keep secrets and unnecessary personal data out of prompts. When they arrive anyway, replace them with `[REDACTED]` before logging.
- **Silence:** logging produces no confirmation in the conversation; report failures only.
- **Versioning:** the log is local. It is listed in `.gitignore`, is never committed, and must not be published.
- **Repository scope:** this rule applies to this repository only. Never configure it in the user's global agent configuration or in another repository.

## Entry format

Each entry is a header followed by the prompt text:

```markdown
## Wed, 18 Nov 2026 09:14:05 -0300 | provider/model (agent name)
The full prompt, with its spacing and line breaks preserved.

```

- **Date and time:** RFC 5322 local time with the UTC offset, for example `Wed, 18 Nov 2026 09:14:05 -0300`.
- **Agent and model:** `provider/model`, then the receiving agent in parentheses. The provider removes ambiguity between same-named models.
- **Body:** the prompt exactly as sent. Do not rewrite, summarize, or reformat it.
- **Separator:** one blank line after the body; consecutive entries are separated by that line.
- **Attachments:** record them as `[attachment: <name>]` where they were sent, because binary content is not text.

## How logging happens

### Primary: project instructions

The root instruction file (`AGENTS.md`, or `CLAUDE.md` when that is the file this project uses) states the rule, so every agent sees it on every request. The agent appends the entry as its first action. This path depends on the model following instructions and has no mechanical guarantee.

### Optional: repository-scoped hook

Where the host documents a project-scoped hook that runs before each model request, a hook can enforce the rule mechanically. Keep it inside the repository — for example, an OpenCode project plugin under `.opencode/plugins/` or the equivalent documented project configuration of another harness. Never place it in the user's global configuration.

A hook must:

1. select only real user prompts, excluding messages injected by the harness (system reminders, environment context, conversation checkpoints, plan-mode notices);
2. append synchronously before the request continues, and abort the request if the write fails;
3. preserve the prompt text and redact known secret patterns;
4. avoid duplicating an entry already written by the instruction layer.

Verify a new hook with a test prompt and confirm that exactly one entry was written. Record the host and version that were tested, because plugin APIs change between releases.

### Existing hook

If the repository already logs prompts, verify its entry instead of creating a second one. One mechanism is enough; a duplicate rule or hook produces duplicate entries.

## Security

Redaction is best effort. It covers common patterns — PEM private keys, `sk-`/`rk-`/`pk-` keys, `ghp_`/`github_pat_` tokens, `AKIA` keys, `AIza` keys, `xox*` tokens, JWTs, `Bearer` values, and values after `password`, `secret`, `token`, or `api_key` — but it does not identify personal data or unknown formats. Pasting secrets into prompts remains prohibited. A secret that reached the log must be revoked, not merely deleted: the file is local, but the value has already circulated.

## Concurrency

The log is opened in append mode (`O_APPEND`), so simultaneous agents do not overwrite each other's write position. The order of concurrent entries is not guaranteed, and a very large entry can interleave with another. For audit, read the set of entries, not their absolute order.

## Limits

- Prompts that never reach a model request (for example, cancelled before sending) are not logged.
- Manual capture depends on model compliance; only a hook can enforce it mechanically.
- A hook depends on the host continuing to offer the event it uses; a host update may require adjustment and revalidation.
- Deduplication is in memory only in some implementations: restarting the host and resuming a session may log earlier prompts again. Accept duplicates rather than editing the log.
- There is no automatic rotation. Rotate manually by copying the file and starting a new one; never edit existing entries.
- The log can contain sensitive operational text. Keep it out of Git, restrict access, and treat it as local audit data.

## Maintenance

- Keep `AGENTS.log` and `AGENTS.log.*` in `.gitignore`.
- Rotate by copying the current file to a dated name (also ignored) and starting a fresh `AGENTS.log`.
- Never change the rule to make a failing write look successful.
