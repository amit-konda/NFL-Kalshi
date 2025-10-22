# Kalshi Data Integration

This document explains how to fetch and integrate Kalshi prediction market data with the NFL analysis.

## Overview

The Kalshi integration fetches:
1. **Pregame odds** - Moneyline probabilities before kickoff
2. **First TD timing** - When the first touchdown was scored (real timestamp)
3. **Post-TD odds** - Moneyline probabilities 1 minute after first TD
4. **Probability changes** - How much the odds shifted after the first TD

## Files Created

- `scripts/data/fetch_kalshi_data.py` - Main integration script
- `scripts/data/test_kalshi_api.py` - API testing script
- `scripts/data/merge_kalshi_data.py` - Merge Kalshi with unified dataset
- `scripts/analysis/kalshi_analysis.py` - Analysis of Kalshi vs Vegas odds
- `run_kalshi_fetch.py` - Easy runner script for data fetching
- `run_kalshi_merge.py` - Easy runner script for data merging
- `run_kalshi_analysis.py` - Easy runner script for analysis
- `results/data/kalshi_nfl_data.csv` - Kalshi dataset
- `results/data/nfl_unified_with_kalshi.csv` - Merged dataset

## Usage

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test the API connection
python3 scripts/data/test_kalshi_api.py

# Run the full data fetch
python3 run_kalshi_fetch.py

# Merge with unified dataset
python3 run_kalshi_merge.py

# Run analysis
python3 run_kalshi_analysis.py
```

### Manual Execution

```bash
# Fetch Kalshi data
cd scripts/data
python3 fetch_kalshi_data.py

# Merge datasets
python3 merge_kalshi_data.py

# Run analysis
cd ../analysis
python3 kalshi_analysis.py
```

## Output Dataset

**File:** `results/data/kalshi_nfl_data.csv`

**Columns:**
- `game_id` - Links to unified dataset
- `kalshi_ticker` - Kalshi market identifier
- `pregame_home_prob_kalshi` - Home team win probability (pregame)
- `pregame_away_prob_kalshi` - Away team win probability (pregame)
- `first_td_timestamp` - When first TD occurred (ISO timestamp)
- `first_td_team` - Which team scored first TD
- `post_td_home_prob_kalshi` - Home win probability (1 min after TD)
- `post_td_away_prob_kalshi` - Away win probability (1 min after TD)
- `prob_change_home` - Change in home win probability
- `prob_change_away` - Change in away win probability
- `data_quality_flag` - Data completeness indicator

## Data Coverage

- **Time Range:** 2021-2024 seasons (Kalshi launched July 2021)
- **Games:** Only games with available Kalshi markets
- **Rate Limiting:** Built-in delays to respect API limits
- **Error Handling:** Logs issues, continues processing

## API Details

- **Endpoint:** `https://api.kalshi.com/trade-api/v2`
- **Authentication:** None required for public data
- **Rate Limits:** ~1 request per second
- **Data Types:** Market search, details, candlesticks

## Troubleshooting

### Common Issues

1. **No markets found**
   - Kalshi may not have markets for all NFL games
   - Some games may not have sufficient trading activity
   - Check the log file for details

2. **API errors**
   - Network connectivity issues
   - Rate limiting (script includes delays)
   - Market may be closed or inactive

3. **Missing timestamps**
   - Some games may not have first TD data
   - Play-by-play data may be incomplete

### Log Files

- `results/data/kalshi_fetch_log.txt` - Detailed processing log
- Console output shows progress and errors

## Merged Dataset

The Kalshi data has been automatically merged with the unified NFL dataset:

**File:** `results/data/nfl_unified_with_kalshi.csv`

This merged dataset contains all original columns plus:
- All Kalshi columns (pregame odds, first TD timing, post-TD odds)
- Derived comparison columns (Kalshi vs Vegas differences)
- Data quality flags

**Usage:**
```python
import pandas as pd

# Load the merged dataset
merged_data = pd.read_csv('results/data/nfl_unified_with_kalshi.csv')

# Filter to games with Kalshi data
kalshi_games = merged_data[merged_data['has_kalshi_data'] == 1]

# Compare Kalshi vs Vegas odds
kalshi_games[['home_prob', 'pregame_home_prob_kalshi', 'kalshi_vs_vegas_home_diff']]
```

## Analysis Opportunities

With Kalshi data integrated, you can analyze:

1. **Market Efficiency** - How well do Kalshi odds predict outcomes vs Vegas?
2. **First TD Impact** - How much do Kalshi odds change after first TD?
3. **Overreaction Detection** - Are Kalshi markets more/less reactive than Vegas?
4. **Arbitrage Opportunities** - Price differences between markets
5. **Temporal Analysis** - How odds evolve throughout games

## Notes

- The script processes games sequentially to respect rate limits
- Processing time depends on number of games and API response times
- Some games may not have Kalshi markets available
- All data is saved incrementally to avoid loss on interruption
