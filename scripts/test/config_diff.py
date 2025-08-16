FILE: /ccie/ccie/scripts/test/config_diff.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: config_diff.py
Purpose: Compare two configuration files to identify differences.
Author: zwu Network Automation Team
Date: [Date]
"""

import sys

def read_file(file_path):
    """Read the contents of a file and return as a list of lines."""
    with open(file_path, 'r') as file:
        return file.readlines()

def compare_configs(config1, config2):
    """Compare two configuration files and print the differences."""
    differences = []
    for line in config1:
        if line not in config2:
            differences.append(f"- {line.strip()}")
    for line in config2:
        if line not in config1:
            differences.append(f"+ {line.strip()}")
    return differences

def main(file1, file2):
    """Main function to compare two configuration files."""
    config1 = read_file(file1)
    config2 = read_file(file2)

    differences = compare_configs(config1, config2)

    if differences:
        print("Differences found:")
        for diff in differences:
            print(diff)
    else:
        print("No differences found.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: config_diff.py <config_file_1> <config_file_2>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
----------------------------------------