# OpenSpec I2 readiness oracle — 2026-11-26

Pinned OpenSpec v2.2.0 `f1cd852f4edce22b8df9548a4df889172ca8ff25`, actual CLI on Linux Node `v27.0.0-alpha.0.0.0`. This is not CI Node 24 or a stable release. Synthetic temp-only fixtures, isolated HOME/XDG, telemetry and update checks disabled, network-restricted execution. Full reproducible fixture setup and actual commands: `the temporary one-off probe (portable replay pending)`; structured observations: `the temporary captured results`. `<TMP>` masks the throwaway fixture parent. All reported calls yielded no persistent file-byte/symlink-target differences within temporary tree; this does not establish absence of transient writes or changes elsewhere.

Source observations: root ordering, qualifying planning/config shape and declared/default store precedence are `src/core/root-selection.ts:275–340, 414–501`; targeted store pointer/YAML handling and precedence `src/core/project-config.ts:622–665`; global default path `$XDG_CONFIG_HOME/openspec/config.json` in `src/core/global-config.ts:59–84, 135–193`. `list` sets allowImplicitRoot based on cwd project.md (`src/cli/index.ts:470–501`); `show` calls root selection with its default (`src/commands/show.ts:25–32`), so they differ without roots. List sorting is JavaScript `id.localeCompare` (`src/core/list.ts:287`); text padding uses JS UTF-16 string length and padEnd in the same file, not Rust byte length.

## no-root-human-list

Fixture: empty cwd no root, no configured stores. Command: `openspec list --specs`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
```

stderr:

```text
✖ Error: No OpenSpec root found from the current directory.
Fix: Run openspec init to create a root here.
```

## no-root-human-show

Fixture: same empty cwd. Command: `openspec show alpha --type spec`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
```

stderr:

```text
✖ Error: Spec 'alpha' not found at <TMP>/empty/openspec/specs/alpha/spec.md
```

## no-root-json-show

Fixture: same empty cwd. Command: `openspec show alpha --type spec --json`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Spec 'alpha' not found at <TMP>/empty/openspec/specs/alpha/spec.md"
    }
  ]
}
```

stderr:

```text
```

## legacy-project-list

Fixture: openspec/project.md only, no config/specs/changes. Command: `openspec list --specs --json`. Additional environment: `{}`. Exit: 0; monitored tree changed: False.

stdout:

```text
{
  "specs": [],
  "root": {
    "path": "<TMP>/legacy",
    "source": "implicit"
  }
}
```

stderr:

```text
```

## legacy-project-show

Fixture: same legacy project. Command: `openspec show alpha --type spec --json`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Spec 'alpha' not found at <TMP>/legacy/openspec/specs/alpha/spec.md"
    }
  ]
}
```

stderr:

```text
```

## bare-root-list

Fixture: only empty openspec directory. Command: `openspec list --specs --json`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
{
  "specs": [],
  "root": null,
  "status": [
    {
      "severity": "error",
      "code": "no_openspec_root",
      "message": "No OpenSpec root found from the current directory.",
      "target": "openspec.root",
      "fix": "Run openspec init to create a root here."
    }
  ]
}
```

stderr:

```text
```

## pointer-config-only

Fixture: config-only root with store: alpha, no registered store. Command: `openspec list --specs --json`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
{
  "specs": [],
  "root": null,
  "status": [
    {
      "severity": "error",
      "code": "no_registered_stores",
      "message": "Declared in <TMP>/pointer/openspec/config.yaml: Unknown store 'alpha'. No stores are registered.",
      "target": "store.id",
      "fix": "Run openspec store setup alpha or openspec store register <path> first."
    }
  ]
}
```

stderr:

```text
```

## pointer-with-planning

Fixture: specs directory and config store: alpha, no registry. Command: `openspec list --specs --json`. Additional environment: `{}`. Exit: 0; monitored tree changed: False.

stdout:

```text
{
  "specs": [],
  "root": {
    "path": "<TMP>/shape",
    "source": "nearest"
  }
}
```

stderr:

```text
Warning: <TMP>/shape/openspec/config.yaml declares store 'alpha', but this directory is a real OpenSpec root; the declaration is ignored.
```

## malformed-config-only

Fixture: config-only invalid YAML. Command: `openspec list --specs --json`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
{
  "specs": [],
  "root": null,
  "status": [
    {
      "severity": "error",
      "code": "invalid_store_pointer",
      "message": "Invalid store declaration in <TMP>/malformed/openspec/config.yaml: the config file could not be read as YAML.",
      "target": "store.pointer",
      "fix": "Fix the YAML syntax in <TMP>/malformed/openspec/config.yaml."
    }
  ]
}
```

stderr:

```text
```

## default-store-no-root

Fixture: empty cwd and global config defaultStore alpha with no registered store. Command: `openspec list --specs --json`. Additional environment: `{}`. Exit: 1; monitored tree changed: False.

stdout:

```text
{
  "specs": [],
  "root": null,
  "status": [
    {
      "severity": "error",
      "code": "no_registered_stores",
      "message": "Global defaultStore 'alpha': Unknown store 'alpha'. No stores are registered.",
      "target": "store.id",
      "fix": "Register the store (openspec store register <path> --id alpha) or clear the stale global default (openspec config unset defaultStore)."
    }
  ]
}
```

stderr:

```text
```

## default-store-nearest

Fixture: local planning shape with store pointer and global default alpha. Command: `openspec list --specs --json`. Additional environment: `{}`. Exit: 0; monitored tree changed: False.

stdout:

```text
{
  "specs": [],
  "root": {
    "path": "<TMP>/shape",
    "source": "nearest"
  }
}
```

stderr:

```text
Warning: <TMP>/shape/openspec/config.yaml declares store 'alpha', but this directory is a real OpenSpec root; the declaration is ignored.
```

## order-C

Fixture: spec ids ['a', 'A', 'b', 'z', 'é', 'e', 'ä', 'aa', 'a-1', 'a_1', 'a1', 'Å', 'ö', 'ß', '中', '😀']. Command: `openspec list --specs --json`. Additional environment: `{'LC_ALL': 'C', 'LANG': 'C'}`. Exit: 0; monitored tree changed: False.

stdout:

```text
{
  "specs": [
    {
      "id": "😀",
      "requirementCount": 1
    },
    {
      "id": "a",
      "requirementCount": 1
    },
    {
      "id": "A",
      "requirementCount": 1
    },
    {
      "id": "Å",
      "requirementCount": 1
    },
    {
      "id": "ä",
      "requirementCount": 1
    },
    {
      "id": "a_1",
      "requirementCount": 1
    },
    {
      "id": "a-1",
      "requirementCount": 1
    },
    {
      "id": "a1",
      "requirementCount": 1
    },
    {
      "id": "aa",
      "requirementCount": 1
    },
    {
      "id": "b",
      "requirementCount": 1
    },
    {
      "id": "e",
      "requirementCount": 1
    },
    {
      "id": "é",
      "requirementCount": 1
    },
    {
      "id": "ö",
      "requirementCount": 1
    },
    {
      "id": "ß",
      "requirementCount": 1
    },
    {
      "id": "z",
      "requirementCount": 1
    },
    {
      "id": "中",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<TMP>/ordering",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## order-en_US.utf8

Fixture: spec ids ['a', 'A', 'b', 'z', 'é', 'e', 'ä', 'aa', 'a-1', 'a_1', 'a1', 'Å', 'ö', 'ß', '中', '😀']. Command: `openspec list --specs --json`. Additional environment: `{'LC_ALL': 'en_US.utf8', 'LANG': 'en_US.utf8'}`. Exit: 0; monitored tree changed: False.

stdout:

```text
{
  "specs": [
    {
      "id": "😀",
      "requirementCount": 1
    },
    {
      "id": "a",
      "requirementCount": 1
    },
    {
      "id": "A",
      "requirementCount": 1
    },
    {
      "id": "Å",
      "requirementCount": 1
    },
    {
      "id": "ä",
      "requirementCount": 1
    },
    {
      "id": "a_1",
      "requirementCount": 1
    },
    {
      "id": "a-1",
      "requirementCount": 1
    },
    {
      "id": "a1",
      "requirementCount": 1
    },
    {
      "id": "aa",
      "requirementCount": 1
    },
    {
      "id": "b",
      "requirementCount": 1
    },
    {
      "id": "e",
      "requirementCount": 1
    },
    {
      "id": "é",
      "requirementCount": 1
    },
    {
      "id": "ö",
      "requirementCount": 1
    },
    {
      "id": "ß",
      "requirementCount": 1
    },
    {
      "id": "z",
      "requirementCount": 1
    },
    {
      "id": "中",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<TMP>/ordering",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## order-pt_BR.utf8

Fixture: spec ids ['a', 'A', 'b', 'z', 'é', 'e', 'ä', 'aa', 'a-1', 'a_1', 'a1', 'Å', 'ö', 'ß', '中', '😀']. Command: `openspec list --specs --json`. Additional environment: `{'LC_ALL': 'pt_BR.utf8', 'LANG': 'pt_BR.utf8'}`. Exit: 0; monitored tree changed: False.

stdout:

```text
{
  "specs": [
    {
      "id": "😀",
      "requirementCount": 1
    },
    {
      "id": "a",
      "requirementCount": 1
    },
    {
      "id": "A",
      "requirementCount": 1
    },
    {
      "id": "Å",
      "requirementCount": 1
    },
    {
      "id": "ä",
      "requirementCount": 1
    },
    {
      "id": "a_1",
      "requirementCount": 1
    },
    {
      "id": "a-1",
      "requirementCount": 1
    },
    {
      "id": "a1",
      "requirementCount": 1
    },
    {
      "id": "aa",
      "requirementCount": 1
    },
    {
      "id": "b",
      "requirementCount": 1
    },
    {
      "id": "e",
      "requirementCount": 1
    },
    {
      "id": "é",
      "requirementCount": 1
    },
    {
      "id": "ö",
      "requirementCount": 1
    },
    {
      "id": "ß",
      "requirementCount": 1
    },
    {
      "id": "z",
      "requirementCount": 1
    },
    {
      "id": "中",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<TMP>/ordering",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## Contract implications and gaps

No-root list human: exit 1, stdout empty and stderr contains the literal Unicode cross, error and Fix lines shown above. No-root typed show instead uses implicit cwd and reports missing spec rather than `no_openspec_root`; JSON diagnostic is stdout. An empty `openspec/` without config/planning shape is not itself a qualifying root. Legacy `openspec/project.md` alone allows list to choose implicit cwd. A config-only `store: alpha` attempts declared store resolution; real planning shape wins over its store pointer and emits a warning; global default applies only after nearest root and declarations. Unsupported override detection must account for those distinctions; no CLI `--store` support is claimed for I2.

With IDs `a A b z é e ä aa a-1 a_1 a1 Å ö ß 中 😀` the result was `😀, a, A, Å, ä, a_1, a-1, a1, aa, b, e, é, ö, ß, z, 中` for all three tested `LC_ALL` C, en_US.utf8, pt_BR.utf8. Even ASCII mixed case/punctuation order differs byte lexical ordering. This is a finite observation under one Node prerelease and its ICU; it neither proves locale independence nor defines a portable collation algorithm. Case equivalence/tie ordering, accents and width vary in untested locales/runtime versions. Rejecting unsupported names or using tested ICU-equivalent behavior requires an explicit accurate boundary.

Only a missing declared store and missing global default were probed: valid registry/default selection, config.yml, symlinked root/store metadata, local inaccessible paths, Node LTS and comprehensive locale/casefold coverage remain unverified. A blanket project store pointer rejection would be a deliberate narrower subset even when upstream would ignore it; document such intentional diagnostics. No validation command was run.
