# Quick Start Guide

## 🎨 Interactive Dashboard (Recommended!)

**Easiest way to explore the analysis:**

```bash
streamlit run dashboard.py
```

Opens at **http://localhost:8501**

Features all analyses, visualizations, and data explorer in one place!

See [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) for full instructions.

---

## 🔧 Setup

Install required packages:
```bash
pip3 install -r requirements.txt
```

## 📁 Project Structure

Files are organized by category:
- **`docs/`** - All documentation (you are here!)
- **`scripts/data/`** - Data generation scripts
- **`scripts/analysis/`** - Analysis and visualization scripts
- **`results/data/`** - Generated datasets
- **`results/analysis/`** - Analysis outputs (CSVs)
- **`visualizations/`** - Charts and graphs (PNGs)

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed layout.

## 📊 Single Source of Truth

**`results/data/nfl_unified_data.csv`** - One unified dataset with everything:
- 1,334 games (2020-2024 regular season)
- 24 columns including first TD, Vegas odds, opening possession
- 100% complete data

## 🚀 Quick Commands

### Verify Everything Works
```bash
python3 verify_setup.py
```

### Regenerate Data (if needed)
```bash
cd scripts/data
python3 generate_unified_data.py
cd ../..
```

### Run Analyses
```bash
cd scripts/analysis

# Modeling (creates CSVs)
python3 controlled_first_td_modeling.py

# Visualizations (creates PNGs)
python3 controlled_first_td_visualizations.py

cd ../..
```

### Use Data in Your Own Analysis
```python
import pandas as pd

# Load unified dataset
df = pd.read_csv("results/data/nfl_unified_data.csv")

# Example queries
favorites = df[df['favored_team_prob'] > 0.6]
underdogs_with_ball = df[(df['home_prob'] < 0.5) & (df['home_got_ball_first'] == 1)]
```

## 📁 Key Files

### Data
- ✅ `results/data/nfl_unified_data.csv` - Main dataset (single source of truth!)

### Scripts
- **Data:** `scripts/data/generate_unified_data.py` - Regenerates dataset
- **Analysis:** `scripts/analysis/*.py` - All analysis scripts
- **Utility:** `dashboard.py`, `verify_setup.py` - Dashboard and verification

### Outputs
- **Visualizations:** `visualizations/*.png` - All charts
- **Analysis Results:** `results/analysis/*.csv` - Analysis outputs

## 🎯 Key Insights

- **First TD = +11.2pp boost, opponent scoring = -15.5pp penalty**
- **Opening possession = +12.3pp advantage** (56.1% score first TD)
- **Total first TD swing = ~27 percentage points**
- **Underdogs benefit MORE from opening possession** (+14.9pp vs +12.4pp)
- **70-75% favorites with ball first = 80.8% to score first TD**

## 📚 Full Documentation

See `docs/README.md` for complete documentation.

