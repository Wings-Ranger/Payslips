import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
from PyPDF2 import PdfReader
from dateutil import parser as date_parser


@dataclass
class PayslipRecord:
    file_name: str
    employee: Optional[str]
    pay_date: Optional[str]
    week_start: Optional[str]
    gross: Optional[float]
    net: Optional[float]
    tax: Optional[float]
    ni: Optional[float]
    hours: Optional[float]
    notes: str = ""


def load_config(project_root: Path) -> dict:
    config_path = project_root / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config file: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_text_from_file(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    if file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")

    return ""


def parse_currency(value: str) -> Optional[float]:
    cleaned = re.sub(r"[^0-9.\-]", "", value)
    if cleaned in {"", ".", "-", "-."}:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_float(value: str) -> Optional[float]:
    cleaned = re.sub(r"[^0-9.\-]", "", value)
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def find_value_by_aliases(text: str, aliases: list[str]) -> Optional[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    for line in lines:
        lower = line.lower()
        for alias in aliases:
            a = alias.lower()
            if a in lower:
                parts = re.split(r":|\s{2,}|\t", line, maxsplit=1)
                if len(parts) == 2 and parts[1].strip():
                    return parts[1].strip()

                m = re.search(rf"{re.escape(alias)}\s*[:\-]?\s*(.+)$", line, flags=re.IGNORECASE)
                if m:
                    return m.group(1).strip()

    return None


def find_any_date(text: str) -> Optional[datetime]:
    date_patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",
        r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}\b",
        r"\b[A-Za-z]{3,9}\s+\d{1,2},\s*\d{2,4}\b",
    ]

    for pattern in date_patterns:
        for match in re.findall(pattern, text):
            try:
                return date_parser.parse(match, dayfirst=True, fuzzy=False)
            except Exception:
                continue
    return None


def get_week_start(dt: datetime, start_day: str = "monday") -> datetime:
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    target = weekdays.get(start_day.lower(), 0)
    offset = (dt.weekday() - target) % 7
    return dt - timedelta(days=offset)


def parse_payslip(file_path: Path, text: str, config: dict) -> PayslipRecord:
    aliases = config.get("field_aliases", {})

    employee_raw = find_value_by_aliases(text, aliases.get("employee", []))
    pay_date_raw = find_value_by_aliases(text, aliases.get("pay_date", []))

    gross_raw = find_value_by_aliases(text, aliases.get("gross", []))
    net_raw = find_value_by_aliases(text, aliases.get("net", []))
    tax_raw = find_value_by_aliases(text, aliases.get("tax", []))
    ni_raw = find_value_by_aliases(text, aliases.get("ni", []))
    hours_raw = find_value_by_aliases(text, aliases.get("hours", []))

    pay_dt = None
    if pay_date_raw:
        try:
            pay_dt = date_parser.parse(pay_date_raw, dayfirst=True, fuzzy=True)
        except Exception:
            pay_dt = None
    if pay_dt is None:
        pay_dt = find_any_date(text)

    week_start = None
    pay_date = None
    if pay_dt is not None:
        pay_date = pay_dt.date().isoformat()
        week_start = get_week_start(pay_dt, config.get("week_start_day", "monday")).date().isoformat()

    notes = []
    if pay_dt is None:
        notes.append("Could not determine pay date")
    if gross_raw is None and net_raw is None:
        notes.append("No gross/net value found")

    return PayslipRecord(
        file_name=file_path.name,
        employee=employee_raw,
        pay_date=pay_date,
        week_start=week_start,
        gross=parse_currency(gross_raw) if gross_raw else None,
        net=parse_currency(net_raw) if net_raw else None,
        tax=parse_currency(tax_raw) if tax_raw else None,
        ni=parse_currency(ni_raw) if ni_raw else None,
        hours=parse_float(hours_raw) if hours_raw else None,
        notes="; ".join(notes),
    )


def find_missing_weeks(df: pd.DataFrame) -> list[str]:
    if df.empty or "week_start" not in df.columns:
        return []

    valid = df["week_start"].dropna().unique().tolist()
    if not valid:
        return []

    weeks = sorted(datetime.fromisoformat(x).date() for x in valid)
    start = weeks[0]
    end = weeks[-1]

    observed = set(weeks)
    missing = []

    current = start
    while current <= end:
        if current not in observed:
            missing.append(current.isoformat())
        current += timedelta(days=7)

    return missing


def run() -> None:
    project_root = Path(__file__).resolve().parents[1]
    config = load_config(project_root)

    input_dir = project_root / config.get("input_dir", "input")
    output_dir = project_root / config.get("output_dir", "output")
    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)

    supported = {ext.lower() for ext in config.get("supported_extensions", [".pdf", ".txt"])}
    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in supported]

    if not files:
        print(f"No payslip files found in: {input_dir}")
        print("Add PDF/TXT payslips to input/ and re-run.")
        return

    records: list[PayslipRecord] = []

    for file_path in sorted(files):
        text = read_text_from_file(file_path)
        record = parse_payslip(file_path, text, config)
        records.append(record)

    df = pd.DataFrame([asdict(r) for r in records])
    df = df.sort_values(by=["week_start", "pay_date", "file_name"], na_position="last").reset_index(drop=True)

    missing_weeks = find_missing_weeks(df)

    xlsx_path = output_dir / config.get("output_filename", "payslips.xlsx")
    csv_path = output_dir / "payslips.csv"

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="payslips")
        pd.DataFrame({"missing_week_start": missing_weeks}).to_excel(
            writer, index=False, sheet_name="missing_weeks"
        )

    df.to_csv(csv_path, index=False)

    print(f"Processed {len(df)} payslip file(s)")
    print(f"Spreadsheet: {xlsx_path}")
    print(f"CSV: {csv_path}")

    if missing_weeks:
        print("Missing weekly payslips detected:")
        for w in missing_weeks:
            print(f" - {w}")
    else:
        print("No missing weekly payslips detected in the observed range.")


if __name__ == "__main__":
    run()
