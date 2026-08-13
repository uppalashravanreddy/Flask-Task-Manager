# Phase 7 — Verification Prompt

## Context
You are verifying both the code and the output quality before creating the PR.

## Input
All test files, `.claude/artifacts/<TICKET-ID>/requirements.md`, and any generated output documents.

## Task

### Part A — Code verification
1. Run: `python -m pytest tests/unit/ tests/integration/ -v`
2. Capture full output verbatim.
3. Map each AC from requirements.md to the test(s) covering it.

### Part B — Output document quality check
If the feature generates a document (e.g. Markdown report, CSV, HTML):
1. Run the pipeline: `python src/main.py --repo . --output <temp_path>`
2. Check the output contains no empty sections.
3. Check "Not Specified" appears only where data genuinely cannot be determined.
4. Check the document is well-formed Markdown.

### Write verification_report.md with:
- Test run results (full pytest output)
- Coverage by test type table
- AC verification table (AC-ID, criteria, test, status)
- Regression check (pre-existing tests still pass)
- Output document quality check results (or note: "Not applicable — feature produces no output document")
- Known gaps

## Blocker rule
ANY test failure → BLOCKED → return to Phase 5. Do not modify tests to force a pass.

## Commit
`git add .claude/artifacts/<TICKET-ID>/verification_report.md && git commit -m "docs(<TICKET-ID>): Phase 7 verification"`
