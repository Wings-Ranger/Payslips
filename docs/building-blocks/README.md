# Building Blocks - Beginner to Intermediate Path

This folder bridges foundational knowledge to production-ready implementation choices.

Use this path when a technique or code-block doc feels too advanced, or when you want stronger design guardrails before editing application code.

## Recommended Learning Order

1. [implementation-basics.md](implementation-basics.md)
2. [configuration-and-paths.md](configuration-and-paths.md)
3. [python-data-models.md](python-data-models.md)
4. [regex-basics.md](regex-basics.md)
5. [dataframe-basics.md](dataframe-basics.md)
6. [testing-basics.md](testing-basics.md)
7. [tkinter-basics.md](tkinter-basics.md)

## Expected Outcome Per Step

- `implementation-basics`: you can scope a change and ship in safe increments.
- `configuration-and-paths`: you can design resilient runtime configuration and path handling.
- `python-data-models`: you can model parser output with clear schema boundaries.
- `regex-basics`: you can design maintainable extraction rules and fallback behavior.
- `dataframe-basics`: you can build deterministic table pipelines for reporting.
- `testing-basics`: you can lock behavior before and after refactors.
- `tkinter-basics`: you can keep UI responsive while background work runs.

## How To Use With Other Docs

1. Read one building block.
2. Open one target implementation doc in `docs/code-blocks` or `docs/coding-techniques`.
3. Apply the checklist from the building block while implementing.
4. Add or run tests before finalizing changes.

## When To Skip Ahead

- If you already know a concept deeply, skip directly to the relevant implementation doc.
- If a concept is blocking progress, return to the corresponding building block and complete the practice checklist first.
