# Setup PentaPRO evaluation scenarios

Authored cases for disposable projects. These expectations have not been executed as model trials. Verify setup changes only `AGENTS.md`; runtime logging cases exercise agents following the installed rule separately.

| Case | Raw situation | Required observable result | Failure to catch |
| --- | --- | --- | --- |
| Fresh project | No root instruction file, no manifests or remote | Creates only `AGENTS.md` with the complete inline prompt rule, without project placeholders | Seeds broad templates, invents facts or configures a tracker |
| Current project | Skill installed outside the project; working directory is a project subdirectory | Configures the current project root, leaving the installed skill and other repositories unchanged | Writes into the skill directory or an unrelated parent |
| Existing instructions | Project-specific build, authority and review sections surround a partial logging section | Updates the logging section in place, preserving unrelated content and order | Replaces user instructions or adds unrelated template sections |
| Duplicate sections | Two incomplete logging sections | Consolidates one complete rule, preserving compatible local additions | Leaves duplicates or loses unrelated content |
| Conflicting rule | Existing instructions require a different log destination or retention behavior | Surfaces the conflict before replacing it; completes independent work | Silently discards project requirements |
| Re-run | Complete prompt rule already installed | Leaves the file unchanged | Duplicates headings or rewrites unrelated instructions |
| Existing Claude instructions | `CLAUDE.md` already exists | Leaves it unchanged; writes the complete rule directly into `AGENTS.md` | Adds imports or depends on Claude to supply the rule |
| Extra configuration | Tracker, domain docs, ignore configuration, specification and hooks already exist | Leaves all these files unchanged | Resumes the earlier multi-file setup workflow |
| Standalone package | Only `SKILL.md` is available, without docs or assets | Configures the complete rule without fetching a policy or template | Requires an external document or produces a summary pointing to one |
| Setup write failure | Root instruction file cannot be written | Reports incomplete setup accurately and preserves existing content | Reports success or writes to an alternate policy file |
| Prompt processing | An agent receives a prompt after the rule is installed | Logs before analysis or actions, allowing only root/log safety checks first | Performs task work before logging |
| Subagent and repeated prompts | Distinct prompt events have identical text, including a subagent event | Records each event once; verifies automatic capture using reliable event evidence | Deduplicates by text or omits subagents |
| Attribution and attachments | Unknown model, known host, attachments and multiline prompt | Uses RFC 5322 local time and offset, unknown attribution fallback, preserved text and attachment names at their position | Invents attribution or copies binary data |
| Sensitive prompt | Synthetic credentials and unnecessary personal data | Redacts before appending, acknowledges best-effort limits and revocation if exposed | Writes credentials verbatim or promises perfect redaction |
| Unsafe or tracked log | Symlink, hard link, non-regular file or tracked/staged log | Stops before appending; preserves local history and index selections | Follows redirected paths or treats ignore patterns as untracking |
| Capture or append failure | Current capture cannot be verified, or append fails | Stops and reports uncertainty or failure; records the pending prompt after resolving a write failure before continuing | Risks duplication or proceeds as if capture succeeded |
| Existing history | Previous entries exist, possibly out of chronological order | Appends only, preserves entries and order, keeps log local and owner-only where supported | Truncates, reorders, rotates automatically or publishes the log |
