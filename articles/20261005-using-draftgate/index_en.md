# DraftGate User Guide (Working Title)

When people first use AI to write an article, the task often seems simple: tell the model your ideas, materials, and requirements, and it should be able to produce a complete article directly. For long-form writing that requires repeated judgment, structural control, and clear evidence boundaries, this approach quickly exposes problems. The main point may drift, the structure may become loose, and the relationship between examples and arguments may become unstable. When you ask the model to revise one place, it may also change parts that were already settled.

Another approach is to keep adding prompts, writing skills, and writing rules, hoping that a more complex set of instructions will make AI write the whole article correctly in one pass. But more rules do not automatically make complex writing controllable. The model still has to deal with different questions at the same time: “What is this article really trying to answer?”, “Which materials should be kept?”, “How should the structure move forward?”, “Which claims are too strong?”, “How should paragraphs be organized?”, and “Does the final language sound natural?” Putting all of these responsibilities into one execution increases the risk that they interfere with each other, especially in long-form writing that requires multiple rounds of revision and several levels of judgment.

This article asks one question: **How can DraftGate turn AI-assisted writing from a hard-to-control, one-shot “generate the whole article” task into a process that a person can discuss, judge, revise, and verify step by step?**

The core judgment is that human-in-the-loop remains important for complex long-form writing that requires repeated judgment, revision, and checking. A person needs to stay involved in the key decisions throughout the writing process rather than handing a topic to AI and waiting for a final product. AI can participate in discussion, propose ideas, look for counterexamples, check facts and evidence, help organize the structure, and improve expression, but the article's important decisions still require ongoing human participation. DraftGate separates these different kinds of writing responsibilities into seven stages, G1–G7, with each Gate handling only one kind of problem. It then uses Git state to record where the article currently is and CI to automatically validate Gate order, state consistency, and whether state transitions are legal after every commit.

This article focuses on how to use DraftGate in practice rather than developing an abstract theory of AI writing. It starts from preparation and uses the creation of this tutorial itself as the running example: from the initial vague idea of “write a DraftGate tutorial” all the way through later checks, revisions, reopen, and a new cycle.

## 1. Why writing needs to be split into multiple stages

DraftGate does not start from the assumption that “AI cannot write.” The problem is that complex writing contains many different levels of judgment at the same time. For example, whether the main question is correct belongs to G1; whether an example is off-topic belongs to G2; how the whole article should progress belongs to G3; whether an ordinary reader can understand a concept belongs to G4; whether a claim is too strong belongs to G5; whether each paragraph has a clear argumentative responsibility belongs to G6; and whether the final language contains mechanical repetition belongs to G7.

You can, of course, tell the model all of these requirements at once, but for complex long-form writing that needs multiple rounds of revision, this usually creates two risks. First, the model has to handle many constraints at different levels at the same time. Second, when changing one level, it may also change another level that has already been settled. You may only want to revise the language in one paragraph, but the model may also change the argument; you may only want to add one example, but it may reorganize the article structure.

DraftGate handles this by separating responsibilities. One invocation, meaning one explicit Agent execution, handles only one Gate. After the current Gate is complete, the article and state are committed together, and execution stops. Whether to continue is decided explicitly by the user. The point is not to turn writing into an assembly line, but to give human judgment a clear place to land: when you are discussing the thesis, discuss only the thesis; when you are working on structure, do not simultaneously redo language and evidence.

This is also what human-in-the-loop means in DraftGate. The person does not wait until the end to “accept” an article written by AI. The person participates in decisions at every important point.

## 2. Preparation

The simplest way to use DraftGate is to prepare your own copy of the GitHub repository. Open the DraftGate repository:

```text
https://github.com/ernestyu/DraftGate
```

Choose **Fork** in the upper-right corner of the GitHub page and copy the repository into your own GitHub account. You will then get an address similar to:

```text
https://github.com/<your-name>/DraftGate
```

Your later articles, state, Custom Rules, and GitHub Actions all live in this fork and do not modify the original DraftGate repository. Next, you need an AI Agent that can read and modify a GitHub repository. It can be ChatGPT with GitHub access or another Agent that can read files, edit files, and create Git commits. Give it the URL of your fork and explicitly tell it to read:

```text
AGENTS.md
docs/writing/commentary/workflow.md
```

These two files tell the Agent that it may execute only one Gate at a time, which rules it should read, when it must stop, and how the article and state must be committed together.

If you use DraftGate locally, you can also clone your fork directly. DraftGate itself requires only Git and Python 3.10+. It does not need Docker, a database, or a self-hosted runner. The included GitHub Actions workflow uses GitHub-hosted runners, so ordinary users do not need to maintain their own server.

When starting a new article, first create the Markdown file:

```bash
./writing bootstrap --article-id 20261005-example-topic --title "Working Title"
```

This creates:

```text
articles/20261005-example-topic/index.md
```

There is one easy point to miss here: **do not rush directly into G1 immediately after creating the file.** Before DraftGate's formal state control begins, there is an important Pre-G1 stage.

## 3. Pre-G1: clarify the idea first

Pre-G1 can be understood as brainstorming. It is not part of the state machine, has no Gate ID, and has no PASS / FAIL. This is the stage where you and the AI are allowed to discuss ideas freely.

You can say, “I want to write an article about AI writing, but I have not figured out the angle yet.” You can continue asking: “What is actually worth writing about here?”, “What exactly am I dissatisfied with in current AI writing tools?”, or “Is this question too broad?”

The goal of Pre-G1 is not to produce an article. It is to help you gradually understand why you want to write, what you want to discuss, and what question the article may need to answer. This tutorial itself is an example. At the beginning, we had only one sentence: “Write a DraftGate tutorial.” If we had entered G1 immediately, the main question would probably have been only “How do you use DraftGate?”, and the article could easily have become an expanded README. After several rounds of open discussion, the real question gradually became clear: why one-shot generation and complex writing skills still tend to become hard to control, and how DraftGate breaks human judgment into controllable steps.

Once the direction is reasonably clear, initialize the state:

```bash
./writing init --article-id 20261005-example-topic
```

From this moment on, the article formally enters the controlled G1→G7 process.

## 4. G1 — Main Question & Thesis

G1 handles the highest-level question: **What is this article actually answering, and what is its core judgment?** It does not organize the table of contents and does not polish language. If the main question itself is wrong, a complete structure later will only make the wrong question more completely written.

When entering G1, Pre-G1 had already established that this article was not merely “software instructions.” The final main question was: “How can DraftGate turn AI-assisted writing from a hard-to-control whole-article generation task into a process that a person can discuss, judge, revise, and verify step by step?”

The core judgment, or thesis, was also frozen: for complex long-form writing that requires repeated judgment, revision, and checking, human-in-the-loop remains important; DraftGate separates responsibilities through G1–G7 and then uses Git state and CI to move execution order and validation outside the model. Here, the thesis can be understood as the core answer the article intends to give.

After G1 completes, the state advances from `current_gate = G1` to `current_gate = G2`, and G1 is added to completed. This is a good point to stop and ask: is this really the question you want to write about? If not, do not enter G2.

## 5. G2 — Scope & Branch Control

G2 controls the article boundary, or scope: what belongs in this article, and what should remain outside even if it is related. Many articles do not suffer from having too little content, but from trying to include everything. At this Gate, material needs to be separated into categories: what belongs to the main line, what is only a supporting branch, and what is interesting but should not enter this article.

G2 ultimately froze three main areas: preparation, Pre-G1 brainstorming, and the real execution process from G1 through G7. It also excluded broader Prompt Engineering, Agent architecture, CMS, and publishing systems. Those topics are not unimportant, but if they were all included, the tutorial would drift from “how to use DraftGate” into “a survey of AI writing system design.”

After G2, the article already knows “what it is answering” and “what belongs in this article,” but it has not yet decided how to tell the story and may still not have a complete body draft.

## 6. G3 — Argument Architecture + Draft Construction

G3 is the stage that changed most during the development of this system, and it was also where the first dogfood cycle exposed the most problems.

The first part is Argument Architecture. Based on the G1 main question and G2 scope, the Agent proposes 1–3 suitable narrative modes, meaning the main way the article moves forward. For example, question-driven means the article progresses by going deeper into one question; case-driven means it follows a real case; hybrid allows both, but one must remain the clear primary line. The Agent cannot choose this automatically. The user must explicitly approve it.

For this tutorial, question-driven was selected as the primary driver, while the tutorial's own creation process was used as a case-driven secondary device. In other words, the article mainly moves forward around the question “How do we make AI writing controllable?”, while the real dogfood process repeatedly grounds the explanation. G3 then builds an Explanatory Spine. This is not a table of contents. It is the actual reasoning chain of the article: if you remove headings, examples, and rhetoric, how does the article move step by step from its starting point to its final judgment? The spine of this article can be compressed as follows: one-shot generation gives many kinds of writing responsibility to the model at the same time, making stable control difficult; human-in-the-loop requires breaking human judgment into consecutive stages; DraftGate then uses state and CI to turn these stages into an executable and verifiable process.

The second part is Draft Construction. This responsibility was added after the first dogfood cycle. In the first run, G3 created a complete structure, but many sections contained only one or two sentences. They were only a section skeleton: we knew what each section should do, but the actual prose had not been developed. G4–G7 then worked correctly within their own responsibilities, and all Gates eventually passed, but the article was still only a “structurally correct outline.” This exposed a practical gap: no Gate was explicitly responsible for expanding a skeleton into a complete first draft.

G3 now carries that responsibility. If the article is still a seed, outline, section skeleton, or placeholder-heavy draft, G3 cannot PASS. Every major section must contain substantive prose that actually performs its explanatory, argumentative, or tutorial responsibility instead of only headings and outline notes.

This does not mean G3 should also do all later work in advance. It may write prose, explanation, and transitions, but it must not preempt G4's accessibility audit, G5's evidence pressure test, G6's paragraph organization, or G7's final language cleanup. The second dogfood cycle re-entered from G3 precisely to validate this change. The structure from the first cycle was preserved, while the sections that had originally been too thin were expanded into complete tutorial prose.

## 7. G4 — Reader Accessibility

G4 no longer decides what the article “says.” It checks whether the reader can follow it. Terms such as fork, state, CI, Gate, and human-in-the-loop may feel natural to technical users, but ordinary readers may not know what they mean. G4 checks this kind of comprehension barrier.

The first G4 pass added these explanations: a fork is a copy of the repository in your own GitHub account; state is the JSON file that records the current Gate, completed Gates, and article revision; revision here means the version identifier for the article in Git; CI is the automatic validation that runs after every commit; and Agent means an AI tool that can read and write the repository and commit Git changes.

The G4 criterion is not “use as few technical terms as possible.” The question is whether readers have enough explanation to continue when they first encounter an important concept.

## 8. G5 — Claim & Evidence Boundary

G5 handles claim strength and evidence boundaries. A claim is a judgment the article asks the reader to accept. G5 asks: are any of these judgments too absolute? Is there a reasonable alternative explanation? What is the strongest counterargument? Which statements need conditions?

The first G5 pass encountered a typical problem. The original text said, “Good articles still require human-in-the-loop.” That was too broad, because simple, highly structured, low-risk writing tasks may be perfectly adequate with one-shot generation.

G5 eventually narrowed this to: “For complex long-form writing that requires repeated judgment, revision, and checking, human-in-the-loop remains important.” This looks like only a few added qualifiers, but what changed was the claim boundary, not the writing style.

## 9. G6 — Paragraph Organization

G6 looks only at paragraph responsibility. It does not prescribe “how many words a paragraph should contain,” and it does not declare that a one-sentence paragraph is always wrong. The real criterion is whether one paragraph carries one relatively complete semantic or argumentative responsibility.

If two paragraphs are really performing one argumentative action, they should be considered for merging. If one paragraph contains several different responsibilities, it should be considered for splitting. In the first G6 pass, the paragraphs “this is a tutorial” and “the scope of the tutorial” were separate, but they performed the same framing action, so they were ultimately merged.

This matters because DraftGate Core should not prescribe whether a particular author prefers long or short paragraphs. Paragraph aesthetics belong in Custom Rules, not Core.

## 10. G7 — Final Language & Pattern Audit

G7 is the final language and mechanical-pattern check. By this point, the main question, scope, architecture, claim boundary, and paragraph organization are already frozen, meaning these higher-level decisions are no longer redone by G7. G7 handles only the final expression layer.

It mainly checks repeated meta-signposting, repeated use of the same sentence pattern, templated section openings, fixed strong endings, mechanical parallelism, and other AI traces. The first G7 pass removed repeated framing such as “this section...,” “here...,” and “looking back...,” but did not change the structure again.

After G7, current_gate becomes null and status becomes complete. This means the current cycle is finished and DraftGate releases control of the article.

## 11. What if you are not satisfied: reopen and a new cycle

DraftGate does not treat one G1→G7 pass as a permanent final draft.

One case is when the current cycle is still in progress and you are dissatisfied with the Gate that just finished. For example, G4 has just completed and the state has already advanced to G5, but you think G4's explanation is wrong. You can run:

```bash
./writing reopen --article-id 20261005-example-topic
```

reopen can only return to the most recently completed Gate. It does not automatically change the article. It only restores the state to that Gate, after which you discuss and execute it again with the Agent.

Another case is when G1–G7 are already complete, but the article still needs systematic rework after you read it again. Then start a new cycle:

```bash
./writing start-cycle --article-id 20261005-example-topic --from G3
```

The principle is to begin from the earliest affected Gate: if the main question changed, start from G1; if the scope changed, start from G2; if the structure or draft development needs work, start from G3; if readers have comprehension problems, start from G4; if there is an evidence problem, start from G5; if paragraph organization needs work, start from G6; if the issue is only language, start from G7.

This tutorial itself is a real example. The first G1→G7 cycle fully passed, but the article remained too thin even though the structure was complete. The problem belonged to architecture / draft development, so the process did not restart from G1. Instead, cycle 2 started from G3.

In DraftGate, multiple cycles are treated as normal use, not as evidence that one cycle failed. Each cycle uses the current article as a new baseline and re-enters from the earliest point that needs systematic revision.

## 12. Building your own writing style: Persistent Custom Rules

DraftGate Core is intentionally author-neutral. It does not prescribe whether you must use first person or third person, how long paragraphs must be, what format titles must follow, or include an author's private banned-word list.

Over time, users usually develop their own preferences. For example, you can tell the Agent: “In G6, keep complete long paragraphs when possible. Do not split paragraphs frequently just for visual rhythm.” If you explicitly say this is a long-term rule, the Agent can save it in the corresponding Gate's Custom Rules, such as `.writing-rules/G6.md`.

Ordinary users do not need to open these files and maintain them manually. You only need to say things like “keep this rule from now on” or “remove that long-term rule,” and the Agent maintains the files. There is one strict boundary: when executing Gx, only Gx's Custom Rules may participate. A G3 preference cannot silently enter G4, and a G6 paragraph preference cannot affect G5's evidence judgment.

Core also has higher priority than Custom Rules. If a personal rule conflicts with Core, Core applies, the conflicting Custom Rule is ignored for that execution, the Agent should explicitly tell you about the conflict, and the workflow state must not change merely because the conflict exists. This keeps Core general while still allowing users to gradually develop their own writing system through long-term use.

## 13. You can still edit freely after complete

When state has reached `status = complete`, DraftGate releases the article. At that point, you can continue chatting normally with the Agent and ask for a shorter paragraph, another example, a different title, or a revised ending. These edits do not require state and do not automatically become Custom Rules.

If the change is local, just make the change. If the revision grows until the article's structure or argument has changed substantially, start a new cycle from the earliest affected Gate.

## 14. Looking back: what DraftGate actually controls

The whole process can be summarized as: prepare GitHub / Fork / Agent → Pre-G1 brainstorm → G1 Main Question & Thesis → G2 Scope → G3 Architecture + Draft Construction → G4 Reader Accessibility → G5 Claim & Evidence Boundary → G6 Paragraph Organization → G7 Final Language & Pattern Audit → complete.

If the current Gate is unsatisfactory, you can reopen it; if the whole cycle has ended but you want systematic revision, use start-cycle --from Gx; if the change is only local, edit freely after complete. Meanwhile, long-term style preferences can gradually accumulate in the Custom Rules for the corresponding Gates.

The system separates three roles: the person makes key judgments, AI handles discussion and editing, and Git/state/CI records and validates the process. DraftGate's value is not that it automatically writes an entire article for you, but that it turns AI-assisted writing into a process that can be paused, checked, redone, and improved step by step.

This tutorial itself is also a validation of the method. In the first cycle, we successfully completed G1–G7, but discovered that “the structure is correct” does not mean “the body is complete.” We then changed G3 so that it also owns Draft Construction and started a second cycle from G3. This process shows at least one thing: for this kind of writing workflow, it is not enough for the rules to be logically consistent on paper; real dogfood can expose responsibility gaps that static checks are unlikely to reveal.
