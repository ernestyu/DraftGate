#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

WORKFLOW_DIR = PurePosixPath("docs/writing/commentary")
REGISTRY_REL = WORKFLOW_DIR / "gate-registry.json"
ARTICLE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
BLOB_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def valid_article_id(value: object) -> bool:
    return isinstance(value, str) and ARTICLE_ID_RE.fullmatch(value) is not None and value not in {".", ".."}


def normalize(base: PurePosixPath, rel: str) -> PurePosixPath:
    parts = []
    for part in (base / rel).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return PurePosixPath(*parts)


def load_registry(root: Path) -> dict:
    return json.loads((root / REGISTRY_REL).read_text(encoding="utf-8"))


def gate_ids(registry: dict) -> list[str]:
    return [gate["id"] for gate in registry["gates"]]


def validate_registry(root: Path) -> list[str]:
    failures: list[str] = []
    try:
        registry = load_registry(root)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load registry: {exc}"]
    if registry.get("workflow") != "write-commentary":
        failures.append("registry workflow must be write-commentary")
    if registry.get("execution_mode") != "sequential_single_gate":
        failures.append("execution_mode must be sequential_single_gate")
    gates = registry.get("gates")
    if not isinstance(gates, list) or not gates:
        return failures + ["gates must be a non-empty list"]
    expected = [f"G{i}" for i in range(1, 8)]
    ids = [gate.get("id") for gate in gates]
    if ids != expected:
        failures.append(f"gate order must be {expected}, got {ids}")
    global_resources = registry.get("global_resources", [])
    if not isinstance(global_resources, list):
        failures.append("global_resources must be a list")
    else:
        for rel in global_resources:
            if not isinstance(rel, str) or not (root / normalize(WORKFLOW_DIR, rel)).is_file():
                failures.append(f"global resource missing: {rel}")
    for gate in gates:
        if not isinstance(gate.get("allow_no_change"), bool):
            failures.append(f"{gate.get('id')} allow_no_change must be boolean")
        rule = gate.get("rule")
        if not isinstance(rule, str) or not (root / normalize(WORKFLOW_DIR, rule)).is_file():
            failures.append(f"{gate.get('id')} rule missing: {rule}")
        resources = gate.get("resources", [])
        if not isinstance(resources, list):
            failures.append(f"{gate.get('id')} resources must be a list")
            continue
        for rel in resources:
            if not isinstance(rel, str) or not (root / normalize(WORKFLOW_DIR, rel)).is_file():
                failures.append(f"{gate.get('id')} resource missing: {rel}")
    return failures


def validate_state(registry: dict, state: dict) -> list[str]:
    failures: list[str] = []
    ids = gate_ids(registry)
    if state.get("schema_version") != 4:
        failures.append("schema_version must be 4")
    if state.get("workflow") != "write-commentary":
        failures.append("state workflow must be write-commentary")

    article_id = state.get("article_id")
    if not valid_article_id(article_id):
        failures.append("article_id must be a safe non-empty slug and must not be '.' or '..'")
        article_id = None
    article_path = state.get("article_path")
    if not isinstance(article_path, str) or not article_path:
        failures.append("article_path must be a non-empty string")
    elif article_id is not None and article_path != f"articles/{article_id}/index.md":
        failures.append(f"article_path must equal articles/{article_id}/index.md")

    cycle = state.get("cycle")
    if not isinstance(cycle, int) or isinstance(cycle, bool) or cycle < 1:
        failures.append("cycle must be a positive integer")

    entry = state.get("entry_gate")
    skipped = state.get("skipped_by_user")
    completed = state.get("completed")
    current = state.get("current_gate")
    status = state.get("status")

    if entry not in ids:
        failures.append("entry_gate must be a valid gate")
        entry_idx = None
    else:
        entry_idx = ids.index(entry)

    if not isinstance(skipped, list):
        failures.append("skipped_by_user must be a list")
    elif entry_idx is not None and skipped != ids[:entry_idx]:
        failures.append("skipped_by_user must equal exact prefix before entry_gate")

    if not isinstance(completed, list):
        failures.append("completed must be a list")
    elif entry_idx is not None:
        if any(g in skipped for g in completed):
            failures.append("skipped_by_user and completed must not overlap")
        if status == "in_progress":
            if current not in ids:
                failures.append("in_progress state needs valid current_gate")
            else:
                current_idx = ids.index(current)
                if current_idx < entry_idx:
                    failures.append("current_gate cannot precede entry_gate")
                elif completed != ids[entry_idx:current_idx]:
                    failures.append("completed must be contiguous from entry_gate to before current_gate")
        elif status == "complete":
            if current is not None:
                failures.append("complete state current_gate must be null")
            if completed != ids[entry_idx:]:
                failures.append(f"complete state must contain every gate from entry_gate through {ids[-1]}")
        else:
            failures.append("status must be in_progress or complete")

    revision = state.get("article_revision")
    if not isinstance(revision, str) or not BLOB_SHA_RE.fullmatch(revision):
        failures.append("article_revision must be a 40-character lowercase Git blob SHA")

    allowed = {
        "schema_version", "workflow", "article_id", "article_path", "cycle",
        "entry_gate", "skipped_by_user", "current_gate", "completed",
        "status", "article_revision",
    }
    extra = sorted(set(state) - allowed)
    if extra:
        failures.append(f"unexpected state fields: {', '.join(extra)}")
    return failures


def validate_transition(registry: dict, before: dict, after: dict) -> list[str]:
    failures = validate_state(registry, before) + validate_state(registry, after)
    if failures:
        return failures
    for field in ("workflow", "article_id", "article_path", "cycle", "entry_gate", "skipped_by_user"):
        if before[field] != after[field]:
            return [f"{field} cannot change inside a gate transition"]
    if before == after:
        return ["gate transition must complete exactly one gate; no-op transition is invalid"]
    if before["status"] != "in_progress":
        return ["complete state cannot auto-start a new cycle"]

    ids = gate_ids(registry)
    idx = ids.index(before["current_gate"])
    expected_completed = before["completed"] + [before["current_gate"]]
    if idx + 1 < len(ids):
        if after["status"] != "in_progress" or after["current_gate"] != ids[idx + 1]:
            return [f"only legal next gate is {ids[idx + 1]}"]
        if after["completed"] != expected_completed:
            return ["transition may complete exactly one gate"]
    else:
        terminal = ids[-1]
        if after["status"] != "complete" or after["current_gate"] is not None:
            return [f"{terminal} may transition only to complete"]
        if after["completed"] != expected_completed:
            return [f"{terminal} completion must append only {terminal}"]
    return []


def validate_reopen(registry: dict, before: dict, after: dict) -> list[str]:
    failures = validate_state(registry, before) + validate_state(registry, after)
    if failures:
        return failures
    if before.get("status") != "in_progress" or after.get("status") != "in_progress":
        return ["reopen requires in_progress state before and after"]
    completed = before.get("completed")
    current = before.get("current_gate")
    ids = gate_ids(registry)
    if not isinstance(completed, list) or not completed:
        return ["reopen requires at least one completed gate"]
    if current not in ids:
        return ["reopen requires valid current_gate"]
    last = completed[-1]
    if last not in ids or ids.index(last) + 1 != ids.index(current):
        return ["reopen may restore only the gate directly preceding current_gate"]
    for field in ("schema_version", "workflow", "article_id", "article_path", "cycle", "entry_gate", "skipped_by_user", "article_revision"):
        if before.get(field) != after.get(field):
            failures.append(f"reopen must preserve {field}")
    if after.get("completed") != completed[:-1]:
        failures.append("reopen must remove exactly one final completed gate")
    if after.get("current_gate") != last:
        failures.append("reopen current_gate must equal removed final completed gate")
    return failures


def validate_reconcile(before: dict, after: dict, registry: dict) -> list[str]:
    failures = validate_state(registry, before) + validate_state(registry, after)
    if failures:
        return failures
    for field in ("workflow", "article_id", "article_path", "cycle", "entry_gate", "skipped_by_user", "current_gate", "completed", "status"):
        if before[field] != after[field]:
            failures.append(f"reconcile must preserve {field}")
    return failures


def git_blob_at_head(root: Path, article_path: str) -> str:
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{article_path}"], cwd=root, text=True, stderr=subprocess.STDOUT
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError("article is not present in committed HEAD") from exc
    if not BLOB_SHA_RE.fullmatch(value):
        raise RuntimeError("committed article blob is invalid")
    return value


def validate_freshness(root: Path, state: dict) -> list[str]:
    if state.get("status") == "complete":
        return []
    try:
        current = git_blob_at_head(root, state["article_path"])
    except (KeyError, RuntimeError) as exc:
        return [str(exc)]
    if state.get("article_revision") != current:
        return ["STATE STALE: article_revision does not match current committed article blob"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--state")
    parser.add_argument("--previous-state")
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    failures = validate_registry(root)
    registry = load_registry(root)
    if args.state:
        state = json.loads(Path(args.state).read_text(encoding="utf-8"))
        failures += validate_state(registry, state)
        if args.fresh:
            failures += validate_freshness(root, state)
        if args.previous_state:
            before = json.loads(Path(args.previous_state).read_text(encoding="utf-8"))
            failures += validate_transition(registry, before, state)
    if failures:
        for failure in failures:
            print("WRITING_WORKFLOW_FAIL", failure)
        return 1
    print("WRITING WORKFLOW — PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
