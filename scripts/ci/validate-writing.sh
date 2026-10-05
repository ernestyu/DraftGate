#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

echo "== Validate writing registry =="
python3 scripts/validate-writing-workflow.py .

echo "== Run writing unit and Git-backed tests =="
python3 -m unittest discover -s tests -p 'test_writing*.py' -v

echo "== Validate tracked writing states =="
state_count=0
while IFS= read -r -d '' state_file; do
  state_count=$((state_count + 1))
  python3 scripts/validate-writing-workflow.py . --state "$state_file" --fresh
done < <(find .writing-state/write-commentary -maxdepth 1 -type f -name '*.json' -print0 | sort -z)
echo "tracked writing states validated: $state_count"

echo "== Validate workflow-controlled commits =="
before="${WRITING_CI_BEFORE:-}"
after="${WRITING_CI_AFTER:-HEAD}"

zero_sha="0000000000000000000000000000000000000000"
history_window="${WRITING_CI_HISTORY_WINDOW:-8}"
commits=()
declare -A seen=()

add_commit() {
  local commit="$1"
  [[ -z "$commit" ]] && return
  if [[ -z "${seen[$commit]+x}" ]]; then
    commits+=("$commit")
    seen["$commit"]=1
  fi
}

# Always re-validate a small recent history window. This makes CI self-healing:
# if GitHub fails to create a run for one or more pushes, a later push will
# automatically validate those missed commits without user intervention.
while IFS= read -r commit; do
  add_commit "$commit"
done < <(git rev-list --reverse --max-count="$history_window" "$after")

# Also validate every commit introduced by the current push, even when a push
# contains more commits than the self-healing history window.
if [[ -n "$before" && "$before" != "$zero_sha" ]] && git cat-file -e "$before^{commit}" 2>/dev/null; then
  while IFS= read -r commit; do
    add_commit "$commit"
  done < <(git rev-list --reverse "$before..$after")
else
  add_commit "$after"
fi

if [[ "${#commits[@]}" -eq 0 ]]; then
  echo "no commits to validate"
else
  for commit in "${commits[@]}"; do
    echo "validate commit: $commit"
    python3 scripts/validate-writing-commit.py --root . --commit "$commit"
  done
fi

echo "WRITING CI — PASS"
