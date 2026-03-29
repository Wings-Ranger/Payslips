# Coding Techniques - Index

This directory documents the higher-level coding techniques used in this repository.

Unlike docs/code-blocks (which is organized by function or file block), these notes are organized by technique so future changes can reuse patterns consistently.

## Technique Notes

| File | Technique | Where It Appears |
|------|-----------|------------------|
| [dataclass-modeling.md](../../../coding-techniques/dataclass-modeling.md) | Typed record modeling with dataclasses | src/payslip_tracker.py |
| [regex-and-section-based-parsing.md](../../../coding-techniques/regex-and-section-based-parsing.md) | Section scanning plus regex extraction | src/payslip_tracker.py |
| [defensive-parsing-and-fallbacks.md](../../../coding-techniques/defensive-parsing-and-fallbacks.md) | Defensive parsing, null-safe fallbacks, and skip notes | src/payslip_tracker.py |
| [config-driven-paths-and-behavior.md](config-driven-paths-and-behavior.md) | Config-driven behavior and path resolution | src/payslip_tracker.py, src/config.json |
| [dataframe-transformation-pipeline.md](dataframe-transformation-pipeline.md) | DataFrame pipeline for normalization and export prep | src/payslip_tracker.py |
| [business-rule-validation-columns.md](../../../coding-techniques/business-rule-validation-columns.md) | Cross-field validation with tolerance-based checks | src/payslip_tracker.py, tests/test_sheets.py |
| [excel-presentation-layer-formatting.md](../../../coding-techniques/excel-presentation-layer-formatting.md) | Presentation-layer formatting in openpyxl | src/payslip_tracker.py |
| [test-first-parser-coverage.md](../../../coding-techniques/test-first-parser-coverage.md) | Focused unit testing around parser and calculations | tests/test_parser.py, tests/test_sheets.py |
| [operations-and-debug-tooling.md](../../../coding-techniques/operations-and-debug-tooling.md) | Small-purpose scripts for diagnosis and migration | scripts/*.py |

## How To Use This Folder

1. Start with this index to select a technique.
2. Open the linked technique file for implementation details and guardrails.
3. Cross-reference docs/code-blocks when you need exact code-level behavior.
## Beginner Ramp-Up

This is a legacy document. For beginner-friendly foundations, start with [../../../building-blocks/README.md](../../../building-blocks/README.md).
Then return here only if you specifically need the pre-GUI historical implementation details.

## When This Is Not The Best Fit

- This file documents an older architecture and may not match the current app flow.
- Prefer current docs in docs/code-blocks and docs/coding-techniques for active implementation work.
- Use this as reference context, not as a copy-paste template.
