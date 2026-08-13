# Implementation Plan — FLASK-002: Task Priority

| Field     | Value                                    |
|-----------|------------------------------------------|
| Ticket ID | FLASK-002                                |
| Phase     | 4 — Implementation Planning              |
| Status    | Complete                                 |
| Author    | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date      | 2026-08-13                               |

---

## 1. Dependency-Ordered Task List

Tasks are ordered so that each task's dependencies are complete before it starts.

| # | Task | File(s) | Depends On | Blocked Until |
|---|------|---------|------------|---------------|
| T1 | Add `PRIORITY_RANK` constant and `SelectField` to `forms.py` | `forms.py` | — | Ready |
| T2 | Add `priority` column to `Task` model | `models.py` | T1 | T1 done |
| T3 | Write migration script | `scripts/migrate_add_priority.py` | T2 | T2 done |
| T4 | Update `routes.py` — sort index, pass priority in add, read/write in edit | `routes.py` | T1, T2 | T1 + T2 done |
| T5 | Update `templates/index.html` — add priority badge | `templates/index.html` | T2 | T2 done |
| T6 | Update `templates/add.html` — add priority dropdown | `templates/add.html` | T1 | T1 done |
| T7 | Update `templates/edit.html` — add priority dropdown (pre-selected) | `templates/edit.html` | T1, T4 | T1 + T4 done |
| T8 | Run migration script against local database | `instance/data.db` | T3 | T3 done |
| T9 | Write unit tests for priority sort logic | `tests/unit/test_priority.py` | T1, T2 | T1 + T2 done |
| T10 | Write integration test for migration script | `tests/integration/test_priority_migration.py` | T3 | T3 done |
| T11 | Run full test suite and verify all pass | — | T8, T9, T10 | All above done |

---

## 2. Task Detail

### T1 — forms.py
- Import `SelectField` from `wtforms`.
- Define `PRIORITY_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]`.
- Define `PRIORITY_RANK = {'High': 1, 'Medium': 2, 'Low': 3}` as a module-level constant.
- Add `priority = SelectField('Priority', choices=PRIORITY_CHOICES, default='Medium')` to `AddTaskForm`.

### T2 — models.py
- Add `priority = db.Column(db.String(10), nullable=False, default='Medium')` to `Task`.

### T3 — scripts/migrate_add_priority.py (new file)
- Connect to `instance/data.db`.
- Read `PRAGMA table_info(task)` to check if `priority` column exists.
- If absent: `ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'Medium'`.
- Follow up: `UPDATE task SET priority = 'Medium' WHERE priority IS NULL`.
- Commit and print result.

### T4 — routes.py
- Import `PRIORITY_RANK` from `forms`.
- `index()`: replace `Task.query.all()` with `sorted(Task.query.all(), key=lambda t: PRIORITY_RANK.get(t.priority, 2))`.
- `add()`: add `priority=form.priority.data` to `Task(...)` constructor.
- `edit()` GET: add `form.priority.data = task.priority`.
- `edit()` POST: add `task.priority = form.priority.data`.

### T5 — templates/index.html
- Inside the task card `<h3>`, add a Jinja2 conditional rendering Bootstrap 4 badges:
  - High → `badge badge-danger`
  - Medium → `badge badge-warning`
  - Low → `badge badge-success`

### T6 — templates/add.html
- Add a `<div class="row">` block with `<h3>Priority</h3>` and `{{ form.priority(class="form-control") }}`.

### T7 — templates/edit.html
- Add the same priority row as add.html. Pre-selection is handled server-side via `form.priority.data = task.priority` in the route.

### T8 — Run migration
```bash
python scripts/migrate_add_priority.py
```

### T9 — tests/unit/test_priority.py (new file)
- `test_priority_rank_high_sorts_first` — High before Medium before Low.
- `test_unknown_priority_defaults_to_medium_position` — unknown value sorts at position 2.
- `test_priority_choices_contain_all_three_values` — High, Medium, Low all present.
- `test_default_priority_value_is_medium` — default is 'Medium'.

### T10 — tests/integration/test_priority_migration.py (new file)
- Creates a temp SQLite DB with a `task` table (no priority column).
- Runs migration logic against it.
- Asserts `priority` column exists after migration.
- Asserts existing rows have `priority = 'Medium'`.
- Runs migration a second time — asserts it completes without error (idempotency).

### T11 — Full test run
```bash
pytest tests/unit/ tests/integration/ -v
```
All tests must pass before Phase 6.

---

## 3. Blocked Tasks

| Task | Blocked By | Reason |
|------|------------|--------|
| T4 | T1, T2 | Routes import PRIORITY_RANK from forms and write to Task.priority |
| T7 | T1, T4 | Template depends on form field existing and route pre-populating it |
| T8 | T3 | Cannot run migration until script exists |
| T11 | T8, T9, T10 | Test run is the final verification gate |

---

## 4. Files Inventory

| File | Action |
|------|--------|
| `forms.py` | Modify |
| `models.py` | Modify |
| `routes.py` | Modify |
| `templates/index.html` | Modify |
| `templates/add.html` | Modify |
| `templates/edit.html` | Modify |
| `scripts/migrate_add_priority.py` | Create |
| `tests/unit/test_priority.py` | Create |
| `tests/integration/test_priority_migration.py` | Create |
