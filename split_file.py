#!/usr/bin/env python3
"""
File Splitter - Splits large text files at specified anchors
Enhanced with command-line interface and better error handling
"""
import re
import os
import sys
import argparse

def split_file(input_file, output_dir, lines_per_file=7000, prefix="split"):
    """
    Split a large text file into smaller files at anchor points.
    
    The function will split the file approximately every 'lines_per_file' lines,
    but will look for an anchor pattern (##ANCHOR:iXXXXX##) near that point.
    The split will occur just before the anchor pattern.
    
    Args:
        input_file (str): Path to the input text file
        output_dir (str): Directory where split files will be created
        lines_per_file (int): Approximate number of lines per output file
        prefix (str): Prefix for output filenames (default: "split")
    
    Returns:
        bool: True if successful, False if there were errors
    """
    # Validate input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    # Validate input file is readable
    try:
        with open(input_file, 'r', encoding='utf-8') as test_file:
            test_file.readline()
    except (IOError, UnicodeDecodeError) as e:
        print(f"Error: Cannot read input file '{input_file}': {e}")
        return False
    # Make sure the output directory exists and is writable
    try:
        os.makedirs(output_dir, exist_ok=True)
    except (PermissionError, OSError) as e:
        print(f"Error: Cannot create/access output directory '{output_dir}': {e}")
        return False
    
    # Read the entire input file
    with open(input_file, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    total_lines = len(all_lines)
    print(f"Total lines in input file: {total_lines}")
    
    start_line = 0
    file_count = 0
    
    while start_line < total_lines:
        file_count += 1
        
        # Calculate the approximate end line for this chunk
        approx_end_line = min(start_line + lines_per_file, total_lines)
        
        # If we're at the end of the file, use all remaining lines
        if approx_end_line >= total_lines:
            end_line = total_lines
        else:
            # Look for an anchor pattern after the approximate end line
            found_anchor = False
            search_line = approx_end_line
            
            # Search up to 200 lines after the approximate end line
            max_search = min(approx_end_line + 200, total_lines)
            
            for i in range(approx_end_line, max_search):
                if re.match(r'##ANCHOR:i\d+##', all_lines[i].strip()):
                    end_line = i  # Split just before this line
                    found_anchor = True
                    break
            
            # If no anchor is found, use the approximate end line
            if not found_anchor:
                print(f"Warning: No anchor found near line {approx_end_line}, using exact line number")
                end_line = approx_end_line
        
        # Create the output file name using the prefix
        output_file = os.path.join(output_dir, f"{prefix}{file_count}.txt")
        
        # Extract the chunk of lines and write to output file
        try:
            chunk = all_lines[start_line:end_line]
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(chunk)
            
            print(f"Created {output_file} with lines {start_line+1} to {end_line}")
        except (IOError, PermissionError) as e:
            print(f"Error: Cannot write to file '{output_file}': {e}")
            return False
        
        # Set the start line for the next chunk
        start_line = end_line
    
    print(f"Splitting complete. Created {file_count} files.")
    return True

def main():
    """Main function with command-line interface and fallback to hardcoded values."""
    parser = argparse.ArgumentParser(
        description='Split large genealogy text files at anchor points',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python split_file.py input.txt output_dir/
  python split_file.py "Blake Tonda.txt" "chunks/" --lines 5000 --prefix "chunk"
  python split_file.py data.txt "D:/reports/chunks/" --prefix "parsed_chunked_output"
  
If no arguments provided, uses hardcoded defaults for backward compatibility.
        """
    )
    
    parser.add_argument('input_file', nargs='?', help='Path to input text file')
    parser.add_argument('output_dir', nargs='?', help='Directory to save split files')
    parser.add_argument('--lines', '-l', type=int, default=7000,
                       help='Approximate lines per chunk (default: 7000)')
    parser.add_argument('--prefix', '-p', default='split',
                       help='Prefix for output files (default: "split")')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without actually splitting')
    
    args = parser.parse_args()
    
    # If no arguments provided, use hardcoded defaults for backward compatibility
    if args.input_file is None or args.output_dir is None:
        print("No arguments provided, using hardcoded defaults...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(current_dir, "henkelmann_input.txt")
        output_dir = os.path.join(current_dir, "splits")
        lines_per_file = 14200
        prefix = "split"
    else:
        input_file = args.input_file
        output_dir = args.output_dir
        lines_per_file = args.lines
        prefix = args.prefix
    
    # Show configuration
    print(f"Configuration:")
    print(f"  Input file: {input_file}")
    print(f"  Output directory: {output_dir}")
    print(f"  Lines per file: {lines_per_file}")
    print(f"  File prefix: {prefix}")
    
    if args.dry_run:
        print("\n*** DRY RUN MODE - No files will be created ***")
        if os.path.exists(input_file):
            with open(input_file, 'r', encoding='utf-8') as f:
                total_lines = sum(1 for line in f)
            estimated_files = (total_lines + lines_per_file - 1) // lines_per_file
            print(f"Would process {total_lines} lines into approximately {estimated_files} files")
            for i in range(1, estimated_files + 1):
                print(f"  Would create: {os.path.join(output_dir, f'{prefix}{i}.txt')}")
        else:
            print(f"Input file '{input_file}' not found!")
        return
    
    # Perform the split
    success = split_file(input_file, output_dir, lines_per_file, prefix)
    
    if success:
        print("\n✅ Split operation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Split operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
