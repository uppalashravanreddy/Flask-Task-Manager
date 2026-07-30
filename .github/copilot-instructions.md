# GitHub Copilot Instructions — Flask Task Manager

## Project Context
This is the Flask Task Manager repository. It contains:
- A CRUD web app (Flask + SQLAlchemy + Flask-WTF)
- An Automated Documentation Sync pipeline (`src/doc_sync/`) — ticket FLASK-001
- An Agentic SDLC pipeline driving all phases from requirements to PR

## Agentic SDLC Pipeline
The project uses a multi-agent SDLC pipeline managed by `.github/agents/`, `.github/prompts/`, and `.github/skills/`. Each phase has a dedicated agent and prompt. State is persisted in `.sdlc/state.json`. The orchestrator (`scripts/orchestrator.py`) coordinates phase execution.

## Code Standards
- Python 3.11+, Flask conventions, SQLAlchemy ORM patterns
- All secrets must come from environment variables (never hardcoded)
- Missing documentation values must be written as `"Not Specified"` — never inferred
- Write `pytest` tests for every new function; place units under `tests/unit/`, integration under `tests/integration/`
- URL route patterns must use `/resource/<id>` — never `/resource=/<id>`

## File Ownership by Phase
| SDLC Phase | Primary Output Files |
|---|---|
| 1 — Requirements | `docs/artifacts/FLASK-001/requirements.md` |
| 2 — Architecture | `docs/artifacts/FLASK-001/architecture.md` |
| 3 — Design Review | `docs/artifacts/FLASK-001/design-review.md` |
| 4 — Impl Planning | `docs/artifacts/FLASK-001/impl-plan.md` |
| 5 — Implementation | `src/doc_sync/`, `scripts/`, `tests/` |
| 6 — Code Review | `docs/artifacts/FLASK-001/review_report.md` |
| 7 — Verification | `tests/`, test run output |
| 8 — PR | Pull Request on GitHub |

## Skills Available
Reference these skill files in your instructions:
- `#file:.github/skills/analyze-codebase.md` — how to read and parse this codebase
- `#file:.github/skills/generate-docs.md` — documentation formatting rules
- `#file:.github/skills/run-tests.md` — how to run and interpret tests
- `#file:.github/skills/git-operations.md` — staging, committing, branching
- `#file:.github/skills/sdlc-state.md` — reading and advancing pipeline state

## State Management
Always read `.sdlc/state.json` before starting any phase action. Use `scripts/state_manager.py` to transition phases; do not manually edit `state.json`.
