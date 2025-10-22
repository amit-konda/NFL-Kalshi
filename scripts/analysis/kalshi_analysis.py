"""
Kalshi vs Vegas Analysis

Analyze differences between Kalshi prediction markets and Vegas odds,
and the impact of first touchdowns on Kalshi markets.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Add project root to path
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

def load_merged_data():
    """Load the merged dataset with Kalshi data"""
    data_file = os.path.join(PROJECT_ROOT, "results", "data", "nfl_unified_with_kalshi.csv")
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Run merge_kalshi_data.py first.")
        return None
    
    df = pd.read_csv(data_file)
    print(f"Loaded merged dataset with {len(df)} games")
    return df

def analyze_kalshi_vs_vegas(df):
    """Analyze differences between Kalshi and Vegas odds"""
    print("\n" + "="*60)
    print("KALSHI VS VEGAS ANALYSIS")
    print("="*60)
    
    # Filter to games with Kalshi data
    kalshi_games = df[df['has_kalshi_data'] == 1].copy()
    
    if len(kalshi_games) == 0:
        print("No games with Kalshi data found.")
        return
    
    print(f"Analyzing {len(kalshi_games)} games with Kalshi data")
    
    # Basic statistics
    print(f"\nProbability Differences (Kalshi - Vegas):")
    print(f"  Home team mean difference: {kalshi_games['kalshi_vs_vegas_home_diff'].mean():.4f}")
    print(f"  Home team std difference: {kalshi_games['kalshi_vs_vegas_home_diff'].std():.4f}")
    print(f"  Away team mean difference: {kalshi_games['kalshi_vs_vegas_away_diff'].mean():.4f}")
    print(f"  Away team std difference: {kalshi_games['kalshi_vs_vegas_away_diff'].std():.4f}")
    
    print(f"\nAbsolute Differences:")
    print(f"  Home team mean abs difference: {kalshi_games['kalshi_vs_vegas_home_abs_diff'].mean():.4f}")
    print(f"  Away team mean abs difference: {kalshi_games['kalshi_vs_vegas_away_abs_diff'].mean():.4f}")
    
    # Correlation analysis
    vegas_home = kalshi_games['home_prob']
    kalshi_home = kalshi_games['pregame_home_prob_kalshi']
    vegas_away = kalshi_games['away_prob']
    kalshi_away = kalshi_games['pregame_away_prob_kalshi']
    
    home_corr = vegas_home.corr(kalshi_home)
    away_corr = vegas_away.corr(kalshi_away)
    
    print(f"\nCorrelations:")
    print(f"  Home team correlation: {home_corr:.4f}")
    print(f"  Away team correlation: {away_corr:.4f}")
    
    return kalshi_games

def analyze_first_td_impact(df):
    """Analyze the impact of first touchdowns on Kalshi odds"""
    print("\n" + "="*60)
    print("FIRST TD IMPACT ON KALSHI ODDS")
    print("="*60)
    
    # Filter to games with complete Kalshi data
    complete_games = df[df['has_complete_kalshi_data'] == 1].copy()
    
    if len(complete_games) == 0:
        print("No games with complete Kalshi data found.")
        return
    
    print(f"Analyzing {len(complete_games)} games with complete Kalshi data")
    
    # First TD impact statistics
    print(f"\nFirst TD Impact on Kalshi Odds:")
    print(f"  Home team avg probability change: {complete_games['prob_change_home'].mean():.4f}")
    print(f"  Away team avg probability change: {complete_games['prob_change_away'].mean():.4f}")
    print(f"  Total probability change (should be ~0): {complete_games['kalshi_total_prob_change'].mean():.4f}")
    
    # Impact by first TD team
    home_scored_first = complete_games[complete_games['home_scored_first_td'] == 1]
    away_scored_first = complete_games[complete_games['away_scored_first_td'] == 1]
    
    if len(home_scored_first) > 0:
        print(f"\nWhen Home Team Scored First TD ({len(home_scored_first)} games):")
        print(f"  Home probability change: {home_scored_first['prob_change_home'].mean():.4f}")
        print(f"  Away probability change: {home_scored_first['prob_change_away'].mean():.4f}")
    
    if len(away_scored_first) > 0:
        print(f"\nWhen Away Team Scored First TD ({len(away_scored_first)} games):")
        print(f"  Home probability change: {away_scored_first['prob_change_home'].mean():.4f}")
        print(f"  Away probability change: {away_scored_first['prob_change_away'].mean():.4f}")
    
    return complete_games

def create_visualizations(df):
    """Create visualizations for the analysis"""
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # Filter to games with Kalshi data
    kalshi_games = df[df['has_kalshi_data'] == 1].copy()
    
    if len(kalshi_games) == 0:
        print("No games with Kalshi data for visualization.")
        return
    
    # Create output directory
    viz_dir = os.path.join(PROJECT_ROOT, "visualizations")
    os.makedirs(viz_dir, exist_ok=True)
    
    # 1. Kalshi vs Vegas scatter plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(kalshi_games['home_prob'], kalshi_games['pregame_home_prob_kalshi'], alpha=0.7)
    plt.plot([0, 1], [0, 1], 'r--', alpha=0.5)
    plt.xlabel('Vegas Home Win Probability')
    plt.ylabel('Kalshi Home Win Probability')
    plt.title('Kalshi vs Vegas: Home Team')
    
    plt.subplot(1, 2, 2)
    plt.scatter(kalshi_games['away_prob'], kalshi_games['pregame_away_prob_kalshi'], alpha=0.7)
    plt.plot([0, 1], [0, 1], 'r--', alpha=0.5)
    plt.xlabel('Vegas Away Win Probability')
    plt.ylabel('Kalshi Away Win Probability')
    plt.title('Kalshi vs Vegas: Away Team')
    
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'kalshi_vs_vegas_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. First TD impact (if we have complete data)
    complete_games = df[df['has_complete_kalshi_data'] == 1].copy()
    
    if len(complete_games) > 0:
        plt.figure(figsize=(10, 6))
        
        # Plot probability changes
        x_pos = np.arange(len(complete_games))
        width = 0.35
        
        plt.bar(x_pos - width/2, complete_games['prob_change_home'], width, label='Home Team', alpha=0.7)
        plt.bar(x_pos + width/2, complete_games['prob_change_away'], width, label='Away Team', alpha=0.7)
        
        plt.xlabel('Game')
        plt.ylabel('Probability Change')
        plt.title('First TD Impact on Kalshi Odds')
        plt.legend()
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, 'kalshi_first_td_impact.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    print(f"Visualizations saved to {viz_dir}/")
    print("  - kalshi_vs_vegas_comparison.png")
    if len(complete_games) > 0:
        print("  - kalshi_first_td_impact.png")

def main():
    """Main execution function"""
    print("="*80)
    print("KALSHI ANALYSIS")
    print("="*80)
    
    # Load data
    df = load_merged_data()
    if df is None:
        return
    
    # Analyze Kalshi vs Vegas
    kalshi_games = analyze_kalshi_vs_vegas(df)
    
    # Analyze first TD impact
    complete_games = analyze_first_td_impact(df)
    
    # Create visualizations
    create_visualizations(df)
    
    print(f"\n✅ Analysis complete!")
    print(f"   - Games with Kalshi data: {df['has_kalshi_data'].sum()}")
    print(f"   - Games with complete Kalshi data: {df['has_complete_kalshi_data'].sum()}")

if __name__ == "__main__":
    main()
