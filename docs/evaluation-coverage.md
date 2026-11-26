# Skill evaluation coverage

This inventory distinguishes artifacts from evidence. Package scenarios are authored matching/ambiguous/nonmatching briefs; registered cases are runnable definitions, not proof that a model trial ran. [Recorded trials](../evals/RESULTS.md) own actual execution and its tested snapshots. Helper tests do not establish skill selection or model compliance.

Selection: prioritize authorization/external effects, preservation, changed routes and representative cross-boundary failures. Add or revise a scenario when modifying one of those contracts; platform-specific cases need the actual toolchain/device/service for runtime claims. A missing package brief is a documented coverage gap, not certification or proof of ineffective instructions. Existing cross-boundary cases can cover a route even without a package-local file. Do not count a new brief as a passing trial or register it until an executable fixture/grader exists.

| Skill | Package-local scenarios | Registered executable case IDs |
| --- | --- | --- |
| agent-instructions | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| android-background | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| android-data-layer | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| android-di-koin | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| android-error-handling | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| android-integration-testing | No package brief; use applicable cross-boundary case and add one when this route changes | `android-route` |
| android-module-structure | [Authored brief](../skills/android-module-structure/evals/scenarios.md) | None registered |
| android-ui-testing | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| android-unit-testing | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| behavior-testing | No package brief; use applicable cross-boundary case and add one when this route changes | `behavior-denied-effect` |
| cybersec | [Authored brief](../skills/cybersec/evals/scenarios.md) | None registered |
| diagnose-defect | [Authored brief](../skills/diagnose-defect/evals/scenarios.md) | `diagnose-misdirection` |
| git-ship | [Authored brief](../skills/git-ship/evals/scenarios.md) | None registered |
| http-api | [Authored brief](../skills/http-api/evals/scenarios.md) | `delivery-sdd`, `delivery-plain` |
| mcp-server | [Authored brief](../skills/mcp-server/evals/scenarios.md) | `mcp-revisions` |
| peer-review | [Authored brief](../skills/peer-review/evals/scenarios.md) | `review-injection`, `review-clean` |
| penta-pro | [Authored brief](../skills/penta-pro/evals/scenarios.md) | `sdd-full-scope` |
| pr-quiz | No package brief; use applicable cross-boundary case and add one when this route changes | None registered |
| production-operations | [Authored brief](../skills/production-operations/evals/scenarios.md) | `production-target-mismatch`, `production-stale-green` |
| setup-pentapro | [Authored brief](../skills/setup-pentapro/evals/scenarios.md) | None registered |
| software-delivery | [Authored brief](../skills/software-delivery/evals/scenarios.md) | `delivery-contract-conflict`, `delivery-native-sdd` |
| software-factory | [Authored brief](../skills/software-factory/evals/scenarios.md) | None registered |
| technical-research | No package brief; use applicable cross-boundary case and add one when this route changes | `research-pinned-version` |
| ui-design | [Authored brief](../skills/ui-design/evals/scenarios.md) | None registered |

The four new high-consequence briefs (Git Ship, HTTP API, MCP Server and Diagnose Defect) have not been executed with models in this maintenance. The 15 registered definitions remain unchanged. The next comparison should use matching, ambiguous and nonmatching tasks, independent outcome controls and the actual host/model; record failures and unavailable evidence. No minimum file count can replace that comparison.
