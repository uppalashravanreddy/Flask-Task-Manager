# Test Cases — KAN-27

| Field | Value |
|---|---|
| Ticket ID | KAN-27 |
| Summary | US-21: Assign priority level (High/Medium/Low) to tasks |
| Phase | 7.3 — Test Cases |
| Status | Complete |
| Author | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date | 2026-08-13 |

---

## Deduplication Notes

All test cases below correspond to existing tests in the codebase. No new test files need to be created — the implementation already includes complete test coverage. All cases were checked against the existing test files to avoid duplication:

- `tests/unit/test_priority.py` — 6 unit test functions (all new, no overlap with doc_sync/extractor tests)
- `tests/integration/test_priority_migration.py` — 4 integration test functions (no overlap with `test_pipeline.py`)
- `tests/e2e/test_app_ui.py` — priority-related E2E tests included in existing UI suite

---

## Unit Test Cases

| TC-ID | File | Function | AC | Input | Expected |
|---|---|---|---|---|---|
| TC-U01 | `tests/unit/test_priority.py` | `test_priority_rank_high_sorts_first` | AC-2 | `[Low, High, Medium]` tasks | Sorted: High, Medium, Low |
| TC-U02 | `tests/unit/test_priority.py` | `test_priority_rank_medium_sorts_between_high_and_low` | AC-2 | `[Low, Medium, High]` tasks | Sorted: High, Medium, Low |
| TC-U03 | `tests/unit/test_priority.py` | `test_unknown_priority_defaults_to_medium_position` | AC-2 | `[Critical, High, Low]` tasks | Sorted: High, Critical (pos 2), Low |
| TC-U04 | `tests/unit/test_priority.py` | `test_priority_choices_contain_all_three_values` | AC-1, AC-2 | `PRIORITY_CHOICES` | Contains High, Medium, Low |
| TC-U05 | `tests/unit/test_priority.py` | `test_priority_choices_has_no_extra_values` | AC-1 | `len(PRIORITY_CHOICES)` | Equals 3 |
| TC-U06 | `tests/unit/test_priority.py` | `test_priority_rank_keys_match_choices` | AC-1, AC-2 | `PRIORITY_RANK` keys vs choice values | Sets equal |

---

## Integration Test Cases

| TC-ID | File | Function | AC | Scenario | Expected |
|---|---|---|---|---|---|
| TC-I01 | `tests/integration/test_priority_migration.py` | `test_migration_adds_priority_column` | AC-1 | Run migrate on schema without priority | Column `priority` present after |
| TC-I02 | `tests/integration/test_priority_migration.py` | `test_migration_backfills_existing_rows_with_medium` | AC-1 | Existing row, run migrate | `priority == 'Medium'` |
| TC-I03 | `tests/integration/test_priority_migration.py` | `test_migration_is_idempotent` | AC-1 | Run migrate twice | Exactly 1 `priority` column |
| TC-I04 | `tests/integration/test_priority_migration.py` | `test_new_rows_after_migration_default_to_medium` | AC-1 | Insert after migrate, no priority given | `priority == 'Medium'` |

---

## E2E Test Cases

| TC-ID | File | Function | AC | Scenario | Expected | Status |
|---|---|---|---|---|---|---|
| TC-E01 | `tests/e2e/test_app_ui.py` | `test_add_task_form_renders` | AC-1 | GET /add | Priority select visible | ✅ Passing |
| TC-E02 | `tests/e2e/test_app_ui.py` | `test_add_task_creates_and_redirects` | AC-1, AC-2 | POST /add with High | Redirect to index, badge shown | ✅ Passing |
| TC-E03 | `tests/e2e/test_app_ui.py` | `test_added_task_appears_in_list` | AC-2 | Add High task; check list | Task at top | ✅ Passing |
| TC-E04 | `tests/e2e/test_app_ui.py` | `test_edit_task_form_loads` | AC-3 | GET /edit/<id> | Priority pre-filled | ✅ Passing |
| TC-E05 | `tests/e2e/test_app_ui.py` | `test_edit_task_saves_changes` | AC-3 | Change priority; POST | Badge + sort updated | ⚠️ Skipped |
| TC-E06 | `tests/e2e/test_app_ui.py` | `test_delete_task_removes_from_list` | Regression | Delete task | List updated | ✅ Passing |

---

## Coverage Matrix

| AC | Unit | Integration | E2E | Overall |
|---|---|---|---|---|
| AC-1 (default Medium) | TC-U04, TC-U05, TC-U06 | TC-I01, TC-I02, TC-I03, TC-I04 | TC-E01, TC-E02 | ✅ Covered |
| AC-2 (High badge + sort) | TC-U01, TC-U02, TC-U03, TC-U04, TC-U06 | — | TC-E02, TC-E03 | ✅ Covered |
| AC-3 (edit updates badge + sort) | TC-U01 (sort logic) | — | TC-E04, TC-E05⚠️ | ⚠️ Partial (E2E-5 skipped) |

**Note**: AC-3 has reduced E2E coverage due to TC-E05 being skipped. Sort logic is verified at unit level; edit pre-fill is verified by TC-E04.
