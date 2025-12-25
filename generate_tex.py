#!/usr/bin/env python3
"""
Genealogical Text to LaTeX Converter
"""
import re
import sys
import os

def escape_latex(text):
    """Escape LaTeX special characters."""
    if text is None or text == "":
        return ""
    
    # Replace special characters with LaTeX equivalents
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('#', '\\#')
    text = text.replace('$', '\\$')
    text = text.replace('%', '\\%')
    text = text.replace('&', '\\&')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    
    return text

def process_text(text):
    """Process text for LaTeX output, including links and formatting."""
    # First, convert links to LaTeX
    result = ""
    rest = text
    
    # Process links using a regex pattern
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    
    last_end = 0
    for match in re.finditer(link_pattern, text):
        # Add text before the match
        result += escape_latex(text[last_end:match.start()])
        
        # Extract name and target
        name = match.group(1)
        target = match.group(2)
        
        # Check if it's a person link
        if target.startswith('#i') or target.startswith('i'):
            person_id = target.lstrip('#i')
            # Create a hyperlink to the person
            result += f"\\textcolor{{accent}}{{\\textbf{{\\underline{{\\hyperlink{{person{person_id}}}{{\\breakablename{{{escape_latex(name)}}}}}}}}}}}"
        elif target.startswith('http'):
            # Create a link to an external URL - escape the URL for LaTeX \href parameter
            result += f"\\textcolor{{accent}}{{\\href{{{escape_url(target)}}}{{{escape_latex(name)}}}}}"
        else:
            # Unknown link type, just escape it
            result += escape_latex(match.group(0))
        
        last_end = match.end()
    
    # Add remaining text
    result += escape_latex(text[last_end:])
    
    # Now add our line breaking commands (make sure not to add inside LaTeX commands)
    # Convert to a list of characters to make targeted replacements easier
    chars = list(result)
    i = 0
    while i < len(chars) - 3:
        # Skip over actual LaTeX commands
        if chars[i] == '\\' and i + 1 < len(chars) and chars[i + 1].isalpha():
            # Skip the backslash
            i += 1
            # Skip command name
            while i < len(chars) and chars[i].isalpha():
                i += 1
            # Skip arguments if any
            if i < len(chars) and chars[i] == '{':
                brace_count = 1
                i += 1
                while i < len(chars) and brace_count > 0:
                    if chars[i] == '{':
                        brace_count += 1
                    elif chars[i] == '}':
                        brace_count -= 1
                    i += 1
        else:
            # Check for common phrases to add breaks
            if i + 5 < len(chars) and ''.join(chars[i:i+4]) == " and":
                chars[i:i+4] = list(" and \\allowbreak ")
                i += 14  # "and" + "\\allowbreak" + space
            elif i + 4 < len(chars) and ''.join(chars[i:i+3]) == " of":
                chars[i:i+3] = list(" of \\allowbreak ")
                i += 13  # "of" + "\\allowbreak" + space
            elif i + 8 < len(chars) and ''.join(chars[i:i+7]) == " son of":
                chars[i:i+7] = list(" son of \\penalty10\\hspace{0pt} ")
                i += 24  # "son of" + "\\penalty10\\hspace{0pt}" + space
            elif i + 5 < len(chars) and ''.join(chars[i:i+4]) == " son":
                chars[i:i+4] = list(" son \\allowbreak ")
                i += 14  # "son" + "\\allowbreak" + space
            elif i + 10 < len(chars) and ''.join(chars[i:i+9]) == " daughter":
                chars[i:i+9] = list(" daughter \\allowbreak ")
                i += 19  # "daughter" + "\\allowbreak" + space
            else:
                i += 1
    
    return ''.join(chars)

def create_url_link(url):
    """Create a LaTeX hyperlink for a URL."""
    return f"\\href{{{url}}}{{\\small\\textcolor{{accent}}{{{url}}}}}"

def escape_url(url):
    """Escape special LaTeX characters in URLs while preserving the URL functionality."""
    # For URLs we need to handle underscores and other special characters differently
    # We use \url{} from the url package which properly formats URLs
    return url.replace("_", "\\_").replace("#", "\\#").replace("$", "\\$").replace("%", "\\%").replace("&", "\\&").replace("{", "\\{").replace("}", "\\}").replace("~", "\\~{}").replace("^", "\\^{}")

def process_child_entries(start_idx, lines, output):
    k = start_idx
    while k < len(lines):
        if not lines[k].strip():
            k += 1  # Skip empty lines
            continue
        
        child_line = lines[k].strip()
        
        # Skip if we've reached another section
        if child_line == "General Notes:" or child_line == "Biography:" or "married" in child_line:
            break
        
        # Process different types of child entries
        # Type 1: Reference number in parentheses, then roman numeral
        ref_roman_match = re.match(r'^\((\d+)\)\s+([ivxlcdm]+)\.\s+(.*?)(?:,\s+(.*))?$', child_line, re.IGNORECASE)
        if ref_roman_match:
            ref_number = ref_roman_match.group(1)
            roman_numeral = ref_roman_match.group(2)
            name_part = ref_roman_match.group(3)
            rest_part = ref_roman_match.group(4) if ref_roman_match.group(4) else ""
            
            # Check if name contains a link
            link_match = re.search(r'\[(.*?)\]\((.*?)\)', name_part)
            if link_match:
                # Process the link
                name_and_link = f"[{link_match.group(1)}]({link_match.group(2)})"
                processed_name = process_text(name_and_link)
            else:
                # Bold the name only
                processed_name = f"\\textbf{{{process_text(name_part)}}}"
            
            if rest_part:
                # Format with badge for reference number, unbolded roman numeral, and comma after name
                output.write(f"\\childentry{{\\badge{{{ref_number}}} {roman_numeral}. {processed_name},}}{{{process_text(rest_part)}}}\n\n")
            else:
                # No additional info
                output.write(f"\\childentry{{\\badge{{{ref_number}}} {roman_numeral}. {processed_name}}}{{}}\n\n")
        else:
            # Type 2: Just roman numeral
            roman_match = re.match(r'^([ivxlcdm]+)\.\s+(.*?)(?:(?:,|was)\s+(.*))?$', child_line, re.IGNORECASE)
            if roman_match:
                roman_numeral = roman_match.group(1)
                name_part = roman_match.group(2)
                rest_part = roman_match.group(3) if roman_match.group(3) else ""
                
                # Check if name contains a link
                link_match = re.search(r'\[(.*?)\]\((.*?)\)', name_part)
                if link_match:
                    # Process the link
                    name_and_link = f"[{link_match.group(1)}]({link_match.group(2)})"
                    processed_name = process_text(name_and_link)
                    
                    if rest_part:
                        # Add comma after name and include rest of text unbolded
                        output.write(f"\\childentry{{{roman_numeral}. {processed_name},}}{{{process_text(rest_part)}}}\n\n")
                    else:
                        # No additional info, just output the name
                        output.write(f"\\childentry{{{roman_numeral}. {processed_name}}}{{}}\n\n")
                else:
                    # Bold the name only, fix the spacing issue with comma
                    name_part = name_part.rstrip()  # Remove trailing spaces
                    processed_name = f"\\textbf{{{process_text(name_part)}}}"
                    
                    if rest_part:
                        # Add comma directly after name (no space) and include rest of text unbolded
                        output.write(f"\\childentry{{{roman_numeral}. {processed_name},}}{{{process_text(rest_part)}}}\n\n")
                    else:
                        # No additional info, just output the name
                        output.write(f"\\childentry{{{roman_numeral}. {processed_name}}}{{}}\n\n")
            else:
                # Fallback for any other format
                # Try to extract a name and additional info
                parts = child_line.split(',', 1)
                if len(parts) > 1:
                    name_part = parts[0].strip()
                    rest_part = parts[1].strip()
                    output.write(f"\\childentry{{\\textbf{{{process_text(name_part)}}},}}{{{process_text(rest_part)}}}\n\n")
                else:
                    # Just bold the entire line as a fallback
                    output.write(f"\\childentry{{\\textbf{{{process_text(child_line)}}}}}{{}}\n\n")
        
        k += 1
    
    return k

def main():
    """Main function."""
    if len(sys.argv) != 3:
        print("Usage: python generate_tex.py input.txt output.tex")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process content in a different way to handle all anchors correctly
    # First, find all lines starting with ##ANCHOR
    lines = content.split('\n')
    entries = []
    current_person_id = None
    current_content = []
    current_generation_title = None
    
    # Pattern to detect generation titles (e.g., "First Generation", "Second Generation (Parents)", etc.)
    # Supports both numeric (1st, 2nd, 100th, etc.) and word-based (First, Second, Hundredth, etc.)
    generation_title_pattern = r'^(?:\d+(?:st|nd|rd|th)|First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Thirtieth|Fortieth|Fiftieth|Sixtieth|Seventieth|Eightieth|Ninetieth|Hundredth)\s+Generation.*$'
    
    # Check if the file contains any anchor patterns
    has_anchors = any(line.strip().startswith('##ANCHOR:i') for line in lines)
    
    if has_anchors:
        # Original processing for files with anchors
        for line in lines:
            stripped_line = line.strip()
            
            # Check if this line is a generation title
            if re.match(generation_title_pattern, stripped_line, re.IGNORECASE):
                # Store the generation title to be added before the next person entry
                current_generation_title = stripped_line
                continue
            
            if stripped_line.startswith('##ANCHOR:i'):
                # If we have a previous entry, save it
                if current_person_id is not None and current_content:
                    entries.append((current_person_id, '\n'.join(current_content).strip(), None))
                    current_content = []
                
                # Extract new person ID
                match = re.search(r'##ANCHOR:i(\d+)##', stripped_line)
                if match:
                    current_person_id = match.group(1)
                else:
                    current_person_id = None
                    print(f"Warning: Could not extract person_id from anchor: '{stripped_line}'")
            else:
                # Add line to current content if we have a person ID
                if current_person_id is not None:
                    current_content.append(line)
        
        # Add the last entry if there is one
        if current_person_id is not None and current_content:
            entries.append((current_person_id, '\n'.join(current_content).strip(), None))
        
        # Now process entries and associate generation titles with the first person of each generation
        final_entries = []
        pending_generation_title = None
        
        # Re-parse to properly associate generation titles
        current_person_id = None
        current_content = []
        current_generation_title = None
        
        for line in lines:
            stripped_line = line.strip()
            
            # Check if this line is a generation title
            if re.match(generation_title_pattern, stripped_line, re.IGNORECASE):
                pending_generation_title = stripped_line
                continue
            
            if stripped_line.startswith('##ANCHOR:i'):
                # If we have a previous entry, save it
                if current_person_id is not None and current_content:
                    final_entries.append((current_person_id, '\n'.join(current_content).strip(), current_generation_title))
                    current_generation_title = None  # Reset after using it
                    current_content = []
                
                # Extract new person ID
                match = re.search(r'##ANCHOR:i(\d+)##', stripped_line)
                if match:
                    current_person_id = match.group(1)
                    # Assign the pending generation title to this person
                    if pending_generation_title:
                        current_generation_title = pending_generation_title
                        pending_generation_title = None
                else:
                    current_person_id = None
                    print(f"Warning: Could not extract person_id from anchor: '{stripped_line}'")
            else:
                # Add line to current content if we have a person ID
                if current_person_id is not None:
                    current_content.append(line)
        
        # Add the last entry if there is one
        if current_person_id is not None and current_content:
            final_entries.append((current_person_id, '\n'.join(current_content).strip(), current_generation_title))
        
        # Replace entries with final_entries
        entries = final_entries
    else:
        # Alternative processing for files without anchors
        print("No anchor patterns found in input file. Processing by person entries...")
        
        person_pattern = r'^(\d+)\.\s+(.*?)(?:,\s+|$)'
        generation_pattern = r'^([A-Za-z]+)\s+Generation'
        
        i = 0
        current_generation = "First"
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this is a generation header
            generation_match = re.match(generation_pattern, line)
            if generation_match:
                current_generation = generation_match.group(1)
                i += 1
                continue
            
            # Check if this is a new person entry
            person_match = re.match(person_pattern, line)
            if person_match:
                person_id = person_match.group(1)
                
                # Find the end of this person's entry
                start_idx = i
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    next_person_match = re.match(person_pattern, next_line)
                    next_gen_match = re.match(generation_pattern, next_line)
                    
                    if next_person_match or next_gen_match or i == len(lines) - 1:
                        # If we're at the last line, include it in the current entry
                        end_idx = i if (next_person_match or next_gen_match) else i + 1
                        # Extract the content for this person
                        person_content = '\n'.join(lines[start_idx:end_idx]).strip()
                        entries.append((person_id, person_content))
                        break
                    i += 1
            else:
                i += 1
    
    # Generate output
    with open(output_file, 'w', encoding='utf-8') as output:
        previous_had_generation_title = False
        
        for entry_idx, (person_id, entry_content, generation_title) in enumerate(entries):
            # Output generation title if present
            if generation_title:
                output.write(f"\\generationtitle{{{generation_title}}}\n\n")
                previous_had_generation_title = True
            
            lines = entry_content.split('\n')
            if not lines:
                continue
            
            # Process main entry line
            main_line = lines[0].strip()
            
            # Extract person entry number and name/additional info
            match = re.match(r'^(\d+)\.?\s+(.*?)(?:,\s+(.*))?$', main_line)
            if match:
                entry_number = match.group(1).strip()  # This is the person's unique number
                name = match.group(2).strip()
                additional_info = match.group(3) if match.group(3) else ""
            else:
                # Try with just name and additional info
                match = re.match(r'^(.*?)(?:,\s+(.*))?$', main_line)
                if match:
                    entry_number = ""
                    name = match.group(1).strip()
                    additional_info = match.group(2) if match.group(2) else ""
                else:
                    entry_number = ""
                    name = main_line.strip()
                    additional_info = ""
            
            # Check if the name contains biographical information like birth/death dates
            # Common phrases that indicate this isn't part of the name
            bio_markers = [
                r'was born', r'born', r'died', r'baptized', r'baptised', r'christened',
                r'married', r'buried', r'resided'
            ]
            
            # Create a regex pattern to find these markers
            bio_pattern = '|'.join(bio_markers)
            
            # Check if the name contains any of these markers
            name_parts = re.split(f'\\s+({bio_pattern})\\s+', name, maxsplit=1, flags=re.IGNORECASE)
            
            if len(name_parts) > 1:
                # We found a biographical marker in what was considered the name
                actual_name = name_parts[0].strip()
                # Reconstruct the additional info from the rest of the parts
                additional_text = ' '.join(name_parts[1:]).strip()
                
                # If we already have additional_info from a comma, prepend this bio info
                if additional_info:
                    additional_info = f"{additional_text}, {additional_info}"
                else:
                    additional_info = additional_text
                
                # Update the name to just the actual person's name
                name = actual_name
            
            # Check if the name contains suffixes like "Jr." or "Sr."
            # These should be included in the bolded name with the comma right after them
            name_with_suffix = name
            
            # First, handle specific suffixes like Jr. and Sr.
            # These should ALWAYS be included with the name and the comma should be right after them
            son_of_marker = " son of "
            daughter_of_marker = " daughter of "
            
            # Add handling specifically for Jr. and Sr. and other name suffixes
            # Step 1: Check if the name already has suffixes like Jr. or Sr. and ensure they stay with the name
            suffixes = ["Jr.", "Sr.", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
            
            # Improved approach for detecting suffixes - check for specific patterns
            # Check for specific suffix patterns with regex - enhanced pattern
            suffix_match = re.search(r'(.*?(?:\s+(?:Jr\.|Sr\.|II|III|IV|V|VI|VII|VIII|IX|X)\.?))(?:\s+(.*))?$', name_with_suffix, re.IGNORECASE)
            if suffix_match:
                # Extract the name with suffix
                name_with_suffix = suffix_match.group(1).strip()
                # If there's anything after the suffix that's not part of the name, move it to additional_info
                if suffix_match.group(2):
                    rest_of_line = suffix_match.group(2).strip()
                    if additional_info:
                        additional_info = f"{rest_of_line}, {additional_info}"
                    else:
                        additional_info = rest_of_line
            
            # Now handle son of/daughter of cases if not already handled
            if son_of_marker in name_with_suffix:
                parts = name_with_suffix.split(son_of_marker, 1)
                name_with_suffix = parts[0].strip()
                if len(parts) > 1 and additional_info:
                    additional_info = f"son of {parts[1]}, {additional_info}"
                elif len(parts) > 1:
                    additional_info = f"son of {parts[1]}"
            elif daughter_of_marker in name_with_suffix:
                parts = name_with_suffix.split(daughter_of_marker, 1)
                name_with_suffix = parts[0].strip()
                if len(parts) > 1 and additional_info:
                    additional_info = f"daughter of {parts[1]}, {additional_info}"
                elif len(parts) > 1:
                    additional_info = f"daughter of {parts[1]}"
            elif " and " in name_with_suffix:
                # Handle cases where name might include "and" followed by parent names
                # This checks if "and" is part of the title or connecting to parents
                and_parts = name_with_suffix.split(" and ", 1)
                if len(and_parts) > 1 and ("son of" in name_with_suffix or "daughter of" in name_with_suffix):
                    name_with_suffix = and_parts[0]
                    if additional_info:
                        additional_info = f"and {and_parts[1]}, {additional_info}"
                    else:
                        additional_info = f"and {and_parts[1]}"
            
            # Generate the main entry with properly bolded name
            name_fixed = process_text(name_with_suffix)
            name_bolded = f"\\textbf{{{name_fixed}}}"
            
            # Use the anchor ID only for the hyperlink target, but display the entry_number in the badge
            if additional_info:
                additional_info_fixed = process_text(additional_info)
                # Use person_id for hyperlink target and entry_number for display
                # Add a comma directly to the name
                output.write(f"\\entry{{{person_id}}}{{{entry_number}}}{{{name_bolded},}}{{{additional_info_fixed.strip()}}}\n\n")
            else:
                output.write(f"\\entry{{{person_id}}}{{{entry_number}}}{{{name_bolded}}}{{}}\n\n")
            
            # Process notes, biography, marriages and children
            i = 1
            has_notes = False
            has_bio = False
            bio_url = None
            
            while i < len(lines):
                line = lines[i].strip()
                
                # Process General Notes section
                if line == "General Notes:" or line.startswith("General Notes:"):
                    has_notes = True
                    notes = []
                    j = i + 1
                    
                    # If the notes are on the same line as the header
                    if line.startswith("General Notes:") and len(line) > 15:
                        # Extract the content after the colon
                        first_note = line.split(":", 1)[1].strip()
                        if first_note:
                            notes.append(first_note)
                    
                    # Extract the content of the General Notes section
                    # Keep collecting until we find Biography:, a marriage line, or a child line
                    is_marriage_found_in_notes = False
                    marriage_line_in_notes = None
                    is_child_heading_in_notes = False
                    child_heading_in_notes = None
                    
                    while j < len(lines):
                        current_line = lines[j].strip()
                        if current_line == "Biography:" or current_line.startswith("Biography:"):
                            break
                        
                        # Better detection for marriage lines - check if the line mentions marriage
                        # First-name or full-name followed by "married" should be treated as a marriage line
                        if "married" in current_line.lower() and (
                            current_line.lower().startswith(name.lower()) or
                            (len(name.split()) > 0 and current_line.lower().startswith(name.split()[0].lower()))
                        ):
                            is_marriage_found_in_notes = True
                            marriage_line_in_notes = current_line
                            
                            # Check if the next non-empty line is a child heading
                            next_j = j + 1
                            while next_j < len(lines) and not lines[next_j].strip():
                                next_j += 1
                            
                            if next_j < len(lines):
                                next_line = lines[next_j].strip()
                                if (next_line.lower().startswith("his child was:") or
                                    next_line.lower().startswith("his children were:") or
                                    next_line.lower().startswith("her child was:") or
                                    next_line.lower().startswith("her children were:") or
                                    (next_line.strip() and "child" in next_line.lower() and "from this marriage" in next_line.lower())):
                                    # We found a child heading after a marriage line within General Notes
                                    is_child_heading_in_notes = True
                                    child_heading_in_notes = next_line
                                    j = next_j  # Skip ahead to after the marriage line
                                    break
                            
                            # Don't break - we'll handle this separately
                            j += 1
                            continue
                        
                        # Check for child headings in General Notes
                        if (current_line.lower().startswith("his child was:") or 
                            current_line.lower().startswith("his children were:") or
                            current_line.lower().startswith("her child was:") or
                            current_line.lower().startswith("her children were:") or
                            (current_line.strip() and "child" in current_line.lower() and "from this marriage" in current_line.lower())):
                            is_child_heading_in_notes = True
                            child_heading_in_notes = current_line
                            break  # Break out of General Notes when we find a child heading
                        
                        if current_line:  # Only add non-empty lines
                            notes.append(current_line)
                        j += 1
                    
                    # Output the General Notes section
                    output.write(f"\\noindent \\textbf{{General Notes:}}\n")
                    
                    for note_line in notes:
                        notes_fixed = process_text(note_line)
                        output.write(f"{notes_fixed}\n")
                    
                    output.write("\n")
                    
                    # If we found a marriage line in the notes, process it as a marriage line
                    if is_marriage_found_in_notes and marriage_line_in_notes:
                        # Add an extra newline for proper spacing
                        output.write("\n")
                        marriage_line = process_text(marriage_line_in_notes)
                        output.write(f"\\marriage{{{marriage_line}}}\n\n")
                    
                    # If we found a child heading in the notes, process it now
                    if is_child_heading_in_notes and child_heading_in_notes:
                        # Add an extra newline for proper spacing if there was no marriage line
                        if not is_marriage_found_in_notes:
                            output.write("\n")
                        
                        # Process the child heading based on its type
                        if child_heading_in_notes.lower().startswith("his child was:"):
                            output.write("\\hischildheadingsingular\n\n")
                        elif child_heading_in_notes.lower().startswith("his children were:"):
                            output.write("\\hischildheadingplural\n\n")
                        elif child_heading_in_notes.lower().startswith("her child was:"):
                            output.write("\\herchildheadingsingular\n\n")
                        elif child_heading_in_notes.lower().startswith("her children were:"):
                            output.write("\\herchildheadingplural\n\n")
                        elif "children" in child_heading_in_notes.lower() and "from this marriage" in child_heading_in_notes.lower():
                            output.write("\\childrenheadingplural\n\n")
                        elif "child" in child_heading_in_notes.lower() and "from this marriage" in child_heading_in_notes.lower():
                            output.write("\\childrenheadingsingular\n\n")
                        
                        # Process the child entries
                        k = j + 1
                        k = process_child_entries(k, lines, output)
                        i = k
                        continue  # Skip to the next iteration after processing child entries
                    
                    i = j  # Move to the next section
                    continue
                
                # Process standalone Biography line
                if line == "Biography:" or line.startswith("Biography:"):
                    has_bio = True
                    
                    # If it's just "Biography:", look for content in the next lines
                    if line == "Biography:":
                        j = i + 1
                        bio_content = []
                        
                        # Extract the content of the Biography section
                        while j < len(lines):
                            current_line = lines[j].strip()
                            if current_line.startswith("married") or current_line == "The child from this marriage was:" or current_line == "Children from this marriage were:":
                                break
                            if current_line:  # Only add non-empty lines
                                bio_content.append(current_line)
                            j += 1
                        
                        output.write(f"\\noindent \\textbf{{Biography:}}\n")
                        
                        for bio_line in bio_content:
                            if bio_line.startswith("http://") or bio_line.startswith("https://"):
                                output.write(f"\\href{{{bio_line}}}{{\\small\\textcolor{{accent}}{{{escape_url(bio_line)}}}}}\n")
                            else:
                                bio_fixed = process_text(bio_line)
                                output.write(f"{bio_fixed}\n")
                        
                        output.write("\n")
                        i = j  # Move to the next section
                    else:
                        # If the URL is in the same line (Biography: http://...)
                        parts = line.split(":", 1)
                        if len(parts) > 1:
                            bio_url = parts[1].strip()
                            output.write(f"\\noindent \\textbf{{Biography:}}\n")
                            output.write(f"\\href{{{bio_url}}}{{\\small\\textcolor{{accent}}{{{escape_url(bio_url)}}}}}\n\n")
                        
                        i += 1  # Move to the next line
                    
                    continue
                
                # Process Marriage section
                if "married" in line.lower() or (line.strip() and (line.strip().startswith(name.split()[0]) or line.strip().startswith(name))):
                    # If we just finished processing General Notes and didn't add Biography, make sure we add an extra newline
                    if has_notes and not has_bio:
                        # We already wrote one newline at the end of General Notes, but we need one more for proper spacing
                        output.write("\n")
                    
                    # Process the marriage line with LaTeX formatting commands
                    marriage_line = process_text(line)
                    
                    # Use the marriage command which now has proper spacing built in
                    # The \marriage command in LaTeX already includes \vspace{0.5em} and proper indentation
                    output.write(f"\\marriage{{{marriage_line}}}\n\n")
                    
                    # Find children heading and process children
                    j = i + 1
                    while j < len(lines):
                        # Match various types of children headings
                        current_line = lines[j].strip()
                        is_child_heading = False
                        is_plural = False
                        child_heading_type = None
                        
                        # Check for all possible child heading patterns
                        if current_line and "child" in current_line.lower():
                            # New patterns for His/Her child/children
                            if current_line.lower().startswith("his child was:"):
                                is_child_heading = True
                                is_plural = False
                                child_heading_type = "his_singular"
                            elif current_line.lower().startswith("his children were:"):
                                is_child_heading = True
                                is_plural = True
                                child_heading_type = "his_plural"
                            elif current_line.lower().startswith("her child was:"):
                                is_child_heading = True
                                is_plural = False
                                child_heading_type = "her_singular"
                            elif current_line.lower().startswith("her children were:"):
                                is_child_heading = True
                                is_plural = True
                                child_heading_type = "her_plural"
                            # Original patterns
                            elif "from this marriage" in current_line.lower():
                                is_child_heading = True
                                is_plural = "children" in current_line.lower()
                                child_heading_type = "marriage"
                        
                        if is_child_heading:
                            # Add extra newline for spacing
                            output.write("\n")
                            
                            # Output appropriate children heading based on type
                            if child_heading_type == "his_singular":
                                output.write("\\hischildheadingsingular\n\n")
                            elif child_heading_type == "his_plural":
                                output.write("\\hischildheadingplural\n\n")
                            elif child_heading_type == "her_singular":
                                output.write("\\herchildheadingsingular\n\n")
                            elif child_heading_type == "her_plural":
                                output.write("\\herchildheadingplural\n\n")
                            elif is_plural:
                                output.write("\\childrenheadingplural\n\n")
                            else:
                                output.write("\\childrenheadingsingular\n\n")
                            
                            # Process all subsequent lines with content as child entries
                            k = j + 1
                            k = process_child_entries(k, lines, output)
                            
                            i = k
                            break
                        
                        j += 1
                    
                    if j >= len(lines):
                        i += 1
                    else:
                        i = j
                    continue
                
                i += 1
            
            # Add divider line for all except the last entry
            # BUT: don't add divider if the current entry has a generation title
            if entry_idx < len(entries) - 1:
                # Check if the NEXT entry has a generation title
                next_entry = entries[entry_idx + 1]
                next_has_generation_title = next_entry[2] is not None if len(next_entry) > 2 else False
                
                # Only add divider if next entry doesn't have a generation title
                if not next_has_generation_title:
                    output.write("\\dividerline\n\n")
    
    print(f"Successfully converted {input_file} to {output_file}")

if __name__ == "__main__":
    main() 
