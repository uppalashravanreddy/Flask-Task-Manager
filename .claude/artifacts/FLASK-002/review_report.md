# Code Review Report — FLASK-002: Task Priority

| Field     | Value                                    |
|-----------|------------------------------------------|
| Ticket ID | FLASK-002                                |
| Phase     | 6 — Code Review                          |
| Status    | Complete                                 |
| Author    | SDLC Pipeline (Claude Code — Sonnet 4.6) |
| Date      | 2026-08-13                               |

---

## 1. Review Checklist

| Area | Question | Finding | Verdict |
|------|----------|---------|---------|
| Correctness | Does each component behave as specified in requirements.md? | All 7 FRs implemented and traceable. Sort is server-side (NFR-3 ✓). Badges show text + colour (NFR-1 ✓). | PASS |
| Security | Are secrets excluded? Is user input validated? | No new secrets introduced. `SelectField` with explicit `choices` rejects any value not in `[High, Medium, Low]` at WTForms validation layer. OBS-1 (pre-existing fallback SECRET_KEY) is out of scope. | PASS |
| Error Handling | Are API failures, missing files, and empty states handled? | Migration script has idempotent guard (column-exists check). `PRIORITY_RANK.get(t.priority, 2)` defaults unknown values gracefully. Empty task list renders an empty loop — no crash. | PASS |
| Test Coverage | Happy path AND edge cases covered? | 6 unit tests cover sort order, unknown priority fallback, choices consistency, and count. 4 integration tests cover migration add, backfill, idempotency, and post-migration inserts. | PASS |
| Code Clarity | Self-explanatory names, easy to follow? | `PRIORITY_RANK`, `PRIORITY_CHOICES`, `migrate()` are all self-descriptive. No logic requires comments. | PASS |
| DRY Principle | Any duplicated logic? | `PRIORITY_RANK` and `PRIORITY_CHOICES` are defined once in `forms.py` and imported into `routes.py`. Badge Jinja2 block is small enough (3 branches) that extraction to a macro would add indirection without value. | PASS |
| Dependency Safety | Known-vulnerable packages? | No new dependencies added. Existing `flask>=3.0.0`, `flask-sqlalchemy>=3.0.0`, `flask-wtf>=1.2.0`, `wtforms>=3.1.0` — all modern, no known CVEs flagged. | PASS |

---

## 2. Findings

All checklist areas pass. Two observations noted for awareness:

### OBS-1 — Pre-existing SECRET_KEY Fallback (out of scope)
`app.py:8` contains `os.environ.get('SECRET_KEY', 'dev-only-change-in-production')`. This was flagged in Phase 3 (Design Review) and is a pre-existing issue, not introduced by FLASK-002. Tracked separately.

### OBS-2 — `Task.query.get()` Deprecation Warning
`routes.py` uses `Task.query.get(task_id)` which is deprecated in SQLAlchemy 2.x. This was pre-existing before FLASK-002 and is not introduced by this feature. The recommended replacement is `db.session.get(Task, task_id)`. Out of scope but noted for a future cleanup ticket.

---

## 3. SDLC Feedback Loop

This project follows a **phase-gated feedback model**. The table below defines what triggers a return to each phase:

| If a review finds... | Return to Phase | Action |
|---|---|---|
| A requirement is wrong or missing | Phase 1 — Requirements | Update `requirements.md`, re-approve, cascade changes through Phases 2–5 |
| An architectural decision is invalid | Phase 2/3 — Architecture / Design Review | Update `architecture.md` and `design-review.md`, re-plan implementation |
| A task breakdown is incomplete | Phase 4 — Implementation Planning | Update `impl-plan.md`, re-implement affected tasks |
| A code-level bug or style issue | Phase 5 — Implementation | Fix the code, re-run Phase 6 review and Phase 7 tests |
| Tests fail | Phase 7 — Verification | Root-cause and fix in Phase 5, re-verify |

**For FLASK-002:** Phase 3 (Design Review) caught RISK-1 (Bootstrap version mismatch) and RISK-2 (NULL backfill gap) before any code was written. Both were corrected in Phase 5. No issues were found in Phase 6 that require returning to an earlier phase.

---

## 4. Sign-Off

Code review complete. No blockers. Implementation is approved to proceed to Phase 7 — Verification.
