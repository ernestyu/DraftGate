from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G5 = ROOT / "docs" / "writing" / "commentary" / "gates" / "05-claim-evidence-boundary.md"
REGISTRY = ROOT / "docs" / "writing" / "commentary" / "gate-registry.json"


class WritingG5AdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g5 = G5.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.by_id = {g["id"]: g for g in cls.registry["gates"]}

    def test_g5_requires_strongest_reasonable_objection(self):
        self.assertIn("strongest reasonable objection", self.g5)
        self.assertIn("strawman objection", self.g5)
        self.assertIn("Do not satisfy this check with", self.g5)

    def test_g5_requires_alternative_mechanism(self):
        self.assertIn("Alternative mechanism", self.g5)
        self.assertIn("another mechanism", self.g5)
        self.assertIn("do not present the article's mechanism as the only cause", self.g5)

    def test_g5_requires_falsification_boundary(self):
        self.assertIn("Counterfactual / falsification condition", self.g5)
        self.assertIn("materially weaken or falsify the claim", self.g5)
        self.assertIn("self-sealing", self.g5)

    def test_keep_can_map_to_no_change_only_after_full_check(self):
        self.assertIn("KEEP\n→ G5-authorized NO_CHANGE", self.g5)
        self.assertIn("without completing the pressure test is not a valid NO_CHANGE", self.g5)
        self.assertIn("no necessary G5-authorized article modification remains", self.g5)

    def test_keep_can_still_use_changed(self):
        self.assertIn("KEEP does not force NO_CHANGE", self.g5)
        self.assertIn("use the normal CHANGED path", self.g5)

    def test_stop_conflict_does_not_advance(self):
        self.assertIn("STOP_CONFLICT", self.g5)
        self.assertIn("do not advance G5", self.g5)
        self.assertIn("do not use NO_CHANGE", self.g5)
        self.assertIn("do not automatically roll back G1–G3", self.g5)

    def test_no_mandatory_opposition_section(self):
        self.assertIn("does not require a dedicated opposing-view section", self.g5)
        self.assertIn("Do not mechanically add stock opposition framing", self.g5)

    def test_registry_authorizes_only_g5_new_no_change(self):
        self.assertTrue(self.by_id["G5"]["allow_no_change"])
        for gate_id in ("G1", "G2", "G3", "G4", "G6", "G7"):
            with self.subTest(gate_id=gate_id):
                self.assertFalse(self.by_id[gate_id]["allow_no_change"])

    def test_narrative_compatible_expression_preserves_precision(self):
        self.assertIn("Narrative-compatible adversarial expression", self.g5)
        self.assertIn("strongest reasonable objection", self.g5)
        self.assertIn("counterfactual / falsification condition", self.g5)
        self.assertIn("precision > narrative elegance", self.g5)
        self.assertIn("direct, abstract, or technical language", self.g5)

    def test_narrative_compatibility_does_not_reduce_rigor(self):
        self.assertIn("Narrative compatibility must not reduce", self.g5)
        for term in (
            "objection strength",
            "evidence boundary",
            "causal uncertainty",
            "alternative mechanism",
            "falsification condition",
        ):
            self.assertIn(term, self.g5)


if __name__ == "__main__":
    unittest.main()
