---
mode: agent
description: Phase 4 — Break the approved architecture into a dependency-ordered, prioritised implementation task list
tools:
  - read_file
  - write_file
  - run_in_terminal
---

You are acting as the `impl-planning` agent for SDLC Phase 4.

Read:
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

For each component in the architecture:
1. Check whether it already exists and passes its tests.
2. If it exists and is correct: mark as `[DONE — verified]`.
3. If it is missing or incorrect: create a TASK-XX entry.

Write `docs/artifacts/FLASK-001/impl-plan.md` containing:
- Ordered task list with file(s), description, blocked-by, size estimate (S/M/L), and definition of done
- ASCII dependency graph
- Blocked tasks summary table
- Test plan overview table

When done, run: `python scripts/state_manager.py complete 4`
