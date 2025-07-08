#!/usr/bin/env python3
"""
Utility script to find and suggest fixes for table spacing issues.
Run this to identify pages that might need layout adjustments.
"""

import re
import os
from pathlib import Path

def find_potential_issues(file_path):
    """Find potential spacing issues in a Python file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Look for very narrow columns (md=1) that might need more space
    narrow_cols = re.findall(r'dbc\.Col\([^,]+,.*?md=1[^0-9]', content)
    if narrow_cols:
        issues.append(f"Found {len(narrow_cols)} very narrow columns (md=1)")
    
    # Look for missing responsive breakpoints
    col_patterns = re.findall(r'dbc\.Col\([^)]+\)', content)
    missing_responsive = [col for col in col_patterns if 'xs=' not in col and 'sm=' not in col]
    if missing_responsive:
        issues.append(f"Found {len(missing_responsive)} columns missing responsive breakpoints")
    
    # Check if tables have overflow handling
    datatable_patterns = re.findall(r'DataTable\([^)]+\)', content, re.DOTALL)
    missing_overflow = [dt for dt in datatable_patterns if 'overflowX' not in dt]
    if missing_overflow:
        issues.append(f"Found {len(missing_overflow)} DataTables without overflow handling")
    
    return issues

def main():
    pages_dir = Path('pages')
    problem_files = {}
    
    for py_file in pages_dir.rglob('*.py'):
        if py_file.name.startswith('_'):
            continue
            
        issues = find_potential_issues(py_file)
        if issues:
            problem_files[str(py_file)] = issues
    
    print("Potential spacing/layout issues found:")
    print("=" * 50)
    
    for file_path, issues in problem_files.items():
        print(f"\n{file_path}:")
        for issue in issues:
            print(f"  • {issue}")
    
    print(f"\nTotal files with potential issues: {len(problem_files)}")

if __name__ == "__main__":
    main()