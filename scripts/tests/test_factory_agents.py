"""Validate distributed Codex role configuration before installation."""
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "setup-pentapro/assets/factory/codex-agents"


class FactoryAgentTests(unittest.TestCase):
    def test_roles_have_unique_names_and_required_schema(self):
        names = set()
        for path in TEMPLATES.glob("*.toml"):
            with self.subTest(path=path.name):
                role = tomllib.loads(path.read_text())
                for key in ("name", "description", "developer_instructions", "model", "model_reasoning_effort"):
                    self.assertIsInstance(role[key], str)
                    self.assertTrue(role[key].strip())
                self.assertNotIn(role["name"], names)
                names.add(role["name"])
                self.assertEqual(path.stem.replace("-", "_"), role["name"])
        self.assertEqual(names, {"factory_spec", "factory_implementer", "factory_verifier",
                                 "factory_reviewer", "factory_retrospective"})

    def test_roles_do_not_embed_unsupported_permission_or_provider_overrides(self):
        allowed = {"name", "description", "developer_instructions", "model", "model_reasoning_effort"}
        for path in TEMPLATES.glob("*.toml"):
            with self.subTest(path=path.name):
                role = tomllib.loads(path.read_text())
                self.assertFalse(set(role) - allowed)
                self.assertIn(role["model_reasoning_effort"], {"low", "medium", "high", "xhigh", "max", "ultra"})


if __name__ == "__main__":
    unittest.main()
