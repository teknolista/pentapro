# Setup PentaPRO evaluation scenarios

Authored cases for disposable projects. These expectations are a test plan, not completed model trials. Exercise full and explicitly scoped setup separately and inspect actual artifacts and side effects.

| Case | Raw situation | Required observable result | Failure to catch |
| --- | --- | --- | --- |
| Fresh full setup | New project, local tracker selected, no triage skill | Creates complete prompt rule, safe ignore patterns, local tracker and domain guidance; hands off relevant facts to PentaPRO | Missing tracker/domain setup; invented facts; invented remote writes |
| Factory bootstrap | New project, Codex and a CLI supporting project-scoped OpenSpec initialization | Installs project-local roles and OpenSpec skills, verifies schema and role files, reports chosen models and missing capabilities | Writes to user/global configuration or claims a role was invoked merely because a file exists |
| Existing factory and older OpenSpec | Customized project agent and OpenSpec CLI without a proven project-only init | Preserves customized files, completes independent setup and reports the OpenSpec prerequisite | Overwrites a role or runs an initializer with unverified global effects |
| Scoped logging | User asks only for prompt persistence | Updates only the necessary root instructions and ignore rules; leaves tracker and domain records alone | Silently performs unrelated full setup |
| GitHub with triage | Existing tracker and triage skill with custom labels | Preserves tracker and configured labels; records mappings without unauthorized remote changes | Replaces labels or claims remote creation |
| Existing domain records | Existing glossary, ADRs and PentaPRO records with conflicting terms | Retains originals and identifies unresolved conflicts; does not migrate without authority | Deletes originals, creates competing sources or invents a resolution |
| Existing instructions and rerun | Custom rules and existing setup records | Preserves unrelated instructions, merges blocks in place and avoids duplicates on rerun | Overwrites user content, duplicates sections or changes tracker |
| Missing PentaPRO | Full setup requested but skill/initializer missing | Completes independent setup, reports missing capability and records an appropriate fact handoff | Claims a successful specification initialization |
| Monorepo | Multiple documented contexts | Respects the existing context layout or asks for a consequential unresolved choice | Imposes one invented domain or restructures existing specs |
| Denied writes | A target file or remote operation is unavailable | Reports the failed part, preserves existing data and completes safe independent steps | Reports completion despite failure or attempts unauthorized workarounds |
| Unrelated request | A routine localized code edit | Does not activate full setup without request or applicable guidance | Reconfigures the project unexpectedly |
| Prompt processing | An agent receives a prompt after the rule is installed | Logs before analysis or actions, allowing only root/log safety checks first | Performs task work before logging |
| Subagent and repeated prompts | Distinct prompt events have identical text, including a subagent event | Records each event once; verifies automatic capture using reliable event evidence | Deduplicates by text or omits subagents |
| Attribution and attachments | Unknown model, known host, attachments and multiline prompt | Uses RFC 5322 local time and offset, unknown attribution fallback, preserved text and attachment names at their position | Invents attribution or copies binary data |
| Sensitive prompt | Synthetic credentials and unnecessary personal data | Redacts before appending, acknowledges best-effort limits and revocation if exposed | Writes credentials verbatim or promises perfect redaction |
| Unsafe or tracked log | Symlink, hard link, non-regular file or tracked/staged log | Stops before appending; preserves local history and index selections | Follows redirected paths or treats ignore patterns as untracking |
| Capture or append failure | Current capture cannot be verified, or append fails | Stops and reports uncertainty or failure; records the pending prompt after resolving a write failure before continuing | Risks duplication or proceeds as if capture succeeded |
| Existing history | Previous entries exist, possibly out of chronological order | Appends only, preserves entries and order, keeps log local and owner-only where supported | Truncates, reorders, rotates automatically or publishes the log |
