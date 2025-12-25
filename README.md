# 🌱 Sapling Family Formatter

A powerful genealogical LaTeX document generator that transforms family tree data into beautifully formatted PDF reports.

## 📖 Overview

**Sapling Family Formatter** converts genealogy text files into professional-quality LaTeX documents with proper formatting, hyperlinks, and typesetting. Perfect for creating stunning family history reports, ancestor documentation, and genealogical publications.

## ✨ Features

- **📝 Text-to-LaTeX Conversion**: Automatically converts genealogy text files to LaTeX format
- **✂️ Smart File Splitting**: Breaks large genealogy reports into manageable chunks at anchor points
- **🔗 Hyperlink Support**: Creates internal links between family members and external URL references
- **👪 Family Relationships**: Properly formats marriages, children, and ancestral relationships
- **📚 Biography Integration**: Handles general notes and biographical information
- **🎨 Professional Typography**: Uses EB Garamond and Public Sans fonts for elegant output
- **⚙️ Flexible CLI**: Command-line interface with customizable options

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- XeLaTeX compiler

### Basic Usage

#### Generate LaTeX from Text File
```bash
python generate_tex.py input.txt output.tex
```

#### Split Large Files
```bash
# Basic split with defaults
python split_file.py input.txt output_dir/

# Custom chunk size and naming
python split_file.py "genealogy_report.txt" "chunks/" --lines 14200 --prefix "parsed_output"

# Preview mode (dry-run)
python split_file.py "report.txt" "chunks/" --dry-run
```

#### Compile to PDF
```bash
xelatex -output-directory="output/" -jobname="Family_Report" main_template.tex
```

## 📂 Project Structure

```
sapling-family-formatter/
├── generate_tex.py          # Main LaTeX converter
├── split_file.py            # File splitting utility
├── main_template.tex        # LaTeX template
├── assets/
│   └── fonts/
│       ├── EBGaramond/     # Serif font for body text
│       └── PublicSans/     # Sans-serif font for headings
├── SPLIT_FILE_GUIDE.md     # Detailed splitting guide
└── .gitignore
```

## 📋 Input Format

The tool expects genealogy text files with:
- Person entries marked with `##ANCHOR:iXXXXX##` tags
- Generation headers
- Person details (birth, death, marriages)
- Children information
- Biographical notes

## 🎨 Output Features

- **Name Formatting**: Bold names with proper suffixes (Jr., Sr., III, etc.)
- **Life Events**: Structured birth, death, baptism, and marriage information
- **Family Trees**: Organized children listings with Roman numerals
- **Hyperlinks**: Clickable cross-references between family members
- **Professional Layout**: Optimized for print and digital viewing

## 🔧 Advanced Options

### Split File Options
```bash
python split_file.py --help

Options:
  --lines LINES, -l LINES    Approximate lines per chunk (default: 7000)
  --prefix PREFIX, -p PREFIX  Prefix for output files (default: "split")
  --dry-run                  Preview without actually splitting
```

## 💡 Examples

### Complete Workflow
```bash
# 1. Split large genealogy file
python split_file.py "Ancestors_Report.txt" "chunks/" --lines 14200 --prefix "part"

# 2. Convert each chunk to LaTeX
python generate_tex.py "chunks/part1.txt" "output/part1.tex"

# 3. Compile to PDF
xelatex -output-directory="output/" main_template.tex
```

### Custom Font Setup
The project includes:
- **EB Garamond**: Elegant serif font for body text and names
- **Public Sans**: Modern sans-serif font for headings and UI elements

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open source and available for genealogical research and documentation.

## 🙏 Acknowledgments

Built with care for preserving family histories and making genealogical documentation beautiful and accessible.

---

**Created by**: [shafiquelhr](https://github.com/shafiquelhr)  
**Repository**: https://github.com/shafiquelhr/sapling-family-formatter
