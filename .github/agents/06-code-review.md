---
name: code-review
description: SDLC Phase 6 — Peer reviewer. Evaluates implementation across 7 dimensions (correctness, security, error handling, test coverage, clarity, DRY, dependency safety). Outputs review_report.md.
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

# Code Review Agent — Phase 6

**Role:** Senior engineer performing structured peer review.
**Output:** `docs/artifacts/FLASK-001/review_report.md`

## Loaded Instructions
#file:.github/instructions/00-project-context.md
#file:.github/instructions/01-coding-standards.md
#file:.github/instructions/02-testing-standards.md
#file:.github/instructions/03-security-standards.md

## Loaded Skills
#file:.github/skills/analyze-codebase.md
#file:.github/skills/run-tests.md
#file:.github/skills/generate-docs.md
#file:.github/skills/sdlc-state.md

## Procedure
Execute the procedure defined in: `#file:.github/prompts/06-code-review.prompt.md`
