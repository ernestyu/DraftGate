# G6 — Paragraph Organization

## Goal

Organize paragraphs by semantic and argumentative responsibility while rejecting both over-merge and fragmentation.

Primary rule:

```text
paragraph boundary
=
semantic / argumentative responsibility boundary
```

Do not split or merge paragraphs mechanically by sentence count, character count, or visual rhythm.

## Reader outcome

Each paragraph performs a coherent argumentative function. Paragraph boundaries correspond to a meaningful change in responsibility.

## Paragraph rule

A paragraph may contain several sentences and several internal moves as long as they serve one coherent argumentative function.

Common functions include:

```text
establish a fact pattern
state a local judgment
explain a mechanism
develop an example
draw an implication
set a boundary
contrast mechanisms
transition from mechanism to consequence
identify the real question
close one local argument action
```

A single argument action should not be split merely because one sentence is short, important, transitional, or conclusive.

A paragraph does not need to follow a fixed internal template.

## Functional short paragraph

A short paragraph is valid when it has independent semantic or argumentative responsibility, for example a real transition, boundary, contrast, question, or mechanism-to-implication shift.

Short length alone is neither a failure nor a virtue.

## Invalid fragmentation

A short paragraph is usually invalid when it exists only for rhythm, emphasis, slogan effect, dramatic pause, visual spacing, or a restatement of the adjacent paragraph.

If adjacent paragraphs are one argument action, they should normally be merged.

## Length policy

Length is not a gate criterion.

Explicitly forbidden:

```text
fixed paragraph target
minimum paragraph length
maximum paragraph length
automatic split by character count
automatic merge by sentence count
single_sentence_paragraphs = 0
```

A long paragraph may remain intact when it has one coherent responsibility. A short paragraph may remain separate when it has an independent responsibility.

## Full Paragraph Audit

Before G6 exits, audit every paragraph rather than sampling.

For each paragraph ask:

1. Does it have one coherent argumentative function?
2. Is there a clear semantic responsibility shift inside it?
3. If short, does it have an independent function rather than a visual or dramatic purpose?
4. Does it actually belong to the same argument action as an adjacent paragraph?
5. If long, is there a genuine responsibility boundary that would justify splitting it?

The audit creates no new persistent artifact or runtime field.

## Over-merge FAIL

At minimum:

- one paragraph contains several separable argumentative responsibilities;
- a mechanism explanation ends and an unrelated policy implication is appended;
- factual setup, objection, and conclusion are compressed together despite doing different work;
- distinct mechanisms are merged only to avoid short paragraphs.

## Fragmentation FAIL

At minimum:

- consecutive short paragraphs perform one argument action;
- claim, explanation, and evidence are separated only for rhythm;
- an isolated sentence exists only for emphasis or slogan effect;
- line breaks manufacture repeated punch lines;
- a paragraph boundary does not correspond to a responsibility shift.

## Allowed

- merge adjacent paragraphs that belong to one argument action;
- split an overloaded paragraph at a real responsibility boundary;
- preserve genuinely functional short paragraphs;
- make minimal connector or reference adjustments required by a legal merge or split.

## Forbidden

- change the main question;
- change section order;
- add or remove arguments;
- add evidence;
- change claim strength;
- perform final language-pattern cleanup;
- impose a target paragraph length;
- decide paragraph boundaries from sentence count alone.

## Conditional resource

Read `../language-rules.md` only for paragraph, fragmentation, and complete-reasoning rules.

If a shared rule conflicts with this file, this G6 contract wins.

## Exit

G6 PASS requires:

```text
Full Paragraph Audit = complete
over-merge = rejected
fragmentation = rejected
Functional Short Paragraphs justified by independent responsibility
```

Every paragraph boundary must be explainable by semantic or argumentative responsibility.

Mark G6 PASS and stop.
