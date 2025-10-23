"""
Simple script to extract only real-world timestamps from nflfastR
Focuses only on getting the timestamp data we need
"""

import pandas as pd
import os
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
from rpy2.robjects.conversion import localconverter

def extract_simple_timestamps(years):
    """Extract real-world timestamps for first TDs and game kickoff times"""
    print(f"Extracting real-world timestamps for years: {years}")
    
    try:
        # Import nflfastR
        nflfastr = importr('nflfastR')
        print("✅ nflfastR imported successfully")
        
        # Load data for specified years
        years_str = ','.join(map(str, years))
        r_code = f'''
        library(nflfastR)
        pbp_data <- load_pbp(c({years_str}))
        '''
        
        print(f"Loading data for {years_str}...")
        robjects.r(r_code)
        print("✅ Data loaded")
        
        # Convert to pandas
        pbp_df = robjects.r('pbp_data')
        with localconverter(robjects.default_converter + pandas2ri.converter):
            pbp_df = robjects.conversion.rpy2py(pbp_df)
        
        print(f"✅ Converted {len(pbp_df)} plays to pandas")
        
        # Get game-level data (kickoff times)
        # Look for actual game start time columns
        print("Looking for game start time columns...")
        
        # Check for start_time column which should contain actual kickoff times
        if 'start_time' in pbp_df.columns:
            print("Found 'start_time' column - this should contain actual kickoff times")
            time_col = 'start_time'
        else:
            print("No start_time column found. Available time-related columns:")
            time_cols = [col for col in pbp_df.columns if 'time' in col.lower()]
            print(time_cols)
            
            # Try to find the best alternative
            if 'game_time_eastern' in pbp_df.columns:
                time_col = 'game_time_eastern'
            elif 'kickoff_time' in pbp_df.columns:
                time_col = 'kickoff_time'
            else:
                print("No suitable time column found, will use game_date as fallback")
                time_col = 'game_date'
        
        print(f"Using time column: {time_col}")
        
        game_data = pbp_df.groupby('game_id').agg({
            'game_date': 'first',
            time_col: 'first',
            'season': 'first',
            'week': 'first',
            'home_team': 'first',
            'away_team': 'first'
        }).reset_index()
        
        print(f"Found {len(game_data)} games")
        
        # Filter to touchdowns and get first TD per game
        td_plays = pbp_df[pbp_df['touchdown'] == 1].copy()
        td_plays = td_plays.sort_values(['game_id', 'play_id'])
        first_td = td_plays.groupby('game_id').first().reset_index()
        
        print(f"Found first TD for {len(first_td)} games")
        
        # Merge game data with first TD data
        merged_data = game_data.merge(
            first_td[['game_id', 'time_of_day']], 
            on='game_id', 
            how='left'
        )
        
        # Extract timestamps and game info
        timestamp_data = []
        for idx, row in merged_data.iterrows():
            game_id = row['game_id']
            kickoff_time = row.get(time_col, None)
            first_td_timestamp = row.get('time_of_day', None)
            
            timestamp_data.append({
                'game_id': game_id,
                'season': row.get('season', None),
                'week': row.get('week', None),
                'home_team': row.get('home_team', None),
                'away_team': row.get('away_team', None),
                'game_date': row.get('game_date', None),
                'kickoff_time': str(kickoff_time) if pd.notna(kickoff_time) else None,
                'first_td_real_timestamp': str(first_td_timestamp) if pd.notna(first_td_timestamp) else None
            })
        
        timestamp_df = pd.DataFrame(timestamp_data)
        
        # Count how many have real timestamps
        kickoff_count = timestamp_df['kickoff_time'].notna().sum()
        first_td_count = timestamp_df['first_td_real_timestamp'].notna().sum()
        print(f"Games with kickoff times: {kickoff_count}/{len(timestamp_df)}")
        print(f"Games with first TD timestamps: {first_td_count}/{len(timestamp_df)}")
        
        return timestamp_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()

def main():
    """Main execution"""
    print("="*60)
    print("EXTRACTING REAL-WORLD TIMESTAMPS (KICKOFF + FIRST TD)")
    print("="*60)
    
    # Process only 2024 for testing
    years = [2024]
    timestamp_df = extract_simple_timestamps(years)
    
    if len(timestamp_df) > 0:
        # Save to simple CSV
        output_file = 'results/data/nfl_real_timestamps.csv'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        timestamp_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Timestamp data saved to: {output_file}")
        print(f"Total games: {len(timestamp_df)}")
        print(f"Games with kickoff times: {timestamp_df['kickoff_time'].notna().sum()}")
        print(f"Games with first TD timestamps: {timestamp_df['first_td_real_timestamp'].notna().sum()}")
        
        # Show sample
        print("\nSample data:")
        sample = timestamp_df.head(3)
        for idx, row in sample.iterrows():
            print(f"  {row['game_id']}: {row['home_team']} vs {row['away_team']}")
            print(f"    Kickoff: {row['kickoff_time']}")
            print(f"    First TD: {row['first_td_real_timestamp']}")
        
        print(f"\n✅ CSV file created: {output_file}")
        print("This file contains both kickoff times and first TD timestamps for 2024 games")
    else:
        print("❌ No data extracted")

if __name__ == "__main__":
    main()
