# G3 — Argument Architecture + Draft Construction

## Goal

Organize sections and reasoning in the order a reader needs to understand the problem, not in the order the author happened to research it.

G3 first completes a human-in-the-loop Narrative Mode Decision. After the user selects a mode, G3 builds the formal argument architecture. Once the architecture is stable, G3 must also determine whether the article is already a substantive first draft. If it is still only a seed, outline, section skeleton, placeholder-heavy draft, or materially incomplete draft, G3 must complete Draft Construction before PASS.

Narrative mode determines how the article progresses. A central explanatory frame or narrative anchor is only one optional structural device and is not the default for every article.

## Reader outcome

A general reader can tell what drives the article, why the sections appear in the current order, and what responsibility each class of material carries.

An intermediate reader can distinguish:

~~~text
Primary narrative driver
Primary mechanism
Supporting evidence
Local analogy
Removable / demoted material
~~~

## Narrative Mode Decision

Before formal architecture work, G3 must propose 1–3 narrative-mode candidates appropriate to the frozen G1 main question and G2 scope.

Candidates may include:

~~~text
question-driven
frame-driven
case-driven
hybrid
other / no special narrative mode
~~~

These are not mandatory templates and are not an enumeration that must always be shown in full.

The Agent may combine, refine, or propose another mode that better fits the article, but must not mechanically present every option.

For each candidate, explain briefly:

1. why it fits the article;
2. how the article would progress;
3. which material becomes the main line;
4. which material becomes supporting evidence;
5. the primary risk.

### Explicit user selection

Narrative Mode Decision is a human-in-the-loop writing decision.

The Agent must not choose the mode on the user's behalf.

If the user has not explicitly selected a candidate, or explicitly proposes and selects another workable mode:

~~~text
G3 state unchanged
do not advance
do not mark G3 PASS
do not create a Gate completion transaction
~~~

Waiting for user selection is not Gate completion.

Narrative mode is not persisted in workflow state, does not add a state field, and does not add a runtime status.

## Mode contracts

These contracts define basic progression principles. They are not fixed table-of-contents templates.

### question-driven

The primary driver is the main question.

Typical progression:

~~~text
main question
→ progressively deeper explanation
→ mechanism
→ implication / boundary / judgment
~~~

Requirements:

- deepen the same question step by step;
- do not require a central frame;
- Central frame decision may be NOT NEEDED;
- each major section must continue the same question rather than becoming a separate mini-article;
- examples and evidence must serve an explanatory step rather than create a competing main line.

### frame-driven

The primary driver is the central explanatory frame.

Typical progression:

~~~text
central frame
→ mechanism inside the frame
→ mapping to the real problem
→ primary mechanism
→ competing explanation / boundary
→ return to the frame
~~~

Requirements:

- Central frame decision must be USED;
- the frame must remain useful across multiple major parts;
- the frame must perform real analytical work, not only opening-hook work;
- the frame must help explain the mechanism;
- material that serves neither the frame nor the primary mechanism must be demoted or removed;
- G1 and G2 retain higher authority.

### case-driven

The primary driver is a case or observable situation.

Typical progression:

~~~text
case / phenomenon
→ what happens inside the case
→ mechanism
→ controlled generalization
→ boundary / implication
~~~

Requirements:

- the case itself is the object of analysis;
- generalization develops gradually;
- do not silently convert the case into an unrelated metaphor;
- do not jump from one case directly to a universal law;
- keep local analogy separate from the case's role.

### hybrid

Hybrid may combine two or more narrative devices, but exactly one must be the primary driver.

Examples:

~~~text
primary driver = question-driven
secondary device = frame
~~~

or:

~~~text
primary driver = case-driven
secondary device = question progression
~~~

Do not create two competing main lines.

If readers could reasonably interpret two different material groups as co-equal article spines, architecture is not stable and G3 cannot PASS.

### other / no special narrative mode

If none of the named modes fits, use another clearly described architecture or no special narrative mode.

Requirements:

- identify the primary driver;
- identify the progression rule;
- do not invent a frame or case merely because no special narrative device exists.

## Conditional phenomenon-first architecture

For frame-driven or case-driven articles, a concrete and genuinely explanatory phenomenon may sometimes come first:

~~~text
phenomenon
→ mechanism
→ main question / larger implication
~~~

Phenomenon-first is conditional, not a universal opening requirement.

Do not force it when:

- the phenomenon is only a decorative hook;
- the main question must be established first;
- the article is primarily question-driven;
- the phenomenon delays the real analytical problem;
- the opening would become anecdotal storytelling without analytical value.

## Explanatory Spine Check

After Narrative Mode Decision and before architecture PASS, G3 must establish an Explanatory Spine.

Definition:

~~~text
Explanatory Spine
=
one continuing mechanism / relationship / contradiction / constraint chain
that advances across the whole article
~~~

It answers:

~~~text
Why can the article move logically from its first step to its last step?
~~~

The Explanatory Spine must contain causal, logical, or structural progression. A list of section topics is not enough.

### Narrative Mode != Explanatory Spine

Narrative Mode answers:

~~~text
How is the article told?
~~~

Explanatory Spine answers:

~~~text
Why does the reasoning progress from the first step to the last?
~~~

Therefore:

~~~text
Narrative Mode != Explanatory Spine
~~~

Every mode—question-driven, frame-driven, case-driven, hybrid, or other—requires an Explanatory Spine.

### Central Frame != Explanatory Spine

A Central Frame is an optional narrative device.

An Explanatory Spine is the required reasoning chain.

Therefore:

~~~text
Central Frame != Explanatory Spine
~~~

A frame may help display the spine but cannot replace it.

If a frame-driven article leaves the reader remembering only the frame but unable to explain the mechanism chain, G3 cannot PASS.

If a case-driven article only describes what happened in the case but does not derive a mechanism, relationship, constraint, or implication chain, G3 cannot PASS.

### Required spine output

G3 must explicitly output:

~~~text
Explanatory spine:
<expressed in 1–3 sentences>
~~~

The 1–3 sentence form is a reasoning-compression artifact. It is not persisted in workflow state.

A qualifying spine normally makes visible:

~~~text
starting condition
→ core mechanism / relationship
→ intermediate implication
→ final structural judgment
~~~

This is not a fixed rhetorical formula. The requirement is continuity.

### Section binding

Every major section must answer:

~~~text
How does this section advance or support the Explanatory Spine?
~~~

It is not enough to say:

~~~text
This section is related to the main question.
~~~

Each major section should have a clear spine function, such as:

- establish a starting condition;
- explain the primary mechanism;
- introduce a required intermediate link;
- test or qualify the mechanism;
- derive an implication;
- expose a structural contradiction;
- move from mechanism to final judgment.

If a section is interesting but does not advance or support the spine, it must be:

~~~text
demoted
removed
or assigned a different role
~~~

This remains part of the existing Material Hierarchy and does not create a parallel structure.

## Material Hierarchy

After Narrative Mode Decision, G3 must classify the responsibilities of major material.

At minimum:

~~~text
Primary narrative driver
Primary mechanism
Supporting evidence
Local analogy
Removable / demoted material
~~~

For a frame-driven article, also identify:

~~~text
Central frame role
~~~

Material Hierarchy is a G3 reasoning artifact, not persistent state.

### Primary narrative driver

The single device that determines how the reader moves from the opening to the ending.

The article has exactly one primary narrative driver.

### Primary mechanism

The core explanatory mechanism that answers the G1 main question.

Narrative devices may help display it but cannot replace it.

### Supporting evidence

Facts, cases, data, observations, and examples must carry a clear supporting responsibility.

Each group of supporting evidence must answer:

~~~text
Which claim or mechanism step does this support?
~~~

Supporting evidence must not form a competing narrative spine.

### Local analogy

A local analogy or concrete scenario exists only to support local understanding.

A local analogy must not become the whole-article central frame unless the user re-enters G3 architecture decision and explicitly approves that change.

### Removable / demoted material

Material may be correct, vivid, or interesting but still inappropriate for the current article.

If it serves neither the primary narrative driver, primary mechanism, nor a clear supporting role, it should be removed, shortened, or demoted.

Core rule:

~~~text
good example != suitable example
~~~

## Compression Test

Before G3 Exit, run the Compression Test:

~~~text
After removing headings, examples, data, subsection labels, and rhetoric,
can the article's distinctive reasoning chain be expressed in 3–4 sentences?
~~~

Those 3–4 sentences must retain:

~~~text
starting point
core mechanism
key intermediate inference
final judgment
~~~

Sentence count here is a reasoning test, not a body-format rule.

### PASS

The compressed version still shows:

- where the reasoning starts;
- which mechanism or relationship performs the main explanatory work;
- which intermediate inference moves the mechanism forward;
- why the final judgment follows.

### FAIL

At minimum, FAIL includes:

- only a list of opinions remains;
- only a list of section topics remains;
- the compressed form merely repeats the main question;
- only theme words remain and the mechanism disappears;
- the key intermediate inference disappears;
- the final judgment appears without a visible reasoning path;
- coherence depends on restoring examples or rhetoric.

The Compression Test does not require the article body to contain only 3–4 ideas.

It checks whether the article has one compressible reasoning skeleton.

## Draft Construction

After architecture is complete, G3 performs the Draft Construction Check.

Core target:

~~~text
major section responsibility
→ substantive prose that performs that responsibility
~~~

### When expansion is required

If the current article remains any of the following:

- seed draft;
- outline;
- section skeleton;
- placeholder-heavy draft;
- major sections containing only one or two responsibility notes;
- materially incomplete draft;

G3 must expand the major sections into a continuously readable complete first draft before PASS.

The following do not satisfy a section responsibility:

- one-line placeholder;
- section-purpose note;
- outline bullets;
- a sentence that only says what the section will explain later;
- a heading with no substantive development below it.

Do not use fixed word count, paragraph count, sentence count, or character threshold to determine draft completeness.

### Existing substantive prose

If existing prose already performs its section responsibility, preserve it as much as possible.

G3 makes only the changes necessary to satisfy the current architecture and Draft Construction Check.

Entering G3 does not authorize regenerating the whole article.

### Allowed Draft Construction work

G3 may:

- expand explanations already authorized by G1, G2, and G3;
- develop mechanisms already inside scope;
- turn section responsibility into substantive prose;
- use facts, examples, and material already supplied by the user or already present in the article;
- write necessary paragraphs, ordinary sentences, and transitions;
- connect major sections continuously to the Explanatory Spine;
- apply G3 Custom Rules.

### Downstream authority boundary

Core boundary:

~~~text
draft construction necessity
!=
downstream Gate responsibility
~~~

G3 may write explanation, paragraphs, transitions, and ordinary sentences when necessary to create a complete first draft.

But G3 must not make the following independent objectives:

- G4 accessibility audit;
- G5 adversarial / evidence pressure test;
- G6 paragraph audit / restructuring;
- G7 language / pattern / AI-trace cleanup.

If G3 notices downstream problems, leave them to the corresponding Gate unless a minimal correction is strictly necessary to produce coherent substantive draft prose.

G3 also must not:

- invent facts, data, quotations, sources, or evidence;
- treat unsupported factual claims as verified;
- expand merely to increase length;
- cross G2 scope;
- silently rewrite the G1 thesis.

## Central frame decision

After Narrative Mode Decision, G3 records a reasoning artifact:

~~~text
Central frame decision:
USED
or
NOT NEEDED
~~~

This decision is not persistent state.

By mode:

~~~text
question-driven
→ central frame may be NOT NEEDED

frame-driven
→ central frame must be USED

case-driven
→ the case is the driver; do not automatically add another metaphorical frame

hybrid
→ central frame usage follows the declared primary driver
~~~

### USED

Use a frame only if it:

- directly serves the G1 main question;
- serves the G2 frozen main line;
- performs mechanism explanation rather than only story-making;
- continues to add analytical value later in the article;
- remains useful across at least two major article stages or sections;
- does not pull the reader toward a different article.

The frame must serve the article. The article must not be rewritten merely to fit the frame.

### NOT NEEDED

If no naturally useful central frame exists, choose NOT NEEDED.

Do not invent a story for virality, attractiveness, or Gate completion.

## Frame quality check

Before adopting a frame, ask:

1. Does it materially help explain the main question?
2. Does it perform analysis beyond acting as a hook?
3. Can it still advance the mechanism in the middle of the article?
4. Can the ending return to it naturally?
5. Does it compete with the main line or distort the article to fit the analogy?
6. Would the article be clearer without it?

Weak frames include:

- a historical story used only to attract attention;
- a celebrity, war, film, or literary metaphor weakly related to the main question;
- a disconnected hook that disappears after the opening;
- a grand scene added only to create scale;
- a memorable image that cannot continue to explain the mechanism.

## G3 / G4 boundary

G3 owns:

~~~text
whole-article frame / narrative architecture
primary narrative driver
central frame decision
~~~

G4 owns:

~~~text
local explanatory analogy
concrete scenario
local intuitive explanation
~~~

If G3 already uses a central frame, G4 may improve local mapping, explanation, and boundary statements, but may not invent a new whole-article frame or promote a local analogy into one.

## G5 challenge boundary

Central frame and narrative mode remain open to G5 pressure testing.

G5 may challenge:

- whether the frame overextends the analogy;
- whether the mapping is valid;
- whether a competing mechanism exists;
- where the similarity stops;
- whether a case supports the current generalization.

If G5 finds that the frame or case distorts claim validity, use existing G5 / reopen / correction semantics.

Do not preserve a false mapping merely because the frame is rhetorically effective.

## Allowed

- propose 1–3 suitable narrative-mode candidates;
- complete architecture after explicit user selection;
- establish and output the Explanatory Spine;
- bind major sections to the spine;
- run the Compression Test;
- reorder sections;
- merge or split sections;
- define one responsibility for each major section;
- adjust necessary transitions so progression works;
- establish the Material Hierarchy;
- decide whether the central frame is USED or NOT NEEDED;
- remove or demote supporting material that creates a competing main line;
- expand a seed, outline, or incomplete draft into a complete first draft when required;
- write necessary explanation, paragraphs, transitions, and ordinary sentences for Draft Construction.

## Forbidden

- choosing narrative mode for the user;
- advancing G3 before user selection;
- treating Narrative Mode or Central Frame as the Explanatory Spine;
- allowing a major section to be merely related to the main question without advancing the spine;
- silently rewriting the G1 thesis;
- changing the frozen G1 main question;
- promoting a G2-demoted branch into the main line;
- inventing a story only for attractiveness;
- forcing a historical analogy weakly related to the main question;
- allowing supporting evidence to create a competing narrative;
- changing G1 thesis or G2 scope to preserve a frame;
- using a decorative hook that has no later function;
- treating phenomenon-first as a universal requirement;
- performing G4 accessibility audit as an independent G3 objective;
- performing G5 adversarial / evidence pressure testing as an independent G3 objective;
- performing G6 paragraph audit / restructuring as an independent G3 objective;
- performing G7 language / pattern / AI-trace cleanup as an independent G3 objective;
- sentence-level polishing as an independent cleanup task;
- AI-trace cleanup.

## G1 / G3 authority boundary

G1 owns:

~~~text
discover and freeze a core insight / thesis worth writing
~~~

G3 owns:

~~~text
expand the frozen insight into a coherent Explanatory Spine
→ organize that spine into narrative architecture
~~~

G3 may clarify implications but must not silently replace or rewrite the G1 thesis.

If a coherent spine cannot be built because the frozen G1 thesis is the problem:

~~~text
STOP
→ report G1 conflict
→ do not advance G3
→ do not silently rewrite thesis
~~~

The user continues with existing reopen / correction / start-cycle semantics.

Do not introduce a rollback mechanism.

If architecture review exposes a claim-strength or evidence problem:

~~~text
STOP
→ report conflict
~~~

Do not silently perform G5 work inside G3.

## Conditional resource

Read `../structure-rules.md`.

## Exit

Before G3 PASS, all of the following must hold:

1. the user has explicitly selected or approved the narrative mode;
2. the Primary narrative driver is unique and clear;
3. the Primary mechanism is clear;
4. the Explanatory Spine is expressed in 1–3 sentences;
5. every major section advances or supports the Explanatory Spine;
6. supporting evidence has a clear supporting responsibility;
7. supporting evidence does not form a competing narrative;
8. local analogy remains local;
9. removable or demoted material has been identified when necessary;
10. section progression matches the selected mode;
11. Central frame decision matches the selected mode;
12. Compression Test = PASS;
13. G1 thesis unchanged;
14. G2 scope unchanged;
15. Draft Construction Check = PASS;
16. every major section contains substantive prose that performs its section responsibility;
17. the article reads as a complete first draft rather than an outline or placeholder skeleton;
18. sufficient existing prose has been preserved where possible;
19. G4–G7 downstream responsibilities have not been executed as independent G3 objectives.

If waiting for user selection:

~~~text
G3 = WAITING FOR USER
state unchanged
no advance
~~~

WAITING FOR USER is only a conversational execution condition. It is not a runtime state status.

Mark G3 PASS and stop.
