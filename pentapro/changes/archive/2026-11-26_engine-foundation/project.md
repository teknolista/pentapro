# PROJECT · Architecture and decisions

## Decisions

- ADR-001 Confirmed: OpenSpec v2.2.0 SHA f1cd852f4edce22b8df9548a4df889172ca8ff25 is the frozen baseline; new upstream versions require a separate reviewed update.
- ADR-002 Confirmed: Rust monorepo, executable `pentapro`, sources `src/`, integration tests `test/`, output `target/`. Cargo package `pentapro-engine` starts at 0.1.0, separate from bundle 3.1.2. Existing MIT license applies; retained third-party notices accompany copied/adapted material.
- ADR-003 Proposed for first delivery: synchronous filesystem-oriented core and thin clap CLI; Serde/serde_json for versioned output; std filesystem APIs, no async runtime/database/daemon until required. Pin resolved dependencies in Cargo.lock. Rust edition 2024, rust-version chosen from actual dependency support and verified toolchain; do not claim lower MSRV without testing.
- ADR-004 Native records remain the six-file contract. Compatibility facade is explicit and uses upstream files; no silent OpenSpec-to-native migration. Core parsers/storage shared where semantics match. Separate command adapters avoid accidental schema conflation.
- ADR-005 Existing Python run/event helpers remain canonical contracts and usable without Engine. Port by fixture-backed equivalence before introducing Engine-owned writers. Never allow Python and Rust to concurrently mutate the same run.
- ADR-006 Files are source of truth; derived indexes may be discarded. All writers require scoped locks, preflight, staging and conflict checks. No automatic lock removal or archive repair. Reject unsafe path components before resolution.
- ADR-007 Semantic acceptance, cognitive agent reasoning and human authorization cannot be made true by deterministic validation. Explicit receipts record observations and limits.

## Boundaries and data

CLI parser/presentation → command service → pure native/change/domain validation → guarded filesystem adapter. Later: compat command adapter, loss-aware Markdown/delta parser, schema DAG, run/event repository, policy/evidence service, host adapters and packaging. Business logic is testable independently; integration tests execute the real binary. No imported record string is executed as shell.

Native baseline lives in pentapro/{product,project,production,proof,process}/; changes and archive match existing collection contracts. Root detection uses nearest ancestor marker. I1 change identifier grammar: `[a-z]+(-[a-z]+){1,2}`, no path separators. Manifest ownership remains plugin.json and existing packaging scripts; Cargo does not regenerate them.

Threats: traversal/symlink escape, collision overwrite, concurrent creation, stale evidence, untrusted Markdown execution, prompt/credential leakage, and false approval. I1 addresses static unsafe paths/collisions and cooperating-writer exclusion. Adversarial simultaneous path replacement is not a sandbox guarantee; stronger descriptor-relative filesystem access is a later hardening gate before hostile shared roots. Partial init is recoverable by idempotent retry; change creation is staged. Do not delete stale locks automatically.

## Dependency assessment

See [technology assessment](technology.md). Prefer established maintained crates, minimal features and measured workload performance. Popularity and benchmark superiority are not inferred from language choice. Dependency selection is revisited with licenses/advisories and actual build/benchmark evidence each increment.
