---
mode: agent
description: "Phase 4 — Break the approved architecture into a dependency-ordered, prioritised implementation task list"
tools:
  - read_file
  - write_file
  - run_in_terminal
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/01-coding-standards.md
#file:.github/instructions/02-testing-standards.md
#file:.github/skills/analyze-codebase.md
#file:.github/skills/generate-docs.md

## Constraints
- Do NOT plan tasks for already-correct, passing code — verify first with the analyze-codebase skill
- Every task needs a Definition of Done with at least one test criterion
- Tasks must be ordered by dependency — no task can reference a component that doesn't exist yet
- Mark already-implemented and verified tasks as `[DONE — verified]`
- Do NOT write to any file outside `docs/artifacts/FLASK-001/impl-plan.md`

## Input
Read in this order:
- #file:docs/artifacts/FLASK-001/architecture.md
- #file:docs/artifacts/FLASK-001/design-review.md
- #file:docs/artifacts/FLASK-001/requirements.md
- #file:src/doc_sync/repo_scanner.py
- #file:src/doc_sync/extractor.py
- #file:src/doc_sync/page_creator.py
- #file:src/main.py
- #file:tests/unit/test_doc_sync.py
- #file:tests/unit/test_extractor.py
- #file:tests/unit/test_repo_scanner.py
- #file:tests/integration/test_pipeline.py

## Task
For each component in the architecture: check existence + test pass status. Create TASK-XX entries only for missing or broken components.

## Output Specification

```markdown
# Implementation Plan — FLASK-001: Automated Documentation Sync

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Phase | 4 — Implementation Planning |
| Status | Draft |
| Author | GitHub Copilot (impl-planning agent) |
| Date | YYYY-MM-DD |

## 1. Task List (dependency order)

### TASK-01: [Component Name]
- **File(s):** path/to/file.py
- **Description:** What must be implemented (one paragraph)
- **Blocked By:** None / TASK-XX
- **Estimate:** S (< 1h) / M (1-3h) / L (3h+)
- **Definition of Done:**
  - [ ] Function X exists and returns Y for valid input
  - [ ] Returns "Not Specified" when source file is missing
  - [ ] pytest test_X passes

## 2. Dependency Graph
TASK-01 --> TASK-02 --> TASK-05
                    \-> TASK-03 --> TASK-04

## 3. Blocked Tasks Summary
| Task | Blocked By | Reason |
|---|---|---|

## 4. Test Plan Overview
| Task | Test File | Test Type | Happy Path | Edge Case |
|---|---|---|---|---|
```

## Success Criteria
- Every pending task has a complete TASK-XX entry with DoD
- Dependency graph is consistent with the task list
- Already-verified tasks are clearly marked `[DONE — verified]`

## On Failure
If `architecture.md` or `design-review.md` missing: stop and instruct developer to run earlier phases.

## State Transition
When complete: `python scripts/state_manager.py complete 4`
${input:task_scope:Include all components from architecture.md}
