# Phase 7.2 — Test Plan Prompt

## Context
You are writing the detailed test execution plan that describes HOW and WHEN the tests will run.

## Input
`.claude/artifacts/<TICKET-ID>/test-strategy.md` and `.claude/artifacts/<TICKET-ID>/requirements.md`.

## Task

1. Read both inputs.
2. Check environment readiness:
   ```bash
   python -m pytest --version
   python -c "import pytest_html" 2>&1
   python -c "import playwright" 2>&1
   ```
3. Write `.claude/artifacts/<TICKET-ID>/test-plan.md` with:
   - Entry criteria checklist (all must pass before execution)
   - Exit criteria checklist (all must pass before Phase 7.5)
   - Test environment table (OS, Python, DB, browser, port)
   - Install commands for missing dependencies
   - Test execution order table with exact commands and report output paths
   - Defect management rules (blocker → halt, critical → Phase 5 return)
   - Risk table
4. Push to Confluence: `confluence_create_page` with title `<TICKET-ID> Test Plan`, child of `<TICKET-ID> Test Strategy`.
5. Commit: `git add .claude/artifacts/<TICKET-ID>/test-plan.md && git commit -m "docs(<TICKET-ID>): Phase 7.2 test plan"`

## Required commands in execution order table
```
python -m pytest tests/unit/ -v --html=.claude/reports/<TICKET-ID>/unit-report.html --self-contained-html
python -m pytest tests/integration/ -v --html=.claude/reports/<TICKET-ID>/integration-report.html --self-contained-html
python -m pytest tests/e2e/ -v --html=.claude/reports/<TICKET-ID>/e2e-report.html --self-contained-html
python scripts/generate_html_report.py --ticket <TICKET-ID>
```
