# 📁 Project Structure

This document describes the organization of the NFL First Touchdown Analysis project.

## Directory Layout

```
NFL-Kalshi/
├── 📄 dashboard.py              # Interactive Streamlit dashboard
├── 📄 verify_setup.py           # Project verification script
├── 📄 launch_dashboard.sh       # Dashboard launcher
├── 📄 requirements.txt          # Python dependencies
│
├── 📂 docs/                     # Documentation
│   ├── README.md                # Main project README
│   ├── QUICK_START.md           # Quick start guide
│   ├── DASHBOARD_GUIDE.md       # Dashboard usage guide
│   ├── TROUBLESHOOTING.md       # Common issues and solutions (incl. interpreter setup)
│   └── PROJECT_STRUCTURE.md     # This file
│
├── 📂 scripts/                  # All analysis and data scripts
│   ├── 📂 data/                # Data generation scripts
│   │   └── generate_unified_data.py  # Main data pipeline
│   │
│   └── 📂 analysis/            # Analysis scripts
│       ├── controlled_first_td_modeling.py       # Modeling + CSVs
│       └── controlled_first_td_visualizations.py # All plots
│
├── 📂 results/                  # Output data and results
│   ├── 📂 data/                # Generated datasets
│   │   └── nfl_unified_data.csv  # Main unified dataset ⭐
│   │
│   └── 📂 analysis/            # Analysis results (CSVs)
│       ├── controlled_first_td_results.csv
│       ├── first_td_marginal_effects.csv
│       ├── first_td_marginal_effects_1pct.csv
│       ├── first_td_win_probabilities.csv
│       └── first_td_win_probabilities_5pct.csv
│
└── 📂 visualizations/           # Generated charts (PNGs)
    ├── controlled_first_td_analysis.png
    ├── first_td_correlations.png
    ├── first_td_marginal_effects.png
    ├── first_td_marginal_effects_1pct.png
    ├── first_td_win_probability_curves.png
    ├── first_td_win_probability_curves_5pct.png
    ├── first_td_raw_data_scatter.png
    └── model_comparison.png
```

## File Categories

### 🏠 Root Level

**Dashboard & Utilities:**
- `dashboard.py` - Main interactive dashboard application
- `verify_setup.py` - Verifies project setup and data completeness
- `launch_dashboard.sh` - Convenience script to launch dashboard
- `requirements.txt` - Python package dependencies

### 📚 Documentation (`docs/`)

All project documentation in one place:
- **README.md** - Main project documentation, explains everything
- **QUICK_START.md** - Get started quickly
- **DASHBOARD_GUIDE.md** - Complete dashboard usage guide
- **DASHBOARD_README.txt** - Quick dashboard reference
- **SETUP_INTERPRETER.md** - Python interpreter configuration
- **TROUBLESHOOTING.md** - Common issues and fixes
- **PROJECT_STRUCTURE.md** - This file!

### 🔧 Scripts (`scripts/`)

#### Data Scripts (`scripts/data/`)

Scripts for downloading and processing raw data:
- **generate_unified_data.py** - Downloads NFL data and creates unified dataset
  - Inputs: nfl_data_py package (downloads from internet)
  - Outputs: `results/data/nfl_unified_data.csv`
  - Runtime: ~5-10 minutes (downloads play-by-play data)

#### Analysis Scripts (`scripts/analysis/`)

All analysis and visualization scripts:

**Correlation Analysis:**
- **first_td_correlations.py** - Calculates correlations between variables
  - Reads: `results/data/nfl_unified_data.csv`
  - Outputs: `visualizations/first_td_correlations.png`

**Regression Analysis:**
- **logistic_regression_analysis.py** - Logistic regression models
  - Reads: `results/data/nfl_unified_data.csv`
  - Outputs: 
    - `visualizations/logistic_regression_analysis.png`
    - `results/analysis/logistic_regression_results.csv`

- **controlled_first_td_analysis.py** - Controlled regression (most rigorous)
  - Reads: `results/data/nfl_unified_data.csv`
  - Outputs:
    - `visualizations/controlled_first_td_analysis.png`
    - `results/analysis/controlled_first_td_results.csv`

**Specialized Analysis:**
- **opening_possession_analysis.py** - Opening possession impact
  - Reads: `results/data/nfl_unified_data.csv`
  - Outputs: `results/analysis/opening_possession_stratified_stats.csv`

**Visualization:**
- **visualize_odds_v2.py** - First TD probability changes viz
  - Reads: `results/data/nfl_unified_data.csv`
  - Outputs: `visualizations/first_td_probability_changes.png`

- **visualize_opening_possession.py** - Opening possession viz
  - Reads: `results/analysis/opening_possession_stratified_stats.csv`
  - Outputs: `visualizations/opening_possession_impact.png`

### 📊 Results (`results/`)

#### Data (`results/data/`)

Generated datasets:
- **nfl_unified_data.csv** - Main unified dataset (⭐ single source of truth)
  - 1,334 games (2020-2024 regular season)
  - 24 columns with all analysis data
  - Generated by: `scripts/data/generate_unified_data.py`

#### Analysis (`results/analysis/`)

Analysis result CSVs:
- **controlled_first_td_results.csv** - Tier-specific correlations
- **logistic_regression_results.csv** - Regression results by tier
- **opening_possession_stratified_stats.csv** - Opening possession statistics

### 🎨 Visualizations (`visualizations/`)

All generated charts (PNG format):
- **controlled_first_td_analysis.png** - Controlled analysis results
- **first_td_correlations.png** - Correlation analysis
- **first_td_probability_changes.png** - Probability shifts
- **logistic_regression_analysis.png** - Regression results
- **opening_possession_impact.png** - Opening possession analysis
- **pregame_vs_actual_odds.png** - Calibration plots

## Workflow

### 1. Initial Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Generate data (run once, or when you want to update data)
cd scripts/data
python3 generate_unified_data.py
cd ../..
```

### 2. Run Analysis

```bash
# Run all analyses from root directory
cd scripts/analysis

# Correlation analysis
python3 first_td_correlations.py

# Regression analyses
python3 logistic_regression_analysis.py
python3 controlled_first_td_analysis.py

# Opening possession
python3 opening_possession_analysis.py

# Visualizations
python3 visualize_odds_v2.py
python3 visualize_opening_possession.py

# Return to root
cd ../..
```

### 3. View Results

**Option A: Dashboard (Recommended)**
```bash
streamlit run dashboard.py
# Or use: ./launch_dashboard.sh
```

**Option B: Direct File Access**
- View PNGs in `visualizations/`
- Open CSVs in `results/analysis/`
- Explore data in `results/data/nfl_unified_data.csv`

## Key Design Principles

1. **Separation of Concerns**
   - Data generation separate from analysis
   - Analysis separate from visualization
   - Results segregated by type

2. **Single Source of Truth**
   - One unified dataset: `results/data/nfl_unified_data.csv`
   - All analyses read from this file

3. **Clear Output Locations**
   - CSVs go to `results/`
   - PNGs go to `visualizations/`
   - No output files at root level

4. **Documentation Centralized**
   - All docs in `docs/` folder
   - Easy to find and maintain

5. **Intuitive Organization**
   - Scripts grouped by purpose
   - Results grouped by type
   - Clear naming conventions

## File Dependencies

```
generate_unified_data.py
    ↓ creates
results/data/nfl_unified_data.csv
    ↓ used by
├─ first_td_correlations.py → visualizations/first_td_correlations.png
├─ logistic_regression_analysis.py → {
│       visualizations/logistic_regression_analysis.png
│       results/analysis/logistic_regression_results.csv
│   }
├─ controlled_first_td_analysis.py → {
│       visualizations/controlled_first_td_analysis.png
│       results/analysis/controlled_first_td_results.csv
│   }
├─ opening_possession_analysis.py → results/analysis/opening_possession_stratified_stats.csv
│       ↓ used by
│   visualize_opening_possession.py → visualizations/opening_possession_impact.png
└─ visualize_odds_v2.py → visualizations/first_td_probability_changes.png

dashboard.py (reads from all results/ and visualizations/)
```

## Notes

- Scripts should be run from the root directory or from within their respective folders
- All scripts use relative paths that work from their location
- Dashboard must be run from root directory: `streamlit run dashboard.py`
- `verify_setup.py` checks that all files are in the correct locations

## Updating Data

To refresh the analysis with new data:

```bash
# 1. Regenerate unified dataset
cd scripts/data
python3 generate_unified_data.py
cd ../..

# 2. Rerun desired analyses
cd scripts/analysis
python3 <analysis_script>.py
cd ../..

# 3. Dashboard will automatically show updated results
streamlit run dashboard.py
```

