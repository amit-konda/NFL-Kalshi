# NFL First Touchdown Analysis for Kalshi Trading

This project analyzes NFL regular season games (2020-2024) to understand the impact of scoring the first touchdown on win probability, incorporating pregame Vegas odds and opening possession data.

## 📁 Project Organization

The project is organized into clear categories:
- **`docs/`** - All documentation (you are here!)
- **`scripts/`** - Data generation (`scripts/data/`) and analysis (`scripts/analysis/`)
- **`results/`** - Generated datasets (`results/data/`) and analysis outputs (`results/analysis/`)
- **`visualizations/`** - All charts and graphs (PNG files)
- **Root** - Dashboard, verification, and utilities

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed layout and workflow.

## 🎨 Interactive Dashboard

**View all analyses in a beautiful interactive dashboard:**

```bash
streamlit run dashboard.py
```

Opens at: http://localhost:8501

Features:
- 📊 All visualizations and analyses in one place
- 🔍 Interactive data explorer with filters
- 📈 Real-time metrics and statistics
- 💾 Export filtered data
- 📱 Mobile-friendly responsive design

See [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) for detailed instructions.

## 📊 Main Dataset

**`results/data/nfl_unified_data.csv`** - Single source of truth containing all game data:
- Game identifiers and basic info (game_id, season, home/away teams)
- First touchdown data (which team scored, player, play type)
- Game outcomes (winner, scores)
- Pregame Vegas odds (moneyline, spreads, implied probabilities)
- Opening possession data (which team received the kickoff)
- Derived metrics (favorite won, opening possession scored first, etc.)

**Total: 1,334 games, 24 columns**

## 🔧 Data Generation

**`scripts/data/generate_unified_data.py`** - Master script that creates the unified dataset
- Downloads play-by-play and schedule data from nfl_data_py
- Identifies first touchdown in each game
- Adds pregame moneyline odds and implied probabilities
- Determines opening possession for each game
- Creates derived columns for analysis
- **Run this to regenerate the dataset from scratch**

To run:
```bash
cd scripts/data
python3 generate_unified_data.py
```

## 📈 Analysis & Visualization Workflow

### Controlled First TD Analysis (current workflow)

- **`scripts/analysis/controlled_first_td_modeling.py`**
  - Fits logistic models (basic, controlled, interaction)
  - Computes marginal effects at 1% and 5% intervals
  - Calculates tier-specific correlations and win-probability curves
  - Writes CSVs to `results/analysis/` and `model_summaries.txt`

- **`scripts/analysis/controlled_first_td_visualizations.py`**
  - Reads CSVs and generates all plots in `visualizations/`
  - Produces: `controlled_first_td_analysis.png`, `first_td_marginal_effects.png`,
    `first_td_marginal_effects_1pct.png`, `first_td_win_probability_curves.png`,
    `first_td_win_probability_curves_5pct.png`, `first_td_correlations.png`,
    `first_td_raw_data_scatter.png`, `model_comparison.png`

### Utilities

- **`verify_setup.py`** - Project verification utility
  - Checks that all data files exist and are properly formatted
  - Validates data completeness
  - Useful for troubleshooting

## 📁 Output Files

### Main Data
- `nfl_unified_data.csv` - Complete unified dataset ⭐

### Visualizations (in `visualizations/` folder)
- `controlled_first_td_analysis.png` - 4-panel overview
- `first_td_marginal_effects.png` - 5% interval marginal effects
- `first_td_marginal_effects_1pct.png` - 1% interval marginal effects
- `first_td_win_probability_curves.png` - 1% interval curves
- `first_td_win_probability_curves_5pct.png` - 5% interval labeled curves
- `first_td_correlations.png` - Correlation matrix
- `first_td_raw_data_scatter.png` - Raw data overlay
- `model_comparison.png` - AIC/BIC comparison

### Derived Statistics
- `opening_possession_stratified_stats.csv` - Statistics by pregame bucket

### Documentation
- `README.md` - Complete project documentation
- `QUICK_START.md` - Quick reference guide

## 🎯 Key Findings

### First Touchdown Impact
- Teams scoring first TD win **68%** of games overall
- Average probability boost from scoring first: **+11.2 percentage points**
- Average probability drop from opponent scoring: **-15.5 percentage points**
- Total swing: **~27 percentage points**

### Opening Possession
- Teams getting ball first score first TD **56.1%** of the time
- Advantage from opening possession: **+12.3 percentage points**
- Correlation: **0.123** (modest but significant)
- **Underdogs benefit more** from opening possession (+14.9pp vs +12.4pp for favorites)

### Pregame Odds
- Vegas favorites win **67%** of games
- When favorite scores first TD: **80%** win rate
- When underdog scores first TD: **51%** win rate (essentially a toss-up)

### Combined Effects (Most Important for Trading)
- **70-75% favorites getting ball first**: 80.8% chance to score first TD
- Opening possession has **biggest impact** on strong favorites and heavy underdogs
- Pick-em games (45-50% pregame): First TD essentially decides the game (+18.6pp swing)

## 🚀 Usage

### To Regenerate All Data
```bash
python3 generate_unified_data.py
```

### To Run Analyses
```bash
cd scripts/analysis

# Modeling (creates CSVs in results/analysis/)
python3 controlled_first_td_modeling.py

# Visualizations (creates PNGs in visualizations/)
python3 controlled_first_td_visualizations.py

cd ../..
```

### To Use Data in Custom Analysis
```python
import pandas as pd

# Load the unified dataset
df = pd.read_csv("results/data/nfl_unified_data.csv")

# Example: Filter to favorites who got ball first
favorites_with_ball = df[
    (df['favored_team_prob'] > 0.6) & 
    (df['opening_possession_scored_first'] == 1)
]
```

## 📦 Dependencies

Install all required packages:

```bash
pip3 install -r requirements.txt
```

Or install individually:
```bash
pip3 install pandas nfl_data_py matplotlib numpy scipy
```

### IDE Setup (VSCode/Cursor)

If you see import warnings in your IDE:
1. Make sure you're using the correct Python interpreter (Cmd+Shift+P → "Python: Select Interpreter")
2. The interpreter should match the one where packages are installed (check with `which python3`)
3. Reload the window (Cmd+Shift+P → "Developer: Reload Window")

## 📅 Data Coverage

- **Seasons**: 2020-2024
- **Games**: 1,334 regular season games
- **Completeness**: 100% for all metrics (moneyline, spread, first TD, opening possession)

## 💡 Trading Implications for Kalshi

1. **Opening possession + pregame odds** = powerful combined predictor
2. **Heavy favorites (70-75%) are most impacted** by who gets ball first
3. **Underdogs scoring first** creates near 50/50 odds despite pregame lines
4. **Live betting edge**: Market may overreact to favorites falling behind early
5. **First TD is worth ~27pp of win probability** on average

## 🔄 Future Enhancements

Potential additions:
- Expand to 2015-2024 (full 10 years)
- Add weather data correlation
- Include point differential at first TD
- Track first TD type (rush/pass/defense/special teams)
- Model exact win probability given (pregame odds + opening possession + first TD)

