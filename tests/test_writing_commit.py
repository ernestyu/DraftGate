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


VW = load_module("validate_writing_workflow_commit_test", REPO_ROOT / "scripts" / "validate-writing-workflow.py")
VC = load_module("validate_writing_commit_test", REPO_ROOT / "scripts" / "validate-writing-commit.py")


class WritingCommitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.article_id = "20261003-test-article"
        self.article_path = f"articles/{self.article_id}/index.md"
        self.state_path = f".writing-state/write-commentary/{self.article_id}.json"

        src = REPO_ROOT / "docs" / "writing" / "commentary"
        dst = self.root / "docs" / "writing" / "commentary"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)

        article = self.root / self.article_path
        article.parent.mkdir(parents=True, exist_ok=True)
        article.write_text("---\ntitle: test\n---\n\nInitial.\n", encoding="utf-8")

        self.git("init")
        self.git("config", "user.name", "Writing Commit Test")
        self.git("config", "user.email", "writing-commit-test@example.invalid")
        self.git("add", ".")
        self.git("commit", "-m", "initial")

        self.write_state(self.make_state("G1"))
        self.git("add", self.state_path)
        self.git("commit", "-m", self.msg("init", article=self.article_id))

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            ["git", *args],
            cwd=self.root,
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()

    def blob(self, commit: str, path: str) -> str:
        return self.git("rev-parse", f"{commit}:{path}")

    def msg(self, op: str, *, article: str | None = None, gate: str | None = None) -> str:
        lines = [f"test {op}", "", f"Writing-Workflow: {op}"]
        if article is not None:
            lines.append(f"Writing-Article: {article}")
        if gate is not None:
            lines.append(f"Writing-Gate: {gate}")
        return "\n".join(lines)

    def read_state(self) -> dict:
        return json.loads((self.root / self.state_path).read_text(encoding="utf-8"))

    def write_state(self, state: dict) -> None:
        path = self.root / self.state_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def modify_article(self, body: str) -> None:
        (self.root / self.article_path).write_text(f"---\ntitle: test\n---\n\n{body}\n", encoding="utf-8")

    def commit(self, message: str) -> str:
        self.git("add", ".")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def make_state(self, entry: str) -> dict:
        ids = VW.gate_ids(VW.load_registry(self.root))
        idx = ids.index(entry)
        return {
            "schema_version": 4,
            "workflow": "write-commentary",
            "article_id": self.article_id,
            "article_path": self.article_path,
            "cycle": 1,
            "entry_gate": entry,
            "skipped_by_user": ids[:idx],
            "current_gate": entry,
            "completed": [],
            "status": "in_progress",
            "article_revision": self.blob("HEAD", self.article_path),
        }

    def advance_state_one_gate(self, *, wrong_revision: str | None = None, skip_to: str | None = None) -> None:
        before = self.read_state()
        ids = VW.gate_ids(VW.load_registry(self.root))
        after = json.loads(json.dumps(before))
        if skip_to is not None:
            after["current_gate"] = skip_to
            after["completed"] = before["completed"] + [before["current_gate"]]
        else:
            idx = ids.index(before["current_gate"])
            after["completed"] = before["completed"] + [before["current_gate"]]
            if idx + 1 < len(ids):
                after["current_gate"] = ids[idx + 1]
                after["status"] = "in_progress"
            else:
                after["current_gate"] = None
                after["status"] = "complete"
        after["article_revision"] = wrong_revision or self.git("hash-object", "--", self.article_path)
        self.write_state(after)

    # Stage C regression coverage

    def test_ordinary_article_edit_without_trailer_is_ignored(self):
        self.modify_article("ordinary edit")
        commit = self.commit("ordinary article edit")
        self.assertEqual(VC.validate_commit(self.root, commit), [])

    def test_valid_gate_same_commit_passes(self):
        self.modify_article("G1 result")
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))
        self.assertEqual(VC.validate_commit(self.root, commit), [])

    def test_stale_parent_article_rejects_subsequent_gate_commit(self):
        self.modify_article("external ordinary edit")
        self.commit("ordinary article edit")

        self.modify_article("G1 result after stale baseline")
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))

        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("STATE STALE" in x for x in failures))

    def test_state_only_gate_advance_fails(self):
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("does not allow NO_CHANGE" in x for x in failures))

    def test_article_only_gate_commit_fails(self):
        self.modify_article("article only")
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("must change bound state" in x for x in failures))

    def test_wrong_resulting_article_revision_fails(self):
        self.modify_article("G1 result")
        self.advance_state_one_gate(wrong_revision="1" * 40)
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("does not equal resulting commit article blob" in x for x in failures))

    def test_multi_gate_transition_fails(self):
        self.modify_article("bad skip")
        self.advance_state_one_gate(skip_to="G3")
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(failures)

    def test_gate_trailer_must_match_completed_gate(self):
        self.modify_article("G1 result")
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G2"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("does not equal gate completed" in x for x in failures))

    def test_unknown_workflow_trailer_fails(self):
        self.modify_article("edit")
        commit = self.commit(self.msg("mystery", article=self.article_id))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("unknown Writing-Workflow" in x for x in failures))

    def test_missing_article_trailer_fails(self):
        self.modify_article("edit")
        commit = self.commit(self.msg("gate", gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("requires Writing-Article" in x for x in failures))

    def test_non_gate_with_gate_trailer_fails(self):
        self.modify_article("edit")
        commit = self.commit(self.msg("reconcile", article=self.article_id, gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("Writing-Gate is allowed only" in x for x in failures))

    # Selectable-entry commit coverage

    def test_init_from_g4_commit_passes(self):
        other_id = "20261003-g4-init"
        other_path = f"articles/{other_id}/index.md"
        p = self.root / other_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("initial\n", encoding="utf-8")
        self.commit("add G4 article")
        ids = VW.gate_ids(VW.load_registry(self.root))
        state = {
            "schema_version": 4,
            "workflow": "write-commentary",
            "article_id": other_id,
            "article_path": other_path,
            "cycle": 1,
            "entry_gate": "G4",
            "skipped_by_user": ids[:3],
            "current_gate": "G4",
            "completed": [],
            "status": "in_progress",
            "article_revision": self.blob("HEAD", other_path),
        }
        sp = self.root / f".writing-state/write-commentary/{other_id}.json"
        sp.parent.mkdir(parents=True, exist_ok=True)
        sp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        commit = self.commit(self.msg("init", article=other_id))
        self.assertEqual(VC.validate_commit(self.root, commit), [])

    def test_g7_gate_completes(self):
        state = self.read_state()
        state["entry_gate"] = "G7"
        state["skipped_by_user"] = ["G1","G2","G3","G4","G5","G6"]
        state["current_gate"] = "G7"
        state["completed"] = []
        self.write_state(state)
        self.commit("prepare G7")
        self.modify_article("G7 result")
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G7"))
        self.assertEqual(VC.validate_commit(self.root, commit), [])
        self.assertIsNone(self.read_state()["current_gate"])
        self.assertEqual(self.read_state()["completed"], ["G7"])
        self.assertEqual(self.read_state()["status"], "complete")

    def test_g8_gate_trailer_fails(self):
        self.modify_article("invalid G8")
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G8"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("requires valid Writing-Gate" in x for x in failures))

    def test_synthetic_comment_only_gate_change_fails(self):
        before = (self.root / self.article_path).read_text(encoding="utf-8")
        (self.root / self.article_path).write_text(before + "\n<!-- synthetic -->\n", encoding="utf-8")
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("substantive bound article change" in x for x in failures))

    def test_lastmod_only_gate_change_fails(self):
        (self.root / self.article_path).write_text("---\ntitle: test\nlastmod: 2026-10-04T12:00:00\n---\n\nInitial.\n", encoding="utf-8")
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G1"))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("substantive bound article change" in x for x in failures))

    def test_non_g1_gate_same_commit_passes(self):
        state = self.read_state()
        state["entry_gate"] = "G4"
        state["skipped_by_user"] = ["G1", "G2", "G3"]
        state["current_gate"] = "G4"
        state["completed"] = []
        self.write_state(state)
        self.commit("prepare G4 state")

        self.modify_article("G4 result")
        self.advance_state_one_gate()
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G4"))
        self.assertEqual(VC.validate_commit(self.root, commit), [])

    def test_wrong_transition_after_selected_entry_fails(self):
        state = self.read_state()
        state["entry_gate"] = "G4"
        state["skipped_by_user"] = ["G1", "G2", "G3"]
        state["current_gate"] = "G4"
        state["completed"] = []
        self.write_state(state)
        self.commit("prepare G4 state")

        self.modify_article("bad G4 skip")
        after = self.read_state()
        after["completed"] = ["G4"]
        after["current_gate"] = "G6"
        after["article_revision"] = self.git("hash-object", "--", self.article_path)
        self.write_state(after)
        commit = self.commit(self.msg("gate", article=self.article_id, gate="G4"))
        self.assertTrue(VC.validate_commit(self.root, commit))

    def test_start_cycle_rebases_after_complete_state_human_edit(self):
        state = self.read_state()
        state["entry_gate"] = "G7"
        state["skipped_by_user"] = ["G1","G2","G3","G4","G5","G6"]
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        self.write_state(state)
        self.commit("complete cycle")

        old_snapshot = self.read_state()["article_revision"]
        self.modify_article("human edit after complete")
        human_commit = self.commit("ordinary human edit")
        current_blob = self.blob(human_commit, self.article_path)
        self.assertNotEqual(old_snapshot, current_blob)

        after = self.read_state()
        after["cycle"] = 2
        after["entry_gate"] = "G6"
        after["skipped_by_user"] = ["G1","G2","G3","G4","G5"]
        after["completed"] = []
        after["current_gate"] = "G6"
        after["status"] = "in_progress"
        after["article_revision"] = current_blob
        self.write_state(after)
        start_commit = self.commit(self.msg("start-cycle", article=self.article_id))
        self.assertEqual(VC.validate_commit(self.root, start_commit), [])
        self.assertEqual(self.blob(human_commit, self.article_path), self.blob(start_commit, self.article_path))

    def test_reconcile_commit_requires_confirmation_trailer(self):
        self.modify_article("external edit before reconcile")
        external = self.commit("external article edit")
        state = self.read_state()
        state["article_revision"] = self.blob(external, self.article_path)
        self.write_state(state)
        commit = self.commit(self.msg("reconcile", article=self.article_id))
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("Writing-Recovery: confirmed" in x for x in failures))

    def test_complete_reconcile_commit_fails(self):
        state = self.read_state()
        state["entry_gate"] = "G7"
        state["skipped_by_user"] = ["G1","G2","G3","G4","G5","G6"]
        state["current_gate"] = None
        state["completed"] = ["G7"]
        state["status"] = "complete"
        self.write_state(state)
        self.commit("complete cycle")

        self.modify_article("ordinary human edit after complete")
        human_commit = self.commit("ordinary human edit")
        current_blob = self.blob(human_commit, self.article_path)

        state = self.read_state()
        self.assertNotEqual(state["article_revision"], current_blob)
        state["article_revision"] = current_blob
        self.write_state(state)
        commit = self.commit(self.msg("reconcile", article=self.article_id) + "\nWriting-Recovery: confirmed")
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("reconcile requires in_progress state" in x for x in failures))

    def test_repository_schema_migration_without_trailer_is_ignored(self):
        state = self.read_state()
        state["article_revision"] = state["article_revision"]
        self.write_state(state)
        # Ensure a real state-file change while remaining a non-runtime commit.
        path = self.root / self.state_path
        path.write_text(path.read_text(encoding="utf-8").replace('"cycle": 1', '"cycle": 1'), encoding="utf-8")
        self.modify_article("ordinary migration companion edit")
        commit = self.commit("repository schema migration")
        self.assertEqual(VC.validate_commit(self.root, commit), [])


if __name__ == "__main__":
    unittest.main()
