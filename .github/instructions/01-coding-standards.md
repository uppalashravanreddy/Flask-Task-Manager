# Instruction: Coding Standards

Apply these rules to every Python file written or modified in this repository.

## File I/O
- Always use `pathlib.Path` — never raw string paths or `os.path`
- Wrap all file reads in `try/except`; return `None` on `FileNotFoundError`
- Wrap all file writes in `try/except`; return `False` or raise a typed exception on failure
- Never use `open()` without specifying `encoding="utf-8"`

## Error Handling
- Return `None` or `"Not Specified"` on I/O failure — do NOT raise to the caller
- Log failures with `print(f"WARNING: ...", file=sys.stderr)` — never silently swallow
- Use typed exceptions (`FileNotFoundError`, `ValueError`) — never bare `except Exception`

## Secrets and Configuration
- All configuration from `os.environ` or `python-dotenv` — never hardcoded
- If a required env var is missing: print a clear error and `sys.exit(1)` — never default to a secret value
- Never log, print, or write secrets to any output file

## Function Design
- One function = one responsibility
- Max 40 lines per function (excluding docstrings and blank lines)
- Function names: descriptive verbs (`read_repository_files`, not `process`)
- One-line docstring only for public API functions — no multi-line docstrings
- No inline comments unless the WHY is non-obvious (a hidden constraint, a workaround)

## Imports
- Standard library first, then third-party, then local — separated by blank lines
- Prefer explicit imports (`from pathlib import Path`) over wildcard imports

## Not Specified Convention
Any field that cannot be populated from repository evidence must be set to the string `"Not Specified"` — never `None`, never `""`, never `"N/A"`.

## Flask/SQLAlchemy Specifics
- URL routes: always `/resource/<id>` — never `/resource=/<id>`
- All database writes inside a `try/except`; call `db.session.rollback()` on failure
- SECRET_KEY always from `os.environ.get("SECRET_KEY")` with no fallback default

## File Size Guideline
Source files should not exceed 200 lines. If a file approaches that, extract a helper module.
