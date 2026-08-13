# Requirements — FLASK-002: Task Priority

| Field        | Value                                       |
|--------------|---------------------------------------------|
| Ticket ID    | FLASK-002                                   |
| Phase        | 1 — Requirements                            |
| Status       | Complete                                    |
| Author       | SDLC Pipeline (Claude Code — Sonnet 4.6)    |
| Date         | 2026-08-13                                  |

---

## 1. User Story

As a user of the Flask Task Manager, I want to assign a priority level (High, Medium, or Low) to each task, so that I can visually identify and focus on the most important work first.

---

## 2. Functional Requirements

| ID   | Requirement                                                                                                                                                   | Priority     |
|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| FR-1 | The system shall provide a `priority` field on the Add Task form, presented as a dropdown with options: High, Medium, Low.                                    | Must Have    |
| FR-2 | The `priority` field shall be optional. If not selected by the user, the system shall default the value to `Medium`.                                          | Must Have    |
| FR-3 | The system shall display a colour-coded badge alongside each task on the task list: High = red, Medium = orange, Low = green.                                 | Must Have    |
| FR-4 | The task list shall be sorted by priority in descending order of urgency (High first, then Medium, then Low) by default on page load.                         | Must Have    |
| FR-5 | The `priority` field shall be editable via the Edit Task form, using the same dropdown options as the Add Task form.                                          | Must Have    |
| FR-6 | All existing tasks already stored in the database at the time of migration shall be assigned a default priority of `Medium` automatically.                    | Must Have    |
| FR-7 | Priority filtering (e.g. show only High priority tasks) is explicitly out of scope for this sprint and shall not be implemented.                              | Out of Scope |

---

## 3. Non-Functional Requirements

| ID    | Requirement                                                                                                                                       | Metric                                                                 |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| NFR-1 | The priority badge shall be visually distinct and accessible — colour alone shall not be the only differentiator; the text label must also appear. | Badge renders text (High / Medium / Low) alongside the colour.         |
| NFR-2 | The database migration adding the `priority` column shall not destroy or alter any existing task data.                                             | All pre-existing tasks remain intact after migration with priority=Medium. |
| NFR-3 | The priority sort shall be applied server-side in the route query, not via client-side JavaScript.                                                 | Task list order is correct even with JavaScript disabled.              |
| NFR-4 | The `SECRET_KEY` for the Flask application shall continue to be read exclusively from the OS environment; no secrets introduced by this feature.   | Static review confirms no hardcoded secrets in any new or modified file. |

---

## 4. Constraints

- The existing Flask + SQLAlchemy + SQLite stack must be used; no new ORM or database engine is permitted.
- Priority values are restricted to the enumerated set: `High`, `Medium`, `Low`. Free-text priority input is not supported.
- No JavaScript framework may be introduced for sorting or display; server-side rendering only.
- The feature must be backward-compatible: the application must start and function correctly even if the migration has not yet been applied (graceful degradation via column default).

---

## 5. Acceptance Criteria

| ID   | Criteria                                                                                                                                  | Testable? |
|------|-------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| AC-1 | A user can create a new task without selecting a priority; the saved task displays a Medium badge on the task list.                       | Yes       |
| AC-2 | A user can create a new task and select High priority; the saved task displays a red High badge on the task list.                         | Yes       |
| AC-3 | The task list displays tasks sorted High → Medium → Low by default on page load.                                                          | Yes       |
| AC-4 | A user can edit an existing task and change its priority; the updated badge reflects the new value immediately after save.                | Yes       |
| AC-5 | All tasks existing before the migration are displayed with a Medium badge after the migration is applied.                                 | Yes       |
| AC-6 | Priority badges display the text label (High / Medium / Low) alongside the colour — not colour alone.                                    | Yes       |
| AC-7 | No filter UI element is present on the task list page.                                                                                    | Yes       |

---

## 6. Out of Scope

- Priority filtering or search by priority level.
- Priority-based notifications or alerts.
- More than three priority levels (e.g. Critical, Blocker).
- Inline priority editing directly on the task list (without opening the Edit form).
- Any changes to the Delete Task flow or the known `/delete=/<id>` URL quirk.

---

## 7. Assumptions

- The developer has Python 3.11+ and the project virtual environment active before running migrations or tests.
- SQLite supports the `ALTER TABLE` statement used to add the `priority` column via Flask-Migrate or a direct migration script.
- The Bootstrap CSS already included in `base.html` is sufficient to render coloured badge classes (`badge bg-danger`, `badge bg-warning`, `badge bg-success`) without adding new dependencies.
- The product team accepts `Medium` as the default priority for all pre-existing tasks; no manual backfill review is required.
- A single `priority` column of type `String` with a server-level default of `"Medium"` is sufficient; an SQL `ENUM` type is not required given SQLite constraints.
