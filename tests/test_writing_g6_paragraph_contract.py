from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G6 = ROOT / "docs" / "writing" / "commentary" / "gates" / "06-paragraph-organization.md"


class WritingG6ParagraphContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g6 = G6.read_text(encoding="utf-8")

    def test_semantic_responsibility_is_primary(self):
        self.assertIn("paragraph boundary", self.g6)
        self.assertIn("semantic / argumentative responsibility boundary", self.g6)
        self.assertIn("coherent argumentative function", self.g6)

    def test_functional_short_paragraph_is_allowed(self):
        self.assertIn("Functional short paragraph", self.g6)
        self.assertIn("independent semantic or argumentative responsibility", self.g6)
        self.assertIn("Short length alone is neither a failure nor a virtue", self.g6)

    def test_visual_or_slogan_fragmentation_is_rejected(self):
        self.assertIn("rhythm", self.g6)
        self.assertIn("slogan effect", self.g6)
        self.assertIn("visual spacing", self.g6)
        self.assertIn("one argument action", self.g6)

    def test_no_language_specific_length_thresholds(self):
        self.assertNotIn("350 Chinese characters", self.g6)
        self.assertNotIn("450 Chinese characters", self.g6)
        self.assertIn("Length is not a gate criterion", self.g6)
        self.assertIn("automatic split by character count", self.g6)

    def test_full_paragraph_audit_covers_every_paragraph(self):
        self.assertIn("Full Paragraph Audit", self.g6)
        self.assertIn("audit every paragraph", self.g6)

    def test_over_merge_and_fragmentation_both_fail(self):
        self.assertIn("Over-merge FAIL", self.g6)
        self.assertIn("Fragmentation FAIL", self.g6)


if __name__ == "__main__":
    unittest.main()
