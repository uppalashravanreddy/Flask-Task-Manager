# Instruction: Testing Standards

Apply these rules when writing, running, or evaluating tests.

## Framework and Location
- Test framework: `pytest` (not unittest)
- Unit tests: `tests/unit/test_<module_name>.py`
- Integration tests: `tests/integration/test_<module_name>.py`
- Never mix unit and integration tests in the same file

## Required Coverage Per Function
Every new public function must have at minimum:
1. **Happy-path test** — valid inputs, expected output
2. **Missing-input test** — `None`, empty string, or missing file → output is `"Not Specified"` or `None`
3. **Error-path test** — if the function calls I/O or external APIs

## Test Naming Convention
```python
def test_<function_name>_<scenario>():
    # arrange
    # act
    # assert
```
Examples:
- `test_read_repository_files_returns_dict_for_valid_repo()`
- `test_read_repository_files_returns_empty_strings_for_missing_files()`
- `test_extract_returns_not_specified_when_readme_missing()`

## Test Design Rules
- Use `tmp_path` fixture for file-system tests — never hardcode paths
- Never modify `instance/data.db` or any committed file in tests
- Never use `monkeypatch` to skip real I/O in integration tests
- Assert specific values, not just "not None" or "truthy"
- Never delete a failing test — fix the root cause

## Running Tests
```bash
# All tests
python -m pytest tests/ -v --tb=short

# Unit only
python -m pytest tests/unit/ -v --tb=short

# Integration only
python -m pytest tests/integration/ -v --tb=short

# With HTML report
python scripts/test_runner.py

# Rerun only failures
python -m pytest tests/ --lf -v --tb=short
```

## Diagnosing Failures
1. Read the `FAILED` line — find the exact assertion
2. Read the source file at the failing line number
3. Ask: is the test wrong, or is the code wrong?
4. Fix the root cause — if code is wrong, fix the code; if test expectation changed with a valid requirement update, update the test

## CI Gate
All tests must pass before Phase 7 (Verification) can be marked complete. Failed tests block the PR creation in Phase 8.
