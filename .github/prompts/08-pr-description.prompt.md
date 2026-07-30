---
mode: agent
description: "Phase 8 — Create the PR with complete description, changelog, and reviewer checklist. Generate final SDLC HTML report."
tools:
  - read_file
  - write_file
  - run_in_terminal
---

## Context
#file:.github/instructions/00-project-context.md
#file:.github/instructions/03-security-standards.md
#file:.github/instructions/04-failure-handling.md
#file:.github/skills/git-operations.md
#file:.github/skills/sdlc-state.md

## Constraints
- NEVER create the PR if any verification gate shows FAIL
- NEVER create the PR if open High severity findings remain in review_report.md
- PR description MUST contain all six required sections
- Branch must be pushed to origin before PR creation
- CHANGELOG.md must be updated as part of this phase

## Input
Read these gate-check files first:
- #file:docs/artifacts/FLASK-001/verification_report.md  ← all gates must be PASS
- #file:docs/artifacts/FLASK-001/review_report.md        ← no open High findings

## Task

**Pre-flight checks:**
1. Read `verification_report.md` — confirm "Overall: PASS" and all 5 gates show PASS
2. Read `review_report.md` — confirm no High severity finding is unresolved
3. If either check fails: STOP — report the blocker to the developer

**When checks pass:**

Step 1 — Ensure branch and commits
```bash
git checkout -b feat/FLASK-001-doc-sync 2>/dev/null || git checkout feat/FLASK-001-doc-sync
git status
git push -u origin feat/FLASK-001-doc-sync
```

Step 2 — Write `.sdlc/pr-description.md` using the template below

Step 3 — Create PR
```bash
gh pr create \
  --title "feat(FLASK-001): Automated Documentation Sync pipeline" \
  --body-file .sdlc/pr-description.md \
  --base main \
  --head feat/FLASK-001-doc-sync
```

Step 4 — Update CHANGELOG.md (append if exists, create if not)

Step 5 — Advance state and generate final reports
```bash
python scripts/state_manager.py complete 8
python scripts/html_report.py
python scripts/test_runner.py
```

## PR Description Template (write to `.sdlc/pr-description.md`)

```markdown
## Summary
(2-3 sentences: what was built, why it was built, what problem it solves)

## Changes Made
| File | Change Type | Reason |
|---|---|---|
| src/doc_sync/repo_scanner.py | Added | Reads 6 canonical repo files |

## Test Evidence
Run: python scripts/test_runner.py
Open: reports/test-report.html

(paste full pytest output here)

## Known Limitations
- (list "Not Specified" items or deferred scope)

## CHANGELOG Entry
### [1.0.0] — YYYY-MM-DD
#### Added
- FLASK-001: Automated Documentation Sync pipeline

## Reviewer Checklist
- [ ] requirements.md covers all acceptance criteria from problem_spec.md
- [ ] architecture.md matches the actual implementation
- [ ] All tests pass (see Test Evidence section)
- [ ] No hardcoded secrets in any production file
- [ ] Generated report has no blank sections (all missing values show "Not Specified")
- [ ] CHANGELOG.md updated
- [ ] Branch is based on latest main
- [ ] PR description contains all six required sections
```

## Success Criteria
- PR created on GitHub with URL returned
- `CHANGELOG.md` updated
- `reports/sdlc-summary.html` shows all 8 phases green
- `reports/test-report.html` generated and accurate

## On Failure
If `gh pr create` fails: check `gh auth status`, push branch, retry once.
If branch push fails: check remote permissions.

## State Transition
`python scripts/state_manager.py complete 8`
${input:pr_labels:enhancement,documentation}
