# Test Strategy — KAN-27

| Field | Value |
|---|---|
| Ticket ID | KAN-27 |
| Summary | US-21: Assign priority level (High/Medium/Low) to tasks |
| Phase | 7.1 — Test Strategy |
| Status | Complete |
| Author | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date | 2026-08-13 |

---

## Objectives

1. Verify that all three acceptance criteria (AC-1, AC-2, AC-3) are met by the implementation.
2. Confirm the migration script handles all database states (fresh install, upgrade, re-run).
3. Ensure no regression is introduced in existing task CRUD flows.

---

## Test Levels

| Level | Tool | Scope | Rationale |
|---|---|---|---|
| Unit | pytest | `PRIORITY_RANK` sort logic, `PRIORITY_CHOICES` contract, form field definition | Fast, isolated, no DB or Flask context needed |
| Integration | pytest + sqlite3 | Migration script (column add, backfill, idempotency, new-row default) | Validates DB schema change in isolation from Flask app |
| E2E | pytest-playwright (Chromium) | Full browser flows: add task, view badges, edit priority, delete | Validates AC-1, AC-2, AC-3 at the user-visible layer |

---

## Risks Covered

| Risk | Test Level | Test Case(s) |
|---|---|---|
| Priority not saved with correct default on submit | Unit + E2E | `test_priority_choices_contain_all_three_values`, E2E add flow |
| Sort order wrong after add/edit | Unit | `test_priority_rank_high_sorts_first`, `test_priority_rank_medium_sorts_between_high_and_low` |
| Migration corrupts existing data | Integration | `test_migration_backfills_existing_rows_with_medium`, `test_migration_is_idempotent` |
| Edit form doesn't pre-fill priority | E2E | `test_edit_task_form_loads` |
| Regression in add/delete flows | E2E | `test_add_task_creates_and_redirects`, `test_delete_task_removes_from_list` |

---

## Out of Scope

- Performance/load testing.
- Cross-browser testing beyond Chromium (no multi-browser requirement defined).
- API-level testing (no REST API for priority).
- Accessibility (WCAG) testing.

---

## Test Environment

| Item | Value |
|---|---|
| Python | 3.14.6 |
| pytest | 9.1.1 |
| pytest-playwright | 0.9.0 |
| Browser | Chromium (headless) |
| Database | SQLite (`instance/data.db`) |
| Flask env | Testing (in-memory for unit; live server on port 5000 for E2E) |

---

## Entry Criteria

- Phase 5 (implementation) complete with all 13 tasks verified.
- Phase 6 (code review) approved.
- `pytest tests/unit/ tests/integration/` passes with 0 failures.

## Exit Criteria

- All unit and integration tests pass.
- E2E tests: AC-1, AC-2, AC-3 scenarios executed; any skips documented with reason.
- No regression in existing test suite.
- Test results published in HTML report.
