# Agent Instructions

This repository is a plain-Markdown AI writing workflow.

When working on an article:

1. Read `docs/writing/commentary/workflow.md`.
2. Read the bound state at `.writing-state/write-commentary/<article_id>.json`.
3. Load only the current Gate Core rule and resources declared by `gate-registry.json`, plus `.writing-rules/Gx.md` for the current Gate if it exists.
4. Custom Rules from other Gates must not participate in execution, editing, evaluation, or PASS decisions. They may be read only when the user explicitly requests rule maintenance.
5. Core rules override Custom Rules. If they conflict, apply Core, ignore the conflicting Custom Rule for that execution, inform the user, and do not modify workflow state merely because of the conflict.

The repository ships `.writing-rules/G1.md` through `.writing-rules/G7.md` as empty scaffolding. They form the persistent writing-profile layer. Do not turn ordinary article edits into Persistent Custom Rules. Update a Gate file only when the user explicitly asks to keep, change, or remove a preference as a long-term rule.
6. Execute exactly one gate per invocation.
7. Do not redesign earlier frozen decisions unless the user explicitly reopens or starts a correction cycle.
8. For CHANGED gate completion, commit the article and state together with the required trailers.
9. Stop after the gate transition.

Do not introduce Hugo, CMS, site-generation, cover-image, or publishing behavior into the core workflow.


## Lifecycle authority

Normal article work should run on `writing/<article-id>/c<cycle>`, not directly on `main`. Do not rebase the writing branch or merge `main` into it during the cycle; closeout uses the recorded `Writing-Main-Base` to compare the cycle against current `main`.

For a new or archived article cycle, prefer `./writing begin ...`. In GitHub-backed normal use, stop after the G7 Gate commit. A successful CI run for that exact terminal G7 commit triggers automatic closeout; do not ask the user to run a closeout command. `./writing closeout --article-id <id> --ci-passed-for <G7_SHA>` is reserved for local/recovery use.

After every Gate commit on a writing branch, push that branch so GitHub Actions can validate the exact Gate commit. Automatic closeout is fail-closed: it revalidates the exact terminal branch/state identity, constructs and validates the closeout candidate, publishes the evidence tag, pushes the high-level closeout commit to `main`, verifies remote main, and deletes the remote writing branch last. Do not delete a writing branch before evidence ref, main durable result, and cycle-aware archive are verified.

Evidence refs are write-once by policy: an existing same-target ref is accepted; a different-target ref must stop the operation.

Do not auto-run `reconcile`. Report STATE STALE, explain that reconcile accepts external edits without validating Gate authority, and require explicit user confirmation. A reconcile recovery commit must include `Writing-Workflow: reconcile`, `Writing-Article: <id>`, and `Writing-Recovery: confirmed`.

Repository maintenance must not modify an in-progress bound article or active state except through a lifecycle operation explicitly authorized by the workflow.
