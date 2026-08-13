# Skill: write-test-cases

## Purpose
Write structured test cases from Acceptance Criteria, covering all three levels (unit / integration / E2E), and produce both the test-cases.md artifact and runnable pytest code.

## TC-ID naming convention
```
TC-<TICKET-ID>-UNIT-<NN>       (e.g. TC-FLASK-002-UNIT-01)
TC-<TICKET-ID>-INT-<NN>        (e.g. TC-FLASK-002-INT-01)
TC-<TICKET-ID>-E2E-<NN>        (e.g. TC-FLASK-002-E2E-01)
```

## Per-AC decision tree

```
AC requires visual rendering (badge, colour, layout)?
  └─ YES → E2E test (pytest-playwright)

AC requires DB column or route?
  └─ YES → Integration test
      └─ Also needs unit test for the logic? → BOTH

AC is pure Python logic (sort key, dict lookup, constant)?
  └─ YES → Unit test only
```

## Unit test template
```python
def test_<feature>_<scenario>():
    """One-line docstring: what this asserts."""
    # arrange
    ...
    # act
    result = function_under_test(...)
    # assert
    assert result == expected_value
```

## Integration test template (with Flask test client)
```python
@pytest.fixture
def app():
    from app import app as flask_app, db
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False,
                             SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_<feature>_route(client):
    resp = client.post("/add", data={"title": "T", "desc": "D", "priority": "High"}, follow_redirects=True)
    assert resp.status_code == 200
```

## E2E test template (pytest-playwright)
```python
from playwright.sync_api import Page, expect

def test_<feature>_renders(page: Page, flask_base_url: str) -> None:
    """E2E: <what the user sees>."""
    page.goto(f"{flask_base_url}/")
    element = page.locator("<selector>")
    expect(element).to_be_visible()
```

## test-cases.md table structure
```markdown
| TC-ID | AC-ID | Title | Level | Automated | Pytest Path | Priority | Status |
|-------|-------|-------|-------|-----------|-------------|----------|--------|
```

## Writing rules
- One test function = one assertion group (don't mix multiple ACs in one test).
- Descriptive names: `test_high_priority_task_sorted_before_medium` not `test_sort`.
- E2E tests that add data must use unique titles to avoid collision with other tests.
- Parametrize where 3+ test cases share the same logic but different values.
