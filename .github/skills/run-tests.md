# Skill: Run Tests

Use this skill whenever you need to execute or interpret the test suite for Flask Task Manager.

## Test Commands

### Run all tests
```bash
python -m pytest tests/ -v --tb=short
```

### Run only unit tests
```bash
python -m pytest tests/unit/ -v --tb=short
```

### Run only integration tests
```bash
python -m pytest tests/integration/ -v --tb=short
```

### Run a specific test file
```bash
python -m pytest tests/unit/test_extractor.py -v --tb=short
```

### Run with coverage report
```bash
python -m pytest tests/ -v --tb=short --cov=src --cov-report=term-missing
```

## Test File Locations

| File | What It Tests | Type |
|---|---|---|
| `tests/unit/test_repo_scanner.py` | File reading (exists/missing), scan target list | Unit |
| `tests/unit/test_extractor.py` | Metadata extraction, fallback to "Not Specified" | Unit |
| `tests/unit/test_doc_sync.py` | Fact collection, Markdown generation, pipeline run | Unit |
| `tests/integration/test_pipeline.py` | Full end-to-end: temp repo → report file | Integration |

## Interpreting Results

- `PASSED` — test succeeded
- `FAILED` — assertion error; read the diff in `--tb=short` output
- `ERROR` — exception before assertion; read the traceback
- `WARNING` — non-fatal; check if it affects correctness

## When Tests Fail

1. Read the `FAILED` section carefully — find the exact assertion.
2. Read the source file at the failing line.
3. Determine: is the test wrong, or is the code wrong?
4. Fix the root cause — never delete a failing test.
5. Re-run after fixing to confirm green.

## Generate HTML Test Report

After any test run, generate the HTML test report:
```bash
python scripts/test_runner.py
```
Opens at: `reports/test-report.html`

The report includes:
- Summary bar (total / passed / failed / errors / duration)
- Test results table with status badges
- Failure accordion with full tracebacks for each failed test
- Re-run hint showing the exact `pytest --lf` command

## Required Test Coverage

Every new function must have:
- A happy-path test
- A "Not Specified" / missing-file / empty-input edge case test

Test file naming convention: `test_<module_name>.py` in the appropriate `unit/` or `integration/` directory.
