# Phase 7.4 — Test Execution Prompt

## Context
You are running the full test suite, generating HTML reports, and recording results in Confluence and JIRA.

## Input
All test files in `tests/` and `.claude/artifacts/<TICKET-ID>/test-cases.md`.

## Task

### 1. Ensure dependencies
```bash
pip install pytest-html pytest-playwright
playwright install chromium
```

### 2. Create report directory
```powershell
New-Item -ItemType Directory -Force ".claude/reports/<TICKET-ID>"
```

### 3. Run tests (in this order)
```bash
# Unit
python -m pytest tests/unit/ -v --html=.claude/reports/<TICKET-ID>/unit-report.html --self-contained-html

# Integration
python -m pytest tests/integration/ -v --html=.claude/reports/<TICKET-ID>/integration-report.html --self-contained-html

# E2E
python -m pytest tests/e2e/ -v --html=.claude/reports/<TICKET-ID>/e2e-report.html --self-contained-html
```

### 4. Generate combined report
```bash
python scripts/generate_html_report.py --ticket <TICKET-ID>
```

### 5. Evaluate
- Any unit/integration failure → BLOCKED → return to Phase 5
- E2E infra failure (browser missing) → fix infrastructure, retry
- E2E logic failure → BLOCKED → return to Phase 5

### 6. Update Confluence
`confluence_create_page` titled `<TICKET-ID> Test Results` with pass/fail table and report links.

### 7. JIRA comment
Post test results summary + Confluence URL to the JIRA ticket.

### 8. Commit reports
```bash
git add .claude/reports/<TICKET-ID>/
git commit -m "test(<TICKET-ID>): Phase 7.4 test execution HTML reports"
```

## Rules
- All three test types MUST run. Do not skip E2E just because it's harder.
- Report HTML files MUST be self-contained (`--self-contained-html`).
- Never modify tests to force a pass. Fix the production code.
