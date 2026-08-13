# Skill: run-tests

## Purpose
Run the test suite and report results in a standard format.

## Commands

### Full suite (Phase 5 and Phase 7)
```bash
python -m pytest tests/unit/ tests/integration/ -v
```

### Unit tests only
```bash
python -m pytest tests/unit/ -v
```

### Integration tests only
```bash
python -m pytest tests/integration/ -v
```

### List tests without running
```bash
python -m pytest tests/ --collect-only -q
```

## Reporting format
After the test run, output:
```
Test results: <N> passed, <M> failed, <K> errors
Unit tests:   <n> passed
Integration:  <m> passed
```

If any test fails, output the failure name and the first assertion error line.

## Rules
- Run from the project root directory (`Flask-Task-Manager/`).
- If `ModuleNotFoundError` occurs: run `pip install -r requirements.txt` first.
- Do NOT modify tests to make them pass — fix the source code.
- A migration test failure may indicate the migration script has a bug — check `scripts/migrate_*.py`.
