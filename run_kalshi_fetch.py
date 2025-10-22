#!/usr/bin/env python3
"""
Runner script for Kalshi data fetching
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

from scripts.data.fetch_kalshi_data import main

if __name__ == "__main__":
    print("Starting Kalshi data fetch...")
    print("Note: This may take a while due to API rate limiting")
    print("Press Ctrl+C to cancel")
    print()
    
    main()
