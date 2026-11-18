# Domain Docs

How the collection skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`pentapro/product/domain.md`** — the PRODUCT glossary. If it exists and is non-trivial, its terms are the project's vocabulary; use them as written, including their boundaries and examples.
- **`pentapro/product/domain-<context>.md`** — per-context term files in multi-context (monorepo) layouts. Read the ones relevant to the area you're about to touch.
- **`pentapro/project/decisions.md`** — accepted and proposed decisions with provenance. Read the records that touch the area you're about to work in.

If none of these files exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The first `$penta-pro` pass creates the skeleton and fills the glossary lazily, when terms are actually resolved.

## File structure

Single-context repo (most repos):

```
/
└── pentapro/
    ├── product/
    │   └── domain.md          ← glossary: terms, boundaries, examples, IDs
    └── project/
        └── decisions.md       ← decisions: alternatives, trade-offs, provenance
```

Multi-context repo (a monorepo with a bounded multi-package layout): one PentaPRO specification still covers the repository.

```
/
└── pentapro/
    ├── product/
    │   ├── domain.md          ← context map: points at the per-context files below
    │   ├── domain-ordering.md ← per-context terms when they differ by context
    │   └── domain-billing.md
    └── project/
        └── decisions.md       ← context-scoped decisions (IDs carry the context)
```

Keep the context map in `domain.md` rather than duplicating terms. A term drawn from several contexts is defined once in the map or scoped per file with the same name.

Do **not** create a root `GLOSSARY.md`, `GLOSSARY-MAP.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, or a parallel `docs/adr/` tree for this purpose. The specification owns the vocabulary; the root instruction file only points at it.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `pentapro/product/domain.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (record it as a proposed term for `$penta-pro`, or ask the developer).

## Flag decision conflicts

If your output contradicts an accepted decision in `pentapro/project/decisions.md`, surface it explicitly rather than silently overriding:

> _Contradicts decision DEC-0007 (event-sourced orders), but worth reopening because…_
