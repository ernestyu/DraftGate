from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G2 = ROOT / "docs" / "writing" / "commentary" / "gates" / "02-scope-branch-control.md"


class WritingG2ScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g2 = G2.read_text(encoding="utf-8")

    def test_scope_roles_are_preserved(self):
        for role in ("core", "support", "boundary", "separate-article candidate"):
            self.assertIn(role, self.g2)

    def test_article_keeps_one_center(self):
        self.assertIn("one center", self.g2)
        self.assertIn("no two co-equal centers", self.g2)

    def test_g2_does_not_take_over_architecture(self):
        self.assertIn("redesign section order", self.g2)
        self.assertIn("perform G3 architecture work", self.g2)

    def test_g2_allows_only_minimum_scope_adjustment(self):
        self.assertIn("minimum scope adjustment", self.g2)
        self.assertIn("keep the main question intact", self.g2)


if __name__ == "__main__":
    unittest.main()
