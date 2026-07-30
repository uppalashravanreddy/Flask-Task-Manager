---
mode: agent
description: Phase 8 — Create the Pull Request with a complete description, changelog entry, and reviewer checklist, completing the agentic SDLC cycle.
tools:
  - read_file
  - write_file
  - run_in_terminal
---

You are acting as the `pr` agent for SDLC Phase 8.

Before creating the PR, verify:
1. Read `docs/artifacts/FLASK-001/verification_report.md` — all gates must show PASS.
2. Read `docs/artifacts/FLASK-001/review_report.md` — no open High severity findings.

If either check fails, stop and report the issue.

When checks pass:
1. Ensure all changes are committed on branch `feat/FLASK-001-doc-sync`.
2. Push: `git push -u origin feat/FLASK-001-doc-sync`
3. Write `.sdlc/pr-description.md` with all six required sections:
   - **Summary** (2–3 sentences: what, why, outcome)
   - **Changes Made** (table: file, change type, reason)
   - **Test Evidence** (paste pytest output from verification_report.md)
   - **Known Limitations** (anything "Not Specified" or deferred)
   - **CHANGELOG Entry** (version, date, what was added)
   - **Reviewer Checklist** (tick-list the reviewer must complete before approving)
4. Create the PR:
   ```
   gh pr create --title "feat(FLASK-001): Automated Documentation Sync pipeline" --body-file .sdlc/pr-description.md --base main --head feat/FLASK-001-doc-sync
   ```
5. Append the changelog entry to `CHANGELOG.md`.
6. Run: `python scripts/state_manager.py complete 8`
7. Run: `python scripts/reporter.py` to generate the final SDLC pipeline report at `.sdlc/sdlc-report.md`
