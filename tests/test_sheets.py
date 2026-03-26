from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path.cwd() / "src"))

from payslip_tracker import EXCEL_HEADERS, add_pay_validation_columns, find_missing_weeks, rename_for_excel


def test_rename_for_excel_uses_human_headers() -> None:
    df = pd.DataFrame(
        [
            {
                "file_name": "a.txt",
                "employee": "Jane",
                "pay_date": "2026-03-07",
                "week_start": "2026-03-02",
                "net_this_pay": 100.0,
            }
        ]
    )
    renamed = rename_for_excel(df)
    assert EXCEL_HEADERS["file_name"] in renamed.columns
    assert EXCEL_HEADERS["net_this_pay"] in renamed.columns


def test_find_missing_weeks_detects_gap() -> None:
    df = pd.DataFrame(
        {
            "week_start": [
                "2026-03-02",
                "2026-03-16",
            ]
        }
    )
    missing = find_missing_weeks(df)
    assert missing == ["2026-03-09"]


def test_find_missing_weeks_handles_empty_or_missing_column() -> None:
    assert find_missing_weeks(pd.DataFrame()) == []
    assert find_missing_weeks(pd.DataFrame({"pay_date": ["2026-03-07"]})) == []


def test_add_pay_validation_columns_pass_case() -> None:
    df = pd.DataFrame(
        [
            {
                "ordinary_hours": 8.0,
                "ordinary_rate": 20.0,
                "ordinary_pay_this": 160.0,
                "weekend_hours": 2.0,
                "weekend_rate": 30.0,
                "weekend_pay_this": 60.0,
                "public_holiday_hours": 0.0,
                "public_holiday_rate": 0.0,
                "public_holiday_pay_this": 0.0,
                "gross_this_pay": 220.0,
                "tax_this_pay": 10.0,
                "payg_this_pay": 0.0,
                "net_this_pay": 210.0,
            }
        ]
    )
    out = add_pay_validation_columns(df)
    assert out.loc[0, "ordinary_check"] == "PASS"
    assert out.loc[0, "weekend_check"] == "PASS"
    assert out.loc[0, "gross_check"] == "PASS"
    assert out.loc[0, "net_check"] == "PASS"
    assert out.loc[0, "overall_pay_check"] == "PASS"


def test_add_pay_validation_columns_fail_case() -> None:
    df = pd.DataFrame(
        [
            {
                "ordinary_hours": 8.0,
                "ordinary_rate": 20.0,
                "ordinary_pay_this": 150.0,
                "weekend_hours": 0.0,
                "weekend_rate": 0.0,
                "weekend_pay_this": 0.0,
                "public_holiday_hours": 0.0,
                "public_holiday_rate": 0.0,
                "public_holiday_pay_this": 0.0,
                "gross_this_pay": 150.0,
                "tax_this_pay": 5.0,
                "payg_this_pay": 0.0,
                "net_this_pay": 130.0,
            }
        ]
    )
    out = add_pay_validation_columns(df)
    assert out.loc[0, "ordinary_check"] == "FAIL"
    assert out.loc[0, "net_check"] == "FAIL"
    assert out.loc[0, "overall_pay_check"] == "FAIL"
