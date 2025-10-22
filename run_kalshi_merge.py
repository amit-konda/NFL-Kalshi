#!/usr/bin/env python3
"""
Run Kalshi data merging script
"""

import sys
import os

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.join(SCRIPT_DIR, 'scripts', 'data')
sys.path.append(SCRIPTS_DIR)

from merge_kalshi_data import main

if __name__ == "__main__":
    print("Starting Kalshi data merge...")
    print("This will merge the Kalshi dataset with the unified NFL dataset")
    print()
    
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
