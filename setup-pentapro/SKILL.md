---
name: setup-pentapro
description: "Configure prompt persistence in the current project's AGENTS.md. Create or update its complete, self-contained rule for saving prompts in AGENTS.log while preserving existing project instructions."
license: MIT
metadata:
  version: "1.4.0"
---

# Setup PentaPRO

Configure only the current project's root `AGENTS.md` with the complete prompt-persistence rule below. This skill contains every instruction needed for setup; no policy document or packaged template needs to be read or copied.

## Setup procedure

1. Locate the current project root and read its applicable instructions and existing `AGENTS.md`, if present. Use the current project's root, not the installed skill directory or an unrelated parent repository. Resolve an ambiguous project boundary before writing.
2. Create `AGENTS.md` with a `# AGENTS.md` heading and the complete section below if it does not exist. For an existing file, insert or update one `## Prompt Logging` section in place, preserving unrelated content and order. Consolidate duplicate prompt-logging sections into one complete rule. Preserve compatible project-specific logging requirements; surface a conflicting requirement rather than silently discarding it.
3. Write the entire rule directly into `AGENTS.md`. Keep its format, timing, scope, attribution, attachment handling, redaction, duplicate prevention, append-only safeguards and failure handling. The section must stand alone: no links, imports, or instructions to consult another file for the rule. `AGENTS.log` is the prompt destination, not an external policy source.
4. Re-read the result and inspect the diff. Verify the complete rule is present exactly once and unrelated instructions are preserved. If already configured correctly, leave the file unchanged. Report the created, updated or unchanged `AGENTS.md` and that prompts must be saved in `AGENTS.log`; describe any unresolved conflict or failed write accurately.

The only setup output is `AGENTS.md`. Preserve other files, including `CLAUDE.md`, ignore configuration, logs and existing specifications. Apply any prompt-logging instructions already governing this session; configuring the rule does not authorize rewriting log history. Do not install or configure hooks, plugins, slash commands, or global agent settings. Tracker setup, labels, domain migrations, specification initialization, project-fact interviews and broad instruction-template seeding are outside this skill's current scope. Execute the requested setup without an additional approval step when the project boundary and rule are clear.

## Complete rule to write into AGENTS.md

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
