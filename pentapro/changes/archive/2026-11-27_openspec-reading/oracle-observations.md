# OpenSpec executable oracle observations — I2

Pinned OpenSpec v2.2.0 commit `f1cd852f4edce22b8df9548a4df889172ca8ff25`; local `node v27.0.0-alpha.0.0.0` (prerelease, not CI Node 24). Built in isolated clone using lockfile-resolved dependencies. This is a small Linux source/CLI probe, not full parity, validation coverage, tested Windows behavior, or assurance about all networks/inputs. Commands ran in the restricted sandbox with throwaway HOME/XDG directories, `OPENSPEC_TELEMETRY=0`, `DO_NOT_TRACK=1`, `OPENSPEC_NO_UPDATE_CHECK=1`, `NO_COLOR=1`, `CI=1`, `TERM=dumb`. No network requests were intentionally made. Project and HOME file-content hashes were compared before and after each call; no differences observed. The file-only comparison does not detect transient writes that leave identical bytes, directory-only changes, or writes outside those two trees.

The captured normalized [machine results](oracle-results.json) include fixture Markdown and command arguments. The original one-off probe was executed in temporary storage; an automated portable replay harness remains pending. Fixture: `openspec/config.yaml` = `schema: spec-driven`, `openspec/specs/alpha/spec.md`, `openspec/specs/platform/session/spec.md`, hidden and top-level spec.md controls, `openspec/changes`, and nested working directory. The complete fixture Markdown and command list are in the script/results. `<PROJECT>` below replaces only the absolute temporary fixture path. Fixture is synthetic.

Observed source locators: `src/cli/index.ts:470–510` for list, `src/core/list.ts`, `src/commands/show.ts`, `src/commands/spec.ts`, `src/core/root-selection.ts`, `src/utils/spec-discovery.ts`, `src/core/parsers/markdown-parser.ts`. Source links are pinned by commit in upstream repository; consult source for exhaustive behavior.

## Exact observed outputs

### `openspec list --specs` (project)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
Specs:
  alpha                requirements 1
  platform/session     requirements 1
```

stderr:

```text
```

### `openspec list --specs --json` (project)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "specs": [
    {
      "id": "alpha",
      "requirementCount": 1
    },
    {
      "id": "platform/session",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<PROJECT>",
    "source": "nearest"
  }
}
```

stderr:

```text
```

### `openspec list --specs --json` (nested)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "specs": [
    {
      "id": "alpha",
      "requirementCount": 1
    },
    {
      "id": "platform/session",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<PROJECT>",
    "source": "nearest"
  }
}
```

stderr:

```text
```

### `openspec show alpha --type spec` (project)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
# Alpha

## Purpose

Explain the alpha capability for testing.

## Requirements

### Requirement: Login

The system SHALL support login.

#### Scenario: Success

- **GIVEN** an account
- **WHEN** login is requested
- **THEN** login succeeds

```

stderr:

```text
```

### `openspec show alpha --type spec --json` (project)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "id": "alpha",
  "title": "alpha",
  "overview": "Explain the alpha capability for testing.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Login",
      "text": "The system SHALL support login.",
      "scenarios": [
        {
          "name": "Success",
          "rawText": "- **GIVEN** an account\n- **WHEN** login is requested\n- **THEN** login succeeds"
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<PROJECT>",
    "source": "nearest"
  }
}
```

stderr:

```text
```

### `openspec show platform/session --type spec --json` (project)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "id": "platform/session",
  "title": "platform/session",
  "overview": "Nested session specification for testing.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Session",
      "text": "The system SHALL support sessions.",
      "scenarios": [
        {
          "name": "Start",
          "rawText": "- **WHEN** a session starts\n- **THEN** it is active"
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<PROJECT>",
    "source": "nearest"
  }
}
```

stderr:

```text
```

### `openspec show missing --type spec --json` (project)

Exit: 1; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Spec 'missing' not found at <PROJECT>/openspec/specs/missing/spec.md"
    }
  ]
}
```

stderr:

```text
```

### `openspec show missing --json --no-interactive` (project)

Exit: 1; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "unknown_item",
      "message": "Unknown item 'missing'. Did you mean: alpha, platform/session?"
    }
  ]
}
```

stderr:

```text
```

### `openspec list --specs --all --json` (project)

Exit: 1; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "specs": [],
  "root": null,
  "status": [
    {
      "severity": "error",
      "code": "list_error",
      "message": "--archived and --all can only be used when listing changes."
    }
  ]
}
```

stderr:

```text
```

### `openspec show alpha --type spec --json --requirements` (project)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "id": "alpha",
  "title": "alpha",
  "overview": "Explain the alpha capability for testing.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Login",
      "text": "The system SHALL support login.",
      "scenarios": []
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<PROJECT>",
    "source": "nearest"
  }
}
```

stderr:

```text
```

### `openspec show alpha --type spec --json --requirement 1` (project)

Exit: 0; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "id": "alpha",
  "title": "alpha",
  "overview": "Explain the alpha capability for testing.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Login",
      "text": "The system SHALL support login.",
      "scenarios": [
        {
          "name": "Success",
          "rawText": "- **GIVEN** an account\n- **WHEN** login is requested\n- **THEN** login succeeds"
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<PROJECT>",
    "source": "nearest"
  }
}
```

stderr:

```text
```

### `openspec show ../alpha --type spec --json` (project)

Exit: 1; filesystem content changes in fixture/home: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Path is outside the allowed directory: <PROJECT>/openspec/alpha/spec.md"
    }
  ]
}
```

stderr:

```text
```

## Interpretation and limits

The measured list excludes the hidden-directory and root-level spec.md controls and finds the nested ID. Nested cwd resolved `root.source=nearest`. Human show adds a newline to the file content, resulting in two trailing newlines for the fixture. JSON show uses the spec ID as title; scenario text excludes Markdown heading. Errors for missing typed spec, unknown autodetected item, traversal and incompatible list flags were JSON on stdout with exit 1; stdout JSON is not the native Engine error envelope. These observations support only the shown cases. No validation command was run: Engine compatibility validation must remain explicitly unsupported until its actual rules are ported and independently checked. Investigate malformed headings, CRLF/BOM, symlinks, empty roots, permissions, config errors, TTY, locale ordering, root-selection variants and pinned supported Node before defining complete acceptance. No conclusions about OpenSpec write behavior or other flags are implied.
