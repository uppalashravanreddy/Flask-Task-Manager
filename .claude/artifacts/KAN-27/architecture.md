# Architecture — KAN-27

| Field | Value |
|---|---|
| Ticket ID | KAN-27 |
| Summary | US-21: Assign priority level (High/Medium/Low) to tasks |
| Phase | 2 — Architecture |
| Status | Complete |
| Author | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date | 2026-08-13 |

---

## Overview

The task priority feature adds a `priority` field (constrained to `High`, `Medium`, `Low`) to the existing `Task` model. It is surfaced via a Bootstrap 4 dropdown on both Add and Edit forms, displayed as coloured badges on the task list, and used as the primary sort key on the home page. All changes are confined to existing files; no new routes, no new dependencies, and no new template files are introduced. A one-time, idempotent migration script backfills existing rows with the default value `Medium`.

---

## Component Diagram

```
Browser
  │
  ├─ GET  /           ──► index()         ──► Task.query.all()  ──► sorted(PRIORITY_RANK)
  │                                             └─► index.html   ──► priority badge
  │
  ├─ POST /add        ──► add()           ──► AddTaskForm.priority ──► Task(priority=...)
  │                                             └─► add.html    ──► priority <select>
  │
  └─ POST /edit/<id>  ──► edit()          ──► AddTaskForm.priority ──► task.priority = ...
                                               └─► edit.html   ──► priority <select> (pre-filled)

SQLite (instance/data.db)
  └─ task table
       ├─ id, title, date, desc  (pre-existing)
       └─ priority TEXT NOT NULL DEFAULT 'Medium'  (new column, added by migration)

scripts/migrate_add_priority.py
  └─ ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'Medium'
  └─ UPDATE task SET priority = 'Medium' WHERE priority IS NULL
```

---

## Component Responsibilities

| Component | File | Responsibility |
|---|---|---|
| Data model | `models.py` | Declares `priority` column; enforces `nullable=False, default='Medium'` at ORM level |
| Form definition | `forms.py` | Defines `PRIORITY_CHOICES`, `PRIORITY_RANK`, and `priority` `SelectField` with default `Medium` |
| Route — index | `routes.py` | Sorts all tasks by `PRIORITY_RANK` before passing to template |
| Route — add | `routes.py` | Persists `form.priority.data` on new `Task` creation |
| Route — edit | `routes.py` | Pre-populates `form.priority.data` from existing task; persists updated value on POST |
| Template — index | `templates/index.html` | Renders Bootstrap 4 badge (`badge-danger` / `badge-warning` / `badge-success`) per priority value |
| Template — add | `templates/add.html` | Renders priority `<select>` via WTForms |
| Template — edit | `templates/edit.html` | Renders pre-filled priority `<select>` via WTForms |
| Migration | `scripts/migrate_add_priority.py` | Idempotent SQLite `ALTER TABLE` + `UPDATE` for existing rows |

---

## Data Flow

### Add Task (POST /add)
1. User selects priority in `<select>` (defaults to `Medium` if untouched).
2. `AddTaskForm.validate_on_submit()` validates; `form.priority.data` contains chosen value.
3. `Task(priority=form.priority.data)` is persisted to SQLite.
4. Redirect to `/index`; task appears sorted by `PRIORITY_RANK`.

### Edit Task (POST /edit/<id>)
1. GET: `form.priority.data = task.priority` pre-fills the select widget.
2. User may change the value; POST carries the new selection.
3. `task.priority = form.priority.data` updated; `db.session.commit()`.
4. Redirect to `/index`; badge and position reflect updated priority.

### Home Page (GET /)
1. `Task.query.all()` retrieves all tasks.
2. `sorted(..., key=lambda t: PRIORITY_RANK.get(t.priority, 2))` orders: High (1) → Medium (2) → Low (3).
3. Jinja2 template conditionally assigns `badge-danger` / `badge-warning` / `badge-success`.

### Migration (one-time, idempotent)
1. `PRAGMA table_info(task)` checks if `priority` column already exists.
2. If absent: `ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'Medium'` + `UPDATE`.
3. If present: no-op; safe to re-run.

---

## Technology Choices

| Choice | Technology | Rationale |
|---|---|---|
| Form field | WTForms `SelectField` | Already in use; enforces value-set constraint at form-validation layer |
| Badge colours | Bootstrap 4 contextual classes | Already loaded via CDN; zero new CSS |
| Sorting | Python built-in `sorted()` | Stable, predictable; avoids SQL `ORDER BY` complexity with SQLite |
| Default value | SQLAlchemy `default='Medium'` + `nullable=False` | Enforced at ORM and DB levels |
| Migration | Raw `sqlite3` + `PRAGMA table_info` | SQLAlchemy-Migrate / Alembic not in project; lightweight approach consistent with project size |

---

## Files Changed

| File | Action | Reason |
|---|---|---|
| `models.py` | Modified | Add `priority` column with `nullable=False, default='Medium'` |
| `forms.py` | Modified | Add `PRIORITY_CHOICES`, `PRIORITY_RANK`, and `priority` `SelectField` |
| `routes.py` | Modified | Sort by `PRIORITY_RANK` in `index()`; persist/pre-fill priority in `add()` / `edit()` |
| `templates/index.html` | Modified | Render priority badge next to task title |
| `templates/add.html` | Modified | Render priority `<select>` field |
| `templates/edit.html` | Modified | Render pre-filled priority `<select>` field |
| `scripts/migrate_add_priority.py` | Created | Idempotent migration for existing databases |
| `tests/unit/test_priority.py` | Created | Unit tests for `PRIORITY_RANK` sort logic and `PRIORITY_CHOICES` contract |
| `tests/integration/test_priority_migration.py` | Created | Integration tests for migration script (add column, backfill, idempotency, default) |

---

## Migration Requirements

- **Required**: Run `python scripts/migrate_add_priority.py` against `instance/data.db` before starting the application if upgrading from a pre-priority schema.
- **Safe to re-run**: The script checks for column existence before altering; no data loss on repeated execution.
- **New installs**: SQLAlchemy `db.create_all()` creates the column automatically from the model definition.

---

## Out of Scope

- Filter/search by priority.
- API endpoints for priority.
- Alembic or Flask-Migrate integration.
- Client-side reordering or drag-and-drop.
- Priority change history or audit log.
