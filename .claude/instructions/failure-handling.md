# Failure Handling — SDLC Feedback Loop Rules

## Phase return rules

When a blocker is found during any phase, return to the EARLIEST affected phase:

| Blocker type | Return to |
|---|---|
| Requirements are ambiguous or missing | Phase 1 (Requirements) |
| Architecture is wrong or incomplete | Phase 2 (Architecture) |
| Design review finds a HIGH risk | Phase 3 (Design Review) → resolve → re-sign-off |
| Implementation plan is missing a task | Phase 4 (Implementation Plan) |
| Code doesn't compile or a test fails | Phase 5 (Implementation) |
| Code review finds a blocker | Phase 5 (Implementation) |
| Verification test suite fails | Phase 5 (Implementation) |
| PR creation fails (branch, remote, auth) | Fix the git issue, re-run Phase 8 |

## What to do when you return to a phase
1. Update the artifact for that phase (add the missing content, fix the wrong content).
2. Commit the updated artifact.
3. Re-run all downstream phases that depend on it.
4. Record the feedback loop in the `review_report.md` or `verification_report.md` for traceability.

## Never do
- Do NOT skip a phase to speed up delivery.
- Do NOT modify tests to make them pass — fix the code.
- Do NOT mark a phase COMPLETE if it has an open HIGH blocker.
- Do NOT push directly to `main`.
- Do NOT merge the PR — create it and stop.

## State tracking
Pipeline state is persisted in `.sdlc/state.json`:
```json
{
  "ticket_id": "FLASK-002",
  "current_phase": 8,
  "phases": { "1": "complete", "2": "complete", ... }
}
```
Update `current_phase` each time a phase completes or a return is triggered.
