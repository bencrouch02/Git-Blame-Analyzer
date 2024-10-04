import os
import subprocess
import sys
from collections import defaultdict

# Define a dictionary to normalize author names with multiple aliases
author_aliases = {
    "senchy26": "Ryan Senchyshak",
    "Hzzzzzzz777": "Zhi(Tom) Huang",
    # Add more aliases as needed for each team member
}

def normalize_author_name(author):
    """Normalize the author name using the alias dictionary."""
    return author_aliases.get(author, author)  # Return the canonical name if an alias exists

def get_git_blame(file_path):
    """Run git blame on the file and return a list of authors per line."""
    try:
        blame_output = subprocess.run(
            ["git", "blame", "--line-porcelain", file_path], 
            capture_output=True, 
            text=True
        )
        if blame_output.returncode != 0:
            print(f"Error running git blame on {file_path}: {blame_output.stderr}")
            return None
        return blame_output.stdout
    except Exception as e:
        print(f"Failed to run git blame on {file_path}: {e}")
        return None

def count_contributions(files_to_check):
    """Count the actual lines of code each author contributed to each specified file."""
    contributions = defaultdict(lambda: defaultdict(list))  # contributions[author][file] = list_of_lines
    in_multiline_comment = False  # Track whether we are inside a multi-line comment block

    for file in files_to_check:
        blame_output = get_git_blame(file)
        
        if blame_output is None:
            continue
        
        # Process each line of the blame output
        blame_lines = blame_output.splitlines()
        author = None
        
        for line in blame_lines:
            # Look for the author line, which is formatted like this: "author Name"
            if line.startswith("author "):
                raw_author = line[7:].strip()  # Extract the author's name and strip extra spaces
                normalized_author = normalize_author_name(raw_author)  # Normalize using alias dictionary
                author = normalized_author
            elif line.startswith("\t"):  # This marks the start of actual code lines
                actual_code_line = line[1:].strip()  # The actual code part (skip the tab)
                
                # Handle multi-line comment blocks in Ruby (from '=begin' to '=end')
                if actual_code_line.startswith('=begin'):
                    in_multiline_comment = True
                elif actual_code_line.startswith('=end'):
                    in_multiline_comment = False
                    continue  # Skip the =end line itself

                # Skip lines inside multi-line comments
                if in_multiline_comment:
                    continue

                # Exclude empty lines and single-line comments (lines that start with #)
                if actual_code_line and not actual_code_line.startswith("#"):
                    if author:  # Only tally if we have an author name
                        contributions[author][file].append(actual_code_line)

    return contributions

def store_contributions_in_files(contributions, output_dir="author_contributions"):
    """Store the actual code contributions in separate files for each author in a specified folder."""
    # Create the folder if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for author, files in contributions.items():
        # Create a file for the author in the specified output directory
        file_name = os.path.join(output_dir, f"{author}_contributions.rb")
        with open(file_name, "w") as author_file:
            for file, lines in files.items():
                author_file.write(f"## File: {file}\n")
                for line in lines:
                    author_file.write(f"{line}\n")  # Use !r to preserve white space
                author_file.write("\n")

def print_contributions(contributions):
    """Print the number of lines each author contributed without printing actual code."""
    if not contributions:
        print("No contributions found.")
        return

    for author, files in contributions.items():
        print(f"Author: {author}")
        total_lines = 0
        for file, lines in files.items():
            print(f"  {file}: {len(lines)} lines")
            total_lines += len(lines)
        print(f"  Total lines: {total_lines}")
        print()

if __name__ == "__main__":
    # Ensure there is at least one file argument
    if len(sys.argv) < 2:
        print("Usage: python3 code.py <file1> [<file2> ... <fileN>]")
        sys.exit(1)

    # Get the list of files to check from the command-line arguments
    files_to_check = sys.argv[1:]

    # Check if the files exist in the current directory
    for file in files_to_check:
        if not os.path.isfile(file):
            print(f"Error: The file '{file}' does not exist in the current directory.")
            sys.exit(1)

    # Run the contribution count function
    contributions = count_contributions(files_to_check)

    # Store the contributions in files in the specified directory
    store_contributions_in_files(contributions)

    # Print the contributions, including totals
    print_contributions(contributions)
