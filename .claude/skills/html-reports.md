# Skill: html-reports

## Purpose
Generate self-contained HTML test reports for each story and a combined index page that links all three test types.

## Directory structure
```
reports/
  <TICKET-ID>/
    unit-report.html          ← pytest-html output
    integration-report.html   ← pytest-html output
    e2e-report.html           ← pytest-html output
    index.html                ← combined summary (from generate_html_report.py)
```

## Generating individual reports

### Unit tests
```bash
python -m pytest tests/unit/ -v \
  --html=reports/<TICKET-ID>/unit-report.html \
  --self-contained-html
```

### Integration tests
```bash
python -m pytest tests/integration/ -v \
  --html=reports/<TICKET-ID>/integration-report.html \
  --self-contained-html
```

### E2E tests
```bash
python -m pytest tests/e2e/ -v \
  --html=reports/<TICKET-ID>/e2e-report.html \
  --self-contained-html
```

## Generating the combined index

```bash
python scripts/generate_html_report.py --ticket <TICKET-ID>
```

This script reads the three individual reports, extracts pass/fail counts, and writes a `reports/<TICKET-ID>/index.html` with:
- Summary table (type, total, passed, failed, skipped)
- Overall status badge (PASS / FAIL)
- Links to each sub-report
- Timestamp and ticket ID

## Opening a report
```bash
# Windows
start reports/<TICKET-ID>/index.html
# Or open in browser:
python -m http.server 8080 --directory reports/<TICKET-ID>/
# Then visit http://localhost:8080/
```

## pytest.ini configuration (add if missing)
Add to `pytest.ini` or `pyproject.toml`:
```ini
[pytest]
addopts = --tb=short
```

## Installing pytest-html
```bash
pip install pytest-html
```

## Report in Confluence
After generating reports, create/update the `<TICKET-ID> Test Results` Confluence page (see `confluence-sync` skill) with a summary table and a note that full HTML reports are available locally at `reports/<TICKET-ID>/index.html`.
