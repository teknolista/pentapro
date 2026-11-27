# I2 independent specification review

- Invocation: `spec-i2-01`; run: `engine-openspec-read`, record version 6.
- Reviewed source fingerprint: `e19460d33e26bed8f2d630955990da853e522fe16fa80bfa7e6179f2127e9264`; HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`. A fresh `run_state.py snapshot` matched the supplied record.
- Verdict: **BLOCK for implementation pending three bounded contract clarifications below**. These are document corrections within the authorized scope, not requests for new product approval or broad additional research.
- Read-only review; only required prompt log was appended. No source, specification, index, run/event or lesson edits. Report saved in /tmp as requested.

## Reconstructed journey and scope assessment

A developer enters a Linux OpenSpec project, invokes `pentapro compat openspec list --specs --json`, selects a supported lowercase spec ID, then invokes `show ID --type spec` or `--json`. The reader selects a nearest local root, refuses deliberately unsupported registry/config/identifier cases, discovers specs with upstream link semantics, emits native OpenSpec-shaped output and does not mutate project or isolated HOME. The product explicitly preserves I1 native behavior and the complete future OpenSpec/factory roadmap. Unsupported validation, stores, worksets, filters and platform/locale cases are temporary feature restrictions, not removal from the final product.

PRODUCT/PROJECT/PRODUCTION specify a meaningful read-only slice. PROOF connects I2-001–004 to real-binary differential tests, golden cases, read-only checks and I1 regression controls. Existing oracle observations are limited examples rather than parity certification. Source SHA, final I1 delivery and authority are clear. An engineer can reconstruct the successful simple-spec journey, but currently must guess the following failure/refusal rules.

## Blocking findings

### SPEC-I2-01 — Make root preflight predicates internally consistent and executable

Evidence: product.md:14 says XDG paths have HOME fallbacks, then says to treat **unset** XDG paths as unsupported. These conflict for the common environment with HOME present and XDG_CONFIG_HOME/XDG_DATA_HOME unset. It also requires refusal on a “store metadata marker” without defining that path. The linked source does define it: OpenSpec `src/core/store/foundation.ts:28–29,86–93` uses `.openspec-store/store.yaml`, and `src/core/project-config.ts:691–708` checks that path under each specs/changes candidate.

Consequence: two correct-looking implementations can disagree on ordinary shell environments and store-layout detection, affecting both advertised commands before their observable output.

Correction: choose one exact policy and save it. Recommended: unset XDG => absolute HOME fallback; set-but-empty/relative/invalid XDG => explicit unsupported (or another explicit rule); absent HOME matters only when needed for fallback. Define the precise marker path or a deliberately more conservative existing-marker-directory rule. State whether ancestor preflight stops at the selected nearest qualified root or continues above it. Define “uninspectable” metadata versus an EACCES *directory scan* so the product's explicit EACCES list/show envelopes do not accidentally get replaced by `unsupported root selection`. Include distinguishing tests for unset XDG, relative XDG, marker file/directory and the EACCES fixture.

Owner: orchestrator/specification author. No new user decision required for these routine clarifications.

### SPEC-I2-02 — Close supported text/error outcomes instead of delegating them as Pending

Evidence: product.md:7–8 advertises both text and JSON commands. Lines 20 and 26 explicitly leave human errors and other unreadable paths pending. PROOF:7–8,12–16 nevertheless requires exact stderr/status/human comparison and meaningful error cases. The no-root text cases are recorded, but EACCES, external-link discovery failure and malformed JSON-show input text fallback are not governed consistently. An operational failure is still a result of a supported invocation.

Consequence: implementer must invent diagnostics or silently narrow supported text behavior while fulfilling a public form already in the contract.

Correction: define one exact per-command error renderer for all supported operational failures, with the appropriate exit/channel and template, and show how the recorded JSON diagnostic message maps to it. The pinned upstream shared renderer/source and existing no-root human observations can supply this without an exhaustive permission matrix; add focused executable controls for the chosen representative errors. Alternatively explicitly define a deterministic unsupported-error fallback and identify it as a deliberate divergence. State unsupported/unexpected OS-error handling; untested OS coverage may remain a disclosed validation gap, not an undefined runtime branch.

Owner: specification author; independent verifier later proves only exercised cases.

### SPEC-I2-03 — Define parser support and error/refusal precedence

Evidence: product.md:20 requires a discovered spec read/parse failure to yield `requirementCount: 0`. Line 30 allows the implementation to decide that an unhandled lexical construct instead fails the entire result with `unsupported Markdown construct`. No exact unsupported construct set or detection rule is specified, while pinned parser behavior and S4 include BOM/CRLF/fences and malformed content. There is no deterministic boundary between an upstream parse error, a supported parse result and an unsupported lexical form.

Consequence: count-zero versus whole-command exit 2 and JSON-show support become implementation-dependent; a simplistic parser could reject almost everything or accept inputs incorrectly while claiming the same requirement was met.

Correction: choose either (a) the complete pinned `parseSpec`/section/requirement/scenario helper path as normative for I2, with explicit errors and no discretionary lexical fallback, or (b) a precise bounded grammar plus enumerated reliably detected excluded constructs and precedence. Preserve upstream parser failure => list count 0 separately from a documented unsupported-feature refusal, if that latter class remains. Add cases proving both categories. The selected source routines are concrete and finite; no need to recover unrelated OpenSpec validators before this read-only slice.

Owner: specification author and later implementer; review the saved clarification before dependent code.

## Nonblocking reconciliation

- product.md:16 still says stable Node/OS permission semantics are unverified, while production.md and proof.md correctly record the exact Node 26 rerun and scoped EACCES observation. Replace that broad stale sentence with the narrower actual gaps.
- change.md Next still mentions provisioning the oracle despite the saved build/execution evidence. Point it to contract correction/review, preserving historical chronology separately.
- Existing generated reports retain /tmp reproduction pointers and only partial fixture bodies. PROOF correctly requires a portable repository harness during implementation. Do not promote the one-off report pointers to reproducible parity evidence until that harness exists.
- Extremely conservative ID/config refusals are visible in PRODUCT and maintain full future parity scope; they are acceptable as an initial subset if the result is labeled accordingly. They do not satisfy entire OpenSpec list/show feature families.

## Checks and limits

Inspected the six change records, saved oracle reports/results, I1 architecture/context, PentaPRO specification-review procedure, PDSA protocol and relevant LL-009. Inspected pinned upstream list rendering, root qualification/classification, store marker constants, shared error plumbing, show dispatch and parser entry points. Executed only source reads and `run_state.py snapshot`; no CLI oracle, Rust tests, dependency installs or collection validator were rerun for this document-only review. Parent's previous validation results are not reported as new executions.

No assertion that all source, safety behavior, locales, platforms or parser features have been audited. Full OpenSpec parity, runtime security and user acceptance remain separate gates.

## PDSA

Plan: reconstruct the supported journey and follow one success plus root/parser/error failures through five dimensions. Do: compare saved contract with evidence and exact owning source. Study: the slice is coherent but three failure-policy boundaries remain ambiguous. Act: return bounded corrections to the owner; no read-only source changes. No new lesson identified beyond the existing evidence-vs-claim and complete boundary-contract guidance.

Requested/configured role is factory_spec; independent runtime/model attribution and token/cost data are unavailable. Invocation outcome: review completed with changes requested, not developer acceptance.
