from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


VW = load_module("validate_writing_workflow_custom_rules_test", ROOT / "scripts" / "validate-writing-workflow.py")
WORKFLOW = (ROOT / "docs" / "writing" / "commentary" / "workflow.md").read_text(encoding="utf-8")
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")


class WritingCustomRulesTests(unittest.TestCase):
    def registry(self):
        return {"gates": [{"id": f"G{i}"} for i in range(1, 8)]}

    def test_missing_custom_rules_directory_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(VW.validate_custom_rules(Path(tmp), self.registry()), [])

    def test_valid_per_gate_custom_rule_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rules = root / ".writing-rules"
            rules.mkdir()
            (rules / "G3.md").write_text("Prefer case-driven secondary material.\n", encoding="utf-8")
            self.assertEqual(VW.validate_custom_rules(root, self.registry()), [])

    def test_unknown_gate_custom_rule_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rules = root / ".writing-rules"
            rules.mkdir()
            (rules / "G8.md").write_text("invalid\n", encoding="utf-8")
            failures = VW.validate_custom_rules(root, self.registry())
            self.assertTrue(any("unexpected Custom Rules entry" in x for x in failures))

    def test_current_gate_only_execution_contract(self):
        self.assertIn("Custom Rules from any other Gate", WORKFLOW)
        self.assertIn("execution, editing, evaluation, or PASS / FAIL decisions", WORKFLOW)
        self.assertIn("rule maintenance", WORKFLOW)

    def test_core_precedence_and_conflict_behavior(self):
        self.assertIn("Core always has higher authority than Custom Rules", WORKFLOW)
        self.assertIn("conflicting Custom Rule is ignored for this execution", WORKFLOW)
        self.assertIn("explicitly inform the user", WORKFLOW)
        self.assertIn("do not modify workflow state merely because of the conflict", WORKFLOW)

    def test_agents_load_only_current_gate_custom_rules(self):
        self.assertIn(".writing-rules/Gx.md", AGENTS)
        self.assertIn("Custom Rules from other Gates must not participate", AGENTS)


if __name__ == "__main__":
    unittest.main()
