#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_writing_workflow", ROOT / "scripts" / "validate-writing-workflow.py")
VW = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VW
SPEC.loader.exec_module(VW)


class StateError(RuntimeError):
    pass


def state_path(article_id: str, root: Path = ROOT) -> Path:
    if not VW.valid_article_id(article_id):
        raise StateError("invalid article_id")
    return root / ".writing-state" / "write-commentary" / f"{article_id}.json"


def read_state(article_id: str, root: Path = ROOT) -> dict:
    path = state_path(article_id, root)
    if not path.is_file():
        raise StateError(f"state not found: {article_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_state(state: dict, root: Path = ROOT) -> Path:
    path = state_path(state["article_id"], root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def registry(root: Path) -> dict:
    return VW.load_registry(root)


def validate_or_raise(state: dict, root: Path) -> None:
    failures = VW.validate_state(registry(root), state)
    if failures:
        raise StateError("; ".join(failures))


def entry_prefix(entry_gate: str, root: Path) -> list[str]:
    ids = VW.gate_ids(registry(root))
    if entry_gate not in ids:
        raise StateError("invalid entry gate")
    return ids[:ids.index(entry_gate)]


def committed_article_blob(root: Path, article_path: str) -> str:
    try:
        return VW.git_blob_at_head(root, article_path)
    except RuntimeError as exc:
        raise StateError(str(exc)) from exc


def working_tree_article_blob(root: Path, article_path: str) -> str:
    article = root / article_path
    if not article.is_file():
        raise StateError("article file does not exist")
    try:
        value = subprocess.check_output(["git", "hash-object", "--", article_path], cwd=root, text=True, stderr=subprocess.STDOUT).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise StateError("failed to hash article working tree") from exc
    if not VW.BLOB_SHA_RE.fullmatch(value):
        raise StateError("working-tree article blob is invalid")
    return value


def ensure_fresh(state: dict, root: Path) -> str:
    actual = committed_article_blob(root, state["article_path"])
    failures = VW.validate_freshness(root, state)
    if failures:
        raise StateError("; ".join(failures))
    return actual


def init_state(article_id: str, article_path: str, root: Path = ROOT, entry_gate: str = "G1") -> dict:
    target = state_path(article_id, root)
    if target.exists():
        raise StateError(f"state already exists: {article_id}")
    expected = f"articles/{article_id}/index.md"
    if article_path != expected:
        raise StateError(f"article_path must equal {expected}")
    revision = committed_article_blob(root, article_path)
    state = {
        "schema_version": 4,
        "workflow": "write-commentary",
        "article_id": article_id,
        "article_path": article_path,
        "cycle": 1,
        "entry_gate": entry_gate,
        "skipped_by_user": entry_prefix(entry_gate, root),
        "current_gate": entry_gate,
        "completed": [],
        "status": "in_progress",
        "article_revision": revision,
    }
    validate_or_raise(state, root)
    atomic_write_state(state, root)
    return state


def validate_for_resume(article_id: str, root: Path = ROOT) -> dict:
    state = read_state(article_id, root)
    validate_or_raise(state, root)
    ensure_fresh(state, root)
    return state


def build_advanced_state(before: dict, new_revision: str, root: Path) -> dict:
    if before.get("status") != "in_progress":
        raise StateError("cannot advance a complete state")
    ids = VW.gate_ids(registry(root))
    idx = ids.index(before["current_gate"])
    after = json.loads(json.dumps(before))
    after["article_revision"] = new_revision
    after["completed"] = before["completed"] + [before["current_gate"]]
    if idx + 1 < len(ids):
        after["current_gate"] = ids[idx + 1]
    else:
        after["current_gate"] = None
        after["status"] = "complete"
    failures = VW.validate_transition(registry(root), before, after)
    if failures:
        raise StateError("; ".join(failures))
    return after


def advance_state(article_id: str, root: Path = ROOT) -> dict:
    before = read_state(article_id, root)
    validate_or_raise(before, root)
    ensure_fresh(before, root)
    after = build_advanced_state(before, working_tree_article_blob(root, before["article_path"]), root)
    atomic_write_state(after, root)
    return after


def reconcile_state(article_id: str, root: Path = ROOT) -> dict:
    before = read_state(article_id, root)
    validate_or_raise(before, root)
    if before.get("status") != "in_progress":
        raise StateError("reconcile requires in_progress state")
    after = json.loads(json.dumps(before))
    after["article_revision"] = committed_article_blob(root, before["article_path"])
    failures = VW.validate_reconcile(before, after, registry(root))
    if failures:
        raise StateError("; ".join(failures))
    atomic_write_state(after, root)
    return after


def reopen_state(article_id: str, root: Path = ROOT) -> dict:
    before = read_state(article_id, root)
    validate_or_raise(before, root)
    ensure_fresh(before, root)
    if before.get("status") != "in_progress":
        raise StateError("reopen requires in_progress state")
    completed = before.get("completed")
    if not completed:
        raise StateError("reopen requires at least one completed gate")
    after = json.loads(json.dumps(before))
    after["current_gate"] = completed[-1]
    after["completed"] = completed[:-1]
    failures = VW.validate_reopen(registry(root), before, after)
    if failures:
        raise StateError("; ".join(failures))
    atomic_write_state(after, root)
    return after


def start_cycle(article_id: str, root: Path = ROOT, entry_gate: str = "G1") -> dict:
    before = read_state(article_id, root)
    validate_or_raise(before, root)
    if before.get("status") != "complete":
        raise StateError("new cycle requires complete state and explicit start-cycle")
    current_revision = committed_article_blob(root, before["article_path"])
    after = json.loads(json.dumps(before))
    after["cycle"] = before["cycle"] + 1
    after["entry_gate"] = entry_gate
    after["skipped_by_user"] = entry_prefix(entry_gate, root)
    after["current_gate"] = entry_gate
    after["completed"] = []
    after["status"] = "in_progress"
    after["article_revision"] = current_revision
    validate_or_raise(after, root)
    atomic_write_state(after, root)
    return after


def emit(state: dict) -> None:
    print(json.dumps(state, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--article-id", required=True)
    p.add_argument("--article-path")
    p.add_argument("--from", dest="entry_gate", default="G1")

    p = sub.add_parser("show")
    p.add_argument("--article-id", required=True)

    p = sub.add_parser("validate")
    p.add_argument("--article-id", required=True)

    p = sub.add_parser("advance")
    p.add_argument("--article-id", required=True)

    p = sub.add_parser("reconcile")
    p.add_argument("--article-id", required=True)

    p = sub.add_parser("reopen")
    p.add_argument("--article-id", required=True)

    p = sub.add_parser("start-cycle")
    p.add_argument("--article-id", required=True)
    p.add_argument("--from", dest="entry_gate", default="G1")

    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        if args.command == "init":
            article_path = args.article_path or f"articles/{args.article_id}/index.md"
            state = init_state(args.article_id, article_path, root, args.entry_gate)
        elif args.command == "show":
            state = read_state(args.article_id, root)
        elif args.command == "validate":
            state = validate_for_resume(args.article_id, root)
        elif args.command == "advance":
            state = advance_state(args.article_id, root)
        elif args.command == "reconcile":
            state = reconcile_state(args.article_id, root)
        elif args.command == "reopen":
            state = reopen_state(args.article_id, root)
        elif args.command == "start-cycle":
            state = start_cycle(args.article_id, root, args.entry_gate)
        else:
            raise StateError("unknown command")
    except (StateError, json.JSONDecodeError) as exc:
        print(f"WRITING_STATE_FAIL {exc}")
        return 1
    emit(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
