from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "docs" / "writing" / "commentary" / "ai-trace" / "rules.md"
LEXICON = ROOT / "docs" / "writing" / "commentary" / "ai-trace" / "lexicon.yaml"


def rule_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (RULE-\d+):[^\n]*$", text, re.M))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[match.start():end]
    return sections


class WritingPatternRulesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules_text = RULES.read_text(encoding="utf-8")
        cls.lexicon_text = LEXICON.read_text(encoding="utf-8")
        cls.rules = rule_sections(cls.rules_text)

    def test_core_pattern_rules_exist(self):
        for rule_id in [f"RULE-{i:03d}" for i in range(1, 16)]:
            with self.subTest(rule_id=rule_id):
                self.assertIn(rule_id, self.rules)

    def test_rules_are_contextual_and_preserve_meaning(self):
        for section in self.rules.values():
            self.assertIn("Candidate trigger:", section)
            self.assertTrue(
                "Context judgment:" in section or "Authorized action:" in section
            )
            self.assertIn("Preservation constraints:", section)

    def test_public_lexicon_has_no_language_specific_entries(self):
        self.assertIn("entries: []", self.lexicon_text)
        self.assertNotIn("越来越", self.lexicon_text)
        self.assertNotIn("真正", self.lexicon_text)
        self.assertNotIn("总而言之", self.lexicon_text)

    def test_personal_style_constraints_are_not_in_pattern_rules(self):
        forbidden = [
            "authorial singular first-person",
            "350 Chinese characters",
            "450 Chinese characters",
            "公众号",
            "我认为",
            "在我看来",
        ]
        combined = self.rules_text + "\n" + self.lexicon_text
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, combined)


if __name__ == "__main__":
    unittest.main()
