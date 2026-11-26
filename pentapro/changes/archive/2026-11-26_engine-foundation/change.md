# Change: engine-foundation

- Status: Archived; accepted I1
- Baseline: `5b39b1bd2c760a4d1c96bd9d05bd28f72dcec6ad`; existing collection pillars remain authoritative for skills/plugin behavior.
- Owner: host main orchestrator; result acceptance: developer.
- Intent: specify the complete hybrid software factory Engine, recover OpenSpec 2.2.0 behavior, and begin Rust implementation with a reviewed vertical CLI increment.
- Authority: developer explicitly requested specification and implementation on 2026-11-26. Developer approved the reviewed I1 result, consolidation, archive, commit and normal push on 2026-11-26. No merge, release, deployment, consumer rollout or global configuration authority.
- Scope: complete target requirement inventory (detailed executable contracts are refined and reviewed per increment) and incremental delivery; first implementation is native filesystem CLI foundation. Product-wide parity remains mandatory for 1.0 and is not claimed by the first increment.
- Coexistence: preserve `skills/`, plugin manifests/adapters, installed/custom agents, existing pillar records, active changes and histories. `src/`, `test/`, `Cargo.toml`, `Cargo.lock`, `target/` belong to Engine; collection and binary versions are independent.
- Reference: OpenSpec v2.2.0, commit `f1cd852f4edce22b8df9548a4df889172ca8ff25`; developer selected current stable pinned revision. Initial Portuguese report is historical design input, not a second specification.
- Overlap: other active collection changes are preserved; Engine increment does not consolidate them or change their status.
- Next: publish the accepted I1 snapshot; subsequent increments remain pending in PROCESS.
- Final disposition: I1 accepted; archive 2026-11-26; publication to be confirmed separately in the run record.

## Five dimensions

[PRODUCT](product.md), [PROJECT](project.md), [PRODUCTION](production.md), [PROOF](proof.md), [PROCESS](process.md).

## Evidence inventories

[OpenSpec recovery](openspec-inventory.md) and [factory deterministic inventory](factory-inventory.md) own detailed recovered capabilities, sources and improvement-plan reconciliation. These are input evidence; PRODUCT owns requirements. Research is not behavioral parity proof.
