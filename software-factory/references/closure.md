# Consolidation, archive and recovery

## Accepted result

Read the exact developer result approval and narrower restrictions in change.md/process.md. By default one explicit acceptance covers baseline consolidation, archival, commit and normal push for the reviewed change. Present that scope before requesting acceptance. If separate approvals, local-only or planning-only work were specified, follow those limits. Process-policy approval is not acceptance of an unfinished implementation.

Before closure, confirm current source, contract and review/check evidence still match. No unresolved required gate may be converted into a pass by approval or archiving. User risk acceptance may be recorded honestly without asserting that an untested premise was verified. New substantive feedback returns to specification/implementation and invalidates affected prior results.

Use penta-pro for five-pillar reconciliation. Compare the identified baseline, accepted change and actual implemented/verified behavior. Apply additions, modifications, removals and identity mappings deliberately; preserve every unaffected requirement and scenario. Reconcile dependent design, operating instructions, evidence and process links. For changed fields without current evidence keep explicit limits. A full change file must never blindly replace a baseline topic. Greenfield consolidation populates the root pillars; brownfield consolidation updates only affected records.

Record files updated and reconciliation pending before the first write. Inspect each saved result and compare intended versus actual diff. Only after all affected dimensions and links are reconciled, and required rechecks pass, mark ready to move. Never call a partial reconciliation Consistent. Do not rerun unrelated expensive checks solely for a harmless record edit; re-evaluate what the edit can affect.

## Move and links

Use `pentapro/changes/archive/YYYY-MM-DD_<name>/` with the developer's local date at actual archival, not creation date or UTC guessed from the execution host. Inspect actual resolved source/destination paths and existing contents before moving; refuse path escape, unsafe symlinks and collisions. Preserve concurrent edits and never overwrite or merge an existing archive directory. A collision needs an explicit recovery/identity decision; do not invent suffixes silently.

Record disposition, acceptance/cancellation basis, archive date and pending publication separately. Repair relative links for the extra directory level and incoming links from baseline/process/evidence, preserving stable IDs. Check target files and anchors from their new locations. Confirm source absent, destination complete and baseline consistency before reporting archive success. Renaming/moving is performed with available ordinary file tools under host permissions; no dedicated CLI is required.

## Cancellation

Ask for/observe explicit cancellation authority. Record why, what was implemented, retained effects, current source revision, failed or unavailable checks, recovery decision and outstanding work. Do not promote abandoned requirements into the baseline, mark unfinished tasks done, or automatically revert source or other user work. If partial behavior is retained, reconcile its actual approved baseline effects separately; if effects are unresolved, preserve the active change as cancellation pending reconciliation instead of hiding it in archive. Archive a resolved cancelled change with disposition cancelled and implementation/publication limits visible. Publishing cancellation records follows actual user authority; cancellation alone does not authorize destructive recovery.

## Interrupted or overlapping work

On resume read actual baseline/change/archive contents, current Git state and prior operation observations before any replay. If a move succeeded but its record update failed, reconcile the existing destination rather than moving again. If consolidation partly succeeded, preserve already-correct changes, compare remaining work and continue only within authority. Never assume lack of a local receipt means an external operation failed.

Before integrating changes affecting overlapping IDs/files, inspect the other active contracts and baseline revisions. Serialize writes; resolve incompatible accepted intent with the developer. A changed baseline requires re-evaluating affected scenarios, design and evidence before applying an older change. Do not silently consolidate an older snapshot over newer requirements.

After observing delivery, reconcile current operational next actions with the actual receipts. Keep historical archive instructions explicitly labeled as checkpoint history and add a dated completion reference instead of erasing their chronology. Resume guidance must not ask an agent to repeat an already confirmed commit/push. Check lifecycle wording separately from link validity; valid links do not establish that a status is current. Post-publication receipt/lesson updates may stay local for the next authorized commit; do not create another publication merely to update historical wording.

A published commit, archive, deployment and release are different observations. If publication fails preserve the reviewed local commit and archive; mark remote state unverified until actually queried. No automatic new commit, amend, force push, branch deletion, global configuration change or bypass of checks is permitted to conceal a failure.
