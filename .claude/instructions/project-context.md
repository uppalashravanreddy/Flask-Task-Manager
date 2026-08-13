# Project Context

## What this project is
Flask Task Manager — a CRUD web app for managing tasks. Stack:
- **Backend**: Python 3, Flask, SQLAlchemy ORM, SQLite
- **Forms**: Flask-WTF / WTForms with CSRF protection
- **Frontend**: Jinja2 templates, Bootstrap 4.5
- **Tests**: pytest, no virtual environment — system Python
- **Branch strategy**: one feature branch per User Story (`feature/TICKET-ID-slug`)

## Working directory layout
```
Flask-Task-Manager/
  app.py                  # Flask app factory and DB init
  models.py               # SQLAlchemy models
  routes.py               # All Flask routes
  forms.py                # WTForms form classes + shared constants
  templates/              # Jinja2 HTML templates
  tests/unit/             # pytest unit tests
  tests/integration/      # pytest integration tests
  scripts/                # Utility scripts (migrations, JIRA fetch, hooks)
  docs/artifacts/         # SDLC phase outputs, one sub-folder per ticket
  .claude/                # Claude Code config: agents, prompts, skills, instructions
  CHANGELOG.md            # Keep updated with every merged feature
  requirements.txt        # pip dependencies
```

## Key constraints
- Bootstrap 4.5 is pinned — use `badge badge-*` classes, NOT Bootstrap 5 `bg-*`.
- No virtual environment — run `python -m pytest` from the project root.
- `.env` must NEVER be committed — it contains JIRA API keys.
- `SECRET_KEY` has a hardcoded fallback in `app.py` — do not modify it in feature work (pre-existing, out of scope).
- Do not add new pip dependencies without updating `requirements.txt` and documenting the decision.
