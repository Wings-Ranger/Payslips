# ui_theme.json

**File:** `ui_theme.json`

## What It Is

`ui_theme.json` is the beginner-editable theme file for the desktop GUI. It controls how the app looks without requiring changes to Python code.

The GUI reads this file at startup and can reload it live through the **Reload Theme** button.

For a field-by-field explanation linked to the exact code lines where each setting is used, see [../theme-guide/README.md](../theme-guide/README.md).

## What It Controls

- window title and size
- font families, sizes, and weights
- app, panel, text, button, and error colors
- layout spacing and padding
- button labels and section titles

## Current Structure

```json
{
  "window": {
    "title": "Payslip Tracker",
    "geometry": "980x760",
    "min_width": 860,
    "min_height": 640
  },
  "fonts": {
    "title": ["Georgia", 22, "bold"],
    "subtitle": ["Segoe UI", 10],
    "section": ["Segoe UI Semibold", 11],
    "body": ["Segoe UI", 10],
    "button": ["Segoe UI Semibold", 10],
    "mono": ["Consolas", 10],
    "summary": ["Consolas", 10]
  },
  "colors": {
    "app_bg": "#f4efe6",
    "panel_bg": "#fffaf2",
    "panel_border": "#d8c3a3",
    "text": "#2f2618",
    "muted_text": "#75654a",
    "accent": "#1f6f5f",
    "accent_hover": "#18584b",
    "accent_text": "#ffffff"
  },
  "spacing": {
    "outer_padding": 18,
    "panel_padding": 14,
    "section_gap": 14
  },
  "labels": {
    "title": "Payslip Tracker",
    "run_button": "Run",
    "reload_button": "Reload Theme",
    "edit_button": "Open Theme File"
  }
}
```

## How to Re-Implement

1. Keep the theme file in JSON so non-programmers can edit it in any text editor.
2. Group appearance settings into simple sections like `window`, `fonts`, `colors`, `spacing`, and `labels`.
3. Merge the loaded JSON over safe defaults so partial edits do not break the app.
4. Add a live reload action so users can see changes immediately.

## Beginner Editing Workflow

1. Open `ui_theme.json`.
2. Change a value such as `colors.accent` or `fonts.title`.
3. Save the file.
4. Click **Reload Theme** in the app.

## Good First Edits

- change `colors.app_bg` for the page background
- change `colors.accent` for the main button color
- change `fonts.title` for the app heading look
- change `labels.title` if you want a different app title
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
