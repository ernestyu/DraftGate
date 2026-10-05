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


VW = load_module("vw_no_change_test", REPO_ROOT / "scripts" / "validate-writing-workflow.py")
VC = load_module("vc_no_change_test", REPO_ROOT / "scripts" / "validate-writing-commit.py")


class WritingNoChangeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.tmp.name)
        self.article_id = "20261004-no-change"
        self.article_path = f"articles/{self.article_id}/index.md"
        self.state_path = f".writing-state/write-commentary/{self.article_id}.json"

        src = REPO_ROOT / "docs" / "writing" / "commentary"
        shutil.copytree(src, self.root / "docs" / "writing" / "commentary", dirs_exist_ok=True)

        article = self.root / self.article_path
        article.parent.mkdir(parents=True, exist_ok=True)
        article.write_text("---\ntitle: test\n---\n\nInitial.\n", encoding="utf-8")

        self.git("init")
        self.git("config", "user.name", "NO_CHANGE Test")
        self.git("config", "user.email", "no-change@example.invalid")
        self.git("config", "gc.auto", "0")
        self.git("config", "maintenance.auto", "false")
        self.git("add", ".")
        self.git("commit", "-m", "initial")

        self.write_state(self.make_state("G1"))
        self.git("add", self.state_path)
        self.git("commit", "-m", self.msg("init", "G1", include_gate=False))

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True, stderr=subprocess.STDOUT).strip()

    def msg(self, op: str, gate: str, include_gate: bool = True) -> str:
        lines = [f"test {op}", "", f"Writing-Workflow: {op}", f"Writing-Article: {self.article_id}"]
        if include_gate:
            lines.append(f"Writing-Gate: {gate}")
        return "\n".join(lines)

    def article_blob(self, rev: str = "HEAD") -> str:
        return self.git("rev-parse", f"{rev}:{self.article_path}")

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
            "article_revision": self.article_blob(),
        }

    def read_state(self) -> dict:
        return json.loads((self.root / self.state_path).read_text(encoding="utf-8"))

    def write_state(self, state: dict) -> None:
        p = self.root / self.state_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def set_allow(self, gate: str, allowed: bool) -> None:
        p = self.root / "docs" / "writing" / "commentary" / "gate-registry.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        for item in data["gates"]:
            if item["id"] == gate:
                item["allow_no_change"] = allowed
        p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        self.git("add", str(p.relative_to(self.root)))
        self.git("commit", "-m", f"fixture allow {gate}={allowed}")

    def advance_state_only(self, wrong_revision: str | None = None, skip_to: str | None = None) -> None:
        before = self.read_state()
        ids = VW.gate_ids(VW.load_registry(self.root))
        after = json.loads(json.dumps(before))
        idx = ids.index(before["current_gate"])
        after["completed"] = before["completed"] + [before["current_gate"]]
        if skip_to is not None:
            after["current_gate"] = skip_to
        elif idx + 1 < len(ids):
            after["current_gate"] = ids[idx + 1]
        else:
            after["current_gate"] = None
            after["status"] = "complete"
        if wrong_revision is not None:
            after["article_revision"] = wrong_revision
        self.write_state(after)

    def commit_gate(self, gate: str) -> str:
        self.git("add", ".")
        self.git("commit", "-m", self.msg("gate", gate))
        return self.git("rev-parse", "HEAD")

    def test_production_registry_authorizes_g5_only(self):
        data = VW.load_registry(REPO_ROOT)
        self.assertEqual([g["id"] for g in data["gates"]], [f"G{i}" for i in range(1, 8)])
        by_id = {g["id"]: g for g in data["gates"]}
        self.assertTrue(by_id["G5"]["allow_no_change"])
        for gate_id in ("G1","G2","G3","G4","G6","G7"):
            with self.subTest(gate_id=gate_id):
                self.assertFalse(by_id[gate_id]["allow_no_change"])

    def test_missing_allow_no_change_is_invalid(self):
        p = self.root / "docs" / "writing" / "commentary" / "gate-registry.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        del data["gates"][0]["allow_no_change"]
        p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        failures = VW.validate_registry(self.root)
        self.assertTrue(any("allow_no_change must be boolean" in x for x in failures))

    def test_no_change_forbidden_gate_fails(self):
        self.advance_state_only()
        commit = self.commit_gate("G1")
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("does not allow NO_CHANGE" in x for x in failures))

    def test_no_change_allowed_gate_passes(self):
        self.set_allow("G1", True)
        self.advance_state_only()
        commit = self.commit_gate("G1")
        self.assertEqual(VC.validate_commit(self.root, commit), [])

    def test_no_change_extra_path_fails(self):
        self.set_allow("G1", True)
        self.advance_state_only()
        extra = self.root / "extra.txt"
        extra.write_text("extra\n", encoding="utf-8")
        commit = self.commit_gate("G1")
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("changed_paths must equal bound state file only" in x for x in failures))

    def test_no_change_stale_baseline_fails(self):
        self.set_allow("G1", True)
        article = self.root / self.article_path
        article.write_text("---\ntitle: changed\n---\n\nExternal.\n", encoding="utf-8")
        self.git("add", self.article_path)
        self.git("commit", "-m", "external edit")
        self.advance_state_only()
        commit = self.commit_gate("G1")
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("STATE STALE" in x for x in failures))

    def test_no_change_multi_gate_transition_fails(self):
        self.set_allow("G1", True)
        self.advance_state_only(skip_to="G3")
        commit = self.commit_gate("G1")
        self.assertTrue(VC.validate_commit(self.root, commit))

    def test_no_change_article_revision_change_fails(self):
        self.set_allow("G1", True)
        self.advance_state_only(wrong_revision="1" * 40)
        commit = self.commit_gate("G1")
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("article_revision" in x for x in failures))

    def test_changed_branch_still_requires_substantive_change(self):
        self.set_allow("G1", True)
        article = self.root / self.article_path
        article.write_text(article.read_text(encoding="utf-8") + "\n<!-- synthetic -->\n", encoding="utf-8")
        self.advance_state_only(wrong_revision=self.git("hash-object", "--", self.article_path))
        commit = self.commit_gate("G1")
        failures = VC.validate_commit(self.root, commit)
        self.assertTrue(any("substantive bound article change" in x for x in failures))

    def test_terminal_no_change_fixture_passes_without_production_authorization(self):
        self.set_allow("G7", True)
        state = self.read_state()
        state["entry_gate"] = "G7"
        state["skipped_by_user"] = ["G1","G2","G3","G4","G5","G6"]
        state["current_gate"] = "G7"
        state["completed"] = []
        state["article_revision"] = self.article_blob()
        self.write_state(state)
        self.git("add", self.state_path)
        self.git("commit", "-m", "prepare synthetic terminal fixture")
        self.advance_state_only()
        commit = self.commit_gate("G7")
        self.assertEqual(VC.validate_commit(self.root, commit), [])
        self.assertEqual(self.read_state()["status"], "complete")


if __name__ == "__main__":
    unittest.main()
