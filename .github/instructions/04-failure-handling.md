# Instruction: Failure Handling and Pipeline Resumability

## Retry Policy
- Every phase gets **maximum 2 retry attempts** (3 total tries) before being marked `failed`
- Retry only for transient failures: output file not created, command returned non-zero, missing dependency
- Do NOT retry logic errors: wrong output format, wrong content, security violation — fix first
- Track retries in `.sdlc/state.json` → `phases["N"]["retry_count"]`

## Failure States
When a phase fails after all retries:
1. Run: `python scripts/state_manager.py fail <N> "<reason>"`
2. Generate failure HTML: `python scripts/html_report.py` (marks the failed phase in red)
3. Log to `.sdlc/state.json` → `phases["N"]["last_error"]`
4. **HALT** — do not advance to the next phase
5. Report to the developer with exact failure reason and next steps

## Pipeline Resumability (Critical)
The pipeline is **interrupt-tolerant**. On any reconnect or restart:

1. Always read `.sdlc/state.json` first
2. Find the first phase where `status != "completed"` — this is the resume point
3. If that phase's `status == "in_progress"`: it was interrupted mid-execution → **re-run from the start of that phase**
4. If that phase's `status == "pending"`: it hasn't started → start it normally
5. If that phase's `status == "failed"`: fix the error, then run `python scripts/state_manager.py reset <N>` to retry

**NEVER restart from Phase 1 if a later phase shows `completed` or `in_progress`.**

Resume command: `python scripts/orchestrator.py --resume`

## Phase-Level Error Handling

### Documentation phases (1–4, 6):
- If output file is empty after write: retry the phase
- If required sections are missing: fix the document, do not advance state

### Implementation phase (5):
- If a task's tests fail after fix attempt: mark that task as `failed`, continue with next task
- If more than 2 tasks fail: halt Phase 5, mark as `failed`

### Verification phase (7):
- Run `python scripts/test_runner.py` — generates HTML report at `reports/test-report.html`
- If any test fails: read the failure detail in the HTML report, diagnose root cause
- Attempt fix and re-run: `python -m pytest tests/ --lf -v --tb=short`
- If still failing after fix: mark Phase 7 as `failed` — do NOT advance to Phase 8

### PR phase (8):
- If `gh pr create` fails: check authentication, branch push, and GitHub API availability
- If branch not pushed: run `git push -u origin feat/FLASK-001-doc-sync` first

## Escalation
After 3 consecutive phase failures (any phases):
1. Generate full SDLC summary: `python scripts/html_report.py`
2. Print all `last_error` values from state.json
3. Recommend the developer review `reports/sdlc-summary.html` and `reports/test-report.html`
4. Stop the orchestrator
