# Pull Request Description — FLASK-002: Task Priority

| Field     | Value                                    |
|-----------|------------------------------------------|
| Ticket ID | FLASK-002                                |
| Phase     | 8 — Pull Request                         |
| Branch    | feat/FLASK-002-claude-task-priority      |
| Base      | main                                     |
| Author    | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date      | 2026-08-13                               |

---

## Summary

Adds a three-level task priority system (High / Medium / Low) to the Flask Task Manager. Users can now assign priority when creating or editing a task; the task list automatically sorts by priority (High first) and displays a colour-coded Bootstrap badge alongside each task title. All pre-existing tasks receive a default priority of Medium via a safe, idempotent migration script.

---

## Changes Made

| File | Action | Reason |
|------|--------|--------|
| `models.py` | Modified | Added `priority` column (`String(10)`, default `'Medium'`) to `Task` model |
| `forms.py` | Modified | Added `SelectField` with `PRIORITY_CHOICES` and `PRIORITY_RANK` constants; imported `SelectField` from wtforms |
| `routes.py` | Modified | `index()` sorts tasks by `PRIORITY_RANK`; `add()` passes priority to Task constructor; `edit()` reads and writes priority |
| `templates/index.html` | Modified | Priority badge rendered per task using Bootstrap 4 badge classes |
| `templates/add.html` | Modified | Priority dropdown added as optional field (defaults to Medium) |
| `templates/edit.html` | Modified | Priority dropdown added, pre-selected from current task value |
| `scripts/migrate_add_priority.py` | Created | Safe, idempotent SQLite migration — adds column and backfills NULLs |
| `tests/unit/test_priority.py` | Created | 6 unit tests covering sort order, unknown priority fallback, choices consistency |
| `tests/integration/test_priority_migration.py` | Created | 4 integration tests covering migration add, backfill, idempotency, post-migration inserts |
| `.claude/artifacts/FLASK-002/requirements.md` | Created | Phase 1 SDLC artifact |
| `.claude/artifacts/FLASK-002/architecture.md` | Created | Phase 2 SDLC artifact |
| `.claude/artifacts/FLASK-002/design-review.md` | Created | Phase 3 SDLC artifact — caught Bootstrap version mismatch before implementation |
| `.claude/artifacts/FLASK-002/impl-plan.md` | Created | Phase 4 SDLC artifact |
| `.claude/artifacts/FLASK-002/review_report.md` | Created | Phase 6 SDLC artifact |
| `.claude/artifacts/FLASK-002/verification_report.md` | Created | Phase 7 SDLC artifact |

---

## Test Evidence

```
python -m pytest tests/unit/ tests/integration/ -v

21 passed, 0 failed, 18 warnings in 0.46s

New tests:
  tests/unit/test_priority.py            6/6  PASS
  tests/integration/test_priority_migration.py  4/4  PASS

Regression (pre-existing):
  tests/unit/test_doc_sync.py            4/4  PASS
  tests/unit/test_extractor.py           2/2  PASS
  tests/unit/test_repo_scanner.py        3/3  PASS
  tests/unit/test_report_surface.py      1/1  PASS
  tests/integration/test_pipeline.py     1/1  PASS
```

---

## SDLC Feedback Loop Applied

One design issue was caught and corrected before implementation via the Phase 3 Design Review:

| Issue | Phase Caught | Resolution |
|-------|-------------|------------|
| RISK-1: Architecture doc specified Bootstrap 5 badge classes; app uses Bootstrap 4.5 | Phase 3 | Corrected to `badge badge-danger/warning/success` before any template was written |
| RISK-2: `ALTER TABLE` sets default for new rows but does not backfill existing NULLs | Phase 3 | Added `UPDATE task SET priority = 'Medium' WHERE priority IS NULL` to migration script |

---

## Known Limitations

- E2E Playwright tests were not run against a live server in this pipeline pass. UI badge rendering and sort order require a manual smoke test on `python app.py`.
- `Task.query.get()` deprecation (SQLAlchemy 2.x) is a pre-existing issue not introduced by FLASK-002.
- The `SECRET_KEY` fallback in `app.py` is a pre-existing concern (OBS-1), tracked separately.
- Priority filtering (show only High tasks) is explicitly out of scope for this sprint.

---

## Reviewer Checklist

Before approving this PR, the reviewer must confirm:

- [ ] `python scripts/migrate_add_priority.py` runs without error on a local copy of `instance/data.db`
- [ ] After migration, all pre-existing tasks display a Medium badge on the task list
- [ ] A new task created without selecting priority displays a Medium badge
- [ ] A new task created with High priority displays a red badge and sorts to the top of the list
- [ ] Editing an existing task and changing priority to Low updates the badge and repositions the task
- [ ] `pytest tests/unit/ tests/integration/ -v` reports 21 passed, 0 failed
- [ ] No hardcoded secrets are present in any file changed by this PR
- [ ] `requirements.txt` is unchanged (no new dependencies introduced)
