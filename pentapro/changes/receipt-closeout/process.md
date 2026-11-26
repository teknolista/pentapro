# PROCESS

Authority: implement and test the agreed closeout policy. Source publication, baseline consolidation and archival remain pending. This is bounded source maintenance performed directly, not a new factory-role invocation.

- [x] T1 Write distinguishing receipt validation tests before implementation.
- [x] T2 Implement local/staged/committed validator and conditional CI lane.
- [x] T3 Reconcile factory/shipper contracts, versions, templates and docs.
- [x] T4 Run affected checks and inspect outcome/recovery boundaries.

Outcome: local implementation and checks complete. 27 focused receipt cases are included in the final 157-test root Python run; other unchanged package/Node suites passed as recorded in checks.json. Bounded source maintenance was performed directly with self-review; no independent agent verdict or hosted workflow run is claimed. No commit, push, consumer update or old-run rewrite performed. Next: review this change for eventual publication.
