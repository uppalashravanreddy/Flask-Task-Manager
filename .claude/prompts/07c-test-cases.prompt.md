# Phase 7.3 — Test Cases Prompt

## Context
You are writing concrete test cases for every AC, avoiding duplicates, and storing them in Confluence.

## Input
`.claude/artifacts/<TICKET-ID>/requirements.md` and all existing files in `tests/`.

## Task

### 1. Inventory existing tests
```bash
python -m pytest tests/ --collect-only -q
```

### 2. For each AC — dedup check
Use Grep to search `tests/` for assertions similar to the AC. Mark as:
- **COVERED**: existing test covers it fully → record the test path, write no new test
- **PARTIAL**: existing test covers part of it → extend the existing test
- **NEW**: no coverage → write new test(s)

### 3. Write test code for NEW/PARTIAL cases
Follow patterns in `.claude/instructions/testing-standards.md`. Test IDs: `TC-<TICKET-ID>-UNIT-<N>`, `-INT-<N>`, `-E2E-<N>`.

### 4. Write `.claude/artifacts/<TICKET-ID>/test-cases.md`
Include:
- Full test case table (TC-ID, AC-ID, title, level, automated, pytest path, priority, status)
- Duplicate check results table

### 5. Push to Confluence
`confluence_create_page`:
- title: `<TICKET-ID> Test Cases`
- parent: `<TICKET-ID> Test Plan`

### 6. JIRA comment
Use `jira_add_comment` to post test case count on the JIRA ticket.

### 7. Commit
```bash
git add .claude/artifacts/<TICKET-ID>/test-cases.md tests/
git commit -m "test(<TICKET-ID>): Phase 7.3 test cases"
```

## Rules
- Never duplicate. Reuse existing tests when they cover the same assertion.
- E2E tests use `flask_base_url` fixture from `tests/e2e/conftest.py`.
- Bootstrap badge tests MUST be E2E — badge class cannot be verified at unit level.
