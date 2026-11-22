# Fixed change records

Active location: `pentapro/changes/<name>/`. Use a unique identity with two or three lowercase words separated by hyphens, such as `initial-catalog` or `receipt-retry-policy`. Search active and archive directories before selecting a name; use another meaningful name on collision. Do not append a numeric fourth token or reuse an archived identity. An archive directory is not an active change.

Every change has exactly six required human-readable records; supporting assets may be linked when needed. No parser-specific headings or configurable workflow schema is required. Use the penta-pro packaged authoring templates when available, otherwise follow this contract. All five dimensions remain explicit, even if unchanged with a baseline link and reason.

| File | Sole owner and content |
| --- | --- |
| change.md | Identity, problem/value, scope/non-goals, type (initial/feature/behavior-neutral), baseline revision/records, affected IDs, lifecycle, disposition, approval scope, index and next action. Index tasks/evidence without duplicating them. |
| product.md | Requirement/scenario IDs and observable acceptance; add/modify/remove/rename intent with before/after behavior; failures, permissions and compatibility when relevant. |
| project.md | Design, constraints, contracts, decisions/rationale/alternatives, data/security implications and risks. |
| production.md | Installation, runtime, rollout, compatibility, migration, support, recovery and operational effects. |
| proof.md | Criterion-to-check mapping, planned versus executed checks, actual outputs/evidence locators, tested revision, gaps and developer validation. |
| process.md | Actual authority, task checklist, owners, dependencies, write scope, reviews, resumption and reconciliation/publication follow-up. |

A baseline file states consolidated software facts; an active change states intended behavior under development. User approval of a proposal or specification is distinct from approval of the implemented result. Record the scope of each approval, not a generic approved flag.

Lifecycle vocabulary: Draft → Spec reviewed → Implementing → Verifying → Awaiting acceptance → Accepted → Consolidating → Archived. These are agent-maintained descriptions, not automatic proof. A blocked stage records its cause, actual completed work and next action without pretending to have passed. Rework may revisit earlier stages with affected evidence marked stale. Archive disposition is `completed` or `cancelled`, recorded independently of lifecycle/location; a cancelled archive must never appear accepted or implemented merely because it is archived.

For initial changes no accepted baseline exists: record that explicitly, capture repository revision/observed source and keep root scaffolds Pending until accepted consolidation. Existing-project changes reuse baseline IDs and include behavior to preserve. Pure tooling/refactor/documentation changes say which dimensions are unchanged rather than inventing product requirements.

Fresh changes need full required records but only relevant depth. Save incrementally so interruption preserves useful specification. Do not invent research, sign-off, execution evidence or unavailable model metadata. Keep artifacts in English, preserving required localized product copy and identifiers. Keep credentials and personal data out of all records.
