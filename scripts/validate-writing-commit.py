#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_writing_workflow",
    ROOT / "scripts" / "validate-writing-workflow.py",
)
VW = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VW
SPEC.loader.exec_module(VW)

TRAILER_KEYS = {"Writing-Workflow", "Writing-Article", "Writing-Gate", "Writing-Cycle", "Writing-Recovery", "Writing-Maintenance"}
WORKFLOW_OPS = {"init", "gate", "reconcile", "start-cycle", "reopen", "closeout", "maintenance"}
TRAILER_RE = re.compile(r"^(Writing-[A-Za-z-]+):\s*(.*?)\s*$")


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=root,
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def commit_message(root: Path, commit: str) -> str:
    return git(root, "show", "-s", "--format=%B", commit)


def parse_writing_trailers(message: str) -> tuple[dict[str, str], list[str]]:
    trailers: dict[str, str] = {}
    failures: list[str] = []
    for line in message.splitlines():
        match = TRAILER_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        if key not in TRAILER_KEYS:
            continue
        if key in trailers:
            failures.append(f"duplicate trailer: {key}")
        trailers[key] = value

    operation = trailers.get("Writing-Workflow")
    article = trailers.get("Writing-Article")
    gate = trailers.get("Writing-Gate")
    cycle = trailers.get("Writing-Cycle")
    recovery = trailers.get("Writing-Recovery")
    maintenance = trailers.get("Writing-Maintenance")

    if operation is None:
        if article is not None or gate is not None:
            failures.append("Writing-Article/Writing-Gate require Writing-Workflow")
        return trailers, failures

    if operation not in WORKFLOW_OPS:
        failures.append(f"unknown Writing-Workflow value: {operation}")
        return trailers, failures

    if not article:
        failures.append("workflow-controlled commit requires Writing-Article")
    elif not VW.valid_article_id(article):
        failures.append("Writing-Article must be a safe article_id")

    if operation == "gate":
        if gate not in {f"G{i}" for i in range(1, 8)}:
            failures.append("gate operation requires valid Writing-Gate")
    elif gate is not None:
        failures.append("Writing-Gate is allowed only for gate operation")

    if operation == "closeout":
        try:
            if int(cycle or "0") < 1:
                raise ValueError
        except ValueError:
            failures.append("closeout requires positive Writing-Cycle")
    elif cycle is not None:
        failures.append("Writing-Cycle is allowed only for closeout")

    if operation == "reconcile":
        if recovery != "confirmed":
            failures.append("reconcile requires Writing-Recovery: confirmed")
    elif recovery is not None:
        failures.append("Writing-Recovery is allowed only for reconcile")

    if operation == "maintenance":
        if maintenance not in {"temporary-artifact"}:
            failures.append("maintenance requires supported Writing-Maintenance category")
    elif maintenance is not None:
        failures.append("Writing-Maintenance is allowed only for maintenance")

    return trailers, failures


def state_rel(article_id: str) -> str:
    return f".writing-state/write-commentary/{article_id}.json"


def article_rel(article_id: str) -> str:
    return f"articles/{article_id}/index.md"


def file_exists_at(root: Path, commit: str, path: str) -> bool:
    try:
        git(root, "cat-file", "-e", f"{commit}:{path}")
        return True
    except subprocess.CalledProcessError:
        return False


def read_json_at(root: Path, commit: str, path: str) -> dict:
    return json.loads(git(root, "show", f"{commit}:{path}"))


def blob_at(root: Path, commit: str, path: str) -> str:
    return git(root, "rev-parse", f"{commit}:{path}")


def text_at(root: Path, commit: str, path: str) -> str:
    return git(root, "show", f"{commit}:{path}")


def normalize_gate_article(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        if re.match(r"^lastmod:\s*", line):
            continue
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
    return "\n".join(lines)


def parent_of(root: Path, commit: str) -> str | None:
    try:
        return git(root, "rev-parse", f"{commit}^")
    except subprocess.CalledProcessError:
        return None


def changed_paths(root: Path, commit: str) -> set[str]:
    parent = parent_of(root, commit)
    if parent is None:
        return set(git(root, "show", "--pretty=", "--name-only", commit).splitlines())
    return set(git(root, "diff", "--name-only", parent, commit).splitlines())


def validate_gate_commit(root: Path, commit: str, article_id: str, gate: str) -> list[str]:
    failures: list[str] = []
    parent = parent_of(root, commit)
    if parent is None:
        return ["gate commit requires a parent commit"]

    srel = state_rel(article_id)
    arel = article_rel(article_id)
    changed = changed_paths(root, commit)

    if srel not in changed:
        return ["gate commit must change bound state file"]

    if not file_exists_at(root, parent, srel) or not file_exists_at(root, commit, srel):
        return ["gate commit requires state before and after"]
    if not file_exists_at(root, parent, arel) or not file_exists_at(root, commit, arel):
        return ["gate commit requires bound article before and after"]

    before = read_json_at(root, parent, srel)
    after = read_json_at(root, commit, srel)

    parent_blob = blob_at(root, parent, arel)
    resulting_blob = blob_at(root, commit, arel)

    if before.get("article_revision") != parent_blob:
        return ["STATE STALE: before.article_revision does not match parent article blob"]

    registry = VW.load_registry(root)
    failures += VW.validate_transition(registry, before, after)
    if failures:
        return failures

    if before.get("article_id") != article_id or after.get("article_id") != article_id:
        failures.append("Writing-Article does not match bound state article_id")

    if before.get("current_gate") != gate:
        failures.append("Writing-Gate does not equal gate completed by transition")

    if after.get("article_path") != arel:
        failures.append("state article_path does not match Writing-Article")

    if after.get("article_revision") != resulting_blob:
        failures.append("state article_revision does not equal resulting commit article blob")

    article_changed = parent_blob != resulting_blob

    if article_changed:
        if arel not in changed:
            failures.append("CHANGED gate transaction must change bound article path")
            return failures
        before_text = text_at(root, parent, arel)
        after_text = text_at(root, commit, arel)
        if normalize_gate_article(before_text) == normalize_gate_article(after_text):
            failures.append("gate commit must include substantive bound article change")
        return failures

    gate_config = next((item for item in registry["gates"] if item.get("id") == gate), None)
    if gate_config is None:
        failures.append("Writing-Gate not found in registry")
        return failures
    if gate_config.get("allow_no_change") is not True:
        failures.append("gate does not allow NO_CHANGE")

    expected_changed = {srel}
    if changed != expected_changed:
        failures.append("NO_CHANGE changed_paths must equal bound state file only")

    if after.get("article_revision") != before.get("article_revision"):
        failures.append("NO_CHANGE must preserve article_revision")

    return failures

def validate_init_commit(root: Path, commit: str, article_id: str) -> list[str]:
    failures: list[str] = []
    srel = state_rel(article_id)
    arel = article_rel(article_id)
    parent = parent_of(root, commit)
    changed = changed_paths(root, commit)

    if srel not in changed:
        failures.append("init commit must create bound state file")
        return failures
    if not file_exists_at(root, commit, arel):
        failures.append("init requires bound article to exist")
        return failures
    if parent is not None and file_exists_at(root, parent, srel):
        failures.append("init commit must not overwrite existing state")
        return failures

    state = read_json_at(root, commit, srel)
    failures += VW.validate_state(VW.load_registry(root), state)
    if state.get("article_id") != article_id:
        failures.append("Writing-Article does not match state article_id")
    if state.get("completed") != [] or state.get("status") != "in_progress" or state.get("cycle") != 1:
        failures.append("init state must start cycle 1 with no completed gates")
    if state.get("current_gate") != state.get("entry_gate"):
        failures.append("init current_gate must equal entry_gate")
    if state.get("article_path") != arel:
        failures.append("init state article_path mismatch")
    if state.get("article_revision") != blob_at(root, commit, arel):
        failures.append("init article_revision must equal resulting article blob")
    return failures


def validate_reconcile_commit(root: Path, commit: str, article_id: str) -> list[str]:
    failures: list[str] = []
    parent = parent_of(root, commit)
    if parent is None:
        return ["reconcile commit requires parent"]
    srel = state_rel(article_id)
    arel = article_rel(article_id)
    changed = changed_paths(root, commit)

    if srel not in changed:
        failures.append("reconcile must change bound state file")
        return failures
    if arel in changed:
        failures.append("reconcile must not modify article content")
    before = read_json_at(root, parent, srel)
    after = read_json_at(root, commit, srel)
    if before.get("status") != "in_progress":
        failures.append("reconcile requires in_progress state")
        return failures
    failures += VW.validate_reconcile(before, after, VW.load_registry(root))
    if after.get("article_id") != article_id:
        failures.append("Writing-Article does not match state article_id")
    if after.get("article_revision") != blob_at(root, commit, arel):
        failures.append("reconcile article_revision must equal current article blob")
    return failures


def validate_reopen_commit(root: Path, commit: str, article_id: str) -> list[str]:
    failures: list[str] = []
    parent = parent_of(root, commit)
    if parent is None:
        return ["reopen commit requires parent"]

    srel = state_rel(article_id)
    arel = article_rel(article_id)
    changed = changed_paths(root, commit)

    if changed != {srel}:
        return ["reopen changed_paths must equal bound state file only"]
    if not file_exists_at(root, parent, srel) or not file_exists_at(root, commit, srel):
        return ["reopen requires state before and after"]
    if not file_exists_at(root, parent, arel) or not file_exists_at(root, commit, arel):
        return ["reopen requires bound article before and after"]

    before = read_json_at(root, parent, srel)
    after = read_json_at(root, commit, srel)
    registry = VW.load_registry(root)

    parent_blob = blob_at(root, parent, arel)
    resulting_blob = blob_at(root, commit, arel)

    if before.get("article_revision") != parent_blob:
        return ["STATE STALE: before.article_revision does not match parent article blob"]
    if parent_blob != resulting_blob:
        failures.append("reopen must not modify article content")

    failures += VW.validate_reopen(registry, before, after)

    if after.get("article_id") != article_id or before.get("article_id") != article_id:
        failures.append("Writing-Article does not match bound state article_id")
    if after.get("article_revision") != before.get("article_revision"):
        failures.append("reopen must preserve article_revision")
    if after.get("article_revision") != resulting_blob:
        failures.append("reopen article_revision must equal unchanged article blob")
    return failures


def archive_rel(article_id: str, cycle: int) -> str:
    return f".writing-state/archive/write-commentary/{article_id}/c{cycle}.json"


def validate_closeout_commit(root: Path, commit: str, article_id: str, cycle: int) -> list[str]:
    failures: list[str] = []
    parent = parent_of(root, commit)
    if parent is None:
        return ["closeout commit requires parent"]
    arel = article_rel(article_id)
    srel = state_rel(article_id)
    ar = archive_rel(article_id, cycle)
    changed = changed_paths(root, commit)
    if ar not in changed:
        failures.append("closeout must create archived state")
    if file_exists_at(root, commit, srel):
        failures.append("closeout must not retain active state")
    if not file_exists_at(root, commit, arel):
        failures.append("closeout must retain final article")
    if not file_exists_at(root, commit, ar):
        return failures
    archived = read_json_at(root, commit, ar)
    failures += VW.validate_state(VW.load_registry(root), archived)
    if archived.get("article_id") != article_id or archived.get("cycle") != cycle:
        failures.append("closeout archive identity mismatch")
    if archived.get("status") != "complete" or archived.get("current_gate") is not None:
        failures.append("closeout archive must be complete")
    return failures


def validate_maintenance_commit(root: Path, commit: str, article_id: str) -> list[str]:
    parent = parent_of(root, commit)
    if parent is None:
        return ["maintenance commit requires parent"]
    changed = changed_paths(root, commit)

    # Temporary-artifact maintenance is deletion-only.
    for path in changed:
        if not file_exists_at(root, parent, path) or file_exists_at(root, commit, path):
            return ["temporary-artifact maintenance may delete files only"]

    # No in-progress active state, or article bound by one, may be modified.
    for path in changed:
        if path.startswith(".writing-state/write-commentary/") and path.endswith(".json"):
            state = read_json_at(root, parent, path)
            if state.get("status") == "in_progress":
                return ["maintenance must not modify in-progress active state"]

    active_prefix = ".writing-state/write-commentary/"
    for path in git(root, "ls-tree", "-r", "--name-only", parent).splitlines():
        if not path.startswith(active_prefix) or not path.endswith(".json"):
            continue
        state = read_json_at(root, parent, path)
        if state.get("status") == "in_progress" and state.get("article_path") in changed:
            return ["maintenance must not modify in-progress bound article"]

    allowed = (
        "articles/",
        ".writing-state/write-commentary/",
        "tests/fixtures/",
    )
    if any(not path.startswith(allowed) for path in changed):
        return ["temporary-artifact maintenance path is not authorized"]
    return []


def validate_start_cycle_commit(root: Path, commit: str, article_id: str) -> list[str]:
    failures: list[str] = []
    parent = parent_of(root, commit)
    if parent is None:
        return ["start-cycle commit requires parent"]
    srel = state_rel(article_id)
    arel = article_rel(article_id)
    changed = changed_paths(root, commit)

    if srel not in changed:
        failures.append("start-cycle must create/change bound active state file")
        return failures
    if arel in changed:
        failures.append("start-cycle must not modify article content")

    after = read_json_at(root, commit, srel)
    registry = VW.load_registry(root)
    previous_cycle = after.get("cycle", 0) - 1
    if file_exists_at(root, parent, srel):
        before = read_json_at(root, parent, srel)
    else:
        ar = archive_rel(article_id, previous_cycle)
        if not file_exists_at(root, parent, ar):
            return ["start-cycle requires previous complete active state or cycle archive"]
        before = read_json_at(root, parent, ar)
        if ar in changed:
            failures.append("start-cycle must not modify historical archive")

    if VW.validate_state(registry, before):
        failures.append("start-cycle requires valid previous state")
    if before.get("status") != "complete" or before.get("current_gate") is not None:
        failures.append("start-cycle requires complete previous state")
    if after.get("cycle") != before.get("cycle", 0) + 1:
        failures.append("start-cycle must increment cycle by one")
    for field in ("workflow", "article_id", "article_path"):
        if after.get(field) != before.get(field):
            failures.append(f"start-cycle must preserve {field}")
    if after.get("completed") != [] or after.get("status") != "in_progress":
        failures.append("start-cycle must reset completed gates and status")
    if after.get("current_gate") != after.get("entry_gate"):
        failures.append("start-cycle current_gate must equal entry_gate")
    failures += VW.validate_state(registry, after)
    if after.get("article_id") != article_id:
        failures.append("Writing-Article does not match state article_id")
    if after.get("article_revision") != blob_at(root, commit, arel):
        failures.append("start-cycle requires fresh article_revision")
    return failures


def validate_commit(root: Path, commit: str) -> list[str]:
    trailers, failures = parse_writing_trailers(commit_message(root, commit))
    if failures:
        return failures

    operation = trailers.get("Writing-Workflow")
    if operation is None:
        return []

    article_id = trailers["Writing-Article"]
    if operation == "gate":
        return validate_gate_commit(root, commit, article_id, trailers["Writing-Gate"])
    if operation == "init":
        return validate_init_commit(root, commit, article_id)
    if operation == "reconcile":
        return validate_reconcile_commit(root, commit, article_id)
    if operation == "reopen":
        return validate_reopen_commit(root, commit, article_id)
    if operation == "start-cycle":
        return validate_start_cycle_commit(root, commit, article_id)
    if operation == "closeout":
        return validate_closeout_commit(root, commit, article_id, int(trailers["Writing-Cycle"]))
    if operation == "maintenance":
        return validate_maintenance_commit(root, commit, article_id)
    return [f"unsupported workflow operation: {operation}"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    failures = validate_commit(root, args.commit)
    if failures:
        for failure in failures:
            print("WRITING_COMMIT_FAIL", failure)
        return 1

    print("WRITING COMMIT — PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
