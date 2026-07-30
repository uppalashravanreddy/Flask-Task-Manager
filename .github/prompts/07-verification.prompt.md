---
mode: agent
description: Phase 7 — Run the full test suite, validate pipeline output quality, and produce a verification report. All gates must pass before Phase 8.
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

You are acting as the `verification` agent for SDLC Phase 7.

Execute verification in this exact order:

**Gate 1 — Unit tests**
```
python -m pytest tests/unit/ -v --tb=short
```

**Gate 2 — Integration tests**
```
python -m pytest tests/integration/ -v --tb=short
```

**Gate 3 — Full pipeline run**
```
python src/main.py --repo . --output docs/artifacts/FLASK-001/technical_profile_report.md
```

**Gate 4 — Document quality check**
Read `docs/artifacts/FLASK-001/technical_profile_report.md` and verify:
- [ ] Contains: Project Overview, Technical Stack, Entry Point, Data Model, Routes, Forms, Dependencies
- [ ] No section has blank content (missing values show "Not Specified")
- [ ] File size > 500 bytes

Write `docs/artifacts/FLASK-001/verification_report.md` with:
- Test run summary (total/passed/failed/errors)
- Test results detail table
- End-to-end pipeline result (exit code, output file, size)
- Document quality checks table
- Gate status table (PASS/FAIL per gate)
- Overall PASS/FAIL

If any gate is FAIL: diagnose and fix before proceeding.
Only when all gates are PASS: run `python scripts/state_manager.py complete 7`
