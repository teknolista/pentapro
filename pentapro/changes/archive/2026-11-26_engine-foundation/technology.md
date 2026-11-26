# Technology assessment · 2026-11-26

Observed upstream dependencies and source mappings: [OpenSpec inventory](openspec-inventory.md). Upstream uses TypeScript/Node, commander, Zod, YAML, Inquirer, chalk/ora, diff, picomatch/tinyglobby and Vitest. Its implementation is input evidence; Rust does not need one crate per npm dependency.

| Capability | Rust choice / candidate | Decision and evidence |
|---|---|---|
| CLI parser (commander) | clap 4, derive | Select for I1: generated help, typed options and established CLI conventions. [Primary docs](https://docs.rs/clap/latest/clap/) describe maintainership/performance goals, not proof of superiority on this product. Resolve and lock actual version during build. |
| Typed contracts / JSON (Zod) | serde + serde_json | Select I1: typed serializable structures; [Serde design](https://serde.rs/) avoids reflection. Explicit validation still required; serialization alone is not schema validation. |
| Filesystem / locks | std::fs, std locks or create_new lock file | Minimal first increment; no fs2 dependency solely for locks. [fs2](https://docs.rs/fs2/latest/fs2/) is an alternative if supported std APIs prove inadequate. Cooperating-writer locks are not a hostile filesystem sandbox. |
| YAML/schema validation | serde-compatible YAML parser, jsonschema where required | Pending I3 spike: fixture fidelity, maintained parser, license/advisories and untrusted input limits; avoid choosing an unmaintained YAML port by habit. |
| Markdown | pulldown-cmark or source-span parser | Pending I2: preserve original text, fenced examples and upstream delta semantics; round-trip tests decide. |
| Diffs/globs | similar, globset + walkdir | Candidates for I2/I3; check behavior against upstream diff/picomatch fixtures, not assumed equivalence. |
| Prompts/progress | dialoguer/inquire and indicatif | Candidates I5; non-TTY and cancellation parity required. |
| Terminal dashboard | Ratatui + crossterm only if needed | [Ratatui source](https://github.com/ratatui/ratatui) is an established option for interactive UI; avoid adding a TUI runtime to plain I1 CLI output. |
| Dates/hashes/process | time or chrono, sha2, std::process | Defer until actual run/receipt contracts are ported; match Python canonicalization and timeout semantics through fixtures. |
| Tests | Rust test harness, std::process; optional tempfile/assert_cmd | Select harness + actual binary integration target under test/. Additional test crates only if justified. |

No numerical popularity ranking, update-frequency score, performance benchmark or comprehensive dependency security audit was executed. Primary docs were inspected for clap, Serde, Ratatui and fs2 on this date; the source release/tag and exact dependencies were read from pinned OpenSpec. Choices minimize I1 runtime/dependency surface; Cargo.lock captures resolved versions, licenses and advisories require release-time reevaluation. MSRV is only advertised after actual toolchain verification; current observed Rust is 1.100.0. Dependency performance must be measured on representative workloads rather than asserted from reputation.

## Observed I1 resolution

Cargo.lock resolved clap 4.6.10, serde 1.0.229 and serde_json 1.0.154 with Rust/Cargo 1.100.0; Cargo declares rust-version 1.100. No lower MSRV is claimed. Final dependency graph is the committed-candidate lockfile, not a latest-version assumption.
