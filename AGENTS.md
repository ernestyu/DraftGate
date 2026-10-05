# Agent Instructions

This repository is a plain-Markdown AI writing workflow.

When working on an article:

1. Read `docs/writing/commentary/workflow.md`.
2. Read the bound state at `.writing-state/write-commentary/<article_id>.json`.
3. Load only the current gate rule and resources declared by `gate-registry.json`.
4. Execute exactly one gate per invocation.
5. Do not redesign earlier frozen decisions unless the user explicitly reopens or starts a correction cycle.
6. For CHANGED gate completion, commit the article and state together with the required trailers.
7. Stop after the gate transition.

Do not introduce Hugo, CMS, site-generation, cover-image, or publishing behavior into the core workflow.
