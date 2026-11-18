"""Keep Setup PentaPRO's prompt rule complete and in sync with its template."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "setup-pentapro" / "SKILL.md"
TEMPLATE = ROOT / "setup-pentapro" / "assets" / "agents.md"


def prompt_rule(text, *, skill=False):
    if skill:
        opening = "~~~markdown\n"
        start = text.index(opening + "## Prompt Logging\n") + len(opening)
        end = text.index("\n~~~", start)
    else:
        start = text.index("## Prompt Logging\n")
        end = text.index("\n## Project Facts and Navigation", start)
    return text[start:end].rstrip()


class SetupPentaProPromptRuleTests(unittest.TestCase):
    def test_skill_and_generated_template_contain_the_same_complete_rule(self):
        skill_text = SKILL.read_text(encoding="utf-8")
        template_text = TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(
            prompt_rule(skill_text, skill=True),
            prompt_rule(template_text),
        )

    def test_rule_is_self_contained_and_logs_only_to_agents_log(self):
        rule = prompt_rule(TEMPLATE.read_text(encoding="utf-8"))
        self.assertIn("`AGENTS.log`", rule)
        self.assertNotRegex(rule, r"`(?:docs/|\.gitignore|[A-Za-z0-9._/-]+\.(?:md|json|ya?ml))")
        for required in ("subagents", "RFC 5322", "[REDACTED]", "Append only", "never commit", "appending fails", "owner-only", "hard-linked", "Git index", "current event identity", "first tool operation"):
            with self.subTest(required=required):
                self.assertIn(required, rule)

    def test_skill_does_not_depend_on_a_separate_prompt_policy_or_hook_setup(self):
        skill_text = SKILL.read_text(encoding="utf-8")
        self.assertNotIn("docs/agents-log-policy.md", skill_text)
        self.assertNotIn("docs/agents/prompt-logging.md", skill_text)
        self.assertNotIn("assets/prompt-logging/hosts.md", skill_text)
        self.assertIn("Do not install or configure hooks", skill_text)

    def test_deferred_facts_have_an_explicit_consumer(self):
        setup = SKILL.read_text(encoding="utf-8")
        consumer = (ROOT / "penta-pro" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("defer approved facts to `docs/agents/setup-notes.md`", setup)
        self.assertIn("read `docs/agents/setup-notes.md` when present", consumer)
        self.assertIn("preserving sources, dates", consumer)


if __name__ == "__main__":
    unittest.main()
