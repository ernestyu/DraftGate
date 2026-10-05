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


VW = load_module("vw_reopen_test", REPO_ROOT / "scripts" / "validate-writing-workflow.py")
WS = load_module("ws_reopen_test", REPO_ROOT / "scripts" / "writing-state.py")
VC = load_module("vc_reopen_test", REPO_ROOT / "scripts" / "validate-writing-commit.py")


class WritingReopenTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.article_id = "20261004-reopen"
        self.article_path = f"articles/{self.article_id}/index.md"
        self.state_path = f".writing-state/write-commentary/{self.article_id}.json"

        src = REPO_ROOT / "docs" / "writing" / "commentary"
        shutil.copytree(src, self.root / "docs" / "writing" / "commentary", dirs_exist_ok=True)

        article = self.root / self.article_path
        article.parent.mkdir(parents=True, exist_ok=True)
        article.write_text("---\ntitle: test\n---\n\nInitial.\n", encoding="utf-8")

        self.git("init")
        self.git("config", "user.name", "Reopen Test")
        self.git("config", "user.email", "reopen@example.invalid")
        self.git("add", ".")
        self.git("commit", "-m", "initial")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True, stderr=subprocess.STDOUT).strip()

    def init_state(self, entry: str = "G1") -> dict:
        state = WS.init_state(self.article_id, self.article_path, self.root, entry)
        self.git("add", self.state_path)
        self.git("commit", "-m", f"Writing-Workflow: init\nWriting-Article: {self.article_id}")
        return state

    def read_state(self) -> dict:
        return json.loads((self.root / self.state_path).read_text(encoding="utf-8"))

    def write_state(self, state: dict) -> None:
        p = self.root / self.state_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def prepare(self, entry: str, completed: list[str], current: str) -> None:
        self.init_state(entry)
        state = self.read_state()
        state["completed"] = completed
        state["current_gate"] = current
        self.write_state(state)
        self.git("add", self.state_path)
        self.git("commit", "-m", "prepare state")

    def commit_reopen(self) -> str:
        self.git("add", ".")
        self.git("commit", "-m", f"test reopen\n\nWriting-Workflow: reopen\nWriting-Article: {self.article_id}")
        return self.git("rev-parse", "HEAD")

    def test_g1_reopen_to_g1(self):
        self.prepare("G1", ["G1"], "G2")
        before_rev = self.read_state()["article_revision"]
        after = WS.reopen_state(self.article_id, self.root)
        self.assertEqual(after["completed"], [])
        self.assertEqual(after["current_gate"], "G1")
        self.assertEqual(after["article_revision"], before_rev)

    def test_selectable_entry_reopen_last_gate(self):
        self.prepare("G4", ["G4", "G5"], "G6")
        after = WS.reopen_state(self.article_id, self.root)
        self.assertEqual(after["completed"], ["G4"])
        self.assertEqual(after["current_gate"], "G5")
        self.assertEqual(after["entry_gate"], "G4")
        self.assertEqual(after["skipped_by_user"], ["G1","G2","G3"])

    def test_entry_gate_itself_can_be_reopened(self):
        self.prepare("G5", ["G5"], "G6")
        after = WS.reopen_state(self.article_id, self.root)
        self.assertEqual(after["completed"], [])
        self.assertEqual(after["current_gate"], "G5")

    def test_complete_state_reopen_fails(self):
        self.init_state("G7")
        state = self.read_state()
        state["completed"] = ["G7"]
        state["current_gate"] = None
        state["status"] = "complete"
        self.write_state(state)
        self.git("add", self.state_path)
        self.git("commit", "-m", "complete")
        with self.assertRaisesRegex(WS.StateError, "reopen requires in_progress"):
            WS.reopen_state(self.article_id, self.root)

    def test_stale_state_reopen_fails(self):
        self.prepare("G1", ["G1"], "G2")
        (self.root / self.article_path).write_text("---\ntitle: changed\n---\n\nExternal.\n", encoding="utf-8")
        self.git("add", self.article_path)
        self.git("commit", "-m", "external edit")
        with self.assertRaisesRegex(WS.StateError, "STATE STALE"):
            WS.reopen_state(self.article_id, self.root)

    def test_commit_validator_accepts_state_only_reopen(self):
        self.prepare("G1", ["G1"], "G2")
        article_before = self.git("rev-parse", f"HEAD:{self.article_path}")
        WS.reopen_state(self.article_id, self.root)
        commit = self.commit_reopen()
        self.assertEqual(VC.validate_commit(self.root, commit), [])
        self.assertEqual(article_before, self.git("rev-parse", f"{commit}:{self.article_path}"))

    def test_reopen_with_article_change_fails(self):
        self.prepare("G1", ["G1"], "G2")
        WS.reopen_state(self.article_id, self.root)
        (self.root / self.article_path).write_text("---\ntitle: changed\n---\n\nBad.\n", encoding="utf-8")
        commit = self.commit_reopen()
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("changed_paths must equal bound state file only" in x for x in failures))

    def test_reopen_extra_path_fails(self):
        self.prepare("G1", ["G1"], "G2")
        WS.reopen_state(self.article_id, self.root)
        (self.root / "extra.txt").write_text("extra\n", encoding="utf-8")
        commit = self.commit_reopen()
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("changed_paths must equal bound state file only" in x for x in failures))

    def test_multi_gate_rollback_fails(self):
        self.prepare("G4", ["G4","G5"], "G6")
        before = self.read_state()
        after = json.loads(json.dumps(before))
        after["completed"] = []
        after["current_gate"] = "G4"
        failures = VW.validate_reopen(VW.load_registry(self.root), before, after)
        self.assertTrue(failures)

    def test_article_revision_mutation_fails(self):
        self.prepare("G1", ["G1"], "G2")
        before = self.read_state()
        after = json.loads(json.dumps(before))
        after["completed"] = []
        after["current_gate"] = "G1"
        after["article_revision"] = "1" * 40
        failures = VW.validate_reopen(VW.load_registry(self.root), before, after)
        self.assertTrue(any("article_revision" in x for x in failures))

    def test_reopen_trailer_rejects_writing_gate(self):
        self.prepare("G1", ["G1"], "G2")
        WS.reopen_state(self.article_id, self.root)
        self.git("add", ".")
        self.git("commit", "-m", f"test reopen\n\nWriting-Workflow: reopen\nWriting-Article: {self.article_id}\nWriting-Gate: G1")
        commit = self.git("rev-parse", "HEAD")
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("Writing-Gate is allowed only for gate operation" in x for x in failures))


if __name__ == "__main__":
    unittest.main()
