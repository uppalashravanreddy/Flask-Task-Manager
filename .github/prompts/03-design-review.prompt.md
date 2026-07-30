---
mode: agent
description: Phase 3 — Structured design review of architecture.md. Identify risks, gaps, and required corrections before any code is written.
tools:
  - read_file
  - write_file
  - run_in_terminal
---

You are acting as the `design-review` agent for SDLC Phase 3.

Read:
- #file:docs/artifacts/FLASK-001/architecture.md
- #file:docs/artifacts/FLASK-001/requirements.md

Review the architecture against every dimension in this checklist:

| Dimension | Question |
|---|---|
| Requirements Traceability | Does every FR and NFR map to a component or flow? |
| Security | Are secrets in .env? Are file write boundaries enforced? |
| Error Handling | Are all failure modes for scanner/extractor/page-creator handled? |
| Scalability | Is the SQLite ADR appropriate for the stated constraints? |
| Test Strategy | Are test boundaries (unit vs integration) clearly defined? |
| Missing Components | Is __init__.py present? Is the CLI entry point correct? |
| Naming Consistency | Do architecture file names match the actual code file names? |

Write `docs/artifacts/FLASK-001/design-review.md` with:
- Review metadata (reviewer, date, architecture version)
- Findings table (ID, dimension, severity, finding, recommendation)
- List of agreed design decisions applied to architecture.md
- Open items deferred to implementation
- Sign-off checklist

For any **Blocking** finding: apply the correction to `docs/artifacts/FLASK-001/architecture.md` immediately after approval.

When done, run: `python scripts/state_manager.py complete 3`
