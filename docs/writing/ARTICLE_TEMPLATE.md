# Plain Markdown Article Artifact

The project uses one stable artifact shape:

```text
articles/<article_id>/index.md
```

## Rules

- One article = one directory.
- The authoritative article body is always `index.md`.
- `article_id` must be a safe slug containing letters, digits, dots, underscores, or hyphens.
- No front matter is required.
- No publishing metadata is required.
- No image, cover, CMS, or site-generator convention is part of the workflow.
- Other files may be added beside `index.md` by users, but v1 runtime logic binds only `index.md`.

A bootstrapped article starts as:

```markdown
# Provisional Title
```

The writing workflow may then edit the Markdown body gate by gate.
