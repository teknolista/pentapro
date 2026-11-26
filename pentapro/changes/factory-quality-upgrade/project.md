# PROJECT — design and risks

Keep one principal orchestrator and six roles. Use existing owners and progressive disclosure; add no supervisory agents or external orchestration. Preserve five pillars. UI common guidance is concise and local to each installed package; standalone packages must not require sibling filesystem resources. Catalog count changes from 24 to 26 and public metadata follows actual package versions.

Alternatives: a single mixed UI package retains overload; three independent packages improve task selection but need a complete caller/license/tool inventory and negative activation cases. Hidden common package dependency is rejected. Evidence helpers remain optional and explicit; keep current conservative fingerprint guards until a tested replacement is warranted. Safe evidence reuse uses original receipts and relevant delta review rather than weakening run-state validation.

No shell execution from records; preserve exit codes, errors and unknown usage. Existing setup provenance safeguards are assessed before adding helpers. Unknown customized installed copies stay conflicts; never infer baseline from arbitrary old blobs. No credential/prompt copying.
