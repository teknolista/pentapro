# Software factory v1 — comparison and scope

The supplied Castas-based proposal and the ChuteGPT discussion both favor canonical SDD/OpenSpec records, vertical slices, independent review, targeted checks, evidence-bound handoffs, explicit authority and a retrospective. The ChuteGPT history additionally motivates preserving authority through a run, completing authorized work without an unnecessary stop, and testing terminal rendering and cross-language input contracts.

This v1 keeps the proposal's gates as states, while making role count and depth proportional to the change. It uses existing skills rather than replacing their domain workflows. Unlike a hard-coded pipeline, it treats the requested order and project policy as authoritative. It explicitly handles the often-missed case where archiving after publication changes tracked files and requires another authorized publication. A retrospective recorded after the final published revision likewise needs a separate publication if it must be in Git.

This is a portable instruction package and role-packet mechanism, not a deterministic workflow engine or proof of host isolation. The pilot used Setup PentaPRO 1.6 with project-scoped Codex role templates and OpenSpec setup. Follow the [maintained setup procedure](../setup-pentapro/references/factory-setup.md) and the [operational guide](guia-fabrica-changes.md) for current use. A real change and a behavioral evaluation are needed to establish whether it improves quality or efficiency. Project instructions and host policy always take precedence.

[Codex subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Agent Skills specification](https://agentskills.io/specification)
