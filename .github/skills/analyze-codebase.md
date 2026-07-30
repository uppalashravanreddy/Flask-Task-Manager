# Skill: Analyze Codebase

Use this skill whenever you need to understand the structure and content of the Flask Task Manager before proposing or making changes.

## Canonical Files to Read

Always read these files in this order when analyzing the codebase:

| Priority | File | Purpose |
|---|---|---|
| 1 | `app.py` | App factory, DB config, SECRET_KEY |
| 2 | `models.py` | SQLAlchemy models (Task) |
| 3 | `routes.py` | URL handlers — check for `/delete=/` bug |
| 4 | `forms.py` | Flask-WTF form classes |
| 5 | `requirements.txt` | Dependencies and versions |
| 6 | `src/doc_sync/repo_scanner.py` | Which files the scanner reads |
| 7 | `src/doc_sync/extractor.py` | How facts are extracted |
| 8 | `src/doc_sync/page_creator.py` | How the markdown is assembled |
| 9 | `src/main.py` | CLI entry point, exit codes |

## Known Issues to Check For

- `app.py`: `SECRET_KEY = 'secret-key'` is hardcoded — must come from `.env`.
- `routes.py`: `/delete=/<task_id>` has a typo — correct form is `/delete/<task_id>`.
- `requirements.txt`: `datetime` is stdlib, not a pip package — remove it.
- `requirements.txt`: No version pins — recommend pinning all packages.
- `instance/data.db`: Binary file committed to git — should be in `.gitignore`.
- `__pycache__/`: Bytecode committed — should be in `.gitignore`.

## Analysis Output Format

When reporting your analysis findings, use this format:

```
### Codebase Analysis Summary
- Entry point: src/main.py (run_pipeline function)
- Key classes: RepositoryExtractor, RepoScanner, PageCreator
- Test coverage: X unit tests, Y integration tests
- Known issues found: [list]
- Files missing from architecture: [list]
```
