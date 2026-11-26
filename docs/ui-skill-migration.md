# UI skill migration and preservation

PentaPRO 3.0.0 replaces the mixed `ui-design` source package with three standalone 1.0.0 packages. There is no forwarding alias. The owning task agent selects web, native Android or terminal expertise; mixed-platform tasks can use more than one for distinct deliverables. Other platforms require their actual framework guidance and an explicit coverage limit.

## Resource destinations

| Previous resource | New source owner |
| --- | --- |
| Browser guidance, prototype assets, Python gallery tools and tests | `skills/ui-design-web/` |
| Android implementation procedures, native platform guidance and Android worked example | `skills/ui-design-android/` |
| Common design/feedback/maintenance principles | Concise package-local guidance in the applicable standalone package |
| Terminal interaction, output modes and real viewport acceptance | `skills/ui-design-terminal/` (new capability) |

Each package retains its own MIT notice and applicable source attribution. Historical reports retain their dated old names; local resource links resolve to maintained destinations. HTML prototype checks establish web-concept properties, not Android or terminal behavior.

## Reviewed adoption in a consumer

1. Inspect effective host discovery, installed `ui-design` location, installed revision/lock and project customizations. A matching old blob alone is not a reliable installation baseline. Do not infer installation from source availability.
2. Select only the needed new owners and inspect their contracts/resources. Export to a new versioned destination using the existing package helper; never overwrite plugin caches or existing bundles.
3. Review old-to-new content and project references using the actual known installed baseline. Unknown or intentional local changes are conflicts: retain the old customized copy and resolve them explicitly. Preserve custom roles/models, permissions, manifestos, logs, lessons and index selections.
4. Reconcile authorized project references, then retire the old discovered installation only after its custom content is accounted for and replacement discovery is verified. This source change performs no live consumer migration.
5. A repeat adoption with identical selected packages/references needs no change. Reconcile duplicate discovery instead of leaving two active skills with competing ownership. If discovery fails, retain the prior installation and report the missing capability.

Package/host configuration checks do not prove runtime selection or UI quality. Use matching, ambiguous and nonmatching tasks, representative rendered states and actual user-task checks for the affected platform. Keep unavailable host/device/model trials explicit. User-wide adoption and Git publication require their own authority.
