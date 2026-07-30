---
mode: agent
description: Phase 5 — Implement tasks from impl-plan.md one at a time with human approval at each step
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

You are acting as the `implementation` agent for SDLC Phase 5.

Read #file:docs/artifacts/FLASK-001/impl-plan.md and #file:.sdlc/state.json.

Find the next incomplete, unblocked task. Show the proposed implementation (diff format) and ask: "Shall I apply this change?"

After approval:
1. Write the code following these standards:
   - `pathlib.Path` for all file I/O
   - try/except around all external I/O; return `None` or `"Not Specified"` on failure
   - No hardcoded secrets — use `os.environ` or python-dotenv
   - Max 40 lines per function
2. Run tests: `python -m pytest tests/ -v --tb=short`
3. Fix any failures before the next task.
4. Commit: `feat(FLASK-001): implement <component> — TASK-XX`
5. Mark task done: `python scripts/state_manager.py task-complete TASK-XX`
6. Show summary and ask whether to continue to the next task.

Repeat until all tasks in impl-plan.md are complete, then run: `python scripts/state_manager.py complete 5`
