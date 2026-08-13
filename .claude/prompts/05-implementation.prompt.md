# Phase 5 — Implementation Prompt

## Context
You are executing the implementation plan task by task.

## Input
`docs/artifacts/<TICKET-ID>/impl-plan.md` and all upstream artifacts.

## Task
Execute every task in impl-plan.md in dependency order:
1. Read the current state of each target file before editing.
2. Make the change described in the task detail.
3. Write the file back.
4. After all source tasks: run migration if schema changed.
5. Run the test suite: `python -m pytest tests/unit/ tests/integration/ -v`
6. Report a one-line summary per file changed.

## If a gap is found during implementation
If a task reveals a design gap not in impl-plan.md → **stop immediately**:
- Do NOT improvise.
- Return to Phase 4: update impl-plan.md with the missing task.
- Resume from that task.

## Quality rules
- Bootstrap 4.5 badge classes only: `badge badge-danger`, `badge badge-warning`, `badge badge-success`.
- No new comments unless the WHY is non-obvious.
- No new dependencies beyond requirements.txt.
- All test files go in `tests/unit/` or `tests/integration/`.
