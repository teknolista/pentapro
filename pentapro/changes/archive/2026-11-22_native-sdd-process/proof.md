# PROOF — planned and observed checks

Result acceptance: explicit owner approval “sim, prossiga” on 2026-11-22. Current migration execution evidence belongs in [the maintenance review](../../../../docs/native-sdd-review.md) and [run record](../../../../docs/agents/runs/native-sdd-process/run.json); preserve tested snapshot identities there instead of duplicating full logs.

| Criteria | Check method | Current evidence state |
| --- | --- | --- |
| SC-SDD-1, SC-SDD-3 | Existing initializer preservation/symlink regressions and fresh output inspection | 14 initializer tests passed, including an integrated rerun; bootstrap separately reviewed |
| SC-SDD-2, SC-SDD-4 through SC-SDD-8 | Independent instruction/contract review plus representative disposable agent-guided trials | Authored scenarios plus three bounded synthetic agent trials; independent review found and rechecked corrections; final pre-closure freshness confirmed; closure receives separate checks, no universal claim |
| SC-SDD-9 | Active-reference inventory, CLI option/fixture tests and package metadata/links | Integrated metadata/case/link checks passed; historical/provenance references retained |
| SC-SDD-10 | Host-adapter parity/schema tests, package export tests, grader controls and isolated probes | Integrated suite and isolated probes passed; affected instruction/package tests rerun after corrections |
| Preserved domain behavior | All existing Python/Node helper suites and collection checks | 130 Python tests and 47 Node controls passed; affected 41 package/role/validator tests and 26 UI tests rechecked after instruction-only fixes |

A structural check or authored scenario does not establish a real host invocation, deployed service, device behavior or semantic correctness. Report model/runtime limits and actual failures explicitly. A changed contract or code invalidates affected previous evidence.
