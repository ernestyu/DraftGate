# G7 — Final Language & Pattern Audit

## Goal

After G1–G6 have passed, perform final language cleanup and audit mechanical writing patterns.

G7 does not reopen or repair the main question, scope, architecture, accessibility design, claim boundary, or paragraph organization.

## Reader outcome

The article reads naturally and consistently without relying on repetitive signposting, rhetorical inflation, or templated rhythms.

## Allowed

- remove redundant expression;
- tighten verbose sentences without changing meaning;
- clean mechanical connectors, empty emphasis, and repetitive sentence patterns;
- apply the registered pattern-cleanup rules;
- clean the opening as part of the article body;
- check only for a clear semantic conflict between the existing title and body;
- run the G7 checklist.

## Forbidden

- modify G1 main question or thesis;
- modify G2 scope roles;
- modify G3 architecture;
- modify G4 accessibility structure;
- modify G5 claim strength, evidence boundary, or uncertainty;
- modify G6 paragraph boundaries;
- add important arguments or evidence;
- strengthen conclusions for click-through or rhetorical effect;
- redesign the opening hook as a separate task;
- perform title optimization or packaging.

If G7 reveals a probable earlier-gate problem, do not silently fix it. Finish only work authorized by G7; a new correction cycle requires explicit user action.

## Opening → Section 1 Handoff Check

The opening must establish an entry problem, tension, scene, or main question. Section 1 must advance to a new mechanism or explanatory layer.

FAIL at minimum when Section 1 merely repeats:

- the same enumeration;
- the same example with no new analytical use;
- the same major claim;
- the same sentence skeleton;
- the opening in different words.

This check does not authorize architecture redesign.

## Narrative Repetition Audit

Check the whole article for structural repetition:

1. repeated `summary → explanation → summary` section rhythm;
2. section openings that only restate the previous ending;
3. every section ending with the same thesis-like closure;
4. repeated meta-signposting;
5. sections that restate the main thesis without adding mechanism, evidence, boundary, or implication;
6. repeated transition structures;
7. major claims repeated without new analytical work.

## Mechanical Writing Pattern Audit

Read `../ai-trace/rules.md`.

The rules are semantic and language-neutral. They target patterns such as empty emphasis, redundant signposting, mechanical parallelism, abstract padding, boilerplate openings/closings, fake progression, and rhetorical question-answer templates.

No bundled word blacklist is authoritative. Phrase-level matches alone never justify editing.

## G6 cleanup boundary

G7 may make sentence-level cleanup after legal G6 paragraphing, but it must not:

```text
merge paragraph
split paragraph
change paragraph boundary
re-run G6
```

If paragraph boundaries appear wrong, the user decides whether to start a G6 correction cycle.

## Exit

Before G7 PASS confirm:

```text
Opening → Section 1 handoff = coherent and non-redundant
Narrative Repetition Audit = PASS
Mechanical Writing Pattern Audit = PASS
paragraph boundaries unchanged by G7
```

Then mark G7 PASS, set the workflow to complete, and stop.

G7 is the only normal terminal gate. It is the final body-editing boundary.
