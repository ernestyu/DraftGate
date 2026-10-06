# DraftGate Core Language Normalization SPEC

Status: FROZEN CANDIDATE FOR AUDIT  
Date: 2026-10-06  
Repository: `ernestyu/DraftGate`

## 1. Purpose

This SPEC defines a narrow normalization of DraftGate public Core rule language.

The target is:

```text
English contract language
+
language-neutral semantics
+
author-neutral defaults
+
unrestricted article language
```

This is not a writing-system redesign.

The implementation may translate and normalize public Core wording, examples, and tests, but it MUST NOT change Gate authority, lifecycle behavior, state semantics, or Persistent Custom Rules behavior.

---

## 2. Authority and baseline

### 2.1 Semantic authority

DraftGate v1.0.0 is the semantic authority for this normalization.

```text
Repository:
ernestyu/DraftGate

Tag:
v1.0.0

Tag target:
ef7bb831992e058e7c81b31c7bf90ca327713e8c
```

All G1–G7 Gate responsibilities and lifecycle semantics are frozen against that authority.

### 2.2 Working repository baseline

The SPEC is authored from current main:

```text
b32e4b8c602dbee83912c1871f3b1da9d3686681
```

The difference between the v1.0.0 tag target and this current main is reader-facing English translation material under `articles/`; it does not redefine Gate or runtime authority for this task.

---

## 3. Background

DraftGate public Core is already mostly author-neutral and language-neutral in semantics.

Shared Core files are already English-oriented:

```text
docs/writing/commentary/base-rules.md
docs/writing/commentary/structure-rules.md
docs/writing/commentary/language-rules.md
docs/writing/commentary/checklist.md
docs/writing/commentary/ai-trace/rules.md
```

However, Gate contracts are not language-normalized:

```text
G1  Chinese-dominant
G2  Chinese
G3  Chinese-dominant
G4  Chinese
G5  Chinese-dominant
G6  English
G7  English
```

This creates an unnecessary presentation bias in the public Core even where the actual semantics are already language-neutral.

The goal is to make public Core internally consistent:

```text
Core contract language = English
Article language = unrestricted
Custom Rules = empty by default
```

English is the implementation language of the public contract. It is NOT the required language of user articles.

---

## 4. Public Core boundary

For this SPEC, public Core includes the following rule and registry surfaces.

### 4.1 Gate contracts

```text
docs/writing/commentary/gates/01-main-question.md
docs/writing/commentary/gates/02-scope-branch-control.md
docs/writing/commentary/gates/03-argument-architecture.md
docs/writing/commentary/gates/04-reader-accessibility.md
docs/writing/commentary/gates/05-claim-evidence-boundary.md
docs/writing/commentary/gates/06-paragraph-organization.md
docs/writing/commentary/gates/07-final-language-ai-trace.md
```

### 4.2 Shared Core resources

```text
docs/writing/commentary/base-rules.md
docs/writing/commentary/structure-rules.md
docs/writing/commentary/language-rules.md
docs/writing/commentary/checklist.md
docs/writing/commentary/ai-trace/rules.md
```

### 4.3 Core routing metadata

```text
docs/writing/commentary/gate-registry.json
```

### 4.4 Core-facing documentation and tests

Minimal changes are allowed when necessary to keep contract documentation and semantic tests aligned:

```text
README.md
tests/test_writing_author_voice.py
tests/test_writing_g1_insight.py
tests/test_writing_g3_central_frame.py
tests/test_writing_g5_adversarial.py
new Core-neutrality tests
```

Other tests may be updated only when they contain assertions tied to Chinese wording rather than semantic behavior.

---

## 5. Out of scope

This normalization MUST NOT modify:

```text
G1–G7 count
Gate order
Gate authority
one invocation = one Gate
schema v4
Selectable Entry
same-commit semantics
freshness semantics
NO_CHANGE semantics
reopen semantics
start-cycle semantics
reconcile semantics
writing branch lifecycle
evidence refs
archive semantics
closeout semantics
automatic closeout
Persistent Custom Rules design
Core > Custom precedence
per-Gate Custom Rule isolation
Pre-G1 semantics
```

No runtime/state redesign is authorized.

The implementation MUST NOT introduce:

- a new Gate;
- a new state field;
- a new runtime status;
- new lifecycle commands;
- new persistence semantics;
- new Custom Rules defaults;
- a new article-language restriction.

---

## 6. Definition of language-neutral Core

A public Core rule is language-neutral when its validity depends on writing function, reasoning, evidence, reader comprehension, structure, or workflow responsibility rather than on the vocabulary, punctuation, grammar, formatting customs, or author voice conventions of a particular natural language.

Allowed public Core examples include:

- require one primary question;
- distinguish observation from explanatory insight;
- require a coherent Explanatory Spine;
- preserve claim/evidence boundaries;
- avoid unsupported causal claims;
- prevent paragraph fragmentation when semantic responsibility is split artificially;
- detect repeated mechanical rhetorical patterns;
- require explanatory analogies to map correctly to the real mechanism.

Public Core MUST NOT prescribe:

```text
specific Chinese words or phrases
specific English words or phrases
Chinese heading conventions
English Title Case
language-specific punctuation
fixed paragraph length
fixed sentence length
specific word count
specific character count
mandatory or forbidden first-person usage
connector blacklists
language-specific phrase blacklists
author-specific tone
publication-specific style
```

A rule that cannot be expressed without referring to one language's wording conventions does not belong in public Core unless the rule is itself about detecting a universal functional pattern and uses language-specific examples only as non-authoritative illustrations.

---

## 7. English contract language vs article language

After implementation:

```text
G1–G7 contract language = English
Shared Core contract language = English
Article language = unrestricted
```

The Core MUST explicitly distinguish these concepts.

English contract language means:

- rule definitions are written in English;
- headings, contract prose, exit conditions, and examples are expressed in English;
- public tests should assert semantic English anchors rather than Chinese wording.

It does NOT mean:

- articles must be English;
- headings in articles must be English;
- English rhetoric is preferred;
- English grammar or style conventions become normative.

README MUST state this distinction clearly if it is not already sufficiently explicit.

---

## 8. Gate semantic preservation

Translation and normalization MUST preserve the existing v1.0.0 Gate responsibilities.

### 8.1 G1 — Main Question & Thesis

G1 MUST continue to require:

```text
Main Question & Thesis
Insight Test
correct observation != explanatory insight
novelty not required
forced profundity forbidden
weak insight → no PASS
weak insight → state unchanged
weak insight → no advance
```

G1 MUST continue to distinguish descriptive consequences from an explanatory mechanism, relationship, constraint, structural role, or structural change.

The implementation MUST preserve the rule that Insight Test failure is a conversational waiting condition, not a new runtime status.

### 8.2 G2 — Scope & Branch Control

G2 MUST continue to preserve:

```text
core
support
boundary
separate-article candidate
single center
no architecture redesign
```

G2 MUST NOT absorb G3 structure work.

### 8.3 G3 — Argument Architecture + Draft Construction

G3 MUST continue to preserve:

```text
human-selected Narrative Mode
one primary driver
Explanatory Spine
Narrative Mode != Explanatory Spine
Central Frame != Explanatory Spine
Material Hierarchy
Compression Test
substantive first draft requirement
outline / section skeleton cannot PASS
preserve substantive existing prose
draft construction necessity != downstream Gate responsibility
G1 thesis unchanged
G2 scope unchanged
```

No translation may weaken the human selection requirement.

No normalization may turn narrative-mode examples into mandatory templates.

### 8.4 G4 — Reader Accessibility

G4 MUST continue to preserve:

```text
reduce reader effort
without deleting mechanism
without deleting boundary
analogy/scenario for explanation only
analogy != evidence
analogy must map correctly
analogy must return to the real mechanism
analogy cannot establish causality
G3 architecture boundary
G5 claim-strength boundary
```

G4 MUST NOT imply Chinese rhetorical habits, English rhetorical habits, or a preferred metaphor style.

### 8.5 G5 — Claim & Evidence Boundary

G5 MUST continue to require:

```text
strongest reasonable objection
alternative mechanism
counterfactual / falsification condition
```

The allowed outcome vocabulary remains:

```text
KEEP
NARROW_SCOPE
LOWER_STRENGTH
ADD_CONDITION
ADD_COMPETING_EXPLANATION
REMOVE_UNSUPPORTED_CLAIM
STOP_CONFLICT
```

G5-authorized NO_CHANGE MUST remain unchanged.

A KEEP decision may use NO_CHANGE only after the full pressure test has been completed and no necessary G5-authorized article modification exists.

### 8.6 G6 / G7

G6 and G7 are already English-oriented.

Their semantics MUST remain unchanged.

Only minimal normalization is allowed if required to remove a language-specific example or keep terminology consistent with G1–G5.

---

## 9. Example normalization policy

Translation is not required to be mechanically sentence-for-sentence.

Each existing example in G1–G5 MUST be classified as one of:

```text
A. universal explanatory example
B. language-specific illustration
C. unnecessary illustration
```

Implementation behavior:

### A. Universal explanatory example

Translate to English while preserving the same semantic function.

### B. Language-specific illustration

Replace with a language-neutral logical example where possible.

If a language-specific example is useful only to illustrate a universal functional pattern, it may be retained only if:

- it is clearly labeled as an example;
- it is not treated as a rule;
- it does not create a default wording template;
- equivalent examples in other languages would satisfy the same contract.

### C. Unnecessary illustration

Remove it if the contract is already clear without it.

Examples MUST remain explanatory artifacts, not normative templates.

---

## 10. G4 analogy/scenario normalization

G4 receives special review because rhetorical examples can accidentally imply language-specific writing style.

The retained public contract is:

```text
analogy may explain a mechanism
analogy must map correctly
analogy must return to the real mechanism
analogy cannot replace evidence
analogy cannot prove causality
```

The implementation MUST remove or neutralize any example whose force depends on a Chinese rhetorical convention or any English-specific rhetorical convention.

No analogy form is mandatory.

No narrative flourish is required for G4 PASS.

---

## 11. Persistent Custom Rules

This task MUST NOT change the Persistent Custom Rules design.

The following files must remain default-empty scaffolding:

```text
.writing-rules/G1.md
.writing-rules/G2.md
.writing-rules/G3.md
.writing-rules/G4.md
.writing-rules/G5.md
.writing-rules/G6.md
.writing-rules/G7.md
```

No author preference discovered during normalization may be migrated into public default Custom Rules.

No normalization may use Custom Rules as a place to preserve language-specific public Core policy.

---

## 12. Gate registry preservation

`docs/writing/commentary/gate-registry.json` MUST preserve:

- workflow identity;
- gate count;
- gate order;
- rule path for every Gate;
- resource path for every Gate;
- `allow_no_change` values;
- execution mode.

The implementation may update no registry semantics unless required only for path-preserving terminology consistency.

Expected Gate order remains:

```text
G1
G2
G3
G4
G5
G6
G7
```

G5 remains the only currently authorized production NO_CHANGE Gate unless existing v1.0.0 registry authority already says otherwise.

---

## 13. Automated neutrality validation

Implementation MUST add a static public-Core neutrality regression test.

The preferred design is a test module, for example:

```text
tests/test_writing_core_language_neutrality.py
```

It MUST inspect all public Core files listed in §4.

The test MUST validate at least:

1. all G1–G7 contract files are English contract documents;
2. no public Core file imposes an author persona;
3. no public Core file imposes a first-person policy;
4. no public Core file imposes a fixed heading style;
5. no public Core file imposes fixed paragraph/sentence/word/character lengths;
6. no public Core file contains a language-specific phrase blacklist as policy;
7. no public Core file makes Chinese or English the required article language;
8. default Custom Rules remain empty scaffolding;
9. registry still points to the same G1–G7 contracts.

### 13.1 Static validator limits

The neutrality validator MUST NOT pretend that a short blacklist can prove full semantic neutrality.

Therefore:

- static forbidden-pattern checks are allowed for known prohibited policy forms;
- tests should also assert required neutral statements;
- tests must not reject harmless discussion of prohibited concepts, such as a rule saying “Do not impose fixed paragraph length.”

The validator must distinguish:

```text
prohibition of a language-specific policy
vs
presence of that policy
```

### 13.2 English-contract detection

The implementation MUST include a deterministic regression check that prevents G1–G5 from returning to Chinese-dominant contract prose.

The exact mechanism is implementation-defined, but it must be conservative and reviewable.

Acceptable approaches include:

- rejecting CJK code points in normative G1–G7 contract prose, while allowing explicitly marked example blocks when justified;
- or enforcing that any remaining non-English text is confined to clearly labeled non-normative examples.

The preferred end state is no Chinese normative prose in G1–G7.

---

## 14. Semantic regression tests

Existing semantic tests MUST be updated from wording-specific Chinese assertions to English semantic anchors.

At minimum:

### G1 tests

Must continue to prove:

```text
Insight Test exists
correct observation != explanatory insight
explanatory value required
consequence aggregation insufficient
weak insight cannot PASS
weak insight does not advance state
novelty not required
forced profundity forbidden
claim inflation forbidden
```

### G3 tests

Must continue to prove:

```text
Narrative Mode requires explicit user selection
one primary driver
Central Frame optional
Explanatory Spine required
Narrative Mode != Explanatory Spine
Central Frame != Explanatory Spine
major sections bind to spine
Compression Test required
G1 thesis cannot be silently rewritten
Draft Construction required when draft incomplete
no fixed length threshold
existing substantive prose preserved
G3 does not take over G4–G7
```

### G5 tests

Must continue to prove:

```text
strongest reasonable objection
alternative mechanism
counterfactual / falsification condition
KEEP only after pressure test
KEEP can use changed path when needed
G5-authorized NO_CHANGE
STOP_CONFLICT does not advance
no mandatory opposition section
precision is not reduced for narrative elegance
```

Tests MUST validate behavior/contract semantics rather than preserve Chinese wording.

---

## 15. Shared Core preservation

The shared Core files listed in §4.2 are already largely English and neutral.

Implementation MUST NOT broadly rewrite them.

They may change only when one of the following is true:

1. a minimal terminology sync is needed because G1–G5 terminology becomes standardized in English;
2. a remaining language-specific or author-specific public policy is discovered;
3. a neutrality statement is needed to make an existing boundary explicit.

Any such change must be minimal and called out in implementation audit notes.

---

## 16. README requirement

README MUST make clear:

```text
Core contract language = English
Article language = unrestricted
```

The README should state that DraftGate can process articles in Chinese, English, or other languages, and that English is only the public rule language.

README MUST NOT imply that English is the preferred article language.

No broader README rewrite is authorized.

---

## 17. Proof that Gate authority did not change

Implementation audit MUST provide a semantic-preservation matrix.

At minimum:

| Gate | Frozen authority | Normalized contract | Semantic result |
| --- | --- | --- | --- |
| G1 | v1.0.0 | English | unchanged |
| G2 | v1.0.0 | English | unchanged |
| G3 | v1.0.0 | English | unchanged |
| G4 | v1.0.0 | English | unchanged |
| G5 | v1.0.0 | English | unchanged |
| G6 | v1.0.0 | English | unchanged |
| G7 | v1.0.0 | English | unchanged |

For G1, G3, and G5 the audit evidence MUST include passing semantic tests.

For G2 and G4, implementation should add or update focused tests if current coverage does not sufficiently protect the frozen authority.

For G6/G7, existing tests must continue to PASS.

---

## 18. Tests

Implementation acceptance requires:

### 18.1 Neutrality

```text
G1–G7 English contract language              PASS
no author persona in public Core             PASS
no fixed first-person policy                 PASS
no fixed heading style                       PASS
no fixed paragraph/sentence length           PASS
no language-specific phrase blacklist        PASS
article language unrestricted                PASS
Custom Rules default empty                   PASS
```

### 18.2 Semantic preservation

```text
G1 Insight Test semantics                    PASS
G2 scope semantics                           PASS
G3 Narrative Mode semantics                  PASS
G3 Explanatory Spine semantics               PASS
G3 Draft Construction semantics              PASS
G4 accessibility/analogy boundaries          PASS
G5 pressure-test semantics                   PASS
G5 NO_CHANGE semantics                       PASS
G6 semantics                                 PASS
G7 semantics                                 PASS
```

### 18.3 Runtime preservation

All existing runtime/lifecycle/state tests MUST continue to PASS.

No runtime test may be weakened merely because this task is documentation-heavy.

### 18.4 Full suite

```text
./writing test
```

or the repository-equivalent full writing test command MUST PASS.

GitHub Writing Workflow CI MUST PASS.

---

## 19. Implementation sequence

After SPEC audit PASS, implementation should proceed in this order:

1. normalize G1 to English;
2. normalize G2 to English;
3. normalize G3 to English;
4. normalize G4 to English;
5. normalize G5 to English;
6. inspect G6/G7 for terminology-only synchronization;
7. inspect shared Core for minimal required synchronization only;
8. update semantic tests from Chinese wording assertions to English semantic anchors;
9. add Core-neutrality regression test;
10. update README with Core-language/article-language distinction if needed;
11. verify default Custom Rules remain empty;
12. run full test suite and CI;
13. produce semantic-preservation matrix for audit.

Do not combine this task with lifecycle, state, release, article, or Custom Rules redesign.

---

## 20. Fail-closed policy

Implementation MUST stop and request audit clarification if normalization appears to require any of the following:

- changing Gate authority;
- changing a Gate exit condition;
- changing runtime/state behavior;
- adding a language-specific writing preference to public Core;
- moving an author preference into default Custom Rules;
- changing G5 NO_CHANGE authorization;
- changing Narrative Mode user-selection semantics;
- changing G3 Draft Construction responsibility;
- changing G4/G5 authority boundary;
- changing article-language eligibility.

If an existing Chinese rule cannot be translated without deciding between two materially different semantics, implementation MUST NOT choose silently.

---

## 21. Acceptance criteria

Final acceptance requires:

```text
G1–G7 Core language               English
Shared Core language              English
Core author neutrality            PASS
Core language neutrality          PASS
Custom Rules default empty        PASS
Article language unrestricted     PASS
Gate semantics unchanged          PASS
Runtime/state semantics unchanged PASS
Existing writing CI               PASS
```

No implementation is authorized until this SPEC passes audit.

---

## 22. Audit questions

Audit should explicitly review:

1. Is the public Core boundary complete and neither too narrow nor too broad?
2. Does “English contract language” remain clearly separate from article-language policy?
3. Are the G1–G5 frozen semantic requirements complete enough to prevent translation drift?
4. Is the example-normalization policy strict enough to prevent English replacing Chinese as a new stylistic default?
5. Does the neutrality validator avoid both false confidence and trivial blacklist-only enforcement?
6. Should CJK be completely absent from G1–G7 normative contract prose, or may clearly labeled non-normative examples retain it?
7. Is README clarification sufficient without changing product positioning?
8. Are there any existing tests whose Chinese wording assertions encode real semantics not fully captured by this SPEC?
