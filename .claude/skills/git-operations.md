# Skill: git-operations

## Purpose
Standard git operations used throughout the SDLC pipeline.

## Commit an artifact
```bash
git add docs/artifacts/<TICKET-ID>/<filename>.md
git commit -m "docs(<TICKET-ID>): Phase <N> <name>"
```

## Commit source code changes
```bash
git add <file1> <file2> ...   # stage specific files — never `git add .`
git status                    # verify only intended files are staged
git commit -m "feat(<TICKET-ID>): <summary>"
```

## Create a PR
```bash
gh pr create \
  --title "<TICKET-ID>: <story summary>" \
  --body-file docs/artifacts/<TICKET-ID>/pr-description.md \
  --base main \
  --head <current-branch>
```

## Rules
- NEVER `git add .` — always stage specific files to avoid committing `.env` or generated artifacts.
- NEVER `git push --force` to main.
- NEVER `--no-verify` — hooks must run.
- NEVER merge the PR — create it and stop.
- Branch naming: `feature/<TICKET-ID>-<short-slug>` (e.g. `feature/FLASK-002-task-priority`).
- After `git status`, if `.env` appears in the staged list → STOP and remove it with `git restore --staged .env`.
