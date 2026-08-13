# Phase 8 — PR Description Prompt

## Context
You are completing the SDLC cycle by creating the Pull Request.

## Input
All phase artifacts from `.claude/artifacts/<TICKET-ID>/` and the git diff.

## Task

### 1. Write `.claude/artifacts/<TICKET-ID>/pr-description.md` with ALL sections:
- **Summary** — 2–3 sentences: what was built and why
- **Changes Made** — table: file, action, reason
- **Test Evidence** — full pytest output from Phase 7
- **SDLC Feedback Loop Applied** — any phase returns and their resolutions
- **Known Limitations** — out of scope items, pre-existing issues, manual steps needed
- **Reviewer Checklist** — tick-list the human reviewer must complete before approving

### 2. Update CHANGELOG.md
Add an entry under `## [Unreleased]` or a new version heading:
```markdown
### Added — <TICKET-ID>: <story summary>
- <one bullet per significant change>
```

### 3. Commit all artifacts
```bash
git add .claude/artifacts/<TICKET-ID>/
git add <all changed source files>
git add CHANGELOG.md
git commit -m "feat(<TICKET-ID>): <one-line summary from requirements>"
```

### 4. Create the GitHub PR
```bash
gh pr create \
  --title "<TICKET-ID>: <story summary>" \
  --body-file .claude/artifacts/<TICKET-ID>/pr-description.md \
  --base main \
  --head <current-branch>
```

### 5. Output the PR URL.

## Rules
- Never push to main directly.
- Never merge the PR — create it and stop.
- CHANGELOG.md entry is mandatory — a PR without a changelog entry is incomplete.
