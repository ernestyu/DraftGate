# DraftGate

**English** | [简体中文](README.zh-CN.md)

A Git-native, staged editorial workflow for AI-assisted long-form writing.

DraftGate turns one Markdown article into a stateful G1→G7 process. The language model handles judgment and editing; Git records document revisions; deterministic validators enforce gate order, freshness, and legal state transitions.

The built-in editorial rules are intentionally language-neutral. They focus on reasoning, structure, evidence, paragraph responsibility, and mechanical repetition rather than a particular author's voice. The same workflow can be used for Chinese or English writing.

## Why

Large writing prompts often mix thesis selection, scope control, structure, evidence boundaries, paragraph organization, and final language cleanup in one execution. DraftGate separates those responsibilities into narrow gates and gives each gate an explicit contract.

Built-in gates:

1. G1 — Main Question & Thesis
2. G2 — Scope & Branch Control
3. G3 — Argument Architecture
4. G4 — Reader Accessibility
5. G5 — Claim & Evidence Boundary
6. G6 — Paragraph Organization
7. G7 — Final Language & Pattern Audit

## Artifact layout

```text
articles/
  20261005-example-topic/
    index.md

.writing-state/
  write-commentary/
    20261005-example-topic.json
```

There is no Hugo, CMS, front matter, cover image, or publishing dependency.

## Requirements

- Git
- Python 3.10+
- Optional: GitHub Actions for remote enforcement

No Docker, database, model server, or self-hosted runner is required.

## Quick start

Clone the repository, then create an article:

```bash
./writing bootstrap --article-id 20261005-example-topic --title "Provisional Title"
git add articles/20261005-example-topic/index.md
git commit -m "Bootstrap article"
```

Initialize the workflow:

```bash
./writing init --article-id 20261005-example-topic
git add .writing-state/write-commentary/20261005-example-topic.json
git commit -m $'Initialize writing workflow\n\nWriting-Workflow: init\nWriting-Article: 20261005-example-topic'
```

Then work with an AI agent one gate at a time.

## Using with an AI agent

A repository-aware agent should read `AGENTS.md` first. For an agent that does not automatically read repository instructions, use a prompt like:

```text
Read AGENTS.md and docs/writing/commentary/workflow.md.
Work on article 20261005-example-topic.
Read its state file, load only the current gate and declared resources,
execute exactly that gate, update the article and state according to the workflow,
commit with the required Writing-* trailers, then stop.
```

After each gate, request the next one explicitly:

```text
execute G1
execute G2
...
```

The agent should not pre-run later gates. Human discussion and decisions remain part of the workflow; DraftGate is an editorial control system, not a one-shot article generator.

## Local commands

```bash
./writing bootstrap --article-id <id> [--title "..."]
./writing init --article-id <id> [--from Gx]
./writing show --article-id <id>
./writing validate --article-id <id>
./writing advance --article-id <id>
./writing reopen --article-id <id>
./writing start-cycle --article-id <id> [--from Gx]
./writing reconcile --article-id <id>
./writing test
```

`advance` updates the state file from the current working-tree article. A valid CHANGED gate commit must contain both the article change and the matching state transition.

A gate commit uses trailers such as:

```text
Complete G1

Writing-Workflow: gate
Writing-Article: 20261005-example-topic
Writing-Gate: G1
```

## GitHub Actions

The included workflow runs on `ubuntu-latest` and validates:

- workflow registry and resources;
- all writing unit tests;
- tracked state freshness;
- workflow-controlled commits and trailers.

GitHub Actions is optional. The same validators run locally with:

```bash
./writing test
```

## Core invariants

- one invocation = one gate;
- no gate skipping after the selected entry gate;
- stale in-progress state fails closed;
- gate completion advances exactly one gate;
- article + state are committed together for substantive changes;
- NO_CHANGE is gate-authorized, never implicit;
- reopen can restore only the immediately previous gate;
- completed cycles never restart automatically.

## Scope

The public rules deliberately avoid language-specific phrase bans, fixed paragraph-length targets, mandatory first-person policies, and a prescribed authorial voice. Those belong in project-specific or personal extensions, not in the core workflow.

## License

MIT.
