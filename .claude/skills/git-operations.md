# Skill: git-operations

## Purpose
Standard git operations used throughout the SDLC pipeline.

## Commit an artifact
```bash
git add .claude/artifacts/<TICKET-ID>/<filename>.md
git commit -m "docs(<TICKET-ID>): Phase <N> <name>"
```

## Commit source code changes
```bash
git add <file1> <file2> ...   # stage specific files — never `git add .`
git status                    # verify only intended files are staged
git commit -m "feat(<TICKET-ID>): <summary>"
```

## Create a PR

**Preferred — GitHub MCP** (see `github-operations` skill):
```
github_create_pull_request:
  owner: uppalashravanreddy
  repo: Flask-Task-Manager
  title: "<TICKET-ID>: <story summary>"
  body: <contents of .claude/artifacts/<TICKET-ID>/pr-description.md>
  head: <current-branch>
  base: main
```

**Fallback — gh CLI**:
```bash
gh pr create \
  --title "<TICKET-ID>: <story summary>" \
  --body-file .claude/artifacts/<TICKET-ID>/pr-description.md \
  --base main \
  --head <current-branch>
```

## Push branch
```bash
git push origin <current-branch>
```
Always push before creating a PR. Do NOT use `--force` to main.

## Rules
- NEVER `git add .` — always stage specific files to avoid committing `.env` or generated artifacts.
- NEVER `git push --force` to main.
- NEVER `--no-verify` — hooks must run.
- NEVER merge the PR — create it and stop.
- Branch naming: `feature/<TICKET-ID>-<short-slug>` (e.g. `feature/FLASK-002-task-priority`).
- After `git status`, if `.env` appears in the staged list → STOP and remove it with `git restore --staged .env`.
