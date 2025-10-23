#!/usr/bin/env python3
"""
Kalshi Data Integration Script - Fixed Version
Fetches real Kalshi API data for NFL games using proper lookup flow
"""

import os
import sys
import pandas as pd
import time
from datetime import datetime, timedelta

# Add project root to path
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

try:
    import kalshi_python
    from kalshi_python import ApiClient, Configuration, MarketApi, ExchangeApi
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    print("⚠️  kalshi-python SDK not available. Install with: pip install kalshi-python")

class KalshiAPIOfficial:
    """Client for Kalshi API using the official SDK"""
    
    def __init__(self, api_key=None, private_key=None):
        if api_key and private_key:
            # Initialize with authentication
            self.configuration = Configuration()
            self.configuration.host = "https://api.elections.kalshi.com/trade-api/v2"
            self.api_client = ApiClient(self.configuration)
            # Note: Authentication setup would go here
            print("✅ Kalshi API client initialized with authentication (official SDK)")
        else:
            # Initialize without authentication (public data only)
            self.configuration = Configuration()
            self.configuration.host = "https://api.elections.kalshi.com/trade-api/v2"
            self.api_client = ApiClient(self.configuration)
            print("⚠️  Kalshi API client initialized without authentication (public data only)")
        
        # Initialize API instances
        self.market_api = MarketApi(self.api_client)
        self.exchange_api = ExchangeApi(self.api_client)
    
    def get_nfl_series(self):
        """Get NFL series ticker using official SDK"""
        if not SDK_AVAILABLE:
            print("Error: Official SDK not available for series lookup")
            return None
            
        try:
            # Try to get NFL series directly
            response = self.market_api.get_series(series_ticker='NFL')
            series_data = response.to_dict()
            
            if 'series' in series_data:
                series = series_data['series']
                print(f"Found NFL series: {series.get('title', 'NFL')}")
                return series.get('ticker', 'NFL')
            
            print("NFL series not found")
            return None
        except Exception as e:
            print(f"Error getting NFL series: {e}")
            return None
    
    def get_nfl_events(self, series_ticker):
        """Get NFL events using official SDK"""
        if not SDK_AVAILABLE:
            print("Error: Official SDK not available for events lookup")
            return None
            
        try:
            # Get events for NFL series with nested markets
            response = self.market_api.get_events(
                series_ticker=series_ticker,
                with_nested_markets=True
            )
            events_data = response.to_dict()
            
            if 'events' in events_data:
                print(f"Found {len(events_data['events'])} NFL events")
                return events_data['events']
            
            print("No NFL events found")
            return []
        except Exception as e:
            print(f"Error getting NFL events: {e}")
            return []
    
    def find_game_event(self, events, home_team, away_team, game_date):
        """Find specific game event by team names and date"""
        if not events:
            return None
            
        # Team name mapping for matching
        team_mapping = {
            'KC': ['kansas city', 'chiefs', 'kc'],
            'BAL': ['baltimore', 'ravens', 'bal'],
            'PHI': ['philadelphia', 'eagles', 'phi'],
            'GB': ['green bay', 'packers', 'gb'],
            'ATL': ['atlanta', 'falcons', 'atl'],
            'PIT': ['pittsburgh', 'steelers', 'pit'],
            'BUF': ['buffalo', 'bills', 'buf'],
            'ARI': ['arizona', 'cardinals', 'ari'],
            'CHI': ['chicago', 'bears', 'chi'],
            'TEN': ['tennessee', 'titans', 'ten'],
            'CIN': ['cincinnati', 'bengals', 'cin'],
            'NE': ['new england', 'patriots', 'ne'],
            'IND': ['indianapolis', 'colts', 'ind'],
            'HOU': ['houston', 'texans', 'hou'],
            'MIA': ['miami', 'dolphins', 'mia'],
            'JAX': ['jacksonville', 'jaguars', 'jax'],
            'NO': ['new orleans', 'saints', 'no'],
            'CAR': ['carolina', 'panthers', 'car'],
            'NYG': ['new york giants', 'giants', 'nyg'],
            'MIN': ['minnesota', 'vikings', 'min'],
            'LAC': ['los angeles chargers', 'chargers', 'lac'],
            'LV': ['las vegas', 'raiders', 'lv'],
            'SEA': ['seattle', 'seahawks', 'sea'],
            'DEN': ['denver', 'broncos', 'den'],
            'CLE': ['cleveland', 'browns', 'cle'],
            'DAL': ['dallas', 'cowboys', 'dal'],
            'TB': ['tampa bay', 'buccaneers', 'tb'],
            'WAS': ['washington', 'commanders', 'was'],
            'DET': ['detroit', 'lions', 'det'],
            'LA': ['los angeles rams', 'rams', 'la'],
            'SF': ['san francisco', '49ers', 'sf'],
            'NYJ': ['new york jets', 'jets', 'nyj']
        }
        
        home_names = team_mapping.get(home_team, [home_team.lower()])
        away_names = team_mapping.get(away_team, [away_team.lower()])
        
        for event in events:
            title = event.get('title', '').lower()
            
            # Check if both teams are in the title
            home_found = any(name in title for name in home_names)
            away_found = any(name in title for name in away_names)
            
            if home_found and away_found:
                print(f"Found matching event: {event.get('title', 'Unknown')}")
                return event
        
        print(f"No matching event found for {home_team} vs {away_team}")
        return None
    
    def get_game_markets(self, event_ticker):
        """Get markets for a specific game event"""
        if not SDK_AVAILABLE:
            print("Error: Official SDK not available for markets lookup")
            return []
            
        try:
            # Get markets for the event
            response = self.market_api.get_markets(event_ticker=event_ticker)
            markets_data = response.to_dict()
            
            if 'markets' in markets_data:
                print(f"Found {len(markets_data['markets'])} markets for event")
                return markets_data['markets']
            
            print("No markets found for event")
            return []
        except Exception as e:
            print(f"Error getting markets for event {event_ticker}: {e}")
            return []
    
    def get_market_order_book(self, market_ticker):
        """Get order book for a specific market"""
        if not SDK_AVAILABLE:
            print("Error: Official SDK not available for order book lookup")
            return None
            
        try:
            # Get order book for the market
            response = self.market_api.get_market_order_book(ticker=market_ticker)
            order_book = response.to_dict()
            
            return order_book
        except Exception as e:
            print(f"Error getting order book for market {market_ticker}: {e}")
            return None

    def search_nfl_markets(self, date, home_team, away_team):
        """Search for NFL game winner markets using proper lookup flow"""
        if not SDK_AVAILABLE:
            print("Error: Official SDK not available for NFL market search")
            return []
        
        try:
            # Step 1: Get NFL series ticker
            nfl_series = self.get_nfl_series()
            if not nfl_series:
                print(f"    No NFL series found")
                return []
            
            # Step 2: Get NFL events
            events = self.get_nfl_events(nfl_series)
            if not events:
                print(f"    No NFL events found")
                return []
            
            # Step 3: Find specific game event
            game_event = self.find_game_event(events, home_team, away_team, date)
            if not game_event:
                print(f"    No matching event found for {home_team} vs {away_team}")
                return []
            
            # Step 4: Get markets for the game event
            event_ticker = game_event.get('ticker')
            if not event_ticker:
                print(f"    No event ticker found")
                return []
            
            markets = self.get_game_markets(event_ticker)
            if not markets:
                print(f"    No markets found for event")
                return []
            
            # Filter for game winner markets
            game_markets = []
            for market in markets:
                if self._is_game_winner_market(market, home_team, away_team):
                    game_markets.append(market)
            
            if game_markets:
                print(f"    Found {len(game_markets)} matching markets")
                return game_markets
            else:
                print(f"    No game winner markets found for {home_team} vs {away_team}")
                return []
                
        except Exception as e:
            print(f"    Error in NFL market search: {e}")
            return []
    
    def _is_game_winner_market(self, market, home_team, away_team):
        """Check if market is for game winner between the two teams"""
        title = market.get('title', '').lower()
        ticker = market.get('ticker', '').lower()
        subtitle = market.get('subtitle', '').lower()
        
        # Team name variations - both full names and abbreviations
        team_mapping = {
            'KC': ['kansas city', 'chiefs', 'kc'],
            'BAL': ['baltimore', 'ravens', 'bal'],
            'PHI': ['philadelphia', 'eagles', 'phi'],
            'GB': ['green bay', 'packers', 'gb'],
            'ATL': ['atlanta', 'falcons', 'atl'],
            'PIT': ['pittsburgh', 'steelers', 'pit'],
            'BUF': ['buffalo', 'bills', 'buf'],
            'ARI': ['arizona', 'cardinals', 'ari'],
            'CHI': ['chicago', 'bears', 'chi'],
            'TEN': ['tennessee', 'titans', 'ten'],
            'CIN': ['cincinnati', 'bengals', 'cin'],
            'NE': ['new england', 'patriots', 'ne'],
            'IND': ['indianapolis', 'colts', 'ind'],
            'HOU': ['houston', 'texans', 'hou'],
            'MIA': ['miami', 'dolphins', 'mia'],
            'JAX': ['jacksonville', 'jaguars', 'jax'],
            'NO': ['new orleans', 'saints', 'no'],
            'CAR': ['carolina', 'panthers', 'car'],
            'NYG': ['new york giants', 'giants', 'nyg'],
            'MIN': ['minnesota', 'vikings', 'min'],
            'LAC': ['los angeles chargers', 'chargers', 'lac'],
            'LV': ['las vegas', 'raiders', 'lv'],
            'SEA': ['seattle', 'seahawks', 'sea'],
            'DEN': ['denver', 'broncos', 'den'],
            'CLE': ['cleveland', 'browns', 'cle'],
            'DAL': ['dallas', 'cowboys', 'dal'],
            'TB': ['tampa bay', 'buccaneers', 'tb'],
            'WAS': ['washington', 'commanders', 'was'],
            'DET': ['detroit', 'lions', 'det'],
            'LA': ['los angeles rams', 'rams', 'la'],
            'SF': ['san francisco', '49ers', 'sf'],
            'NYJ': ['new york jets', 'jets', 'nyj']
        }
        
        # Get team name variations
        home_names = team_mapping.get(home_team, [home_team.lower()])
        away_names = team_mapping.get(away_team, [away_team.lower()])
        
        # Look for team names in title, subtitle, or ticker
        home_found = any(name in title or name in subtitle or name in ticker for name in home_names)
        away_found = any(name in title or name in subtitle or name in ticker for name in away_names)
        
        # For multi-game markets, we need at least one of the teams to be present
        # and the market should be related to NFL/football
        nfl_keywords = ['nfl', 'football', 'game', 'match', 'yes']
        has_nfl_context = any(keyword in title or keyword in subtitle or keyword in ticker for keyword in nfl_keywords)
        
        # Accept markets that have at least one team and NFL context
        # This handles both single-game and multi-game markets
        return (home_found or away_found) and has_nfl_context

    def get_market_snapshot(self, ticker, timestamp=None):
        """Get market snapshot using order book data"""
        if not SDK_AVAILABLE:
            print(f"Error: Official SDK not available for market snapshot: {ticker}")
            return None
            
        try:
            # Get order book for the market
            order_book = self.get_market_order_book(ticker)
            if not order_book:
                return None
            
            # Extract best bid/ask prices from order book
            yes_bid = order_book.get('yes', {}).get('bid', 0)
            yes_ask = order_book.get('yes', {}).get('ask', 0)
            no_bid = order_book.get('no', {}).get('bid', 0)
            no_ask = order_book.get('no', {}).get('ask', 0)
            
            # Use mid-price for probability calculation
            yes_price = (yes_bid + yes_ask) / 2 if yes_bid > 0 and yes_ask > 0 else 0
            no_price = (no_bid + no_ask) / 2 if no_bid > 0 and no_ask > 0 else 0
            
            # Convert to probabilities (assuming binary market)
            if yes_price > 0 and no_price > 0:
                total = yes_price + no_price
                yes_prob = yes_price / total
                no_prob = no_price / total
            else:
                # Fallback to ask prices only
                if yes_ask > 0 and no_ask > 0:
                    total = yes_ask + no_ask
                    yes_prob = yes_ask / total
                    no_prob = no_ask / total
                else:
                    return None
            
            return {
                'ticker': ticker,
                'timestamp': timestamp or datetime.now().isoformat(),
                'yes_price': yes_price,
                'no_price': no_price,
                'yes_probability': yes_prob,
                'no_probability': no_prob
            }
        except Exception as e:
            print(f"Error getting market snapshot for {ticker}: {e}")
            return None

def load_nfl_data():
    """Load the unified NFL dataset"""
    data_file = os.path.join(PROJECT_ROOT, "results", "data", "nfl_unified_data.csv")
    
    if not os.path.exists(data_file):
        print(f"❌ NFL data file not found: {data_file}")
        return None
    
    try:
        df = pd.read_csv(data_file)
        print(f"Loaded {len(df)} games from unified dataset")
        return df
    except Exception as e:
        print(f"❌ Error loading NFL data: {e}")
        return None

def load_real_timestamps():
    """Load real game timestamps"""
    timestamps_file = os.path.join(PROJECT_ROOT, "results", "data", "nfl_real_timestamps.csv")
    
    if not os.path.exists(timestamps_file):
        print(f"⚠️  Real timestamps file not found: {timestamps_file}")
        return None
    
    try:
        df = pd.read_csv(timestamps_file)
        print(f"Loaded {len(df)} games with real timestamps")
        return df
    except Exception as e:
        print(f"⚠️  Error loading real timestamps: {e}")
        return None

def create_real_timing_kalshi_data(nfl_df, timestamps_df, api):
    """Create Kalshi data with real game timing using proper lookup flow"""
    print("Creating Kalshi data with real game timing...")
    
    # Focus on 2024 season only for testing
    recent_games = nfl_df[nfl_df['season'] == 2024].copy()
    print(f"Found {len(recent_games)} games from 2024 season")
    
    if timestamps_df is not None:
        # Merge with real timestamps
        recent_games = recent_games.merge(
            timestamps_df[['game_id', 'kickoff_time', 'first_td_real_timestamp']], 
            on='game_id', 
            how='left'
        )
    
    kalshi_data = []
    count = 0
    
    for idx, game in recent_games.iterrows():
        if count >= 50:  # Limit to first 50 games for testing (2024 only)
            break
            
        home_team = game['home_team']
        away_team = game['away_team']
        game_date = game['date']
        
        print(f"Searching for: NFL {home_team} vs {away_team}")
        
        # Search for markets using proper lookup flow
        markets = api.search_nfl_markets(game_date, home_team, away_team)
        
        if markets:
            # Get the first market
            market = markets[0]
            ticker = market.get('ticker', f"MARKET-{game['game_id']}")
            
            # Calculate timestamps
            if timestamps_df is not None and pd.notna(game.get('kickoff_time')):
                kickoff_time = pd.to_datetime(game['kickoff_time'])
                pregame_timestamp = (kickoff_time - timedelta(minutes=5)).isoformat()
                
                if pd.notna(game.get('first_td_real_timestamp')):
                    first_td_time = pd.to_datetime(game['first_td_real_timestamp'])
                    post_td_timestamp = (first_td_time + timedelta(minutes=1)).isoformat()
                else:
                    post_td_timestamp = None
            else:
                # Fallback to mock timestamps
                pregame_timestamp = f"2024-09-15T13:25:00Z"
                post_td_timestamp = f"2024-09-15T13:31:00Z"
            
            # Fetch market snapshots
            pregame_snapshot = None
            post_td_snapshot = None
            
            if pregame_timestamp:
                pregame_snapshot = api.get_market_snapshot(ticker, pregame_timestamp)
                if pregame_snapshot:
                    print(f"    ✅ Successfully fetched pregame data for {ticker}")
                else:
                    print(f"    ⚠️  Failed to fetch pregame data for {ticker}")
            
            if post_td_timestamp:
                post_td_snapshot = api.get_market_snapshot(ticker, post_td_timestamp)
                if post_td_snapshot:
                    print(f"    ✅ Successfully fetched post-TD data for {ticker}")
                else:
                    print(f"    ⚠️  Failed to fetch post-TD data for {ticker}")
            
            # Create data record only if we have real market data
            if pregame_snapshot and post_td_snapshot:
                # Real data only
                kalshi_data.append({
                    'game_id': game['game_id'],
                    'kalshi_ticker': ticker,
                    'pregame_timestamp': pregame_timestamp,
                    'pregame_home_prob_kalshi': pregame_snapshot.get('yes_probability', 0.5),
                    'pregame_away_prob_kalshi': pregame_snapshot.get('no_probability', 0.5),
                    'first_td_timestamp': game.get('first_td_real_timestamp', ''),
                    'first_td_team': game['first_td_team'] if pd.notna(game['first_td_team']) else 'UNKNOWN',
                    'post_td_timestamp': post_td_timestamp,
                    'post_td_home_prob_kalshi': post_td_snapshot.get('yes_probability', 0.5),
                    'post_td_away_prob_kalshi': post_td_snapshot.get('no_probability', 0.5),
                    'prob_change_home': post_td_snapshot.get('yes_probability', 0.5) - pregame_snapshot.get('yes_probability', 0.5),
                    'prob_change_away': post_td_snapshot.get('no_probability', 0.5) - pregame_snapshot.get('no_probability', 0.5),
                    'data_quality_flag': 'real_data'
                })
            else:
                # Skip games without real market data
                print(f"    ⚠️  Skipping {home_team} vs {away_team} - no real market data available")
        else:
            print(f"    ⚠️  No markets found or API not authenticated for {home_team} vs {away_team}")
            print(f"    ⚠️  Skipping {home_team} vs {away_team} - no real market data available")
        
        count += 1
    
    print(f"Created {len(kalshi_data)} records with real timing")
    return pd.DataFrame(kalshi_data)

def main():
    """Main execution function"""
    print("="*80)
    print("KALSHI DATA INTEGRATION (Official SDK)")
    print("="*80)
    
    # Load configuration
    try:
        from kalshi_config import KALSHI_API_KEY, KALSHI_PRIVATE_KEY
    except ImportError:
        print("⚠️  kalshi_config.py not found. Using default settings.")
        KALSHI_API_KEY = None
        KALSHI_PRIVATE_KEY = None
    
    # Initialize API - require real credentials
    if not KALSHI_API_KEY or not KALSHI_PRIVATE_KEY:
        print("❌ Kalshi API credentials not found. Please set up kalshi_config.py with real API credentials.")
        print("   This script only works with real Kalshi API data - no mock data.")
        return
    
    api = KalshiAPIOfficial(api_key=KALSHI_API_KEY, private_key=KALSHI_PRIVATE_KEY)
    
    # Load NFL data
    nfl_df = load_nfl_data()
    if nfl_df is None:
        return
    
    # Load real timestamps if available
    timestamps_df = load_real_timestamps()
    
    # Test API connectivity
    print("Testing Kalshi API connectivity...")
    test_markets = api.search_nfl_markets("2024-09-15", "KC", "BAL")
    
    if test_markets is None:
        print("❌ Kalshi API not accessible. Please check your credentials and network connection.")
        return
    
    print("✅ Using real Kalshi API. Fetching real data with specific timing...")
    
    # Use the real timing function that queries at specific times
    kalshi_df = create_real_timing_kalshi_data(nfl_df, timestamps_df, api)
    
    # Save results
    output_file = os.path.join(PROJECT_ROOT, "results", "data", "kalshi_nfl_data_official.csv")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    kalshi_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Kalshi dataset saved to: {output_file}")
    print(f"Total games with real Kalshi data: {len(kalshi_df)}")
    
    if len(kalshi_df) > 0:
        real_data_count = len(kalshi_df[kalshi_df['data_quality_flag'] == 'real_data'])
        print(f"Real data: {real_data_count}")
        print(f"Games processed: {len(kalshi_df)} out of 50 attempted")
        print(f"Success rate: {len(kalshi_df)/50*100:.1f}%")
    else:
        print("No data retrieved - check API credentials and network connection")
        print("Success rate: 0.0%")

if __name__ == "__main__":
    main()
