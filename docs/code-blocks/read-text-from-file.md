# read_text_from_file

**File:** `src/payslip_tracker.py`

## What It Is

`read_text_from_file` extracts plain text from a payslip file. It handles two formats:

- **PDF** (`.pdf`) — uses `PyPDF2.PdfReader` to extract text from every page and joins them with newlines.
- **Plain text** (`.txt`) — reads the file directly with UTF-8 encoding, ignoring undecodable bytes.

Any other file extension returns an empty string, which upstream callers treat as an unreadable file.

## Code Block

```python
from pathlib import Path
from PyPDF2 import PdfReader

def read_text_from_file(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    if file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")

    return ""
```

## How to Re-Implement

1. Install `PyPDF2`: `pip install PyPDF2`.
2. Use `.suffix.lower()` so the check is case-insensitive (`.PDF` and `.pdf` both work).
3. For PDFs, call `page.extract_text() or ""` — `extract_text()` returns `None` for scanned/image-only pages, so the `or ""` prevents `None` values in the list.
4. For TXT files, `errors="ignore"` drops bytes that are not valid UTF-8 rather than raising an exception.

### Usage

```python
from pathlib import Path

file_path = Path("input/payslip_march.pdf")
text = read_text_from_file(file_path)

if len(text.strip()) < 50:
    print("Warning: Very little text extracted — file may be a scanned image PDF.")
```

### Extending for Other Formats

To add support for a new format (e.g. `.docx`), append another branch before the final `return ""`:

```python
if file_path.suffix.lower() == ".docx":
    import docx
    doc = docx.Document(str(file_path))
    return "\n".join(p.text for p in doc.paragraphs)
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
