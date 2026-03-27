# Schema Validation

**File:** `src/payslip_tracker.py`

## What It Is

Three closely-related items work together to validate that parsed payslip records contain the minimum required data before they are written to the report:

| Name | Type | Role |
|------|------|------|
| `REQUIRED_SCHEMA_FIELDS` | `list[str]` | Declares which fields are mandatory |
| `validate_record_schema` | function | Returns the list of missing/empty required fields |
| `append_validation_notes` | function | Appends a `SCHEMA_INVALID` message to the record's `notes` field |

A record with missing required fields is still written to the report — the failure is surfaced as a note rather than silently dropped, keeping the data visible for manual review.

## Code Block

```python
from dataclasses import asdict

REQUIRED_SCHEMA_FIELDS = [
    "file_name",
    "employee",
    "pay_date",
    "week_start",
    "net_this_pay",
]


def validate_record_schema(record: PayslipRecord) -> list[str]:
    """Return list of missing required fields for a parsed record."""
    data = asdict(record)
    missing: list[str] = []
    for field_name in REQUIRED_SCHEMA_FIELDS:
        value = data.get(field_name)
        if value is None:
            missing.append(field_name)
            continue
        if isinstance(value, str) and not value.strip():
            missing.append(field_name)
    return missing


def append_validation_notes(record: PayslipRecord) -> PayslipRecord:
    """Add schema validation errors into record notes for downstream visibility."""
    missing = validate_record_schema(record)
    if not missing:
        return record

    schema_note = f"SCHEMA_INVALID: missing required fields: {', '.join(missing)}"
    if schema_note in (record.notes or ""):
        return record   # idempotent — don't duplicate

    if record.notes:
        record.notes = f"{record.notes}; {schema_note}"
    else:
        record.notes = schema_note
    return record
```

## How to Re-Implement

1. Define `REQUIRED_SCHEMA_FIELDS` as a module-level list so it can be updated without changing function signatures.
2. `validate_record_schema` uses `asdict()` to avoid coupling to the dataclass field API directly — it works with any dataclass.
3. Check for both `None` and blank strings (a field may be parsed as `""` rather than `None`).
4. `append_validation_notes` is idempotent: it checks whether the note is already present before appending, so calling it multiple times is safe.
5. The function mutates `record.notes` in place and returns the same record — callers do not need to handle a return value separately but should still assign it for clarity.

### Usage

```python
record = parse_payslip(file_path, text, config)
record = append_validation_notes(record)

if "SCHEMA_INVALID" in record.notes:
    print(f"Warning: {record.file_name} is missing required fields.")
```

### Extending the required fields list

`net_this_pay` is already required by default. To require additional fields (e.g. `pay_period`), simply add the field name to the list:

```python
REQUIRED_SCHEMA_FIELDS = [
    "file_name",
    "employee",
    "pay_date",
    "week_start",
    "net_this_pay",
    "pay_period",   # added
]
```
