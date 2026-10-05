from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G7 = ROOT / "docs" / "writing" / "commentary" / "gates" / "07-final-language-ai-trace.md"


class WritingG7NarrativeConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g7 = G7.read_text(encoding="utf-8")

    def test_opening_to_section1_handoff_exists(self):
        self.assertIn("Opening → Section 1 Handoff Check", self.g7)
        self.assertIn("advance to a new mechanism or explanatory layer", self.g7)
        self.assertIn("same major claim", self.g7)

    def test_narrative_repetition_audit_exists(self):
        self.assertIn("Narrative Repetition Audit", self.g7)
        self.assertIn("summary → explanation → summary", self.g7)
        self.assertIn("meta-signposting", self.g7)

    def test_pattern_rules_are_language_neutral(self):
        self.assertIn("Mechanical Writing Pattern Audit", self.g7)
        self.assertIn("semantic and language-neutral", self.g7)
        self.assertIn("No bundled word blacklist is authoritative", self.g7)
        self.assertNotIn("lexicon.yaml", self.g7)

    def test_g7_cannot_change_paragraph_boundaries(self):
        self.assertIn("merge paragraph", self.g7)
        self.assertIn("split paragraph", self.g7)
        self.assertIn("change paragraph boundary", self.g7)
        self.assertIn("re-run G6", self.g7)

    def test_g7_remains_terminal(self):
        self.assertIn("only normal terminal gate", self.g7)
        self.assertIn("final body-editing boundary", self.g7)
        self.assertIn("set the workflow to complete", self.g7)


if __name__ == "__main__":
    unittest.main()
