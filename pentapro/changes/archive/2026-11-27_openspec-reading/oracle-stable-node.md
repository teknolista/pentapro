# Stable Node verification of OpenSpec I2 oracle fixtures

On Linux with actual Node `v26.10.0`, reran the pinned OpenSpec 2.2.0 build at `f1cd852f4edce22b8df9548a4df889172ca8ff25`. This Node version is within the upstream `>=22.20.0` declared range; it is not Node 24 and this observation does not certify other versions or operating systems. PATH prefixed the Node 26 binary through a child-only environment; isolated HOME/XDG and telemetry/update-disabled settings remained in the existing scripts. Restricted sandbox network applied.

Original Node 27 alpha outputs preserved in `/tmp/engine-oracle-node27.json` and `/tmp/engine-boundary-node27.json`; new outputs `/tmp/engine-oracle-results.json`, `/tmp/engine-boundary-results.json`. Scripts `/tmp/engine-oracle-probe.py` and `/tmp/engine-boundaries-probe.py` both exited 0. For corresponding cases, compared `exit`, normalized `stdout`, normalized `stderr`, and per-command `changed` boolean exactly: **12/12 initial cases and 21/21 boundary cases matched**. Scripts normalize randomized project roots as `<PROJECT>` or `<TMP>` before output; no other semantics were normalized. This compares only tested synthetic cases, not full parser/root semantics or Unicode locale matrix from the separate readiness probe. Fixture content hashes/symlink-target snapshots report no persistent changes in their monitored trees; transient identical writes or effects outside the trees are not excluded.

## Inaccessible specs directory

Repro `/tmp/engine-inaccessible-probe.py`: create a temporary project with config.yaml `schema: spec-driven`, a changes directory and specs directory, chmod specs to `000`, run list/show, then restore directory permissions. Effective UID was 1000; `os.access` denied read and execute and a real `readdir` raised `PermissionError` errno 13, confirming the restriction was effective. Other fixtures were unaffected. Commands used Node 26 with throwaway HOME/XDG and no network-requesting command. Captured output (project root normalized):

### `openspec list --specs --json`

Exit 1. stdout:

```text
{
  "specs": [],
  "root": null,
  "status": [
    {
      "severity": "error",
      "code": "list_error",
      "message": "EACCES: permission denied, scandir '<PROJECT>/openspec/specs'"
    }
  ]
}
```

stderr:

```text
```

### `openspec show alpha --type spec --json`

Exit 1. stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "EACCES: permission denied, scandir '<PROJECT>/openspec/specs'"
    }
  ]
}
```

stderr:

```text
```

The permission case validates the observed nonroot Linux EACCES diagnostic for an unreadable specs directory only. It does not cover inaccessible individual spec files, config, CWD, other users, Windows permissions or shell UI. No `validate` command was run.
