# Testing Standards

## Structure
- Unit tests: `tests/unit/test_<feature>.py`
- Integration tests: `tests/integration/test_<feature>_<scope>.py`
- No E2E tests in this project (Playwright not configured).

## Running tests
```bash
python -m pytest tests/unit/ tests/integration/ -v
```
Run from the project root (`Flask-Task-Manager/`).

## Unit test rules
- Test one function/constant at a time.
- No Flask app context needed for pure Python logic (constants, sort keys, PRIORITY_RANK).
- Use `pytest.mark.parametrize` for value-driven tests (multiple priorities, edge cases).
- Must include: happy path + at least one edge case per function.

## Integration test rules
- Use `pytest` fixtures with `app.config['TESTING'] = True` and `SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'`.
- Each test gets a fresh in-memory database — never share state across tests.
- Migration tests: create a real SQLite file in `tmp_path`, run the migration, assert schema + data.

## What to test
For every new field or feature, tests must cover:
1. The data model stores and returns the value correctly.
2. The form validates acceptable values and rejects invalid ones.
3. The sort/display order matches the specification.
4. Edge cases: unknown values, NULL/empty state, duplicate inserts.
5. Idempotency of any migration script.

## What NOT to test
- Flask internals (routing, CSRF, session) — trust the framework.
- HTML rendering details — test data logic, not template string matching.
- Do NOT mock the database in integration tests.
