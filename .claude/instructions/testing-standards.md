# Testing Standards

## Test directory layout
```
tests/
  unit/             pytest unit tests (pure Python, no DB, no Flask)
  integration/      pytest integration tests (in-memory SQLite, Flask test client)
  e2e/
    conftest.py     starts Flask on ephemeral port for Playwright
    test_*.py       Playwright E2E tests
```

## Running tests
```bash
# Quick check (Phase 5)
python -m pytest tests/unit/ tests/integration/ -v -q

# Full with HTML reports (Phase 7.4)
python -m pytest tests/unit/ -v --html=.claude/reports/<TICKET-ID>/unit-report.html --self-contained-html
python -m pytest tests/integration/ -v --html=.claude/reports/<TICKET-ID>/integration-report.html --self-contained-html
python -m pytest tests/e2e/ -v --html=.claude/reports/<TICKET-ID>/e2e-report.html --self-contained-html
python scripts/generate_html_report.py --ticket <TICKET-ID>
```

Run from the project root (`Flask-Task-Manager/`).

## Unit test rules
- No Flask app context, no database.
- Test: constants, sort keys, PRIORITY_RANK dict, form choices.
- Use `pytest.mark.parametrize` for value-driven tests.
- Must include: happy path + at least one edge case.

## Integration test rules
- Use `pytest` fixtures with `app.config['TESTING'] = True` and `SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'`.
- Each test gets a fresh in-memory database — no shared state.
- Migration tests: create a real SQLite file in `tmp_path`, run the migration, assert schema + data.
- NEVER mock the database.

## E2E test rules (Playwright)
- Use `flask_base_url` fixture from `tests/e2e/conftest.py` — DO NOT hardcode `localhost:5000`.
- Use `expect(locator).to_be_visible()` for assertions — not raw string matching on HTML.
- Unique task titles per test to avoid inter-test collisions.
- Badge rendering MUST be tested at E2E level — unit tests cannot verify CSS classes in rendered HTML.
- Selector priority: `data-testid` > `name` attribute > visible text > CSS class.

## Test case deduplication
Before writing a new test: run `python -m pytest tests/ --collect-only -q` and search existing tests.
If a test already covers the same assertion → reference it, don't duplicate.

## What to test per feature
1. The data model stores and returns the value correctly.
2. The form validates acceptable values and rejects invalid ones.
3. The sort/display order matches the specification.
4. Edge cases: unknown values, NULL/empty state, duplicate inserts.
5. Idempotency of any migration script.
6. Visual rendering (badge colour, label text) — E2E only.

## Phase 7 testing sub-pipeline artifacts
Each story produces:
- `.claude/artifacts/<TICKET-ID>/test-strategy.md`
- `.claude/artifacts/<TICKET-ID>/test-plan.md`
- `.claude/artifacts/<TICKET-ID>/test-cases.md`
- `.claude/reports/<TICKET-ID>/unit-report.html`
- `.claude/reports/<TICKET-ID>/integration-report.html`
- `.claude/reports/<TICKET-ID>/e2e-report.html`
- `.claude/reports/<TICKET-ID>/index.html`
- `.claude/artifacts/<TICKET-ID>/verification_report.md`

## Confluence
- Every test artifact is pushed to Confluence using `confluence-sync` skill.
- Page hierarchy: QA > <TICKET-ID> Test Strategy > Test Plan > Test Cases > Test Results > Verification

## What NOT to test
- Flask routing internals and CSRF — trust the framework.
- HTML string matching — use Playwright `expect(locator)` instead.
- Do NOT modify tests to make them pass — fix the production code.
