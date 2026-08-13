# Skill: analyze-codebase

## Purpose
Read and summarize the current state of the Flask Task Manager codebase to give an agent full context before starting any phase.

## Steps
1. Read `models.py` — note every model class, column, and its type/nullable/default.
2. Read `forms.py` — note every form class, field, validator, and shared constant.
3. Read `routes.py` — note every route path, method (GET/POST), and what it reads/writes.
4. Read `templates/index.html`, `add.html`, `edit.html` — note the Bootstrap version in use and any dynamic rendering patterns.
5. Run `python -m pytest tests/unit/ tests/integration/ --collect-only -q` — list existing tests without running them.
6. Output a structured summary:
   - Models: list of columns with types
   - Forms: list of fields with validators
   - Routes: list of routes with HTTP methods
   - Templates: Bootstrap version confirmed, any badge/class patterns in use
   - Existing tests: count by directory

## When to use
- At the start of Phase 2 (Architecture) to understand what already exists.
- At the start of Phase 5 (Implementation) before editing any file.
- Whenever an agent needs to verify the current state matches the artifacts.
