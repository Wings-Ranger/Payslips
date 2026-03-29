from __future__ import annotations

import json
import queue
import threading
import traceback
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from payslip_tracker import ProcessResult, get_project_root, load_config, open_in_default_app, process_payslips


class PayslipTrackerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.project_root = get_project_root()
        self.config = self._load_defaults()
        self.state_path = self.project_root / ".payslip_tracker_ui.json"
        self.ui_state = self._load_ui_state()
        self.queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.last_result: ProcessResult | None = None
        self.worker: threading.Thread | None = None

        self.input_history = self._merge_history("input", self.project_root / self.config.get("input_dir", "input"))
        self.output_history = self._merge_history("output", self.project_root / self.config.get("output_dir", "output"))

        self.input_var = tk.StringVar(value=self.input_history[0])
        self.output_var = tk.StringVar(value=self.output_history[0])
        self.summary_var = tk.StringVar(value="No run yet.")

        self.root.title("Payslip Tracker")
        self.root.geometry("920x720")
        self.root.minsize(820, 620)

        self._configure_style()
        self._build_ui()
        self.root.after(100, self._poll_queue)

    def _load_defaults(self) -> dict:
        try:
            return load_config(self.project_root)
        except Exception:
            return {}

    def _load_ui_state(self) -> dict:
        if not self.state_path.exists():
            return {}
        try:
            with self.state_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception:
            return {}

    def _merge_history(self, key: str, fallback: Path) -> list[str]:
        items = self.ui_state.get(f"recent_{key}_dirs", [])
        cleaned = [str(Path(item).expanduser()) for item in items if item]
        fallback_str = str(fallback)
        if fallback_str not in cleaned:
            cleaned.insert(0, fallback_str)
        return cleaned[:8]

    def _save_ui_state(self) -> None:
        payload = {
            "recent_input_dirs": self.input_history[:8],
            "recent_output_dirs": self.output_history[:8],
        }
        with self.state_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def _remember_directory(self, kind: str, value: str) -> None:
        normalized = str(Path(value).expanduser())
        history_name = f"{kind}_history"
        history = [normalized] + [item for item in getattr(self, history_name) if item != normalized]
        history = history[:8]
        setattr(self, history_name, history)

        combo = self.input_combo if kind == "input" else self.output_combo
        combo.configure(values=history)
        if kind == "input":
            self.input_var.set(normalized)
        else:
            self.output_var.set(normalized)

        self._save_ui_state()

    def _configure_style(self) -> None:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")

        style.configure("Title.TLabel", font=("Segoe UI Semibold", 18))
        style.configure("Section.TLabelframe.Label", font=("Segoe UI Semibold", 11))
        style.configure("Summary.TLabel", font=("Consolas", 10))

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)
        container.rowconfigure(3, weight=1)

        header = ttk.Frame(container)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Payslip Tracker", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Choose folders, run processing, review results, and open the generated spreadsheet.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        controls = ttk.LabelFrame(container, text="Folders and Actions", style="Section.TLabelframe", padding=12)
        controls.grid(row=1, column=0, sticky="ew", pady=(16, 12))
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Input folder").grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.input_combo = ttk.Combobox(controls, textvariable=self.input_var, values=self.input_history)
        self.input_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=(0, 8))
        ttk.Button(controls, text="Browse...", command=self._pick_input_dir).grid(row=0, column=2, sticky="ew", pady=(0, 8))

        ttk.Label(controls, text="Output folder").grid(row=1, column=0, sticky="w")
        self.output_combo = ttk.Combobox(controls, textvariable=self.output_var, values=self.output_history)
        self.output_combo.grid(row=1, column=1, sticky="ew", padx=8)
        ttk.Button(controls, text="Browse...", command=self._pick_output_dir).grid(row=1, column=2, sticky="ew")

        buttons = ttk.Frame(controls)
        buttons.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(14, 0))
        buttons.columnconfigure(3, weight=1)

        self.run_button = ttk.Button(buttons, text="Run", command=self._start_run)
        self.run_button.grid(row=0, column=0, sticky="w")

        self.open_button = ttk.Button(buttons, text="Open Spreadsheet", command=self._open_spreadsheet, state="disabled")
        self.open_button.grid(row=0, column=1, sticky="w", padx=(8, 0))

        ttk.Button(buttons, text="Clear Status", command=self._clear_panels).grid(row=0, column=2, sticky="w", padx=(8, 0))

        self.status_frame = ttk.LabelFrame(container, text="Progress and Status", style="Section.TLabelframe", padding=12)
        self.status_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
        self.status_text = ScrolledText(self.status_frame, height=14, wrap="word", font=("Consolas", 10))
        self.status_text.pack(fill="both", expand=True)
        self.status_text.configure(state="disabled")

        lower = ttk.Frame(container)
        lower.grid(row=3, column=0, sticky="nsew")
        lower.columnconfigure(0, weight=1)
        lower.columnconfigure(1, weight=1)
        lower.rowconfigure(1, weight=1)

        summary_frame = ttk.LabelFrame(lower, text="Summary", style="Section.TLabelframe", padding=12)
        summary_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        ttk.Label(summary_frame, textvariable=self.summary_var, style="Summary.TLabel", justify="left").pack(fill="both", expand=True)

        errors_frame = ttk.LabelFrame(lower, text="Errors", style="Section.TLabelframe", padding=12)
        errors_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        self.error_text = ScrolledText(errors_frame, height=8, wrap="word", font=("Consolas", 10), foreground="#8B0000")
        self.error_text.pack(fill="both", expand=True)
        self.error_text.configure(state="disabled")

        self._append_status("Ready.")

    def _pick_input_dir(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.input_var.get() or str(self.project_root))
        if selected:
            self._remember_directory("input", selected)

    def _pick_output_dir(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.output_var.get() or str(self.project_root))
        if selected:
            self._remember_directory("output", selected)

    def _clear_panels(self) -> None:
        self._set_text(self.status_text, "")
        self._set_text(self.error_text, "")
        self.summary_var.set("No run yet.")

    def _start_run(self) -> None:
        if self.worker is not None and self.worker.is_alive():
            return

        input_dir = Path(self.input_var.get()).expanduser()
        output_dir = Path(self.output_var.get()).expanduser()

        if not input_dir.exists():
            messagebox.showerror("Invalid input folder", f"Input folder does not exist:\n{input_dir}")
            return

        self._remember_directory("input", str(input_dir))
        self._remember_directory("output", str(output_dir))

        self.last_result = None
        self.open_button.configure(state="disabled")
        self.run_button.configure(state="disabled")
        self._set_text(self.error_text, "")
        self._set_text(self.status_text, "")
        self.summary_var.set("Running...")
        self._append_status("Starting payslip processing...")

        self.worker = threading.Thread(
            target=self._run_worker,
            args=(input_dir, output_dir),
            daemon=True,
        )
        self.worker.start()

    def _run_worker(self, input_dir: Path, output_dir: Path) -> None:
        try:
            result = process_payslips(
                project_root=self.project_root,
                input_dir=input_dir,
                output_dir=output_dir,
                open_spreadsheet=False,
                status_callback=lambda message: self.queue.put(("status", message)),
            )
        except Exception as exc:
            self.queue.put(("error", self._format_error(exc)))
            return

        self.queue.put(("result", result))

    def _format_error(self, exc: Exception) -> str:
        if isinstance(exc, FileNotFoundError):
            return str(exc)
        return f"{type(exc).__name__}: {exc}\n\n{traceback.format_exc()}"

    def _poll_queue(self) -> None:
        while True:
            try:
                event_type, payload = self.queue.get_nowait()
            except queue.Empty:
                break

            if event_type == "status":
                self._append_status(str(payload))
            elif event_type == "error":
                self._set_text(self.error_text, str(payload))
                self.summary_var.set("Run failed.")
                self._append_status("Processing failed.")
                self.run_button.configure(state="normal")
            elif event_type == "result":
                result = payload
                if isinstance(result, ProcessResult):
                    self.last_result = result
                    self._remember_directory("input", str(result.input_dir))
                    self._remember_directory("output", str(result.output_dir))
                    self.summary_var.set(self._build_summary(result))
                    self._append_status("Run complete.")
                    self.open_button.configure(state="normal")
                    self.run_button.configure(state="normal")

        self.root.after(100, self._poll_queue)

    def _build_summary(self, result: ProcessResult) -> str:
        missing_weeks = ", ".join(result.missing_weeks) if result.missing_weeks else "None"
        return (
            f"Files found: {result.files_found}\n"
            f"Processed: {result.processed_count}\n"
            f"Skipped: {result.skipped_count}\n"
            f"Schema issues: {result.schema_invalid_count}\n"
            f"Missing weeks: {missing_weeks}\n\n"
            f"Spreadsheet: {result.xlsx_path}\n"
            f"CSV: {result.csv_path}"
        )

    def _open_spreadsheet(self) -> None:
        if self.last_result is None:
            return
        try:
            open_in_default_app(self.last_result.xlsx_path)
        except Exception as exc:
            self._set_text(self.error_text, self._format_error(exc))
            return
        self._append_status(f"Opened spreadsheet: {self.last_result.xlsx_path}")

    def _append_status(self, message: str) -> None:
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")

    def _set_text(self, widget: ScrolledText, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        if value:
            widget.insert("1.0", value)
        widget.configure(state="disabled")


def main() -> None:
    root = tk.Tk()
    app = PayslipTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()