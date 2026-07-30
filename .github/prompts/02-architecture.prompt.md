---
mode: agent
description: Phase 2 — Design high-level system architecture from requirements.md and output architecture.md
tools:
  - read_file
  - write_file
  - run_in_terminal
---

You are acting as the `architecture` agent for SDLC Phase 2.

Read:
- #file:docs/artifacts/FLASK-001/requirements.md
- #file:src/doc_sync/repo_scanner.py
- #file:src/doc_sync/extractor.py
- #file:src/doc_sync/page_creator.py
- #file:src/main.py

Propose and then (after approval) write `docs/artifacts/FLASK-001/architecture.md` containing:

1. **Architecture Summary** — one paragraph describing the approach
2. **ASCII Component Diagram** — showing Scanner → Extractor → PageCreator flow with file names
3. **Component Responsibilities Table** — file, class/function, and responsibility for each component
4. **Data Flow** — numbered steps from developer trigger to output file
5. **Technology Choices Table** — tool, choice, and rationale (Python, pathlib, regex, SQLite, .env)
6. **Security Design** — how secrets are handled, what file paths are writable, what is never committed
7. **Architecture Decision Records** — at least ADR-001 (SQLite for state) with Status/Context/Decision/Consequences
8. **Acceptance Criteria** — how reviewers will confirm the architecture is implemented correctly

Flag any gap between the existing code and the requirements as a risk item.

When done, run: `python scripts/state_manager.py complete 2`
