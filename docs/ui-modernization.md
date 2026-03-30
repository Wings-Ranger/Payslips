# UI Modernization & Drag-and-Drop Support

## Overview

The Payslip Tracker GUI has been modernized with a contemporary design and drag-and-drop file support. The app now features:

- **Modern Design**: Clean blue color scheme with professional styling
- **Drag-and-Drop Support**: Drop folders directly into the input area while the app is running
- **Enhanced Typography**: Better fonts and hierarchy
- **Visual Feedback**: Interactive elements with visual states and animations
- **Improved Spacing**: Better layout and organization

## What's New

### Modern Color Scheme
- Primary accent: Modern blue (#3b82f6)
- Clean white panels with subtle gray borders
- Professional typography using Segoe UI
- Better contrast and readability

### Drag-and-Drop Functionality
The input folder area now supports drag-and-drop:
1. Drag a folder from Windows Explorer
2. Drop it directly into the input field while the app is open
3. The app automatically updates the input folder path
4. Visual feedback shows when you're hovering over the drop zone

### Visual Enhancements
- Enhanced button styling with emoji icons
- Better visual hierarchy in labels
- Improved spacing between elements
- Cleaner borders and panels
- Visual feedback on hover and interaction

## Installation: Full Drag-and-Drop Support

For full drag-and-drop functionality, install the `tkinterdnd2` library:

```bash
pip install tkinterdnd2
```

### Platform-Specific Notes

**Windows:**
```bash
pip install tkinterdnd2
```

**macOS:**
```bash
pip install tkinterdnd2
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-tk-dev
pip install tkinterdnd2

# Fedora/RHEL
sudo dnf install python3-tkinter python3-devel
pip install tkinterdnd2
```

### Without tkinterdnd2

The app will still work without `tkinterdnd2`, but you can only select input folders using the "Browse..." button. The drag-and-drop area will have visual styling but won't accept drops.

## Customization

You can customize the appearance by editing [ui_theme.json](../ui_theme.json):

```json
{
  "colors": {
    "accent": "#3b82f6",           // Primary button color
    "accent_hover": "#2563eb",     // Button hover state
    "app_bg": "#f5f7fa",           // Background color
    "panel_bg": "#ffffff",         // Panel background
    "drop_zone_bg": "#dbeafe"      // Drag-over highlight color
  },
  "fonts": {
    "title": ["Segoe UI", 28, "bold"],
    "body": ["Segoe UI", 10]
  }
}
```

After editing, click **🔄 Reload Theme** in the app to apply changes immediately.

## Usage

### Traditional Method (Browse Button)
1. Click the "Browse..." button next to the input folder field
2. Select a folder from the dialog
3. The path appears in the input field

### Modern Method (Drag-and-Drop)
1. Open Windows Explorer (or Finder/File Manager on Mac/Linux)
2. Navigate to your payslips folder
3. Drag and drop it directly onto the input folder field
4. The field automatically updates with the folder path

## Responsive Design

The UI automatically adapts to different window sizes:
- **Minimum size**: 900×700 pixels
- **Default size**: 1020×800 pixels
- All elements scale proportionally
- Text remains readable at any size

## Troubleshooting

**Drag-and-drop not working?**
- Install tkinterdnd2: `pip install tkinterdnd2`
- Restart the application
- Check console for error messages

**Theme not applying?**
- Click "🔄 Reload Theme" button
- Check ui_theme.json for syntax errors (use JSON validator)
- Ensure the file is in the project root or src/ directory

**Text looks blurry?**
- This is a Windows/display scaling issue
- Try running with: `python -m pyinstaller --dpi-aware=all`

## Developer Notes

### Architecture
- **payslip_gui.py**: Main GUI application class
- **ui_theme.json**: Theme configuration (colors, fonts, spacing)
- **Drag-drop handlers**: `_on_drag_enter()`, `_on_drag_leave()`, `_on_drop_files()`

### Color Variables Used
```python
colors = {
    "app_bg": "#f5f7fa",              # Root window background
    "panel_bg": "#ffffff",             # Card/panel background
    "text": "#1a202c",                 # Primary text color
    "accent": "#3b82f6",               # Primary action color
    "drop_zone_bg": "#dbeafe",         # Hover state for drop zones
    "status_bg": "#f8fafc",            # Status text background
    "error_bg": "#fef2f2",             # Error message background
}
```

### Key Methods
- `_on_drag_enter(event)`: Visual feedback when dragging over drop zone
- `_on_drag_leave(event)`: Restore normal appearance when leaving drop zone
- `_on_drop_files(event)`: Process dropped files and update input folder
- `_apply_theme()`: Apply theme colors to all elements

## Future Enhancements

Potential improvements for future versions:
- [ ] Dark mode theme
- [ ] Multi-file drag-drop (process multiple files in one operation)
- [ ] File preview in drop zone
- [ ] Keyboard shortcuts (e.g., Ctrl+O for browse)
- [ ] Progress bar with percentage
- [ ] File type validation on drop
