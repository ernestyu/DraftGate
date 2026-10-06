# G4 — Reader Accessibility

## Goal

Reduce reader effort while preserving technical content, mechanism, conditions, uncertainty, and evidence boundaries.

## Reader outcome

- General readers can follow terminology and intermediate reasoning.
- Intermediate readers can take away at least one reusable understanding framework.
- Expert readers do not feel that the mechanism has been oversimplified.
- When an abstract mechanism is difficult to understand directly, an accurate analogy, concrete scenario, or perceptible image may build intuition and then return the reader to the real mechanism.

## Allowed

- add an intuitive explanation when a specialist concept first appears;
- improve explanation order;
- add missing intermediate reasoning;
- express a complex mechanism as a reusable conceptual framework;
- remove unnecessary technical display;
- use an accurate explanatory analogy for an abstract mechanism;
- use a concrete scenario to build intuition;
- use a small amount of physical or real-world imagery to explain an abstract relationship;
- add the minimum boundary statement needed to show where an analogy stops mapping.

An explanatory analogy must perform a clear mechanism mapping. During G4, the Agent must be able to determine:

- what the important elements in the analogy map to in the real problem;
- what relationship in the analogy maps to the real mechanism;
- where the analogy fails or no longer applies.

The article does not need to present a mechanical mapping table, but the mapping must actually hold.

For example, a statement such as:

~~~text
Several agents optimizing locally do not guarantee global coordination.
~~~

may be explained with a neutral scenario in which independent actors make locally reasonable decisions without a shared mechanism for timing, priorities, or global objectives.

The explanation must then return to the real mechanism:

~~~text
local optimization != global coordination
~~~

The analogy must not replace the mechanism explanation.

A concrete scenario may be used instead of a metaphor. Its responsibility is still to explain the mechanism rather than introduce an independent argument.

## Density

Do not turn the article into a sequence of metaphors.

Default principles:

- one complex mechanism should normally use no more than one primary analogy;
- an article may contain multiple analogies, but they should be separated and serve different explanatory tasks;
- each analogy must have an independent explanatory responsibility;
- if a concrete scenario already explains the mechanism adequately, do not add another analogy merely for vividness.

Avoid:

- analogy in every sentence;
- several consecutive paragraphs driven mainly by imagery;
- dense slogan-like rhetoric;
- repeatedly switching analogies for the same mechanism.

These are functional constraints, not language-specific style rules.

## Analogy boundary

An analogy is not evidence.

It cannot prove causality and cannot turn partial similarity into structural identity.

If an analogy draws on history, biological evolution, physical systems, war, disease, ecosystems, financial markets, or another domain with materially different structure, explicitly check those structural differences.

Add the minimum boundary statement when needed.

Do not use an analogy if it would mislead the reader about the core mechanism.

## G3 / G4 boundary

G4 owns local explanatory analogies, concrete scenarios, and local intuitive explanation.

G4 does not redesign the whole-article central explanatory frame, narrative anchor, or argument architecture frozen in G3.

If G3 uses a central frame, G4 may improve local mapping, explanation, and boundary statements, but it must not promote a local analogy into a new whole-article frame.

## G5 boundary

G4 must not change claim strength, causal certainty, or evidence boundaries.

If an explanation can be made coherent only by changing claim strength, the evidence boundary, or the core mechanism:

~~~text
STOP
→ report conflict
~~~

Do not silently perform G5 work inside G4.

## Forbidden

- simplify by deleting a key mechanism, evidence boundary, condition, or uncertainty;
- change the main section architecture;
- add exaggerated wording merely to attract attention;
- perform final language unification;
- use analogy as evidence;
- use metaphor to inflate a claim;
- add rhetoric unrelated to the argument for the sake of vividness;
- use several conflicting analogies for the same mechanism;
- modify the G1 thesis;
- change G2 scope;
- redo G3 argument architecture;
- change G5 claim strength.

## Exit

A reader without specialist background can follow the article without losing the important technical boundaries.

For any major mechanism that remains too abstract for a general reader, G4 must decide whether an analogy, concrete scenario, or local intuitive explanation is actually needed. If one is used, it must perform a real explanatory task and return to the real mechanism.

Mark G4 PASS and stop.
