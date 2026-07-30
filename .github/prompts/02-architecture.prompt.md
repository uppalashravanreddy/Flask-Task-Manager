---
mode: agent
description: "Phase 2 — Design system architecture from requirements and produce architecture.md"
tools:
  - read_file
  - write_file
  - run_in_terminal
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/01-coding-standards.md
#file:.github/instructions/03-security-standards.md
#file:.github/skills/analyze-codebase.md
#file:.github/skills/generate-docs.md

## Constraints
- Architecture must be based on repository evidence — no assumed components
- Every ADR must have: Status, Context, Decision, Consequences
- Prefer ASCII diagrams — no Mermaid, no external tools
- Flag any gap between existing code and requirements as a **Risk** in the architecture
- Do NOT write to files other than `docs/artifacts/FLASK-001/architecture.md`

## Input
Read in this order before writing:
- #file:docs/artifacts/FLASK-001/requirements.md  ← Phase 1 output (must exist)
- #file:src/doc_sync/repo_scanner.py
- #file:src/doc_sync/extractor.py
- #file:src/doc_sync/page_creator.py
- #file:src/main.py

## Task
Propose the architecture design to the developer. After approval, write `docs/artifacts/FLASK-001/architecture.md`.

## Output Specification

```markdown
# Architecture — FLASK-001: Automated Documentation Sync

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Phase | 2 — Architecture |
| Status | Draft |
| Author | GitHub Copilot (architecture agent) |
| Date | YYYY-MM-DD |

## 1. Architecture Summary
(one paragraph describing the three-stage pipeline approach)

## 2. Component Diagram
+------------------+    +------------------+    +------------------+
|  RepoScanner     | -> |  Extractor       | -> |  PageCreator     |
|  repo_scanner.py |    |  extractor.py    |    |  page_creator.py |
+------------------+    +------------------+    +------------------+
         ^                                               |
   Repository Files                        docs/artifacts/FLASK-001/

## 3. Component Responsibilities
| Component File | Class / Function | Responsibility |
|---|---|---|

## 4. Execution Data Flow
1. Developer runs: python src/main.py --repo . --output <path>
2. ...

## 5. Technology Choices
| Area | Choice | Rationale |
|---|---|---|
| Language | Python 3.11 | ... |

## 6. Security Design
(SECRET_KEY via .env, file write boundaries, what is never committed)

## 7. Architecture Decision Records
### ADR-001: SQLite for local execution state
- Status: Accepted
- Context: ...
- Decision: ...
- Consequences: Pros / Cons

## 8. Risk Register
| Risk | Impact | Mitigation |
|---|---|---|

## 9. Acceptance Criteria
```

## Success Criteria
- All 8 sections present and complete
- Component diagram shows all three stages with actual file names
- ADR-001 has all four fields filled
- Risk Register lists at least one item

## On Failure
If `requirements.md` does not exist: stop and instruct the developer to complete Phase 1 first.

## State Transition
When output file written: `python scripts/state_manager.py complete 2`
${input:architecture_notes:No additional architecture notes}
