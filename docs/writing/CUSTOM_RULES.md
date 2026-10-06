# Persistent Custom Rules

DraftGate has two writing-rule layers:

1. **Core rules** — built into DraftGate and shared by every user.
2. **Persistent Custom Rules** — optional long-term preferences for one author or writing profile.

The Core is intentionally author-neutral by default. DraftGate itself is not limited to a neutral style: a fork can gradually accumulate the user's own writing preferences in `.writing-rules/G1.md` through `.writing-rules/G7.md`.

## How to use them

Users normally do not edit these files by hand. State the preference conversationally and make clear that it should persist.

Examples:

```text
"Keep this as a long-term rule: do not use one-sentence paragraphs just for emphasis."
→ G6

"Keep this preference: avoid singular first-person 'I' unless it is necessary."
→ G7

"Keep this rule: do not force a historical anecdote or metaphor into the opening."
→ G3

"Keep this rule: explain a specialist term the first time an ordinary reader needs it."
→ G4
```

The Agent should map the preference to the Gate whose responsibility it affects and update only that Gate's file.

## What becomes persistent

A normal article edit does **not** automatically become a Custom Rule.

A preference becomes persistent only when the user explicitly asks to keep, change, or remove it as a long-term rule.

This prevents one article's local decision from silently becoming a global writing policy.

## Gate isolation

When DraftGate executes Gate `Gx`, only these rule sources may affect that Gate:

```text
DraftGate Core rule for Gx
+
.writing-rules/Gx.md
```

Custom Rules from other Gates do not participate in editing, evaluation, or PASS / FAIL decisions for the current Gate.

## Core always wins

Persistent Custom Rules cannot override the workflow contract.

If a saved preference conflicts with a Core rule:

```text
Core applies
→ conflicting Custom Rule is ignored for that execution
→ the Agent tells the user about the conflict
→ workflow state is not changed merely because of the conflict
```

## Default files

A new DraftGate fork contains:

```text
.writing-rules/
  G1.md
  G2.md
  G3.md
  G4.md
  G5.md
  G6.md
  G7.md
```

They start without author-specific rules. As the user explicitly saves preferences, the fork becomes a long-term writing profile for that author.

A simple operating model is therefore:

```text
one fork
→ one author or writing profile
→ many articles and cycles
→ one persistent Custom Rules layer
```
