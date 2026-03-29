# Building Block: Implementation Basics

## Goal

Learn a simple repeatable way to implement a feature safely.

## Core Workflow

1. Define input, output, and side effects in one short note.
2. Start with the smallest working version.
3. Add one rule at a time.
4. Print or log intermediate values while learning.
5. Add one test for each major rule.
6. Refactor only after behavior is correct.

## Scope Before You Code

- Identify what must stay unchanged (existing outputs, column names, file formats).
- Identify what can change (new fields, new notes, extra validation columns).
- Write one explicit non-goal so you do not drift during implementation.

## Quality Gate Checklist

Before marking a change complete, verify:

1. Existing tests still pass.
2. New behavior has at least one focused test.
3. Error messages are actionable and mention the failing input.
4. Output order is deterministic where reports are generated.
5. Logging/notes help explain skipped or partially parsed records.

## When This Is Enough

- You are adding a small feature.
- You are learning a new part of the codebase.

## When You Need More

- If parsing logic gets complex, read [regex-basics.md](regex-basics.md).
- If data tables are involved, read [dataframe-basics.md](dataframe-basics.md).
- If config or file locations are involved, read [configuration-and-paths.md](configuration-and-paths.md).

## Common Failure Pattern

- Implementing multiple behavior changes in one commit without intermediate validation.

## Better Pattern

1. Add one failing test.
2. Implement one behavior change.
3. Confirm tests.
4. Repeat for the next behavior change.
