from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


VW = load_module("validate_writing_workflow_test", REPO_ROOT / "scripts" / "validate-writing-workflow.py")
WS = load_module("writing_state_test", REPO_ROOT / "scripts" / "writing-state.py")


class WritingStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.article_id = "20261003-test-article"
        self.article_path = f"articles/{self.article_id}/index.md"

        src = REPO_ROOT / "docs" / "writing" / "commentary"
        dst = self.root / "docs" / "writing" / "commentary"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)

        article = self.root / self.article_path
        article.parent.mkdir(parents=True, exist_ok=True)
        article.write_text("---\ntitle: test\n---\n\nInitial article.\n", encoding="utf-8")

        self.git("init")
        self.git("config", "user.name", "Writing Test")
        self.git("config", "user.email", "writing-test@example.invalid")
        self.git("add", ".")
        self.git("commit", "-m", "initial")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            ["git", *args],
            cwd=self.root,
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()

    def commit_all(self, message: str = "test commit") -> None:
        self.git("add", ".")
        self.git("commit", "-m", message)

    def init_state(self, entry_gate: str = "G1") -> dict:
        return WS.init_state(self.article_id, self.article_path, self.root, entry_gate)

    def read_state(self) -> dict:
        return WS.read_state(self.article_id, self.root)

    def write_state(self, state: dict) -> None:
        WS.atomic_write_state(state, self.root)

    def modify_article(self, text: str) -> None:
        (self.root / self.article_path).write_text(text, encoding="utf-8")

    # Stage B regression coverage

    def test_init_and_valid_resume(self):
        state = self.init_state()
        self.assertEqual(state["schema_version"], 4)
        self.assertEqual(state["entry_gate"], "G1")
        self.assertEqual(state["skipped_by_user"], [])
        self.assertEqual(state["current_gate"], "G1")
        self.assertEqual(state["completed"], [])
        self.assertEqual(state["article_revision"], VW.git_blob_at_head(self.root, self.article_path))
        resumed = WS.validate_for_resume(self.article_id, self.root)
        self.assertEqual(resumed, state)

    def test_duplicate_state_fails(self):
        self.init_state()
        with self.assertRaisesRegex(WS.StateError, "state already exists"):
            self.init_state()

    def test_special_path_article_ids_fail(self):
        for bad_id in (".", ".."):
            with self.subTest(article_id=bad_id):
                self.assertFalse(VW.valid_article_id(bad_id))
                with self.assertRaisesRegex(WS.StateError, "invalid article_id"):
                    WS.state_path(bad_id, self.root)

    def test_stale_resume_fails_after_external_article_commit(self):
        self.init_state()
        self.commit_all("init writing state")
        self.modify_article("---\ntitle: test\n---\n\nExternal edit.\n")
        self.commit_all("external article edit")
        with self.assertRaisesRegex(WS.StateError, "STATE STALE"):
            WS.validate_for_resume(self.article_id, self.root)

    def test_stale_advance_fails_after_external_article_commit(self):
        self.init_state()
        self.commit_all("init writing state")
        self.modify_article("---\ntitle: test\n---\n\nExternal edit.\n")
        self.commit_all("external article edit")
        with self.assertRaisesRegex(WS.StateError, "STATE STALE"):
            WS.advance_state(self.article_id, self.root)

    def test_g1_to_g2_advance_and_resume_after_commit(self):
        self.init_state()
        self.commit_all("init writing state")
        self.modify_article("---\ntitle: test\n---\n\nG1 result.\n")
        after = WS.advance_state(self.article_id, self.root)
        self.assertEqual(after["current_gate"], "G2")
        self.assertEqual(after["completed"], ["G1"])
        self.assertEqual(after["entry_gate"], "G1")
        self.assertEqual(after["skipped_by_user"], [])
        working_blob = self.git("hash-object", "--", self.article_path)
        self.assertEqual(after["article_revision"], working_blob)
        self.commit_all("G1 article and state")
        resumed = WS.validate_for_resume(self.article_id, self.root)
        self.assertEqual(resumed["current_gate"], "G2")

    def test_noop_transition_fails(self):
        before = self.init_state()
        failures = VW.validate_transition(
            VW.load_registry(self.root),
            before,
            json.loads(json.dumps(before)),
        )
        self.assertTrue(failures)
        self.assertIn("no-op transition is invalid", failures[0])

    def test_reconcile_changes_only_revision_and_preserves_entry_metadata(self):
        before = self.init_state("G6")
        self.commit_all("init writing state")
        self.modify_article("---\ntitle: test\n---\n\nExternal accepted edit.\n")
        self.commit_all("external article edit")
        old_revision = self.read_state()["article_revision"]
        after = WS.reconcile_state(self.article_id, self.root)
        self.assertNotEqual(after["article_revision"], old_revision)
        for field in (
            "workflow", "article_id", "article_path", "cycle",
            "entry_gate", "skipped_by_user", "current_gate", "completed", "status",
        ):
            self.assertEqual(after[field], before[field])
        self.assertEqual(after["article_revision"], VW.git_blob_at_head(self.root, self.article_path))

    def test_start_cycle_requires_complete_state(self):
        self.init_state()
        with self.assertRaisesRegex(WS.StateError, "requires complete state"):
            WS.start_cycle(self.article_id, self.root)

    def test_complete_resume_allows_article_drift(self):
        state = self.init_state("G7")
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        self.write_state(state)
        self.commit_all("complete cycle")
        self.modify_article("---\ntitle: changed\n---\n\nHuman edit.\n")
        self.commit_all("human edit after complete")
        resumed = WS.validate_for_resume(self.article_id, self.root)
        self.assertEqual(resumed["status"], "complete")
        self.assertNotEqual(resumed["article_revision"], VW.git_blob_at_head(self.root, self.article_path))

    def test_complete_advance_still_fails_after_article_edit(self):
        state = self.init_state("G7")
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        self.write_state(state)
        self.commit_all("complete cycle")
        self.modify_article("---\ntitle: changed\n---\n\nHuman edit.\n")
        self.commit_all("human edit after complete")
        with self.assertRaisesRegex(WS.StateError, "cannot advance a complete state"):
            WS.advance_state(self.article_id, self.root)

    def test_complete_reconcile_fails(self):
        state = self.init_state("G7")
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        self.write_state(state)
        self.commit_all("complete cycle")
        with self.assertRaisesRegex(WS.StateError, "reconcile requires in_progress"):
            WS.reconcile_state(self.article_id, self.root)

    # Selectable-entry coverage

    def test_init_from_g4(self):
        state = self.init_state("G4")
        self.assertEqual(state["entry_gate"], "G4")
        self.assertEqual(state["skipped_by_user"], ["G1", "G2", "G3"])
        self.assertEqual(state["completed"], [])
        self.assertEqual(state["current_gate"], "G4")

    def test_init_from_g8_fails(self):
        with self.assertRaisesRegex(WS.StateError, "invalid entry gate"):
            self.init_state("G8")

    def test_invalid_entry_gate_fails(self):
        with self.assertRaisesRegex(WS.StateError, "invalid entry gate"):
            self.init_state("G9")

    def test_skipped_by_user_non_prefix_fails(self):
        state = self.init_state("G4")
        state["skipped_by_user"] = ["G1", "G3"]
        failures = VW.validate_state(VW.load_registry(self.root), state)
        self.assertTrue(failures)

    def test_skipped_and_completed_overlap_fails(self):
        state = self.init_state("G4")
        state["completed"] = ["G3", "G4"]
        state["current_gate"] = "G5"
        failures = VW.validate_state(VW.load_registry(self.root), state)
        self.assertTrue(failures)

    def test_completed_gap_fails(self):
        state = self.init_state("G4")
        state["current_gate"] = "G7"
        state["completed"] = ["G4", "G6"]
        failures = VW.validate_state(VW.load_registry(self.root), state)
        self.assertTrue(failures)

    def test_g4_to_g5_passes_and_g4_to_g6_fails(self):
        before = self.init_state("G4")
        after = json.loads(json.dumps(before))
        after["completed"] = ["G4"]
        after["current_gate"] = "G5"
        self.assertEqual(VW.validate_transition(VW.load_registry(self.root), before, after), [])

        bad = json.loads(json.dumps(after))
        bad["current_gate"] = "G6"
        self.assertTrue(VW.validate_transition(VW.load_registry(self.root), before, bad))

    def test_transition_cannot_change_entry_gate(self):
        before = self.init_state("G4")
        after = json.loads(json.dumps(before))
        after["completed"] = ["G4"]
        after["current_gate"] = "G5"
        after["entry_gate"] = "G3"
        self.assertTrue(VW.validate_transition(VW.load_registry(self.root), before, after))

    def test_transition_cannot_change_skipped_by_user(self):
        before = self.init_state("G4")
        after = json.loads(json.dumps(before))
        after["completed"] = ["G4"]
        after["current_gate"] = "G5"
        after["skipped_by_user"] = ["G1", "G2"]
        self.assertTrue(VW.validate_transition(VW.load_registry(self.root), before, after))

    def test_g7_to_complete(self):
        self.init_state("G7")
        self.commit_all("init G7")
        self.modify_article("---\ntitle: test\n---\n\nG7 result.\n")
        after = WS.advance_state(self.article_id, self.root)
        self.assertEqual(after["status"], "complete")
        self.assertIsNone(after["current_gate"])
        self.assertEqual(after["completed"], ["G7"])
        self.assertEqual(after["skipped_by_user"], ["G1","G2","G3","G4","G5","G6"])

    def test_start_cycle_default_starts_g1(self):
        state = self.init_state("G7")
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        self.write_state(state)
        self.commit_all("complete cycle one")
        after = WS.start_cycle(self.article_id, self.root)
        self.assertEqual(after["cycle"], 2)
        self.assertEqual(after["entry_gate"], "G1")
        self.assertEqual(after["skipped_by_user"], [])
        self.assertEqual(after["current_gate"], "G1")
        self.assertEqual(after["completed"], [])

    def test_start_cycle_from_g6(self):
        state = self.init_state("G7")
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        self.write_state(state)
        self.commit_all("complete cycle one")
        after = WS.start_cycle(self.article_id, self.root, "G6")
        self.assertEqual(after["cycle"], 2)
        self.assertEqual(after["entry_gate"], "G6")
        self.assertEqual(after["skipped_by_user"], ["G1", "G2", "G3", "G4", "G5"])
        self.assertEqual(after["completed"], [])
        self.assertEqual(after["current_gate"], "G6")

    def test_start_cycle_rebases_to_current_article_after_human_edits(self):
        state = self.init_state("G7")
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        completion_snapshot = state["article_revision"]
        self.write_state(state)
        self.commit_all("complete cycle one")
        self.modify_article("---\ntitle: changed once\n---\n\nHuman edit one.\n")
        self.commit_all("human edit one")
        self.modify_article("---\ntitle: changed twice\n---\n\nHuman edit two.\n")
        self.commit_all("human edit two")
        current_blob = VW.git_blob_at_head(self.root, self.article_path)
        self.assertNotEqual(completion_snapshot, current_blob)
        after = WS.start_cycle(self.article_id, self.root, "G4")
        self.assertEqual(after["article_revision"], current_blob)
        self.assertEqual(after["status"], "in_progress")
        self.assertEqual(WS.validate_for_resume(self.article_id, self.root)["article_revision"], current_blob)


if __name__ == "__main__":
    unittest.main()
