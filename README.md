# DraftGate

**English** | [简体中文](README.zh-CN.md)

[![Writing Workflow CI](https://github.com/ernestyu/DraftGate/actions/workflows/writing-workflow-ci.yml/badge.svg)](https://github.com/ernestyu/DraftGate/actions/workflows/writing-workflow-ci.yml)

A Git-native, staged editorial workflow for AI-assisted long-form writing.

DraftGate turns one Markdown article into a stateful G1→G7 process. The language model handles judgment and editing; Git records document revisions; deterministic validators enforce gate order, freshness, and legal state transitions.

DraftGate Core is intentionally author-neutral by default. It focuses on reasoning, structure, evidence, paragraph responsibility, and mechanical repetition rather than shipping one author's voice. DraftGate also has a native Persistent Custom Rules layer, so a fork can gradually develop the long-term style preferences of one author or writing profile. Core contract language is English, but article language is unrestricted: the same workflow can be used for Chinese, English, or other languages.

## Design principles

- **One invocation, one gate.** Each editing pass has one narrow responsibility and must stop before the next gate.
- **Human-in-the-loop by design.** The workflow keeps discussion, judgment, and user decisions inside the process instead of treating writing as one-shot generation.
- **Deterministic validation outside the model.** Git state and validators check ordering, freshness, and legal transitions instead of trusting the agent to declare its own success.

## Why

Large writing prompts often mix thesis selection, scope control, structure, evidence boundaries, paragraph organization, and final language cleanup in one execution. DraftGate separates those responsibilities into narrow gates and gives each gate an explicit contract.

Built-in gates:

1. G1 — Main Question & Thesis
2. G2 — Scope & Branch Control
3. G3 — Argument Architecture + Draft Construction
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

.writing-rules/
  G1.md
  G2.md
  G3.md
  G4.md
  G5.md
  G6.md
  G7.md
```

There is no Hugo, CMS, front matter, cover image, or publishing dependency.

## Requirements

- Git
- Python 3.10+
- Optional: GitHub Actions for remote enforcement

No Docker, database, model server, or self-hosted runner is required.

## Quick start

Normal use is Agent-first:

1. Fork DraftGate on GitHub.
2. Give your fork URL to a GitHub-capable Agent.
3. Brainstorm freely in Pre-G1.
4. Tell the Agent to begin DraftGate for the article.
5. Execute one Gate at a time through conversation.
6. After G7 and CI PASS, GitHub Actions closes the cycle automatically: it preserves Gate evidence, writes one high-level result to `main`, archives the completed state, and removes the temporary writing branch. No user command is required.

A normal user does not need to manage Git branches, trailers, evidence tags, archive paths, or squash mechanics.

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

G3 is also where an outline becomes a substantive first draft when needed. A seed or section skeleton cannot pass G3 merely because the headings are correct.

## Personalize your writing style

DraftGate Core starts author-neutral, but a DraftGate fork is meant to support a persistent personal writing profile.

The repository includes one Custom Rules file for every Gate:

```text
.writing-rules/G1.md
...
.writing-rules/G7.md
```

These files start without author-specific rules. Users normally do not edit them manually. Tell the Agent conversationally when a preference should become long-term:

```text
"Keep this as a long-term rule: do not use one-sentence paragraphs just for emphasis."
→ G6

"Keep this preference: avoid singular first-person 'I' unless necessary."
→ G7

"Keep this rule: do not force a historical anecdote into the opening."
→ G3
```

A one-off article edit does not automatically become a persistent rule. The user must explicitly ask to keep, change, or remove a long-term preference.

During Gate `Gx`, only `.writing-rules/Gx.md` participates. Custom Rules from other Gates stay out of the current Gate, and Core always wins if a saved preference conflicts with the workflow contract.

See [Persistent Custom Rules](docs/writing/CUSTOM_RULES.md) for the full behavior and examples.

## Advanced / local usage

```bash
./writing begin --article-id <id> [--from Gx] [--title "..."]
./writing bootstrap --article-id <id> [--title "..."]
./writing init --article-id <id> [--from Gx]
./writing show --article-id <id>
./writing validate --article-id <id>
./writing advance --article-id <id>
./writing reopen --article-id <id>
./writing start-cycle --article-id <id> [--from Gx]
./writing reconcile --article-id <id> --confirm-recovery
./writing closeout --article-id <id> --ci-passed-for <G7_SHA>
./writing test
```

`begin` creates the temporary `writing/<article-id>/c<cycle>` branch and initializes the active cycle. `closeout` requires the exact G7 commit already verified by CI, preserves the full Gate chain under `writing-evidence/<article-id>/c<cycle>`, writes a cycle-aware archive, produces one high-level `main` commit, and deletes the temporary branch only after verification.

`reconcile` is recovery-only. It accepts the current committed article as a new baseline but does not prove that external edits complied with the current Gate. Agents must never run it automatically and must obtain explicit user confirmation.

`advance` updates the state file from the current working-tree article. A valid CHANGED gate commit must contain both the article change and the matching state transition.

If the most recently completed Gate is unsatisfactory and the cycle is still in progress, use `reopen` before running the next Gate. After G7 completes, the article is released for ordinary editing. For systematic rework, start a new cycle from the earliest affected Gate, for example `start-cycle --from G3` when structure or draft development needs another pass. Repeated cycles are normal.

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

For GitHub-backed normal use, a successful terminal G7 run triggers `Writing Auto Closeout` automatically. The closeout workflow re-verifies the exact writing-branch head, G7 trailers, complete state, and branch/cycle identity before it receives write permission to publish evidence, update `main`, archive state, and remove the writing branch. No user-side closeout command is part of the normal flow.

GitHub Actions remains optional for local-only use; in that mode `./writing closeout` is the explicit low-level operation. The same validators run locally with:

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

The public Core deliberately avoids language-specific phrase bans, fixed paragraph-length targets, mandatory first-person policies, and a prescribed authorial voice. Those choices belong in Persistent Custom Rules when a user wants them. A new fork starts neutral; explicit long-term preferences gradually turn that fork into the user's writing profile.

## License

MIT.


## Lifecycle and history

Each article cycle uses one temporary branch, `writing/<article-id>/c<cycle>`. Gate commits remain intact there. At successful closeout, DraftGate creates the policy-level write-once evidence ref `writing-evidence/<article-id>/c<cycle>`, archives the exact completed state at `.writing-state/archive/write-commentary/<article-id>/c<cycle>.json`, applies the final article and durable Custom Rules to current `main` in one high-level commit, removes the active state from `main`, then deletes the temporary branch.

Archived states are historical and are never freshness-checked against later article versions. A later cycle reads the latest archive without modifying it and creates a new active state from the current `main` article.

Persistent Custom Rules are repository-wide within a fork. A fork is therefore best treated as one author's or one writing profile's long-term rule space.
