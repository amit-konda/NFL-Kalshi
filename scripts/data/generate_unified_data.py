"""
Master data generation script that creates the unified NFL dataset.
Combines first TD analysis, pregame odds, and opening possession data.
"""

import pandas as pd
import math
import nfl_data_py as nfl
import numpy as np
import os

print("="*80)
print("GENERATING UNIFIED NFL DATASET (2020-2024)")
print("="*80)

# --- Step 1: Pull play-by-play and schedule data ---
years = list(range(2020, 2025))
print("\nStep 1: Downloading play-by-play data...")
pbp = nfl.import_pbp_data(years)
print("Step 1: Downloading schedule data...")
games = nfl.import_schedules(years)

# --- Normalize/derive timing columns so downstream logic is robust ---
# Create quarter_seconds_remaining from clock if missing, then game_seconds_remaining if missing
def _parse_clock_to_seconds(clock_val):
    if pd.isna(clock_val):
        return np.nan
    try:
        if isinstance(clock_val, (int, float)):
            # Already seconds
            return float(clock_val)
        s = str(clock_val)
        if ':' in s:
            minutes_str, seconds_str = s.split(':', 1)
            minutes = int(minutes_str)
            seconds = int(seconds_str)
            return float(minutes * 60 + seconds)
        # If format unexpected, return NaN
        return np.nan
    except Exception:
        return np.nan

if 'quarter_seconds_remaining' not in pbp.columns:
    # Try deriving from clock
    if 'clock' in pbp.columns:
        pbp['quarter_seconds_remaining'] = pbp['clock'].apply(_parse_clock_to_seconds)
    else:
        pbp['quarter_seconds_remaining'] = np.nan

if 'game_seconds_remaining' not in pbp.columns:
    # Derive from qtr and quarter_seconds_remaining if available
    qtr_numeric = pd.to_numeric(pbp.get('qtr', np.nan), errors='coerce')
    qsr = pd.to_numeric(pbp.get('quarter_seconds_remaining', np.nan), errors='coerce')
    # Assume 900s per quarter; OT quarters will produce negative remaining which still
    # sorts later than regulation plays when sorting descending
    pbp['game_seconds_remaining'] = (4 - qtr_numeric) * 900 + qsr

# --- Step 2: Filter to regular-season games ---
if 'season_type' in games.columns:
    games = games[games['season_type'] == 'REG']
elif 'game_type' in games.columns:
    games = games[games['game_type'] == 'REG']

print(f"\nRegular season games: {len(games)}")

# --- Step 3: Identify first TD team for each game ---
print("\nStep 2: Identifying first touchdown in each game...")
td_mask = pbp['touchdown'] == 1

# Sort by game_id and game_seconds_remaining (descending = earlier in game)
if 'game_seconds_remaining' in pbp.columns:
    sort_cols = ['game_id', 'game_seconds_remaining']
    ascending = [True, False]
else:
    sort_cols = ['game_id']
    ascending = True

# Determine which timing columns exist in this pbp dataset
time_cols_possible = [
    'game_seconds_remaining',
    'game_seconds_elapsed',
    'qtr',
    'clock',
    'quarter_seconds_remaining'
]
time_cols_existing = [c for c in time_cols_possible if c in pbp.columns]

base_cols = ['game_id', 'td_team', 'td_player_name', 'play_type']
select_cols = base_cols + time_cols_existing

# Build a rename map only for columns that exist
rename_map = {'td_team': 'first_td_team'}
if 'game_seconds_remaining' in time_cols_existing:
    rename_map['game_seconds_remaining'] = 'first_td_game_seconds_remaining'
if 'game_seconds_elapsed' in time_cols_existing:
    rename_map['game_seconds_elapsed'] = 'first_td_game_seconds_elapsed'
if 'qtr' in time_cols_existing:
    rename_map['qtr'] = 'first_td_qtr'
if 'clock' in time_cols_existing:
    rename_map['clock'] = 'first_td_clock'
if 'quarter_seconds_remaining' in time_cols_existing:
    rename_map['quarter_seconds_remaining'] = 'first_td_quarter_seconds_remaining'

first_td = (
    pbp[td_mask]
    .sort_values(sort_cols, ascending=ascending)
    .groupby('game_id', as_index=False)
    .first()
    [select_cols]
    .rename(columns=rename_map)
)

print(f"Games with first TD identified: {len(first_td)}")

# --- Step 4: Determine winner from final scores ---
print("\nStep 3: Determining game winners...")

def winner(row):
    if row['home_score'] > row['away_score']:
        return row['home_team']
    elif row['away_score'] > row['home_score']:
        return row['away_team']
    else:
        return None

games['winner'] = games.apply(winner, axis=1)

# --- Step 5: Add moneyline odds and probabilities ---
print("\nStep 4: Adding pregame moneyline odds...")

def moneyline_to_prob(moneyline):
    """Convert American moneyline odds to implied probability."""
    if pd.isna(moneyline):
        return None
    if moneyline < 0:
        return abs(moneyline) / (abs(moneyline) + 100)
    else:
        return 100 / (moneyline + 100)

games['home_prob'] = games['home_moneyline'].apply(moneyline_to_prob)
games['away_prob'] = games['away_moneyline'].apply(moneyline_to_prob)

def favored(row):
    if pd.isna(row['home_prob']) or pd.isna(row['away_prob']):
        return None
    return row['home_team'] if row['home_prob'] > row['away_prob'] else row['away_team']

def favored_prob(row):
    if pd.isna(row['home_prob']) or pd.isna(row['away_prob']):
        return None
    return max(row['home_prob'], row['away_prob'])

games['favored_team'] = games.apply(favored, axis=1)
games['favored_team_prob'] = games.apply(favored_prob, axis=1)

# --- Step 6: Add opening possession data ---
print("\nStep 5: Determining opening possession for each game...")

opening_drives = []
for game_id in games['game_id'].unique():
    game_plays = pbp[pbp['game_id'] == game_id].copy()
    
    if len(game_plays) == 0:
        continue
    
    if 'game_seconds_remaining' in game_plays.columns:
        game_plays = game_plays.sort_values('game_seconds_remaining', ascending=False)
    
    for _, play in game_plays.iterrows():
        if pd.notna(play.get('posteam')) and play.get('posteam') != '':
            opening_possession_team = play['posteam']
            opening_drives.append({
                'game_id': game_id,
                'opening_possession_team': opening_possession_team
            })
            break

opening_df = pd.DataFrame(opening_drives)
print(f"Opening possession determined for {len(opening_df)} games")

# --- Step 7: Merge everything together ---
print("\nStep 6: Merging all data together...")

# Select relevant columns from games
games_subset = games[[
    'game_id', 'season', 'home_team', 'away_team', 
    'home_score', 'away_score', 'winner',
    'home_moneyline', 'away_moneyline', 'home_prob', 'away_prob',
    'favored_team', 'favored_team_prob', 'spread_line'
]]

# Merge first TD
merged = pd.merge(first_td, games_subset, on='game_id', how='right')

# Merge opening possession
merged = pd.merge(merged, opening_df, on='game_id', how='left')

# --- Step 8: Create derived columns ---
print("\nStep 7: Creating derived columns...")

# First TD team won?
merged['first_td_team_won'] = (merged['first_td_team'] == merged['winner']).astype(int)

# Opening possession indicators
merged['home_got_ball_first'] = (merged['opening_possession_team'] == merged['home_team']).astype(int)
merged['away_got_ball_first'] = (merged['opening_possession_team'] == merged['away_team']).astype(int)
merged['home_scored_first_td'] = (merged['first_td_team'] == merged['home_team']).astype(int)
merged['away_scored_first_td'] = (merged['first_td_team'] == merged['away_team']).astype(int)

# Additional useful columns
merged['is_pickem'] = ((merged['home_prob'] >= 0.45) & (merged['home_prob'] <= 0.55)).astype(int)
merged['spread_abs'] = merged['spread_line'].abs()
merged['favorite_won'] = (merged['favored_team'] == merged['winner']).astype(int)
merged['opening_possession_scored_first'] = (merged['opening_possession_team'] == merged['first_td_team']).astype(int)
merged['opening_possession_won'] = (merged['opening_possession_team'] == merged['winner']).astype(int)

# Derived readable time feature if available
if 'first_td_game_seconds_remaining' in merged.columns:
    merged['first_td_minutes_remaining'] = (merged['first_td_game_seconds_remaining'] / 60).round(2)

# --- Step 9: Save unified dataset ---
# Resolve project root and prepare output directory
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
output_file = os.path.join(PROJECT_ROOT, "results", "data", "nfl_unified_data.csv")
os.makedirs(os.path.dirname(output_file), exist_ok=True)
merged.to_csv(output_file, index=False)

print("\n" + "="*80)
print("UNIFIED DATASET CREATED SUCCESSFULLY!")
print("="*80)
print(f"✅ Saved to: {output_file}")
print(f"Total games: {len(merged)}")
print(f"Total columns: {len(merged.columns)}")
print(f"\nData completeness:")
print(f"  First TD data: {merged['first_td_team'].notna().sum()} ({merged['first_td_team'].notna().sum()/len(merged)*100:.1f}%)")
print(f"  Moneyline data: {merged['home_moneyline'].notna().sum()} ({merged['home_moneyline'].notna().sum()/len(merged)*100:.1f}%)")
print(f"  Opening possession: {merged['opening_possession_team'].notna().sum()} ({merged['opening_possession_team'].notna().sum()/len(merged)*100:.1f}%)")

print("\n✅ All analysis scripts can now use 'nfl_unified_data.csv' as the single source of truth!")

