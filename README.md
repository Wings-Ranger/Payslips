# Payslip Tracker

A simple tool that reads your payslip files and creates an organised spreadsheet.

## How to Use

1. Double-click **Process Payslips.bat**
2. Choose your **input** folder and **output** folder in the app window
3. Click **Run**
4. Review the progress, summary, and any errors in the app
5. Click **Open Spreadsheet** when processing is complete

The app remembers recently used input and output folders so repeat runs are quicker.
It also reads styling from [ui_theme.json](ui_theme.json), and you can change the look live with **Open Theme File** plus **Reload Theme**.

## What You Get

- **payslips.xlsx** - A colour-coded spreadsheet with all your payslip data
  - Ordinary hours, weekend hours, and public holiday hours broken out separately
  - Gross pay, tax, PAYG, and net pay columns
  - A "Missing Weeks" sheet showing any gaps where no payslip was found
- **payslips.csv** - The same data in a simple format you can open in any program

## Folder Guide

| Folder | What's in it |
|--------|-------------|
| **input** | Put your payslip files here before running |
| **output** | Your reports appear here after running |
| **src** | The program files (no need to touch these) |

## Technique Map (Developer Docs)

If you are extending or maintaining the project, start here:

- [Technical Docs Overview](docs/README.md) - architecture, configuration, and setup
- [Coding Techniques Index](docs/coding-techniques/README.md) - one note per reusable coding technique
- [Code Blocks Index](docs/code-blocks/README.md) - one note per concrete function or script block

Use the Coding Techniques docs when deciding how to implement changes.
Use the Code Blocks docs when you need exact behavior for a specific function.

## Troubleshooting

**Nothing happens when I double-click the bat file**
- Make sure Python is installed on your computer
- Ask your IT team to install Python if needed

**The app shows an error panel**
- Read the message in the Errors section of the window
- Check that your input folder contains .pdf or .txt payslip files
- If needed, try a different output folder where Excel files can be saved

**I want to change how the app looks**
- Click **Open Theme File** in the app
- Edit colours, fonts, labels, or window size in `ui_theme.json`
- Click **Reload Theme** to apply the changes without restarting

**"No payslip files found"**
- Check that your payslip files are in the **input** folder
- Files must be .pdf or .txt format

**Some payslips show "SKIPPED: Scanned PDF, needs OCR"**
- These are image-based PDFs (like a photo or scan)
- The tool can only read text-based PDFs
- Ask your payroll provider for a digital/text version

**The spreadsheet won't update**
- Close the spreadsheet in Excel first, then run again
- If it was locked, a backup copy is saved with a timestamp and shown in the summary

## Privacy

All your payslip data stays on your computer. Nothing is sent online.
