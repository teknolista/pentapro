# Focused I2 final reconciliation review — spec-i2-07

- Run: `engine-openspec-read`; invocation: `spec-i2-07`.
- Reviewed current source fingerprint: `bcc12d2a4fefc6fa009286f9acdb1bc58d7caa45c7bdaa17413d65dd8369f3ad`; HEAD `d17b923bf0c274334f0fbe1812ecefd567367fa2`.
- Verdict: **PASS for the assigned final specification/evidence reconciliation.** No blocking finding in this focused scope. This is not developer acceptance or full OpenSpec parity approval.

## Reconciliation result

Read CHANGE, PRODUCT, PROOF and PROCESS, prior focused `spec-final.md`, the final independent implementation review/verification reports, and the supplemental `eacces-followup.md`. PRODUCT paragraphs 16, 20 and 26 now consistently distinguish the deliberate mode-000 preflight refusal from the actually observed mode-0111 post-preflight scan failure. Each present-tense claim of observation points to the supplemental receipt. The stale phrases that previously described this branch as unobserved/not tested are absent from these current owning documents.

The supplemental receipt records separate equivalent Engine/upstream temporary fixtures, Linux UID 1000, successful marker metadata lookup (ENOENT), failed directory enumeration (EACCES), and matching status/stdout/stderr for list/show in text and JSON. PRODUCT no longer claims that mode 000 itself is equivalent to upstream. The earlier final verification report's unestablished-branch statement is historical evidence for its tested snapshot, and PROOF/current PRODUCT link the later follow-up rather than rewriting that receipt. This chronology is accurate.

CHANGE continues to identify a bounded read-only I2 slice, not all list/show behavior or OpenSpec validation; acceptance is pending. PROCESS marks the research/implementation/review work performed while leaving result presentation/acceptance unfinished. PROOF retains the actual tested implementation snapshot `09f59c1940f0eb08f658c9b02a99054afa5a85b153bb644830a8bfd089385d47` and explicitly identifies documentation-only reconciliation as requiring affected checks; it does not restamp old execution as a new test. The supported syntax, conservative refusals, composed-symlink condition and external-directory disclosure remain explicit.

The recorded independent reports support 23 Rust integration tests and 43 differential comparisons plus the intentional refusal in the tested Linux/Node26 scope. I inherited those execution results by inspecting their receipts; I did not rerun product tests or independently re-prove source/test byte continuity. The orchestrator's verifier/reviewer owns continuity assessment for the current source snapshot. Finite tests do not establish all Markdown inputs, all permissions, other OSes/Node versions, hostile path races or complete upstream parity; the owning documents preserve those limits.

LL-010/LL-011 distinguish locally confirmed causes/corrections from proposed prevention and disclose byte-hash versus build-provenance limits. The three unrelated untracked numbered proposal documents were excluded from this review and were not treated as authority or touched.

## Direct checks and PDSA

Directly executed from the project root:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_collection.py`: 383 Markdown files, 1457 local links/anchors, 26 version checks, zero issues.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_skill_evals.py --check-cases`: 20 cases validated.
- `git diff --check`: exit 0.
- Source fingerprint independently recaptured before and after review: unchanged and equal to the packet snapshot above.

No project source/specification/index/run/events/lesson edits. Only mandatory prompt logging and this requested `/tmp` report were written. PDSA: planned the focused stale-status/evidence check; read current owning documents and chronological receipts; checked links and snapshot; found reconciliation consistent and returned the scoped verdict. **No new lesson identified.** Configured role/model/effort are not independently observed runtime attribution; token usage and cost remain unknown.
