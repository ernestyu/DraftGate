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


VW = load_module("vw_lifecycle_test", REPO_ROOT / "scripts" / "validate-writing-workflow.py")
WS = load_module("ws_lifecycle_test", REPO_ROOT / "scripts" / "writing-state.py")
WL = load_module("wl_lifecycle_test", REPO_ROOT / "scripts" / "writing-lifecycle.py")
VC = load_module("vc_lifecycle_test", REPO_ROOT / "scripts" / "validate-writing-commit.py")


class WritingLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(REPO_ROOT / "docs" / "writing" / "commentary", self.root / "docs" / "writing" / "commentary")
        (self.root / ".writing-rules").mkdir(parents=True)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Lifecycle Test")
        self.git("config", "user.email", "lifecycle@example.invalid")
        (self.root / "README.md").write_text("base\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "base")
        self.article_id = "20261005-lifecycle-test"

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True, stderr=subprocess.STDOUT).strip()

    def write(self, rel: str, text: str) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def complete_g7(self, *, custom_rule: bool = False) -> str:
        self.write(f"articles/{self.article_id}/index.md", "# Final\n\nComplete.\n")
        if custom_rule:
            self.write(".writing-rules/G7.md", "# G7 Persistent Custom Rules\n\n- restrained tone\n")
        after = WS.advance_state(self.article_id, self.root)
        self.assertEqual(after["status"], "complete")
        self.git("add", ".")
        self.git("commit", "-m", f"Complete G7\n\nWriting-Workflow: gate\nWriting-Article: {self.article_id}\nWriting-Gate: G7")
        return self.git("rev-parse", "HEAD")

    def begin_g7(self) -> dict:
        return WL.begin(self.article_id, "G7", "Lifecycle Test", self.root)

    def test_branch_naming(self):
        self.assertEqual(WL.branch_name("abc", 2), "writing/abc/c2")
        self.assertEqual(WL.evidence_name("abc", 2), "writing-evidence/abc/c2")

    def test_begin_creates_one_cycle_branch_and_records_base(self):
        base = self.git("rev-parse", "main")
        result = self.begin_g7()
        self.assertEqual(result["branch"], f"writing/{self.article_id}/c1")
        self.assertEqual(result["cycle"], 1)
        self.assertEqual(result["main_base_commit"], base)
        self.assertEqual(self.git("branch", "--show-current"), result["branch"])
        with self.assertRaisesRegex(WL.LifecycleError, "main"):
            WL.begin("other", "G1", None, self.root)

    def test_evidence_is_write_once_and_idempotent(self):
        self.begin_g7()
        target = self.complete_g7()
        name = WL.ensure_evidence(self.root, self.article_id, 1, target)
        self.assertEqual(WL.ensure_evidence(self.root, self.article_id, 1, target), name)
        self.git("commit", "--allow-empty", "-m", "different")
        with self.assertRaisesRegex(WL.LifecycleError, "different target"):
            WL.ensure_evidence(self.root, self.article_id, 1, self.git("rev-parse", "HEAD"))

    def test_closeout_preserves_current_main_and_custom_rules(self):
        result = self.begin_g7()
        branch = result["branch"]
        self.git("switch", "main")
        self.write("unrelated.txt", "main advanced\n")
        self.git("add", "unrelated.txt")
        self.git("commit", "-m", "advance main")
        self.git("switch", branch)
        terminal = self.complete_g7(custom_rule=True)
        out = WL.closeout(self.article_id, terminal, self.root)
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertIn("unrelated.txt", self.git("ls-tree", "-r", "--name-only", "main"))
        self.assertIn(f"articles/{self.article_id}/index.md", self.git("ls-tree", "-r", "--name-only", "main"))
        self.assertIn(".writing-rules/G7.md", self.git("ls-tree", "-r", "--name-only", "main"))
        self.assertIn(WL.archive_rel(self.article_id, 1), self.git("ls-tree", "-r", "--name-only", "main"))
        self.assertNotIn(WL.active_rel(self.article_id), self.git("ls-tree", "-r", "--name-only", "main"))
        self.assertFalse(WL.ref_exists(self.root, f"refs/heads/{branch}"))
        self.assertEqual(self.git("rev-parse", f"refs/tags/{out['evidence']}^{{}}"), terminal)
        self.assertEqual(VW.validate_archives(self.root, VW.load_registry(self.root)), [])

    def test_closeout_conflicting_article_stops_and_preserves_branch(self):
        result = self.begin_g7()
        branch = result["branch"]
        self.git("switch", "main")
        self.write(f"articles/{self.article_id}/index.md", "# Main conflicting edit\n")
        self.git("add", ".")
        self.git("commit", "-m", "main article conflict")
        self.git("switch", branch)
        terminal = self.complete_g7()
        with self.assertRaisesRegex(WL.LifecycleError, "closeout conflict"):
            WL.closeout(self.article_id, terminal, self.root)
        self.assertTrue(WL.ref_exists(self.root, f"refs/heads/{branch}"))
        self.assertEqual(self.git("branch", "--show-current"), branch)

    def test_closeout_conflicting_custom_rule_stops(self):
        result = self.begin_g7()
        branch = result["branch"]
        self.git("switch", "main")
        self.write(".writing-rules/G7.md", "main rule\n")
        self.git("add", ".writing-rules/G7.md")
        self.git("commit", "-m", "main custom rule")
        self.git("switch", branch)
        self.write(".writing-rules/G7.md", "branch rule\n")
        terminal = self.complete_g7(custom_rule=False)
        with self.assertRaisesRegex(WL.LifecycleError, "closeout conflict"):
            WL.closeout(self.article_id, terminal, self.root)
        self.assertTrue(WL.ref_exists(self.root, f"refs/heads/{branch}"))

    def test_closeout_requires_exact_terminal_ci_attestation(self):
        self.begin_g7()
        terminal = self.complete_g7()
        with self.assertRaisesRegex(WL.LifecycleError, "ci-passed-for"):
            WL.closeout(self.article_id, "0" * 40, self.root)

    def test_archive_is_cycle_aware_and_new_cycle_reads_without_mutation(self):
        self.begin_g7()
        terminal = self.complete_g7()
        WL.closeout(self.article_id, terminal, self.root)
        archive = self.root / WL.archive_rel(self.article_id, 1)
        before = archive.read_bytes()
        result = WL.begin(self.article_id, "G3", None, self.root)
        self.assertEqual(result["cycle"], 2)
        state = WS.read_state(self.article_id, self.root)
        self.assertEqual(state["cycle"], 2)
        self.assertEqual(state["entry_gate"], "G3")
        self.assertEqual(state["completed"], [])
        self.assertEqual(state["article_revision"], VW.git_blob_at_head(self.root, state["article_path"]))
        self.assertEqual(archive.read_bytes(), before)
        self.assertEqual(result["branch"], f"writing/{self.article_id}/c2")

    def test_archive_validation_detects_content_mismatch(self):
        self.begin_g7()
        terminal = self.complete_g7()
        WL.closeout(self.article_id, terminal, self.root)
        archive = self.root / WL.archive_rel(self.article_id, 1)
        data = json.loads(archive.read_text(encoding="utf-8"))
        data["entry_gate"] = "G6"
        archive.write_text(json.dumps(data) + "\n", encoding="utf-8")
        failures = VW.validate_archives(self.root, VW.load_registry(self.root))
        self.assertTrue(any("mismatch" in x for x in failures))

    def test_archive_is_not_freshness_checked_against_later_article(self):
        self.begin_g7()
        terminal = self.complete_g7()
        WL.closeout(self.article_id, terminal, self.root)
        self.write(f"articles/{self.article_id}/index.md", "# Later human edit\n")
        self.git("add", ".")
        self.git("commit", "-m", "later edit")
        self.assertEqual(VW.validate_archives(self.root, VW.load_registry(self.root)), [])

    def test_archived_state_is_not_active(self):
        self.begin_g7()
        terminal = self.complete_g7()
        WL.closeout(self.article_id, terminal, self.root)
        with self.assertRaisesRegex(WS.StateError, "state not found"):
            WS.read_state(self.article_id, self.root)

    def test_unauthorized_cycle_path_blocks_closeout(self):
        self.begin_g7()
        self.write("random.txt", "not durable\n")
        self.git("add", "random.txt")
        self.git("commit", "-m", "unauthorized")
        terminal = self.complete_g7()
        with self.assertRaisesRegex(WL.LifecycleError, "unauthorized durable"):
            WL.closeout(self.article_id, terminal, self.root)


    def test_closeout_candidate_validation_failure_prevents_publish(self):
        result = self.begin_g7()
        branch = result["branch"]
        terminal = self.complete_g7()
        main_before = self.git("rev-parse", "main")

        original = WL.validate_closeout_candidate
        def fail_validation(root, commit):
            raise WL.LifecycleError("forced closeout candidate validation failure")
        WL.validate_closeout_candidate = fail_validation
        try:
            with self.assertRaisesRegex(WL.LifecycleError, "forced closeout candidate validation failure"):
                WL.closeout(self.article_id, terminal, self.root)
        finally:
            WL.validate_closeout_candidate = original

        self.assertEqual(self.git("rev-parse", "main"), main_before)
        self.assertEqual(self.git("branch", "--show-current"), branch)
        self.assertTrue(WL.ref_exists(self.root, f"refs/heads/{branch}"))
        self.assertTrue(WL.ref_exists(self.root, f"refs/tags/{WL.evidence_name(self.article_id, 1)}"))

    def test_closeout_commit_and_evidence_history_validate(self):
        result = self.begin_g7()
        init_commit = self.git("rev-parse", "HEAD")
        terminal = self.complete_g7()
        out = WL.closeout(self.article_id, terminal, self.root)
        self.assertEqual(VC.validate_commit(self.root, out["main_commit"]), [])
        self.git("merge-base", "--is-ancestor", init_commit, f"refs/tags/{out['evidence']}^{{}}")

    def test_archive_based_start_cycle_commit_validates_and_keeps_c1(self):
        self.begin_g7()
        terminal = self.complete_g7()
        first = WL.closeout(self.article_id, terminal, self.root)
        c1_archive = self.root / WL.archive_rel(self.article_id, 1)
        c1_bytes = c1_archive.read_bytes()
        c1_tag = self.git("rev-parse", f"refs/tags/{first['evidence']}^{{}}")

        second = WL.begin(self.article_id, "G7", None, self.root)
        start_commit = self.git("rev-parse", "HEAD")
        self.assertEqual(VC.validate_commit(self.root, start_commit), [])
        terminal2 = self.complete_g7()
        WL.closeout(self.article_id, terminal2, self.root)

        self.assertTrue(c1_archive.is_file())
        self.assertTrue((self.root / WL.archive_rel(self.article_id, 2)).is_file())
        self.assertEqual(c1_archive.read_bytes(), c1_bytes)
        self.assertEqual(self.git("rev-parse", f"refs/tags/{first['evidence']}^{{}}"), c1_tag)

    def test_maintenance_cannot_delete_in_progress_state_or_bound_article(self):
        self.begin_g7()
        state_path = WL.active_rel(self.article_id)
        article_path = WL.article_rel(self.article_id)

        self.git("rm", state_path)
        self.git("commit", "-m", f"bad maintenance\n\nWriting-Workflow: maintenance\nWriting-Article: {self.article_id}\nWriting-Maintenance: temporary-artifact")
        failures = VC.validate_commit(self.root, "HEAD")
        self.assertTrue(any("in-progress active state" in x for x in failures))
        self.git("reset", "--hard", "HEAD^")

        self.git("rm", article_path)
        self.git("commit", "-m", f"bad maintenance\n\nWriting-Workflow: maintenance\nWriting-Article: {self.article_id}\nWriting-Maintenance: temporary-artifact")
        failures = VC.validate_commit(self.root, "HEAD")
        self.assertTrue(any("in-progress bound article" in x for x in failures))


if __name__ == "__main__":
    unittest.main()
