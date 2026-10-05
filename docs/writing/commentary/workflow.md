# Write Commentary Workflow

This file is the execution controller for the built-in `write-commentary` workflow.

The repository is the runtime authority. Articles are plain Markdown artifacts at:

```text
articles/<article_id>/index.md
```

## Goal

Reduce reader effort without reducing idea density.

## Entry assessment

Before starting a workflow or a new cycle, the agent may recommend the earliest relevant gate:

- main question / thesis → G1
- scope / branch control → G2
- argument architecture → G3
- reader accessibility → G4
- claim strength / evidence boundary → G5
- paragraph organization → G6
- final language / AI trace → G7

If several problems exist, recommend the earliest gate. A non-G1 entry requires explicit user confirmation.

## Execution contract

1. Gate order is fixed: G1 → G2 → G3 → G4 → G5 → G6 → G7.
2. New workflows and new cycles default to G1.
3. Gates before `entry_gate` are recorded in `skipped_by_user`, never as completed.
4. From `entry_gate`, execution proceeds sequentially through G7.
5. One invocation executes one gate only.
6. Do not pre-execute or complete later gates.
7. After a gate completes, persist article and state, then stop.
8. Resume from `current_gate`.
9. G7 is the only normal terminal gate.
10. Never start a new cycle automatically.

## Gate loading

1. Read `gate-registry.json`.
2. Load global resources.
3. Read the validated state and current gate.
4. Load only the current gate rule and its declared resources.
5. Write authorized edits directly to `articles/<article_id>/index.md`.
6. Apply freshness, same-commit, and transition rules.
7. Stop.

## Runtime state

State files live at:

```text
.writing-state/write-commentary/<article_id>.json
```

Schema v4 fields:

```text
schema_version
workflow
article_id
article_path
cycle
entry_gate
skipped_by_user
current_gate
completed
status
article_revision
```

`article_revision` is the Git blob SHA of the authoritative Markdown article.

## State commands

```text
init --from Gx
start-cycle --from Gx
reopen
reconcile
validate
show
advance
```

Omitting `--from` defaults to G1.

## Bootstrap

Create a plain Markdown article first:

```bash
./writing bootstrap --article-id 20261005-example-topic
```

This creates:

```text
articles/20261005-example-topic/index.md
```

with a provisional Markdown heading and no publishing-system metadata.

Bootstrap and state initialization are separate operations. Commit the article before initializing state so a committed blob exists.

## Authoritative working article

Each workflow binds exactly one article:

```text
articles/<article_id>/index.md
```

A normal gate completion has one of two outcomes:

```text
A. CHANGED
substantive authorized article change
+ exactly one gate transition
+ article and state in the same commit

B. gate-authorized NO_CHANGE
article already satisfies the gate
+ exactly one gate transition
+ state-only commit
```

NO_CHANGE is allowed only when `gate-registry.json` explicitly enables it.

## Ownership and freshness

While `status = in_progress`, the workflow owns the article baseline:

```text
article_revision == committed article blob
```

Mismatch is `STATE STALE` and fails closed.

When `status = complete`, the cycle releases the article. Normal human edits are allowed without reconciliation. `article_revision` remains the completion snapshot.

`start-cycle --from Gx` reacquires control using the current committed article blob.

## Reopen

Before the next gate runs, the user may explicitly reopen only the most recently completed gate.

Reopen:

- requires fresh `in_progress` state;
- changes state only;
- preserves article blob and `article_revision`;
- cannot roll back multiple gates;
- cannot be used after completion.

After completion, use a new cycle instead.

## Boundary

This project edits Markdown only. It does not publish, build a website, generate covers, manage CMS metadata, or deploy content.
