# Security Standards

## Secrets management
- `.env` is NEVER committed to git (listed in `.gitignore`).
- `.env` contains: `JIRA_INSTANCE_URL`, `JIRA_USER_EMAIL`, `JIRA_API_KEY`, and optionally `SECRET_KEY`.
- `SECRET_KEY` hardcoded fallback in `app.py` is pre-existing and out of scope for feature work — do not change it.
- Never log, print, or embed API keys in source files.

## Input validation
- All user-facing inputs validated via WTForms validators (`DataRequired`, `Length`, `SelectField` choices list).
- SelectField: invalid choices are rejected automatically by WTForms — do not add manual `if value not in [...]` guards.
- No raw SQL — all database queries via SQLAlchemy ORM.

## CSRF
- Every POST form must include `{{ form.hidden_tag() }}` inside the `<form>` tag.
- Flask-WTF CSRF protection is enabled globally — do not disable it.

## Dependency security
- Before adding any new package, check its PyPI page for known CVEs.
- Pin versions in `requirements.txt` — do not use unbounded `>=` ranges for security-sensitive packages.

## JIRA integration
- JIRA REST API calls use HTTP Basic Auth with email + API key from `.env`.
- Never embed credentials in `scripts/jira_fetch.py` or any other source file.
- `python-dotenv` loads credentials at runtime only.
