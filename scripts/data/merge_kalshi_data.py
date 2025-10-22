"""
Merge Kalshi data with unified NFL dataset
"""

import pandas as pd
import os
import sys

# Add project root to path
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

def load_datasets():
    """Load both the unified NFL dataset and Kalshi dataset"""
    print("Loading datasets...")
    
    # Load unified NFL dataset
    nfl_file = os.path.join(PROJECT_ROOT, "results", "data", "nfl_unified_data.csv")
    if not os.path.exists(nfl_file):
        print(f"Error: {nfl_file} not found. Run generate_unified_data.py first.")
        return None, None
    
    nfl_df = pd.read_csv(nfl_file)
    print(f"Loaded {len(nfl_df)} games from unified dataset")
    
    # Load Kalshi dataset
    kalshi_file = os.path.join(PROJECT_ROOT, "results", "data", "kalshi_nfl_data.csv")
    if not os.path.exists(kalshi_file):
        print(f"Error: {kalshi_file} not found. Run fetch_kalshi_data.py first.")
        return None, None
    
    kalshi_df = pd.read_csv(kalshi_file)
    print(f"Loaded {len(kalshi_df)} games from Kalshi dataset")
    
    return nfl_df, kalshi_df

def merge_datasets(nfl_df, kalshi_df):
    """Merge the datasets on game_id"""
    print("Merging datasets...")
    
    # Merge on game_id with left join to keep all NFL games
    merged_df = pd.merge(
        nfl_df,
        kalshi_df,
        on='game_id',
        how='left'
    )
    
    print(f"Merged dataset contains {len(merged_df)} games")
    print(f"Games with Kalshi data: {merged_df['kalshi_ticker'].notna().sum()}")
    print(f"Games without Kalshi data: {merged_df['kalshi_ticker'].isna().sum()}")
    
    return merged_df

def add_derived_columns(merged_df):
    """Add derived columns for analysis"""
    print("Adding derived columns...")
    
    # Kalshi vs Vegas probability differences
    merged_df['kalshi_vs_vegas_home_diff'] = (
        merged_df['pregame_home_prob_kalshi'] - merged_df['home_prob']
    )
    merged_df['kalshi_vs_vegas_away_diff'] = (
        merged_df['pregame_away_prob_kalshi'] - merged_df['away_prob']
    )
    
    # Absolute differences
    merged_df['kalshi_vs_vegas_home_abs_diff'] = merged_df['kalshi_vs_vegas_home_diff'].abs()
    merged_df['kalshi_vs_vegas_away_abs_diff'] = merged_df['kalshi_vs_vegas_away_diff'].abs()
    
    # First TD impact on Kalshi odds
    merged_df['kalshi_first_td_impact_home'] = merged_df['prob_change_home']
    merged_df['kalshi_first_td_impact_away'] = merged_df['prob_change_away']
    
    # Total probability change (should be close to 0 for valid data)
    merged_df['kalshi_total_prob_change'] = (
        merged_df['prob_change_home'] + merged_df['prob_change_away']
    )
    
    # Data quality indicators
    merged_df['has_kalshi_data'] = merged_df['kalshi_ticker'].notna().astype(int)
    merged_df['has_complete_kalshi_data'] = (
        (merged_df['data_quality_flag'] == 'complete').astype(int)
    )
    
    # Season-based analysis
    merged_df['kalshi_era'] = (merged_df['season'] >= 2021).astype(int)
    
    return merged_df

def generate_summary_stats(merged_df):
    """Generate summary statistics for the merged dataset"""
    print("\n" + "="*80)
    print("MERGED DATASET SUMMARY")
    print("="*80)
    
    # Basic counts
    total_games = len(merged_df)
    games_with_kalshi = merged_df['has_kalshi_data'].sum()
    games_with_complete_kalshi = merged_df['has_complete_kalshi_data'].sum()
    
    print(f"Total games: {total_games}")
    print(f"Games with Kalshi data: {games_with_kalshi} ({games_with_kalshi/total_games*100:.1f}%)")
    print(f"Games with complete Kalshi data: {games_with_complete_kalshi} ({games_with_complete_kalshi/total_games*100:.1f}%)")
    
    # Kalshi vs Vegas differences (for games with Kalshi data)
    kalshi_games = merged_df[merged_df['has_kalshi_data'] == 1]
    
    if len(kalshi_games) > 0:
        print(f"\nKalshi vs Vegas Probability Differences:")
        print(f"  Home team avg difference: {kalshi_games['kalshi_vs_vegas_home_diff'].mean():.4f}")
        print(f"  Away team avg difference: {kalshi_games['kalshi_vs_vegas_away_diff'].mean():.4f}")
        print(f"  Home team avg abs difference: {kalshi_games['kalshi_vs_vegas_home_abs_diff'].mean():.4f}")
        print(f"  Away team avg abs difference: {kalshi_games['kalshi_vs_vegas_away_abs_diff'].mean():.4f}")
        
        # First TD impact
        complete_kalshi = merged_df[merged_df['has_complete_kalshi_data'] == 1]
        if len(complete_kalshi) > 0:
            print(f"\nFirst TD Impact on Kalshi Odds:")
            print(f"  Avg home probability change: {complete_kalshi['prob_change_home'].mean():.4f}")
            print(f"  Avg away probability change: {complete_kalshi['prob_change_away'].mean():.4f}")
            print(f"  Avg total probability change: {complete_kalshi['kalshi_total_prob_change'].mean():.4f}")
    
    # Season breakdown
    print(f"\nSeason Breakdown:")
    season_stats = merged_df.groupby('season').agg({
        'has_kalshi_data': ['count', 'sum'],
        'has_complete_kalshi_data': 'sum'
    }).round(2)
    season_stats.columns = ['Total_Games', 'With_Kalshi', 'Complete_Kalshi']
    season_stats['Kalshi_Pct'] = (season_stats['With_Kalshi'] / season_stats['Total_Games'] * 100).round(1)
    print(season_stats)

def main():
    """Main execution function"""
    print("="*80)
    print("KALSHI DATA MERGING")
    print("="*80)
    
    # Load datasets
    nfl_df, kalshi_df = load_datasets()
    if nfl_df is None or kalshi_df is None:
        return
    
    # Merge datasets
    merged_df = merge_datasets(nfl_df, kalshi_df)
    
    # Add derived columns
    merged_df = add_derived_columns(merged_df)
    
    # Save merged dataset
    output_file = os.path.join(PROJECT_ROOT, "results", "data", "nfl_unified_with_kalshi.csv")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    merged_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Merged dataset saved to: {output_file}")
    print(f"Total columns: {len(merged_df.columns)}")
    
    # Generate summary statistics
    generate_summary_stats(merged_df)
    
    print(f"\n📊 Dataset ready for analysis!")
    print(f"   - Original unified dataset: {len(nfl_df)} games, {len(nfl_df.columns)} columns")
    print(f"   - Kalshi dataset: {len(kalshi_df)} games, {len(kalshi_df.columns)} columns")
    print(f"   - Merged dataset: {len(merged_df)} games, {len(merged_df.columns)} columns")

if __name__ == "__main__":
    main()
