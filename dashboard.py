"""
NFL First Touchdown Analysis Dashboard

Interactive dashboard displaying all analyses, visualizations, and key findings.
Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="NFL First TD Analysis",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .key-finding {
        background-color: #e7f3ff;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🏈 NFL First Touchdown Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown("### Comprehensive analysis of first touchdown impact on win probability (2020-2024)")

# Sidebar
st.sidebar.title("📊 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Analysis:",
    [
        "🏠 Overview",
        "📈 First TD Probability Changes",
        "🏈 Opening Possession Impact",
        "🔗 Correlation Analysis",
        "📊 Logistic Regression",
        "🎯 Controlled Analysis (Marginal Effects)",
        "📋 Data Explorer"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Dataset Info")
st.sidebar.info("""
**Coverage:** 2020-2024 NFL Regular Season

**Games:** 1,334

**Data Points:** 
- First TD by team
- Pregame moneyline odds
- Opening possession
- Game outcomes
""")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("results/data/nfl_unified_data.csv")
        return df
    except:
        return None

df = load_data()

# Helper function to load and display images
def display_image(image_path, caption=""):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.image(img, caption=caption, use_container_width=True)
    else:
        st.warning(f"⚠️ Image not found: {image_path}")

# ============================================================================
# OVERVIEW PAGE
# ============================================================================
if page == "🏠 Overview":
    st.markdown('<div class="sub-header">📊 Key Findings Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="First TD Win Rate",
            value="68.0%",
            delta="+36.3pp vs no TD"
        )
    
    with col2:
        st.metric(
            label="Pregame Odds Accuracy",
            value="67.0%",
            delta="Favorites win"
        )
    
    with col3:
        st.metric(
            label="Opening Possession Advantage",
            value="+12.3pp",
            delta="Score first TD"
        )
    
    with col4:
        st.metric(
            label="Odds Ratio (Logistic)",
            value="4.08x",
            delta="Win odds multiplier"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="key-finding">', unsafe_allow_html=True)
        st.markdown("#### 🎯 First TD Impact")
        st.markdown("""
        - **+11.2pp** boost when scoring first
        - **-15.5pp** penalty when opponent scores
        - **~27pp total swing** from first TD
        - Effect consistent across all pregame odds
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="key-finding">', unsafe_allow_html=True)
        st.markdown("#### 📊 Correlation Analysis")
        st.markdown("""
        - **First TD → Win:** r = 0.363 (moderate-strong)
        - **Pregame Odds → Win:** r = 0.405 (strong)
        - **Pregame → First TD:** r = 0.206 (weak)
        - First TD adds **independent value**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="key-finding">', unsafe_allow_html=True)
        st.markdown("#### 🏈 Opening Possession")
        st.markdown("""
        - Teams with ball first: **56.1%** score first TD
        - Correlation: **0.123** (significant)
        - **Underdogs benefit more** (+14.9pp vs +12.4pp)
        - 70-75% favorites with ball: **80.8%** first TD rate
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="key-finding">', unsafe_allow_html=True)
        st.markdown("#### 💰 Trading Implications")
        st.markdown("""
        - First TD is **major independent event**
        - **~30pp win probability shift** (controlled model)
        - Effect varies by pregame odds (25-35pp range)
        - Markets may underreact to first TD
        - **Potential arbitrage opportunities**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats by Pregame Odds")
    
    stats_data = {
        "Pregame Tier": ["Heavy Dog (≤30%)", "Slight Dog (30-45%)", "Even (45-55%)", 
                         "Slight Fav (55-70%)", "Heavy Fav (>70%)"],
        "Without First TD": ["9.2%", "24.5%", "31.3%", "43.7%", "60.2%"],
        "With First TD": ["38.6%", "51.3%", "66.1%", "75.5%", "87.5%"],
        "Impact": ["+29.4pp", "+26.8pp", "+34.8pp", "+31.8pp", "+27.3pp"],
        "Odds Ratio": ["5.94x", "3.25x", "4.27x", "3.94x", "4.42x"]
    }
    
    st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)

# ============================================================================
# FIRST TD PROBABILITY CHANGES
# ============================================================================
elif page == "📈 First TD Probability Changes":
    st.markdown('<div class="sub-header">First TD Probability Changes by Pregame Odds</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This analysis shows how win probability changes after the first touchdown,
    stratified by pregame win probability in 5% buckets.
    """)
    
    display_image("visualizations/first_td_probability_changes.png", "First TD Impact Analysis")
    
    st.markdown("---")
    st.markdown("### 🔑 Key Takeaways")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **When Scoring First TD:**
        - Average boost: **+11.2 percentage points**
        - Biggest boost: **45-50% pregame** (+18.6pp)
        - Consistent across all tiers
        - Even heavy favorites benefit significantly
        """)
    
    with col2:
        st.warning("""
        **When Opponent Scores:**
        - Average penalty: **-15.5 percentage points**
        - Biggest penalty: **75-80% pregame** (-25.4pp)
        - Favorites lose more from opponent scoring
        - Total swing: **~27 percentage points**
        """)

# ============================================================================
# OPENING POSSESSION IMPACT
# ============================================================================
elif page == "🏈 Opening Possession Impact":
    st.markdown('<div class="sub-header">Opening Possession Impact on First TD</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Analysis of how receiving the opening kickoff affects the probability of
    scoring the first touchdown, stratified by pregame odds.
    """)
    
    display_image("visualizations/opening_possession_impact.png", "Opening Possession Analysis")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Correlation", "0.123", help="Between opening possession and first TD")
    
    with col2:
        st.metric("Avg Advantage", "+12.3pp", help="From getting ball first")
    
    with col3:
        st.metric("Biggest Impact", "+34.6pp", help="70-75% favorites")
    
    st.markdown("---")
    st.markdown("### 📊 Stratified Results")
    
    if os.path.exists("results/analysis/opening_possession_stratified_stats.csv"):
        stats_df = pd.read_csv("results/analysis/opening_possession_stratified_stats.csv")
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================
elif page == "🔗 Correlation Analysis":
    st.markdown('<div class="sub-header">Correlation Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Statistical correlations between pregame odds, first TD, opening possession, and wins.
    
    This includes both simple (bivariate) correlations and partial correlations that control for confounding variables.
    
    *For comprehensive controlled analysis, see the "Controlled Analysis (Marginal Effects)" page.*
    """)
    
    display_image("visualizations/controlled_first_td_analysis.png", "Correlation Analysis")
    
    st.markdown("---")
    st.markdown("### 📊 Correlation Matrix")
    
    corr_data = {
        "": ["Pregame Prob", "First TD", "Got Ball First", "Won"],
        "Pregame Prob": [1.000, 0.206, -0.039, 0.405],
        "First TD": [0.206, 1.000, 0.123, 0.363],
        "Got Ball First": [-0.039, 0.123, 1.000, -0.043],
        "Won": [0.405, 0.363, -0.043, 1.000]
    }
    
    st.dataframe(pd.DataFrame(corr_data), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Interpretation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **Strongest Correlations:**
        - Pregame → Win: **0.405** (Vegas knows!)
        - First TD → Win: **0.363** (powerful predictor)
        - Pregame → First TD: **0.206** (better teams score first more)
        """)
    
    with col2:
        st.info("""
        **Key Insight:**
        First TD correlation with winning **(0.363)** is higher than 
        pregame odds correlation with first TD **(0.206)**.
        
        This means **first TD provides NEW information** beyond 
        just pregame expectations!
        """)

# ============================================================================
# LOGISTIC REGRESSION
# ============================================================================
elif page == "📊 Logistic Regression":
    st.markdown('<div class="sub-header">Logistic Regression Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Logistic regression models controlling for pregame odds and opening possession to isolate the
    independent effect of scoring the first touchdown.
    
    **Basic Model:** `P(Win) = logit⁻¹(β₀ + β₁·pregame_prob + β₂·scored_first_td)`
    
    **Controlled Model:** `P(Win) = logit⁻¹(β₀ + β₁·pregame_prob + β₂·scored_first_td + β₃·got_ball_first)`
    
    *For detailed analysis, see the "Controlled Analysis (Marginal Effects)" page.*
    """)
    
    display_image("visualizations/controlled_first_td_analysis.png", "Logistic Regression Results")
    
    st.markdown("---")
    st.markdown("### 📈 Model Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Coefficient", "1.4051", help="For scored_first_td variable")
    
    with col2:
        st.metric("Odds Ratio", "4.08x", help="Multiplier on odds of winning")
    
    with col3:
        st.metric("50-50 Team Impact", "+30.3pp", help="Win probability change")
    
    st.markdown("---")
    
    st.success("""
    ### 🎯 Main Finding
    
    **Controlling for pregame odds, scoring the first TD multiplies a team's odds of winning by 4.08x**
    
    This represents a **308% increase in odds**, independent of pregame team strength!
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Tier-Specific Odds Ratios")
    
    if os.path.exists("results/analysis/logistic_regression_results.csv"):
        lr_df = pd.read_csv("results/analysis/logistic_regression_results.csv")
        st.dataframe(lr_df, use_container_width=True)
    
    st.markdown("---")
    st.warning("""
    ### 💡 Trading Implication
    
    The ~30 percentage point shift is **remarkably consistent** across all pregame odds tiers.
    This suggests that markets which don't fully adjust for first TD (e.g., only adjusting by 20pp)
    present **systematic arbitrage opportunities** worth ~10 percentage points.
    """)

# ============================================================================
# CONTROLLED ANALYSIS (MARGINAL EFFECTS)
# ============================================================================
elif page == "🎯 Controlled Analysis (Marginal Effects)":
    st.markdown('<div class="sub-header">Controlled First TD Analysis with Marginal Effects</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This is the **most rigorous analysis**, controlling for both pregame odds AND opening possession
    to isolate the pure causal effect of scoring the first touchdown.
    
    **Model:** `P(Win) = logit⁻¹(β₀ + β₁·pregame_prob + β₂·scored_first_td + β₃·got_ball_first)`
    """)
    
    # Correlation results
    display_image("visualizations/controlled_first_td_analysis.png", "Controlled Analysis Results")
    
    st.markdown("---")
    st.markdown("### 📊 Key Correlation Findings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Simple Correlation", 
            "r = 0.364", 
            help="First TD → Win (no controls)"
        )
    
    with col2:
        st.metric(
            "Partial Correlation (Pregame)", 
            "r = 0.313", 
            help="First TD → Win (controlling for pregame odds only)"
        )
    
    with col3:
        st.metric(
            "Partial Correlation (Full)", 
            "r = 0.320", 
            "+0.007",
            help="First TD → Win (controlling for pregame odds + opening possession)"
        )
    
    st.success("""
    ### ✅ Key Finding: Effect is ROBUST
    
    The first TD effect is **stable** when controlling for opening possession (+0.007 change).
    This means opening possession does NOT confound the first TD impact!
    """)
    
    st.markdown("---")
    st.markdown("### 📈 Marginal Effects: Percentage Points Added")
    
    st.markdown("""
    The analysis calculates the **actual percentage point** increase in win probability 
    from scoring the first TD at different pregame odds levels.
    """)
    
    display_image("visualizations/first_td_marginal_effects.png", "First TD Marginal Effects by Pregame Odds")
    
    st.markdown("---")
    st.markdown("### 🎯 Percentage Point Impact by Pregame Odds")
    
    if os.path.exists("results/analysis/first_td_marginal_effects.csv"):
        me_df = pd.read_csv("results/analysis/first_td_marginal_effects.csv")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Effect", f"{me_df['avg_effect'].mean():.1f}pp", help="Across all pregame odds")
        
        with col2:
            effect_20 = me_df[me_df['pregame_prob'] == 0.20]['avg_effect'].values[0]
            st.metric("20% Pregame Odds", f"+{effect_20:.1f}pp", help="Underdog team")
        
        with col3:
            effect_50 = me_df[me_df['pregame_prob'] == 0.50]['avg_effect'].values[0]
            st.metric("50% Pregame Odds", f"+{effect_50:.1f}pp", help="Even matchup")
        
        with col4:
            effect_80 = me_df[me_df['pregame_prob'] == 0.80]['avg_effect'].values[0]
            st.metric("80% Pregame Odds", f"+{effect_80:.1f}pp", help="Favorite team")
        
        st.markdown("---")
        st.markdown("### 📊 Detailed Marginal Effects Table")
        
        # Format the dataframe for display
        display_df = me_df.copy()
        display_df['pregame_prob'] = (display_df['pregame_prob'] * 100).astype(int).astype(str) + '%'
        display_df['effect_got_ball'] = display_df['effect_got_ball'].apply(lambda x: f"+{x:.1f}pp")
        display_df['effect_no_ball'] = display_df['effect_no_ball'].apply(lambda x: f"+{x:.1f}pp")
        display_df['avg_effect'] = display_df['avg_effect'].apply(lambda x: f"+{x:.1f}pp")
        
        display_df.columns = ['Pregame Win Prob', 'Got Ball First', 'Did NOT Get Ball', 'Average Effect']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.info("""
    ### 📊 Key Insights
    
    1. **Peak Effect at 50% Pregame Odds:** The first TD has the largest impact (~35pp) for even matchups
    
    2. **Non-Linear Effect:** The impact varies across pregame odds levels, with diminishing returns for heavy favorites/underdogs
    
    3. **Opening Possession Matters:** Teams that got the ball first see slightly different effects, but the overall pattern holds
    
    4. **Average Impact: ~30pp:** Across all scenarios, scoring the first TD adds about 30 percentage points to win probability
    """)
    
    st.markdown("---")
    st.warning("""
    ### 💡 Trading Implication
    
    **This is the CLEANEST estimate for market pricing!**
    
    - The ~30pp average effect represents the pure causal impact after controlling for all confounds
    - Effect varies by pregame odds (25-35pp range)
    - Markets should adjust by at least this amount when the first TD is scored
    - Any market that adjusts by less presents an arbitrage opportunity
    """)

# ============================================================================
# DATA EXPLORER
# ============================================================================
elif page == "📋 Data Explorer":
    st.markdown('<div class="sub-header">Data Explorer</div>', unsafe_allow_html=True)
    
    if df is not None:
        st.markdown(f"### 📊 Unified Dataset ({len(df)} games)")
        
        # Filters
        st.markdown("#### Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            seasons = st.multiselect(
                "Select Seasons",
                options=sorted(df['season'].unique()),
                default=sorted(df['season'].unique())
            )
        
        with col2:
            teams = st.multiselect(
                "Select Teams (Home or Away)",
                options=sorted(df['home_team'].unique()),
                default=[]
            )
        
        with col3:
            first_td_filter = st.radio(
                "First TD Status",
                ["All Games", "Team Scored First", "Team Did Not Score First"]
            )
        
        # Apply filters
        filtered_df = df[df['season'].isin(seasons)]
        
        if teams:
            filtered_df = filtered_df[
                (filtered_df['home_team'].isin(teams)) | 
                (filtered_df['away_team'].isin(teams))
            ]
        
        if first_td_filter == "Team Scored First":
            filtered_df = filtered_df[filtered_df['first_td_team_won'] == 1]
        elif first_td_filter == "Team Did Not Score First":
            filtered_df = filtered_df[filtered_df['first_td_team_won'] == 0]
        
        st.markdown(f"**Showing {len(filtered_df)} games**")
        
        # Display data
        display_columns = [
            'game_id', 'season', 'home_team', 'away_team', 
            'first_td_team', 'winner', 'home_prob', 'away_prob',
            'opening_possession_team', 'first_td_team_won'
        ]
        
        st.dataframe(
            filtered_df[display_columns].head(100),
            use_container_width=True,
            hide_index=True
        )
        
        # Summary statistics
        st.markdown("---")
        st.markdown("### 📊 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            first_td_rate = filtered_df['first_td_team_won'].mean() * 100
            st.metric("First TD Team Win Rate", f"{first_td_rate:.1f}%")
        
        with col2:
            fav_rate = filtered_df['favorite_won'].mean() * 100
            st.metric("Favorite Win Rate", f"{fav_rate:.1f}%")
        
        with col3:
            opening_td_rate = filtered_df['opening_possession_scored_first'].mean() * 100
            st.metric("Opening Poss → First TD", f"{opening_td_rate:.1f}%")
        
        with col4:
            opening_win_rate = filtered_df['opening_possession_won'].mean() * 100
            st.metric("Opening Poss → Win", f"{opening_win_rate:.1f}%")
        
        # Download button
        st.markdown("---")
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name="nfl_filtered_data.csv",
            mime="text/csv"
        )
    
    else:
        st.error("❌ Unable to load data. Make sure nfl_unified_data.csv exists in the project directory.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>NFL First Touchdown Analysis Dashboard | Data: 2020-2024 Regular Season | 1,334 Games</p>
    <p>Built with Streamlit | Run: <code>streamlit run dashboard.py</code></p>
</div>
""", unsafe_allow_html=True)

