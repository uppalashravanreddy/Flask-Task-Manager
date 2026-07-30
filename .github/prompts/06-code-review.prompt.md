---
mode: agent
description: Phase 6 — Structured peer code review across 7 dimensions. Outputs review_report.md.
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

You are acting as the `code-review` agent for SDLC Phase 6.

Review every file in `src/doc_sync/` and `scripts/` against this checklist:

| Area | Question |
|---|---|
| Correctness | Does the code fulfil every FR in requirements.md? |
| Security | No hardcoded secrets? `.env` used correctly? Output is PII-free? |
| Error Handling | Missing files, empty repos, malformed content all handled? |
| Test Coverage | Happy path AND "Not Specified" edge cases tested? |
| Code Clarity | Self-explanatory names? Logic readable without inline comments? |
| DRY | Any duplicated logic that can be extracted to a shared function? |
| Dependency Safety | Are packages in requirements.txt pinned and free of known CVEs? |

For each finding:
1. Show the problem and your proposed fix.
2. Wait for approval before applying the change.
3. Run tests after each fix.

Write `docs/artifacts/FLASK-001/review_report.md` with:
- Findings table (ID, file, line, area, severity, finding, fix applied)
- Refactoring applied
- Test gap analysis
- Dependency audit
- Sign-off checklist

Commit all fixes, then run: `python scripts/state_manager.py complete 6`
