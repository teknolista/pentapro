# Skill directory migration

Scope: relocate all canonical top-level skill packages to `skills/<name>` and update source references, packaging, metadata, evaluation, CI and documentation. Preserve package contents, installed-project `.agents/skills` paths, user customizations and historical evidence.

Acceptance: all 24 packages are discoverable at the new source path, standalone resources and exports remain complete, supported metadata reflects the new paths, historical baseline evaluation remains usable, and the collection checks and affected helper tests pass. Existing installations are not modified.

This relocation record describes the 24-package pre-split snapshot. The current source catalog has 26 packages after the [UI owner migration](ui-skill-migration.md); original relocation acceptance and historical evidence remain tied to their original scope.
