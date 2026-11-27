# Independent I2 review — review-i2-02

- Run: engine-openspec-read, record v11. Reviewed working-tree fingerprint: `a310a001766459b35498b62e4728eb2362d18f2f70eeb9b1cb44ad85add75bae`; HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`.
- Verdict: **Changes requested**. This is an independent read-only code/test review, not product acceptance.

## I2-REVIEW-01 — P2, blocking: preserve ECMAScript line-terminator behavior in parser regex ports

Locations: `src/spec_parser.rs:67–80` (heading) and `src/spec_parser.rs:45–47` (fence opener info string). Introduced in this uncommitted I2 implementation.

The pinned Markdown parser uses `/^(#{1,6})\s+(.+)$/`; JavaScript `.` excludes U+2028 and U+2029. The Rust `heading()` accepts the entire remainder, so a supported spec containing `### Requirement: A<U+2028>B` (or U+2029) is reported with one requirement, while upstream reports zero. The production command succeeds in both cases with different JSON content. The contract expressly requires the complete pinned parseSpec helper behavior for all decoded input; there is no unsupported-Markdown escape hatch.

The same missing distinction appears in fence detection: source `code-fence.ts` matches `^\s*(`{3,}|~{3,})(.*)` and tests only its captured info string for backticks. For the opener `` ```foo<U+2028>` `` followed by a requirement and a closing fence, upstream opens the fence (captured info stops before U+2028) and masks the requirement. Rust checks the entire tail, sees the later backtick and treats the opener as invalid, exposing a requirement that upstream hides.

Minimal spec prefix: `# Alpha\n\n## Purpose\n\nPurpose text\n\n## Requirements\n\n`; append either `### Requirement: A\u2028B\nBody\n`, its U+2029 variant, or `` ```foo\u2028`\n### Requirement: Hidden\nBody\n```\n ``. Execute `show alpha --type spec --json` in a synthetic root. Freshly built Engine produced requirementCount 1; pinned OpenSpec/Node 26.10.0 produced 0 for all three. A normal ASCII control matched exactly.

Reproduction and exact captured outputs: `/tmp/i2-review-resume-probe.py`, `/tmp/i2-review-resume-results.json`. Engine built directly from reviewed source with `CARGO_TARGET_DIR=/tmp/i2-review-resume-target cargo build --locked --offline` (passed); no stale I1 target was used. Reference: OpenSpec f1cd852f4edce22b8df9548a4df889172ca8ff25 built CLI, Node v26.10.0, isolated HOME/XDG and disabled telemetry/update controls.

Correction: port the exact regex capture/end-anchor semantics rather than accepting/rejecting all Unicode separators indiscriminately; preserve the differing heading-start versus section-boundary regexes. Add real differential regressions for U+2028/U+2029 inside heading titles and fence info strings, including ASCII controls and trailing-separator edge cases. Recheck full suite.

## I2-REVIEW-02 — P2, blocking evidence gap: differential runner does not verify its reference identity

Location: `test/differential.py:14–23`. PROOF explicitly requires exact upstream SHA verification and Node/build identity. The runner merely resolves three supplied paths and immediately invokes them; it never checks the source commit, dirty state, Node version or built output identity and reports only `PASS <arguments>`. Pointing it at a later/stale OpenSpec checkout can therefore produce an indistinguishable successful receipt without testing the pinned baseline. The present manual comparisons used the correct checkout, but the committed acceptance tool does not enforce or record that premise.

Correction: preflight the supplied oracle's exact pinned repository SHA (and relevant clean-source/build identity), fail before tests on mismatch/unverifiable reference, and emit Node version plus binary/build hashes/identity in its receipt. Add a mismatched-reference control and retain the existing passing pinned execution. This is a harness contract deficiency, not a claim that the 15 manually observed comparisons used a wrong oracle.

## Coverage and limits

Inspected CLI option dispatch, root/global preflight, spec discovery, raw/JSON output, parser, MIT attribution and the differential runner. Read the pinned parseSpec, requirement-text, requirement-blocks and code-fence implementations. Checked PDSA protocol and relevant LL-008/009. No source, index, run/event or lessons writes were made; only the mandatory prompt log and this requested /tmp report were written. Full suites are owned by the parallel verifier and were not duplicated here.

The external *directory* symlink read is not separately asserted as a blocker: PRODUCT expressly preserves explicitly shown directory links, upstream trusts the resolved capability directory for such a show, and the generic PROJECT containment wording does not unambiguously override this. This remains an explicit contract/security limitation rather than evidence of a new unintended write; no production write or process/network execution was found in the reader. Adversarial replacement races and other OS behavior remain unverified.

PDSA: planned targeted parser/path/evidence review; built a fresh isolated binary; compared three adversarial Unicode cases plus a normal control; routed corrections to orchestrator without edits. Lesson candidate: when porting regex-based parsers across languages, compare capture boundaries and line-terminator semantics, not only whitespace trimming. Status proposed; local counterexamples confirmed, general prevention not measured. Runtime/model usage attribution remains unknown.
