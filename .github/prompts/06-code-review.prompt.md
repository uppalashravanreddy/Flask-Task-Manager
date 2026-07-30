---
mode: agent
description: "Phase 6 — Structured peer code review across 7 dimensions. Propose each fix before applying. Output review_report.md."
tools:
  - read_file
  - write_file
  - run_in_terminal
  - get_errors
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/01-coding-standards.md
#file:.github/instructions/02-testing-standards.md
#file:.github/instructions/03-security-standards.md
#file:.github/skills/analyze-codebase.md
#file:.github/skills/run-tests.md
#file:.github/skills/generate-docs.md

## Constraints
- NEVER change working logic without proposing the change and waiting for approval
- NEVER delete a test — if a test is wrong, flag it as a Minor finding and propose the fix
- Only fix files in `src/doc_sync/`, `scripts/`, `tests/`, `app.py`, `routes.py`, `requirements.txt`
- Run tests after every fix to confirm nothing broke

## Input
Review all of these:
- #file:src/doc_sync/repo_scanner.py
- #file:src/doc_sync/extractor.py
- #file:src/doc_sync/page_creator.py
- #file:src/main.py
- #file:app.py
- #file:routes.py
- #file:requirements.txt
- #file:tests/unit/test_doc_sync.py
- #file:tests/unit/test_extractor.py
- #file:tests/unit/test_repo_scanner.py
- #file:tests/integration/test_pipeline.py
- #file:docs/artifacts/FLASK-001/requirements.md  ← traceability

## Review Dimensions (cover ALL seven)

| Dimension | Review Question |
|---|---|
| Correctness | Does each component fulfil every FR in requirements.md? |
| Security | No hardcoded secrets? `.env` used? Output is PII-free? SECRET_KEY from env? |
| Error Handling | Missing files, empty repos, malformed content all handled? Returns "Not Specified"? |
| Test Coverage | Happy path AND "Not Specified" / missing-file / empty edge cases tested? |
| Code Clarity | Self-explanatory names? Logic readable without comments? |
| DRY | Duplicated logic that can be extracted to a shared function? |
| Dependency Safety | Version pins present? Known CVEs? `datetime` removed from requirements.txt? |

## Output Specification

```markdown
# Code Review Report — FLASK-001

| Field | Value |
|---|---|
| Ticket ID | FLASK-001 |
| Phase | 6 — Code Review |
| Status | Draft |
| Author | GitHub Copilot (code-review agent) |
| Files Reviewed | (list) |
| Date | YYYY-MM-DD |

## 1. Findings
| ID | File | Line | Dimension | Severity | Finding | Fix Applied |
|---|---|---|---|---|---|---|
| CR-01 | app.py | 4 | Security | High | Hardcoded SECRET_KEY | Yes |

## 2. Refactoring Applied
(description of DRY improvements)

## 3. Test Gap Analysis
| Missing Test | Scenario | Added |
|---|---|---|

## 4. Dependency Audit
| Package | Version in requirements.txt | Issue | Recommendation |
|---|---|---|---|

## 5. Sign-Off Checklist
- [ ] All High severity findings resolved
- [ ] No hardcoded secrets remain
- [ ] All tests pass after fixes
- [ ] Dependency pins added
```

## Success Criteria
- All High findings resolved
- Tests pass after all fixes
- `review_report.md` exists and is > 500 bytes

## On Failure
If a High finding cannot be resolved: `python scripts/state_manager.py fail 6 "<reason>"`

## State Transition
When complete: `python scripts/state_manager.py complete 6`
${input:review_depth:Full review across all 7 dimensions}
