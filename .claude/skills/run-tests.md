# Skill: run-tests

## Purpose
Run the test suite and generate HTML reports. Called by Phases 5, 7.4, and 7.5.

## Install test dependencies (one-time)
```bash
pip install pytest-html pytest-playwright
playwright install chromium
```

## Phase 5 — quick check (no HTML reports)
```bash
python -m pytest tests/unit/ tests/integration/ -v -q
```

## Phase 7.4 — full run with HTML reports
```bash
# Create report directory first
python -c "import os; os.makedirs('reports/<TICKET-ID>', exist_ok=True)"

# Unit
python -m pytest tests/unit/ -v --html=.claude/reports/<TICKET-ID>/unit-report.html --self-contained-html

# Integration
python -m pytest tests/integration/ -v --html=.claude/reports/<TICKET-ID>/integration-report.html --self-contained-html

# E2E
python -m pytest tests/e2e/ -v --html=.claude/reports/<TICKET-ID>/e2e-report.html --self-contained-html

# Combined index
python scripts/generate_html_report.py --ticket <TICKET-ID>
```

## Single test file (debugging)
```bash
python -m pytest tests/unit/test_priority.py -v -s
```

## Collect without running
```bash
python -m pytest tests/ --collect-only -q
```

## Reporting format
After any run, output:
```
Test results: <N> passed, <M> failed, <K> errors
Unit:        <n> passed
Integration: <m> passed
E2E:         <k> passed, <s> skipped
Reports:     .claude/reports/<TICKET-ID>/index.html
```

## If a test fails
1. Read the failure message carefully — it shows file + line + assertion.
2. Fix the SOURCE code (models.py, routes.py, forms.py, templates/) — NEVER modify tests to pass.
3. Re-run only the failing test file first, then the full suite.

## Common issues

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `playwright not found` | `pip install pytest-playwright && playwright install chromium` |
| `pytest-html not found` | `pip install pytest-html` |
| `pytest: no tests ran` | Check test file name starts with `test_`, function starts with `test_` |
| Wrong rootdir in output | Run pytest from `Flask-Task-Manager/` directory |
