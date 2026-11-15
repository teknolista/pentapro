"""Exercise PentaPRO project initialization against an actual temporary Git root."""

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[2] / "penta-pro/scripts/init_pentapro.py"
spec = importlib.util.spec_from_file_location("pentapro_init", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InitializationTests(unittest.TestCase):
    def test_creates_five_pillars_and_preserves_existing_content(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            existing = root / "pentapro/product/overview.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("Accepted product contract\n")
            module.initialize(root)
            self.assertEqual(existing.read_text(), "Accepted product contract\n")
            self.assertEqual({p.name for p in (root / "pentapro").iterdir() if p.is_dir()},
                             {*module.ARTIFACTS, "assets"})
            self.assertTrue((root / "pentapro/process/change-control.md").is_file())
            before = {str(p.relative_to(root)): p.read_bytes()
                      for p in (root / "pentapro").rglob("*.md")}
            module.initialize(root)
            self.assertEqual(before, {str(p.relative_to(root)): p.read_bytes()
                                      for p in (root / "pentapro").rglob("*.md")})

    def test_rejects_subdirectory_and_symlinked_specification(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            child = root / "child"
            child.mkdir()
            with self.assertRaisesRegex(ValueError, "repository root"):
                module.initialize(child)
            (root / "pentapro").symlink_to(child, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symbolic-link"):
                module.initialize(root)

    def test_rejects_symlinked_assets_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            target = root / "pentapro"
            target.mkdir()
            (target / "assets").symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symbolic-link assets"):
                module.initialize(root)
            self.assertEqual({p.name for p in target.iterdir()}, {"assets"})
