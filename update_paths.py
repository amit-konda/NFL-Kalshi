"""
Quick script to update all file paths in analysis scripts after reorganization.
"""

import os
import re

def update_file(filepath, replacements):
    """Update file paths in a given file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {filepath}")
        return True
    else:
        print(f"⏭️  No changes: {filepath}")
        return False

# Define path replacements for analysis scripts
analysis_replacements = {
    '"nfl_unified_data.csv"': '"../../results/data/nfl_unified_data.csv"',
    "'nfl_unified_data.csv'": "'../../results/data/nfl_unified_data.csv'",
    
    '"opening_possession_stratified_stats.csv"': '"../../results/analysis/opening_possession_stratified_stats.csv"',
    "'opening_possession_stratified_stats.csv'": "'../../results/analysis/opening_possession_stratified_stats.csv'",
    
    '"logistic_regression_results.csv"': '"../../results/analysis/logistic_regression_results.csv"',
    "'logistic_regression_results.csv'": "'../../results/analysis/logistic_regression_results.csv'",
    
    '"controlled_first_td_results.csv"': '"../../results/analysis/controlled_first_td_results.csv"',
    "'controlled_first_td_results.csv'": "'../../results/analysis/controlled_first_td_results.csv'",
    
    "'visualizations/": "'../../visualizations/",
    '"visualizations/': '"../../visualizations/',
}

# Define path replacements for dashboard (at root)
dashboard_replacements = {
    '"nfl_unified_data.csv"': '"results/data/nfl_unified_data.csv"',
    "'nfl_unified_data.csv'": "'results/data/nfl_unified_data.csv'",
    
    '"opening_possession_stratified_stats.csv"': '"results/analysis/opening_possession_stratified_stats.csv"',
    "'opening_possession_stratified_stats.csv'": "'results/analysis/opening_possession_stratified_stats.csv'",
    
    '"logistic_regression_results.csv"': '"results/analysis/logistic_regression_results.csv"',
    "'logistic_regression_results.csv'": "'results/analysis/logistic_regression_results.csv'",
}

print("="*60)
print("Updating file paths in analysis scripts...")
print("="*60)

# Update analysis scripts
analysis_scripts = [
    'scripts/analysis/first_td_correlations.py',
    'scripts/analysis/logistic_regression_analysis.py',
    'scripts/analysis/controlled_first_td_analysis.py',
    'scripts/analysis/opening_possession_analysis.py',
    'scripts/analysis/visualize_odds_v2.py',
    'scripts/analysis/visualize_opening_possession.py',
]

for script in analysis_scripts:
    if os.path.exists(script):
        update_file(script, analysis_replacements)

print("\n" + "="*60)
print("Updating file paths in dashboard...")
print("="*60)

if os.path.exists('dashboard.py'):
    update_file('dashboard.py', dashboard_replacements)

print("\n✅ All paths updated!")

