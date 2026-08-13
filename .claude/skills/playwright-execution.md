# Skill: playwright-execution

## Purpose
Run Playwright E2E tests via pytest-playwright, use the Playwright MCP to visually verify the running app, and generate HTML reports.

## Two modes of Playwright in this pipeline

### Mode 1 — pytest-playwright (automated test runner)
Used in Phase 7.4 to run the full E2E test suite.

```bash
# Install (one-time)
pip install pytest-playwright
playwright install chromium

# Run all E2E tests with HTML report
python -m pytest tests/e2e/ -v \
  --html=.claude/reports/<TICKET-ID>/e2e-report.html \
  --self-contained-html

# Run a single test for debugging
python -m pytest tests/e2e/test_priority_ui.py::test_priority_badge_shown_for_high_task -v -s
```

### Mode 2 — Playwright MCP (visual verification by Claude)
Used to interactively verify the UI is working as expected after implementation.

The MCP is configured in `.vscode/mcp.json` under key `"playwright"`.

Available tools:
- `playwright_navigate` — go to a URL
- `playwright_screenshot` — take a screenshot
- `playwright_click` — click an element
- `playwright_fill` — fill an input field
- `playwright_select` — select a dropdown option
- `playwright_get_text` — get visible text

**Example: verify priority badge after adding a task**
```
playwright_navigate: http://localhost:5000/add
playwright_fill: selector="input[name='title']", value="Test High Task"
playwright_fill: selector="input[name='desc']", value="desc"
playwright_select: selector="select[name='priority']", value="High"
playwright_click: selector="button[type='submit']"
playwright_navigate: http://localhost:5000/
playwright_screenshot: → verify badge-danger is visible
```

## conftest.py pattern
The project's `tests/e2e/conftest.py` starts Flask on an ephemeral port in a background thread. Tests use `flask_base_url` fixture, NOT `localhost:5000`. This avoids conflicts with a running dev server.

## Running the Flask dev server separately (for MCP mode)
```bash
python app.py   # starts on port 5000
```
Then use the Playwright MCP against `http://localhost:5000`.

## HTML report generation
```bash
python -m pytest tests/e2e/ -v --html=.claude/reports/<TICKET-ID>/e2e-report.html --self-contained-html
```
The `--self-contained-html` flag embeds all CSS/JS so the file opens anywhere.

## Common failures and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Executable doesn't exist` | Chromium not installed | `playwright install chromium` |
| `Connection refused` | Flask not started | Check conftest.py, add `time.sleep(1.5)` after thread start |
| `TimeoutError on locator` | Element not visible in time | Use `expect(locator).to_be_visible(timeout=5000)` |
| `StrictModeViolation` | Multiple elements match selector | Use `.first` or a more specific selector |
