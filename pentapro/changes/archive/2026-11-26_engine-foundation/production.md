# PRODUCTION · Local runtime and distribution

I1 is a local development CLI, no hosted service. Build from repository root using `cargo build --locked`; run `cargo run --locked -- --help`; install with `cargo install --path . --locked` after review. Tests use `cargo test --locked` (integration target explicitly maps to test/cli.rs). Cargo.lock is versioned for binary reproducibility; target/ is ignored and holds disposable outputs only. No root/global dependency installation is part of the change.

Linux x86_64 is the observed development target; Rust 1.100.0/Cargo 1.100.0 were available at intake. macOS/Windows, older Rust, package managers, signed releases and native integration are pending checks; do not advertise certified support. Runtime uses only project filesystem and process environment required for path selection; there is no automatic network, analytics or model invocation.

Developer and installed journeys both require writable chosen root only for mutations. Read operations work on read-only projects. Errors identify operation and path without dumping record contents or secrets. Non-UTF8 paths must fail clearly or remain losslessly represented internally; presentation is not an authorization decision. Local symlink policies are documented and tested.

Upgrade retains files; removal of the binary does not remove specifications/logs/agents. No automatic project migration in I1. Migration later requires preflight plan, conflict inventory, backup location, explicit apply and evidence; read-only inspection is always available. Existing collection Python/Node validation and plugin manifests continue to work independently.

Recovery: failed init can be retried, preserving prior files; failed staged change never appears as a completed active change. A leftover operation lock/stage after interruption is reported for inspection, never silently removed. No power-loss/hostile-writer guarantees are claimed. Any remote install/update/Git effects in future compatibility mode require explicit user-selected commands and offline behavior diagnostics.

CI: a separate Rust job/workflow runs fmt, clippy and tests with locked dependencies, retaining collection CI. No registry publication or release automation in I1.
