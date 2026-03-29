# Building Block: Testing Basics

## Goal

Protect behavior while you refactor or add parsing rules.

## Beginner Testing Workflow

1. Pick one function.
2. Write one success test with realistic sample data.
3. Write one failure/edge-case test.
4. Run tests.
5. Implement or refactor.
6. Re-run tests and check regressions.

## Intermediate Test Design

- Prefer behavior-focused assertions over implementation details.
- Keep fixtures small but representative of real payslip variance.
- Use parameterized tests for repeated pattern cases.
- Separate parser tests from export-format tests to isolate failures quickly.

## What To Test First Here

- Date parsing and week start logic.
- Currency extraction edge cases.
- Missing required schema fields.
- Missing-week detection.

## Failure Triage Order

1. Parser extraction failures.
2. Schema validation mismatches.
3. DataFrame transformation inconsistencies.
4. Output formatting regressions.

Fix in this order so root-cause errors do not create noisy downstream failures.

## When To Add More

- Add integration tests when multiple functions interact.
- Add UI tests only after core processing tests are stable.

## Stability Guardrail

If a test fails intermittently, remove nondeterminism first (ordering, timestamps, locale-specific formatting).
