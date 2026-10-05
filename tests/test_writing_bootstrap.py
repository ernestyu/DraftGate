from __future__ import annotations

import importlib.util
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


WB = load_module("writing_bootstrap_test", REPO_ROOT / "scripts" / "bootstrap-writing-article.py")
WS = load_module("writing_state_bootstrap_test", REPO_ROOT / "scripts" / "writing-state.py")


class WritingBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        commentary = REPO_ROOT / "docs" / "writing" / "commentary"
        shutil.copytree(commentary, self.root / "docs" / "writing" / "commentary", dirs_exist_ok=True)
        (self.root / "docs" / "writing" / "ARTICLE_TEMPLATE.md").write_text("authority\n", encoding="utf-8")
        self.git("init")
        self.git("config", "user.name", "Bootstrap Test")
        self.git("config", "user.email", "bootstrap@example.invalid")
        self.git("add", ".")
        self.git("commit", "-m", "base")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True, stderr=subprocess.STDOUT).strip()

    def bootstrap(self):
        article_id = "20261005-ai-work"
        path = WB.bootstrap_article(self.root, article_id, "临时标题")
        return article_id, path

    def test_bootstrap_creates_plain_markdown_article(self):
        article_id, path = self.bootstrap()
        self.assertEqual(path, self.root / f"articles/{article_id}/index.md")
        self.assertEqual(path.read_text(encoding="utf-8"), "# 临时标题\n\n")

    def test_bootstrap_does_not_create_state(self):
        article_id, _ = self.bootstrap()
        self.assertFalse((self.root / f".writing-state/write-commentary/{article_id}.json").exists())

    def test_init_requires_committed_article(self):
        article_id, path = self.bootstrap()
        rel = str(path.relative_to(self.root))
        with self.assertRaisesRegex(WS.StateError, "committed HEAD"):
            WS.init_state(article_id, rel, self.root)
        self.git("add", rel)
        self.git("commit", "-m", "bootstrap article")
        state = WS.init_state(article_id, rel, self.root)
        self.assertEqual(state["schema_version"], 4)
        self.assertEqual(state["current_gate"], "G1")
        self.assertEqual(state["completed"], [])
        self.assertEqual(state["article_revision"], self.git("rev-parse", f"HEAD:{rel}"))

    def test_invalid_article_id_is_rejected(self):
        with self.assertRaisesRegex(WB.BootstrapError, "article-id"):
            WB.bootstrap_article(self.root, "../bad", "x")


if __name__ == "__main__":
    unittest.main()
