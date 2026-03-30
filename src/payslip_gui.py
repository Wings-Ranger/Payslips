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

try:
    from tkinterdnd2 import DND_FILES, DND_TEXT
    HAS_DND = True
except ImportError:
    HAS_DND = False


DEFAULT_THEME = {
    "window": {
        "title": "Payslip Tracker",
        "geometry": "1020x800",
        "min_width": 900,
        "min_height": 700,
    },
    "fonts": {
        "title": ["Segoe UI", 28, "bold"],
        "subtitle": ["Segoe UI", 11],
        "section": ["Segoe UI Semibold", 12],
        "body": ["Segoe UI", 10],
        "button": ["Segoe UI Semibold", 11],
        "mono": ["Consolas", 9],
        "summary": ["Consolas", 9],
    },
    "colors": {
        "app_bg": "#f5f7fa",
        "panel_bg": "#ffffff",
        "panel_border": "#e0e6ed",
        "text": "#1a202c",
        "muted_text": "#64748b",
        "accent": "#3b82f6",
        "accent_hover": "#2563eb",
        "accent_text": "#ffffff",
        "secondary_bg": "#f1f5f9",
        "secondary_text": "#475569",
        "input_bg": "#ffffff",
        "input_fg": "#1a202c",
        "status_bg": "#f8fafc",
        "status_fg": "#1a202c",
        "summary_bg": "#eff6ff",
        "summary_fg": "#1a202c",
        "error_bg": "#fef2f2",
        "error_fg": "#991b1b",
        "drop_zone_bg": "#dbeafe",
        "drop_zone_border": "#3b82f6",
    },
    "spacing": {
        "outer_padding": 20,
        "panel_padding": 16,
        "section_gap": 16,
    },
    "labels": {
        "title": "📊 Payslip Tracker",
        "subtitle": "Process payslips with drag-and-drop support. Edit ui_theme.json for custom styling.",
        "theme_hint": "Customize the theme and click Reload",
        "controls_title": "📁 Folders & Actions",
        "status_title": "⚙️ Processing Status",
        "summary_title": "📈 Summary",
        "errors_title": "⚠️ Errors",
        "input_label": "Drop files here or select input folder",
        "output_label": "Output folder",
        "run_button": "▶ Process Payslips",
        "open_button": "📄 View Results",
        "clear_button": "🗑️ Clear",
        "reload_button": "🔄 Reload Theme",
        "edit_button": "✏️ Edit Theme",
        "ready": "Ready.",
        "no_run": "No run yet.",
        "running": "Processing...",
    },
}


def _deep_merge(base: dict, overrides: dict) -> dict:
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


class PayslipTrackerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.project_root = get_project_root()
        self.config = self._load_defaults()
        self.state_path = self.project_root / ".payslip_tracker_ui.json"
        self.ui_state = self._load_ui_state()
        self.theme_path = self._resolve_theme_path()
        self.theme = self._load_theme()
        self.queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.last_result: ProcessResult | None = None
        self.worker: threading.Thread | None = None
        self.style = ttk.Style(self.root)
        self.drag_active = False

        self.input_history = self._merge_history("input", self.project_root / self.config.get("input_dir", "input"))
        self.output_history = self._merge_history("output", self.project_root / self.config.get("output_dir", "output"))

        self.input_var = tk.StringVar(value=self.input_history[0])
        self.output_var = tk.StringVar(value=self.output_history[0])
        self.summary_var = tk.StringVar(value=self.theme["labels"]["no_run"])

        self.root.title(self.theme["window"]["title"])
        self.root.geometry(self.theme["window"]["geometry"])
        self.root.minsize(self.theme["window"]["min_width"], self.theme["window"]["min_height"])

        self._build_ui()
        self._apply_theme(initial=True)
        self.root.after(100, self._poll_queue)

    def _load_defaults(self) -> dict:
        try:
            return load_config(self.project_root)
        except Exception:
            return {}

    def _resolve_theme_path(self) -> Path:
        candidates = [
            self.project_root / "ui_theme.json",
            self.project_root / "src" / "ui_theme.json",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return self.project_root / "ui_theme.json"

    def _load_theme(self) -> dict:
        theme = DEFAULT_THEME
        if self.theme_path.exists():
            with self.theme_path.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            theme = _deep_merge(DEFAULT_THEME, loaded)
        return theme

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

    def _font(self, key: str) -> tuple:
        value = self.theme["fonts"].get(key, DEFAULT_THEME["fonts"][key])
        return tuple(value)

    def _configure_style(self) -> None:
        colors = self.theme["colors"]
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.style.configure("App.TFrame", background=colors["app_bg"])
        self.style.configure(
            "App.TLabel",
            background=colors["app_bg"],
            foreground=colors["text"],
            font=self._font("body"),
        )
        self.style.configure(
            "Title.TLabel",
            background=colors["app_bg"],
            foreground=colors["text"],
            font=self._font("title"),
        )
        self.style.configure(
            "Subtitle.TLabel",
            background=colors["app_bg"],
            foreground=colors["muted_text"],
            font=self._font("subtitle"),
        )
        self.style.configure(
            "ThemeHint.TLabel",
            background=colors["app_bg"],
            foreground=colors["muted_text"],
            font=self._font("subtitle"),
        )
        self.style.configure(
            "Card.TLabelframe",
            background=colors["panel_bg"],
            bordercolor=colors["panel_border"],
            borderwidth=1,
            relief="solid",
        )
        self.style.configure(
            "Card.TLabelframe.Label",
            background=colors["panel_bg"],
            foreground=colors["text"],
            font=self._font("section"),
        )
        self.style.configure(
            "Summary.TLabel",
            background=colors["summary_bg"],
            foreground=colors["summary_fg"],
            font=self._font("summary"),
        )
        self.style.configure(
            "Primary.TButton",
            background=colors["accent"],
            foreground=colors["accent_text"],
            font=self._font("button"),
            borderwidth=0,
            focusthickness=0,
            padding=(14, 8),
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", colors["accent_hover"]), ("disabled", colors["secondary_bg"])],
            foreground=[("disabled", colors["muted_text"])],
        )
        self.style.configure(
            "Secondary.TButton",
            background=colors["secondary_bg"],
            foreground=colors["secondary_text"],
            font=self._font("button"),
            borderwidth=0,
            focusthickness=0,
            padding=(12, 8),
        )
        self.style.map("Secondary.TButton", background=[("active", colors["panel_border"])])
        self.style.configure(
            "TCombobox",
            fieldbackground=colors["input_bg"],
            background=colors["input_bg"],
            foreground=colors["input_fg"],
            arrowsize=15,
            padding=6,
        )
        self.style.map("TCombobox", fieldbackground=[("readonly", colors["input_bg"])])

    def _build_ui(self) -> None:
        outer_padding = self.theme["spacing"]["outer_padding"]
        section_gap = self.theme["spacing"]["section_gap"]
        panel_padding = self.theme["spacing"]["panel_padding"]

        self.container = ttk.Frame(self.root, padding=outer_padding, style="App.TFrame")
        self.container.pack(fill="both", expand=True)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(2, weight=1)
        self.container.rowconfigure(3, weight=1)

        self.header = ttk.Frame(self.container, style="App.TFrame")
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self.header, style="Title.TLabel")
        self.title_label.grid(row=0, column=0, sticky="w")
        self.subtitle_label = ttk.Label(self.header, style="Subtitle.TLabel")
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(4, 2))
        self.theme_hint_label = ttk.Label(self.header, style="ThemeHint.TLabel")
        self.theme_hint_label.grid(row=2, column=0, sticky="w")

        self.header_actions = ttk.Frame(self.header, style="App.TFrame")
        self.header_actions.grid(row=0, column=1, rowspan=3, sticky="e")
        self.edit_theme_button = ttk.Button(self.header_actions, command=self._open_theme_file, style="Secondary.TButton")
        self.edit_theme_button.grid(row=0, column=0, padx=(8, 0))
        self.reload_theme_button = ttk.Button(self.header_actions, command=self._reload_theme, style="Secondary.TButton")
        self.reload_theme_button.grid(row=0, column=1, padx=(8, 0))

        self.controls = ttk.LabelFrame(self.container, style="Card.TLabelframe", padding=panel_padding)
        self.controls.grid(row=1, column=0, sticky="ew", pady=(section_gap, 12))
        self.controls.columnconfigure(1, weight=1)

        self.input_label = ttk.Label(self.controls, style="App.TLabel")
        self.input_label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        # Create drop zone frame with drag-and-drop support
        self.drop_frame = tk.Frame(self.controls, bg=self.theme["colors"]["input_bg"], relief="solid", borderwidth=1)
        self.drop_frame.grid(row=0, column=1, sticky="ew", padx=8, pady=(0, 8))
        self.drop_frame.columnconfigure(0, weight=1)
        
        self.input_combo = ttk.Combobox(self.drop_frame, textvariable=self.input_var, values=self.input_history)
        self.input_combo.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.input_browse_button = ttk.Button(self.controls, command=self._pick_input_dir, style="Secondary.TButton")
        self.input_browse_button.grid(row=0, column=2, sticky="ew", pady=(0, 8))
        
        # Setup drag-and-drop if available
        if HAS_DND:
            try:
                self.drop_frame.drop_target_register(DND_FILES)
                self.drop_frame.dnd_bind('<<Drop>>', self._on_drop_files)
                self.drop_frame.dnd_bind('<<DragEnter>>', self._on_drag_enter)
                self.drop_frame.dnd_bind('<<DragLeave>>', self._on_drag_leave)
                self.input_combo.drop_target_register(DND_FILES)
                self.input_combo.dnd_bind('<<Drop>>', self._on_drop_files)
                self.input_combo.dnd_bind('<<DragEnter>>', self._on_drag_enter)
                self.input_combo.dnd_bind('<<DragLeave>>', self._on_drag_leave)
            except Exception:
                pass  # DND not fully supported on this platform

        self.output_label = ttk.Label(self.controls, style="App.TLabel")
        self.output_label.grid(row=1, column=0, sticky="w")
        self.output_combo = ttk.Combobox(self.controls, textvariable=self.output_var, values=self.output_history)
        self.output_combo.grid(row=1, column=1, sticky="ew", padx=8)
        self.output_browse_button = ttk.Button(self.controls, command=self._pick_output_dir, style="Secondary.TButton")
        self.output_browse_button.grid(row=1, column=2, sticky="ew")

        self.buttons = ttk.Frame(self.controls, style="App.TFrame")
        self.buttons.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(14, 0))
        self.buttons.columnconfigure(4, weight=1)

        self.run_button = ttk.Button(self.buttons, command=self._start_run, style="Primary.TButton")
        self.run_button.grid(row=0, column=0, sticky="w")
        self.open_button = ttk.Button(self.buttons, command=self._open_spreadsheet, state="disabled", style="Secondary.TButton")
        self.open_button.grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.clear_button = ttk.Button(self.buttons, command=self._clear_panels, style="Secondary.TButton")
        self.clear_button.grid(row=0, column=2, sticky="w", padx=(8, 0))

        self.status_frame = ttk.LabelFrame(self.container, style="Card.TLabelframe", padding=panel_padding)
        self.status_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
        self.status_text = ScrolledText(self.status_frame, height=14, wrap="word")
        self.status_text.pack(fill="both", expand=True)
        self.status_text.configure(state="disabled")

        self.lower = ttk.Frame(self.container, style="App.TFrame")
        self.lower.grid(row=3, column=0, sticky="nsew")
        self.lower.columnconfigure(0, weight=1)
        self.lower.columnconfigure(1, weight=1)
        self.lower.rowconfigure(1, weight=1)

        self.summary_frame = ttk.LabelFrame(self.lower, style="Card.TLabelframe", padding=panel_padding)
        self.summary_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self.summary_label = ttk.Label(self.summary_frame, textvariable=self.summary_var, style="Summary.TLabel", justify="left")
        self.summary_label.pack(fill="both", expand=True)

        self.errors_frame = ttk.LabelFrame(self.lower, style="Card.TLabelframe", padding=panel_padding)
        self.errors_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        self.error_text = ScrolledText(self.errors_frame, height=8, wrap="word")
        self.error_text.pack(fill="both", expand=True)
        self.error_text.configure(state="disabled")

    def _apply_theme(self, initial: bool = False) -> None:
        colors = self.theme["colors"]
        labels = self.theme["labels"]
        spacing = self.theme["spacing"]

        self.root.configure(bg=colors["app_bg"])
        self.root.title(self.theme["window"]["title"])
        self.root.minsize(self.theme["window"]["min_width"], self.theme["window"]["min_height"])
        if initial:
            self.root.geometry(self.theme["window"]["geometry"])

        self._configure_style()

        self.container.configure(padding=spacing["outer_padding"])
        self.controls.configure(text=labels["controls_title"], padding=spacing["panel_padding"])
        self.status_frame.configure(text=labels["status_title"], padding=spacing["panel_padding"])
        self.summary_frame.configure(text=labels["summary_title"], padding=spacing["panel_padding"])
        self.errors_frame.configure(text=labels["errors_title"], padding=spacing["panel_padding"])

        # Update drop frame colors
        self.drop_frame.configure(bg=colors["input_bg"], relief="solid", borderwidth=1)

        self.title_label.configure(text=labels["title"])
        self.subtitle_label.configure(text=labels["subtitle"])
        self.theme_hint_label.configure(text=f"{labels['theme_hint']}  File: {self.theme_path}")
        self.input_label.configure(text=labels["input_label"])
        self.output_label.configure(text=labels["output_label"])
        self.run_button.configure(text=labels["run_button"])
        self.open_button.configure(text=labels["open_button"])
        self.clear_button.configure(text=labels["clear_button"])
        self.reload_theme_button.configure(text=labels["reload_button"])
        self.edit_theme_button.configure(text=labels["edit_button"])
        self.input_browse_button.configure(text="Browse...")
        self.output_browse_button.configure(text="Browse...")

        if self.summary_var.get() in {"No run yet.", "No run yet", "Running...", "Running... "}:
            if self.summary_var.get().startswith("Running"):
                self.summary_var.set(labels["running"])
            else:
                self.summary_var.set(labels["no_run"])

        self.summary_label.configure(style="Summary.TLabel")
        self.status_text.configure(
            font=self._font("mono"),
            background=colors["status_bg"],
            foreground=colors["status_fg"],
            insertbackground=colors["status_fg"],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=colors["panel_border"],
            highlightcolor=colors["accent"],
            padx=8,
            pady=8,
        )
        self.error_text.configure(
            font=self._font("mono"),
            background=colors["error_bg"],
            foreground=colors["error_fg"],
            insertbackground=colors["error_fg"],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=colors["panel_border"],
            highlightcolor=colors["accent"],
            padx=8,
            pady=8,
        )

    def _on_drag_enter(self, event) -> str:
        """Handle drag enter event - highlight drop zone."""
        if HAS_DND:
            self.drag_active = True
            self.drop_frame.configure(
                bg=self.theme["colors"]["drop_zone_bg"],
                relief="solid",
                borderwidth=2
            )
            # Change border color to accent
            try:
                self.drop_frame.configure(highlightbackground=self.theme["colors"]["drop_zone_border"])
            except Exception:
                pass
        return "copy"

    def _on_drag_leave(self, event) -> None:
        """Handle drag leave event - restore normal appearance."""
        if HAS_DND:
            self.drag_active = False
            self.drop_frame.configure(
                bg=self.theme["colors"]["input_bg"],
                relief="solid",
                borderwidth=1
            )

    def _on_drop_files(self, event) -> None:
        """Handle file drop event."""
        self.drag_active = False
        self.drop_frame.configure(
            bg=self.theme["colors"]["input_bg"],
            relief="solid",
            borderwidth=1
        )
        
        if not HAS_DND:
            return
        
        try:
            # Parse the dropped files from the event data
            files_str = event.data
            # Handle different formats of file paths
            files = []
            if files_str.startswith("{"):
                # Windows format with braces
                files_str = files_str.strip("{}")
                files = [f.strip() for f in files_str.split("} {")]
                files = [f.replace("{", "").replace("}", "") for f in files]
            else:
                # Unix format with spaces
                files = files_str.split()
            
            # Filter for the first directory or most logical input
            valid_dirs = []
            for file_path in files:
                clean_path = file_path.strip()
                if clean_path:
                    path = Path(clean_path)
                    if path.is_dir():
                        valid_dirs.append(str(path))
                    elif path.is_file() and path.parent.exists():
                        # If it's a file, use its parent directory
                        valid_dirs.append(str(path.parent))
            
            if valid_dirs:
                # Use the first valid directory
                selected_dir = valid_dirs[0]
                self._remember_directory("input", selected_dir)
                self._append_status(f"Dropped folder: {selected_dir}")
        except Exception as exc:
            self._append_status(f"Drop failed: {exc}")

    def _apply_theme(self, initial: bool = False) -> None:
        try:
            self.theme = self._load_theme()
            self._apply_theme()
        except Exception as exc:
            self._set_text(self.error_text, self._format_error(exc))
            messagebox.showerror("Theme reload failed", f"Could not reload theme file:\n{exc}")
            return
        self._append_status(f"Theme reloaded from {self.theme_path}")

    def _open_theme_file(self) -> None:
        try:
            if not self.theme_path.exists():
                with self.theme_path.open("w", encoding="utf-8") as handle:
                    json.dump(DEFAULT_THEME, handle, indent=2)
            open_in_default_app(self.theme_path)
        except Exception as exc:
            self._set_text(self.error_text, self._format_error(exc))
            messagebox.showerror("Theme file error", f"Could not open theme file:\n{exc}")
            return
        self._append_status(f"Opened theme file: {self.theme_path}")

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
        self.summary_var.set(self.theme["labels"]["no_run"])

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
        self.summary_var.set(self.theme["labels"]["running"])
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