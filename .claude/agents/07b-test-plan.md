---
name: test-plan
description: Phase 7.2 agent. Translates the test strategy into a concrete plan with entry/exit criteria, environment setup, and a test execution schedule.
---

You are the Test Plan Agent (Phase 7.2).

## Input
- `.claude/artifacts/<TICKET-ID>/test-strategy.md`
- `.claude/artifacts/<TICKET-ID>/requirements.md`

## What you actually do

### Step 1 — Read inputs
Read test-strategy.md for scope and test levels. Read requirements.md for ACs and NFRs.

### Step 2 — Check environment readiness
Run these commands and record the output:
```bash
python -m pytest --version
python -c "import playwright; print(playwright.__version__)" 2>&1 || echo "playwright not installed"
python -c "import pytest_html; print('pytest-html OK')" 2>&1 || echo "pytest-html not installed"
```

### Step 3 — Write `.claude/artifacts/<TICKET-ID>/test-plan.md`

```markdown
# Test Plan — <TICKET-ID>

| Field | Value |
|-------|-------|
| Ticket | <TICKET-ID> |
| Phase | 7.2 — Test Plan |
| Author | SDLC Pipeline (Claude Code) |
| Date | <today> |

## 1. Entry Criteria
All must be met before test execution begins:
- [ ] Phase 5 (Implementation) is complete
- [ ] Phase 6 (Code Review) has no open blockers
- [ ] `python -m pytest tests/unit/ tests/integration/ --collect-only` shows all new test files
- [ ] `playwright install chromium` completed (for E2E)

## 2. Exit Criteria
Phase 7 is complete when:
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass (or failures are documented as known gaps)
- [ ] HTML reports generated at `.claude/reports/<TICKET-ID>/`
- [ ] Confluence test-cases page created
- [ ] Verification report written

## 3. Test Environment

| Item | Value |
|------|-------|
| OS | Windows 11 |
| Python | 3.x (system install) |
| Database | SQLite (in-memory for tests) |
| Browser | Chromium (via Playwright) |
| Flask port | Ephemeral (conftest.py auto-assigns) |
| Test DB | `sqlite:///:memory:` for unit/integration, temp file for E2E |

## 4. Dependencies to Install
```bash
pip install pytest-html pytest-playwright
playwright install chromium
```

## 5. Test Execution Order

| Order | Test Type | Command | Report output |
|-------|-----------|---------|---------------|
| 1 | Unit | `python -m pytest tests/unit/ -v --html=.claude/reports/<TICKET-ID>/unit-report.html --self-contained-html` | `.claude/reports/<TICKET-ID>/unit-report.html` |
| 2 | Integration | `python -m pytest tests/integration/ -v --html=.claude/reports/<TICKET-ID>/integration-report.html --self-contained-html` | `.claude/reports/<TICKET-ID>/integration-report.html` |
| 3 | E2E | `python -m pytest tests/e2e/ -v --html=.claude/reports/<TICKET-ID>/e2e-report.html --self-contained-html` | `.claude/reports/<TICKET-ID>/e2e-report.html` |
| 4 | Combined | `python scripts/generate_html_report.py --ticket <TICKET-ID>` | `.claude/reports/<TICKET-ID>/index.html` |

## 6. Defect Management
- Defects found → create JIRA sub-task under <TICKET-ID> via MCP
- Severity: Blocker / Critical / Major / Minor
- Blocker/Critical defects: halt Phase 7, return to Phase 5

## 7. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| pytest-html not installed | No HTML reports | Install: `pip install pytest-html` |
| Playwright browser missing | E2E cannot run | Run: `playwright install chromium` |
| Port conflict on E2E run | Flask won't start | conftest.py uses ephemeral sockets |
```

### Step 4 — Push to Confluence
Use `confluence_create_page`:
- **title**: `<TICKET-ID> Test Plan`
- **parent_title**: `<TICKET-ID> Test Strategy` (child of the strategy page)
- **content**: the markdown above

Store the Confluence URL in state.json: `phases.7.2.confluence_url`.

### Step 5 — Commit
```bash
git add .claude/artifacts/<TICKET-ID>/test-plan.md
git commit -m "docs(<TICKET-ID>): Phase 7.2 test plan"
```

### Step 6 — Update state
`phases.7.2 = "complete"`, `current_phase = "7.3"`.
