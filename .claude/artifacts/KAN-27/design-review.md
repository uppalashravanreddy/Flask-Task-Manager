# Design Review — KAN-27

| Field | Value |
|---|---|
| Ticket ID | KAN-27 |
| Summary | US-21: Assign priority level (High/Medium/Low) to tasks |
| Phase | 3 — Design Review |
| Status | APPROVED |
| Reviewer | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date | 2026-08-13 |

---

## Review Summary

The architecture is minimal, well-contained, and directly implements the three acceptance criteria with no unnecessary complexity. All changes are in existing files; no new dependencies are introduced. The migration approach is appropriate for a single-developer SQLite-based project.

**Verdict: APPROVED — no blocking risks. Proceed to Phase 4.**

---

## Risk Assessment

| ID | Risk | Severity | Mitigation | Status |
|---|---|---|---|---|
| R-1 | Existing database rows have no `priority` value after schema change | LOW | Migration script sets `DEFAULT 'Medium'` and backfills `NULL` rows; idempotent and safe to re-run | Mitigated |
| R-2 | `SelectField` doesn't prevent out-of-set values at the HTTP layer (crafted POST with `priority=Critical`) | LOW | WTForms `SelectField` rejects values not in `choices` and fails validation; route only persists on `validate_on_submit()` | Mitigated |
| R-3 | `sorted()` on `Task.query.all()` loads all tasks into memory for sorting | LOW | Application is single-user, task count expected to remain small; no pagination requirement defined | Accepted |
| R-4 | `PRIORITY_RANK.get(t.priority, 2)` silent default for unknown values sorts them as `Medium` | LOW | All entry points enforce the three-value set; unknown values can only arise from direct DB manipulation, not UI | Accepted |
| R-5 | Bootstrap badge classes (`badge-danger`, etc.) depend on Bootstrap 4 being loaded | LOW | Bootstrap 4.5 CDN already in `base.html`; no version change needed | Mitigated |

No HIGH-severity risks identified. Phase 2 architecture does not need revision.

---

## Architecture Checklist

| Check | Result | Notes |
|---|---|---|
| Minimal change footprint | ✅ Pass | Only existing files modified; one new migration script and two test files added |
| No new external dependencies | ✅ Pass | No new pip packages; no new CDN links |
| Database migration handled | ✅ Pass | `scripts/migrate_add_priority.py` is idempotent and handles backfill |
| Bootstrap version constraint respected | ✅ Pass | Uses `badge-*` classes present in Bootstrap 4.5 |
| Form validation enforces value set | ✅ Pass | WTForms `SelectField` validates against `PRIORITY_CHOICES` |
| Sort is stable and deterministic | ✅ Pass | Python `sorted()` is stable by spec; rank values are unique integers |
| All ACs covered by architecture | ✅ Pass | AC-1 (default Medium), AC-2 (red badge + top sort), AC-3 (edit re-sorts) all addressed |
| Tests planned at unit + integration level | ✅ Pass | Unit tests for `PRIORITY_RANK`/`PRIORITY_CHOICES`; integration tests for migration |
| `.env` not affected | ✅ Pass | No new secrets or environment variables required |

---

## Design Decisions Confirmed

1. **Reuse `AddTaskForm` for edit**: No separate `EditTaskForm` needed — the same form pre-populates via `form.priority.data = task.priority`. This is consistent with the existing pattern for `title` and `desc`.

2. **Server-side sort over SQL `ORDER BY`**: Given project size constraints and the desire to avoid raw SQL in routes, Python `sorted()` is appropriate. If the task list grows beyond a few hundred items, switching to a SQL `ORDER BY CASE` would be the correct next step.

3. **Migration as a standalone script**: Flask-Migrate/Alembic is not in the project stack. A standalone `sqlite3` script is consistent with `scripts/jira_fetch.py` and other project scripts.

---

## Sign-off

Design review complete. No phase return required.

**Next phase: Phase 4 — Implementation Planning**
