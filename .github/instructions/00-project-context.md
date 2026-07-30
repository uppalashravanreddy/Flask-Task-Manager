# Instruction: Project Context — FLASK-001

## Ticket
- **ID:** FLASK-001
- **Feature:** Automated Documentation Sync
- **Repository:** Flask-Task-Manager
- **Status:** Active

## User Story
> As a developer working on the Flask Task Manager repository, I want a manual documentation sync process that scans the repository and generates a technical profile page for Confluence, so that project documentation stays accurate, versioned, and based on repository evidence.

## Repository Map
```
Flask-Task-Manager/
├── app.py               Flask app factory; SQLite config; SECRET_KEY (currently hardcoded — bug)
├── models.py            Task model: id, title (unique), date, desc
├── routes.py            CRUD routes; NOTE: delete route has URL bug /delete=/ → /delete/
├── forms.py             AddTaskForm, DeleteTaskForm (Flask-WTF)
├── requirements.txt     Dependencies (no version pins; datetime is stdlib — remove it)
├── templates/           Jinja2 HTML templates
├── src/
│   ├── main.py          CLI entry point: python src/main.py --repo . --output <path>
│   └── doc_sync/
│       ├── repo_scanner.py   Reads 6 source files into a dict
│       ├── extractor.py      Extracts structured facts; missing → "Not Specified"
│       └── page_creator.py   Renders facts into Markdown technical profile
├── tests/
│   ├── unit/            test_repo_scanner.py, test_extractor.py, test_doc_sync.py
│   └── integration/     test_pipeline.py
├── docs/artifacts/FLASK-001/   All SDLC phase output documents
├── .sdlc/
│   ├── state.json               Pipeline state (source of truth)
│   └── phase-outputs/           Immutable archive of each phase's outputs
├── scripts/
│   ├── orchestrator.py          Pipeline coordinator (resume-aware)
│   ├── state_manager.py         State CLI
│   ├── html_report.py           SDLC HTML summary generator
│   ├── test_runner.py           pytest → HTML test report
│   └── hooks/                   Write/delete guards + post-phase copier
└── reports/                     Generated HTML reports (sdlc-summary.html, test-report.html)
```

## Scope: IN
- Scan 6 files: README.md, requirements.txt, app.py, models.py, routes.py, forms.py
- Generate structured Markdown technical profile with "Not Specified" for missing values
- Manual trigger via `python src/main.py`
- Output to `docs/artifacts/FLASK-001/technical_profile_report.md`
- New versioned file per run (never overwrite)

## Scope: OUT
- Automatic triggers (push/merge CI)
- CI/CD pipeline integration
- Confluence API publishing (deferred)
- Inferring or guessing missing information

## Known Bugs to Fix During SDLC
| Bug | Location | Fix |
|---|---|---|
| Hardcoded SECRET_KEY | app.py line 4 | Load from os.environ / .env |
| URL typo `/delete=/` | routes.py | Change to `/delete/` |
| `datetime` in requirements.txt | requirements.txt | Remove it (stdlib) |
| No version pins | requirements.txt | Add pinned versions |
| `__pycache__` committed | repo root | Add to .gitignore |
| `instance/data.db` committed | instance/ | Add to .gitignore |

## Pipeline State
State is persisted in `.sdlc/state.json`. On any interruption or reconnect, always read this file first to determine where to resume. Never restart from Phase 1 if state shows a later phase was in progress.

## Resume Rule
If interrupted: find the first phase where `status != "completed"` — resume from there. If `status == "in_progress"`, that phase was running when interrupted; re-run it from the start of its procedure.
