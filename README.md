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
- **🔄 Multi-line Link Handling**: Properly joins markdown links split across multiple lines
- **📛 Long Name Support**: Handles names with commas (e.g., "Count of Aargau, Auxerre and Paris")

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- XeLaTeX compiler

### Complete Workflow

```bash
# Step 1: Split large genealogy file into chunks (if file is large)
python split_file.py "Ancestors_Report.txt" "chunks/" --lines 14200 --prefix "parsed_chunked_output"

# Step 2: Convert each chunk to LaTeX
python generate_tex.py "chunks/parsed_chunked_output1.txt" "tex-output/parsed_chunked_output1.tex"
python generate_tex.py "chunks/parsed_chunked_output2.txt" "tex-output/parsed_chunked_output2.tex"
# ... repeat for all chunks

# Step 3: Update main_template.tex to include your chunks (edit the \input{} lines)

# Step 4: Compile to PDF
xelatex -output-directory="output/" -jobname="Family_Report" main_template.tex
```

## 📂 Project Structure

```
sapling-family-formatter/
├── generate_tex.py          # Main LaTeX converter (CORE)
├── split_file.py            # File splitting utility (CORE)
├── main_template.tex        # LaTeX template (CORE)
├── README.md                # This documentation
├── SPLIT_FILE_GUIDE.md      # Detailed splitting guide
├── .gitignore               # Git ignore patterns
└── assets/
    └── fonts/
        ├── EBGaramond/      # Serif font for headers
        └── PublicSans/      # Sans-serif font for body text
```

## 🛠️ Core Tools

### 1. `generate_tex.py` - LaTeX Generator

The main conversion tool that transforms genealogy text files to LaTeX format.

**Usage:**
```bash
python generate_tex.py <input.txt> <output.tex>
```

**Features:**
- Detects and formats person entries with anchor tags (`##ANCHOR:iXXXXX##`)
- Creates hyperlinks for person references (`[Name](#iXXXXX)`)
- Formats marriages, children, and biographical information
- Handles generation titles (First Generation, Second Generation, etc.)
- Properly escapes LaTeX special characters
- Joins multi-line markdown links automatically

### 2. `split_file.py` - File Splitter

Splits large genealogy files into smaller chunks at anchor points.

**Usage:**
```bash
python split_file.py <input.txt> <output_dir/> [options]

Options:
  --lines LINES, -l LINES    Approximate lines per chunk (default: 7000)
  --prefix PREFIX, -p PREFIX  Prefix for output files (default: "split")
  --dry-run                  Preview without actually splitting
```

**Example:**
```bash
# Split a 70,000 line file into ~5 chunks
python split_file.py "large_file.txt" "chunks/" --lines 14200 --prefix "parsed_chunked_output"
```

### 3. `main_template.tex` - LaTeX Template

The master LaTeX template that includes all your generated chunks and produces the final PDF.

**To customize:**
1. Edit the `\reportmaintitle{}` to change the document title
2. Update the `\input{}` lines to point to your generated .tex chunks
3. Modify fonts, colors, or styling as needed

## 📋 Input Format

The tool expects genealogy text files with:
- Person entries marked with `##ANCHOR:iXXXXX##` tags
- Generation headers (e.g., "First Generation", "Second Generation (Parents)")
- Markdown-style links: `[Person Name](#iXXXXX)` or `[Person Name](#iXXXXX)`
- Marriage information
- Children listings
- General Notes and Biography sections

**Example Input:**
```
First Generation

##ANCHOR:i12345##
1. John Smith, son of [William Smith](#i12346) and [Mary Jones](#i12347), was born on 15 Jan 1850 in Boston, Massachusetts.

General Notes: He was a prominent merchant.

John married [Jane Doe](#i12348), daughter of [James Doe](#i12349).

Children from this marriage were:
(123456) i. [William Smith Jr.](#i12350)
(123457) ii. [Sarah Smith](#i12351)
```

## 🎨 Output Features

- **Name Formatting**: Bold names with proper suffixes (Jr., Sr., III, etc.)
- **Life Events**: Structured birth, death, baptism, and marriage information
- **Family Trees**: Organized children listings with reference badges and Roman numerals
- **Hyperlinks**: Clickable cross-references between family members
- **Professional Layout**: Optimized for print and digital viewing
- **Generation Sections**: Automatic detection and formatting of generation titles

## 📚 Additional Documentation

- **[SPLIT_FILE_GUIDE.md](SPLIT_FILE_GUIDE.md)** - Detailed guide for using the file splitter

## 🔧 Troubleshooting

### Common Issues

1. **Links appearing as `](#iXXXXX)`**: This usually means a link was split across lines. The tool now handles this automatically by joining multi-line content.

2. **Names with commas getting split wrong**: Names like "Count of Aargau, Auxerre and Paris" are now handled correctly - the tool detects complete markdown links before splitting on commas.

3. **XeLaTeX errors**: Make sure you have the required fonts installed (EB Garamond and Public Sans are included in the `assets/fonts/` folder).

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
