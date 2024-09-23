# Git-Blame-Analyzer

This Python script counts the number of lines each author contributed to specified files in a Git repository, excluding comments and empty lines. It also supports the normalization of author names via aliases, allowing you to unify contributions from multiple aliases or variations of the same name.

## Features
- Counts lines of code contributed by each team member for specific files.
- Excludes comments and empty lines.
- Handles Ruby-style comments (`#`, `=begin`, `=end`).
- Supports the use of aliases to merge contributions from different names used by the same person.

## Requirements
- Python 3.x
- Git installed on your system

## Usage

1. Make sure the source code has been git cloned to have access to git blame.

2. Place the python script in folder directory.

3. You may need to update the author_aliases dictionary after running the code.

4. Run the script. Usage:
```bash
python3 <script_name.py> file1.rb file2.rb file3.rb
```

5. The script will output the contributions for each author, showing the number of lines they contributed to each file, excluding comments and empty lines. It will also show the total lines contributed by each author.



## How to update the `author_aliases` Dictionary
In Git, users can configure their author name and email address differently for each commit. This may result in one person appearing with different names or email addresses (e.g., "devDude123" vs. "Sam Developer"). The author_aliases dictionary is provided so you can normalize these names and aggregate contributions from the same person, even if they used different aliases.

Open the Python script and update the author_aliases dictionary if there are contributors who used multiple aliases or slightly different names. This allows you to combine their contributions under a single, canonical name.

```python
author_aliases = {
    "devDude123": "Sam Developer",
    "codeMaster2020": "Alex Coder",
}
```

You can freely update the `author_aliases` dictionary to reflect any new aliases or changes in the way team members are identifying themselves in their Git commits.
