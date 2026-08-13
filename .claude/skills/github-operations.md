# Skill: github-operations

## Purpose
Use the GitHub MCP server to create PRs, push files, create issues, and comment on PRs — directly from Claude Code without leaving the agent loop.

## MCP server
Configured in `.vscode/mcp.json` under key `"github"`. Reads `GITHUB_PERSONAL_ACCESS_TOKEN` from `.env`.

## Available MCP tools (key ones for this pipeline)

### Create a Pull Request (Phase 8)
```
github_create_pull_request:
  owner: uppalashravanreddy
  repo: Flask-Task-Manager
  title: "FLASK-002: Add Task Priority (High/Medium/Low)"
  body: <contents of .claude/artifacts/<TICKET-ID>/pr-description.md>
  head: feat/FLASK-002-task-priority
  base: main
  draft: false
```
Returns the PR URL and PR number. Store both in `.sdlc/state.json` under `phases.8.pr_url` and `phases.8.pr_number`.

### Add a comment to a PR (Phase 8 — post test results)
```
github_add_issue_comment:
  owner: uppalashravanreddy
  repo: Flask-Task-Manager
  issue_number: <PR number>
  body: |
    ## Test Results — FLASK-002
    | Type | Passed | Failed |
    |------|--------|--------|
    | Unit | 6 | 0 |
    | Integration | 4 | 0 |
    | E2E | 11 | 0 |
    Report: .claude/reports/FLASK-002/index.html
```

### Create a GitHub Issue from a test failure (Phase 7.4)
When a test fails in Phase 7.4 and you need to track it as a defect:
```
github_create_issue:
  owner: uppalashravanreddy
  repo: Flask-Task-Manager
  title: "[DEFECT] <TICKET-ID>: <failing test name>"
  body: |
    **Found in**: Phase 7.4 Test Execution
    **Story**: <TICKET-ID>
    **Failing test**: tests/unit/test_priority.py::test_sort_high_first
    **Error**: AssertionError: expected [High, Medium, Low], got [Low, Medium, High]
    **Impact**: AC-2 not met
  labels: ["bug", "phase-7"]
```

### Push a single file to a branch (use sparingly — prefer git CLI for commits)
```
github_create_or_update_file:
  owner: uppalashravanreddy
  repo: Flask-Task-Manager
  path: .claude/artifacts/FLASK-002/verification_report.md
  message: "docs(FLASK-002): Phase 7.5 verification report"
  content: <base64-encoded file content>
  branch: feat/FLASK-002-task-priority
```
**When to use**: When Claude needs to write a file directly to the remote branch without a local git commit (e.g., from a remote agent context). For normal local development, use `git add` + `git commit` + `git push` instead — it preserves proper git history.

### Get PR status
```
github_get_pull_request:
  owner: uppalashravanreddy
  repo: Flask-Task-Manager
  pull_number: <PR number>
```

### List open PRs
```
github_list_pull_requests:
  owner: uppalashravanreddy
  repo: Flask-Task-Manager
  state: open
```

## Token setup
Add to `.env` (never commit this file):
```
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

Required token scopes: `repo` (read + write), `pull_requests` (read + write).

Generate at: https://github.com/settings/tokens/new

## Fallback — gh CLI
If the GitHub MCP is not available (MCP not started, token expired), fall back to:
```bash
gh pr create --title "..." --body-file .claude/artifacts/<TICKET-ID>/pr-description.md --base main
gh issue create --title "..." --body "..."
gh pr comment <PR-number> --body "..."
```

## When to use GitHub MCP vs git CLI

| Operation | Use |
|-----------|-----|
| Create PR | GitHub MCP `create_pull_request` (preferred) or `gh pr create` |
| Push commits | `git push` CLI — preserves commit history and author |
| Create defect issue | GitHub MCP `create_issue` |
| Comment on PR | GitHub MCP `add_issue_comment` |
| Push single file remotely | GitHub MCP `create_or_update_file` (agentic/remote context only) |
| Branch operations | `git` CLI |
