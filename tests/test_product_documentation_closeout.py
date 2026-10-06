from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

VW = load_module("validate_writing_workflow_product_closeout", ROOT / "scripts" / "validate-writing-workflow.py")


class ProductDocumentationCloseoutTests(unittest.TestCase):
    def test_all_default_custom_rule_scaffolds_exist(self):
        for gate in range(1, 8):
            path = ROOT / ".writing-rules" / f"G{gate}.md"
            self.assertTrue(path.is_file(), path)
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"# G{gate} Persistent Custom Rules", text)

    def test_default_scaffolds_do_not_ship_author_preferences(self):
        for gate in range(1, 8):
            text = (ROOT / ".writing-rules" / f"G{gate}.md").read_text(encoding="utf-8")
            visible = [
                line.strip()
                for line in text.splitlines()
                if line.strip() and not line.lstrip().startswith("<!--")
            ]
            self.assertEqual(visible, [f"# G{gate} Persistent Custom Rules"])

    def test_repository_custom_rules_validate(self):
        registry = VW.load_registry(ROOT)
        self.assertEqual(VW.validate_custom_rules(ROOT, registry), [])

    def test_documentation_describes_personal_profile_layer(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        workflow = (ROOT / "docs" / "writing" / "commentary" / "workflow.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs" / "writing" / "CUSTOM_RULES.md").read_text(encoding="utf-8")

        self.assertIn("Personalize your writing style", readme)
        self.assertIn("Persistent Custom Rules", readme)
        self.assertIn("自定义长期写作风格", zh)
        self.assertIn("GitHub Actions 自动完成 closeout", zh)
        self.assertIn("one-off article edits", agents)
        self.assertIn("empty scaffolding", workflow)
        self.assertIn("A normal article edit does **not** automatically become a Custom Rule.", guide)
        self.assertIn("Core always wins", guide)

    def test_version_and_release_contract(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "v1.0.0")
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())
        self.assertTrue((ROOT / "docs" / "releases" / "v1.0.0.md").is_file())
        release = (ROOT / ".github" / "workflows" / "release-version.yml").read_text(encoding="utf-8")
        self.assertIn("contents: write", release)
        self.assertIn("gh release create", release)
        self.assertIn("git tag -a", release)


if __name__ == "__main__":
    unittest.main()
