# format_excel_output

**File:** `src/payslip_tracker.py`

## What It Is

`format_excel_output` applies visual formatting to the Excel workbook after it has been written by pandas. It uses `openpyxl` to:

- Apply colour-coded section fills to columns (ordinary = blue, weekend = yellow, public holiday = green, gross = orange, tax = red).
- Bold and colour the header row (white text on blue background).
- Add thin borders to every cell.
- Set appropriate column widths.
- Apply number formats: currency (`$#,##0.00`), numeric (`0.00`), date (`yyyy-mm-dd`).
- Freeze the header row.
- Style the `missing_weeks` sheet with black-filled empty cells.

## Code Block

```python
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def format_excel_output(xlsx_path: Path) -> None:
    """Apply formatting to Excel output for readability."""
    wb = load_workbook(str(xlsx_path))
    ws = wb.active

    # --- Style definitions ---
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)

    ordinary_fill     = PatternFill(start_color="E7E6FF", end_color="E7E6FF", fill_type="solid")
    weekend_fill      = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    public_fill       = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    gross_fill        = PatternFill(start_color="FDB766", end_color="FDB766", fill_type="solid")
    tax_fill          = PatternFill(start_color="FFB3B3", end_color="FFB3B3", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"),  bottom=Side(style="thin"),
    )

    # --- Column widths ---
    col_widths = {
        "A": 20, "B": 18, "C": 12, "D": 18, "E": 12,
        "F": 15, "G": 13, "H": 16, "I": 15,
        "J": 14, "K": 13, "L": 16, "M": 15,
        "N": 16, "O": 15, "P": 18, "Q": 17,
        "R": 15, "S": 12, "T": 14, "U": 11,
        "V": 15, "W": 12, "X": 14, "Y": 11,
        "Z": 18, "AA": 15,
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # --- Column-to-fill mapping ---
    color_map = {
        "F": ordinary_fill, "G": ordinary_fill, "H": ordinary_fill, "I": ordinary_fill,
        "J": weekend_fill,  "K": weekend_fill,  "L": weekend_fill,  "M": weekend_fill,
        "N": public_fill,   "O": public_fill,   "P": public_fill,   "Q": public_fill,
        "R": gross_fill,    "S": gross_fill,
        "T": tax_fill,      "U": tax_fill,      "V": tax_fill,      "W": tax_fill,
    }

    # --- Header row ---
    for col_num, cell in enumerate(ws[1], 1):
        col_letter = get_column_letter(col_num)
        cell.font      = header_font
        cell.fill      = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border    = thin_border

    # --- Data rows ---
    currency_cols = {"H", "I", "L", "M", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"}
    numeric_cols  = {"F", "G", "J", "K", "N", "O", "Z"}
    date_cols     = {"C", "E"}

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for col_num, cell in enumerate(row, 1):
            col_letter = get_column_letter(col_num)
            if col_letter in color_map:
                cell.fill = color_map[col_letter]
            cell.border = thin_border
            if col_letter in currency_cols:
                cell.number_format = "$#,##0.00"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_letter in numeric_cols:
                cell.number_format = "0.00"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_letter in date_cols:
                cell.number_format = "yyyy-mm-dd"
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_letter == "AA":
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    ws.freeze_panes = "A2"

    # --- missing_weeks sheet ---
    if "missing_weeks" in wb.sheetnames:
        mw = wb["missing_weeks"]
        mw.column_dimensions["A"].width = 16
        black_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
        for cell in mw[1]:
            cell.font      = header_font
            cell.fill      = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border    = thin_border
        for row in mw.iter_rows(min_row=2, max_row=mw.max_row):
            for cell in row:
                if cell.value is None or str(cell.value).strip() == "":
                    cell.fill = black_fill
                else:
                    cell.number_format = "yyyy-mm-dd"
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = thin_border
        mw.freeze_panes = "A2"

    wb.save(str(xlsx_path))
```

## Colour Reference

| Column range | Section | Hex colour |
|---|---|---|
| F–I | Ordinary hours | `#E7E6FF` (light blue) |
| J–M | Weekend hours | `#FFF2CC` (light yellow) |
| N–Q | Public holiday | `#E2EFDA` (light green) |
| R–S | Gross pay | `#FDB766` (orange) |
| T–W | Tax / PAYG | `#FFB3B3` (light red) |
| Header row | All | `#4472C4` (blue), white bold text |

## How to Re-Implement

1. Install `openpyxl`: `pip install openpyxl`.
2. Call `load_workbook(path)` **after** the file has been written by pandas — openpyxl cannot safely write and format in a single pass with pandas' `ExcelWriter`.
3. Build `PatternFill`, `Font`, `Border`, and `Alignment` objects once and reuse them across rows.
4. Use `get_column_letter(col_num)` to convert 1-based column numbers to letters for the color map lookup.
5. Save with `wb.save(path)` at the end.

### Usage

```python
from pathlib import Path

xlsx_path = Path("output/payslips.xlsx")

# Write with pandas first
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="payslips")

# Then apply formatting
format_excel_output(xlsx_path)
```
