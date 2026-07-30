---
mode: agent
description: "Phase 7 — Run full test suite, generate HTML test report, validate pipeline output. All gates must pass before Phase 8."
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/02-testing-standards.md
#file:.github/instructions/04-failure-handling.md
#file:.github/skills/run-tests.md
#file:.github/skills/generate-docs.md

## Constraints
- NEVER advance to Phase 8 if any gate shows FAIL
- NEVER modify source code or tests in this phase — fix failures belong in Phase 5/6
- If a test fails that cannot be fixed here: mark Phase 7 failed and instruct developer
- All 4 gates must show PASS in `verification_report.md`

## Input
No files to pre-read — all verification is done by running commands.

## Task

Run all 4 gates in sequence:

**Gate 1 — Unit Tests**
```bash
python -m pytest tests/unit/ -v --tb=short
```
Capture full output. Count passed/failed/errors.

**Gate 2 — Integration Tests**
```bash
python -m pytest tests/integration/ -v --tb=short
```
Capture full output.

**Gate 3 — HTML Test Report**
```bash
python scripts/test_runner.py
```
Confirms `reports/test-report.html` is generated. Open and verify it shows results.

**Gate 4 — End-to-End Pipeline Run**
```bash
python src/main.py --repo . --output docs/artifacts/FLASK-001/technical_profile_report.md
```
Check exit code is 0. If non-zero: capture stderr with `get_errors`.

**Gate 5 — Document Quality Check**
Read `docs/artifacts/FLASK-001/technical_profile_report.md` and verify:
- Contains ALL sections: Project Overview, Technical Stack, Entry Point, Data Model, Routes, Forms, Dependencies
- No section has blank or empty content (missing values must be "Not Specified")
- File size > 500 bytes

**Failure Recovery (if any gate fails):**
1. Read the failure message
2. Identify root cause (wrong function, missing file, import error)
3. Fix only if it's a configuration or path issue
4. Re-run the gate
5. If still failing after 1 fix attempt: mark gate as FAIL and continue to produce the report

## Output Specification

```markdown
# Verification Report — FLASK-001

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Phase | 7 — Verification |
| Status | Draft |
| Author | GitHub Copilot (verification agent) |
| Date | YYYY-MM-DD |

## 1. Test Run Summary
| Metric | Value |
|---|---|
| Total tests | X |
| Passed | X |
| Failed | X |
| Errors | X |

## 2. Test Results Detail
| Test File | Test Name | Result | Notes |
|---|---|---|---|

## 3. HTML Test Report
- Generated: reports/test-report.html
- Open in browser to view failure details and tracebacks

## 4. End-to-End Pipeline
- Exit code: 0 / 1
- Output file: docs/artifacts/FLASK-001/technical_profile_report.md
- File size: X bytes

## 5. Document Quality Checks
| Section | Present | Has Content |
|---|---|---|
| Project Overview | PASS/FAIL | PASS/FAIL |

## 6. Gate Status
| Gate | Status | Notes |
|---|---|---|
| Gate 1: Unit Tests | PASS/FAIL | X passed, Y failed |
| Gate 2: Integration Tests | PASS/FAIL | ... |
| Gate 3: HTML Test Report | PASS/FAIL | ... |
| Gate 4: E2E Pipeline | PASS/FAIL | exit code 0 |
| Gate 5: Document Quality | PASS/FAIL | all sections present |

## 7. Overall: PASS / FAIL
```

## Success Criteria
- All 5 gates show PASS
- `reports/test-report.html` exists and non-empty
- `verification_report.md` exists and is > 500 bytes

## On Failure
If any gate is FAIL after fix attempt: `python scripts/state_manager.py fail 7 "Gate X failed: <reason>"`
Generate HTML: `python scripts/html_report.py`

## State Transition
When ALL gates PASS: `python scripts/state_manager.py complete 7`
${input:test_scope:Run all test suites and all quality gates}
