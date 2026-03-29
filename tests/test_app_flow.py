from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path.cwd() / "src"))

from payslip_tracker import process_payslips


VALID_PAYSLIP = """
Jane Citizen
Pay Period: 01/03/2026 - 07/03/2026
Payment Date: 07/03/2026
Salary & Wages
Ordinary Hours 7.5000 16.7100 125.32 7337.90
TOTAL 125.32 7337.90
Tax
TOTAL 0.00 0.00
Net Pay: 125.32
"""


def test_process_payslips_writes_outputs_and_summary_counts() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        input_dir = temp_root / "input"
        output_dir = temp_root / "output"
        input_dir.mkdir()

        (input_dir / "valid.txt").write_text(VALID_PAYSLIP, encoding="utf-8")
        (input_dir / "scan.txt").write_text("tiny", encoding="utf-8")

        result = process_payslips(
            project_root=Path.cwd(),
            input_dir=input_dir,
            output_dir=output_dir,
            open_spreadsheet=False,
        )

        assert result.files_found == 2
        assert result.processed_count == 2
        assert result.skipped_count == 1
        assert result.schema_invalid_count == 1
        assert result.xlsx_path.exists()
        assert result.csv_path.exists()
        assert result.missing_weeks == []


def test_process_payslips_raises_when_no_supported_files_exist() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        input_dir = temp_root / "input"
        output_dir = temp_root / "output"
        input_dir.mkdir()

        try:
            process_payslips(
                project_root=Path.cwd(),
                input_dir=input_dir,
                output_dir=output_dir,
                open_spreadsheet=False,
            )
        except FileNotFoundError as exc:
            assert "No payslip files found" in str(exc)
        else:
            raise AssertionError("Expected FileNotFoundError for empty input folder")