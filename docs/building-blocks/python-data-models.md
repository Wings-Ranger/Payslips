# Building Block: Python Data Models

## Goal

Use structured objects so parsing, validation, and export stay consistent.

## Why Models Help

- Field names are explicit and reusable.
- Missing values are easier to reason about.
- Conversions to dict/table format are predictable.

## Design Pattern

Split fields into three categories:

1. Source fields: directly parsed from payslip text.
2. Derived fields: computed from source fields.
3. Operational fields: metadata such as parse notes.

Keeping these categories clear prevents accidental mixing of business data and debugging state.

## Beginner Implementation Steps

1. List all fields needed for one record.
2. Group fields by topic.
3. Create a dataclass with optional types where needed.
4. Add a notes field for diagnostics.
5. Convert to dictionaries only at export time.

## Type Hint Guidance

- Use `Optional[float]` for values that may be missing during parsing.
- Use `str | None` style only if your Python version and project style support it consistently.
- Reserve `Any` for temporary migration periods and remove it once schema stabilizes.

## Schema Evolution Rules

When adding or renaming a field:

1. Update dataclass.
2. Update parser assignment.
3. Update schema validation.
4. Update header mapping/export.
5. Update tests and fixtures.

## When Not To Overdo It

- For a tiny throwaway script, plain dicts can be faster.
- For long-lived code, models are usually worth it.

## Red Flags

- Model has fields that are never written.
- Derived values are stored but can drift from source values.
- Parsing notes are embedded in business fields instead of metadata.
