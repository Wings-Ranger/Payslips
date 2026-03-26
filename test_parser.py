from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd() / "src"))

from payslip_tracker import append_validation_notes, parse_payslip


def _config() -> dict:
    return {"week_start_day": "monday"}


def test_parse_scanned_text_sets_skip_note() -> None:
    record = parse_payslip(Path("scan.pdf"), "tiny", _config())
    assert record.employee is None
    assert record.pay_date is None
    assert "SCANNED" in record.notes.upper() or "SKIPPED" in record.notes.upper()


def test_parse_missing_payment_date_adds_note() -> None:
    text = """
Jane Citizen
Pay Period: 01/03/2026 - 07/03/2026
Salary & Wages
Ordinary Hours 7.5000 16.7100 125.32 7337.90
TOTAL 125.32 7337.90
Tax
TOTAL 0.00 0.00
Net Pay: 125.32
"""
    record = parse_payslip(Path("missing-date.txt"), text, _config())
    assert record.pay_date is None
    assert "Could not determine pay date" in record.notes


def test_schema_validation_flags_missing_required_fields() -> None:
    text = """
Jane Citizen
Pay Period: 01/03/2026 - 07/03/2026
Payment Date: 07/03/2026
Salary & Wages
Ordinary Hours 7.5000 16.7100 125.32 7337.90
TOTAL 125.32 7337.90
Tax
TOTAL 0.00 0.00
"""
    record = parse_payslip(Path("missing-net.txt"), text, _config())
    validated = append_validation_notes(record)
    assert validated.net_this_pay is None
    assert "SCHEMA_INVALID" in validated.notes
    assert "net_this_pay" in validated.notes


def test_total_hours_sums_all_hour_buckets() -> None:
    text = """
Jane Citizen
Pay Period: 01/03/2026 - 07/03/2026
Payment Date: 07/03/2026
Salary & Wages
Ordinary Hours 7.5000 16.7100 125.32 7337.90
Weekends Sat/Sun 5.0000 21.8000 109.00 4352.33
Public Holiday 2.0000 30.0000 60.00 120.00
TOTAL 294.32 11810.23
Tax
TOTAL 0.00 0.00
Net Pay: 294.32
"""
    record = parse_payslip(Path("hours.txt"), text, _config())
    assert record.total_hours_this_pay == 14.5
