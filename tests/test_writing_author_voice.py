from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "writing" / "commentary" / "base-rules.md"
LANG = ROOT / "docs" / "writing" / "commentary" / "language-rules.md"
G7 = ROOT / "docs" / "writing" / "commentary" / "gates" / "07-final-language-ai-trace.md"
CHECKLIST = ROOT / "docs" / "writing" / "commentary" / "checklist.md"


class WritingVoiceNeutralityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = "\n".join(
            p.read_text(encoding="utf-8")
            for p in (BASE, LANG, G7, CHECKLIST)
        )

    def test_public_rules_do_not_forbid_first_person(self):
        self.assertNotIn("作者正文默认不使用作者单数第一人称", self.text)
        self.assertNotIn("authorial singular first-person = 0", self.text)
        self.assertNotIn("必须先得到用户明确授权", self.text)

    def test_public_rules_explicitly_avoid_personal_voice_policy(self):
        self.assertIn("Do not impose a default authorial persona", self.text)
        self.assertIn("No specific paragraph length", self.text)
        self.assertIn("Voice is internally consistent", self.text)


if __name__ == "__main__":
    unittest.main()
