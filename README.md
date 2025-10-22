# NFL First Touchdown Analysis

Explore how scoring the first touchdown affects NFL win probability (2020–2024), controlling for pregame odds and opening possession.

## Quick Start

```bash
pip3 install -r requirements.txt

# Generate data (if needed)
cd scripts/data && python3 generate_unified_data.py && cd ../..

# Run analysis
cd scripts/analysis
python3 controlled_first_td_modeling.py
python3 controlled_first_td_visualizations.py
cd ../..

# Launch dashboard
streamlit run dashboard.py
```

## Key Files
- `results/data/nfl_unified_data.csv` – unified dataset (single source of truth)
- `results/analysis/*.csv` – analysis outputs
- `visualizations/*.png` – generated charts
- `dashboard.py` – Streamlit dashboard

## Documentation
- `docs/README.md` – full project docs
- `docs/QUICK_START.md` – quick reference
- `docs/DASHBOARD_GUIDE.md` – dashboard usage
- `docs/PROJECT_STRUCTURE.md` – repo layout
- `docs/TROUBLESHOOTING.md` – fixes for common issues

## Status
All analyses and the dashboard read from `results/` and `visualizations/`. Re-run the modeling script if data changes.


