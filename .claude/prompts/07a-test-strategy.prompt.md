# Phase 7.1 — Test Strategy Prompt

## Context
You are designing the test approach for a completed Flask Task Manager feature before any tests are written or run.

## Input
`docs/artifacts/<TICKET-ID>/requirements.md` and `docs/artifacts/<TICKET-ID>/architecture.md`.

## Task

1. Read both input artifacts.
2. Run `python -m pytest tests/ --collect-only -q` to see the current test inventory.
3. For each AC in requirements.md, decide the minimum-cost test level:
   - Pure logic / constants → **unit**
   - DB changes / route behaviour → **integration**
   - Visual output / user flow / badge rendering → **E2E**
4. Write `docs/artifacts/<TICKET-ID>/test-strategy.md` with:
   - Objective paragraph
   - In-scope / out-of-scope lists
   - Test levels table (level, framework, location, covers)
   - AC → test level mapping table
   - Tools table (tool, version, purpose)
   - Coverage targets
   - Risks + mitigations
5. Push the document to Confluence using `confluence_create_page`:
   - title: `<TICKET-ID> Test Strategy`
   - Place under QA parent page
6. Store the returned Confluence URL in `.sdlc/state.json` under `phases.7.1.confluence_url`.
7. Commit: `git add docs/artifacts/<TICKET-ID>/test-strategy.md && git commit -m "docs(<TICKET-ID>): Phase 7.1 test strategy"`

## Quality gates
- Every AC must appear in the AC → test level mapping table.
- Bootstrap badge rendering must be assigned to E2E (it cannot be tested at unit level).
- If no ACs exist → BLOCKED → return to Phase 1.
