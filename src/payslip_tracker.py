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
    pay_period: Optional[str]
    week_start: Optional[str]
    # Ordinary hours
    ordinary_hours: Optional[float] = None
    ordinary_rate: Optional[float] = None
    ordinary_pay_this: Optional[float] = None
    ordinary_pay_ytd: Optional[float] = None
    # Weekend hours
    weekend_hours: Optional[float] = None
    weekend_rate: Optional[float] = None
    weekend_pay_this: Optional[float] = None
    weekend_pay_ytd: Optional[float] = None
    # Public holiday hours
    public_holiday_hours: Optional[float] = None
    public_holiday_rate: Optional[float] = None
    public_holiday_pay_this: Optional[float] = None
    public_holiday_pay_ytd: Optional[float] = None
    # Totals
    gross_this_pay: Optional[float] = None
    gross_ytd: Optional[float] = None
    tax_this_pay: Optional[float] = None
    tax_ytd: Optional[float] = None
    payg_this_pay: Optional[float] = None
    payg_ytd: Optional[float] = None
    net_this_pay: Optional[float] = None
    net_ytd: Optional[float] = None
    total_hours_this_pay: Optional[float] = None
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
    # Extract employee name - first non-empty line
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    employee_raw = lines[0] if lines else None

    # Normalize text for regex (join lines, preserve structure)
    text_normalized = text.replace("\n", " ")
    
    # Extract pay period and payment date
    pay_date = None
    pay_period = None
    m = re.search(r"pay period:\s*(\d{1,2}/\d{1,2}/\d{4})\s*-\s*(\d{1,2}/\d{1,2}/\d{4})", text_normalized, re.IGNORECASE)
    if m:
        pay_period = f"{m.group(1)} - {m.group(2)}"
    
    m = re.search(r"payment date:\s*(\d{1,2}/\d{1,2}/\d{4})", text_normalized, re.IGNORECASE)
    if m:
        pay_date_str = m.group(1)
        try:
            pay_date_obj = date_parser.parse(pay_date_str, dayfirst=True)
            pay_date = pay_date_obj.date().isoformat()
        except Exception:
            pass

    # Initialize field values
    ordinary_hours = None
    ordinary_rate = None
    ordinary_pay_this = None
    ordinary_pay_ytd = None
    weekend_hours = None
    weekend_rate = None
    weekend_pay_this = None
    weekend_pay_ytd = None
    public_holiday_hours = None
    public_holiday_rate = None
    public_holiday_pay_this = None
    public_holiday_pay_ytd = None
    gross_this_pay = None
    gross_ytd = None
    payg_this_pay = None
    payg_ytd = None
    tax_this_pay = None
    tax_ytd = None
    net_this_pay = None
    net_ytd = None

    # Parse salary & wages section line by line
    in_salary_section = False
    for line in text.splitlines():
        line_lower = line.lower()
        
        if "salary & wages" in line_lower:
            in_salary_section = True
            continue
        if in_salary_section and ("tax" in line_lower or line_lower.startswith("tax")):
            in_salary_section = False
        
        if in_salary_section:
            # Extract ordinary hours line: "Ordinary Hours 7.5000 $16.7100 $125.32 $7,337.90"
            if "ordinary hours" in line_lower:
                parts = re.findall(r"[\d.]+", line)
                if len(parts) >= 4:
                    try:
                        ordinary_hours = float(parts[0])
                        ordinary_rate = float(parts[1])
                        ordinary_pay_this = float(parts[2])
                        ordinary_pay_ytd = float(parts[3])
                    except (ValueError, IndexError):
                        pass
            
            # Extract weekend hours line: "Weekends Sat/Sun 5.0000 $21.8000 $109.00 $4,352.33"
            elif "weekends" in line_lower and ("sat" in line_lower or "sun" in line_lower):
                parts = re.findall(r"[\d.]+", line)
                if len(parts) >= 4:
                    try:
                        weekend_hours = float(parts[0])
                        weekend_rate = float(parts[1])
                        weekend_pay_this = float(parts[2])
                        weekend_pay_ytd = float(parts[3])
                    except (ValueError, IndexError):
                        pass
            
            # Extract public holiday line
            elif "public" in line_lower and "holiday" in line_lower:
                parts = re.findall(r"[\d.]+", line)
                if len(parts) >= 4:
                    try:
                        public_holiday_hours = float(parts[0])
                        public_holiday_rate = float(parts[1])
                        public_holiday_pay_this = float(parts[2])
                        public_holiday_pay_ytd = float(parts[3])
                    except (ValueError, IndexError):
                        pass
            
            # Extract TOTAL line for gross: "TOTAL $234.32 $12,235.23"
            elif line_lower.strip() == "total":
                parts = re.findall(r"[\d.]+", line)
                if len(parts) >= 2:
                    try:
                        gross_this_pay = float(parts[0])
                        gross_ytd = float(parts[1])
                    except (ValueError, IndexError):
                        pass

    # Parse TAX section
    in_tax_section = False
    for line in text.splitlines():
        line_lower = line.lower()
        
        if line_lower.startswith("tax"):
            in_tax_section = True
            continue
        if in_tax_section and "payment details" in line_lower:
            in_tax_section = False
        
        if in_tax_section:
            # PAYG line: "PAYG $0.00 $264.00"
            if "payg" in line_lower:
                parts = re.findall(r"[\d.]+", line)
                if len(parts) >= 2:
                    try:
                        payg_this_pay = float(parts[0])
                        payg_ytd = float(parts[1])
                    except (ValueError, IndexError):
                        pass
            
            # TAX or other tax types
            elif "tax" in line_lower and "payg" not in line_lower and line_lower.strip() != "tax":
                parts = re.findall(r"[\d.]+", line)
                if len(parts) >= 2:
                    try:
                        tax_this_pay = float(parts[0])
                        tax_ytd = float(parts[1])
                    except (ValueError, IndexError):
                        pass
            
            # TOTAL under tax: "TOTAL $0.00 $264.00"
            elif line_lower.strip() == "total":
                parts = re.findall(r"[\d.]+", line)
                if len(parts) >= 2 and tax_this_pay is None:  # Only set if not already set
                    try:
                        tax_this_pay = float(parts[0])
                        tax_ytd = float(parts[1])
                    except (ValueError, IndexError):
                        pass

    # Extract Net Pay: "Net Pay: $234.32"
    m = re.search(r"net pay:\s*\$?([\d.]+)", text_normalized, re.IGNORECASE)
    if m:
        try:
            net_this_pay = float(m.group(1))
        except ValueError:
            pass

    # Total hours this pay = ordinary + weekend + public holiday
    total_hours_this_pay = 0.0
    if ordinary_hours:
        total_hours_this_pay += ordinary_hours
    if weekend_hours:
        total_hours_this_pay += weekend_hours
    if public_holiday_hours:
        total_hours_this_pay += public_holiday_hours
    total_hours_this_pay = total_hours_this_pay if total_hours_this_pay > 0 else None

    # Calculate week_start from pay_date
    week_start = None
    if pay_date:
        try:
            pay_date_obj = datetime.fromisoformat(pay_date)
            week_start = get_week_start(pay_date_obj, config.get("week_start_day", "monday")).date().isoformat()
        except Exception:
            pass

    notes = []
    if pay_date is None:
        notes.append("Could not determine pay date")

    return PayslipRecord(
        file_name=file_path.name,
        employee=employee_raw,
        pay_date=pay_date,
        pay_period=pay_period,
        week_start=week_start,
        ordinary_hours=ordinary_hours,
        ordinary_rate=ordinary_rate,
        ordinary_pay_this=ordinary_pay_this,
        ordinary_pay_ytd=ordinary_pay_ytd,
        weekend_hours=weekend_hours,
        weekend_rate=weekend_rate,
        weekend_pay_this=weekend_pay_this,
        weekend_pay_ytd=weekend_pay_ytd,
        public_holiday_hours=public_holiday_hours,
        public_holiday_rate=public_holiday_rate,
        public_holiday_pay_this=public_holiday_pay_this,
        public_holiday_pay_ytd=public_holiday_pay_ytd,
        gross_this_pay=gross_this_pay,
        gross_ytd=gross_ytd,
        tax_this_pay=tax_this_pay,
        tax_ytd=tax_ytd,
        payg_this_pay=payg_this_pay,
        payg_ytd=payg_ytd,
        net_this_pay=net_this_pay,
        net_ytd=net_ytd,
        total_hours_this_pay=total_hours_this_pay,
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

    # Try to write Excel file; if locked, use timestamped backup
    try:
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="payslips")
            pd.DataFrame({"missing_week_start": missing_weeks}).to_excel(
                writer, index=False, sheet_name="missing_weeks"
            )
    except PermissionError:
        from datetime import datetime as dt
        backup_name = f"payslips_{dt.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        xlsx_path = output_dir / backup_name
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="payslips")
            pd.DataFrame({"missing_week_start": missing_weeks}).to_excel(
                writer, index=False, sheet_name="missing_weeks"
            )
        print(f"(Note: Main file was locked, saved as: {backup_name})")

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
