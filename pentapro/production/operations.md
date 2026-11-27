# PRODUCTION — adoption and recovery

Status: accepted scoped baseline, 2026-11-22.

Bundle 2.0.0 contains Setup PentaPRO 2.0.0, PentaPRO 4.0.0, Software Delivery 2.0.0, Software Factory 1.0.0 and UI Design 2.0.0 alongside unchanged packages. The [collection catalog](../../README.md#available-skills) owns current versions and supported installation routes.

Adopt updates deliberately at project scope. Preserve customized guidance/profiles, logs, historical records, active contracts and staged selections. Map prior work into native records with provenance rather than fabricating a baseline. No global tool uninstall, hooks, permission weakening or application deployment is part of this migration. See the [adoption guide](../../docs/native-sdd-migration.md).

Archive uses the developer's local date and refuses collisions. Reconcile actual source/target/effect state before resuming interrupted consolidation, archive or publication. Cancelled changes preserve partial effects/recovery decisions, never silently promote abandoned intent or roll back source. Publication failure preserves successful local work. Merge, deployment, release, force push and rewriting history retain their own authority.

Collection-local installed copies/profiles have been reconciled with source; former empty planning scaffolds remain dated history and former local workflow copies were moved outside discovery. Other consuming projects are outside this accepted change's scope. Runtime discovery and application-specific checks remain adoption requirements where applicable.


## Engine I1 operation

Build and run the local Engine using the Rust commands in the [repository README](../../README.md#pentapro-engine-early-development). The first increment targets observed Linux behavior; other platforms and hosted CI remain unverified. Managed files are preserved, and interrupted lock/staging state requires inspection. Installation/removal does not migrate or delete project records. [Operating contract](../changes/archive/2026-11-26_engine-foundation/production.md).


## OpenSpec read compatibility I2

The [accepted operating contract](../changes/archive/2026-11-27_openspec-reading/production.md) covers the local offline read-only slice. Evidence is limited to Linux and exercised cases; other platforms and complete compatibility are not certified. The CLI may read content outside the project via an explicitly selected capability directory symlink, matching the observed OpenSpec behavior; evaluate project trust before use.
