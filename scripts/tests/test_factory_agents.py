"""Validate distributed Codex role configuration before installation."""
from pathlib import Path
import tomllib
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "setup-pentapro/assets/agents"


class FactoryAgentTests(unittest.TestCase):
    def test_roles_have_unique_names_and_required_schema(self):
        names = set()
        for path in TEMPLATES.glob("*/codex.toml"):
            with self.subTest(path=path.name):
                role = tomllib.loads(path.read_text())
                for key in ("name", "description", "developer_instructions", "model", "model_reasoning_effort"):
                    self.assertIsInstance(role[key], str)
                    self.assertTrue(role[key].strip())
                self.assertNotIn(role["name"], names)
                names.add(role["name"])
                self.assertEqual(path.parent.name.replace("-", "_"), role["name"])
        self.assertEqual(names, {"factory_spec", "factory_implementer", "factory_verifier",
                                 "factory_reviewer", "factory_retrospective", "factory_shipper"})

    def test_all_host_adapters_cover_each_role_and_shipper_guard(self):
        roles = {"factory-spec", "factory-implementer", "factory-verifier", "factory-reviewer", "factory-retrospective", "factory-shipper"}
        hosts = {"codex.toml", "claude-code.md", "github-copilot.md", "opencode.md", "antigravity.md", "cursor.md"}
        self.assertEqual({p.name for p in TEMPLATES.iterdir() if p.is_dir()}, roles)
        for role in roles:
            self.assertEqual({p.name for p in (TEMPLATES / role).iterdir()}, hosts)
        for path in (TEMPLATES / "factory-shipper").iterdir():
            text = path.read_text()
            for required in ("git-ship", "direct request to invoke factory_shipper", "commit", "normal push"):
                self.assertIn(required, text, str(path))
        role = tomllib.loads((TEMPLATES / "factory-shipper/codex.toml").read_text())
        self.assertEqual((role["model"], role["model_reasoning_effort"]), ("gpt-6-luna", "high"))

    def test_native_workflow_does_not_depend_on_external_sdd_tool(self):
        entrypoint = (ROOT / "setup-pentapro/SKILL.md").read_text()
        guidance = (ROOT / "setup-pentapro/references/factory-setup.md").read_text()
        project_instructions = (ROOT / "setup-pentapro/assets/agents.md").read_text()
        for text in (entrypoint, guidance, project_instructions):
            self.assertNotIn("openspec", text.lower())
        self.assertIn("pentapro/changes/archive/", guidance)
        self.assertIn("one explicit developer approval", guidance)
        for path in TEMPLATES.glob("*/*"):
            with self.subTest(path=str(path)):
                text = path.read_text()
                self.assertNotIn("openspec", text.lower())
                if path.parent.name == "factory-shipper":
                    self.assertIn("one explicit developer approval", text)
                    self.assertIn("narrower scope", text)

    def test_pdsa_contract_is_available_in_every_host_role(self):
        for path in TEMPLATES.glob("*/*"):
            with self.subTest(role=path.parent.name, host=path.name):
                if path.suffix == ".toml":
                    body = tomllib.loads(path.read_text())["developer_instructions"]
                else:
                    _, header, body = path.read_text().split("---", 2)
                    metadata = yaml.safe_load(header)
                    self.assertIsInstance(metadata["description"], str)
                for clause in ("Plan-Do-Study-Act", "even when invoked alone", "two attempts",
                               "Never write the shared lessons record", "persistence pending"):
                    self.assertIn(clause, body)
                if path.parent.name in {"factory-spec", "factory-reviewer", "factory-verifier", "factory-retrospective"}:
                    self.assertIn("Read-only roles report required fixes", body)

    def test_setup_bundles_protocol_and_empty_record_separately(self):
        assets = ROOT / "setup-pentapro/assets"
        protocol = (assets / "continuous-improvement.md").read_text()
        for clause in ("orchestrator alone", "after commit or push", "Never amend", "cause confidence"):
            self.assertIn(clause, protocol)
        ledger = (assets / "lessons-learned.md").read_text()
        self.assertIn("No lessons recorded yet", ledger)
        self.assertNotIn("LL-001", ledger)

    def test_host_metadata_and_instructions_match_the_canonical_role(self):
        class UniqueLoader(yaml.SafeLoader):
            def construct_mapping(self, node, deep=False):
                result = super().construct_mapping(node, deep=deep)
                if len(result) != len(node.value):
                    raise yaml.YAMLError("duplicate host metadata field")
                return result

        for directory in TEMPLATES.iterdir():
            if not directory.is_dir():
                continue
            canonical = tomllib.loads((directory / "codex.toml").read_text())
            for path in directory.glob("*.md"):
                with self.subTest(role=directory.name, host=path.name):
                    _, header, body = path.read_text().split("---", 2)
                    metadata = yaml.load(header, Loader=UniqueLoader)
                    self.assertEqual(metadata["description"], canonical["description"])
                    self.assertEqual(body.strip(), canonical["developer_instructions"].strip())
                    expected = {"description", "mode"} if path.name == "opencode.md" else {"name", "description"}
                    if path.name == "antigravity.md":
                        expected.add("subagent")
                        self.assertIs(metadata["subagent"], True)
                    self.assertEqual(set(metadata), expected)
                    if path.name == "opencode.md":
                        self.assertEqual(metadata["mode"], "subagent")
                    else:
                        self.assertEqual(metadata["name"], directory.name if path.name == "cursor.md" else canonical["name"])

    def test_roles_do_not_embed_unsupported_permission_or_provider_overrides(self):
        allowed = {"name", "description", "developer_instructions", "model", "model_reasoning_effort"}
        for path in TEMPLATES.glob("*/codex.toml"):
            with self.subTest(path=path.name):
                role = tomllib.loads(path.read_text())
                self.assertFalse(set(role) - allowed)
                self.assertIn(role["model_reasoning_effort"], {"low", "medium", "high", "xhigh", "max", "ultra"})


if __name__ == "__main__":
    unittest.main()
