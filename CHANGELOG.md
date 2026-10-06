# Changelog

## v1.0.0 — 2026-10-06

First stable DraftGate release.

### Writing workflow

- Git-native G1–G7 staged editorial lifecycle.
- Selectable entry Gate for later revision cycles.
- Same-commit article/state transitions with stale-state protection.
- Gate-authorized NO_CHANGE, reopen, and recovery-only reconcile semantics.
- G3 narrative-mode selection, explanatory spine, and complete first-draft construction.

### Lifecycle and evidence

- One temporary `writing/<article-id>/c<cycle>` branch per cycle.
- Write-once `writing-evidence/<article-id>/c<cycle>` refs preserve Gate history.
- Cycle-aware completed-state archives.
- Automatic terminal closeout after successful G7 CI.
- Closeout conflict protection against concurrent `main` changes.
- Deterministic closeout commit validation before publication.
- Automatic writing-branch cleanup after verified closeout.

### Personal writing profiles

- DraftGate Core starts author-neutral.
- Default `.writing-rules/G1.md` through `.writing-rules/G7.md` scaffolding.
- Persistent Custom Rules let one fork accumulate explicit long-term author preferences.
- Current-Gate-only Custom Rule loading with Core precedence.

### Validation

- GitHub Actions enforcement for workflow registry, state freshness, commit trailers, Gate transitions, archives, and lifecycle invariants.
- Real dogfood acceptance completed across two cycles, including selectable entry, NO_CHANGE, evidence retention, automatic closeout, archive carryover, and branch cleanup.
