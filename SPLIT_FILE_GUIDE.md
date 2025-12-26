# Split File Tool - User Guide

## Overview

Enhanced genealogy file splitter that breaks large text files into smaller chunks at anchor points (`##ANCHOR:iXXXXX##`). Includes command-line interface, error handling, and flexible configuration.

## 🚀 Quick Start (Recommended)

**For most users, just run one of these:**

```bash
# Split your file into chunks with custom naming
python split_file.py "your_file.txt" "output_folder/" --lines 14200 --prefix "parsed_chunked_output"

# Preview what will happen first (recommended)
python split_file.py "your_file.txt" "output_folder/" --lines 14200 --prefix "parsed_chunked_output" --dry-run
```

**That's it!** The tool handles everything else automatically.

---

## Complete Workflow

This guide walks you through the entire process from raw text file to formatted PDF.

### Step 1: Split Large File (Optional but Recommended)

If your genealogy file is very large (50,000+ lines), split it into manageable chunks:

```bash
python split_file.py "Ancestors_Report.txt" "chunks/" --lines 14200 --prefix "parsed_chunked_output"
```

This creates files like:
- `chunks/parsed_chunked_output1.txt`
- `chunks/parsed_chunked_output2.txt`
- `chunks/parsed_chunked_output3.txt`
- etc.

### Step 2: Convert Each Chunk to LaTeX

Use `generate_tex.py` to convert each text chunk to LaTeX:

```bash
python generate_tex.py "chunks/parsed_chunked_output1.txt" "tex-output/parsed_chunked_output1.tex"
python generate_tex.py "chunks/parsed_chunked_output2.txt" "tex-output/parsed_chunked_output2.tex"
python generate_tex.py "chunks/parsed_chunked_output3.txt" "tex-output/parsed_chunked_output3.tex"
python generate_tex.py "chunks/parsed_chunked_output4.txt" "tex-output/parsed_chunked_output4.tex"
python generate_tex.py "chunks/parsed_chunked_output5.txt" "tex-output/parsed_chunked_output5.tex"
```

### Step 3: Update main_template.tex

Edit `main_template.tex` to include your generated chunks. Find the section near the bottom:

```latex
% ======== DROP CONTENT BELOW ========

\input{path/to/tex-output/parsed_chunked_output1.tex}
\input{path/to/tex-output/parsed_chunked_output2.tex}
\input{path/to/tex-output/parsed_chunked_output3.tex}
\input{path/to/tex-output/parsed_chunked_output4.tex}
\input{path/to/tex-output/parsed_chunked_output5.tex}

% ======== DROP CONTENT ENDS ========
```

Also update the report title:
```latex
\reportmaintitle{Ancestors of Your Person Name}
```

### Step 4: Compile to PDF

```bash
xelatex -output-directory="output/" -jobname="Family_Report" main_template.tex
```

---

## Command Examples

### Basic Usage
```bash
# Simple split with defaults
python split_file.py input.txt output_dir/

# Custom chunk size and naming
python split_file.py "Blake Tonda.txt" "chunks/" --lines 5000 --prefix "chunk"

# Full Windows path example
python split_file.py "data.txt" "D:/reports/chunks/" --prefix "parsed_chunked_output"
```

### Advanced Features
```bash
# Preview mode (see what will happen without doing it)
python split_file.py "large_file.txt" "output/" --dry-run

# Custom configuration
python split_file.py "input.txt" "output/" --lines 10000 --prefix "split_part"

# Get help
python split_file.py --help
```

---

## Help Output Example

When you run `python split_file.py --help`:

```
usage: split_file.py [-h] [--lines LINES] [--prefix PREFIX] [--dry-run] [input_file] [output_dir]

Split large genealogy text files at anchor points

positional arguments:
  input_file            Path to input text file
  output_dir            Directory to save split files

options:
  -h, --help            show this help message and exit
  --lines LINES, -l LINES
                        Approximate lines per chunk (default: 7000)
  --prefix PREFIX, -p PREFIX
                        Prefix for output files (default: "split")
  --dry-run             Show what would be done without actually splitting

Examples:
  python split_file.py input.txt output_dir/
  python split_file.py "Blake Tonda.txt" "chunks/" --lines 5000 --prefix "chunk"
  python split_file.py data.txt "D:/reports/chunks/" --prefix "parsed_chunked_output"

If no arguments provided, uses hardcoded defaults for backward compatibility.
```

---

## Parameters Explained

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `input_file` | - | Path to your text file | Required* |
| `output_dir` | - | Where to save chunks | Required* |
| `--lines` | `-l` | Lines per chunk | 7000 |
| `--prefix` | `-p` | Output filename prefix | "split" |
| `--dry-run` | - | Preview mode only | Off |

*Not required if using backward compatibility mode

---

## Real-World Examples

### Genealogy Report Processing
```bash
# Split a large ancestor report into 5 chunks
python split_file.py "Jeremiah Parranto - Ancestors.txt" "chunks/" --lines 14200 --prefix "parsed_chunked_output"

# Results in:
# parsed_chunked_output1.txt (lines 1-14,211)
# parsed_chunked_output2.txt (lines 14,212-28,412)
# ... and so on
```

### Safe Testing
```bash
# Always test first with dry-run
python split_file.py "my_big_file.txt" "test_output/" --dry-run

# Output shows:
# Would process 50000 lines into approximately 8 files
# Would create: test_output/split1.txt
# Would create: test_output/split2.txt
# ... etc
```

---

## XeLaTeX Compilation

After generating your .tex files, compile to PDF:

```bash
# Basic compilation
xelatex main_template.tex

# With custom output directory and job name
xelatex -output-directory="output/" -jobname="Ancestors_Report" main_template.tex

# Windows example with full paths
xelatex -output-directory="D:\reports\output" -jobname="Family_Report_v1" main_template.tex
```

**Note:** You may need to run xelatex twice if you have hyperlinks to ensure all cross-references are resolved.

---

## Error Handling

The tool validates everything and gives clear error messages:

- ✅ **File not found**: "Error: Input file 'filename.txt' not found!"
- ✅ **Permission issues**: "Error: Cannot create/access output directory"
- ✅ **Success feedback**: "✅ Split operation completed successfully!"
- ✅ **Failure feedback**: "❌ Split operation failed!"

---

## Tips & Best Practices

1. **Always use `--dry-run` first** to preview the operation before actually splitting
2. **Use consistent naming** with `--prefix` for easier file management
3. **Keep chunk sizes reasonable** (~14,000 lines) to avoid LaTeX memory issues
4. **Create a tex-output folder** to keep generated LaTeX files organized
5. **Back up your original files** before processing

---

## Quick Reference

```bash
# Most common command for genealogy reports
python split_file.py "report.txt" "chunks/" --lines 14200 --prefix "parsed_chunked_output"

# Convert to LaTeX
python generate_tex.py "chunks/parsed_chunked_output1.txt" "tex-output/parsed_chunked_output1.tex"

# Compile to PDF
xelatex -output-directory="output/" -jobname="Ancestors_Report" main_template.tex
```

**Pro tip**: Always use `--dry-run` first to preview the operation before actually splitting!
