# Building Block: DataFrame Basics

## Goal

Transform record dictionaries into stable report tables.

## Beginner Implementation Steps

1. Build a DataFrame from a list of dictionaries.
2. Ensure key columns exist.
3. Sort with deterministic keys.
4. Add derived columns in separate steps.
5. Export to Excel/CSV only after validation columns are ready.

## Intermediate Pipeline Pattern

Use small named stages:

1. `ingest`: create DataFrame and normalize dtypes.
2. `shape`: add/fill required columns.
3. `derive`: compute checks and derived metrics.
4. `present`: rename/reorder columns for outputs.

This makes debugging faster because each stage has one purpose.

## Good Habits

- Keep transformation stages small and named.
- Avoid mutating unrelated columns in one big statement.
- Validate expected columns before final export.

## Data Quality Checks

- Assert required columns are present before each major stage.
- Keep sort keys explicit to prevent random output ordering.
- Handle missing numeric values before arithmetic to avoid `NaN` cascades.
- Keep `N/A` placeholders for presentation, but prefer numeric nulls during calculations.

## Performance Note

Vectorized operations are preferred over row-by-row loops for large data sets.

## When DataFrames Are Overkill

- Very small data and simple output can use plain lists or csv module.
