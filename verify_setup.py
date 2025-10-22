"""
Verification script to ensure all data and scripts are properly configured.
"""

import pandas as pd
import os

print("="*80)
print("NFL-KALSHI PROJECT VERIFICATION")
print("="*80)

# Check main data file
print("\n1. Checking main data file...")
data_path = "results/data/nfl_unified_data.csv"
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    print(f"   ✅ {data_path} exists")
    print(f"   ✅ {len(df)} games loaded")
    print(f"   ✅ {len(df.columns)} columns")
    
    # Check key columns
    required_columns = [
        'game_id', 'season', 'home_team', 'away_team',
        'first_td_team', 'winner', 'first_td_team_won',
        'home_prob', 'away_prob', 'favored_team',
        'opening_possession_team', 'home_got_ball_first'
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"   ❌ Missing columns: {missing}")
    else:
        print(f"   ✅ All required columns present")
else:
    print(f"   ❌ {data_path} not found!")
    print("   Run: cd scripts/data && python3 generate_unified_data.py")

# Check legacy files (should not exist)
print("\n2. Checking for legacy files (should be removed)...")
legacy_files = [
    "first_td_win_odds.csv",
    "nfl_pregame_odds_analysis.csv", 
    "nfl_pregame_odds_analysis_with_possession.csv",
    "first_td_analysis.py",
    "pregame_odds_analysis.py",
    "visualize_odds.py",
    "consolidate_data.py"
]
legacy_found = False
for file in legacy_files:
    if os.path.exists(file):
        print(f"   ⚠️  {file} still exists (can be deleted)")
        legacy_found = True

if not legacy_found:
    print(f"   ✅ All legacy files cleaned up")

# Check visualization files
print("\n3. Checking visualization outputs...")
viz_files = {
    "visualizations/first_td_correlations.png": "Correlation analysis",
    "visualizations/logistic_regression_analysis.png": "Logistic regression",
    "visualizations/first_td_marginal_effects.png": "Marginal effects (5%)",
    "visualizations/first_td_marginal_effects_1pct.png": "Marginal effects (1%)",
    "visualizations/first_td_raw_data_scatter.png": "Raw data scatter",
    "visualizations/first_td_win_probability_curves.png": "Win probability curves (1%)",
    "visualizations/first_td_win_probability_curves_5pct.png": "Win probability curves (5%)"
}
for file, desc in viz_files.items():
    if os.path.exists(file):
        size = os.path.getsize(file) / 1024  # KB
        print(f"   ✅ {desc}: {file} ({size:.1f} KB)")
    else:
        print(f"   ❌ {file} missing (run controlled_first_td_analysis.py)")

# Check scripts
print("\n4. Checking scripts...")
script_paths = {
    "scripts/data/generate_unified_data.py": "Main data generation",
    "scripts/analysis/controlled_first_td_analysis.py": "Main regression analysis (all-in-one)"
}
for script, description in script_paths.items():
    if os.path.exists(script):
        print(f"   ✅ {description}: {script}")
    else:
        print(f"   ❌ {script} missing")

# Check analysis results
print("\n5. Checking analysis results...")
result_files = {
    "results/analysis/controlled_first_td_results.csv": "Controlled analysis results",
    "results/analysis/first_td_marginal_effects.csv": "Marginal effects (5%)",
    "results/analysis/first_td_marginal_effects_1pct.csv": "Marginal effects (1%)",
    "results/analysis/first_td_win_probabilities.csv": "Win probabilities (1%)",
    "results/analysis/first_td_win_probabilities_5pct.csv": "Win probabilities (5%)"
}
for file, desc in result_files.items():
    if os.path.exists(file):
        print(f"   ✅ {desc}: {file}")
    else:
        print(f"   ⚠️  {file} not generated yet (run controlled_first_td_analysis.py)")

# Quick data quality check
print("\n6. Data quality checks...")
if 'df' in locals():
    print(f"   ✅ Seasons: {df['season'].min()}-{df['season'].max()}")
    print(f"   ✅ Unique teams: {df['home_team'].nunique()}")
    
    completeness = {
        'First TD': df['first_td_team'].notna().sum() / len(df) * 100,
        'Moneyline': df['home_moneyline'].notna().sum() / len(df) * 100,
        'Opening possession': df['opening_possession_team'].notna().sum() / len(df) * 100
    }
    
    for metric, pct in completeness.items():
        status = "✅" if pct == 100 else "⚠️"
        print(f"   {status} {metric}: {pct:.1f}% complete")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80)
print("\n📚 Read docs/README.md for detailed documentation")
print("🚀 Run 'cd scripts/data && python3 generate_unified_data.py' to regenerate data")
print("📊 Run 'cd scripts/analysis && python3 controlled_first_td_analysis.py' for all analysis")
print("🎯 Run 'streamlit run dashboard.py' to launch interactive dashboard")

