#!/usr/bin/env python3
"""
Analyze pages for spacing issues and categorize by complexity.
"""
import re
import os
from pathlib import Path
from collections import defaultdict

def analyze_file(file_path):
    """Analyze a single file for spacing issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None
    
    issues = {
        'has_datatable': False,
        'has_dbc_col': False,
        'narrow_cols': 0,
        'missing_responsive': 0,
        'missing_overflow': 0,
        'bad_minwidth': 0,
        'bad_gutters': 0,
        'needs_container': False
    }
    
    # Check for DataTable
    if 'DataTable(' in content:
        issues['has_datatable'] = True
        
        # Check for missing overflow handling
        datatable_matches = re.findall(r'DataTable\([^)]+(?:\)[^)]*\))*[^)]*\)', content, re.DOTALL)
        for dt in datatable_matches:
            if 'overflowX' not in dt:
                issues['missing_overflow'] += 1
            if 'minWidth.*100%' in dt:
                issues['bad_minwidth'] += 1
    
    # Check for dbc.Col
    if 'dbc.Col(' in content:
        issues['has_dbc_col'] = True
        
        # Find narrow columns (md=1)
        narrow_matches = re.findall(r'dbc\.Col\([^)]+md=1[^0-9][^)]*\)', content)
        issues['narrow_cols'] = len(narrow_matches)
        
        # Find columns missing responsive breakpoints
        col_matches = re.findall(r'dbc\.Col\([^)]+\)', content)
        for col in col_matches:
            if 'xs=' not in col or 'sm=' not in col:
                issues['missing_responsive'] += 1
    
    # Check for bad gutter spacing
    if 'className="g-2"' in content or 'className="g-3"' in content:
        issues['bad_gutters'] += 1
    
    # Check if needs container wrapping
    if 'body = html.Div(row)' in content or 'body = html.Div([' in content:
        issues['needs_container'] = True
    
    return issues

def get_priority_score(issues):
    """Calculate priority score for a file."""
    if not issues:
        return 0
    
    score = 0
    if issues['has_datatable'] and issues['has_dbc_col']:
        score += 10  # High priority
    elif issues['has_datatable'] or issues['has_dbc_col']:
        score += 5   # Medium priority
    
    score += issues['narrow_cols'] * 2
    score += issues['missing_responsive']
    score += issues['missing_overflow'] * 2
    score += issues['bad_minwidth'] * 3
    score += issues['bad_gutters'] * 2
    if issues['needs_container']:
        score += 2
    
    return score

def main():
    pages_dir = Path('pages')
    chapters = defaultdict(list)
    
    # Group files by chapter (subfolder)
    for py_file in pages_dir.rglob('*.py'):
        if (py_file.name.endswith('_figtbl.py') or 
            py_file.name.startswith('__') or
            py_file.name in ['urls.py', 'formatting.py', 'register_pages.py']):
            continue
        
        chapter = py_file.parent.name
        if chapter == 'pages':
            chapter = 'root'
        
        issues = analyze_file(py_file)
        if issues:
            priority = get_priority_score(issues)
            chapters[chapter].append({
                'file': str(py_file),
                'issues': issues,
                'priority': priority
            })
    
    # Sort chapters by total priority
    chapter_priorities = {}
    for chapter, files in chapters.items():
        total_priority = sum(f['priority'] for f in files)
        chapter_priorities[chapter] = total_priority
        # Sort files within chapter by priority
        chapters[chapter] = sorted(files, key=lambda x: x['priority'], reverse=True)
    
    # Display results
    print("SPACING ISSUES ANALYSIS")
    print("=" * 60)
    
    sorted_chapters = sorted(chapter_priorities.items(), key=lambda x: x[1], reverse=True)
    
    for chapter, total_priority in sorted_chapters:
        if total_priority == 0:
            continue
            
        files = chapters[chapter]
        print(f"\n📁 {chapter.upper()} (Priority: {total_priority}, Files: {len(files)})")
        print("-" * 40)
        
        for file_info in files[:5]:  # Show top 5 files per chapter
            f = file_info['file']
            issues = file_info['issues']
            priority = file_info['priority']
            
            if priority == 0:
                continue
                
            print(f"  📄 {f.split('/')[-1]} (Score: {priority})")
            
            problems = []
            if issues['has_datatable'] and issues['has_dbc_col']:
                problems.append("Tables + Columns")
            elif issues['has_datatable']:
                problems.append("Tables only")
            elif issues['has_dbc_col']:
                problems.append("Columns only")
            
            if issues['narrow_cols']:
                problems.append(f"{issues['narrow_cols']} narrow cols")
            if issues['missing_responsive']:
                problems.append(f"{issues['missing_responsive']} missing responsive")
            if issues['missing_overflow']:
                problems.append(f"{issues['missing_overflow']} missing overflow")
            if issues['bad_minwidth']:
                problems.append(f"{issues['bad_minwidth']} bad minWidth")
            if issues['bad_gutters']:
                problems.append("bad gutters")
            if issues['needs_container']:
                problems.append("needs container")
            
            print(f"     Issues: {', '.join(problems)}")
        
        if len(files) > 5:
            print(f"     ... and {len(files) - 5} more files")
    
    print(f"\n📊 SUMMARY:")
    print(f"Total chapters with issues: {len([c for c, p in sorted_chapters if p > 0])}")
    print(f"Total files needing fixes: {sum(len(files) for files in chapters.values())}")
    
    # Recommend starting chapter
    if sorted_chapters and sorted_chapters[0][1] > 0:
        start_chapter = sorted_chapters[0][0]
        print(f"🎯 Recommended starting chapter: {start_chapter}")

if __name__ == "__main__":
    main()