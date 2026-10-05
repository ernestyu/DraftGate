# Write Commentary Workflow

This file is the execution controller for the built-in `write-commentary` workflow.

The repository is the runtime authority. Articles are plain Markdown artifacts at:

```text
articles/<article_id>/index.md
```

## Goal

Reduce reader effort without reducing idea density.

## Pre-G1 brainstorm

Before state initialization, users may hold an open brainstorm with the Agent.

Pre-G1 is outside the state machine:

- no state file;
- no Gate ID;
- no PASS / FAIL;
- no transition;
- free exploration is allowed.

Use Pre-G1 to make the rough topic, motivation, and direction clear enough that G1 can make a real commitment. Do not model Pre-G1 as G0.

## Entry assessment

Before starting a workflow or a new cycle, the agent may recommend the earliest relevant gate:

- main question / thesis → G1
- scope / branch control → G2
- argument architecture / incomplete first draft → G3
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
3. Read the validated state and current gate Gx.
4. Load only Gx Core rule and Gx declared Core resources.
5. If `.writing-rules/Gx.md` exists, load that file as Gx Persistent Custom Rules.
6. Do not load Custom Rules from any other Gate into execution, editing, evaluation, or PASS / FAIL decisions.
7. If the user explicitly requests maintenance of another Gate's Custom Rule, that file may be read only for rule maintenance; it still does not participate in the current Gate.
8. Write authorized edits directly to `articles/<article_id>/index.md`.
9. Apply freshness, same-commit, and transition rules.
10. Stop.

Core always has higher authority than Custom Rules. If a Custom Rule conflicts with Core:

```text
Core applies
→ conflicting Custom Rule is ignored for this execution
→ explicitly inform the user
→ do not modify workflow state merely because of the conflict
```

## Persistent Custom Rules

Persistent Custom Rules are optional per-Gate user preferences stored as:

```text
.writing-rules/G1.md
...
.writing-rules/G7.md
```

Users are not expected to edit these files manually. The intended interaction is conversational: the user explicitly asks the Agent to keep, change, or remove a long-term preference, and the Agent maintains the corresponding Gate file.

Do not automatically turn one-off article edits into persistent rules.

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

## New cycles and free editing

When `status = complete`, DraftGate releases the article. The user may edit the Markdown freely with an Agent or by hand; those edits do not automatically become Persistent Custom Rules.

For systematic rework, start a new cycle from the earliest affected Gate:

```text
thesis → G1
scope → G2
architecture or draft development → G3
reader accessibility → G4
claim / evidence → G5
paragraph organization → G6
language / pattern cleanup → G7
```

Use:

```bash
./writing start-cycle --article-id <id> --from Gx
```

Repeated cycles are normal. DraftGate does not assume one G1→G7 pass creates a permanently final article.

## Boundary

This project edits Markdown only. It does not publish, build a website, generate covers, manage CMS metadata, or deploy content.


## Repository lifecycle

Normal cycles run on `writing/<article-id>/c<cycle>`. Gate commits remain intact on that branch. The lifecycle begin commit records the exact starting `main` commit as `Writing-Main-Base`; the writing branch must not be rebased or merged with `main` during the cycle.

After G7 and CI PASS, closeout:

1. verifies the terminal G7 commit;
2. creates or idempotently verifies `writing-evidence/<article-id>/c<cycle>`;
3. applies only authorized durable cycle changes onto current `main`;
4. stores the exact completed state at `.writing-state/archive/write-commentary/<article-id>/c<cycle>.json`;
5. removes the completed active-state representation from the main closeout tree;
6. preserves durable Persistent Custom Rules changes;
7. deletes the writing branch only after all verification passes.

If current `main` changed since the writing branch base, non-conflicting changes are preserved. A conflict on the article, Custom Rules, or another authorized durable path stops closeout without deleting the writing branch.

Evidence refs are policy-level write-once. They may not be moved or reused for a different target.

Archived state is historical. It remains schema v4 but is not resumable and is not freshness-checked against later article versions. A later cycle reads the latest archive without modifying it, creates a new active state with cycle + 1, and uses the current main article blob as `article_revision`.

`reconcile` is exceptional recovery only and requires explicit confirmation. It rebinds revision identity; it does not validate whether external edits complied with Gate authority.
