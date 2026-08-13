# Phase 3 — Design Review Prompt

## Context
You are acting as a senior engineer reviewing the architecture before any code is written.

## Input
`docs/artifacts/<TICKET-ID>/architecture.md` and the current codebase.

## Task
1. Review architecture.md against requirements.md for correctness, security, reliability, and maintainability.
2. Identify at least one finding (even observation-level). A review with zero findings was not done.
3. Write `docs/artifacts/<TICKET-ID>/design-review.md` with:
   - Review summary paragraph
   - Findings table (RISK-ID, severity: High/Medium/Low/Obs, finding, resolution, status)
   - SDLC feedback loop table (what triggers returning to each phase)
   - Architecture sign-off section
4. **Update `architecture.md`** for any finding that changes the design — this is mandatory per the SDLC process.
5. Commit both files: `git add docs/artifacts/<TICKET-ID>/ && git commit -m "docs(<TICKET-ID>): Phase 3 design review + architecture corrections"`

## Blocker rule
If any HIGH severity finding requires changing requirements.md → mark as BLOCKED, do not sign off, return to Phase 1.

## Checklist
- [ ] Bootstrap version compatibility verified (project uses Bootstrap 4.5)
- [ ] Migration NULL backfill handled if schema changes
- [ ] No hardcoded secrets introduced
- [ ] Input validation via WTForms SelectField or validators confirmed
