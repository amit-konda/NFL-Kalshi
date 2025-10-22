#!/usr/bin/env python3
"""
Run Kalshi analysis script
"""

import sys
import os

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.join(SCRIPT_DIR, 'scripts', 'analysis')
sys.path.append(SCRIPTS_DIR)

from kalshi_analysis import main

if __name__ == "__main__":
    print("Starting Kalshi analysis...")
    print("This will analyze Kalshi vs Vegas odds and first TD impact")
    print()
    
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
