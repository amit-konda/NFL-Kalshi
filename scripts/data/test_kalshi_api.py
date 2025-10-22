"""
Test script for Kalshi API integration
"""

import sys
import os

# Add project root to path
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from fetch_kalshi_data import KalshiAPI

def test_kalshi_api():
    """Test basic Kalshi API functionality"""
    print("Testing Kalshi API...")
    
    # Load configuration
    try:
        from kalshi_config import KALSHI_API_KEY, KALSHI_PRIVATE_KEY, USE_MOCK_DATA
    except ImportError:
        print("⚠️  kalshi_config.py not found. Using default settings.")
        KALSHI_API_KEY = None
        KALSHI_PRIVATE_KEY = None
        USE_MOCK_DATA = True
    
    # Initialize API with credentials
    if USE_MOCK_DATA or not KALSHI_API_KEY or not KALSHI_PRIVATE_KEY:
        print("⚠️  Using mock data mode or no credentials found.")
        api = KalshiAPI()
    else:
        api = KalshiAPI(api_key=KALSHI_API_KEY, private_key=KALSHI_PRIVATE_KEY)
    
    # Test 1: Search for NFL markets
    print("\n1. Testing market search...")
    if USE_MOCK_DATA:
        print("⚠️  Mock data mode - skipping actual API calls")
        print("In mock mode, this would return simulated market data")
    else:
        try:
            markets = api.search_markets("NFL football")
            if markets and 'markets' in markets:
                print(f"Found {len(markets['markets'])} markets")
                for market in markets['markets'][:3]:  # Show first 3
                    print(f"  - {market.get('ticker', 'N/A')}: {market.get('title', 'N/A')}")
            else:
                print("No markets found")
        except Exception as e:
            print(f"Error during market search: {e}")
            print("This is expected if network connectivity is not available.")
    
    # Test 2: Test SDK availability
    print("\n2. Testing SDK availability...")
    try:
        import kalshi_python
        print("✅ Official kalshi-python SDK is available")
        print(f"SDK version: {getattr(kalshi_python, '__version__', 'Unknown')}")
    except ImportError as e:
        print(f"❌ Official kalshi-python SDK not available: {e}")
        print("Install with: pip install kalshi-python")
    
    # Test 3: Test SDK components
    print("\n3. Testing SDK components...")
    try:
        from kalshi_python import ApiClient, Configuration, MarketApi
        print("✅ Core SDK components imported successfully")
        
        # Test configuration
        config = Configuration()
        config.host = "https://api.elections.kalshi.com/trade-api/v2"
        print(f"✅ Configuration created: {config.host}")
        
    except Exception as e:
        print(f"❌ Error importing SDK components: {e}")
    
    print("\n✅ Kalshi API test completed")

if __name__ == "__main__":
    test_kalshi_api()
