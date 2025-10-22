# 🏈 Dashboard Guide

## 🚀 Launching the Dashboard

The interactive dashboard displays all analyses, visualizations, and key findings in a user-friendly interface.

### Quick Start

```bash
cd /Users/amitk./Downloads/NFL-Kalshi
streamlit run dashboard.py
```

The dashboard will automatically open in your default browser at **http://localhost:8501**

### First Time Setup

If you haven't installed the dependencies:

```bash
pip3 install -r requirements.txt
```

## 📊 Dashboard Features

### Navigation

Use the **sidebar** on the left to navigate between different sections:

#### 🏠 Overview
- Summary of all key findings
- Quick statistics and metrics
- High-level insights
- Summary table of results by pregame odds

#### 📈 First TD Probability Changes
- Interactive visualization of win probability changes
- Impact by 5% pregame probability buckets
- Shows both "scored first TD" and "opponent scored" scenarios
- Key takeaways and insights

#### 🏈 Opening Possession Impact
- Analysis of how receiving the kickoff affects first TD
- Correlation analysis by pregame odds
- Stratified statistics table
- Detailed breakdown by tier

#### 🔗 Correlation Analysis
- Correlation matrix between all key variables
- Scatter plots and relationship visualizations
- Statistical interpretation
- Key insights about independent predictive value

#### 📊 Logistic Regression
- Full logistic regression results
- Model coefficients and odds ratios
- Tier-specific analysis
- Model predictions visualization
- Trading implications

#### 📋 Data Explorer
- Interactive data browser
- Filter by season, team, first TD status
- Summary statistics
- Download filtered data as CSV

## 🎯 Key Features

### Interactive Filters
In the Data Explorer, you can:
- **Select seasons** (2020-2024)
- **Filter by teams** (any team as home or away)
- **Filter by first TD status**
- **Download** filtered data

### Metrics Display
Each page shows relevant metrics with:
- ✅ **Value indicators** (↑ positive, ↓ negative)
- 📊 **Statistical significance**
- 💡 **Contextual explanations**

### Visualizations
All charts are displayed in high resolution and can be:
- Viewed in full size
- Analyzed in detail
- Cross-referenced with data

## 🔧 Troubleshooting

### Port Already in Use

If you get "Port 8501 is already in use":

```bash
# Find and kill the process
lsof -ti:8501 | xargs kill -9

# Or use a different port
streamlit run dashboard.py --server.port 8502
```

### Dashboard Won't Load

1. Check that all image files exist in `visualizations/`:
   - `visualizations/first_td_probability_changes.png`
   - `visualizations/opening_possession_impact.png`
   - `visualizations/first_td_correlations.png`
   - `visualizations/logistic_regression_analysis.png`

2. Check that data files exist:
   - `nfl_unified_data.csv`
   - `opening_possession_stratified_stats.csv`
   - `logistic_regression_results.csv`

3. Regenerate if needed:
   ```bash
   python3 generate_unified_data.py
   python3 opening_possession_analysis.py
   python3 visualize_odds_v2.py
   python3 visualize_opening_possession.py
   python3 first_td_correlations.py
   python3 logistic_regression_analysis.py
   ```

### Slow Loading

- First load may be slow as Streamlit caches data
- Subsequent page navigation is fast
- Clear cache: Click hamburger menu (☰) → "Clear cache"

## 🎨 Customization

You can customize the dashboard by editing `dashboard.py`:

### Change Colors
Look for the CSS in the `st.markdown()` section at the top

### Add New Pages
Add new options to the `st.sidebar.radio()` section

### Modify Metrics
Update the `st.metric()` calls with your own calculations

## 📱 Accessing from Other Devices

To access the dashboard from other devices on your network:

```bash
streamlit run dashboard.py --server.address 0.0.0.0
```

Then access via: `http://YOUR_IP_ADDRESS:8501`

Find your IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## ⌨️ Keyboard Shortcuts

- `Cmd/Ctrl + K`: Focus search
- `R`: Rerun the app
- `C`: Clear cache
- `?`: Show keyboard shortcuts

## 🛑 Stopping the Dashboard

Press `Ctrl + C` in the terminal where the dashboard is running.

## 💡 Tips

1. **Bookmark it**: Save `http://localhost:8501` for quick access
2. **Wide mode**: Dashboard is optimized for wide screen layout
3. **Dark mode**: Click hamburger menu (☰) → Settings → Theme
4. **Export data**: Use the Data Explorer to download filtered CSVs
5. **Refresh**: Dashboard auto-updates when you change files

## 📊 Best Practices

- **Start with Overview** to get context
- **Use Data Explorer** for custom analysis
- **Export results** for presentations
- **Cross-reference** between different analysis pages
- **Check correlations** to understand relationships

## 🎓 Understanding the Analyses

Each section builds on previous ones:

1. **Overview** → High-level summary
2. **First TD Changes** → Win probability shifts
3. **Opening Possession** → Contributing factor
4. **Correlations** → Statistical relationships
5. **Logistic Regression** → Controlled, causal analysis
6. **Data Explorer** → Raw data validation

## 🔄 Updating Data

When you update the underlying data:

1. Regenerate all analyses
2. Restart the dashboard (or click "Rerun")
3. Clear cache if needed
4. Dashboard will show updated results

## 📝 Notes

- Dashboard is read-only (doesn't modify data)
- All calculations are done on cached data for speed
- Images are loaded once and cached
- CSV exports include current filters only

