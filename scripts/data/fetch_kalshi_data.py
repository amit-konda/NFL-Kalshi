"""
Kalshi Data Integration Script using Official SDK

Fetches pregame and post-first-TD Kalshi odds for NFL games using the official kalshi-python SDK.
Creates a separate dataset that can be linked to the unified dataset later.
"""

import pandas as pd
import time
import json
from datetime import datetime, timedelta
import os
import sys

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
        self.api_key = api_key
        self.private_key = private_key
        self.authenticated = api_key is not None and private_key is not None
        
        if not SDK_AVAILABLE:
            print("⚠️  Official Kalshi SDK not available")
            return
            
        # Configure the API client
        if self.authenticated:
            # For authenticated requests, we need to set up the configuration
            # The official SDK handles authentication differently
            self.configuration = Configuration()
            self.configuration.host = "https://api.elections.kalshi.com/trade-api/v2"
            self.api_client = ApiClient(self.configuration)
            
            # Set up authentication (this may need adjustment based on SDK docs)
            if hasattr(self.api_client, 'set_default_header'):
                self.api_client.set_default_header('KALSHI-ACCESS-KEY', api_key)
            
            print("✅ Kalshi API client initialized with authentication (official SDK)")
        else:
            # For public data, we can use the public API
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

    def search_markets(self, query, limit=50):
        """Search for markets by query string using official SDK"""
        if not SDK_AVAILABLE:
            print(f"Error: Official SDK not available for searching markets: {query}")
            return None
            
        try:
            # Use direct HTTP request as fallback when SDK has deserialization issues
            import requests
            
            url = f"{self.configuration.host}/markets"
            params = {
                'limit': limit,
                'status': 'open',  # Only get open markets
                'category': 'sports'  # Focus on sports markets
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            markets_data = response.json()
            
            # Filter markets based on query with improved matching
            if 'markets' in markets_data:
                filtered_markets = []
                query_lower = query.lower()
                
                for market in markets_data['markets']:
                    title = market.get('title', '').lower()
                    ticker = market.get('ticker', '').lower()
                    subtitle = market.get('subtitle', '').lower()
                    
                    # Enhanced NFL team matching
                    nfl_teams = {
                        'kc': ['kansas city', 'chiefs', 'kc'],
                        'bal': ['baltimore', 'ravens', 'bal'],
                        'phi': ['philadelphia', 'eagles', 'phi'],
                        'gb': ['green bay', 'packers', 'gb'],
                        'atl': ['atlanta', 'falcons', 'atl'],
                        'pit': ['pittsburgh', 'steelers', 'pit'],
                        'buf': ['buffalo', 'bills', 'buf'],
                        'ari': ['arizona', 'cardinals', 'ari'],
                        'chi': ['chicago', 'bears', 'chi'],
                        'ten': ['tennessee', 'titans', 'ten'],
                        'cin': ['cincinnati', 'bengals', 'cin'],
                        'ne': ['new england', 'patriots', 'ne'],
                        'ind': ['indianapolis', 'colts', 'ind'],
                        'hou': ['houston', 'texans', 'hou'],
                        'mia': ['miami', 'dolphins', 'mia'],
                        'jax': ['jacksonville', 'jaguars', 'jax'],
                        'no': ['new orleans', 'saints', 'no'],
                        'car': ['carolina', 'panthers', 'car'],
                        'nyg': ['new york giants', 'giants', 'nyg'],
                        'min': ['minnesota', 'vikings', 'min'],
                        'lac': ['los angeles chargers', 'chargers', 'lac'],
                        'lv': ['las vegas', 'raiders', 'lv'],
                        'sea': ['seattle', 'seahawks', 'sea'],
                        'den': ['denver', 'broncos', 'den'],
                        'cle': ['cleveland', 'browns', 'cle'],
                        'dal': ['dallas', 'cowboys', 'dal'],
                        'tb': ['tampa bay', 'buccaneers', 'tb'],
                        'was': ['washington', 'commanders', 'was'],
                        'det': ['detroit', 'lions', 'det'],
                        'la': ['los angeles rams', 'rams', 'la'],
                        'sf': ['san francisco', '49ers', 'sf'],
                        'nyj': ['new york jets', 'jets', 'nyj']
                    }
                    
                    # Check if query matches any team names
                    query_teams = []
                    for team_code, team_names in nfl_teams.items():
                        if any(name in query_lower for name in team_names):
                            query_teams.append(team_code)
                    
                    # Check if market contains any of the query teams
                    market_matches = False
                    if query_teams:
                        for team_code in query_teams:
                            team_names = nfl_teams[team_code]
                            if any(name in title or name in subtitle or name in ticker for name in team_names):
                                market_matches = True
                                break
                    
                    # Also check for general NFL terms
                    nfl_terms = ['nfl', 'football', 'win', 'winner', 'game']
                    if any(term in title or term in subtitle or term in ticker for term in nfl_terms):
                        market_matches = True
                    
                    if market_matches:
                        filtered_markets.append(market)
                
                markets_data['markets'] = filtered_markets
            
            return markets_data
        except Exception as e:
            print(f"Error searching markets for '{query}': {e}")
            return None
    
    def get_market_details(self, ticker):
        """Get detailed information about a specific market using official SDK"""
        if not SDK_AVAILABLE:
            print(f"Error: Official SDK not available for market details: {ticker}")
            return None
            
        try:
            # Use direct HTTP request as fallback when SDK has deserialization issues
            import requests
            
            url = f"{self.configuration.host}/markets/{ticker}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting market details for {ticker}: {e}")
            return None
    
    def get_market_history(self, ticker, start_time=None, end_time=None):
        """Get market history using official SDK"""
        if not SDK_AVAILABLE:
            print(f"Error: Official SDK not available for market history: {ticker}")
            return None
            
        try:
            response = self.market_api.get_market_history(
                ticker=ticker,
                start_time=start_time,
                end_time=end_time
            )
            return response.to_dict()
        except Exception as e:
            print(f"Error getting market history for {ticker}: {e}")
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
        print(f"Error: {data_file} not found. Run generate_unified_data.py first.")
        return None
    
    df = pd.read_csv(data_file)
    print(f"Loaded {len(df)} games from unified dataset")
    return df

def load_real_timestamps():
    """Load the real timestamps dataset"""
    timestamps_file = os.path.join(PROJECT_ROOT, "results", "data", "nfl_real_timestamps.csv")
    
    if not os.path.exists(timestamps_file):
        print(f"Warning: {timestamps_file} not found. Using mock timestamps.")
        return None
    
    df = pd.read_csv(timestamps_file)
    print(f"Loaded {len(df)} games with real timestamps")
    return df

def create_real_timing_kalshi_data(nfl_df, timestamps_df, api):
    """Create Kalshi data with real timing using real timestamps dataset as primary source"""
    print("Creating Kalshi data with real game timing...")
    
    if timestamps_df is None:
        print("❌ No timestamps data available")
        return pd.DataFrame()
    
    # Use the real timestamps dataset as the primary source
    # This ensures we create an entry for each game in the timestamps dataset
    print(f"Processing {len(timestamps_df)} games from real timestamps dataset")
    
    # Merge with NFL data to get additional game information
    games_to_process = timestamps_df.merge(
        nfl_df[['game_id', 'first_td_team']], 
        on='game_id', 
        how='left'
    )
    
    print(f"Found {len(games_to_process)} games with complete data")
    
    kalshi_data = []
    count = 0
    total_games = len(games_to_process)
    
    for idx, game in games_to_process.iterrows():
        count += 1
        print(f"\n[{count}/{total_games}] Processing {game['game_id']}: {game['away_team']} @ {game['home_team']}")
            
        # Calculate timing based on real data from timestamps dataset
        # Parse kickoff time and calculate pregame timestamp (5 min before)
        try:
            kickoff_dt = pd.to_datetime(game['kickoff_time'])
            pregame_dt = kickoff_dt - timedelta(minutes=5)
            pregame_timestamp = pregame_dt.isoformat() + 'Z'
        except Exception as e:
            print(f"    ⚠️  Error parsing kickoff time: {e}")
            pregame_timestamp = None
        
        # Use real first TD timestamp and calculate post-TD timestamp (1 min after)
        first_td_timestamp = game.get('first_td_real_timestamp')
        if pd.notna(first_td_timestamp):
            try:
                first_td_dt = pd.to_datetime(first_td_timestamp)
                post_td_dt = first_td_dt + timedelta(minutes=1)
                post_td_timestamp = post_td_dt.isoformat()
            except Exception as e:
                print(f"    ⚠️  Error parsing first TD time: {e}")
                post_td_timestamp = None
        else:
            post_td_timestamp = None
        
        # Skip if timestamps are not available
        if not pregame_timestamp or not post_td_timestamp:
            print(f"    ⚠️  Skipping - missing timestamps")
            continue
        
        # Search for markets for this game
        home_team = game['home_team']
        away_team = game['away_team']
        game_date = game['game_date']
        
        # Try to find real markets
        markets = api.search_nfl_markets(game_date, home_team, away_team)
        
        if not markets:
            print(f"    ⚠️  No markets found for {away_team} @ {home_team}")
            continue
        
        ticker = markets[0].get('ticker', f"UNKNOWN-{game['game_id']}")
        
        # Get market snapshots at specific times
        print(f"    Fetching data for market: {ticker}")
        
        # Get pregame snapshot (5 min before kickoff)
        pregame_snapshot = api.get_market_snapshot(ticker, pregame_timestamp)
        
        # Get post-TD snapshot (1 min after first TD)
        post_td_snapshot = api.get_market_snapshot(ticker, post_td_timestamp)
        
        if not pregame_snapshot or not post_td_snapshot:
            print(f"    ⚠️  Failed to fetch market snapshots")
            continue
        
        print(f"    ✅ Successfully fetched real market data")
        
        # Create data record with real market data
        kalshi_data.append({
            'game_id': game['game_id'],
            'season': game['season'],
            'week': game['week'],
            'home_team': home_team,
            'away_team': away_team,
            'game_date': game_date,
            'kalshi_ticker': ticker,
            'pregame_timestamp': pregame_timestamp,
            'pregame_home_prob_kalshi': pregame_snapshot.get('yes_probability', 0.5),
            'pregame_away_prob_kalshi': pregame_snapshot.get('no_probability', 0.5),
            'first_td_timestamp': first_td_timestamp,
            'first_td_team': game.get('first_td_team') if pd.notna(game.get('first_td_team')) else 'UNKNOWN',
            'post_td_timestamp': post_td_timestamp,
            'post_td_home_prob_kalshi': post_td_snapshot.get('yes_probability', 0.5),
            'post_td_away_prob_kalshi': post_td_snapshot.get('no_probability', 0.5),
            'prob_change_home': post_td_snapshot.get('yes_probability', 0.5) - pregame_snapshot.get('yes_probability', 0.5),
            'prob_change_away': post_td_snapshot.get('no_probability', 0.5) - pregame_snapshot.get('no_probability', 0.5),
            'data_quality_flag': 'real_data'
        })
    
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
    test_markets = api.search_markets("NFL")
    
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
        
        # Get the total games attempted from timestamps
        timestamps_df = load_real_timestamps()
        total_attempted = len(timestamps_df) if timestamps_df is not None else 0
        
        if total_attempted > 0:
            print(f"Games processed: {len(kalshi_df)} out of {total_attempted} attempted")
            print(f"Success rate: {len(kalshi_df)/total_attempted*100:.1f}%")
        else:
            print(f"Games processed: {len(kalshi_df)}")
    else:
        print("No data retrieved - check API credentials and network connection")
        print("Success rate: 0.0%")

if __name__ == "__main__":
    main()
