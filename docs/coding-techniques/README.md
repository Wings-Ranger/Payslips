# Coding Techniques - Index

This directory documents the higher-level coding techniques used in this repository.

Unlike docs/code-blocks (which is organized by function or file block), these notes are organized by technique so future changes can reuse patterns consistently.

If you are new to these concepts, start with [../building-blocks/README.md](../building-blocks/README.md) before diving into advanced technique notes.

## Technique Notes

| File | Technique | Where It Appears |
|------|-----------|------------------|
| [dataclass-modeling.md](dataclass-modeling.md) | Typed record modeling with dataclasses | src/payslip_tracker.py |
| [regex-and-section-based-parsing.md](regex-and-section-based-parsing.md) | Section scanning plus regex extraction | src/payslip_tracker.py |
| [defensive-parsing-and-fallbacks.md](defensive-parsing-and-fallbacks.md) | Defensive parsing, null-safe fallbacks, and skip notes | src/payslip_tracker.py |
| [config-driven-paths-and-behavior.md](config-driven-paths-and-behavior.md) | Config-driven behavior and path resolution | src/payslip_tracker.py, src/config.json |
| [dataframe-transformation-pipeline.md](dataframe-transformation-pipeline.md) | DataFrame pipeline for normalization and export prep | src/payslip_tracker.py |
| [business-rule-validation-columns.md](business-rule-validation-columns.md) | Cross-field validation with tolerance-based checks | src/payslip_tracker.py, tests/test_sheets.py |
| [excel-presentation-layer-formatting.md](excel-presentation-layer-formatting.md) | Presentation-layer formatting in openpyxl | src/payslip_tracker.py |
| [theme-driven-ui-customization.md](theme-driven-ui-customization.md) | Theme-driven GUI styling with live reload | ui_theme.json, src/payslip_gui.py |
| [test-first-parser-coverage.md](test-first-parser-coverage.md) | Focused unit testing around parser and calculations | tests/test_parser.py, tests/test_sheets.py |
| [operations-and-debug-tooling.md](operations-and-debug-tooling.md) | Small-purpose scripts for diagnosis and migration | scripts/*.py |

## How To Use This Folder

1. Start with this index to select a technique.
2. Open the linked technique file for implementation details and guardrails.
3. Cross-reference docs/code-blocks when you need exact code-level behavior.

## When A Technique May Not Be The Best Choice

- Prefer simpler direct code for one-off scripts.
- Prefer robust documented patterns for reusable production paths.
- Adjust each technique to the payslip/provider format instead of copying blindly.
