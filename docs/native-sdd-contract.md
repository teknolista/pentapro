# Native SDD transition contract

Status: Implementation authorized. Owner decisions received on 2026-11-22: preserve historical evidence, remove operational references except required provenance, and use one result approval for consolidation, archive, commit and normal push by default. Explicit narrower or separate approval instructions prevail. This migration must first present its reviewed result for that approval; the rule decision is not acceptance of the resulting implementation.

## Confirmed outcomes

- Retain PRODUCT, PROJECT, PRODUCTION, PROOF and PROCESS as the five specification dimensions.
- Active changes live at `pentapro/changes/<name>/`; names contain two or three lowercase words separated by hyphens and identify one change uniquely.
- Completed or explicitly cancelled changes move to `pentapro/changes/archive/YYYY-MM-DD_<name>/` using the owner's local archive date. Never overwrite a collision.
- Initial project specification is authored in a change; existing-project changes describe affected behavior and preservation against an identified baseline.
- The developer invokes a principal exploration/orchestration agent, which guides clarification and dispatches scoped specification review, planning, implementation, verification and review automatically within granted authority.
- Read-only reviewers do not author or modify product source. Preserve configured model/effort and host permissions.
- The maintained baseline is reconciled across all affected pillars before completed changes are archived. Cancellation preserves the baseline and records any partial implementation, recovery decision and residual work; never consolidate abandoned requirements as delivered behavior.
- Remove the previous external SDD dependency from active workflows, setup, agents, configurations and current documentation. No replacement SDD CLI or configurable schema engine is introduced.
- Existing product tests and collection maintenance checks remain applicable. Model judgment and document completion are not proof of runtime behavior.

## Implementation design

Reuse existing skills for specification, implementation, review and coordination. Prefer one owner of change lifecycle; settle whether a new skill is necessary after tracing existing owners. A change needs a concise index/status/authority/baseline, scoped records across all five dimensions, tasks, revision-bound evidence and final disposition; avoid duplicating canonical facts. The settled section defines the six files and reuses the host main session as orchestrator.

The supplied scenarios require implementation feedback loops and developer validation. The owner has updated the final transition: one approval of the result authorizes baseline reconciliation, archive, commit and normal push unless separate steps were requested. Preserve bounded non-progress handling rather than infinite retries. A paused human acceptance gate is an intentional handoff; independent authorized work may continue.

## Acceptance and migration checks

- Fresh setup and rerun preserve existing records and logs; the new change/archive structure exists and is documented.
- Greenfield, brownfield, cancellation, interruption/resume, overlapping change, archive collision and negative-feedback scenarios have explicit outcomes and ownership.
- Review of a fixed integrated snapshot precedes acceptance; changes invalidate affected evidence.
- Archive rewrites links from the new location and checks preservation of unaffected requirements and scenarios.
- Six host adapters remain syntactically valid, distributed, discoverable by documented identifiers and consistent with canonical role behavior. Actual native discovery/inference remains an execution gap when unavailable.
- Catalog/version/installation/routing/templates/documentation/evaluations and tests are reconciled; portable packages retain licenses and required provenance.
- Inventory executable helpers and map their direct/indirect tests; run affected regressions and required collection checks and report unavailable evidence honestly.
- Keep existing customized work, index selections, dated historical evidence and required legal notices. Remove obsolete operational references; retain a concise origin/attribution statement. A pre-existing `w` prefix in `skills/setup-pentapro/references/factory-setup.md` belongs to the initial dirty snapshot and must not be silently reverted.

## Settled implementation decisions

Use six fixed change files: change.md, product.md, project.md, production.md, proof.md and process.md. Keep all five dimensions present; unaffected dimensions link the baseline. Reuse existing skill owners rather than creating overlapping skills. The host main session is the principal exploration/orchestration agent; existing specialist profiles keep their selected models and effort.

Changes pass through Draft, Spec reviewed, Implementing, Verifying, Awaiting acceptance, Accepted, Consolidating and Archived, or Cancelled. One explicit result approval covers closure/publication by default; no timeout, model verdict or tool success counts as human approval. Cancelled work never promotes abandoned intent; reconcile actual retained effects or document recovery before archive. Native workflows do not require or install an external SDD tool, schemas or stores.

## Artifact comparison and proposed adaptation

Reviewed upstream `schemas/spec-driven/templates/{proposal,spec,design,tasks}.md` through the public repository on 2026-11-22. Source locators: https://github.com/Fission-AI/OpenSpec/tree/main/schemas/spec-driven/templates and the associated schema instructions. These are permitted research provenance; no source template text or CLI dependency is copied into the proposed contract.

| Source practice | Proposed native owner and adaptation |
| --- | --- |
| Motivation, changed capabilities, affected systems | `change.md`: problem, expected value, scope/non-goals, identified baseline and affected record IDs; distinguish behavior change from implementation-only maintenance. |
| Requirements with trigger/outcome scenarios | `product.md`: stable requirement and scenario IDs, observable behavior and before/after effects; include permitted, denied, failure and compatibility cases as applicable. |
| Add/modify/remove/rename operations | Explicit change intent per affected ID; retain full unaffected scenarios, retirement reason/recovery and identity mapping. Do not require source identifiers to be renamed when a behavior ID changes. |
| Context, goals, decisions, alternatives and risks | `project.md`: owned design choices and their rationale, with links to product requirements rather than repeated requirements. |
| Numbered task checkboxes | `process.md`: owner, dependencies and observable completion check per task; tests and documentation accompany their owning increment. Keep pending and executed results separate. |
| Operational impacts and acceptance evidence | Separate `production.md` and `proof.md`, extending the four-document pattern to the existing five-dimensional specification. |

Proposed fixed layout: `change.md`, `product.md`, `project.md`, `production.md`, `proof.md`, `process.md`. Each dimension is present; an unaffected dimension links its identified baseline and records that it is unchanged. `change.md` indexes tasks/evidence but does not duplicate their content. This layout is the implementation choice within the owner’s delegated scope.

Current review recommends no new skill: `penta-pro` owns specification content/reconciliation, `software-factory` owns lifecycle/coordination, and `software-delivery` owns task planning/implementation. The host's main session can be the principal orchestration agent, keeping existing specialist model/effort choices. Any additional host role needs an explicit model/effort choice, not an invented default.

Specification review: the settled bootstrap slice is ready. Full lifecycle implementation can proceed after the revised contract review. Cancellation never promotes abandoned requirements into the baseline or implies permission to revert source. Preserve existing root files as Pending scaffolds until an accepted change is consolidated.
