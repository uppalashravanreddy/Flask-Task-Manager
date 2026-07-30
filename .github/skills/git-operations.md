# Skill: Git Operations

Use this skill for all git operations in the Flask Task Manager repository.

## Branch Naming Convention

| Purpose | Branch Name |
|---|---|
| FLASK-001 feature work | `feat/FLASK-001-doc-sync` |
| Bug fix | `fix/<description>` |
| Documentation only | `docs/<description>` |
| Chores | `chore/<description>` |

## Commit Message Convention

Format: `<type>(scope): <imperative description> — <ticket-ref>`

| Type | When to Use |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `test` | Adding or fixing tests |
| `docs` | Documentation changes only |
| `chore` | Dependency updates, `.gitignore`, tooling |
| `refactor` | Code change with no behaviour change |

Examples:
```
feat(FLASK-001): implement repo_scanner file reading — TASK-01
fix(FLASK-001): handle missing README.md gracefully — CR-02
test(FLASK-001): add edge case for empty requirements.txt
docs(FLASK-001): add architecture.md
chore: add .gitignore for __pycache__ and instance/
```

## Safe Staging Procedure

Always use specific file staging — never `git add .` or `git add -A`:

```bash
git add src/doc_sync/repo_scanner.py
git add tests/unit/test_repo_scanner.py
git status   # verify exactly what is staged before committing
git commit -m "feat(FLASK-001): implement repo_scanner — TASK-01"
```

## Files That Must Never Be Committed

Add these to `.gitignore` if not already present:
```
__pycache__/
*.pyc
instance/data.db
.env
.env.*
*.egg-info/
dist/
.coverage
htmlcov/
```

## Pre-Commit Checklist

Before every commit, confirm:
- [ ] No `.env` file staged
- [ ] No `instance/data.db` staged  
- [ ] No `__pycache__` staged
- [ ] `git status` shows only the intended files
- [ ] Tests pass: `python -m pytest tests/ -q`

## Creating and Pushing a Feature Branch

```bash
git checkout -b feat/FLASK-001-doc-sync
# ... make changes ...
git push -u origin feat/FLASK-001-doc-sync
```
