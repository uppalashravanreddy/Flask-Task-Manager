# Instruction: Security Standards

Apply these rules across all phases. Security violations are **Blocking** findings.

## Secrets Management
- ALL secrets (API keys, tokens, passwords, SECRET_KEY) must come from environment variables
- Use `python-dotenv` to load from a local `.env` file — add `.env` to `.gitignore`
- Never hardcode a secret value, even for testing
- If a required secret is missing at runtime: fail fast with a clear message, not a default

```python
# WRONG
SECRET_KEY = 'my-secret'

# CORRECT
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")
```

## Protected Files (Never Write Directly)
These files must only be modified through the designated tool or script:
| File | How to Modify |
|---|---|
| `.sdlc/state.json` | `python scripts/state_manager.py <command>` only |
| `.github/agents/*.md` | Approved agent redesign only — not by phase agents |
| `.github/instructions/*.md` | Manual review required — not by phase agents |
| `.github/prompts/*.prompt.md` | Manual review required — not by phase agents |

## File Write Boundaries
Phase agents may only write to:
- `docs/artifacts/FLASK-001/` — documentation outputs
- `src/doc_sync/` — pipeline source code
- `tests/` — test files
- `scripts/orchestrator.py`, `scripts/reporter.py` — orchestration scripts
- `.sdlc/phase-outputs/` — via the post-write hook (automatically)

Writing to any other path requires explicit human approval.

## Output Content Rules
Generated documentation must NEVER contain:
- Secrets, tokens, API keys, or passwords
- PII (names, emails, phone numbers) not already in the source repository
- References to internal systems not present in the repository
- Inferred or guessed values — use `"Not Specified"` for missing data

## Git Safety
Never stage or commit:
- `.env` or any `*.env` file
- `instance/data.db`
- `__pycache__/` or `*.pyc` files
- Any file matching `*secret*`, `*token*`, `*password*`

## Dependency Safety
Pin all package versions in `requirements.txt`. When reviewing dependencies:
1. Check for known CVEs on PyPI or GHSA
2. Prefer packages with recent maintenance history
3. Flag any package without version pins as a Minor finding in the code review
