# Phase 6 — Code Review Prompt

## Context
You are a peer reviewer evaluating the Phase 5 implementation before the PR.

## Input
All changed source files and `.claude/artifacts/<TICKET-ID>/requirements.md`.

## Task
Review every changed file against this checklist and write `.claude/artifacts/<TICKET-ID>/review_report.md`:

| Area | Question |
|------|----------|
| Correctness | Does each component satisfy the FRs and ACs in requirements.md? |
| Security | Are secrets excluded? Is user input validated at the form layer? |
| Error Handling | Are missing records, empty states, and bad inputs handled? |
| Test Coverage | Do tests cover happy path AND edge cases (unknown values, empty DB)? |
| Code Clarity | Are names self-explanatory? Can a reader follow the logic without comments? |
| DRY | Is any logic duplicated that should be a shared constant or function? |
| Dependency Safety | Are any known-vulnerable package versions introduced? |

## Blocker rule
Any HIGH severity finding → mark review BLOCKED → return to Phase 5.

## Commit
`git add .claude/artifacts/<TICKET-ID>/review_report.md && git commit -m "docs(<TICKET-ID>): Phase 6 code review"`
