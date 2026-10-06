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
        self.assertIn("use an accurate explanatory analogy", self.g4)
        self.assertIn("must not replace the mechanism explanation", self.g4)

    def test_g4_allows_concrete_scenario(self):
        self.assertIn("use a concrete scenario to build intuition", self.g4)
        self.assertIn("A concrete scenario may be used instead of a metaphor", self.g4)

    def test_analogy_must_serve_mechanism(self):
        self.assertIn("must perform a clear mechanism mapping", self.g4)
        self.assertIn("Analogies may build intuition", self.lang)
        self.assertIn("return to the real mechanism", self.lang)

    def test_analogy_cannot_replace_evidence(self):
        self.assertIn("An analogy is not evidence", self.g4)
        self.assertIn("use analogy as evidence", self.g4)
        self.assertIn("does not prove causality", self.lang)

    def test_analogy_boundary_required(self):
        self.assertIn("where the analogy fails or no longer applies", self.g4)
        self.assertIn("minimum boundary statement", self.g4)

    def test_public_language_rules_do_not_impose_personal_style(self):
        self.assertIn("do not prescribe a personal voice", self.lang)
        self.assertIn("No specific paragraph length", self.lang)
        self.assertIn("first-person policy", self.lang)

    def test_g4_does_not_change_claim_strength(self):
        self.assertIn("must not change claim strength", self.g4)
        self.assertIn("STOP", self.g4)
        self.assertIn("Do not silently perform G5 work inside G4", self.g4)


if __name__ == "__main__":
    unittest.main()
