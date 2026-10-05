# DraftGate Writing Lifecycle / Repository Hygiene SPEC

Status: FROZEN FOR AUDIT
Scope: lifecycle, Git history, repository hygiene, archive, recovery UX
Implementation: NOT STARTED

## 1. Purpose

This SPEC defines the repository lifecycle around the existing DraftGate G1→G7 writing workflow.

It does not redesign writing Gates. It addresses repository history growth, evidence retention, ordinary-user Git complexity, state archival, recovery semantics, and maintenance safety discovered during real dogfood.

Primary goals:

1. keep Gate commits as execution evidence without filling `main` with Gate-level noise;
2. make normal usage Agent-first rather than Git-CLI-first;
3. preserve each completed cycle as durable evidence;
4. archive completed state per cycle without losing history;
5. reduce `reconcile` to explicit recovery-only behavior;
6. distinguish writing transactions from repository maintenance;
7. preserve Persistent Custom Rules created during a writing cycle.

## 2. Frozen invariants

This SPEC MUST NOT change:

- Gate count = 7;
- Gate order = G1→G7;
- any Gate writing authority;
- schema v4 fields or field meaning;
- one invocation = one Gate;
- same-commit semantics for Gate completion;
- freshness fail-closed semantics;
- NO_CHANGE semantics;
- reopen semantics;
- selectable entry semantics;
- `start-cycle --from Gx` decision semantics;
- Pre-G1 remaining outside state control;
- Persistent Custom Rules precedence: Core > Custom;
- per-Gate Custom Rule isolation.

## 3. Terminology

### 3.1 Active state

An in-progress cycle state at:

`.writing-state/write-commentary/<article-id>.json`

Only active/resumable workflows live in this directory.

### 3.2 Archived state

A completed historical cycle state stored per article and per cycle at:

`.writing-state/archive/write-commentary/<article-id>/c<cycle>.json`

Examples:

- `.writing-state/archive/write-commentary/example/c1.json`
- `.writing-state/archive/write-commentary/example/c2.json`

Archived states are historical evidence, not active workflow state.

### 3.3 Writing branch

A temporary branch used for exactly one article cycle:

`writing/<article-id>/c<cycle>`

### 3.4 Evidence ref

A policy-level write-once Git ref naming one completed cycle:

`writing-evidence/<article-id>/c<cycle>`

The recommended implementation is an annotated Git tag. A lightweight tag is acceptable only if implementation constraints require it.

### 3.5 Main closeout commit

The single high-level commit placed on `main` when one completed writing cycle is closed out.

## 4. Agent-first normal lifecycle

The default public workflow is:

`Fork repository → give fork URL to GitHub-capable Agent → Pre-G1 → begin writing lifecycle → writing branch → G1...G7 → closeout → main`

Ordinary users MUST NOT be required to manually execute:

- `git checkout -b`;
- `git add`;
- `git commit`;
- `git tag`;
- `git merge --squash`;
- `git branch -d`;
- direct JSON state edits.

Git CLI instructions MAY remain under an explicit Advanced / Local Usage section.

## 5. Writing branch lifecycle

### 5.1 Creation

Every new article cycle MUST run on exactly one temporary writing branch:

`writing/<article-id>/c<cycle>`

At branch creation time, the lifecycle MUST record or deterministically identify the exact `main` commit from which the writing branch was created. This is the cycle's `main_base_commit` for closeout safety.

The base identity MUST NOT require a new schema-v4 field. It MAY be derived from Git ancestry / merge-base or stored in lifecycle-specific metadata outside the writing state schema.

For a new article:

`main → record main base → create writing branch → bootstrap/article commit → init active state → execute Gates`

For a later cycle:

`main → record main base → create writing branch → create new active state from latest archived completed state → execute from selected entry Gate`

### 5.2 Gate execution

All Gate commits for the cycle MUST remain intact on the writing branch.

The implementation MUST NOT squash G1–G7 within the writing branch.

Existing same-commit, freshness, NO_CHANGE, reopen, and sequential Gate semantics remain unchanged.

### 5.3 Branch lifetime

A writing branch is temporary.

It MUST remain present until closeout has successfully completed every destructive-risk step.

It MAY be deleted only after:

1. G7 complete;
2. required CI validation PASS;
3. evidence ref created and verified;
4. main closeout commit created and verified;
5. archived state created and verified.

On any failure before completion:

`STOP → keep writing branch → keep any already-created evidence ref → do not continue silently`

## 6. Cycle-aware archive policy

Archive storage is frozen as:

`.writing-state/archive/write-commentary/<article-id>/c<cycle>.json`

Each archived state MUST correspond one-to-one with:

`writing-evidence/<article-id>/c<cycle>`

Archive is allowed only when:

- state `status = complete`;
- cycle number is valid;
- G7 completion exists;
- required CI is PASS;
- evidence ref exists and points to the expected final Gate commit;
- closeout is constructing or has constructed the corresponding main durable result.

An in-progress state MUST NOT be archived.

Archived state content MUST preserve the exact completed schema-v4 state, including:

- `article_id`;
- `cycle`;
- `entry_gate`;
- `skipped_by_user`;
- `completed`;
- `status`;
- `article_revision`.

Archive MUST NOT mutate schema v4.

## 7. Main closeout final tree

Main closeout MUST be a squash-style lifecycle operation, not a raw `git merge --squash` of the writing branch HEAD.

### 7.1 Current-main closeout safety

Closeout MUST be based on the current `main` HEAD at closeout time, not by directly constructing a result from the stale branch-creation base.

The lifecycle MUST identify:

```text
main_base_commit
writing_branch_final_commit
current_main_commit
```

If `current_main_commit == main_base_commit`, normal closeout construction may proceed.

If `main` advanced after the writing branch was created, closeout MUST compare:

```text
changes introduced by current main since main_base_commit
vs
this cycle's authorized durable changes since main_base_commit
```

Authorized durable cycle changes are limited to the objects defined by this SPEC for closeout, including:

- final article;
- durable Persistent Custom Rules changes;
- archived completed state;
- other explicitly authorized durable repository changes.

Closeout MUST NOT replace current main with the writing-branch tree.

Instead, it MUST construct the closeout tree by applying only the cycle's authorized durable changes onto the current main tree.

If current-main changes and cycle durable changes are non-conflicting:

```text
current main
+ authorized durable cycle delta
→ closeout tree
```

If both sides changed the same durable object or otherwise create an unresolved semantic/path conflict:

```text
STOP
→ do not overwrite current main
→ do not auto-resolve
→ preserve writing branch
→ preserve any already-created evidence ref
```

Custom Rules MUST receive the same conflict treatment. A cycle MUST NOT silently overwrite newer Custom Rules that landed on main after the writing branch base.

No automatic force-update, last-writer-wins behavior, or stale-base tree replacement is permitted.

The final tree of the single main closeout commit MUST contain at least:

1. the final article content from the completed writing cycle;
2. all durable Persistent Custom Rules changes produced during that cycle;
3. the archived completed state at `.writing-state/archive/write-commentary/<article-id>/c<cycle>.json`;
4. any other explicitly authorized durable repository changes produced during the cycle.

The final main closeout commit MUST NOT contain the completed cycle's active state at:

`.writing-state/write-commentary/<article-id>.json`

Therefore closeout MUST transform the writing-branch result into the durable main tree:

`final article + durable Custom Rules + archived cycle state + explicitly authorized durable changes - active cycle state`

This entire durable result MUST land in one high-level main commit.

Main history semantics are frozen as:

`main = durable product-level history`

`evidence history = Gate execution / audit history`

## 8. Persistent Custom Rules durability

Persistent Custom Rules modified during a cycle are durable user data.

Any changes under:

`.writing-rules/G1.md ... .writing-rules/G7.md`

that are valid and authorized during the writing cycle MUST be carried into the main closeout final tree.

Writing branch deletion MUST NOT discard those rule changes.

Closeout MUST compare the durable Custom Rules state from the writing branch against main and include the intended cycle changes.

Custom Rules remain subject to existing validation and Core > Custom semantics.

## 9. Evidence ref policy

Evidence refs are policy-level write-once, not technically immutable.

For expected evidence ref:

`writing-evidence/<article-id>/c<cycle>`

the implementation MUST apply:

- ref absent → create pointing to expected final Gate commit;
- ref exists and already points to the same expected commit → accept as idempotent;
- ref exists and points to a different commit → STOP;
- existing evidence ref MUST NOT be moved, overwritten, force-updated, or reused.

Evidence creation MUST happen before writing-branch deletion.

The evidence ref target MUST be the cycle's G7 completion commit.

No alternate terminal target is permitted for a normal completed DraftGate cycle.

Because prior Gate commits are ancestors of the final Gate commit, deleting the writing branch MUST still leave the complete Gate commit chain reachable through the evidence ref.

## 10. Archive to new active cycle

Starting a new cycle after archive MUST NOT modify any historical archive file.

Required semantics:

`latest archived complete state`
`→ read as historical source`
`→ current main article blob becomes new baseline`
`→ create new active state`
`→ cycle = previous cycle + 1`
`→ selected entry_gate`
`→ skipped_by_user = exact prefix before entry_gate`
`→ completed = []`
`→ current_gate = entry_gate`
`→ status = in_progress`
`→ article_revision = current main article blob`

The previous archived state remains byte-for-byte unchanged.

No user should manually copy archive JSON.

The runtime MUST provide a deterministic operation for this path, whether by extending `start-cycle` or adding a lifecycle command.

A non-G1 entry still requires explicit user confirmation under existing semantics.

## 11. Reconcile recovery-only policy

`reconcile` is frozen as exceptional recovery only.

It MUST NOT be presented as a normal writing command in the default Quick Start.

Important meaning:

`STATE STALE → reconcile`

rebinds the state to the current committed article baseline; it does NOT prove that the external article modification complied with the current Gate contract.

Required behavior:

1. Agent MUST NOT auto-run reconcile;
2. Agent MUST report article/state divergence;
3. Agent MUST explain that reconcile accepts the current committed article as new baseline without validating Gate-authority correctness;
4. explicit user confirmation is required;
5. reconcile remains state-preserving except for allowed revision rebinding under existing schema semantics;
6. reconciliation must leave auditable recovery evidence, such as a dedicated commit trailer or deterministic commit classification;
7. failure MUST be fail-closed.

## 12. Repository maintenance authority boundary

Repository maintenance is distinct from writing execution.

Repository maintenance MUST NOT modify:

- an in-progress bound article;
- an active workflow state;

unless the modification is part of an explicitly authorized lifecycle operation defined by this SPEC.

Allowed maintenance categories and object boundaries:

### 12.1 Evidence maintenance

May create or verify only the expected evidence ref for a completed cycle.

Must not rewrite article content, active state, archived state, or Custom Rules.

### 12.2 Branch cleanup

May delete only a completed writing branch after all closeout safety preconditions PASS.

Must not alter main content, evidence refs, state, or Custom Rules.

### 12.3 Archive operation

May move the completed cycle from active-state representation to its cycle-aware archive representation as part of closeout.

Must not edit historical archived cycles.

### 12.4 Temporary artifact cleanup

May delete explicitly identified temporary test artifacts only.

Must not delete or change an in-progress bound article or active state.

### 12.5 Other maintenance

Any maintenance category not explicitly authorized MUST fail closed until defined.

Maintenance MUST NOT be usable to bypass Gate transition, freshness, same-commit, or Core authority rules.

## 13. Active-state and archive CI semantics

CI MUST distinguish active and archived state validation.

Active states:

- schema validation;
- freshness validation;
- normal transition / commit validation;
- fail closed when stale.

Archived states:

- schema validation;
- must have `status = complete`;
- must have cycle/path agreement;
- MUST NOT require freshness against the current main article blob;
- MUST NOT become stale merely because later cycles changed the article.

### 13.1 Archive ↔ evidence historical consistency

Archive/evidence validation MUST be content-level, not naming-only.

For archived state:

`.writing-state/archive/write-commentary/<article-id>/c<cycle>.json`

the expected evidence ref is:

`writing-evidence/<article-id>/c<cycle>`

Validation MUST require all of the following:

1. the expected evidence ref exists;
2. the evidence ref points exactly to that cycle's G7 completion commit;
3. the evidence target commit contains the completed active state for that cycle at:
   `.writing-state/write-commentary/<article-id>.json`;
4. the completed active state contained in the evidence target is content-equivalent to the archived JSON, except for representation/path relocation outside the JSON content itself;
5. at minimum, the following fields MUST match exactly:
   - `schema_version`;
   - `workflow`;
   - `article_id`;
   - `article_path`;
   - `cycle`;
   - `entry_gate`;
   - `skipped_by_user`;
   - `current_gate`;
   - `completed`;
   - `status`;
   - `article_revision`;
6. archived `status` MUST equal `complete`;
7. archived `current_gate` MUST be `null`;
8. archived `article_revision` MUST equal the Git blob SHA of the final article at `article_path` in the evidence target commit.

Any mismatch between archive content and evidence-target historical content MUST fail closed.

The archive is therefore not considered valid merely because its path and evidence-ref name have matching article/cycle identifiers.

CI MUST NOT scan archived states as resumable active states.

## 14. Maintenance-aware commit validation

CI/commit validation MUST distinguish:

- writing transactions;
- lifecycle closeout;
- reconcile recovery;
- repository maintenance.

Repository maintenance commits MUST NOT be forced through Gate-transition validation when no Gate transition is occurring.

However, maintenance commits MUST have deterministic classification and path restrictions so maintenance cannot become a validation bypass.

Implementation MUST define the required commit trailers or equivalent deterministic signals.

## 15. Closeout safety ordering

Closeout ordering is frozen as:

1. verify completed state and confirm the cycle terminal commit is G7 completion;
2. verify required CI PASS;
3. identify the recorded/derived writing-branch main base and current main HEAD;
4. compute current-main changes since base and the cycle's authorized durable delta;
5. detect any conflict between current main and the cycle durable delta; on conflict STOP;
6. create or idempotently verify evidence ref pointing exactly to the G7 completion commit;
7. construct the exact durable closeout tree on top of current main;
8. create one high-level main closeout commit;
9. verify main tree contains final article, durable Custom Rules, archived cycle state, and no active state for that cycle;
10. verify archive/evidence historical consistency at content level;
11. delete writing branch.

Archive representation is part of the same main closeout tree, not a later maintenance commit.

Any failure:

`STOP → preserve writing branch → preserve existing evidence ref → do not delete active source data prematurely`

## 16. Main closeout idempotency

Closeout MUST be safe to retry after partial failure.

At minimum:

- existing correct evidence ref is accepted;
- existing different evidence ref causes STOP;
- if main already contains the exact expected closeout durable result, retry MUST NOT create a duplicate closeout commit;
- writing branch deletion is the last step and may be retried safely;
- historical archived state is never overwritten by retry.

## 17. Agent-first documentation requirements

`README.md` and `README.zh-CN.md` MUST make the normal Quick Start conversational and Agent-first:

1. Fork DraftGate;
2. give fork URL to a GitHub-capable Agent;
3. Pre-G1 brainstorm;
4. tell the Agent to begin DraftGate;
5. execute one Gate at a time through conversation;
6. Agent manages branch, state commits, evidence ref, closeout, archive, and branch cleanup.

Direct Git/Python commands remain documented under Advanced / Local Usage.

Ordinary users MUST NOT need to understand trailers, branch naming, evidence refs, archive paths, or squash mechanics to complete a normal cycle.

## 18. Lifecycle command surface

Implementation MAY extend existing commands or add lifecycle commands, but semantics MUST be deterministic.

The implementation design MUST cover at least:

- begin/start article cycle and writing branch;
- closeout completed cycle;
- archive as part of closeout;
- start a new cycle from archived history;
- recovery-only reconcile.

Command naming is not frozen by this SPEC.

Normal lifecycle operations SHOULD be orchestratable by an Agent without manual Git CLI steps.

## 19. Validation and tests

Implementation MUST add tests covering at least:

1. writing branch naming;
2. one branch per article cycle;
3. writing branch creation records or deterministically identifies exact main base commit;
4. Gate commits remain intact on writing branch;
5. evidence ref points exactly to the cycle's G7 completion commit;
6. evidence ref is write-once by policy;
7. existing same-target evidence ref is idempotent;
8. existing different-target evidence ref causes STOP;
9. deleting writing branch leaves Gate history reachable through evidence ref;
10. closeout uses current main HEAD, not stale main base tree;
11. non-conflicting current-main changes are preserved;
12. cycle durable changes are applied onto current main;
13. conflicting current-main/article changes cause STOP;
14. conflicting current-main/Custom-Rules changes cause STOP;
15. closeout conflict preserves writing branch;
16. closeout conflict preserves any already-created evidence ref;
17. main closeout produces one high-level commit;
18. main closeout final tree contains final article;
19. main closeout final tree contains durable Custom Rules changes;
20. main closeout final tree contains `.writing-state/archive/write-commentary/<article-id>/c<cycle>.json`;
21. main closeout final tree does not contain the completed cycle active state;
22. archive is cycle-aware and does not overwrite earlier cycles;
23. archived state maps one-to-one to evidence ref;
24. archived-state content matches the completed active state contained in the evidence target;
25. archived `article_revision` equals the final article blob in the evidence target;
26. archive/evidence content mismatch fails closed;
27. evidence ref targeting anything other than cycle G7 completion fails closed;
28. archived state is not freshness-checked against later article versions;
29. archived state cannot be advanced/reopened as active state;
30. new cycle reads previous archive without mutating it;
31. new active cycle uses current main article blob;
32. reconcile cannot run automatically;
33. reconcile requires explicit confirmation at Agent contract level;
34. reconcile does not claim Gate-authority validation;
35. maintenance cannot modify in-progress bound article;
36. maintenance cannot modify active state except explicitly authorized lifecycle operation;
37. branch cleanup occurs only after verified closeout;
38. closeout failure preserves writing branch;
39. retry/idempotency behavior;
40. existing schema v4 tests;
41. existing same-commit tests;
42. existing freshness tests;
43. existing NO_CHANGE tests;
44. existing reopen tests;
45. existing start-cycle/selectable-entry tests;
46. existing Custom Rules isolation tests.

## 20. Dogfood acceptance

After implementation audit PASS, run one real small article through:

`Fork/main baseline`
`→ Pre-G1`
`→ create writing/<article-id>/c1`
`→ G1...G7`
`→ CI PASS`
`→ create writing-evidence/<article-id>/c1`
`→ one squash-style main closeout commit`
`→ archive c1 state in the same main closeout tree`
`→ remove c1 active state from main closeout tree`
`→ preserve durable Custom Rules changes`
`→ delete writing branch`

Acceptance MUST verify:

- writing branch base commit is recorded or deterministically recoverable;
- main history contains one high-level cycle closeout commit;
- if main advanced during the cycle, unrelated/non-conflicting main changes are preserved;
- no completed c1 active state remains;
- archived c1 state exists;
- evidence ref exists and points exactly to the c1 G7 completion commit;
- archived c1 JSON matches the completed active state stored in that G7 evidence target;
- archived c1 `article_revision` equals the final article blob in that G7 evidence target;
- G1–G7 commits remain reachable;
- final article exists on main;
- durable Custom Rules changes exist on main;
- writing branch is deleted;
- CI PASS.

Then start cycle 2 from the archived c1 article:

`latest c1 archive → read only → create active c2 state using current main article blob → selected entry Gate`

Verify:

- c1 archive unchanged;
- c2 active state uses `cycle = 2`;
- c2 branch name is correct;
- c2 can complete and archive to `c2.json`;
- c1 archive and evidence remain untouched.

## 21. Public rule neutrality

This SPEC concerns repository lifecycle only.

It MUST NOT add personal writing preferences, language-specific style rules, or new writing authority to DraftGate Core.

## 22. Implementation boundary

This SPEC commit contains design only.

Implementation MUST NOT begin before SPEC audit PASS.
