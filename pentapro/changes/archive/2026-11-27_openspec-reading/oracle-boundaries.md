# OpenSpec I2 executable boundary observations

Pinned OpenSpec v2.2.0 SHA `f1cd852f4edce22b8df9548a4df889172ca8ff25`, Linux, Node `v27.0.0-alpha.0.0.0` (not release/CI Node). See [captured results](oracle-boundary-results.json) for commands and exact outcomes. The one-off reproduction script ran in temporary storage; a portable replay harness is pending. `<TMP>` substitutes only the randomized temp root. Telemetry/update controls disabled, restricted sandbox. File bytes and symlink target snapshots of temporary root compared before/after each command; no differences observed for shown calls. This does not detect transient identical writes, directory-only modifications, or effects outside monitored root. Do not generalize beyond these cases.

## empty-list-json

Fixture: valid schema config; empty specs and changes. Command: `openspec list --specs --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "specs": [],
  "root": {
    "path": "<TMP>/empty",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## empty-list-text

Fixture: same empty project. Command: `openspec list --specs`. Exit: 0; checked filesystem changes: False.

stdout:

```text
No specs found.
```

stderr:

```text
```

## empty-missing

Fixture: same empty project. Command: `openspec show missing --type spec --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Spec 'missing' not found at <TMP>/empty/openspec/specs/missing/spec.md"
    }
  ]
}
```

stderr:

```text
```

## no-project

Fixture: empty cwd, no openspec directory or config. Command: `openspec list --specs --json`. Exit: 1; checked filesystem changes: False.

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

## markdown-list

Fixture: alpha spec.md bytes EF BB BF + BOM Markdown, CRLF, fenced fake requirement then real requirement; see script. Command: `openspec list --specs --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "specs": [
    {
      "id": "alpha",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<TMP>/markdown",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## markdown-show-json

Fixture: same BOM/CRLF/fenced alpha. Command: `openspec show alpha --type spec --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "id": "alpha",
  "title": "alpha",
  "overview": "BOM and CRLF description.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Real",
      "text": "The system SHALL work.",
      "scenarios": [
        {
          "name": "Test",
          "rawText": "- **WHEN** called\n- **THEN** works"
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<TMP>/markdown",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## markdown-show-text

Fixture: same BOM/CRLF/fenced alpha. Command: `openspec show alpha --type spec`. Exit: 0; checked filesystem changes: False.

stdout:

```text
﻿# Spec

## Purpose

BOM and CRLF description.

## Requirements

```markdown
### Requirement: Fake
```

### Requirement: Real

The system SHALL work.

#### Scenario: Test

- **WHEN** called
- **THEN** works

```

stderr:

```text
```

## invalid-utf8-list

Fixture: alpha contains invalid raw byte FF in purpose. Command: `openspec list --specs --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "specs": [
    {
      "id": "alpha",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<TMP>/badutf8",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## invalid-utf8-show

Fixture: same invalid byte. Command: `openspec show alpha --type spec --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "id": "alpha",
  "title": "alpha",
  "overview": "Invalid � bytes.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "A",
      "text": "The system SHALL work.",
      "scenarios": []
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<TMP>/badutf8",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## bad-config-list

Fixture: config.yaml is schema: [broken; alpha spec only # Alpha. Command: `openspec list --specs --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "specs": [
    {
      "id": "alpha",
      "requirementCount": 0
    }
  ],
  "root": {
    "path": "<TMP>/malformed",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## bad-config-show

Fixture: same malformed config. Command: `openspec show alpha --type spec --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Spec must have a Purpose section"
    }
  ]
}
```

stderr:

```text
```

## symlink-list

Fixture: inside/spec.md -> ../real/spec.md; outside/spec.md -> external file; broken/spec.md -> missing.md; directory-link -> real. Command: `openspec list --specs --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "specs": [],
  "root": null,
  "status": [
    {
      "severity": "error",
      "code": "list_error",
      "message": "Path is outside the allowed directory: <TMP>/links/openspec/specs/outside/spec.md"
    }
  ]
}
```

stderr:

```text
```

## symlink-inside

Fixture: same link fixture. Command: `openspec show inside --type spec --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Path is outside the allowed directory: <TMP>/links/openspec/specs/outside/spec.md"
    }
  ]
}
```

stderr:

```text
```

## symlink-outside

Fixture: same link fixture. Command: `openspec show outside --type spec --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Path is outside the allowed directory: <TMP>/links/openspec/specs/outside/spec.md"
    }
  ]
}
```

stderr:

```text
```

## symlink-broken

Fixture: same link fixture. Command: `openspec show broken --type spec --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Path is outside the allowed directory: <TMP>/links/openspec/specs/outside/spec.md"
    }
  ]
}
```

stderr:

```text
```

## symlink-dir

Fixture: same link fixture. Command: `openspec show directory-link --type spec --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Path is outside the allowed directory: <TMP>/links/openspec/specs/outside/spec.md"
    }
  ]
}
```

stderr:

```text
```

## without-outside-list

Fixture: external link removed; internal, dangling and directory links remain. Command: `openspec list --specs --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "specs": [
    {
      "id": "inside",
      "requirementCount": 1
    },
    {
      "id": "real",
      "requirementCount": 1
    }
  ],
  "root": {
    "path": "<TMP>/links",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## without-outside-inside

Fixture: external link removed. Command: `openspec show inside --type spec --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "id": "inside",
  "title": "inside",
  "overview": "Example",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Exists",
      "text": "Requirement: Exists",
      "scenarios": []
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<TMP>/links",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## without-outside-broken

Fixture: external link removed. Command: `openspec show broken --type spec --json`. Exit: 1; checked filesystem changes: False.

stdout:

```text
{
  "status": [
    {
      "severity": "error",
      "code": "show_error",
      "message": "Cannot verify dangling symbolic link: <TMP>/links/openspec/specs/broken/spec.md"
    }
  ]
}
```

stderr:

```text
```

## without-outside-dir

Fixture: external link removed. Command: `openspec show directory-link --type spec --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "id": "directory-link",
  "title": "directory-link",
  "overview": "Example",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Exists",
      "text": "Requirement: Exists",
      "scenarios": []
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<TMP>/links",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## bad-config-valid-show

Fixture: malformed config, valid spec with purpose and requirement. Command: `openspec show valid --type spec --json`. Exit: 0; checked filesystem changes: False.

stdout:

```text
{
  "id": "valid",
  "title": "valid",
  "overview": "A valid purpose.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "A",
      "text": "The system SHALL work.",
      "scenarios": []
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "<TMP>/malformed",
    "source": "nearest"
  }
}
```

stderr:

```text
```

## Evidence notes

The combined BOM+CRLF+fenced-heading fixture validates only that combination, not each independently. The external symlink control caused whole discovery to fail, including unrelated `show`, until removed; isolated inside/dangling/directory-link outputs are included afterward. JS decoding replaced malformed UTF-8 with U+FFFD in tested JSON. The malformed YAML list and valid-show cases demonstrate only those commands; validation may read configuration differently. Raw text output preserves CRLF/BOM in stdout as captured, plus CLI-added newline. The report uses UTF-8 text rendering; JSON data retains escapes and full command outputs in the machine results. Remaining gaps include permissions, locale sorting, unusual Markdown combinations, Windows/macOS and supported release Node; no validate behavior was tested.
