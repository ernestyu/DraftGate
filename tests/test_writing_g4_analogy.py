from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G4 = ROOT / "docs" / "writing" / "commentary" / "gates" / "04-reader-accessibility.md"
LANG = ROOT / "docs" / "writing" / "commentary" / "language-rules.md"


class WritingG4AnalogyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g4 = G4.read_text(encoding="utf-8")
        cls.lang = LANG.read_text(encoding="utf-8")

    def test_g4_allows_explanatory_analogy(self):
        self.assertIn("使用准确的解释型类比", self.g4)
        self.assertIn("类比不能替代机制解释", self.g4)

    def test_g4_allows_concrete_scenario(self):
        self.assertIn("使用具体场景帮助读者形成直觉", self.g4)
        self.assertIn("过去需要十个人", self.g4)

    def test_analogy_must_serve_mechanism(self):
        self.assertIn("解释型类比必须承担清楚的机制映射", self.g4)
        self.assertIn("Analogies may build intuition", self.lang)
        self.assertIn("return to the real mechanism", self.lang)

    def test_analogy_cannot_replace_evidence(self):
        self.assertIn("类比不是证据", self.g4)
        self.assertIn("用类比替代证据", self.g4)
        self.assertIn("does not prove causality", self.lang)

    def test_analogy_boundary_required(self):
        self.assertIn("类比在哪些地方会失效或不再适用", self.g4)
        self.assertIn("必要时增加一句最小边界说明", self.g4)

    def test_public_language_rules_do_not_impose_personal_style(self):
        self.assertIn("do not prescribe a personal voice", self.lang)
        self.assertIn("No specific paragraph length", self.lang)
        self.assertIn("first-person policy", self.lang)

    def test_g4_does_not_change_claim_strength(self):
        self.assertIn("改变 G5 claim strength", self.g4)
        self.assertIn("STOP", self.g4)
        self.assertIn("不得在 G4 顺手修复 G5 问题", self.g4)


if __name__ == "__main__":
    unittest.main()
