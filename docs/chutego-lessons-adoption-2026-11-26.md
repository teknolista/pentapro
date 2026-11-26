# ChuteGo lesson adoption follow-up — 2026-11-26

Scope: three developer-approved follow-ups from the lesson review. Source baseline: PentaPRO `7be471763b322bec91399e8929c36c47fccd69d0`; ChuteGo `e34f43d140cadd7cc65f70aa5aa0636fa150e0d4`. This is bounded instruction/documentation maintenance by the main session, not a new multi-agent implementation or a product-equivalence audit. No publication was requested.

## Adoption and ownership

| ChuteGo finding | Current owner and disposition |
| --- | --- |
| LL-001: stable requirement IDs | Already covered by PentaPRO identity and specification-review guidance; retain existing owner. |
| LL-002: decimal rejection and large-value misrepresentation | Behavior Testing 1.3.1 explicitly reaches numeric guidance for relevant work. Its test-design reference traces input, conversion, calculation, rounding and presentation, independent expectations, accepted/out-of-range values and valid controls. |
| LL-003: selected content outside viewport | Already covered by UI Design Terminal real-PTY and viewport guidance. |
| LL-004: late discovery of criteria | Already covered by Software Factory journey inventory, criterion/owner/evidence mapping and early representative slice. |
| LL-005: mistyped push SHA | Git Ship 2.2.1 obtains the complete candidate from Git after commit/hooks, compares it with the inspected commit, retains that value for the refspec and remote query, and reconciles changed HEAD. |
| Retrospective: downloader and development context omitted | Existing journey-evidence contract inventories supporting tools, acquisition, contexts, exclusions and authority. |
| Retrospective: readability and technical trade-offs | Existing terminal and delivery guidance covers rendered acceptance and practical alternatives with total validation/maintenance cost. |
| Stale closure navigation | ChuteGo's archived uniform-picks current disposition cites its recorded publication; the initial checkpoint points to subsequent completed runs and reports. Historical phase entries, completed JSON records and append-only events remain intact. |

The ChuteGo sources are `docs/agents/lessons-learned.md`, `docs/agents/relatorio-consolidado-pentapro.md`, `docs/agents/relatorio-retrospectiva-chutego-pentapro-2026-11-25.md` and the historical-analysis, uniform-picks and product-process-audit run records in that repository. Their original observations and limits retain authority; adoption of a prevention proposal does not establish its effectiveness on future projects.

## Verification and limits

Executed successfully: package metadata freshness, collection validation (335 Markdown files, 1,370 local links/anchors, 26 package versions, zero issues), 20 evaluation-case definitions and whitespace checks. All 10 links in the two modified ChuteGo documents resolve; all eight completed run/event files checked match their HEAD bytes, and the referenced publication commit exists locally. These checks do not query the remote. Authored numeric and commit-identity briefs include matching, ambiguous and narrower/nonmatching controls; they are not executed model trials. No executable source changed, so no new application/helper unit tests are warranted for this maintenance. Existing helper regressions and the prior source CI remain historical evidence, not a new execution here.

The instructions add concrete decision steps but do not mechanically enforce numeric correctness or prevent every wrong-ref publication. No new runner, hook, dependency, model setting, consumer synchronization, remote query or causal quality/cost experiment was introduced. Full ChuteGo/ChuteGPT equivalence and the previously recorded S21 decisions, untested scenarios, platform and accessibility limits remain outside this bounded correction.
