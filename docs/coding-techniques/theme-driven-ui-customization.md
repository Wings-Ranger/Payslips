# Technique: Theme-Driven UI Customization

## Purpose

Make the frontend easy to restyle without requiring users to edit Python widget code.

## Where Used

- `ui_theme.json`
- `DEFAULT_THEME`, `_load_theme()`, and `_apply_theme()` in `src/payslip_gui.py`

## Core Pattern

1. Keep a complete in-code default theme for safety.
2. Load a JSON file with user overrides.
3. Deep-merge the user theme over defaults.
4. Apply the merged theme to fonts, colors, spacing, and labels.
5. Expose a live reload action in the app.

## Why This Helps Beginners

- Users can change appearance with simple JSON edits.
- Small mistakes are less likely to break the app because defaults still exist.
- Designers or non-programmers can experiment without understanding Tkinter internals.

## Design Guidance

1. Keep the theme schema flat and readable.
2. Prefer named sections over many scattered variables.
3. Separate visual theme settings from runtime processing settings.
4. Document a few safe first edits so beginners know where to start.
## Beginner Ramp-Up

If this feels advanced, read these first:

- [../building-blocks/implementation-basics.md](../building-blocks/implementation-basics.md)
- [../building-blocks/configuration-and-paths.md](../building-blocks/configuration-and-paths.md)
- [../building-blocks/python-data-models.md](../building-blocks/python-data-models.md)
- [../building-blocks/regex-basics.md](../building-blocks/regex-basics.md)
- [../building-blocks/dataframe-basics.md](../building-blocks/dataframe-basics.md)
- [../building-blocks/testing-basics.md](../building-blocks/testing-basics.md)
- [../building-blocks/tkinter-basics.md](../building-blocks/tkinter-basics.md)

Follow this order: building block -> this file's implementation steps -> tests.

## When This Is Not The Best Fit

- If your requirements are much simpler, prefer a smaller implementation.
- If your input format differs heavily, adapt the pattern rather than copying it exactly.
- If this is a one-time script, consider readability-first code before framework-style structure.
