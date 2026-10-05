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
        self.assertIn("最强的合理反驳", self.g5)
        self.assertIn("strawman objection", self.g5)
        self.assertIn("不得用以下内容完成检查", self.g5)

    def test_g5_requires_alternative_mechanism(self):
        self.assertIn("Alternative mechanism", self.g5)
        self.assertIn("不得把本文机制继续写成唯一原因", self.g5)

    def test_g5_requires_falsification_boundary(self):
        self.assertIn("Counterfactual / falsification condition", self.g5)
        self.assertIn("会让这个 claim 明显变弱或失败", self.g5)
        self.assertIn("self-sealing", self.g5)

    def test_keep_can_map_to_no_change_only_after_full_check(self):
        self.assertIn("KEEP\n→ G5-authorized NO_CHANGE", self.g5)
        self.assertIn("仅仅“没有发现问题”但没有完成完整 pressure test，不构成合法 NO_CHANGE", self.g5)
        self.assertIn("不存在任何必要的 G5-authorized article modification", self.g5)

    def test_keep_can_still_use_changed(self):
        self.assertIn("KEEP 不等于强制 NO_CHANGE", self.g5)
        self.assertIn("则走 CHANGED", self.g5)

    def test_stop_conflict_does_not_advance(self):
        self.assertIn("STOP_CONFLICT", self.g5)
        self.assertIn("不 advance G5", self.g5)
        self.assertIn("不使用 NO_CHANGE", self.g5)
        self.assertIn("不自动回退 G1–G3", self.g5)

    def test_no_mandatory_opposition_section(self):
        self.assertIn("不要求新增“反方观点”章节", self.g5)
        self.assertIn("不得为了展示“考虑全面”机械加入", self.g5)

    def test_registry_authorizes_only_g5_new_no_change(self):
        self.assertTrue(self.by_id["G5"]["allow_no_change"])
        for gate_id in ("G1","G2","G3","G4","G6","G7"):
            with self.subTest(gate_id=gate_id):
                self.assertFalse(self.by_id[gate_id]["allow_no_change"])


    def test_narrative_compatible_expression_preserves_precision(self):
        self.assertIn("Narrative-compatible adversarial expression", self.g5)
        self.assertIn("strongest reasonable objection", self.g5)
        self.assertIn("boundary", self.g5)
        self.assertIn("counterfactual / falsification condition", self.g5)
        self.assertIn("precision > narrative elegance", self.g5)
        self.assertIn("直接、抽象、技术性的表述", self.g5)

    def test_narrative_compatibility_does_not_reduce_rigor(self):
        self.assertIn("Narrative compatibility 不得降低", self.g5)
        self.assertIn("objection strength", self.g5)
        self.assertIn("evidence boundary", self.g5)
        self.assertIn("causal uncertainty", self.g5)
        self.assertIn("alternative mechanism", self.g5)
        self.assertIn("falsification condition", self.g5)


if __name__ == "__main__":
    unittest.main()
