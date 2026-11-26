# PROJECT — native factory architecture

Status: accepted scoped baseline, 2026-11-22.

The host main session is the principal exploration/orchestration agent. Six configured specialists handle specification review, implementation, verification, code review, retrospective and Git shipping. Six host adapter families preserve their declared model/effort and role identity conventions; actual native discovery must be verified in the adopting client.

PentaPRO owns specification content and five-pillar reconciliation; Software Factory owns change lifecycle and handoffs; Software Delivery owns tasks and implementation. UI Design authors proposed screens inside the active change, with root PRODUCT updates only during approved consolidation. Other specialist skills retain their existing domains and authority boundaries.

The fixed change records are change.md, product.md, project.md, production.md, proof.md and process.md. Baseline facts, proposed change intent, execution receipts and user acceptance are distinct. Preserve stable requirement/scenario IDs, before/after change intent and all unaffected scenarios. No configurable schema engine, additional orchestration model tier or replacement SDD utility is required. Existing initializer and record helpers are optional conveniences.

Decisions DEC-SDD-1 through DEC-SDD-6, alternatives and risks are preserved in the [accepted change design](../changes/archive/2026-11-22_native-sdd-process/project.md). Historical evidence and source attribution remain intact. Profiles and model statements are not isolation or correctness proofs.


## Rust Engine boundary

The optional Rust Engine lives alongside the skill collection at repository root, with executable `pentapro`. Native CLI services, filesystem controls and presentation do not make existing skills or factory operation depend on the binary. The [accepted I1 architecture](../changes/archive/2026-11-26_engine-foundation/project.md) records the JSON contract, guarded filesystem scope and limitations; OpenSpec compatibility remains future work. The statement above that no replacement SDD utility is required remains true for the skills-only route.
