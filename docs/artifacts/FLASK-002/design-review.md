# Design Review — FLASK-002: Task Priority

| Field     | Value                                    |
|-----------|------------------------------------------|
| Ticket ID | FLASK-002                                |
| Phase     | 3 — Design Review                        |
| Status    | Complete                                 |
| Author    | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date      | 2026-08-13                               |

---

## 1. Review Summary

Architecture reviewed against `requirements.md` and the existing codebase. Four issues found: one correctness bug (Bootstrap version mismatch), one reliability gap (NULL backfill), one maintainability concern (PRIORITY_RANK placement), and one pre-existing security observation. All have agreed resolutions documented below.

---

## 2. Findings

### RISK-1 — Bootstrap Badge Class Mismatch (Correctness — High)

**Finding:** The architecture doc specifies `badge bg-danger`, `badge bg-warning`, `badge bg-success` — these are Bootstrap **5** classes. The application loads Bootstrap **4.5.0** from the CDN in `base.html`. Bootstrap 4 badge classes are `badge badge-danger`, `badge badge-warning`, `badge badge-success`. Using Bootstrap 5 classes against a Bootstrap 4 stylesheet will render plain unstyled text — no colour, no badge appearance.

**Resolution:** Use Bootstrap 4 badge syntax in all templates:
- High → `<span class="badge badge-danger">High</span>`
- Medium → `<span class="badge badge-warning">Medium</span>`
- Low → `<span class="badge badge-success">Low</span>`

**Status:** Corrected before implementation.

---

### RISK-2 — Migration Does Not Backfill Existing NULLs (Reliability — Medium)

**Finding:** `ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'Medium'` sets the SQL column default for new inserts but does **not** update rows that were inserted before the migration and currently hold `NULL` in the priority column (possible if the app ran before migration). The architecture mentions an idempotent guard but does not mention a backfill `UPDATE` statement.

**Resolution:** Add a follow-up `UPDATE` in the migration script:
```sql
UPDATE task SET priority = 'Medium' WHERE priority IS NULL;
```
This ensures all pre-existing rows are explicitly set to `'Medium'`, satisfying AC-5.

**Status:** Added to implementation.

---

### RISK-3 — PRIORITY_RANK Dict Defined Inline in routes.py (Maintainability — Low)

**Finding:** Defining `PRIORITY_RANK = {'High': 1, 'Medium': 2, 'Low': 3}` inside `routes.py` makes it untestable in isolation and couples sort logic to the route layer. If priority values or sort order change, both `forms.py` choices and `routes.py` sort key must be updated in two places.

**Resolution:** Define `PRIORITY_RANK` as a module-level constant in `forms.py` alongside the `SelectField` choices. `routes.py` imports it from `forms`. Both choices and rank stay co-located.

**Status:** Incorporated into implementation.

---

### OBS-1 — SECRET_KEY Has Hardcoded Fallback (Security — Observation)

**Finding:** `app.py` line 8: `os.environ.get('SECRET_KEY', 'dev-only-change-in-production')` — the fallback string is a hardcoded value. NFR-4 states the SECRET_KEY must be read exclusively from the OS environment. This is a pre-existing issue, not introduced by FLASK-002.

**Resolution:** Out of scope for FLASK-002. Logged as a separate finding. FLASK-002 introduces no new secrets or hardcoded values.

**Status:** Noted, not actioned in this ticket.

---

## 3. Architecture Sign-Off

| Area | Decision |
|------|----------|
| Model change | Approved — single nullable=False String column with default 'Medium' |
| Form change | Approved — SelectField added to existing AddTaskForm, reused for edit |
| Sort mechanism | Approved — Python-level sort with PRIORITY_RANK dict |
| Migration approach | Approved with amendment — ALTER TABLE + UPDATE backfill |
| Badge styling | Corrected — Bootstrap 4 syntax only |
| Test plan | Approved — unit tests for sort logic, integration test for migration |

No architecture changes required beyond the amendments above. Implementation may proceed.
