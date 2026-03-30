# Getting Started with the Modern Payslip Tracker

## Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd Payslips
   ```

2. **Install core dependencies:**
   ```bash
   pip install -r docs/requirements.txt
   ```

3. **Optional: Install GUI enhancements (for drag-and-drop):**
   ```bash
   pip install -r docs/requirements-gui.txt
   ```

4. **Run the application:**
   - **Using the batch file (Windows):**
     ```bash
     Process Payslips.bat
     ```
   - **Using Python directly:**
     ```bash
     python -m src.payslip_gui
     ```

## New Modern Features

### 🎨 Visual Design
- **Contemporary Color Scheme**: Professional blue and gray palette
- **Clean Typography**: Segoe UI fonts with better hierarchy
- **Improved Layout**: Better spacing and visual organization
- **Responsive Design**: Works smoothly at any window size

### 📂 Drag-and-Drop Support
Once you install `tkinterdnd2`, you can:

1. **Drag folders directly into the app:**
   ```
   File Explorer → Select Folder → Drag to "Input folder" field → Drop
   ```

2. **Visual feedback:**
   - Drop zone highlights in blue when you drag over it
   - Light blue background indicates the area is ready to receive files
   - Border changes to show it's active

3. **No installation needed for basic usage:**
   - The "Browse..." button always works
   - Drag-and-drop is optional and requires `tkinterdnd2`

### ⚡ User Experience Improvements
- **Emoji Icons**: Visual indicators for different actions
  - 📊 Payslip Tracker (title)
  - 📁 Folders & Actions (section)
  - ▶ Process Payslips (run button)
  - 📄 View Results (open button)
  - 🗑️ Clear (clear button)
  - 🔄 Reload Theme (reload button)
  - ✏️ Edit Theme (edit button)

- **Better Status Messages**: Clear, informative feedback during processing
- **Live Theme Editing**: Change colors instantly without restarting

## Customizing the Theme

### Edit Colors
1. Open `ui_theme.json`
2. Modify the color values in the `colors` section
3. Click **🔄 Reload Theme** in the app to see changes instantly

### Available Color Settings
```json
{
  "colors": {
    "app_bg": "#f5f7fa",              // Main background
    "panel_bg": "#ffffff",             // Card backgrounds
    "text": "#1a202c",                 // Text color
    "accent": "#3b82f6",               // Primary buttons
    "accent_hover": "#2563eb",         // Button hover
    "drop_zone_bg": "#dbeafe",         // Drag-over color
    "input_bg": "#ffffff",             // Input field background
    "status_bg": "#f8fafc",            // Status area background
    "error_bg": "#fef2f2",             // Error message background
    "summary_bg": "#eff6ff"            // Summary area background
  }
}
```

### Change Fonts
```json
{
  "fonts": {
    "title": ["Segoe UI", 28, "bold"],      // Main title
    "subtitle": ["Segoe UI", 11],           // Subtitle text
    "section": ["Segoe UI Semibold", 12],   // Section headers
    "button": ["Segoe UI Semibold", 11]     // Button text
  }
}
```

### Adjust Spacing
```json
{
  "spacing": {
    "outer_padding": 20,      // Window padding
    "panel_padding": 16,      // Inside panels
    "section_gap": 16         // Between sections
  }
}
```

## Setup by Platform

### Windows
```bash
# Install drag-and-drop support
pip install tkinterdnd2

# Run the app
python -m src.payslip_gui
```

### macOS
```bash
# Ensure you have Python with Tkinter
# Often comes with Python from python.org or Homebrew
python3 -m pip install --upgrade pip
pip install tkinterdnd2
python3 -m src.payslip_gui
```

### Linux (Ubuntu/Debian)
```bash
# System dependencies
sudo apt-get install python3-tk python3-dev

# Python dependencies
pip install -r docs/requirements.txt
pip install -r docs/requirements-gui.txt

# Run
python3 -m src.payslip_gui
```

### Linux (Fedora/RHEL)
```bash
# System dependencies
sudo dnf install python3-tkinter python3-devel

# Python dependencies
pip install -r docs/requirements.txt
pip install -r docs/requirements-gui.txt

# Run
python3 -m src.payslip_gui
```

## Troubleshooting

### Drag-and-Drop Not Working
**Problem**: Drop functionality not active
**Solution**:
```bash
pip install tkinterdnd2
# Restart the application
```

### Theme File Not Found
**Problem**: "Could not find theme file" error
**Solution**:
1. The theme file should be at `ui_theme.json` (root) or `src/ui_theme.json`
2. If missing, click **✏️ Edit Theme** to create it automatically
3. Verify file is valid JSON

### GUI Looks Blurry (Windows)
**Problem**: Text and elements appear fuzzy
**Solution**:
1. Close the application
2. Build with DPI awareness (if compiled with PyInstaller):
   ```bash
   pyinstaller --dpi-aware=all src/payslip_gui.py
   ```

### "ModuleNotFoundError: No module named 'tkinterdnd2'"
**Problem**: Drag-and-drop library not found
**Solution**:
- This is NOT required for the app to work
- You can still use the "Browse..." button to select folders
- To enable drag-and-drop, install: `pip install tkinterdnd2`

### Application Won't Start
**Problem**: "No module named 'payslip_tracker'" or similar
**Solution**:
```bash
# Ensure you're in the project root
cd Payslips

# Install dependencies
pip install -r docs/requirements.txt

# Run with absolute path
python -m src.payslip_gui
```

## Features Deep Dive

### The Input Area (Drag-and-Drop Zone)
- **Default behavior**: Click "Browse..." to select a folder
- **With tkinterdnd2**: Drag any folder directly onto this area
- **Visual feedback**: Area highlights in blue when you hover with files
- **Smart detection**: Works with both folders and files (uses parent directory)

### Status Display
- **Real-time updates**: See processing progress as it happens
- **Clear messaging**: Each action is logged with timestamp
- **Error reporting**: Detailed error messages for debugging

### Summary Panel
- **File count**: Total payslips scanned
- **Success count**: Files successfully processed
- **Skipped**: Files skipped (already processed)
- **Issues**: Schema validation failures
- **Missing weeks**: Weeks not found in the data

### Error Panel
- **Detailed messages**: Full error information for debugging
- **Stack traces**: Complete error context when needed
- **Clear button**: Reset after reviewing errors

## Performance Tips

1. **Folder Selection**: Local folders are faster than network shares
2. **File Format**: Ensure PDF files are readable and not corrupted
3. **Output Size**: For large sets, the CSV might take time to generate
4. **Theme Reload**: Safe at any time, won't interrupt processing

## Tips & Tricks

1. **Keyboard Navigation**:
   - Tab: Move between fields
   - Enter: In folder field, execute run
   - Alt+R: Run button (if enabled in theme)

2. **Recent Folders**: App remembers the last 8 input/output folders

3. **Theme Presets**: Save different theme files:
   - `ui_theme_dark.json` (for custom dark theme)
   - `ui_theme_light.json` (for custom light theme)
   - Then copy to `ui_theme.json` to use

4. **Batch Processing**: Set a static input/output folder in config.json

## Building an Executable

See [build instructions](code-blocks/pyinstaller-build.md) for creating standalone .exe files.

## Next Steps

- [Theme Customization Guide](theme-guide/README.md)
- [Configuration Options](code-blocks/config-json.md)
- [Understanding the Data Flow](building-blocks/README.md)
