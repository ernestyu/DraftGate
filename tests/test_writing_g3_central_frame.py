from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G3 = ROOT / "docs" / "writing" / "commentary" / "gates" / "03-argument-architecture.md"
G4 = ROOT / "docs" / "writing" / "commentary" / "gates" / "04-reader-accessibility.md"
STRUCTURE = ROOT / "docs" / "writing" / "commentary" / "structure-rules.md"


class WritingG3CentralFrameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g3 = G3.read_text(encoding="utf-8")
        cls.g4 = G4.read_text(encoding="utf-8")
        cls.structure = STRUCTURE.read_text(encoding="utf-8")

    def test_g3_checks_whole_article_central_frame(self):
        self.assertIn("central explanatory frame or narrative anchor", self.g3)
        self.assertIn("Central frame decision", self.g3)

    def test_central_frame_is_optional(self):
        self.assertIn("USED", self.g3)
        self.assertIn("NOT NEEDED", self.g3)
        self.assertIn("Do not invent a story", self.g3)
        self.assertIn("central frame or narrative anchor is optional", self.structure)

    def test_frame_must_serve_main_question_and_analysis(self):
        self.assertIn("directly serves the G1 main question", self.g3)
        self.assertIn("serves the G2 frozen main line", self.g3)
        self.assertIn("performs mechanism explanation", self.g3)
        self.assertIn("organize multiple parts of the reasoning", self.structure)

    def test_decorative_hook_is_forbidden(self):
        self.assertIn("disconnected hook", self.g3)
        self.assertIn("decorative hook that has no later function", self.g3)

    def test_frame_cannot_change_g1_or_g2(self):
        self.assertIn("changing G1 thesis or G2 scope to preserve a frame", self.g3)

    def test_g3_g4_boundary_is_explicit(self):
        self.assertIn("whole-article frame", self.g3)
        self.assertIn("local explanatory analogy", self.g3)
        self.assertIn("must not promote a local analogy into a new whole-article frame", self.g4)

    def test_g5_may_challenge_frame_validity(self):
        self.assertIn("G5 challenge boundary", self.g3)
        self.assertIn("whether the frame overextends the analogy", self.g3)
        self.assertIn("Do not preserve a false mapping", self.g3)

    def test_narrative_mode_candidates_require_user_selection(self):
        self.assertIn("Narrative Mode Decision", self.g3)
        self.assertIn("1–3 narrative-mode candidates", self.g3)
        self.assertIn("must not choose the mode on the user's behalf", self.g3)
        self.assertIn("G3 state unchanged", self.g3)
        self.assertIn("do not advance", self.g3)

    def test_narrative_modes_are_distinct(self):
        for mode in ("question-driven", "frame-driven", "case-driven", "hybrid", "other / no special narrative mode"):
            with self.subTest(mode=mode):
                self.assertIn(mode, self.g3)
        self.assertIn("primary driver", self.g3)
        self.assertIn("Do not create two competing main lines", self.g3)

    def test_material_hierarchy_is_explicit(self):
        for role in (
            "Primary narrative driver",
            "Primary mechanism",
            "Supporting evidence",
            "Local analogy",
            "Removable / demoted material",
            "Central frame role",
        ):
            with self.subTest(role=role):
                self.assertIn(role, self.g3)
        self.assertIn("good example != suitable example", self.g3)
        self.assertIn("Supporting evidence must not form a competing narrative spine", self.g3)

    def test_phenomenon_first_is_conditional(self):
        self.assertIn("Conditional phenomenon-first architecture", self.g3)
        self.assertIn("Phenomenon-first is conditional", self.g3)
        self.assertIn("not a universal opening requirement", self.g3)

    def test_frame_driven_requires_used_but_question_driven_does_not(self):
        self.assertIn("frame-driven\n→ central frame must be USED", self.g3)
        self.assertIn("question-driven\n→ central frame may be NOT NEEDED", self.g3)

    def test_explanatory_spine_is_required(self):
        self.assertIn("Explanatory Spine Check", self.g3)
        self.assertIn("Explanatory Spine", self.g3)
        self.assertIn("mechanism / relationship / contradiction / constraint chain", self.g3)

    def test_narrative_mode_and_central_frame_do_not_replace_spine(self):
        self.assertIn("Narrative Mode != Explanatory Spine", self.g3)
        self.assertIn("Central Frame != Explanatory Spine", self.g3)

    def test_spine_is_expressed_in_one_to_three_sentences(self):
        self.assertIn("Explanatory spine:", self.g3)
        self.assertIn("1–3 sentences", self.g3)
        self.assertIn("starting condition", self.g3)
        self.assertIn("intermediate implication", self.g3)

    def test_major_sections_must_advance_or_support_spine(self):
        self.assertIn("How does this section advance or support the Explanatory Spine?", self.g3)
        self.assertIn("demoted", self.g3)
        self.assertIn("removed", self.g3)
        self.assertIn("assigned a different role", self.g3)

    def test_compression_test_requires_reasoning_chain(self):
        self.assertIn("Compression Test", self.g3)
        self.assertIn("3–4 sentences", self.g3)
        for term in ("starting point", "core mechanism", "key intermediate inference", "final judgment"):
            self.assertIn(term, self.g3)

    def test_g3_cannot_silently_rewrite_g1_thesis(self):
        self.assertIn("G1 / G3 authority boundary", self.g3)
        self.assertIn("must not silently replace or rewrite the G1 thesis", self.g3)
        self.assertIn("report G1 conflict", self.g3)
        self.assertIn("do not advance G3", self.g3)

    def test_g3_requires_draft_construction(self):
        self.assertIn("Draft Construction", self.g3)
        self.assertIn("complete first draft", self.g3)
        self.assertIn("section skeleton", self.g3)
        self.assertIn("placeholder-heavy draft", self.g3)

    def test_g3_draft_completeness_has_no_length_threshold(self):
        self.assertIn("Do not use fixed word count", self.g3)
        self.assertIn("paragraph count", self.g3)
        self.assertIn("character threshold", self.g3)

    def test_g3_preserves_sufficient_existing_prose(self):
        self.assertIn("preserve it as much as possible", self.g3)
        self.assertIn("only the changes necessary", self.g3)

    def test_g3_does_not_take_over_downstream_gates(self):
        self.assertIn("draft construction necessity", self.g3)
        self.assertIn("downstream Gate responsibility", self.g3)
        self.assertIn("G4 accessibility audit", self.g3)
        self.assertIn("G5 adversarial / evidence pressure test", self.g3)
        self.assertIn("G6 paragraph audit / restructuring", self.g3)
        self.assertIn("G7 language / pattern / AI-trace cleanup", self.g3)


if __name__ == "__main__":
    unittest.main()
