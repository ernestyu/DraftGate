from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "writing-auto-closeout.yml"


class WritingAutoCloseoutWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_runs_only_after_writing_ci_workflow_run(self):
        self.assertIn("workflow_run:", self.text)
        self.assertIn("- Writing Workflow CI", self.text)
        self.assertIn("types:", self.text)
        self.assertIn("- completed", self.text)

    def test_requires_successful_same_repo_writing_branch_push(self):
        self.assertIn("github.event.workflow_run.conclusion == 'success'", self.text)
        self.assertIn("github.event.workflow_run.event == 'push'", self.text)
        self.assertIn("startsWith(github.event.workflow_run.head_branch, 'writing/')", self.text)
        self.assertIn("github.event.workflow_run.head_repository.full_name == github.repository", self.text)

    def test_revalidates_exact_remote_head_before_closeout(self):
        self.assertIn('actual_sha="$(git rev-parse HEAD)"', self.text)
        self.assertIn('remote_sha="$(git ls-remote origin', self.text)
        self.assertIn('remote_sha" != "$EXPECTED_SHA', self.text)

    def test_requires_terminal_g7_complete_state(self):
        self.assertIn('"$gate" != "G7"', self.text)
        self.assertIn('state.get("status") != "complete"', self.text)
        self.assertIn('state.get("current_gate") is not None', self.text)
        self.assertIn('expected_branch="writing/$article/c$cycle"', self.text)

    def test_closeout_receives_exact_validated_sha(self):
        self.assertIn('./writing closeout', self.text)
        self.assertIn('--ci-passed-for "$VALIDATED_SHA"', self.text)

    def test_write_permission_is_isolated_to_closeout_workflow(self):
        self.assertIn("permissions:\n  contents: write", self.text)


if __name__ == "__main__":
    unittest.main()
