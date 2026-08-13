# Coding Standards

## Python
- Follow PEP 8. Max line length 100.
- No type annotations required — project is Python 3.8 compatible.
- Shared constants go in `forms.py` and are imported by `routes.py`.
- SQLAlchemy models: every column must have an explicit `nullable` setting and a sensible `default`.
- No comments that describe WHAT the code does. Only add a comment if the WHY is non-obvious.

## Flask patterns
- All routes in `routes.py` — no new blueprints unless the feature explicitly requires them.
- `db.session.add()` + `db.session.commit()` for all writes.
- 404 via `db.get_or_404()` or `abort(404)` — never return a blank page for a missing record.
- Redirects after POST: always `redirect(url_for(...))` (PRG pattern).

## HTML/Jinja2
- Bootstrap 4.5 grid and component classes only.
- Badge classes: `badge badge-danger` (High), `badge badge-warning` (Medium), `badge badge-success` (Low/Done).
- Form fields: always render via `{{ form.field(class="form-control") }}`.
- CSRF token: always include `{{ form.hidden_tag() }}` inside every `<form>` tag.

## WTForms
- SelectField choices as list of `(value, label)` tuples.
- Shared constants (PRIORITY_CHOICES, PRIORITY_RANK) defined once in `forms.py`.
- Validators: `DataRequired()` for required text fields; SelectField validates against choices automatically.

## Database migrations
- All schema changes via `scripts/migrate_*.py` — never modify the DB directly.
- Migration scripts must be idempotent: check `PRAGMA table_info` before `ALTER TABLE`.
- Always backfill NULLs after `ALTER TABLE ADD COLUMN`: `UPDATE table SET col = default WHERE col IS NULL`.

## Git commit message format
```
<type>(<ticket-id>): <one-line summary>
```
Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
