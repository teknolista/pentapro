# I2 focused specification rereview

- Invocation `spec-i2-02`, run `engine-openspec-read`, record v7.
- Reviewed fingerprint `3bff0fc9fb87e6c222c80bf60f42f287ab7383adf03c037ee0c9f093073e3ca0`, HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`. Fresh snapshot matches the record.
- Verdict: **BLOCK for one remaining contradictory permission path**. The previous three findings are otherwise resolved; this is a bounded clarification, not a new user decision or a request for broad research.

## Prior finding disposition

- SPEC-I2-01: XDG unset/fallback, exact conservative `.openspec-store` marker, ancestor stopping and metadata/scan distinction are now written clearly. One dependency between those steps and the existing permission fixture remains, below.
- SPEC-I2-02: resolved. PRODUCT defines text error rendering and explicit unknown-filesystem-error fallback; PROOF requires representative executable comparison before acceptance.
- SPEC-I2-03: resolved. Complete pinned parseSpec/helper path is mandatory; list per-entry read/parse errors produce zero, show parse errors produce show_error, discovery errors remain whole-command failures. No discretionary unsupported lexical shortcut remains.
- Stale next-action and overly broad unverified-evidence statements were reconciled.

## Remaining blocker — marker preflight prevents the promised mode-000 scan error

PRODUCT Resolution requires inspecting `.openspec-store` under each planning directory before qualification and says metadata EACCES yields `unsupported root selection`, exit 2. Lists/Show then promise the captured unreadable-specs-directory EACCES diagnostic, linking oracle-stable-node.md. That actual fixture chmods `specs` to 000.

A direct scoped POSIX control during this rereview under effective UID 1000 confirmed:

- lstat(specs) succeeds;
- lstat(specs/.openspec-store) fails errno 13 (EACCES).

Therefore the required preflight necessarily returns unsupported-root before the selected-directory scandir stage for that captured fixture. The current normative result and required scan-EACCES result cannot both be produced. This is a contract contradiction, not untested implementation behavior.

Choose and save a precise correction. Recommended conservative version: explicitly classify mode-000/uninspectable nested marker as preflight refusal (documented divergence), remove the assertion that the existing mode-000 oracle fixture must be matched by this slice, and retain actual oracle observation as historical upstream behavior. If scan-EACCES compatibility remains required, add a fixture whose execute permission permits marker lookup but whose read permission denies listing (e.g. mode 111), observe both programs and specify that branch. Alternatively deliberately redefine the marker/metadata error precedence to match the mode-000 upstream envelope. Do not silently skip a required safety preflight or fabricate absence of a marker.

Add one acceptance control proving preflight EACCES refusal and a distinct scan EACCES control only if that latter branch remains supported. Adjust PRODUCT, PROOF and PROCESS consistently.

## Assessment and limits

The bounded list/show slice, explicit configuration/identifier restrictions, source-pinned parser contract, readable error behavior and portable differential harness plan are coherent after this one correction. Full OpenSpec parity remains in the roadmap. No other blocking issue identified in the focused scope.

Read six current contract documents and previous report, verified current fingerprint, and executed only the disposable permission-metadata control above. No Rust, oracle or full collection suite rerun; no project/source/index/record edits aside from mandatory prompt log. Linux-only permission observation is not a sandbox or all-platform guarantee.

PDSA: planned rereview of the three corrected boundaries; inspected definitions and tested the consequential permission-path premise; found one deterministic conflict; returned the bounded correction to the owner. No new lesson identified. Configured role factory_spec; independently observed model/runtime usage and costs unavailable. Review outcome is not developer acceptance.
