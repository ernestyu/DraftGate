# Agent Instructions

This repository is a plain-Markdown AI writing workflow.

When working on an article:

1. Read `docs/writing/commentary/workflow.md`.
2. Read the bound state at `.writing-state/write-commentary/<article_id>.json`.
3. Load only the current Gate Core rule and resources declared by `gate-registry.json`, plus `.writing-rules/Gx.md` for the current Gate if it exists.
4. Custom Rules from other Gates must not participate in execution, editing, evaluation, or PASS decisions. They may be read only when the user explicitly requests rule maintenance.
5. Core rules override Custom Rules. If they conflict, apply Core, ignore the conflicting Custom Rule for that execution, inform the user, and do not modify workflow state merely because of the conflict.
6. Execute exactly one gate per invocation.
7. Do not redesign earlier frozen decisions unless the user explicitly reopens or starts a correction cycle.
8. For CHANGED gate completion, commit the article and state together with the required trailers.
9. Stop after the gate transition.

Do not introduce Hugo, CMS, site-generation, cover-image, or publishing behavior into the core workflow.
