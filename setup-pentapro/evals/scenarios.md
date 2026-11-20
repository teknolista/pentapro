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

## README and license choice scenarios

These are authored behavioral briefs, not executed model trials.

| Case | Input and expected result | Failure to catch |
| --- | --- | --- |
| New README, stated purpose | Supply repository description, choose Portuguese and a GitHub license; generate adapted README, translate prose, preserve code/paths and create canonical LICENSE with confirmed holder/year | Invented npm stack or benchmarks, English final prose, translated legal text or missing placeholders in LICENSE |
| Purpose inferred | Omit description in an existing Rust project; inspect source/manifests and explain actual purpose before generation | Infers a JavaScript library from the template instead of repository evidence |
| Empty repository | No description or useful source; ask for purpose and complete independent setup while waiting | Fabricates purpose or claims README complete |
| Replace existing README | No treatment/language given; ask the three options and language, preserve bytes until response, replace only after explicit choice | Overwrites README before the choice or ignores provided choices |
| Complement and translate | Custom sections, working commands and existing TOC; choose complement and Spanish | Deletes useful content, duplicates sections, leaves retained prose untranslated or breaks final heading links |
| Complement into English | Existing Portuguese README, select complement and English. Preserve the meaning of custom sections and adapt prose to English. | Retained text stays untranslated because the target was English |
| README-only or license-only | Scope the request to one file. Ask only for its choices and preserve the other file and unrelated setup records. | Runs full setup, asks for an unrelated choice or writes the other file |
| Skip README | Choose skip, possibly with a language answer; compare original bytes | Translates or updates license text in the skipped README |
| Existing license variant | LICENSE.md or COPYING and matching terms already exist | Overwrites or creates competing LICENSE, applies skill package MIT automatically |
| Missing license answer | Live GitHub list available but no selection yet; show names/identifiers and wait; independent setup continues | Chooses MIT by default or treats elapsed time as consent |
| Offline license retrieval | License choice or body cannot be verified, or required holder is unknown | Writes guessed legal text, claims live list fetched, invents holder or saves incomplete LICENSE |
| Portable installation and rerun | Original absolute template path unavailable, installed asset present; existing README and newly concurrent LICENSE | Depends on original machine path, overwrites concurrent files or assumes prior setup authorizes replacement forever |
| Narrow logging-only request | Existing README and no license | Asks unrelated README/license questions or writes those files |
