from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G1 = ROOT / "docs" / "writing" / "commentary" / "gates" / "01-main-question.md"


class WritingG1InsightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g1 = G1.read_text(encoding="utf-8")

    def test_insight_test_exists(self):
        self.assertIn("Insight Test", self.g1)
        self.assertIn("correct observation", self.g1)
        self.assertIn("worth-writing explanatory insight", self.g1)

    def test_thesis_must_add_explanatory_value(self):
        self.assertIn("non-obvious enough to add explanatory value", self.g1)
        self.assertIn("mechanism", self.g1)
        self.assertIn("relationship", self.g1)
        self.assertIn("constraint", self.g1)
        self.assertIn("structural change", self.g1)

    def test_consequence_aggregation_is_not_enough(self):
        self.assertIn("consequence aggregation", self.g1)
        self.assertIn("common observations", self.g1)

    def test_weak_insight_cannot_pass_or_advance(self):
        self.assertIn("G1 must not automatically PASS", self.g1)
        self.assertIn("G1 state unchanged", self.g1)
        self.assertIn("do not advance", self.g1)
        self.assertIn("no G1 PASS", self.g1)

    def test_novelty_is_not_required(self):
        self.assertIn("novel at all costs", self.g1)
        self.assertIn("novelty is not required", self.g1)
        self.assertIn("new theory", self.g1)

    def test_forced_profundity_and_claim_inflation_are_forbidden(self):
        self.assertIn("forced profundity forbidden", self.g1)
        self.assertIn("夸大 claim strength", self.g1)
        self.assertIn("concept naming", self.g1)

    def test_exit_requires_insight_pass(self):
        self.assertIn("Insight Test = PASS", self.g1)
        self.assertIn("claim strength remains supported", self.g1)


if __name__ == "__main__":
    unittest.main()
