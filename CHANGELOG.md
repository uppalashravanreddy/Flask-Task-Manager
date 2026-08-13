# Changelog

## [Unreleased]
### Added — FLASK-002: Task Priority (KAN-27)
- `priority` field (High/Medium/Low) on the Task model with `default='Medium'`
- `SelectField` priority dropdown on Add Task and Edit Task forms
- Tasks on the index page sorted by priority: High → Medium → Low
- Bootstrap 4.5 badge colour-coding (danger/warning/success) on index page
- `scripts/migrate_add_priority.py` — idempotent migration script with NULL backfill
- `tests/unit/test_priority.py` — 6 unit tests (sort order, PRIORITY_RANK constants)
- `tests/integration/test_priority_migration.py` — 4 migration integration tests
- `.claude/agents/` — 10 agent files for the full 8-phase Agentic SDLC pipeline
- `.claude/prompts/` — 8 standalone phase prompt files (01–08)
- `.claude/instructions/` — 5 instruction files (project-context, coding-standards, testing-standards, security-standards, failure-handling)
- `.claude/skills/` — 6 skill files (analyze-codebase, generate-docs, git-operations, run-tests, sdlc-state, jira-fetch)
- `scripts/jira_fetch.py` — JIRA KAN backlog fetcher with priority scoring
- `.vscode/mcp.json` — `@sooperset/mcp-atlassian` MCP server for JIRA integration
- `docs/artifacts/FLASK-002/` — full SDLC artifact trail (requirements, architecture, design-review, impl-plan, review-report, verification-report, pr-description)

## [1.0.0] - 2026-07-30
### Added
- FLASK-001: Automated Documentation Sync pipeline
