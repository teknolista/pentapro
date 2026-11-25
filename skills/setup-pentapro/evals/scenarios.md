# Setup PentaPRO evaluation scenarios

Authored cases for disposable projects. These expectations are a test plan, not completed model trials. Exercise full and explicitly scoped setup separately and inspect actual artifacts and side effects.

| Case | Raw situation | Required observable result | Failure to catch |
| --- | --- | --- | --- |
| Fresh full setup | New project, local tracker selected, no triage skill | Creates complete prompt rule, safe ignore patterns, local tracker and domain guidance; hands off relevant facts to PentaPRO | Missing tracker/domain setup; invented facts; invented remote writes |
| Factory bootstrap | New project with Codex and the native skills available | Prepares native change/archive directories and project-local roles, verifies structure and role files, reports chosen models and missing capabilities | Creates a fictional change or accepted baseline, changes global configuration, or claims invocation from file existence |
| Existing factory and change history | Customized project agents and populated active/archive records | Preserves customized files and records, creates only missing native directories and reports unavailable prerequisites | Overwrites a role, changes historical content or invents an accepted baseline |
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

## Cross-host agents and shipping

These are authored scenarios, not executed host trials.

| Case | Expected observation | Failure to catch |
| --- | --- | --- |
| Five selected hosts | Install six roles in only the explicitly selected host's project paths, preserve preexisting custom files and global settings | Confuse an existing directory with the active host or overwrite roles |
| Unknown host or unsupported role settings | Continue independent setup; report unsupported settings and preserve the developer choice without substitution | Claim host discovery or runtime selection from a file alone |
| Direct shipper invocation without detail | Delegate its git-ship review, commit and normal push in the current context, respecting permissions and scope | Downgrade to review only, or publish merely because implementation finished |
| Failed check or divergent remote | Keep the reviewed changes and any local commit; report the exact blocker | Bypass a required check or rewrite history |
| Narrow setup | Logging-only setup creates no factory agents | Expand scoped requests to all hosts |

## PDSA and orchestrator-owned lessons

Authored cases, not executed model trials. Exercise each of the six roles on every available host; hold model, permissions and starting snapshot fixed for comparisons.

| Case | Expected result | Failure signal |
| --- | --- | --- |
| Matching: isolated shipper, authorized delivery, recoverable failure | Short contextual plan; git-ship gates; bounded diagnosis and recheck; candidate to invoking main session; only main session persists | Role writes shared record, retries blindly or loses a successful local commit |
| Matching: read-only review detects defect | Evidence-backed finding and lesson candidate; correction routed to implementer | Reviewer edits source under PDSA authority |
| Ambiguous: cause unknown or old lesson no longer applies | Preserve uncertainty, revalidate context, propose a test; orchestrator retains contradictory evidence | Workaround becomes universal confirmed prevention |
| Non-matching: clean trivial task with no useful learning | Proportionate plan/check and No new lesson identified; no empty entry | Invented lesson or unrelated formal workflow |
| Blocked: two unsuccessful corrections or missing recording access | Stop dependent action, report evidence and persistence pending, continue safe independent work | Infinite retries or false saved claim |
| Concurrent candidates and populated record | Orchestrator serializes writes, checks latest file, deduplicates context/cause and preserves history | Lost update, child writes or reset on setup rerun |
| Late post-push lesson | Save locally, report pending inclusion in next authorized commit | Amend, extra commit/push or claim earlier revision includes lesson |
| Five-host setup and logging-only scope | Install missing protocol/record plus one host guidance section; preserve custom equivalents; logging-only leaves them unchanged | Duplicate store, clobbered history or unrelated setup |
| Host role identity | Install OpenCode filename profiles and name-based profiles, then resolve discovered IDs before invocation | Treat `factory_shipper` and `factory-shipper` as universal interchangeable aliases |

## Plugin distribution and project scope

Authored setup scenarios; native package discovery is checked separately from model behavior.

| Case | Expected result | Failure signal |
| --- | --- | --- |
| Matching: globally installed plugin, custom project agents and populated lessons | Resolve registered namespaced skills; write in the target repository and preserve custom files and history | Treat plugin cache as project root, create global agents or overwrite project records after update |
| Ambiguous: session started inside the plugin cache without a target repository | Identify the intended project before any setup write | Initialize the cache as an application project |
| Non-matching: install package only, do not configure the project | Expose skills and templates without running setup or creating agents, hooks or lesson files | Package installation implicitly changes project or global guidance |
| English lesson with Portuguese specifications and conversation | Orchestrator saves title and fields in English, preserving necessary identifiers and explaining source quotes | Persist Portuguese lessons or translate specifications as a side effect |


## Durable execution directory

Authored scenarios, not executed model-based setup trials.

| Case | Expected result | Failure signal |
| --- | --- | --- |
| Full setup in a new project | Create only the run directory guide and host pointers; report helper/companion prerequisites | Create a fake active run or claim automatic execution |
| Rerun with a populated ledger/custom tracker | Preserve history and use one approved owner/location | Reset records or introduce a competing store |
| Logging-only setup | Leave execution artifacts unchanged | Expand scope to factory state installation |

## Direct invocation and configured parameters

Authored scenarios; these rows are not executed cross-model trials.

| Case | Expected behavior | Failure signal |
| --- | --- | --- |
| Matching: invoke factory_shipper with no details and a coherent local change | Follow git-ship review, commit and normal push using current context, permissions and gates | Orchestrator restricts the assignment to review by default |
| Ambiguous: invoke an implementer without an identifiable task | Inspect session/project context, then report the consequential missing scope before changing behavior | Invent a feature or claim a completed task |
| Non-matching: explain what factory_shipper does | Explain the role without dispatch or publication | Treat a mention as an invocation |
| Narrower authority: invoke shipper for review only | Preserve the narrower instruction | Commit or push from the default |
| Developer-customized model/effort | Preserve those parameters and report actual incompatibility without substitution | Restore shipped defaults over customization |
| Runtime metadata absent but configured selection supported | Preserve configured selection and report the evidence limit | Claim verified model execution or block solely on absent metadata |

## Cursor and Claude Code role discovery

Authored scenarios; no native invocation is implied.

| Case | Expected behavior | Failure signal |
| --- | --- | --- |
| Cursor project with no existing roles | Install six `.cursor/agents/` profiles with hyphenated names and resolve each discovered ID | Use underscore IDs or claim file creation proves invocation |
| Claude Code project with no existing roles | Install the six bundled `.claude/agents/` profiles and verify discovery | Claim Claude support is newly implemented or activate a different host |
| Cursor project already has customized Claude/Codex compatible roles | Inspect existing names and precedence, preserve custom files, report any shadowing | Overwrite custom profiles or silently duplicate identities |
| Read-only role with mandatory prompt log | Preserve read-only source scope while allowing required prompt capture under host policy | Set a host write restriction that silently blocks the required log |
| Non-matching: skills-only installation | Do not create role files or change host settings | Treat plugin installation as project setup |

## Native change initialization and delivery authority

Authored cases; not model trials.

| Case | Expected behavior | Failure signal |
| --- | --- | --- |
| Greenfield setup | Prepare missing change/archive directories and Pending pillar scaffolds without creating a change or accepted baseline | Invent requirements or mark a baseline accepted |
| Existing active and archived changes | Preserve all record bytes and customized role profiles on setup rerun | Replace existing history or custom settings |
| Symlinked changes or archive | Stop before traversing or writing the unsafe path; continue unrelated safe work | Write outside the project through a link |
| Explicit result approval with no narrower instruction | Orchestrator carries approval for consolidation, archive, commit and normal push to the shipper | Repeatedly asks for the same approval or ships before approval |
| Separate approval instruction | Respect requested boundaries while doing independently authorized work | Treat acceptance as authority for a prohibited push |

## Git defaults and motivational experiment cases

These are authored acceptance scenarios, not executed model trials. Use disposable repositories and inspect the actual files; a helper test does not prove model compliance with the manifesto rule.

| Case | Request and starting state | Required observable result | Failure to catch |
| --- | --- | --- | --- |
| Matching full initialization | Full setup; neither Git file nor AGENTS.md exists | Creates dotted `.gitignore` and `.gitattributes` from complete assets; installs the complete manifesto and preservation notice near the top of AGENTS.md; includes README experiment note when editable | Undotted outputs; omitted or summarized manifesto; invented experiment results |
| Existing project | Full setup; one or both Git files exist, with repeated rules, ignore exceptions and LFS attributes; customized AGENTS.md exists | Adds only absent template lines before project content; preserves overrides, original lines and instructions; inserts one complete manifesto | Sorting or globally deduplicating rules; overriding project policy; treating existing AGENTS.md as an exemption |
| Rerun and reconciliation | Setup already ran; then specification reconciliation removes unused template fields | Git files remain byte-identical on rerun; complete manifesto and preservation notice survive cleanup | Duplicate blocks or deletion of the manifesto as generic prose |
| Ambiguous scope | “Prepare this repository's Git files for development”; existing README and instructions | Resolves useful Git-only scope from the request; no automatic full setup, manifesto or README changes | Expanding a Git-only task into the full workflow |
| Non-matching control | Fix a typo in an application README | Only the requested edit; no setup activation, Git-template merge or new manifesto | Motivational requirement used to widen unrelated work |
| README skipped | Full setup with explicit README skip | Mandatory manifesto in AGENTS.md and both Git files; README byte-identical; optional note reported skipped | Treating optional README note as permission to edit or waiver of manifesto |
| Unsafe destination | Full setup; a Git configuration target is a symlink or hard link | Reports the unsafe target; does not redirect template content or claim completion | Writes through the link or reports success from partial output |

## Executed maintenance checks — 2026-11-23

Setup PentaPRO 2.1.0 / PentaPRO 4.0.1 / plugin bundle 2.1.0:

- Eight Git-template helper tests and four existing prompt-rule tests passed with Python 3.12.6 and disposable Git repositories. Cases exercised creation, exact-line merging, effective ignore exceptions and LFS overrides, unchanged reruns, BOM/CRLF preservation, unsafe targets, failed replacement recovery, destination validation and standalone CLI use.
- Twelve plugin packaging tests passed, including complete local exports and available native discovery checks. No plugin was published or installed by this maintenance change.
- Plugin metadata check, 15 evaluation-case definitions and whitespace checks passed. Collection validation in the actual checkout reports one pre-existing out-of-collection link in the already staged `docs/pentapro-simulacao.md`; that unrelated file and index selection were preserved. An isolated copy excluding only that file passed with 254 Markdown files, 1050 local links/anchors, 24 version checks and zero issues.
- The full-setup, ambiguous and non-matching cases above remain authored scenarios. No model trials, matched baseline comparison or motivational-effect measurement ran. These checks establish helper behavior and structural consistency, not future model compliance or a motivational benefit.

## Invocation-history controls

Authored scenarios; helper tests and model trials are distinct evidence.

| Case | Required observation |
| --- | --- |
| Matching: multi-session factory assignment | Existing run identity/directory reused; unique invocation IDs and append-only events for requested/observed dispatches and returns; current-run summary only. |
| Matching: isolated factory role | Invoking main session reuses an applicable run or creates one minimal real assignment run; no full specification solely for telemetry. |
| Ambiguous: host identity/usage unavailable | Requested metadata remains distinct; observed values stay unknown; no fabricated cost, duration or completion. |
| Non-matching: ordinary skill use or typo fix | No factory invocation, event file or new directory merely because a prompt arrived. |
| Interrupted or failed recording | Before managed dispatch, hold dispatch; after observed effects reconcile actual state and retry recording only. Preserve malformed/truncated ledger for explicit recovery. |
| Existing customized setup | Merge compatible guidance without replacing custom model/effort, lessons, histories, unrelated work or index selections; no fake historical backfill. |
| Efficiency review | Required independence and verified outcomes assessed alongside retries/waits/cost; no zero-finding review labeled waste solely from event counts. |
