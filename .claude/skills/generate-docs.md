# Skill: generate-docs

## Purpose
Write a phase artifact document to `.claude/artifacts/<TICKET-ID>/` in the standard SDLC format.

## Steps
1. Confirm `.claude/artifacts/<TICKET-ID>/` exists; create it if not.
2. Write the artifact file with the required sections for the phase (see individual phase prompts in `.claude/prompts/`).
3. Always include the header table:
   ```markdown
   | Field | Value |
   |-------|-------|
   | Ticket ID | <TICKET-ID> |
   | Phase | <N — Phase Name> |
   | Status | Draft / Under Review / Approved |
   | Author | Claude Code (Agentic SDLC) |
   | Date | <today> |
   ```
4. Commit after writing: `git add .claude/artifacts/<TICKET-ID>/ && git commit -m "docs(<TICKET-ID>): Phase <N> <name>"`

## Quality rules
- No empty sections — if data is not available, state why explicitly.
- Every table must have a header row.
- Every requirement, risk, or task must have a unique ID.
- Dates use ISO 8601 format: YYYY-MM-DD.
