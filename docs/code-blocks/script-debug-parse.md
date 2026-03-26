# scripts: debug_parse.py and debug_parse2.py

**Files:** `scripts/debug_parse.py`, `scripts/debug_parse2.py`

## What They Are

Two developer utility scripts that step through the section-scanning logic of `parse_payslip()` manually, printing what each line matches (or does not match). They help diagnose why a particular payslip is not being parsed correctly by making the state machine visible.

- **`debug_parse.py`** — highlights significant events (entering/exiting sections, TOTAL, ordinary hours, weekends).
- **`debug_parse2.py`** — more verbose: prints every line with its current section state.

## Code Blocks

### debug_parse.py

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / "src"))

from payslip_tracker import read_text_from_file, extract_currency_values

file_path = Path("input/sample_payslip_25032026.txt")
text = read_text_from_file(file_path)

print("=== Processing Sample Payslip ===\n")
in_salary_section = False
for i, line in enumerate(text.splitlines()):
    line_lower = line.lower()

    if "salary & wages" in line_lower:
        in_salary_section = True
        print(f"Line {i}: Entering salary section")
        continue
    if in_salary_section and ("tax" in line_lower or line_lower.startswith("tax")):
        in_salary_section = False
        print(f"Line {i}: Exiting salary section (line: '{line}')")

    if in_salary_section:
        if line_lower.strip() == "total":
            parts = extract_currency_values(line)
            print(f"Line {i}: FOUND TOTAL LINE!")
            print(f"  Line text: '{line}'")
            print(f"  Extracted values: {parts}")
            if len(parts) >= 2:
                print(f"  gross_this_pay would be: {parts[0]}")
                print(f"  gross_ytd would be: {parts[1]}")
        elif "ordinary hours" in line_lower:
            print(f"Line {i}: Ordinary hours found")
        elif "weekends" in line_lower:
            print(f"Line {i}: Weekends found")
```

### debug_parse2.py

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / "src"))

from payslip_tracker import read_text_from_file, extract_currency_values

file_path = Path("input/sample_payslip_25032026.txt")
text = read_text_from_file(file_path)

print("=== Detailed Parsing Debug ===\n")
in_salary_section = False
for i, line in enumerate(text.splitlines()):
    line_lower = line.lower()

    print(f"Line {i:2d}: in_section={in_salary_section} | '{line}'")

    if "salary & wages" in line_lower:
        in_salary_section = True
        print(f"       -> Entering salary section, continue")
        continue
    if in_salary_section and ("tax" in line_lower or line_lower.startswith("tax")):
        in_salary_section = False
        print(f"       -> Exiting salary section")

    if in_salary_section:
        if line_lower.strip() == "total":
            parts = extract_currency_values(line)
            print(f"       -> TOTAL line detected! values={parts}")
        elif "ordinary hours" in line_lower:
            print(f"       -> Ordinary hours")
        elif "weekends" in line_lower:
            print(f"       -> Weekends")
        elif line.strip():
            print(f"       -> Other line in salary section")
```

## How to Re-Implement

1. Add the `src/` directory to `sys.path` at the top so the script can import from `payslip_tracker`.
2. Use the same section-entering/exiting logic as `parse_payslip()` so the debug output mirrors exactly what the parser sees.
3. Print both the line index and the current section flag so you can correlate output to the raw text.
4. Run from the project root: `python scripts/debug_parse.py`.

### Adapting for a new payslip file

Change the `file_path` variable to point at the file you want to inspect:

```python
file_path = Path("input/my_new_payslip.pdf")
```
