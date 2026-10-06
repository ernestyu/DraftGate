from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMENTARY = ROOT / "docs" / "writing" / "commentary"

GATES = [
    COMMENTARY / "gates" / "01-main-question.md",
    COMMENTARY / "gates" / "02-scope-branch-control.md",
    COMMENTARY / "gates" / "03-argument-architecture.md",
    COMMENTARY / "gates" / "04-reader-accessibility.md",
    COMMENTARY / "gates" / "05-claim-evidence-boundary.md",
    COMMENTARY / "gates" / "06-paragraph-organization.md",
    COMMENTARY / "gates" / "07-final-language-ai-trace.md",
]

SHARED = [
    COMMENTARY / "base-rules.md",
    COMMENTARY / "structure-rules.md",
    COMMENTARY / "language-rules.md",
    COMMENTARY / "checklist.md",
    COMMENTARY / "ai-trace" / "rules.md",
]

PUBLIC_CORE = GATES + SHARED
CJK_RE = re.compile(r"[\u3400-\u9fff]")


class WritingCoreLanguageNeutralityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core_text = "\n".join(p.read_text(encoding="utf-8") for p in PUBLIC_CORE)

    def test_gate_contracts_have_no_cjk_normative_prose(self):
        for path in GATES:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(CJK_RE.search(text))

    def test_shared_core_has_no_cjk_normative_prose(self):
        for path in SHARED:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(CJK_RE.search(text))

    def test_public_core_does_not_impose_author_persona(self):
        self.assertIn("Do not impose a default authorial persona", self.core_text)
        forbidden = (
            "must write in first person",
            "must write in third person",
            "first person is forbidden",
            "third person is forbidden",
        )
        lowered = self.core_text.lower()
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, lowered)

    def test_public_core_does_not_impose_heading_style(self):
        lowered = self.core_text.lower()
        for phrase in (
            "headings must use title case",
            "headings must be title case",
            "headings must be numbered",
            "all headings must be questions",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, lowered)

    def test_public_core_does_not_impose_fixed_length_policy(self):
        lowered = self.core_text.lower()
        for pattern in (
            r"paragraphs? must (?:contain|have|be) \d+",
            r"sentences? must (?:contain|have|be) \d+",
            r"at least \d+ words? per paragraph",
            r"at most \d+ words? per paragraph",
            r"at least \d+ characters? per paragraph",
            r"at most \d+ characters? per paragraph",
        ):
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, lowered))

    def test_public_core_does_not_ship_phrase_blacklist_policy(self):
        self.assertIn("No bundled word blacklist is authoritative", self.core_text)
        self.assertIn("No specific paragraph length, sentence length, heading format, first-person policy, or phrase blacklist", self.core_text)

    def test_article_language_is_not_restricted_to_english(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Core contract language is English", readme)
        self.assertIn("article language is unrestricted", readme)
        self.assertIn("Chinese, English, or other languages", readme)

    def test_default_custom_rules_remain_empty_scaffolding(self):
        for gate in range(1, 8):
            path = ROOT / ".writing-rules" / f"G{gate}.md"
            text = path.read_text(encoding="utf-8")
            visible = [
                line.strip()
                for line in text.splitlines()
                if line.strip() and not line.lstrip().startswith("<!--")
            ]
            self.assertEqual(visible, [f"# G{gate} Persistent Custom Rules"])

    def test_registry_preserves_same_gate_contracts(self):
        registry = json.loads((COMMENTARY / "gate-registry.json").read_text(encoding="utf-8"))
        gates = registry["gates"]
        self.assertEqual([g["id"] for g in gates], [f"G{i}" for i in range(1, 8)])
        self.assertEqual(
            [g["rule"] for g in gates],
            [
                "gates/01-main-question.md",
                "gates/02-scope-branch-control.md",
                "gates/03-argument-architecture.md",
                "gates/04-reader-accessibility.md",
                "gates/05-claim-evidence-boundary.md",
                "gates/06-paragraph-organization.md",
                "gates/07-final-language-ai-trace.md",
            ],
        )
        self.assertTrue(next(g for g in gates if g["id"] == "G5")["allow_no_change"])
        for gate in gates:
            if gate["id"] != "G5":
                self.assertFalse(gate["allow_no_change"])


if __name__ == "__main__":
    unittest.main()
