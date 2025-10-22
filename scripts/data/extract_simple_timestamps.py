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
    """Extract only real-world timestamps for first TDs"""
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
        
        # Filter to touchdowns and get first TD per game
        td_plays = pbp_df[pbp_df['touchdown'] == 1].copy()
        td_plays = td_plays.sort_values(['game_id', 'play_id'])
        first_td = td_plays.groupby('game_id').first().reset_index()
        
        print(f"Found first TD for {len(first_td)} games")
        
        # Extract only what we need: game_id and real timestamp
        timestamp_data = []
        for idx, row in first_td.iterrows():
            game_id = row['game_id']
            real_timestamp = row.get('time_of_day', None)
            
            timestamp_data.append({
                'game_id': game_id,
                'first_td_real_timestamp': str(real_timestamp) if pd.notna(real_timestamp) else None
            })
        
        timestamp_df = pd.DataFrame(timestamp_data)
        
        # Count how many have real timestamps
        real_count = timestamp_df['first_td_real_timestamp'].notna().sum()
        print(f"Games with real timestamps: {real_count}/{len(timestamp_df)}")
        
        return timestamp_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()

def main():
    """Main execution"""
    print("="*60)
    print("EXTRACTING REAL-WORLD TIMESTAMPS ONLY")
    print("="*60)
    
    # Process 2021+ years
    years = list(range(2021, 2025))
    timestamp_df = extract_simple_timestamps(years)
    
    if len(timestamp_df) > 0:
        # Save to simple CSV
        output_file = 'results/data/nfl_real_timestamps.csv'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        timestamp_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Timestamp data saved to: {output_file}")
        print(f"Total games: {len(timestamp_df)}")
        print(f"Games with real timestamps: {timestamp_df['first_td_real_timestamp'].notna().sum()}")
        
        # Show sample
        print("\nSample timestamps:")
        sample = timestamp_df[timestamp_df['first_td_real_timestamp'].notna()].head(3)
        for idx, row in sample.iterrows():
            print(f"  {row['game_id']}: {row['first_td_real_timestamp']}")
        
        print(f"\n✅ CSV file created: {output_file}")
        print("This file can be used as a foreign key reference for your unified dataset")
    else:
        print("❌ No data extracted")

if __name__ == "__main__":
    main()
