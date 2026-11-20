# Tool contracts and task evaluation

Use when adding or changing structured results, discovery descriptions, or a workflow spanning tools. Preserve the actual SDK, protocol revision and supported clients.

## Validate the published result contract

For a declared `outputSchema`, validate actual structured results against it, including empty collections, optional fields, nullability, pagination and truncation where supported. Exercise operation failures and protocol errors against their respective revision-specific contracts rather than fabricating success payloads. When both text and structured representations describe the same result, check that they agree. Never put secrets or internal traces into either representation. [MCP structured results](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#structured-content)

## Exercise the caller's task

Choose representative tasks from the intended caller workflow and prepare isolated data with independently known outcomes. Give the client or agent the task and exposed interface, without coaching it with the expected tool name or hidden solution. Observe whether it discovers the right capability, distinguishes similar tools, supplies valid arguments, interprets results, follows pagination and composes dependent calls when needed. Include a realistic denied or invalid request and recovery from an actionable error. Exercise writes only in authorized disposable fixtures and inspect downstream effects.

Record task success, wrong selections, unnecessary calls, missing information and available time/token metrics with client/model, server snapshot and configuration. Diagnose whether a failure comes from tool wording, schema, missing capability, client support or service behavior before changing the interface. A direct scripted invocation proves the exercised integration, not model discoverability. If no agent trial is available, finish protocol checks and mark task usability unverified. Compare matched old/new interfaces for material changes before claiming improvement; no fixed task quota, model or evaluation framework is required.

Method adapted in original wording from [Anthropic MCP Builder](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/mcp-builder/SKILL.md).
