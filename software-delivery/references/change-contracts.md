# Choose the change contract and checks

Read when the requested change needs explicit specification, its risk or scope changes, an experiment may become maintained software, or the project generates code from a governing source. Apply the project's actual policies and the user's authorized scope. Choose independently how much the agent may do, where intent is recorded, and which checks must pass.

| Work | Minimum useful contract |
| --- | --- |
| Localized edit with clear intent, known callers, low consequence and easy recovery | Use the request and existing contract. Make the scoped edit and run the relevant check. Keep the brief in the existing request or ticket when sufficient. |
| Exploration of a design or technical uncertainty | Name the question, limits, stopping condition and observable result. Run an authorized isolated experiment with synthetic data when useful. Capture the finding and limitations for the next decision. |
| Planned feature, material behavior or boundary change, or work subject to an explicit specification policy | Establish the affected scope, behavior and checks in the authoritative change record before changing that behavior. Reuse a sufficient existing contract. Add a focused specification for the change, or a broader one when the requested scope requires it. |

Judge consequence from actual effects and consumers. A one-line change can weaken access control, alter a public contract, corrupt stored data, or make recovery harder. Sensitive data, irreversible effects, coupled teams or components, unresolved business rules and costly verification are reasons to inspect the contract and strengthen checks. Established review, security and release gates still apply to a short prompt or a small diff.

## Establish readiness before implementation

1. Identify the governing baseline and accepted changes. Derive the draft from the request, project records, examples, known constraints and observed behavior. Cite the origin of material rules and distinguish confirmed intent, delegated decisions, proposals and unknowns. Use existing tickets, specifications, schemas, decision records and checks according to what each actually governs.
2. For the scoped change, establish the outcome and exclusions, consumer contracts, representative success and failure examples, affected constraints, and how to verify them. Include migration, recovery, security, ownership and rollout where they change the design or gates. Use the level of detail that lets an implementer proceed without guessing a consequential decision. Follow project rules for the required format and approval.
3. Ask the accountable person only for unresolved consequential choices outside delegation. Record the answer, scope and dependent work. A combined specification and implementation request can proceed on settled scope under existing authority after applicable readiness gates are met. If the user or project requires the entire selected scope specified before coding, complete that scope and its required review first. Otherwise prepare and verify one coherent increment at a time.
4. Plan checks from the agreed behavior before implementing it. Preserve independent expectations when the same agent edits code and tests. Use controlled counterexamples, representative state and the real affected boundary where appropriate. A schema, test or policy can own a precise part of the contract. Link intent, rationale and constraints those checks cannot express.

Before implementation, challenge a consequential design choice when a wrong answer could change data ownership, security, compatibility, recovery, or the ability to verify the outcome. Trace one realistic request from entry to observed result, then through a failure, retry, or concurrent execution that matters to the contract. Compare the proposed mechanism with the simplest credible alternative, and identify the check that would distinguish them. Record the decision and unresolved premise in the existing change record; use an independent design reviewer when project policy or the user requires one. This review does not itself authorize implementation.

## Change course and reconcile

If implementation reveals that the contract is incomplete, contradictory or infeasible, identify the affected records, consumers and checks. Keep the supported baseline, agreed change and observed implementation distinct. Correct implementation drift against the contract. For a justified change to the contract, obtain or use actual decision authority, update the owning record and recheck affected work. Preserve old results with the revisions they exercised. Resume from the reconciled contract and the next pending check.

When moving an experiment into maintained use, decide what to discard, reuse or rebuild. Review any reused source and dependencies, replace temporary data and shortcuts, establish the maintained behavior and operating constraints, and run the applicable integration and acceptance checks. Carry prototype observations only for the conditions they exercised.

When a project governs generated code through a schema, DSL or another source artifact, edit the governing source and regenerate through the established toolchain. Check the resulting diff, consumer compatibility and actual behavior. Treat unexpected generated drift as a discrepancy to resolve with the owner. Follow the project's exception policy for any direct patch. A Markdown brief or a passing test alone does not establish such a generation workflow.

## Port an existing behavior

Pin the source revision and the behavior being carried forward. Compare authoritative requirements, examples, screenshots and observed source behavior where they disagree. Record the difference, the owner-confirmed behavior to preserve or change, and a check that distinguishes the alternatives. Keep those links in the existing change and evidence records.

Run shared fixtures or domain vectors through the source and target entry points. Cover relevant edge cases, prior stored data, ordering and locale. Exercise platform-specific installation, restart, access and upgrade separately when they are in scope. For example, a questionnaire port can compare score totals and translations using synthetic inputs, then verify that the target app restores the expected result after reopening. A screenshot confirms only the rendered state it captured.

## Worked example with project-native SDD

For `tenant-receipts`, read the baseline and all six files in `pentapro/changes/tenant-receipts/`. The PRODUCT record identifies the requirement and scenario IDs; PROJECT records the design, alternatives and constraints; PRODUCTION records operating impact; PROOF owns acceptance criteria and actual evidence; PROCESS owns numbered tasks and authority. Preserve the current baseline while implementing. Check that distinct tenants using the same ID have independent receipts, an exact replay creates no extra job and a conflicting replay returns the agreed error without mutating state. Exercise the actual handler with representative state and security controls; link scenario, command, result, tested revision and limitations in PROOF. Do not mark a task complete on a skipped check or test plan.

After explicit developer result approval, the specification owner reconciles affected baseline pillars and the factory archives the change. Check preservation of unaffected scenarios and link targets from the archived location. Approval normally also covers commit and normal push; honor narrower instructions or separately requested approvals. A specification-only request does not itself authorize implementation.

## Worked example of adopting a prototype

An isolated upload prototype demonstrated that users can retry a failed submission. Record what it demonstrated with synthetic data. When asked to make it part of the maintained application, inspect the real entry point, account permissions, file limits, dependency changes and the prototype's stubbed storage. Reuse the interaction where it fits the application. Replace the stub through the owning adapter and establish the accepted behavior for failed and repeated submissions in the existing ticket or change record. Exercise successful upload, denied access and retry on the maintained implementation. Record the observed result there.

## Verify removals and renames

For a removal, recover the full baseline requirement and scenarios, reason, affected consumers and migration conditions; verify through the relevant real entry points that retired behavior is no longer delivered when required. Missing or title-only baseline evidence leaves the check unverified. For a rename, verify retained behavior under the new requirement ID; code symbols need not change. When the change also modifies behavior, verify the accepted behavior and preserve unaffected scenarios. Distinguish unavailable checks from not-applicable checks; documentation consistency is not executed behavior.
