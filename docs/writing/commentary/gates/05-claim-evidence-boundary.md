# G5 — Claim & Evidence Boundary

## Goal

Inspect and tighten the boundaries among fact, evidence, causality, analogy, extrapolation, and uncertainty. Apply an adversarial / counterfactual pressure test to the main thesis and major claims.

## Reader outcome

An expert reader can see how far the evidence actually supports the claims and can see that the core judgment has been tested against a reasonable objection, a competing mechanism, and a meaningful failure condition.

## Required pressure test

For the main thesis and major claims, G5 must answer at least:

1. What is the strongest reasonable objection?
2. Is there an alternative mechanism or explanation that can account for the same facts without depending on the article's primary mechanism?
3. What fact, condition, or observation would materially weaken or falsify the claim?
4. After pressure testing, should the claim be kept, narrowed, weakened, conditioned, supplemented with a competing explanation, or removed?

### Strongest reasonable objection

The objection must be informed, logically coherent, relevant to the actual claim, and plausible for a serious reader.

Do not satisfy this check with:

- a strawman objection;
- an obviously false opposing view;
- an extreme case unrelated to the article;
- an artificially simplified opposing position created only to make rebuttal easy.

If several reasonable objections exist, prioritize the one most likely to change the core claim.

### Alternative mechanism

Actively test whether the same facts could reasonably be explained by another mechanism.

If a reasonable competing explanation exists, do not present the article's mechanism as the only cause unless the available evidence actually supports uniqueness.

Allowed G5 repairs include:

- narrow causal language;
- add an applicability boundary;
- state that the mechanism is one explanation rather than the only explanation;
- add the minimum necessary competing mechanism;
- explain why a competing explanation is insufficient only when the article already contains evidence for that conclusion.

### Counterfactual / falsification condition

A major claim should have an understandable failure condition or applicability boundary whenever possible.

G5 must be able to answer:

~~~text
What observation, condition, or fact would make this claim materially weaker or false?
~~~

Do not accept a self-sealing structure in which every possible outcome is treated as confirmation.

## Narrative-compatible adversarial expression

G5 rigor does not change, but the expression of the pressure test may remain compatible with the mechanism or narrative frame already established by the article.

Without sacrificing precision:

- a frame-driven article may apply the strongest objection directly to the central frame and show where the frame stops mapping;
- a case-driven article may express the boundary by showing which facts in the case are insufficient for the generalization;
- a question-driven article may express falsification by asking under what conditions the proposed answer no longer explains the observed pattern.

This avoids mechanically adding an academic-style limitations section.

The priority remains:

~~~text
precision > narrative elegance
~~~

If the existing frame or mechanism cannot express the objection, boundary, or falsification condition accurately, use direct, abstract, or technical language instead.

Narrative compatibility must not reduce:

- objection strength;
- evidence boundary;
- causal uncertainty;
- alternative mechanism;
- falsification condition;
- scope limitation.

Do not hide uncertainty inside metaphor merely to preserve narrative smoothness.

## Pressure-test outcomes

Allowed G5 outcomes:

- KEEP
- NARROW_SCOPE
- LOWER_STRENGTH
- ADD_CONDITION
- ADD_COMPETING_EXPLANATION
- REMOVE_UNSUPPORTED_CLAIM
- STOP_CONFLICT

KEEP means that the full pressure test has been completed and the core claim itself does not need revision.

KEEP does not force NO_CHANGE.

If a real G5-authorized article modification is still necessary after KEEP—for example, adding a condition, tightening one causal sentence, or adding a necessary boundary—use the normal CHANGED path.

If the full adversarial / counterfactual pressure test has been completed and:

- the strongest reasonable objection has been evaluated;
- the alternative mechanism has been evaluated;
- the falsification / weakening condition has been evaluated;
- major claims satisfy the G5 exit contract;
- no necessary G5-authorized article modification remains;

then G5 may use:

~~~text
KEEP
→ G5-authorized NO_CHANGE
~~~

Merely finding no obvious problem without completing the pressure test is not a valid NO_CHANGE.

## Allowed

- distinguish fact / correlation / mechanism explanation / inference;
- narrow overly strong causal language;
- add an applicability boundary to an analogy;
- add a necessary competing explanation or limitation;
- reduce claim strength when it exceeds the evidence;
- add necessary conditions;
- remove an unsupported strong judgment;
- add the minimum boundary statement required.

If the outcome requires article modification, use the existing CHANGED gate transaction.

If the outcome is KEEP and the article already satisfies the full G5 contract, use the frozen NO_CHANGE infrastructure.

## Forbidden

- upgrade inference into fact for rhetorical force;
- turn one case into a universal law;
- add a certain conclusion where evidence is absent;
- ignore a reasonable competing explanation to preserve the thesis;
- construct a weak strawman merely to complete the objection check;
- perform paragraph beautification or AI-trace cleanup;
- change the G1 main question;
- reselect the thesis;
- redo G2 scope;
- redo G3 argument architecture;
- perform large-scale section reordering;
- perform G6 paragraph restructuring;
- perform G7 language cleanup;
- design a final promotional title after workflow completion.

## STOP_CONFLICT

If pressure testing shows that the core thesis cannot stand, or repair requires returning to G1–G3:

~~~text
STOP_CONFLICT
→ do not advance G5
→ do not use NO_CHANGE
→ state unchanged
→ do not automatically roll back G1–G3
~~~

The user decides whether to start a new cycle or correction.

NO_CHANGE must not substitute for:

- STOP;
- NEEDS_USER;
- inability to judge;
- incomplete pressure testing;
- STATE STALE.

## No mandatory opposition section

The counterfactual / adversarial check does not require a dedicated opposing-view section.

If the existing article already covers the objection, add no opposing paragraph.

If only one claim needs tightening, make only the minimum change.

If the reader needs a competing explanation, add only the minimum necessary content.

Do not mechanically add stock opposition framing merely to signal balance.

## NO_CHANGE semantic condition

G5 allows NO_CHANGE only when:

~~~text
full adversarial / counterfactual pressure test completed
+
all major claims satisfy the G5 exit contract
+
no G5-authorized article modification remains
~~~

Then:

~~~text
article blob unchanged
article_revision unchanged
exactly one G5 → G6 transition
state-only gate commit
~~~

Continue to use:

~~~text
Writing-Workflow: gate
Writing-Article: <article_id>
Writing-Gate: G5
~~~

The validator determines the branch from repository facts:

~~~text
article blob changed → CHANGED
article blob unchanged → NO_CHANGE
~~~

The Agent does not self-report this outcome.

## Exit

Before G5 PASS, the workflow must be able to answer:

1. What is the strongest reasonable objection to each major claim?
2. Is there a reasonable competing explanation?
3. What condition would materially weaken the claim?
4. After checking, does claim strength still match the evidence and counterfactual pressure?

G5 may PASS only when the major claims retain clear and defensible boundaries after pressure testing.

If a G5-authorized article change is required, complete it through CHANGED.

If the full check requires no article change, KEEP may complete through G5-authorized NO_CHANGE.

If the result is STOP_CONFLICT, do not PASS and do not advance state.
