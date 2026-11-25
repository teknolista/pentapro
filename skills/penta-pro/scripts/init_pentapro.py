#!/usr/bin/env python3
"""Initialize a project-root PentaPRO specification without replacing existing work."""

import argparse
from pathlib import Path
import subprocess


# Each file owns one subject. Authors replace guidance with project facts or an explicit gap.
ARTIFACTS = {
    "product": {
        "overview.md": "Purpose, users, outcomes, scope, exclusions, supported platforms and languages.",
        "domain.md": "Domain glossary, entity relationships, invariants, business rules and examples.",
        "features.md": "Feature IDs, availability, journeys, permissions, failure behavior and acceptance scenarios.",
        "experience.md": "Screen and interaction inventory, visual assets, accessibility, localization and content rules.",
        "quality.md": "Observable security, privacy, performance, reliability, compatibility and ethical outcomes with measurable criteria.",
    },
    "project": {
        "architecture.md": "System boundaries, components, data model, interfaces, integrations and trust boundaries.",
        "decisions.md": "Accepted and proposed decisions, alternatives, assumptions, constraints, provenance and tradeoffs.",
        "security.md": "Threats, protected data, authorization design, privacy controls, compliance applicability and residual risks.",
        "delivery.md": "Dependencies, licenses, resources, technical budget, maintainability, extensibility and exit paths.",
    },
    "production": {
        "environments.md": "Build and runtime environments, configuration, secrets, installation and distribution.",
        "operations.md": "Observability, support, capacity, cost, availability, incident ownership and response.",
        "evolution.md": "Compatibility, upgrades, migrations, deprecation, rollout, rollback, recovery and retirement.",
    },
    "proof": {
        "traceability.md": "Requirement and decision IDs, checks, evidence, revisions, gaps and acceptance.",
        "verification.md": "Representative, boundary, adversarial, security, privacy, accessibility, performance and recovery checks.",
        "validation.md": "User validation, outcome measures, real-world limits, findings and post-release follow-up.",
    },
    "process": {
        "index.md": "Specification status, pillar map, canonical ownership, coverage, pending decisions and next action.",
        "change-control.md": "Baseline, proposals, accepted changes, impacted records, reconciliation and revision history.",
        "execution.md": "Tasks, responsibilities, agent authority, review gates, handoffs, escalation and resumption.",
    },
}


def initialize(root):
    root = root.resolve()
    try:
        top = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as error:
        raise ValueError(
            f"Not a Git repository root: {(error.stderr or '').strip() or 'git rev-parse failed'}"
        ) from error
    if top != str(root):
        raise ValueError("Pass the repository root, not a subdirectory")
    target = root / "pentapro"
    if target.is_symlink():
        raise ValueError("Refusing a symbolic-link specification directory")
    if (target / "assets").is_symlink():
        raise ValueError("Refusing a symbolic-link assets directory")
    changes = target / "changes"
    archive = changes / "archive"
    for directory in (changes, archive):
        if directory.is_symlink():
            raise ValueError(f"Refusing a symbolic-link changes directory: {directory.name}")
    for path in (changes / "README.md", archive / "README.md"):
        if path.is_symlink():
            raise ValueError(f"Refusing a symbolic-link changes index: {path}")
    for pillar, files in ARTIFACTS.items():
        directory = target / pillar
        if directory.is_symlink():
            raise ValueError(f"Refusing symbolic-link pillar: {pillar}")
        directory.mkdir(parents=True, exist_ok=True)
        for filename, purpose in files.items():
            path = directory / filename
            if path.exists() or path.is_symlink():
                continue
            title = filename.removesuffix(".md").replace("-", " ").title()
            path.write_text(
                f"# {pillar.upper()} · {title}\n\n"
                f"Purpose: {purpose}\n\n"
                "Status: Pending project-specific specification. Record confirmed facts, "
                "proposals, open decisions and their sources separately. Link canonical IDs "
                "and relevant assets instead of copying another record.\n",
                encoding="utf-8",
            )
    (target / "assets").mkdir(exist_ok=True)
    asset_index = target / "assets/README.md"
    if asset_index.is_symlink():
        raise ValueError("Refusing symbolic-link asset index")
    if not asset_index.exists():
        asset_index.write_text(
            "# Specification assets\n\n"
            "Store supporting images, icons, fonts, styles, diagrams, media and other "
            "resources here. Link each resource from its owning pillar record and "
            "record its source, usage rights, format and revision. Never store secrets.\n",
            encoding="utf-8",
        )
    archive.mkdir(parents=True, exist_ok=True)
    changes_index = changes / "README.md"
    if not changes_index.exists():
        changes_index.write_text(
            "# Active changes\n\n"
            "Keep each active change in a uniquely named directory of two or three "
            "lowercase words separated by hyphens. Preserve existing changes and "
            "their records. Completed or cancelled changes belong in [archive](archive/).\n",
            encoding="utf-8",
        )
    archive_index = archive / "README.md"
    if not archive_index.exists():
        archive_index.write_text(
            "# Archived changes\n\n"
            "Store completed or cancelled changes in directories named "
            "`YYYY-MM-DD_<name>`, using the archive date. Preserve existing archives; "
            "do not overwrite an existing destination.\n",
            encoding="utf-8",
        )
    index = target / "README.md"
    if index.is_symlink():
        raise ValueError("Refusing symbolic-link specification index")
    if not index.exists():
        index.write_text(
            "# PentaPRO specification\n\n"
            "Read [PROCESS](process/index.md) for current scope and next action. "
            "The five pillars own the maintained software specification. "
            "Use [PRODUCT](product/overview.md), [PROJECT](project/architecture.md), "
            "[PRODUCTION](production/environments.md), [PROOF](proof/traceability.md), "
            "and [PROCESS](process/index.md). Put supporting images, icons, styles and "
            "other binary resources in [assets](assets/), with source, rights and revision "
            "recorded in the owning pillar. Keep active change records in [changes](changes/) "
            "and preserve completed or cancelled changes in [archive](changes/archive/). "
            "Reconcile affected canonical records and evidence for the tested revision.\n",
            encoding="utf-8",
        )
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository_root", type=Path)
    args = parser.parse_args()
    try:
        print(initialize(args.repository_root))
    except ValueError as error:
        parser.exit(1, f"error: {error}\n")
