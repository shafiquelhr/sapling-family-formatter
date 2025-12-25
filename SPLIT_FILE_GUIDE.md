# Split File Tool - User Guide

## Overview
Enhanced genealogy file splitter that breaks large text files into smaller chunks at anchor points (`##ANCHOR:iXXXXX##`). Now includes command-line interface, error handling, and flexible configuration.

## 🚀 Quick Start (Recommended)

**For most users, just run one of these:**

```bash
# Split your file into 5 chunks with custom naming
python split_file.py "your_file.txt" "output_folder/" --lines 14200 --prefix "parsed_chunked_output"

# Preview what will happen first (recommended)
python split_file.py "your_file.txt" "output_folder/" --lines 14200 --prefix "parsed_chunked_output" --dry-run
```

**That's it!** The tool handles everything else automatically.

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

### Backward Compatibility
```bash
# Old way still works (uses hardcoded defaults)
python split_file.py
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
# Split Blake Tonda report into 5 chunks
python split_file.py "Blake Tonda - Ancestor Report HTML.txt" "D:/reports/chunks/" --lines 14200 --prefix "parsed_chunked_output"

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

## Error Handling

The tool now validates everything and gives clear error messages:

- ✅ **File not found**: "Error: Input file 'filename.txt' not found!"
- ✅ **Permission issues**: "Error: Cannot create/access output directory"
- ✅ **Success feedback**: "✅ Split operation completed successfully!"
- ✅ **Failure feedback**: "❌ Split operation failed!"

---

## Migration from Old Version

**Old way (still works):**
```bash
python split_file.py  # Uses hardcoded values
```

**New recommended way:**
```bash
python split_file.py "your_file.txt" "output_dir/" --lines 14200 --prefix "parsed_chunked_output"
```

**Advantages of new way:**
- No code editing required
- Flexible file naming
- Better error handling
- Preview capability
- Works with any file/directory

---

## Quick Reference

```bash
# Most common command for genealogy reports
python split_file.py "report.txt" "chunks/" --lines 14200 --prefix "parsed_chunked_output"

# Preview first (recommended)
python split_file.py "report.txt" "chunks/" --lines 14200 --prefix "parsed_chunked_output" --dry-run

# Get help
python split_file.py -h
```

**Pro tip**: Always use `--dry-run` first to preview the operation before actually splitting!

### Actual Latex Command Example
xelatex -output-directory="D:\Kharcha Paani\manzoor\reports\r-five" -jobname="Ancestors_of_Blake_Tonda" main_template.tex
