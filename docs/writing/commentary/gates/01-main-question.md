# G1 — Main Question & Thesis

## Goal

Define only the article's single main question, core thesis, and necessary boundary.

Before freezing the thesis, run the Insight Test. The core judgment must be not only technically correct, but explanatory enough to support a full article.

## Reader outcome

A general reader should be able to explain in one sentence what the article is actually answering.

The thesis should also reveal a mechanism, relationship, constraint, structural role, or structural change that helps explain the main question rather than merely listing familiar downstream consequences.

## Correct observation vs explanatory insight

G1 must distinguish:

~~~text
correct observation
!=
worth-writing explanatory insight
~~~

Correct material does not automatically become a thesis worth freezing.

For example:

~~~text
a technology replaces a large amount of work
→ income changes
→ tax revenue changes
→ social identity changes
~~~

These observations may all be correct. But if the article merely links obvious consequences, it may still lack a sufficiently strong explanatory insight.

A stronger insight identifies the mechanism, relationship, constraint, structural role, or structural change that connects the observations.

The core standard is:

~~~text
non-obvious enough to add explanatory value
~~~

not:

~~~text
novel at all costs
~~~

## Insight Test

Before G1 can PASS, answer at least:

1. Is the thesis merely a summary of visible phenomena or downstream consequences?
2. Does it identify a mechanism, relationship, constraint, structural role, or structural change beneath the surface?
3. Does this insight materially help answer the G1 main question?
4. If the insight were removed, would the article collapse into a collection of common observations?
5. Is the insight adequately supported, or has it been inflated only to sound deeper?

The Insight Test does not require an original thesis or a new theory.

The target is explanatory value, not originality prestige.

## Weak insight handling

If the thesis is technically correct but remains mainly obvious, descriptive, or consequence-list based:

~~~text
G1 must not automatically PASS
~~~

Required behavior:

~~~text
explain why the current insight is still weak
→ continue discussing it with the user
→ refine or replace the thesis
→ G1 state unchanged
→ do not advance
~~~

This is a conversational waiting condition.

Do not introduce WAITING_INSIGHT, NEEDS_INSIGHT, or any other runtime state/status.

## Insight boundaries

G1 explicitly forbids:

- manufacturing a contrarian claim only to appear novel;
- inflating claim strength to appear insightful;
- requiring the thesis to be historically original;
- requiring the article to propose a new theory;
- replacing explanation with concept naming;
- turning uncertainty into certainty to create an impression of depth;
- retaining an under-supported mechanism merely because it sounds more interesting.

G1 allows:

- restating a known mechanism in a more explanatory way;
- identifying a structural relationship readers may not already connect;
- using one underlying constraint to explain several familiar consequences;
- freezing a modest but useful insight when that is all the evidence supports.

~~~text
forced profundity forbidden
novelty is not required
~~~

## Allowed

- derive one main question from a topic, source material, or existing draft;
- state the core thesis in 1–2 sentences;
- mark obvious fact / judgment / inference boundaries;
- run the Insight Test;
- continue discussion without advancing when the insight remains weak;
- ask the minimum clarification needed when missing information could change the main question.

## Forbidden

- reorder sections;
- rewrite the whole article;
- reorganize paragraphs;
- perform language polishing or AI-trace cleanup;
- expand side branches;
- treat consequence aggregation as a sufficient thesis;
- invent an unsupported mechanism for the sake of depth;
- treat concept naming as explanation.

## Exit

G1 PASS requires all of:

~~~text
unique main question
+
core thesis
+
necessary boundary
+
Insight Test = PASS
~~~

Insight Test PASS means:

- the thesis is not merely a consequence list;
- the thesis provides real explanatory value;
- the insight materially helps answer the main question;
- removing the insight would materially weaken the article and expose a collection of common observations;
- claim strength remains supported.

If the Insight Test FAILS:

~~~text
no G1 PASS
state unchanged
no advance
~~~

Output the main question, core thesis, necessary boundary, and Insight Test result. Mark G1 PASS only when all conditions are satisfied, then stop.
