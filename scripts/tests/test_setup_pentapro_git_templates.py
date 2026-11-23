"""Exercise the standalone Git-template merger against disposable repositories."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "setup-pentapro"
spec = importlib.util.spec_from_file_location(
    "merge_git_templates", PACKAGE / "scripts/merge_git_templates.py"
)
merger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(merger)


class GitTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "project"
        self.repo.mkdir()
        self.git("init", "-q")

    def git(self, *args):
        return subprocess.check_output(
            ["git", "-C", str(self.repo), *args], text=True
        )

    def test_new_files_match_templates_and_rerun_is_byte_identical(self):
        self.assertEqual(merger.merge_templates(self.repo), [
            "created .gitignore", "created .gitattributes"
        ])
        for name in ("gitignore", "gitattributes"):
            self.assertEqual((self.repo / ("." + name)).read_bytes(),
                             (PACKAGE / "assets" / name).read_bytes())
            self.assertFalse((self.repo / name).exists())
        before = {p.name: p.read_bytes() for p in self.repo.iterdir() if p.is_file()}
        self.assertEqual(merger.merge_templates(self.repo), [
            "unchanged .gitignore", "unchanged .gitattributes"
        ])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.repo.iterdir() if p.is_file()})

    def test_existing_overrides_and_duplicate_rules_keep_effective_behavior(self):
        ignore = b"# Custom\n.env\n!.env.keep\n*.log\n!important.log\n*.tmp\n*.tmp\n!keep.tmp\n"
        attrs = b"# Custom\n* text=auto\n*.md -text\n*.png filter=lfs diff=lfs merge=lfs -text\n"
        (self.repo / ".gitignore").write_bytes(ignore)
        (self.repo / ".gitattributes").write_bytes(attrs)
        merger.merge_templates(self.repo)
        merged = (self.repo / ".gitignore").read_bytes()
        self.assertTrue(merged.endswith(ignore))
        self.assertEqual(merged.splitlines().count(b".env"), 1)
        self.assertEqual(merged.splitlines().count(b"*.tmp"), 2)
        self.assertTrue((self.repo / ".gitattributes").read_bytes().endswith(attrs))
        ignored = self.git("check-ignore", "--no-index", "--", ".env.private", "AGENTS.log", "AGENTS.log.1")
        self.assertEqual(set(ignored.splitlines()), {".env.private", "AGENTS.log", "AGENTS.log.1"})
        for name in (".env.keep", "important.log", "keep.tmp"):
            result = subprocess.run(["git", "-C", str(self.repo), "check-ignore", "--no-index", "--", name], capture_output=True)
            self.assertEqual(result.returncode, 1, name)
        self.assertIn("README.md: text: unset", self.git("check-attr", "text", "--", "README.md"))
        self.assertIn("image.png: filter: lfs", self.git("check-attr", "filter", "--", "image.png"))
        self.assertIn("run.sh: eol: lf", self.git("check-attr", "eol", "--", "run.sh"))
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        self.assertEqual(merger.merge_templates(self.repo), [
            "unchanged .gitignore", "unchanged .gitattributes"
        ])

    def test_one_existing_file_with_bom_crlf_and_no_final_newline(self):
        original = b"\xef\xbb\xbf# Existing\r\n*.tmp\r\n!keep.tmp"
        (self.repo / ".gitignore").write_bytes(original)
        merger.merge_templates(self.repo)
        after = (self.repo / ".gitignore").read_bytes()
        self.assertTrue(after.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(after.endswith(original[3:]))
        self.assertNotIn(b"\n", after.replace(b"\r\n", b""))
        self.assertEqual(merger.merge_templates(self.repo)[0], "unchanged .gitignore")

    def test_unsafe_second_target_is_rejected_before_first_write(self):
        outside = self.repo.parent / "outside"
        outside.write_text("keep me")
        (self.repo / ".gitattributes").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Refusing"):
            merger.merge_templates(self.repo)
        self.assertFalse((self.repo / ".gitignore").exists())
        self.assertEqual(outside.read_text(), "keep me")

    def test_hard_link_and_invalid_encoding_are_rejected(self):
        outside = self.repo.parent / "outside"
        outside.write_bytes(b"\xff")
        target = self.repo / ".gitignore"
        target.hardlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Refusing"):
            merger.merge_templates(self.repo)
        target.unlink()
        target.write_bytes(b"\xff")
        with self.assertRaises(UnicodeError):
            merger.merge_templates(self.repo)
        self.assertEqual(target.read_bytes(), b"\xff")
        self.assertFalse((self.repo / ".gitattributes").exists())

    def test_non_root_destination_is_rejected(self):
        child = self.repo / "nested"
        child.mkdir()
        with self.assertRaisesRegex(ValueError, "repository root"):
            merger.merge_templates(child)
        self.assertEqual(list(child.iterdir()), [])

    def test_failed_replacement_preserves_original_rules_and_cleans_staging(self):
        target = self.repo / ".gitignore"
        target.write_bytes(b"# Custom\n!keep.tmp")
        target.chmod(0o640)
        before = target.read_bytes()
        with patch.object(Path, "replace", side_effect=OSError("simulated failure")):
            with self.assertRaisesRegex(OSError, "simulated failure"):
                merger.merge_templates(self.repo)
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual({p.name for p in self.repo.iterdir()}, {".git", ".gitignore"})
        merger.merge_templates(self.repo)
        self.assertEqual(target.stat().st_mode & 0o777, 0o640)

    def test_cli_runs_from_a_standalone_package_without_checkout_dependencies(self):
        installed = self.repo.parent / "installed" / "setup-pentapro"
        shutil.copytree(PACKAGE, installed)
        result = subprocess.run([
            "python3", "-B", str(installed / "scripts/merge_git_templates.py"), str(self.repo)
        ], cwd=self.repo.parent, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("created .gitattributes", result.stdout)


if __name__ == "__main__":
    unittest.main()
