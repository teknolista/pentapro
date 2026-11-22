"""Exercise PentaPRO project initialization against an actual temporary Git root."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "init_pentapro.py"
SPEC = importlib.util.spec_from_file_location("init_pentapro", SCRIPT)
INIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INIT)


class InitializationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
        )

    def test_creates_every_pillar_file_asset_index_and_root_readme(self):
        target = INIT.initialize(self.root)

        self.assertEqual(self.root.resolve() / "pentapro", target)
        for pillar, files in INIT.ARTIFACTS.items():
            for filename in files:
                path = target / pillar / filename
                self.assertTrue(path.is_file(), path)
                text = path.read_text(encoding="utf-8")
                self.assertIn(f"# {pillar.upper()} · ", text)
                self.assertIn("Purpose: ", text)
                self.assertIn("Status: Pending project-specific specification.", text)

        self.assertTrue((target / "assets/README.md").is_file())
        readme = (target / "README.md").read_text(encoding="utf-8")
        for link in (
            "[PRODUCT](product/overview.md)",
            "[PROJECT](project/architecture.md)",
            "[PRODUCTION](production/environments.md)",
            "[PROOF](proof/traceability.md)",
            "[PROCESS](process/index.md)",
            "[assets](assets/)",
        ):
            self.assertIn(link, readme)

    def test_second_run_preserves_existing_files_and_recreates_deleted_ones(self):
        target = INIT.initialize(self.root)
        custom = target / "product/domain.md"
        custom.write_text("Accepted glossary\n", encoding="utf-8")
        custom_asset = target / "assets/README.md"
        custom_asset.write_text("Owned assets\n", encoding="utf-8")
        custom_index = target / "README.md"
        custom_index.write_text("Owned index\n", encoding="utf-8")
        deleted = target / "project/delivery.md"
        deleted.unlink()

        INIT.initialize(self.root)

        self.assertEqual("Accepted glossary\n", custom.read_text(encoding="utf-8"))
        self.assertEqual("Owned assets\n", custom_asset.read_text(encoding="utf-8"))
        self.assertEqual("Owned index\n", custom_index.read_text(encoding="utf-8"))
        self.assertTrue(deleted.is_file(), deleted)

    def test_creates_change_structure_with_guidance_and_no_active_change(self):
        target = INIT.initialize(self.root)
        changes = target / "changes"
        archive = changes / "archive"
        self.assertEqual({"README.md", "archive"}, {path.name for path in changes.iterdir()})
        self.assertEqual({"README.md"}, {path.name for path in archive.iterdir()})
        self.assertIn("two or three", (changes / "README.md").read_text())
        self.assertIn("YYYY-MM-DD_<name>", (archive / "README.md").read_text())
        self.assertNotIn("OpenSpec", (target / "README.md").read_text())
        self.assertIn("[changes](changes/)", (target / "README.md").read_text())

    def test_rerun_preserves_changes_archive_and_their_indexes(self):
        target = INIT.initialize(self.root)
        changes = target / "changes"
        active = changes / "add-login" / "change.md"
        active.parent.mkdir()
        active.write_text("In progress\n")
        archived = changes / "archive" / "2026-11-22_add-search" / "change.md"
        archived.parent.mkdir()
        archived.write_text("Archived\n")
        for index in (changes / "README.md", changes / "archive/README.md"):
            index.write_text("Custom guidance\n")

        INIT.initialize(self.root)

        self.assertEqual("In progress\n", active.read_text())
        self.assertEqual("Archived\n", archived.read_text())
        for index in (changes / "README.md", changes / "archive/README.md"):
            self.assertEqual("Custom guidance\n", index.read_text())

    def test_rejects_symlinked_changes_and_archive_before_writing(self):
        for linked in ("changes", "archive"):
            with self.subTest(linked=linked), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                subprocess.run(["git", "init", "-q", str(root)], check=True)
                target = root / "pentapro"
                target.mkdir()
                external = root / "external"
                external.mkdir()
                sentinel = external / "sentinel"
                sentinel.write_text("Untouched\n")
                if linked == "changes":
                    (target / "changes").symlink_to(external, target_is_directory=True)
                    expected = {"changes"}
                else:
                    changes = target / "changes"
                    changes.mkdir()
                    (changes / "archive").symlink_to(external, target_is_directory=True)
                    expected = {"changes"}
                with self.assertRaisesRegex(ValueError, "symbolic-link"):
                    INIT.initialize(root)
                self.assertEqual(expected, {path.name for path in target.iterdir()})
                self.assertEqual({"sentinel"}, {path.name for path in external.iterdir()})
                self.assertEqual("Untouched\n", sentinel.read_text())

    def test_requires_the_repository_root(self):
        child = self.root / "child"
        child.mkdir()

        with self.assertRaisesRegex(ValueError, "repository root"):
            INIT.initialize(child)

    def test_rejects_directory_outside_git(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "Not a Git repository root"):
                INIT.initialize(Path(folder))

    def test_cli_reports_failures_without_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            outside = Path(folder)
            result = self.run_cli(outside)

            self.assertEqual(1, result.returncode)
            self.assertEqual("", result.stdout)
            self.assertIn("error: Not a Git repository root", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual([], list(outside.iterdir()))

    def test_rejects_symlinked_specification_directory(self):
        child = self.root / "child"
        child.mkdir()
        (self.root / "pentapro").symlink_to(child, target_is_directory=True)

        with self.assertRaisesRegex(ValueError, "symbolic-link specification directory"):
            INIT.initialize(self.root)

    def test_rejects_symlinked_pillar(self):
        target = self.root / "pentapro"
        target.mkdir()
        child = self.root / "child"
        child.mkdir()
        (target / "product").symlink_to(child, target_is_directory=True)

        with self.assertRaisesRegex(ValueError, "symbolic-link pillar: product"):
            INIT.initialize(self.root)

    def test_rejects_symlinked_assets_before_writing(self):
        target = self.root / "pentapro"
        target.mkdir()
        (target / "assets").symlink_to(self.root, target_is_directory=True)

        with self.assertRaisesRegex(ValueError, "symbolic-link assets"):
            INIT.initialize(self.root)

        self.assertEqual({"assets"}, {path.name for path in target.iterdir()})

    def test_rejects_symlinked_asset_index(self):
        target = self.root / "pentapro"
        assets = target / "assets"
        assets.mkdir(parents=True)
        outside = self.root / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        (assets / "README.md").symlink_to(outside)

        with self.assertRaisesRegex(ValueError, "symbolic-link asset index"):
            INIT.initialize(self.root)

    def test_rejects_symlinked_root_index(self):
        target = self.root / "pentapro"
        target.mkdir()
        outside = self.root / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        (target / "README.md").symlink_to(outside)

        with self.assertRaisesRegex(ValueError, "symbolic-link specification index"):
            INIT.initialize(self.root)

    def test_cli_prints_the_created_target(self):
        result = self.run_cli(self.root)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(str(self.root.resolve() / "pentapro"), result.stdout.strip())
        self.assertTrue((self.root / "pentapro/process/index.md").is_file())


if __name__ == "__main__":
    unittest.main()
