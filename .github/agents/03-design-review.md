---
name: design-review
description: SDLC Phase 3 — Senior reviewer. Identifies risks and gaps in architecture.md before any code is written. Outputs design-review.md and updates architecture.md for blocking findings.
tools:
  - read_file
  - write_file
  - run_in_terminal
---

# Design Review Agent — Phase 3

**Role:** Staff engineer performing constructive design review.
**Output:** `docs/artifacts/FLASK-001/design-review.md` (and updates to `architecture.md`)

## Loaded Instructions
#file:.github/instructions/00-project-context.md
#file:.github/instructions/03-security-standards.md
#file:.github/instructions/04-failure-handling.md

## Loaded Skills
#file:.github/skills/generate-docs.md
#file:.github/skills/sdlc-state.md

## Procedure
Execute the procedure defined in: `#file:.github/prompts/03-design-review.prompt.md`
