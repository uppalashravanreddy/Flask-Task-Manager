# Skill: review-test-cases

## Purpose
Review written test cases for completeness, correctness, and duplication before pushing to Confluence or running.

## Step 1 — Coverage check

For each AC in requirements.md:
- Is there at least one test case? → if NO → flag as gap
- Is the test at the right level? (visual → E2E, DB → integration, logic → unit)
- Does the test case title describe the EXPECTED behaviour, not just the action?

## Step 2 — Duplication check

Run:
```bash
python -m pytest tests/ --collect-only -q 2>&1
```

Then use Grep to search across `tests/` for function names and assertions similar to the new test cases:
- If a function name differs by only `_v2` or `_new` → likely duplicate
- If assertion checks the same field + value → likely duplicate

**Rule**: Duplicates waste CI time and create false confidence. Remove or merge them.

## Step 3 — Quality checklist per test case

| Check | Pass criteria |
|-------|--------------|
| ID format | Follows `TC-<TICKET>-<TYPE>-<NN>` |
| Title | Describes expected outcome, not test mechanics |
| Level correct | Logic → unit, DB/route → integration, visual → E2E |
| Has pytest path | Points to real file + function that exists |
| Preconditions clear | Reader knows what state is needed |
| Expected result specific | Not "it works" — states exact value/behaviour |
| Priority assigned | P1 / P2 / P3 |

## Step 4 — Flag issues

Report findings in this format:
```
REVIEW FINDING
TC-ID: TC-FLASK-002-E2E-03
Issue: Testing badge CSS class at unit level — this requires E2E.
Action: Move to E2E, write Playwright test.
```

## Step 5 — Output

Write a review summary section at the bottom of test-cases.md:
```markdown
## Review Summary
- Reviewed: <N> test cases
- Gaps found: <N> (list them)
- Duplicates removed: <N>
- All remaining cases: APPROVED / NEEDS REWORK
```

## When to use
- After Phase 7.3 writes test-cases.md, before pushing to Confluence.
- When adding tests for a new story: run this to catch duplication against ALL existing tests.
- Before any PR that adds new test files.
