# Host hook recipes

How to connect a coding agent's project-scoped prompt event to the shared core in this folder. Use this file only when the developer chooses mechanical capture; the root instruction rule remains the baseline for every host.

## Prerequisites

- Node.js 18 or newer is available as `node`. If it is not, do not install a hook; keep the instruction rule and report the missing prerequisite.
- `AGENTS.log` and `AGENTS.log.*` are in `.gitignore`.
- The project has, or will have, `scripts/agents-log/core.mjs`; command-based hosts also need `scripts/agents-log/log-prompt.mjs`. OpenCode's adapter lives at `.opencode/plugins/agents-log.ts`.
- The hook configuration is merged into the host's existing project file. Never replace an existing hooks array, reorder entries, or drop another tool's hook.

## Choose the host

| Host | Project configuration | Event | Payload field | Can block? |
| --- | --- | --- | --- | --- |
| OpenCode | `.opencode/plugins/agents-log.ts` | `session.hook("context")` | message content | Yes, a thrown error aborts the request |
| Claude Code | `.claude/settings.json` | `UserPromptSubmit` | `prompt` | Yes, exit 2 |
| Codex CLI | `.codex/hooks.json` | `UserPromptSubmit` | `prompt` | Yes, exit 2 or `decision: block` |
| Cursor | `.cursor/hooks.json` | `beforeSubmitPrompt` | `prompt` + `attachments` | Yes, exit 2 or `continue: false` |
| GitHub Copilot CLI | `.github/hooks/<name>.json` | `userPromptSubmitted` | `prompt` | No, hook output is ignored |
| Gemini CLI | verify the installed version's hook docs | verify | verify | Verify before adding an entry |

Detect the host from repository markers, installed CLIs and the user's configuration; confirm the list instead of guessing. A `.github/` directory alone does not prove Copilot, and `AGENTS.md` is used by several hosts.

## OpenCode

1. Copy `core.mjs` to `scripts/agents-log/core.mjs`.
2. Copy `opencode.ts` to `.opencode/plugins/agents-log.ts`, creating the directory if needed. OpenCode auto-loads plugins from `.opencode/plugins/`; do not add a single-file path to the `plugins` array, because configured local paths must be directories or packages.
3. If the developer has the personal `agents-log` plugin in the OpenCode global configuration, make it check `globalThis.__agentsLogProjectCapture` inside its context hook and return early when the project adapter is loaded. If it cannot be updated, keep one mechanism: either the project hook or the personal capture, not both.
4. Verify with a real prompt and confirm exactly one new entry.

## Claude Code

Merge into `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": [
              "${CLAUDE_PROJECT_DIR}/scripts/agents-log/log-prompt.mjs",
              "--host",
              "claude-code",
              "--root",
              "${CLAUDE_PROJECT_DIR}"
            ],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

- `args` is the exec form, so `${CLAUDE_PROJECT_DIR}` is substituted without shell quoting problems.
- If the installed version does not support `args` in hooks, use one shell command with quoted placeholders instead.
- The workspace must be trusted before project hooks run. Tell the user, and do not weaken their trust settings.

## Codex CLI

Merge into `.codex/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node \"$(git rev-parse --show-toplevel)/scripts/agents-log/log-prompt.mjs\" --host codex --root \"$(git rev-parse --show-toplevel)\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

- Codex recommends resolving repository paths from the Git root because the session may start in a subdirectory.
- Codex requires the user to review and trust the hook with `/hooks`. A changed hook needs a new review.
- `PreModelRequest` is an alternative when the goal is one entry per model request, but it does not receive the prompt text. Use `UserPromptSubmit` for prompt logging.

## Cursor

Merge into `.cursor/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "beforeSubmitPrompt": [
      {
        "command": "node scripts/agents-log/log-prompt.mjs --host cursor --root .",
        "timeout": 10
      }
    ]
  }
}
```

- Project hooks run from the project root; keep the relative script path.
- Exit 2 blocks the submission. The core's normal failure path is exit 2.
- Cursor cloud agents load project hooks from `.cursor/hooks.json`; the user-level file does not travel to them.

## GitHub Copilot CLI

Merge into a new or existing `.github/hooks/<name>.json`:

```json
{
  "version": 1,
  "hooks": {
    "userPromptSubmitted": [
      {
        "type": "command",
        "bash": "node scripts/agents-log/log-prompt.mjs --host copilot --root .",
        "powershell": "node scripts/agents-log/log-prompt.mjs --host copilot --root .",
        "cwd": ".",
        "timeoutSec": 10
      }
    ]
  }
}
```

- Provide both `bash` and `powershell` so the hook works on Unix and Windows.
- Copilot ignores the output of `userPromptSubmitted` and does not let it block the prompt. The hook is an audit aid; the instruction rule is the enforcement layer. Do not claim otherwise in the setup summary.
- Hooks must be merged into the default branch to be available to the cloud agent.

## Gemini CLI and other hosts

Check the installed version's documentation first. If it exposes a project-scoped pre-prompt event that sends the prompt as JSON on stdin, the existing `log-prompt.mjs` works; add only the host configuration and a `--host` value. Do not add a hook based on a remembered or assumed event name.

A host without a project-scoped event keeps the instruction rule. Do not move its configuration to the user's global scope to compensate.

## Merge and verification

1. Read the existing configuration and show the exact entry to add. Preserve every existing hook and key.
2. Validate the JSON after editing. Do not use a regular expression to rewrite a JSON file.
3. Test the core directly:

```sh
printf '%s' '{"prompt":"agents-log smoke test"}' |
  node scripts/agents-log/log-prompt.mjs --host smoke --root .
```

   Confirm one new entry and then remove that test entry only if the project allows editing the log. The append-only rule normally means leaving it; a synthetic entry at the bottom is harmless. Also confirm that a payload without a recognized prompt field fails rather than recording `[empty prompt]`.
4. Send one real prompt through the host. Confirm exactly one new entry with the expected host, model or `unknown`, and the prompt text.
5. Test redaction with a fake value, for example `senha: hunter2`; the log must contain `[REDACTED]`.
6. Test failure handling only when the user agrees: make `AGENTS.log` read-only, send a prompt, confirm the host blocks or reports, then restore permissions.
7. Record the host and version tested in `docs/agents/prompt-logging.md`.

## Trust and ignore rules

- Hooks execute repository code. Show the script, get explicit approval, and tell collaborators that their host may ask them to trust the workspace or the hook.
- Check `git check-ignore -v <config path>`. If the host directory is ignored, the hook works only on that machine. Ask whether the team needs it committed; if so, add a targeted negation or move the configuration to a committed path. Never silently change a project's ignore policy.
- Keep `AGENTS.log` and `AGENTS.log.*` ignored. Never commit the log.
