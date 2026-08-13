# Architecture — FLASK-002: Task Priority

| Field     | Value                                    |
|-----------|------------------------------------------|
| Ticket ID | FLASK-002                                |
| Phase     | 2 — Architecture                         |
| Status    | Complete                                 |
| Author    | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date      | 2026-08-13                               |

---

## 1. Overview

FLASK-002 adds a `priority` field (High / Medium / Low) to the existing `Task` model. The feature touches four layers of the application: the database schema, the data model, the form layer, and the HTML templates. No new routes are introduced; existing routes are extended. No new dependencies are required.

---

## 2. Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     User Browser                        │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP (GET / POST)
┌──────────────────────▼──────────────────────────────────┐
│                  Flask Application                      │
│                                                         │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐  │
│  │  routes.py  │   │   forms.py   │   │  models.py  │  │
│  │             │   │              │   │             │  │
│  │ index()  ◄──┼───┤              │   │ Task        │  │
│  │  sort by    │   │ AddTaskForm  │   │  id         │  │
│  │  priority   │   │  title       │   │  title      │  │
│  │             │   │  desc        │   │  date       │  │
│  │ add()    ◄──┼───┤  priority ★  │   │  desc       │  │
│  │  write      │   │  (SelectField│   │  priority ★ │  │
│  │  priority   │   │   default:   │   │  (default:  │  │
│  │             │   │   Medium)    │   │   Medium)   │  │
│  │ edit()   ◄──┼───┤              │   │             │  │
│  │  read +     │   └──────────────┘   └──────┬──────┘  │
│  │  write      │                             │ ORM      │
│  │  priority   │                             │          │
│  └─────────────┘                             │          │
│                                              │          │
│  ┌───────────────────────────────────────┐   │          │
│  │            templates/                 │   │          │
│  │  index.html — badge per task ★        │   │          │
│  │  add.html   — priority dropdown ★     │   │          │
│  │  edit.html  — priority dropdown ★     │   │          │
│  └───────────────────────────────────────┘   │          │
└──────────────────────────────────────────────┼──────────┘
                                               │ SQLAlchemy
┌──────────────────────────────────────────────▼──────────┐
│              SQLite  (instance/data.db)                 │
│                                                         │
│  task table                                             │
│    id       INTEGER PRIMARY KEY                         │
│    title    TEXT NOT NULL UNIQUE                        │
│    date     DATE NOT NULL                               │
│    desc     TEXT NOT NULL                               │
│    priority TEXT DEFAULT 'Medium'  ★ new column         │
└─────────────────────────────────────────────────────────┘

★ = new or modified by FLASK-002
```

---

## 3. Component Responsibilities

### 3.1 models.py — Task model
- **Change:** Add `priority = db.Column(db.String(10), nullable=False, default='Medium')`.
- **Responsibility:** Persist and expose the priority value for each task. The `default` ensures new tasks created programmatically (e.g. in tests) receive `Medium` without explicit assignment.

### 3.2 forms.py — AddTaskForm
- **Change:** Add `priority = SelectField(...)` with choices `[High, Medium, Low]` and default `Medium`.
- **Responsibility:** Validate and expose priority input from both the Add and Edit pages. `AddTaskForm` is reused for editing (existing pattern in the codebase) so no new form class is needed.

### 3.3 routes.py — index(), add(), edit()
| Route | Change |
|-------|--------|
| `index()` | Replace `Task.query.all()` with a priority-sorted query using a Python-level sort keyed on `PRIORITY_RANK = {'High': 1, 'Medium': 2, 'Low': 3}`. |
| `add()` | Pass `priority=form.priority.data` when constructing the `Task` object. |
| `edit()` | Read `task.priority` into `form.priority.data` on GET; write `form.priority.data` back to `task.priority` on POST. |

**Sort implementation** (server-side, no JS):
```python
PRIORITY_RANK = {'High': 1, 'Medium': 2, 'Low': 3}
tasks = sorted(Task.query.all(), key=lambda t: PRIORITY_RANK.get(t.priority, 2))
```

### 3.4 templates/index.html
- **Change:** Add a Bootstrap badge inside each task card, rendered via a Jinja2 conditional:
```html
{% if task.priority == 'High' %}
  <span class="badge badge-danger">High</span>
{% elif task.priority == 'Low' %}
  <span class="badge badge-success">Low</span>
{% else %}
  <span class="badge badge-warning">Medium</span>
{% endif %}
```

### 3.5 templates/add.html and edit.html
- **Change:** Render the `priority` SelectField using `{{ form.priority.label }}` and `{{ form.priority() }}`.
- `edit.html` pre-selects the current task priority by setting `form.priority.data = task.priority` in the route before rendering.

### 3.6 Database Migration
- **Approach:** A standalone migration script `scripts/migrate_add_priority.py` that issues a single `ALTER TABLE` via the `sqlite3` standard library.
- **Script logic:**
  1. Connect to `instance/data.db`.
  2. Check if column `priority` already exists (idempotent guard).
  3. If absent, execute `ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'Medium'`.
  4. Execute `UPDATE task SET priority = 'Medium' WHERE priority IS NULL` to backfill any pre-existing rows that hold NULL (rows inserted before the migration ran).
  5. Commit and close.
- **Result:** All existing rows receive `priority = 'Medium'` — new rows via the SQL column default, pre-existing NULL rows via the explicit UPDATE backfill.

---

## 4. Data Flow

### Add Task (POST /add)
```
User submits form
  → AddTaskForm validates (title required, desc required, priority defaults to Medium)
  → routes.add() constructs Task(title, date, desc, priority)
  → db.session.add() + commit()
  → redirect to index
  → index() queries all tasks, sorts by PRIORITY_RANK
  → index.html renders badge for each task
```

### Edit Task (POST /edit/<id>)
```
User opens edit form (GET)
  → routes.edit() loads task from DB
  → sets form.priority.data = task.priority  (pre-selects current value)
  → edit.html renders dropdown with current value selected

User submits form (POST)
  → AddTaskForm validates
  → task.priority = form.priority.data
  → db.session.commit()
  → redirect to index
```

---

## 5. Technology Choices

| Decision | Choice | Reason |
|----------|--------|--------|
| Priority storage type | `String(10)` column | SQLite has no native ENUM; String is sufficient for 3 fixed values |
| Sort mechanism | Python-level sort in `index()` | Avoids SQL CASE complexity; task list is small, performance impact negligible |
| Form field type | `wtforms.SelectField` | Already in the WTForms dependency; no new library needed |
| Migration tool | Custom `sqlite3` script | Flask-Migrate is not in the current stack; a one-off ALTER TABLE is simpler and safer |
| Badge styling | Bootstrap 4 badge classes | Bootstrap 4.5 already loaded in `base.html`; no new CSS dependency |

---

## 6. Files Changed

| File | Type | Change |
|------|------|--------|
| `models.py` | Modified | Add `priority` column |
| `forms.py` | Modified | Add `SelectField` for priority |
| `routes.py` | Modified | Sort in `index()`, pass priority in `add()`, read/write in `edit()` |
| `templates/index.html` | Modified | Render priority badge per task |
| `templates/add.html` | Modified | Render priority dropdown |
| `templates/edit.html` | Modified | Render priority dropdown (pre-selected) |
| `scripts/migrate_add_priority.py` | New | One-off migration script |
| `tests/unit/test_priority.py` | New | Unit tests for priority behaviour |
| `tests/integration/test_priority_routes.py` | New | Integration tests for add/edit/index routes |

---

## 7. Out of Scope (Architecture)

- No new routes added.
- No changes to `delete.html` or the delete route.
- No JavaScript introduced.
- No changes to `app.py` configuration.
- No Confluence or documentation pipeline changes.
