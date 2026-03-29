# Theme Guide

This guide explains what each part of `ui_theme.json` changes in the app and links to the exact code lines where the theme values are applied.

Use this when you want to restyle the frontend without editing Python code.

## Important Rule

`ui_theme.json` must stay valid JSON.

- Do not add `// comments`
- Do not add trailing commas
- Keep strings in double quotes

## Theme File

- Theme file: [ui_theme.json](../../ui_theme.json)
- Theme loader: [src/payslip_gui.py](../../src/payslip_gui.py#L126)
- Theme application entry point: [src/payslip_gui.py](../../src/payslip_gui.py#L353)

## Window

- `window.title`: changes the app window title shown at the top of the window. Used in [src/payslip_gui.py](../../src/payslip_gui.py#L109) and [src/payslip_gui.py](../../src/payslip_gui.py#L356).
- `window.geometry`: changes the startup size of the window. Used in [src/payslip_gui.py](../../src/payslip_gui.py#L110) and [src/payslip_gui.py](../../src/payslip_gui.py#L359).
- `window.min_width` and `window.min_height`: change the minimum allowed resize size. Used in [src/payslip_gui.py](../../src/payslip_gui.py#L111) and [src/payslip_gui.py](../../src/payslip_gui.py#L357).

## Fonts

- All `fonts.*` values are resolved through [the font helper](../../src/payslip_gui.py#L182).
- `fonts.title`: changes the large heading font. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L200).
- `fonts.subtitle`: changes the smaller helper text under the title. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L206) and [src/payslip_gui.py](../../src/payslip_gui.py#L212).
- `fonts.section`: changes panel heading fonts like “Folders and Actions” and “Summary”. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L226).
- `fonts.body`: changes normal label text. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L195).
- `fonts.button`: changes button text styling. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L239) and [src/payslip_gui.py](../../src/payslip_gui.py#L253).
- `fonts.mono`: changes the status log and error panel font. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L390) and [src/payslip_gui.py](../../src/payslip_gui.py#L403).
- `fonts.summary`: changes the summary panel content font. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L233).

## Colors

- Main styling setup happens in [the style configuration block](../../src/payslip_gui.py#L186).
- `colors.app_bg`: changes the overall page background. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L191), [src/payslip_gui.py](../../src/payslip_gui.py#L194), [src/payslip_gui.py](../../src/payslip_gui.py#L200), [src/payslip_gui.py](../../src/payslip_gui.py#L206), [src/payslip_gui.py](../../src/payslip_gui.py#L212), and [src/payslip_gui.py](../../src/payslip_gui.py#L355).
- `colors.panel_bg`: changes the background inside the card sections. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L218) and [src/payslip_gui.py](../../src/payslip_gui.py#L225).
- `colors.panel_border`: changes the border around cards and text panels. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L219), [src/payslip_gui.py](../../src/payslip_gui.py#L258), [src/payslip_gui.py](../../src/payslip_gui.py#L397), [src/payslip_gui.py](../../src/payslip_gui.py#L410).
- `colors.text`: changes main text color for labels and headings. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L195), [src/payslip_gui.py](../../src/payslip_gui.py#L201), [src/payslip_gui.py](../../src/payslip_gui.py#L226).
- `colors.muted_text`: changes subtitle/helper text color and disabled primary button text. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L207), [src/payslip_gui.py](../../src/payslip_gui.py#L213), [src/payslip_gui.py](../../src/payslip_gui.py#L247).
- `colors.accent`: changes the main action color and focus highlight. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L237), [src/payslip_gui.py](../../src/payslip_gui.py#L398), and [src/payslip_gui.py](../../src/payslip_gui.py#L411).
- `colors.accent_hover`: changes the hover state of the main button. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L246).
- `colors.accent_text`: changes text color on the main button. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L238).
- `colors.secondary_bg`: changes the background of secondary buttons and disabled primary buttons. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L246) and [src/payslip_gui.py](../../src/payslip_gui.py#L251).
- `colors.secondary_text`: changes text color on secondary buttons. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L252).
- `colors.input_bg`: changes the folder selector background. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L261), [src/payslip_gui.py](../../src/payslip_gui.py#L262), and [src/payslip_gui.py](../../src/payslip_gui.py#L267).
- `colors.input_fg`: changes the folder selector text color. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L263).
- `colors.status_bg` and `colors.status_fg`: change the progress/status log colors. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L391), [src/payslip_gui.py](../../src/payslip_gui.py#L392), [src/payslip_gui.py](../../src/payslip_gui.py#L393).
- `colors.summary_bg` and `colors.summary_fg`: change the summary panel colors. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L231) and [src/payslip_gui.py](../../src/payslip_gui.py#L232).
- `colors.error_bg` and `colors.error_fg`: change the error panel colors. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L404), [src/payslip_gui.py](../../src/payslip_gui.py#L405), [src/payslip_gui.py](../../src/payslip_gui.py#L406).

## Spacing

- `spacing.outer_padding`: changes the space around the whole app. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L273) and [src/payslip_gui.py](../../src/payslip_gui.py#L363).
- `spacing.panel_padding`: changes internal padding inside the major panels. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L295), [src/payslip_gui.py](../../src/payslip_gui.py#L324), [src/payslip_gui.py](../../src/payslip_gui.py#L336), [src/payslip_gui.py](../../src/payslip_gui.py#L341), and refreshed in [src/payslip_gui.py](../../src/payslip_gui.py#L364).
- `spacing.section_gap`: changes vertical space between major sections. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L296).

## Labels

- `labels.title`: main heading text. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L369).
- `labels.subtitle`: helper text under the title. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L370).
- `labels.theme_hint`: helper text that explains live theming. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L371).
- `labels.controls_title`: panel title for folder/action controls. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L364).
- `labels.status_title`: status panel title. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L365).
- `labels.summary_title`: summary panel title. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L366).
- `labels.errors_title`: errors panel title. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L367).
- `labels.input_label` and `labels.output_label`: folder field labels. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L372) and [src/payslip_gui.py](../../src/payslip_gui.py#L373).
- `labels.run_button`, `labels.open_button`, `labels.clear_button`, `labels.reload_button`, `labels.edit_button`: button text. Applied in [src/payslip_gui.py](../../src/payslip_gui.py#L374), [src/payslip_gui.py](../../src/payslip_gui.py#L375), [src/payslip_gui.py](../../src/payslip_gui.py#L376), [src/payslip_gui.py](../../src/payslip_gui.py#L377), and [src/payslip_gui.py](../../src/payslip_gui.py#L378).
- `labels.ready`, `labels.no_run`, `labels.running`: default idle/running text values. Used in [src/payslip_gui.py](../../src/payslip_gui.py#L106), [src/payslip_gui.py](../../src/payslip_gui.py#L383), [src/payslip_gui.py](../../src/payslip_gui.py#L451), and [src/payslip_gui.py](../../src/payslip_gui.py#L472).

## Easiest Things To Change First

1. Change `colors.accent` to restyle the main button.
2. Change `colors.app_bg` and `colors.panel_bg` to shift the whole mood.
3. Change `fonts.title` to make the app feel more formal, modern, or playful.
4. Change `labels.title` and `labels.subtitle` to customize the app wording.
