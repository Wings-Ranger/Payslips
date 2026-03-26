from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path.cwd() / "src"))

from payslip_tracker import EXCEL_HEADERS, find_missing_weeks, rename_for_excel


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
