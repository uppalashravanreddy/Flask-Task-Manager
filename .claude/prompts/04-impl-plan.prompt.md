# Phase 4 — Implementation Plan Prompt

## Context
You are breaking approved architecture into atomic, executable tasks.

## Input
`.claude/artifacts/<TICKET-ID>/architecture.md` and `.claude/artifacts/<TICKET-ID>/design-review.md`.

## Task
1. List every file in the "Files Changed" table from architecture.md.
2. Break each file change into one atomic task (one task = one file, one logical change).
3. Order tasks by dependency — tasks with no dependencies first.
4. Write `.claude/artifacts/<TICKET-ID>/impl-plan.md` with:
   - Dependency-ordered task list table (T#, Task, File, Depends On, Blocked Until)
   - Task detail section (one paragraph per task: exact code change description)
   - Blocked tasks table (task, blocked by, reason)
   - Files inventory table (file, action)
5. Commit: `git add .claude/artifacts/<TICKET-ID>/impl-plan.md && git commit -m "docs(<TICKET-ID>): Phase 4 implementation plan"`

## Rules
- Migration tasks must precede all route and template tasks.
- Test-writing tasks must be explicit — not implied.
- Final task must always be: "Run full test suite and verify all pass."
