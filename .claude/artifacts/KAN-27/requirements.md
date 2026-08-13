# Requirements — KAN-27

| Field | Value |
|---|---|
| Ticket ID | KAN-27 |
| Summary | US-21: Assign priority level (High/Medium/Low) to tasks |
| Phase | 1 — Requirements |
| Status | Complete |
| Author | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date | 2026-08-13 |

---

## User Story

> As a user of the Flask Task Manager, I want to assign a priority level (High, Medium, or Low) to each task, so that I can visually identify and focus on the most important work first.

---

## Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-1 | The system shall store a `priority` field on every task, constrained to the values `High`, `Medium`, or `Low`. | Must |
| FR-2 | When a task is created without an explicit priority selection, the system shall default the priority to `Medium`. | Must |
| FR-3 | The task creation form shall present a dropdown/select field with three choices: `High`, `Medium`, `Low`; `Medium` shall be pre-selected. | Must |
| FR-4 | The task list (home page) shall display a coloured badge alongside each task title to indicate its priority level: red for `High`, yellow/amber for `Medium`, green for `Low`. | Must |
| FR-5 | The task list shall be sorted by priority in descending importance order: `High` first, then `Medium`, then `Low`. | Must |
| FR-6 | The task edit form shall pre-populate the priority field with the task's current priority value and allow the user to change it. | Must |
| FR-7 | After editing a task's priority, the badge on the task card and its position in the sorted list shall reflect the updated priority immediately upon save. | Must |
| FR-8 | The task edit form shall use the same dropdown with the same three choices as the creation form. | Should |

---

## Non-Functional Requirements

| ID | Requirement | Metric |
|---|---|---|
| NFR-1 | Badge colours shall conform to Bootstrap contextual classes (danger, warning, success) for accessibility and visual consistency. | All three badges use standard Bootstrap 4 contextual classes |
| NFR-2 | Priority sorting shall be deterministic — tasks of equal priority shall maintain stable relative order. | Python `sorted()` stable sort guarantees this |
| NFR-3 | The `priority` column default shall be enforced at the database level via a `NOT NULL DEFAULT 'Medium'` constraint so existing rows without a value receive `Medium`. | Migration script sets `nullable=False, default='Medium'` via SQLAlchemy |
| NFR-4 | No additional page loads or AJAX calls shall be required beyond the existing add/edit POST–redirect–GET cycle. | Zero new HTTP round-trips for priority display |

---

## Constraints

- Backend: Flask + SQLAlchemy (SQLite via `instance/data.db`).
- Frontend: Bootstrap 4 (badge classes available: `badge-danger`, `badge-warning`, `badge-success`).
- Priority values are restricted to the exact strings `High`, `Medium`, `Low` — no free-text input.
- Sorting is server-side only; no client-side JavaScript sorting.
- Migration must be non-destructive for existing tasks (set `Medium` as default for any row where `priority` is NULL).

---

## Acceptance Criteria

| ID | Given / When / Then | Testable? |
|---|---|---|
| AC-1 | **Default on submit:** Given I am on the Add Task page, When I submit without selecting a priority, Then the task is saved with `Medium` and a yellow badge is displayed. | Yes |
| AC-2 | **High badge and sort:** Given I select `High` priority, When the task is saved, Then a red `High` badge is shown and the task appears at the top of the sorted list above any `Medium` or `Low` tasks. | Yes |
| AC-3 | **Edit updates badge and sort:** Given I edit an existing task and change its priority, When I save the edit, Then the badge on the task card updates to the new priority colour and the task re-sorts to the correct position in the home page list. | Yes |

---

## Out of Scope

- Priority-based filtering or searching.
- Custom priority labels beyond the three fixed values.
- Priority-based notifications or reminders.
- Drag-and-drop reordering of tasks.
- Per-user priority preferences.
- API endpoints for priority — UI-only for this story.

---

## Assumptions

- The Bootstrap 4 CDN is already included in `base.html`; no additional CSS libraries are needed.
- A database migration script (`scripts/migrate_add_priority.py`) will handle the schema change for any pre-existing tasks.
- The `AddTaskForm` is reused for both add and edit flows; a separate `EditTaskForm` is not required.
- `date` field is set automatically server-side (`datetime.utcnow()`); it is not a priority-related concern.
- All existing tests must continue to pass after the priority feature is added.
