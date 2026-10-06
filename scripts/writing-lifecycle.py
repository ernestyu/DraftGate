#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

VW = load_module("validate_writing_workflow_lifecycle", ROOT / "scripts" / "validate-writing-workflow.py")
WS = load_module("writing_state_lifecycle", ROOT / "scripts" / "writing-state.py")

class LifecycleError(RuntimeError):
    pass

def git(root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and proc.returncode:
        raise LifecycleError(proc.stdout.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()

def ensure_clean(root: Path) -> None:
    if git(root, "status", "--porcelain"):
        raise LifecycleError("working tree must be clean")

def current_branch(root: Path) -> str:
    return git(root, "branch", "--show-current")


def has_origin(root: Path) -> bool:
    return subprocess.run(["git", "remote", "get-url", "origin"], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def fetch_origin(root: Path) -> None:
    git(root, "fetch", "origin", "main", "--tags")


def sync_main_for_begin(root: Path) -> str:
    if not has_origin(root):
        return git(root, "rev-parse", "main")
    fetch_origin(root)
    local_main = git(root, "rev-parse", "main")
    remote_main = git(root, "rev-parse", "refs/remotes/origin/main")
    if local_main == remote_main:
        return local_main
    if git(root, "merge-base", local_main, remote_main) == local_main:
        git(root, "merge", "--ff-only", "refs/remotes/origin/main")
        return remote_main
    raise LifecycleError("local main diverges from origin/main")


def current_main_for_closeout(root: Path) -> str:
    if not has_origin(root):
        return git(root, "rev-parse", "main")
    fetch_origin(root)
    return git(root, "rev-parse", "refs/remotes/origin/main")


def remote_branch_exists(root: Path, name: str) -> bool:
    if not has_origin(root):
        return False
    proc = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", f"refs/heads/{name}"], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc.returncode == 0


def push_begin_branch(root: Path, name: str) -> None:
    if has_origin(root):
        git(root, "push", "-u", "origin", f"HEAD:refs/heads/{name}")


def validate_closeout_candidate(root: Path, commit: str) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate-writing-commit.py"),
            "--root",
            str(root),
            "--commit",
            commit,
        ],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.returncode != 0:
        raise LifecycleError(
            "closeout candidate failed commit validation:\n" + proc.stdout.strip()
        )


def publish_closeout(root: Path, tag: str, closeout_commit: str, current_main: str, branch: str) -> None:
    if not has_origin(root):
        git(root, "update-ref", "refs/heads/main", closeout_commit, current_main)
        return

    # Evidence is published before main; an already-correct remote tag is idempotent.
    git(root, "push", "origin", f"refs/tags/{tag}:refs/tags/{tag}")
    if closeout_commit != current_main:
        git(root, "push", "origin", f"{closeout_commit}:refs/heads/main")
    remote_main = git(root, "ls-remote", "origin", "refs/heads/main").split()[0]
    if remote_main != closeout_commit:
        raise LifecycleError("remote main verification failed")
    git(root, "update-ref", "refs/heads/main", closeout_commit)

def branch_name(article_id: str, cycle: int) -> str:
    if not VW.valid_article_id(article_id) or cycle < 1:
        raise LifecycleError("invalid article/cycle")
    return f"writing/{article_id}/c{cycle}"

def evidence_name(article_id: str, cycle: int) -> str:
    return f"writing-evidence/{article_id}/c{cycle}"

def archive_rel(article_id: str, cycle: int) -> str:
    return f".writing-state/archive/write-commentary/{article_id}/c{cycle}.json"

def active_rel(article_id: str) -> str:
    return f".writing-state/write-commentary/{article_id}.json"

def article_rel(article_id: str) -> str:
    return f"articles/{article_id}/index.md"

def ref_exists(root: Path, ref: str) -> bool:
    return subprocess.run(["git", "show-ref", "--verify", "--quiet", ref], cwd=root).returncode == 0

def blob_or_none(root: Path, commit: str, path: str) -> str | None:
    proc = subprocess.run(["git", "rev-parse", f"{commit}:{path}"], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return proc.stdout.strip() if proc.returncode == 0 else None

def text_at(root: Path, commit: str, path: str) -> str:
    return git(root, "show", f"{commit}:{path}")

def g7_terminal(root: Path, commit: str, article_id: str) -> bool:
    msg = git(root, "show", "-s", "--format=%B", commit)
    return all(x in msg for x in (
        "Writing-Workflow: gate",
        f"Writing-Article: {article_id}",
        "Writing-Gate: G7",
    ))

def latest_cycle(root: Path, article_id: str) -> int:
    archive = root / ".writing-state" / "archive" / "write-commentary" / article_id
    values = []
    if archive.is_dir():
        for p in archive.glob("c*.json"):
            try:
                values.append(int(p.stem[1:]))
            except ValueError:
                pass
    return max(values, default=0)

def begin(article_id: str, entry_gate: str, title: str | None, root: Path) -> dict:
    ensure_clean(root)
    if current_branch(root) != "main":
        raise LifecycleError("begin must start from main")
    archive_failures = VW.validate_archives(root, VW.load_registry(root))
    if archive_failures:
        raise LifecycleError("; ".join(archive_failures))
    main_base = sync_main_for_begin(root)
    if (root / active_rel(article_id)).exists():
        raise LifecycleError("active state already exists")
    previous_cycle = latest_cycle(root, article_id)
    cycle = previous_cycle + 1
    name = branch_name(article_id, cycle)
    if ref_exists(root, f"refs/heads/{name}"):
        raise LifecycleError("writing branch already exists")
    git(root, "switch", "-c", name)

    article = root / article_rel(article_id)
    if not article.exists():
        article.parent.mkdir(parents=True, exist_ok=True)
        article.write_text(f"# {title or article_id}\n", encoding="utf-8")
        git(root, "add", article_rel(article_id))
        git(root, "commit", "-m", "Bootstrap article")

    if previous_cycle == 0:
        state = WS.init_state(article_id, article_rel(article_id), root, entry_gate)
        op = "init"
    else:
        state = WS.start_cycle(article_id, root, entry_gate)
        op = "start-cycle"
    git(root, "add", active_rel(article_id))
    git(root, "commit", "-m", f"Begin writing cycle {cycle}\n\nWriting-Workflow: {op}\nWriting-Article: {article_id}\nWriting-Main-Base: {main_base}")
    push_begin_branch(root, name)
    return {"branch": name, "cycle": cycle, "main_base_commit": main_base, "state": state}

def ensure_evidence(root: Path, article_id: str, cycle: int, target: str) -> str:
    tag = evidence_name(article_id, cycle)
    ref = f"refs/tags/{tag}"
    if ref_exists(root, ref):
        existing = git(root, "rev-parse", f"{ref}^{{}}")
        if existing != target:
            raise LifecycleError("evidence ref exists with different target")
        return tag
    git(root, "tag", "-a", tag, target, "-m", f"DraftGate evidence {article_id} cycle {cycle}")
    if git(root, "rev-parse", f"{ref}^{{}}") != target:
        raise LifecycleError("evidence ref verification failed")
    return tag

def changed_since(root: Path, base: str, tip: str) -> set[str]:
    out = git(root, "diff", "--name-only", base, tip)
    return {x for x in out.splitlines() if x}

def durable_paths(root: Path, article_id: str, base: str, tip: str) -> set[str]:
    allowed = {article_rel(article_id)}
    changed = changed_since(root, base, tip)
    for path in changed:
        if path.startswith(".writing-rules/") and path.endswith(".md"):
            allowed.add(path)
    ignored = {active_rel(article_id)}
    unexpected = changed - allowed - ignored
    if unexpected:
        raise LifecycleError("unauthorized durable cycle paths: " + ", ".join(sorted(unexpected)))
    return {p for p in allowed if blob_or_none(root, base, p) != blob_or_none(root, tip, p)}

def detect_conflicts(root: Path, base: str, main: str, branch: str, paths: set[str]) -> None:
    for path in sorted(paths):
        b = blob_or_none(root, base, path)
        m = blob_or_none(root, main, path)
        w = blob_or_none(root, branch, path)
        if m != b and w != b and m != w:
            raise LifecycleError(f"closeout conflict: {path}")

def build_closeout_tree(root: Path, main: str, branch: str, article_id: str, cycle: int, paths: set[str], archived_json: str) -> str:
    with tempfile.NamedTemporaryFile(prefix="draftgate-index-", delete=False) as tmp:
        index = tmp.name
    os.unlink(index)
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = index
    def igit(*args: str) -> str:
        proc = subprocess.run(["git", *args], cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode:
            raise LifecycleError(proc.stdout.strip())
        return proc.stdout.strip()
    try:
        igit("read-tree", main)
        for path in sorted(paths):
            blob = blob_or_none(root, branch, path)
            if blob is None:
                igit("update-index", "--force-remove", path)
            else:
                igit("update-index", "--add", "--cacheinfo", "100644", blob, path)
        archive_blob = subprocess.check_output(["git", "hash-object", "-w", "--stdin"], cwd=root, input=archived_json, text=True).strip()
        igit("update-index", "--add", "--cacheinfo", "100644", archive_blob, archive_rel(article_id, cycle))
        igit("update-index", "--force-remove", active_rel(article_id))
        return igit("write-tree")
    finally:
        if os.path.exists(index):
            os.unlink(index)

def verify_archive(root: Path, main_commit: str, evidence_target: str, article_id: str, cycle: int) -> None:
    ar = archive_rel(article_id, cycle)
    sr = active_rel(article_id)
    archived = json.loads(text_at(root, main_commit, ar))
    historical = json.loads(text_at(root, evidence_target, sr))
    if archived != historical:
        raise LifecycleError("archive/evidence state mismatch")
    if archived.get("status") != "complete" or archived.get("current_gate") is not None:
        raise LifecycleError("archive is not terminal complete state")
    if archived.get("cycle") != cycle or archived.get("article_id") != article_id:
        raise LifecycleError("archive identity mismatch")
    if archived.get("article_revision") != blob_or_none(root, evidence_target, archived["article_path"]):
        raise LifecycleError("archive article_revision mismatch")

def recorded_main_base(root: Path, article_id: str, terminal: str) -> str:
    log = git(root, "log", terminal, "--format=%H%x00%B%x00")
    chunks = log.split("\x00")
    for i in range(0, len(chunks) - 1, 2):
        message = chunks[i + 1]
        if f"Writing-Article: {article_id}" not in message:
            continue
        for line in message.splitlines():
            if line.startswith("Writing-Main-Base: "):
                value = line.split(": ", 1)[1].strip()
                if VW.BLOB_SHA_RE.fullmatch(value):
                    return value
                raise LifecycleError("invalid recorded main base")
    raise LifecycleError("writing cycle is missing recorded main base")


def closeout(article_id: str, ci_passed_for: str, root: Path) -> dict:
    ensure_clean(root)
    state = WS.read_state(article_id, root)
    if state.get("status") != "complete":
        raise LifecycleError("closeout requires complete state")
    cycle = state["cycle"]
    expected_branch = branch_name(article_id, cycle)
    if current_branch(root) != expected_branch:
        raise LifecycleError(f"closeout must run on {expected_branch}")
    terminal = git(root, "rev-parse", "HEAD")
    if ci_passed_for != terminal:
        raise LifecycleError("--ci-passed-for must equal terminal G7 commit")
    if not g7_terminal(root, terminal, article_id):
        raise LifecycleError("terminal commit must be G7 completion")

    base = recorded_main_base(root, article_id, terminal)
    if git(root, "merge-base", base, terminal) != base:
        raise LifecycleError("recorded main base is not an ancestor of terminal commit")
    current_main = current_main_for_closeout(root)
    paths = durable_paths(root, article_id, base, terminal)
    detect_conflicts(root, base, current_main, terminal, paths)

    base_active = blob_or_none(root, base, active_rel(article_id))
    main_active = blob_or_none(root, current_main, active_rel(article_id))
    if main_active != base_active:
        raise LifecycleError("closeout conflict: active state changed on main")

    expected_archive = text_at(root, terminal, active_rel(article_id))
    existing_archive = blob_or_none(root, current_main, archive_rel(article_id, cycle))
    if existing_archive is not None:
        expected_blob = subprocess.check_output(["git", "hash-object", "-w", "--stdin"], cwd=root, input=expected_archive, text=True).strip()
        if existing_archive != expected_blob:
            raise LifecycleError("historical archive already exists with different content")
    tag = ensure_evidence(root, article_id, cycle, terminal)

    historical_state = expected_archive
    tree = build_closeout_tree(root, current_main, terminal, article_id, cycle, paths, historical_state)
    current_tree = git(root, "rev-parse", f"{current_main}^{{tree}}")
    if tree == current_tree:
        closeout_commit = current_main
    else:
        msg = f"Close writing cycle {cycle}\n\nWriting-Workflow: closeout\nWriting-Article: {article_id}\nWriting-Cycle: {cycle}"
        closeout_commit = git(root, "commit-tree", tree, "-p", current_main, "-m", msg)

    if blob_or_none(root, closeout_commit, active_rel(article_id)) is not None:
        raise LifecycleError("closeout retained active state")
    verify_archive(root, closeout_commit, terminal, article_id, cycle)
    validate_closeout_candidate(root, closeout_commit)

    publish_closeout(root, tag, closeout_commit, current_main, expected_branch)
    git(root, "switch", "main")
    if remote_branch_exists(root, expected_branch):
        git(root, "push", "origin", "--delete", expected_branch)
    git(root, "branch", "-D", expected_branch)
    return {"main_commit": closeout_commit, "evidence": tag, "archive": archive_rel(article_id, cycle), "deleted_branch": expected_branch}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("begin")
    p.add_argument("--article-id", required=True)
    p.add_argument("--from", dest="entry_gate", default="G1")
    p.add_argument("--title")

    p = sub.add_parser("closeout")
    p.add_argument("--article-id", required=True)
    p.add_argument("--ci-passed-for", required=True)

    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        result = begin(args.article_id, args.entry_gate, args.title, root) if args.command == "begin" else closeout(args.article_id, args.ci_passed_for, root)
    except (LifecycleError, WS.StateError, json.JSONDecodeError) as exc:
        print("WRITING_LIFECYCLE_FAIL", exc)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
