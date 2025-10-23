# Kalshi Data Fetch Script

## Overview
The `fetch_kalshi_data.py` script fetches real-time market data from Kalshi's prediction markets for NFL games. It uses the official `kalshi-python` SDK to query market odds at specific times relative to game events.

## Location
```
scripts/data/fetch_kalshi_data.py
```

## Features

### 1. **Real Timestamps Integration**
- Uses `nfl_real_timestamps.csv` as the primary data source
- Processes all 285 games with verified timestamps
- Calculates precise query times based on actual game events

### 2. **Timing Precision**
- **Pregame Odds**: Queried 5 minutes before actual kickoff time
- **Post-TD Odds**: Queried 1 minute after actual first TD timestamp
- Real-time calculation from verified game data

### 3. **Official SDK Integration**
- Uses `kalshi-python` official SDK
- Proper API authentication and error handling
- Market search, event lookup, and order book data retrieval

### 4. **Data Quality**
- Only real data - no mock data fallback
- Skips games with missing timestamps or failed lookups
- Comprehensive validation and error handling

## Requirements

### Python Packages
```bash
pip install kalshi-python pandas
```

### API Credentials
Create `kalshi_config.py` in the project root:
```python
KALSHI_API_KEY = "your_api_key_here"
KALSHI_PRIVATE_KEY = "your_private_key_here"
```

See `docs/KALSHI_API_SETUP.md` for detailed credential setup instructions.

## Usage

### Basic Run
```bash
cd /path/to/NFL-Kalshi
python3 scripts/data/fetch_kalshi_data.py
```

### Expected Output
```
================================================================================
KALSHI DATA INTEGRATION (Official SDK)
================================================================================
✅ Kalshi API client initialized with authentication (official SDK)
Loaded 1343 games from unified dataset
Loaded 285 games with real timestamps
Testing Kalshi API connectivity...
✅ Using real Kalshi API. Fetching real data with specific timing...

Processing 285 games from real timestamps dataset
Found 285 games with complete data

[1/285] Processing 2024_01_KC_BAL: BAL @ KC
    Fetching data for market: KXMVENFL...
    ✅ Successfully fetched real market data

[2/285] Processing 2024_01_PHI_GB: GB @ PHI
    ⚠️  No markets found for GB @ PHI

...

Created 200 records with real timing

✅ Kalshi dataset saved to: results/data/kalshi_nfl_data_official.csv
Total games with real Kalshi data: 200
Real data: 200
Games processed: 200 out of 285 attempted
Success rate: 70.2%
```

## Data Flow

```
Input: nfl_real_timestamps.csv (285 games)
  ↓
Merge with nfl_unified_data.csv (for first_td_team)
  ↓
For each game:
  1. Parse kickoff_time → Calculate pregame_timestamp (kickoff - 5 min)
  2. Parse first_td_timestamp → Calculate post_td_timestamp (first_td + 1 min)
  3. Search Kalshi markets by team names and date
  4. Fetch market snapshot at pregame_timestamp
  5. Fetch market snapshot at post_td_timestamp
  6. Create data entry if both snapshots successful
  ↓
Output: kalshi_nfl_data_official.csv
```

## Output Format

### File: `results/data/kalshi_nfl_data_official.csv`

Columns:
- `game_id`: Unique game identifier
- `season`: NFL season (e.g., 2024)
- `week`: Game week number
- `home_team`: Home team abbreviation
- `away_team`: Away team abbreviation
- `game_date`: Date of the game
- `kalshi_ticker`: Kalshi market ticker
- `pregame_timestamp`: ISO timestamp of pregame query
- `pregame_home_prob_kalshi`: Home team win probability (pregame)
- `pregame_away_prob_kalshi`: Away team win probability (pregame)
- `first_td_timestamp`: ISO timestamp of first touchdown
- `first_td_team`: Team that scored first TD
- `post_td_timestamp`: ISO timestamp of post-TD query
- `post_td_home_prob_kalshi`: Home team win probability (post-TD)
- `post_td_away_prob_kalshi`: Away team win probability (post-TD)
- `prob_change_home`: Change in home team probability
- `prob_change_away`: Change in away team probability
- `data_quality_flag`: Always "real_data"

## Key Functions

### `create_real_timing_kalshi_data(nfl_df, timestamps_df, api)`
Main data processing function that:
1. Uses timestamps dataset as primary source
2. Merges with NFL data for additional information
3. Processes each game sequentially
4. Handles errors gracefully with skip logic
5. Returns DataFrame with Kalshi data

### `search_nfl_markets(date, home_team, away_team)`
Market search function using proper API lookup flow:
1. Get NFL series ticker
2. Get NFL events for the series
3. Find specific game event by teams and date
4. Get markets for the event
5. Filter for game winner markets

### `get_market_snapshot(ticker, timestamp)`
Fetches market data using order book:
1. Get order book for market ticker
2. Extract bid/ask prices
3. Calculate mid-price
4. Convert to probabilities
5. Return snapshot data

## Error Handling

### Skipped Games
Games are skipped with warning messages for:
- Missing or invalid timestamps
- No Kalshi markets found
- Failed market snapshot retrieval

### Error Messages
- `⚠️  Skipping - missing timestamps`: Game lacks kickoff or first TD time
- `⚠️  No markets found`: Kalshi has no markets for this game
- `⚠️  Failed to fetch market snapshots`: API call failed

## Performance

### Expected Metrics
- **Total Games**: 285 (all games in timestamps dataset)
- **Processing Time**: ~2-5 seconds per game
- **Total Duration**: ~10-20 minutes for all games
- **Expected Success Rate**: 60-80% (depends on Kalshi market availability)

### Rate Limiting
- Built-in delays between API calls
- Respects Kalshi API rate limits
- Sequential processing to avoid throttling

## Troubleshooting

### No API Credentials
```
❌ Kalshi API credentials not found
```
**Solution**: Create `kalshi_config.py` with valid credentials

### API Connection Error
```
❌ Kalshi API not accessible
```
**Solution**: Check network connection and API credentials

### Low Success Rate
```
Success rate: 20.0%
```
**Possible Causes**:
- Kalshi markets not available for many games
- Network issues
- API authentication problems
- Market search logic needs refinement

### Import Error
```
⚠️  kalshi-python SDK not available
```
**Solution**: Run `pip install kalshi-python`

## Best Practices

1. **Run during off-peak hours** to avoid API rate limits
2. **Monitor progress** through the detailed logging output
3. **Check success rate** after completion
4. **Backup existing data** before running script
5. **Review skipped games** to identify patterns

## Related Files
- `docs/KALSHI_API_SETUP.md`: API credential setup
- `docs/KALSHI_INTEGRATION.md`: Integration overview
- `results/data/nfl_real_timestamps.csv`: Input timestamps
- `results/data/kalshi_nfl_data_official.csv`: Output data

## Version History
- **v2.0**: Use real timestamps dataset as primary source (285 games)
- **v1.5**: Remove all mock data, real data only
- **v1.0**: Initial implementation with SDK integration
