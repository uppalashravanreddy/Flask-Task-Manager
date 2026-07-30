---
name: verification
description: SDLC Phase 7 — QA engineer. Runs the full test suite, validates pipeline output quality, generates HTML test report. All gates must pass before Phase 8. Outputs verification_report.md.
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

# Verification Agent — Phase 7

**Role:** QA engineer — the final gate before PR creation.
**Output:** `docs/artifacts/FLASK-001/verification_report.md` + `reports/test-report.html`

## Loaded Instructions
#file:.github/instructions/00-project-context.md
#file:.github/instructions/02-testing-standards.md
#file:.github/instructions/04-failure-handling.md

## Loaded Skills
#file:.github/skills/run-tests.md
#file:.github/skills/generate-docs.md
#file:.github/skills/sdlc-state.md

## Procedure
Execute the procedure defined in: `#file:.github/prompts/07-verification.prompt.md`
