# Why AI Writing Needs Explicit State

AI can already read long contexts and understand instructions such as “only revise the structure in this round” or “check the evidence in the next step.” If all previous discussion remains in the conversation, it may seem that the model should already know how far the article has progressed. So why does complex long-form writing still need a separate explicit state?

## Two different kinds of problems

Writing involves two different kinds of problems. The first is content judgment: whether an argument is sound, whether an example is off-topic, or whether a paragraph is easy to understand. These questions do not have one mechanical answer and require the model to make semantic judgments from context. The second is workflow fact: whether a writing stage has already been completed, what may be handled next, and which article version the current revision should be based on. These facts do not need to be “understood”; they only need to be accurate.

If both kinds of responsibility remain only in the model context, the model simultaneously acts as editor and state machine. Here, a “state machine” can be understood as a strict progress record: what step the process is currently on, which steps have already been completed, and what is allowed next. The model must not only judge the content, but also remember which decisions have been frozen, which steps are complete, and whether the current version is still the one confirmed in the previous round. This may not be a serious problem in one short conversation. But once an article goes through multiple rounds of revision, reopens an earlier step, enters a new revision cycle, or is modified outside the repository workflow, the workflow facts can diverge from the model's current understanding.

## Put workflow facts outside the model

The purpose of explicit state is to move these deterministic facts out of the model. State is a machine-readable workflow record; a Gate is a stage that handles one writing responsibility; a cycle is one complete round of controlled revision. State can record the current Gate, completed Gates, cycle, article path, and article revision. The article revision can be understood as the current version's “fingerprint”: whenever the body changes, its corresponding Git identifier changes as well.

Git, in turn, provides the actual version objects. Git + structured state is only one implementation. The important condition is that workflow facts are stored by a deterministic, inspectable mechanism outside the model. The model still decides “how should this article be revised?”, but no longer has to rely on its own memory to determine “what am I allowed to change now?” Before the next step runs, the system can compare state with the article version and decide whether execution may continue.

This division becomes clearer when the version changes. Suppose the article has just finished the structure stage, and the system records that “the next step may only perform a readability check.” If someone then edits the body outside the repository workflow, the article version no longer matches the revision recorded in state. The model may still remember that “the next step is readability,” but it can no longer know whether the article in front of it is still the version confirmed in the previous round. External state and Git can detect this mismatch directly and stop the process instead of letting the model continue guessing.

This division also makes the workflow inspectable. If the model tries to skip the current stage and jump directly to a later one, the external state can reject it. If the article is modified outside the current Gate, a revision mismatch can stop execution.

After a cycle is complete, its final state can also be archived, and an evidence ref can be preserved to point to the final Gate commit. The archive is the state snapshot saved at the end of that cycle; the evidence ref is like an index card that cannot be casually rewritten and points to the actual Git commit from that moment. The former answers “what was the final state of this cycle?”, while the latter answers “which exact version did that state correspond to?”

## What external state can guarantee

Explicit state does not prove that the content itself is correct. State can confirm that “the evidence-checking stage is complete,” but it cannot prove that the judgment made there was reasonable. Git can confirm that the article has not silently been replaced by another version, but it cannot decide whether the argument is sound. Content quality still comes from the user, the model, the evidence, and the judgments made at each writing stage. External state solves a different problem: whether the process followed its constraints and which exact version produced the result now being examined.

Complex long-form writing needs to separate not only who is responsible for what, but also which tasks require semantic judgment and which tasks are only deterministic state. The former are suitable for people and models to handle together; the latter are better placed in Git and structured state. Once these responsibilities are separated, an AI writing workflow gains an external skeleton that can be verified, recovered, and continued.
