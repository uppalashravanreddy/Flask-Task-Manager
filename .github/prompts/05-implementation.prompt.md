---
mode: agent
description: "Phase 5 — Implement tasks from impl-plan.md one at a time. Show diff, get approval, write code, run tests, commit."
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/01-coding-standards.md
#file:.github/instructions/02-testing-standards.md
#file:.github/instructions/03-security-standards.md
#file:.github/instructions/04-failure-handling.md
#file:.github/skills/analyze-codebase.md
#file:.github/skills/run-tests.md
#file:.github/skills/git-operations.md

## Constraints
- NEVER implement more than one task without human approval
- NEVER delete or modify a passing test — fix the code, not the test
- NEVER write to `.sdlc/state.json` directly — use `state_manager.py`
- NEVER skip the test run step after any file write
- NEVER advance to next task if tests fail — fix first

## Input
- #file:docs/artifacts/FLASK-001/impl-plan.md  ← task list
- Read `.sdlc/state.json` to find last completed task
- Read each source file before modifying it

## Task

**Loop until all TASK-XX items are complete:**

1. Find next incomplete, unblocked task from `impl-plan.md`
2. Read any files the task modifies (analyze-codebase skill)
3. Show proposed implementation as a unified diff — wait for "yes" / "no"
4. On approval: write the code following all coding standards from context
5. Run: `python -m pytest tests/ -v --tb=short`
6. If tests fail: diagnose with `get_errors`, fix root cause, re-run
7. If tests fail after fix attempt: mark this task blocked, skip to next
8. If tests pass: commit `feat(FLASK-001): implement <component> — TASK-XX`
9. Run: `python scripts/state_manager.py task-complete TASK-XX`
10. Show summary: "TASK-XX done. Tests: X passed. Ready for TASK-XY?"

## Coding Standards (summary — see instructions/01-coding-standards.md for full rules)
- `pathlib.Path` for all file I/O
- `try/except` around all external I/O; return `None` or `"Not Specified"` on failure
- No hardcoded secrets — `os.environ` or python-dotenv
- Max 40 lines per function
- No inline comments unless WHY is non-obvious

## Success Criteria
- All TASK-XX items marked complete or explicitly skipped with reason
- All tests pass: `python -m pytest tests/ -v`

## On Failure
- If 2+ tasks fail consecutively: mark Phase 5 as failed
- Run: `python scripts/state_manager.py fail 5 "X tasks failed: TASK-XX, TASK-XY"`
- Generate report: `python scripts/html_report.py`

## State Transition
When all tasks complete: `python scripts/state_manager.py complete 5`
${input:start_task:Start from the first incomplete task in impl-plan.md}
