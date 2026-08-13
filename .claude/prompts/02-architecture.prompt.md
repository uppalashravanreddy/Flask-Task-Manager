# Phase 2 — Architecture Prompt

## Context
You are acting as an AI pair programmer driving Phase 2 of the Agentic SDLC pipeline.

## Input
`docs/artifacts/<TICKET-ID>/requirements.md` (written in Phase 1).

## Task
1. Read requirements.md fully.
2. Read the current source files: `models.py`, `routes.py`, `forms.py`, `templates/`, `requirements.txt`.
3. Design the minimal architecture to satisfy all FRs — no over-engineering.
4. Write `docs/artifacts/<TICKET-ID>/architecture.md` with:
   - Overview paragraph
   - Component diagram (ASCII art)
   - Component responsibilities (one sub-section per component)
   - Data flow section (one sub-section per user action)
   - Technology choices table (decision, choice, rationale)
   - Files changed table (file, action: Modify/Create/Delete, reason)
   - Out of scope section
5. Commit: `git add docs/artifacts/<TICKET-ID>/architecture.md && git commit -m "docs(<TICKET-ID>): Phase 2 architecture"`

## Constraints
- Bootstrap 4.5 only — use `badge badge-danger/warning/success`, NOT Bootstrap 5 `bg-*` classes.
- No new Python dependencies unless absolutely required.
- Prefer modifying existing files over creating new ones.
- If schema changes: always include a migration script in the files changed table.
