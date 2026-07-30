# Skill: Generate Documentation

Use this skill whenever you are generating or updating any Markdown document in `docs/artifacts/FLASK-001/`.

## Formatting Rules

1. **Document header**: Every document must start with a level-1 heading matching the filename.
2. **Metadata block**: Every document must have a metadata table immediately after the heading:
   ```
   | Field | Value |
   |---|---|
   | Ticket ID | FLASK-001 |
   | Feature | Automated Documentation Sync |
   | Phase | N — Phase Name |
   | Status | Draft / Under Review / Approved |
   | Author | GitHub Copilot (<agent-name> agent) |
   | Date | YYYY-MM-DD |
   ```
3. **Section numbering**: Use `## 1.`, `## 2.` etc — never skip numbers.
4. **Tables**: Always include a header row separator (`|---|---|`).
5. **Code blocks**: Always specify the language (` ```python`, ` ```bash`, ` ```text`).
6. **Not Specified**: Use exactly `"Not Specified"` (with quotes in tables, without in prose) for any missing value — never blank, never `N/A`, never `Unknown`.
7. **Status fields**: Use exactly: `Draft`, `Under Review`, `Approved`, `Closed`.
8. **File size**: Documents should be at least 500 bytes — if a section has nothing to say, write "No issues identified in this dimension."

## Prohibited Content

- No PII (names, email addresses, phone numbers)
- No secrets, tokens, API keys, or passwords
- No references to internal systems not in the repository
- No inferred facts — only facts verifiable in the repository files

## Output Path Convention

All documents for FLASK-001 go in: `docs/artifacts/FLASK-001/`

| Phase | Filename |
|---|---|
| 1 — Requirements | `requirements.md` |
| 2 — Architecture | `architecture.md` |
| 3 — Design Review | `design-review.md` |
| 4 — Impl Planning | `impl-plan.md` |
| 5 — Implementation | (code files only) |
| 6 — Code Review | `review_report.md` |
| 7 — Verification | `verification_report.md` |
| 8 — PR | `.sdlc/pr-description.md` |
