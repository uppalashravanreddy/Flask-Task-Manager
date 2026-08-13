# Implementation Plan — KAN-27

| Field | Value |
|---|---|
| Ticket ID | KAN-27 |
| Summary | US-21: Assign priority level (High/Medium/Low) to tasks |
| Phase | 4 — Implementation Planning |
| Status | Complete |
| Author | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date | 2026-08-13 |

---

## Overview

All implementation tasks are ordered so that data-layer changes happen before form/route changes, which happen before template changes. The migration and tests are handled last to validate the full stack. Each task is atomic (one file or one logical change) and independently verifiable.

---

## Implementation Tasks

### TASK-1 — Update `models.py`: add `priority` column
- **File**: `models.py`
- **Change**: Add `priority = db.Column(db.String(10), nullable=False, default='Medium')` to `Task` model.
- **Depends on**: nothing
- **Verify**: `from models import Task; print(Task.priority)` — no import error; column present in `Task.__table__.columns`.

### TASK-2 — Update `forms.py`: add `PRIORITY_CHOICES`, `PRIORITY_RANK`, `priority` field
- **File**: `forms.py`
- **Change**:
  1. Add `PRIORITY_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]`
  2. Add `PRIORITY_RANK = {'High': 1, 'Medium': 2, 'Low': 3}`
  3. Add `priority = SelectField('Priority', choices=PRIORITY_CHOICES, default='Medium')` to `AddTaskForm`
- **Depends on**: TASK-1
- **Verify**: `from forms import PRIORITY_RANK, PRIORITY_CHOICES, AddTaskForm` — no error; `len(PRIORITY_CHOICES) == 3`.

### TASK-3 — Update `routes.py`: sort by priority in `index()`
- **File**: `routes.py`
- **Change**:
  1. `from forms import PRIORITY_RANK`
  2. Change `Task.query.all()` to `sorted(Task.query.all(), key=lambda t: PRIORITY_RANK.get(t.priority, 2))`
- **Depends on**: TASK-2
- **Verify**: `GET /` returns tasks in High→Medium→Low order.

### TASK-4 — Update `routes.py`: persist priority in `add()`
- **File**: `routes.py`
- **Change**: Include `priority=form.priority.data` in `Task(...)` constructor call.
- **Depends on**: TASK-2
- **Verify**: POST to `/add` with `priority=High` stores `High`; default POST stores `Medium`.

### TASK-5 — Update `routes.py`: pre-fill and persist priority in `edit()`
- **File**: `routes.py`
- **Change**:
  1. On GET: `form.priority.data = task.priority`
  2. On POST: `task.priority = form.priority.data`
- **Depends on**: TASK-2
- **Verify**: Edit form shows current priority pre-selected; POST updates priority in DB.

### TASK-6 — Update `templates/index.html`: render priority badge
- **File**: `templates/index.html`
- **Change**: Add Jinja2 `{% if %}` block inside task card to render `badge-danger` / `badge-warning` / `badge-success` based on `task.priority`.
- **Depends on**: TASK-3
- **Verify**: Home page shows red badge for High, yellow for Medium, green for Low.

### TASK-7 — Update `templates/add.html`: render priority select
- **File**: `templates/add.html`
- **Change**: Add `{{ form.priority(class="form-control") }}` inside a new form row.
- **Depends on**: TASK-2
- **Verify**: Add page shows Priority dropdown with three options; Medium pre-selected.

### TASK-8 — Update `templates/edit.html`: render pre-filled priority select
- **File**: `templates/edit.html`
- **Change**: Add `{{ form.priority(class="form-control") }}` inside a new form row.
- **Depends on**: TASK-5
- **Verify**: Edit page shows Priority dropdown with the task's current priority pre-selected.

### TASK-9 — Create `scripts/migrate_add_priority.py`
- **File**: `scripts/migrate_add_priority.py` (new)
- **Change**: Idempotent script: `ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'Medium'` + `UPDATE` for NULL rows.
- **Depends on**: TASK-1
- **Verify**: Run on test DB twice; column appears once; existing rows have `priority = 'Medium'`.

### TASK-10 — Run migration against `instance/data.db`
- **Action**: `python scripts/migrate_add_priority.py`
- **Depends on**: TASK-9
- **Verify**: Script prints "Migration complete" or "Migration skipped"; `PRAGMA table_info(task)` shows `priority`.

### TASK-11 — Write unit tests in `tests/unit/test_priority.py`
- **File**: `tests/unit/test_priority.py` (new)
- **Change**: Tests for `PRIORITY_RANK` sort order, `PRIORITY_CHOICES` completeness and consistency.
- **Depends on**: TASK-2
- **Verify**: `pytest tests/unit/test_priority.py` — all tests pass.

### TASK-12 — Write integration tests in `tests/integration/test_priority_migration.py`
- **File**: `tests/integration/test_priority_migration.py` (new)
- **Change**: Tests: column add, backfill, idempotency, new-row default.
- **Depends on**: TASK-9
- **Verify**: `pytest tests/integration/test_priority_migration.py` — all tests pass.

### TASK-13 — Run full test suite
- **Action**: `pytest tests/ -v`
- **Depends on**: TASK-11, TASK-12
- **Verify**: All tests pass, zero regressions.

---

## Dependency Order

```
TASK-1 (models)
  └─ TASK-2 (forms)
       ├─ TASK-3 (routes index sort)
       ├─ TASK-4 (routes add priority)
       ├─ TASK-5 (routes edit priority)
       │    └─ TASK-8 (template edit)
       ├─ TASK-7 (template add)
       └─ TASK-11 (unit tests)
  └─ TASK-9 (migration script)
       └─ TASK-10 (run migration)
       └─ TASK-12 (integration tests)
TASK-3 → TASK-6 (template index badge)
TASK-11 + TASK-12 → TASK-13 (full suite)
```

---

## Completion Criteria

All 13 tasks complete with `pytest tests/ -v` returning 0 failures and all three acceptance criteria (AC-1, AC-2, AC-3) manually or programmatically verifiable.
