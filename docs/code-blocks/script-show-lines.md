# script: show_lines.py

**File:** `scripts/show_lines.py`

## What It Is

A developer utility that reads a payslip file and prints the first 25 lines with their line numbers. It is the fastest way to inspect the raw text that the parser receives, helping you verify that the payslip layout matches the patterns expected by `parse_payslip()`.

## Code Block

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / "src"))

from payslip_tracker import read_text_from_file

file_path = Path("input/sample_payslip_25032026.txt")
text = read_text_from_file(file_path)

lines = text.splitlines()
print(f"Total lines: {len(lines)}\n")

for i, line in enumerate(lines):
    print(f"Line {i:2d}: '{line}'")
    if i >= 24:
        break
```

## How to Re-Implement

1. Use `read_text_from_file()` from `payslip_tracker` so PDFs and TXT files are both handled identically to how the parser sees them.
2. Wrap each line in single quotes (`'...'`) when printing — this makes leading/trailing whitespace and empty strings immediately visible.
3. Use `{i:2d}` to right-align the line number so columns stay aligned.
4. The `if i >= 24: break` limit keeps output manageable; remove or increase it if you need to inspect more of the file.
5. Run from the project root: `python scripts/show_lines.py`.

### Adapting for a different file

```python
file_path = Path("input/my_payslip.pdf")
```

### Printing all lines

Remove the `break` condition:

```python
for i, line in enumerate(lines):
    print(f"Line {i:2d}: '{line}'")
```
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
