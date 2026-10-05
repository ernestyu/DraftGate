# DraftGate G3 Draft Construction + Persistent Custom Rules SPEC

Status: FROZEN FOR AUDIT
Scope: design only; no implementation in this commit

## 1. Purpose

This SPEC addresses gaps found during a full DraftGate dogfood run on:

`articles/20261005-using-draftgate/index.md`

The dogfood completed G1→G7 successfully, but the resulting article remained structurally complete while still too thin to function as a full tutorial. The run also confirmed the need to document Pre-G1 brainstorming, persistent user style rules, reopen behavior, selectable entry, and multi-cycle refinement more clearly.

This SPEC changes the workflow only where needed to close those gaps.

## 2. Frozen design goals

The implementation MUST:

1. extend G3 so that it owns both argument architecture and construction of a complete first draft when the article is still only a seed, outline, or incomplete draft;
2. prevent G3 from passing when major sections remain only placeholders or short responsibility notes rather than substantive prose;
3. add persistent per-Gate Custom Rules that users can build through normal conversation with an Agent;
4. keep DraftGate Core rules separate from Custom Rules;
5. define Core contract precedence over Custom Rules;
6. document Pre-G1 as an open brainstorm stage outside state control;
7. document reopen, selectable entry, start-cycle, and multi-cycle refinement as normal usage;
8. preserve current G1→G7 order and schema v4.

## 3. Non-goals

This SPEC MUST NOT:

- add G0, G8, or any new Gate;
- change Gate order;
- change schema v4 fields;
- change same-commit semantics;
- change freshness semantics;
- change reopen semantics;
- change start-cycle semantics;
- add CMS, publishing, Hugo, cover-image, or deployment behavior;
- add user-managed configuration that ordinary users must edit manually;
- add language-specific style rules to DraftGate Core;
- introduce paragraph, sentence, or character-count thresholds;
- redefine G4–G7 responsibilities.

## 4. Pre-G1 brainstorm

Pre-G1 is a documented usage stage outside the state machine.

Flow:

`idea → open discussion / brainstorm → rough topic, motivation, and direction become clear → initialize DraftGate → G1`

Pre-G1:

- has no state file;
- has no PASS / FAIL;
- has no Gate ID;
- does not modify schema;
- may be divergent and exploratory;
- may revise or abandon the original topic;
- ends when the user can approximately explain why the article should exist, what it may discuss, and what question it may answer.

Pre-G1 MUST NOT be implemented as a state-controlled Gate.

README and workflow documentation MUST explain this distinction.

## 5. G3 authority expansion

Current G3 authority is expanded from `Argument Architecture` to `Argument Architecture + Draft Construction`.

This remains one Gate and one state transition.

### 5.1 G3 internal phases

#### G3A — Architecture

G3A preserves current responsibilities:

- Narrative Mode Decision;
- central frame decision;
- Explanatory Spine;
- Material Hierarchy;
- major section responsibilities;
- section-to-spine binding;
- Compression Test;
- G1/G2 authority boundary.

If user selection is required by the current G3 contract, state MUST remain unchanged until the user selects.

#### G3B — Draft Construction

After architecture is selected and internally coherent, G3 MUST determine whether the article already contains a substantive draft.

If the article is a seed, outline, section skeleton, placeholder-heavy draft, or materially incomplete draft, G3 MUST expand it into a complete first draft before G3 PASS.

If the article is already substantively complete, G3 MUST preserve existing prose where possible and only make changes required to align the article with the frozen architecture.

### 5.2 Draft Construction objective

G3B MUST ensure:

`major section responsibility → substantive prose that performs that responsibility`

G3 MUST NOT pass if major sections are only:

- one-line placeholders;
- section-purpose notes;
- outline bullets;
- "this section will explain..." prose;
- headings with little or no substantive development.

The implementation MUST NOT use fixed word-count, paragraph-count, sentence-count, or character-count thresholds to determine completeness.

### 5.3 Allowed G3B work

G3B MAY:

- expand explanations already authorized by G1/G2/G3;
- develop mechanisms already inside the frozen scope;
- turn section responsibilities into substantive prose;
- use existing facts, examples, and materials already present in the article or supplied by the user;
- connect sections to the Explanatory Spine;
- preserve or minimally adapt existing prose;
- add necessary transitional reasoning;
- incorporate Custom Rules applicable to G3.

### 5.4 Forbidden G3B work

G3B MUST NOT:

- replace or rewrite the G1 thesis without explicit correction-cycle authority;
- expand beyond G2 scope;
- invent facts, data, quotations, sources, or evidence;
- treat unsupported factual claims as true;
- perform G4 accessibility cleanup as a substitute for G3 drafting;
- perform G5 claim-strength pressure testing as a substitute for G3 drafting;
- perform G6 paragraph restructuring as a substitute for G3 drafting;
- perform G7 final language cleanup as a substitute for G3 drafting;
- expand text merely to increase length;
- rewrite a substantively complete draft from scratch without necessity.

### 5.5 G3 exit contract

G3 PASS requires all existing G3 architecture requirements plus `Draft Construction Check = PASS`.

Draft Construction Check passes only when:

- each major section has substantive prose;
- the prose performs the section's declared responsibility;
- the article can be read as a complete first draft rather than an outline;
- no major section remains placeholder-only;
- the article remains consistent with G1 and G2;
- later Gate responsibilities remain available for G4–G7.

## 6. Persistent Custom Rules

DraftGate MUST support a second rule layer:

`Layer 1: DraftGate Core`

`Layer 2: Persistent Custom Rules`

No third persistent layer is required by this SPEC.

Article-local edits after workflow completion remain ordinary article edits and are outside Custom Rules unless the user explicitly asks to preserve a preference for future use.

### 6.1 User interaction model

Ordinary users MUST NOT be required to edit rule files manually.

The intended interaction is conversational.

Examples:

- "Keep this as a long-term G6 preference."
- "Do not use this paragraph pattern in future articles."
- "Remove the custom rule I added about first person."
- "For G3, prefer case-driven explanation when appropriate."

The Agent is responsible for translating explicit long-term preferences into persistent Custom Rules.

The Agent MUST NOT automatically convert every local edit or one-off preference into a persistent rule.

### 6.2 Storage

Custom Rules MUST be stored separately from DraftGate Core.

Recommended layout:

`.writing-rules/G1.md` through `.writing-rules/G7.md`

A file may be absent when no custom rules exist for that Gate.

The implementation MAY choose an equivalent per-Gate storage path if needed, but it MUST preserve:

- per-Gate separation;
- Core/Custom separation;
- absence = no custom rules;
- plain-text, Git-trackable representation.

### 6.3 Loading

When executing Gate Gx, the Agent MUST load:

`Gx Core contract + declared Core resources + Custom Rules for Gx, if present`

Custom Rules for unrelated Gates MUST NOT be loaded by default.

### 6.4 Precedence

Precedence is frozen:

`DraftGate Core contract > Persistent Custom Rules`

Custom Rules MAY refine style or preferences within Gate authority.

Custom Rules MUST NOT:

- disable Core checks;
- broaden Gate authority;
- change state semantics;
- change freshness or same-commit rules;
- weaken evidence boundaries;
- weaken transition validation;
- override explicit Forbidden sections of Core Gate contracts.

If a Custom Rule conflicts with Core, Core wins and the conflict must not silently alter Core behavior.

### 6.5 Custom Rule examples

Appropriate examples:

G3:
- prefer case-driven secondary material;
- prefer fewer, larger sections;
- prefer explicit tutorial progression.

G6:
- prefer longer paragraphs when one argument action remains coherent;
- avoid repeated very short paragraphs unless functionally necessary.

G7:
- prefer first person plural;
- avoid a particular recurring phrase;
- prefer a restrained tone.

Inappropriate examples:

- skip G5 evidence checks;
- allow G6 to change thesis;
- allow G7 to rewrite architecture;
- ignore state freshness;
- disable CI validation.

## 7. Completion, free editing, reopen, and new cycles

### 7.1 After complete

When `status = complete`, DraftGate releases the article.

The user MAY then edit the Markdown freely with an Agent or by hand without state control.

These edits do not automatically become Custom Rules.

### 7.2 Reopen

While a cycle is still in progress, before the next Gate runs, the user MAY reopen only the most recently completed Gate.

Existing semantics remain unchanged.

Documentation MUST explain:

`recent Gate result is unsatisfactory → reopen → re-run that Gate`

Reopen cannot:

- roll back multiple Gates;
- operate after workflow completion;
- modify article content by itself.

### 7.3 New cycle and selectable entry

After completion, if the user wants systematic rework, use `start-cycle --from Gx`.

The user or Agent should select the earliest affected Gate.

Examples:

- thesis changed → G1;
- scope changed → G2;
- structure too thin / article needs richer development → G3;
- reader explanation problem → G4;
- claim/evidence problem → G5;
- paragraph problem → G6;
- language-only problem → G7.

Documentation MUST explain that repeated cycles are expected and valid.

DraftGate MUST NOT imply that one G1→G7 cycle creates a permanently final article.

## 8. README and tutorial documentation requirements

README.md and README.zh-CN.md MUST document:

1. Fork the repository before normal use.
2. Give the forked repository to a GitHub-capable Agent.
3. Pre-G1 brainstorm happens before state initialization.
4. G1→G7 purpose at a practical level.
5. G3 now includes first-draft construction when needed.
6. Persistent Custom Rules are built through conversation, not manual file editing.
7. Core rules override Custom Rules.
8. reopen usage.
9. start-cycle --from Gx usage.
10. multi-cycle refinement.
11. completed articles may be freely edited outside state control.

The existing dogfood article MAY be updated after implementation, but article rewriting is not part of this SPEC implementation itself unless explicitly requested in the implementation task.

## 9. Validation and tests

Implementation MUST add tests for at least the following.

### 9.1 G3 contract tests

Tests MUST assert that G3 documentation includes:

- Draft Construction;
- substantive first-draft requirement;
- outline-only / placeholder-only PASS prohibition;
- no fixed length threshold;
- preservation of G1/G2 authority;
- no takeover of G4–G7 responsibilities;
- preserve existing substantive prose when possible.

### 9.2 Custom Rule loading tests

Tests MUST assert:

- per-Gate Custom Rules are optional;
- only current-Gate Custom Rules are loaded;
- missing custom file is valid;
- Core resources remain authoritative;
- Custom Rules cannot override Core Forbidden semantics.

The implementation MAY enforce this through deterministic routing/validation, documented Agent contract, or both, but behavior MUST be test-covered.

### 9.3 Runtime regression

Existing tests for schema v4, same-commit, freshness, NO_CHANGE, reopen, start-cycle, selectable entry, and CI commit validation MUST remain PASS.

No schema migration is allowed.

## 10. Dogfood acceptance case

After implementation is complete and audited, the existing article `20261005-using-draftgate` MUST be used as a real acceptance case.

Current completed cycle remains historical evidence.

Start a new cycle:

`./writing start-cycle --article-id 20261005-using-draftgate --from G3`

Acceptance expectation:

- G3 must recognize that the current article is structurally complete but still too thin as a tutorial;
- G3 must expand the major tutorial sections into substantive first-draft prose;
- G3 must preserve G1 thesis and G2 scope;
- G4–G7 must remain responsible for their existing downstream checks;
- the resulting cycle must complete through G7 with CI PASS;
- the final article should function as an actual tutorial, not only as an outline.

## 11. Public-rule neutrality requirement

Implementation and documentation MUST preserve the public-core boundary established during dogfood.

DraftGate Core MUST remain:

- language-neutral;
- author-neutral;
- free of personal phrase blacklists;
- free of fixed paragraph-length rules;
- free of mandatory first-person policy;
- free of a prescribed heading style;
- free of user-specific voice constraints.

Persistent author style belongs only in Custom Rules.

## 12. Frozen invariants

The following remain unchanged:

- Gate count = 7
- Gate order = G1→G7
- schema = v4
- one invocation = one Gate
- same-commit semantics
- freshness fail-closed
- G7 terminal semantics
- reopen = immediately previous completed Gate only
- start-cycle requires complete state
- selectable entry requires explicit user confirmation when non-G1

## 13. Implementation boundary

This SPEC commit MUST contain no implementation.

Implementation begins only after SPEC audit and explicit approval.
