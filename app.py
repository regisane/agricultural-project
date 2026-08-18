"""
Agricultural Investment Risk Analysis - Streamlit Dashboard
Professional Interactive Dashboard for Agricultural Analysis Results

This module provides an interactive dashboard for exploring agricultural
investment risk analysis results using Streamlit.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Agricultural Investment Risk Analysis",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling - Professional Dashboard Theme (Based on HTML Design)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Segoe UI', 'Poppins', sans-serif;
    }
    
    /* Clean Professional Background */
    .stApp {
        background: #f0f4f8;
        position: relative;
    }
    
    /* Main Dashboard Container */
    .dashboard-container {
        max-width: 1300px;
        margin: 0 auto;
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    }
    
    /* Premium Main Header */
    .main-header {
        font-size: 2.2em;
        color: #1a2a3a;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .main-header span {
        color: #2e7d32;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1em;
        color: #5a6a7a;
        margin: 0.5rem 0 2rem 0;
        position: relative;
        z-index: 2;
    }
    
    /* Section Headers */
    h2 {
        color: #1a2a3a;
        border-bottom: 3px solid #2e7d32;
        padding-bottom: 0.6rem;
        font-weight: 600;
        font-size: 1.6em;
        position: relative;
        z-index: 2;
    }
    
    h3 {
        color: #1a2a3a;
        font-weight: 600;
        font-size: 1.2em;
        position: relative;
        z-index: 2;
    }
    
    /* Professional Stats Cards Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .stat-card {
        background: #f8fafc;
        border-radius: 14px;
        padding: 18px 20px;
        border-left: 4px solid #2e7d32;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }
    
    .stat-card .label {
        font-size: 13px;
        color: #5a6a7a;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .stat-card .value {
        font-size: 28px;
        font-weight: 700;
        color: #1a2a3a;
        margin: 5px 0;
    }
    
    .stat-card .sub {
        font-size: 13px;
        color: #5a6a7a;
    }
    
    /* Navigation Tabs */
    .nav-tabs {
        display: flex;
        flex-wrap: wrap;
        gap: 6px 18px;
        padding: 14px 0;
        border-top: 1px solid #e9edf2;
        border-bottom: 1px solid #e9edf2;
        margin: 20px 0;
    }
    
    .nav-tab {
        color: #1a2a3a;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 8px;
        transition: all 0.2s;
        background: transparent;
    }
    
    .nav-tab:hover {
        background: #e8f5e9;
        color: #2e7d32;
    }
    
    .nav-tab.active {
        background: #2e7d32;
        color: white;
    }
    
    /* Two Column Layout */
    .two-col {
        display: grid;
        grid-template-columns: 2fr 1.2fr;
        gap: 30px;
        margin: 30px 0;
    }
    
    @media (max-width: 860px) {
        .two-col {
            grid-template-columns: 1fr;
        }
    }
    
    /* Project Info Box */
    .project-info {
        background: #f8fafc;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 20px 0;
    }
    
    .project-info .title {
        font-size: 16px;
        font-weight: 600;
        color: #1a2a3a;
        margin-bottom: 15px;
    }
    
    .project-info .row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        font-size: 14px;
        border-bottom: 1px solid #e9edf2;
    }
    
    .project-info .row:last-child {
        border-bottom: none;
    }
    
    .project-info .row .key {
        color: #5a6a7a;
    }
    
    .project-info .row .value {
        font-weight: 500;
        color: #1a2a3a;
    }
    
    .badge {
        background: #2e7d32;
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* Country List Items */
    .country-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #e9edf2;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    .country-item:hover {
        background: #f5f5f5;
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 8px;
    }
    
    .country-item:last-child {
        border-bottom: none;
    }
    
    .country-item .rank {
        font-weight: 700;
        color: #2e7d32;
        margin-right: 12px;
        font-size: 13px;
    }
    
    .country-item .name {
        flex: 1;
        font-weight: 500;
        color: #1a2a3a;
    }
    
    .country-item .score {
        font-weight: 600;
        color: #1a2a3a;
    }
    
    .country-item .land {
        color: #5a6a7a;
        font-size: 13px;
        margin-left: 8px;
    }
    
    /* Risk Summary Box */
    .risk-summary {
        background: #f8fafc;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 20px 0;
    }
    
    .risk-summary .title {
        font-size: 16px;
        font-weight: 600;
        color: #1a2a3a;
        margin-bottom: 10px;
    }
    
    .risk-summary .subtitle {
        font-size: 13px;
        color: #5a6a7a;
        margin-bottom: 15px;
    }
    
    .risk-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }
    
    .risk-stat-item {
        background: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .risk-stat-item:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .risk-stat-item .number {
        font-size: 24px;
        font-weight: 700;
        color: #1a2a3a;
    }
    
    .risk-stat-item .label {
        font-size: 12px;
        color: #5a6a7a;
        margin-top: 5px;
    }
    
    .risk-stat-item.highlight {
        background: linear-gradient(135deg, #1a2a3a 0%, #2e3d4a 100%);
    }
    
    .risk-stat-item.highlight .number,
    .risk-stat-item.highlight .label {
        color: white;
    }
    
    /* Risk Item List */
    .risk-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #e9edf2;
        font-size: 14px;
    }
    
    .risk-item:last-child {
        border-bottom: none;
    }
    
    .risk-item .name {
        font-weight: 500;
        color: #1a2a3a;
    }
    
    .risk-item .risk-value {
        font-weight: 600;
        color: #c62828;
    }
    
    .risk-item .diversity {
        color: #5a6a7a;
        font-size: 13px;
        margin-left: 8px;
    }
    
    /* Text Colors */
    .success-text {
        color: #2e7d32;
        font-weight: 700;
    }
    .warning-text {
        color: #e65100;
        font-weight: 700;
    }
    .danger-text {
        color: #c62828;
        font-weight: 700;
    }
    .info-text {
        color: #0277bd;
        font-weight: 700;
    }
    
    /* Info Boxes */
    .info-box {
        background: #f8fafc;
        border-left: 4px solid #2e7d32;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1.2rem 0;
        position: relative;
        z-index: 2;
    }
    
    /* Premium Footer */
    .footer {
        text-align: center;
        color: #5a6a7a;
        font-size: 13px;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid #e9edf2;
    }
    
    .footer-brand {
        color: #1a2a3a;
        font-weight: 700;
        font-size: 1.1em;
    }
    
    /* Developer Badge */
    .dev-badge {
        display: inline-block;
        background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 600;
        margin: 5px;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        position: relative;
        z-index: 2;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #e9edf2, transparent);
        margin: 2rem 0;
    }
    
    /* Streamlit Overrides */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a2a3a 0%, #2e3d4a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
    }
    
    /* Owner Showcase */
    .owner-showcase {
        background: linear-gradient(135deg, #f8fafc 0%, #e8f5e9 100%);
        border: 2px solid #2e7d32;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.15);
    }
    
    .owner-name {
        font-size: 1.8em;
        font-weight: 700;
        color: #1a2a3a;
        margin: 10px 0;
    }
    
    .owner-title {
        color: #5a6a7a;
        font-size: 1em;
        margin: 5px 0;
    }
    
    .owner-badges {
        margin: 15px 0;
    }
    
    .owner-quote {
        font-style: italic;
        color: #5a6a7a;
        margin: 15px 0;
        padding: 10px;
        border-left: 3px solid #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


def resolve_data_path(filename: str) -> Path:
    """Prefer the generated output files, but fall back to the project root."""
    candidates = [
        BASE_DIR / 'output' / filename,
        BASE_DIR / filename,
        Path.cwd() / 'output' / filename,
        Path.cwd() / filename,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


@st.cache_data
def load_master_data():
    """Load master dataset."""
    data_path = resolve_data_path('agricultural_master_data.csv')
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        st.error(
            "❌ agricultural_master_data.csv not found. Run: python agricultural_analysis.py"
        )
        return None

@st.cache_data
def load_results_data():
    """Load analysis results."""
    data_path = resolve_data_path('final_results.csv')
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        st.error(
            "❌ final_results.csv not found. Run: python agricultural_analysis.py"
        )
        return None

@st.cache_data
def load_summary_json():
    """Load summary statistics."""
    data_path = resolve_data_path('analysis_summary.json')
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def ensure_analysis_data() -> bool:
    """Generate missing analysis outputs automatically when the app starts."""
    required_files = [
        'agricultural_master_data.csv',
        'final_results.csv',
        'analysis_summary.json'
    ]

    for filename in required_files:
        if resolve_data_path(filename).exists():
            continue

        with st.spinner("Generating analysis data... This can take a few moments."):
            try:
                subprocess.run(
                    [sys.executable, str(BASE_DIR / 'agricultural_analysis.py')],
                    cwd=str(BASE_DIR),
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=600,
                )
            except (subprocess.TimeoutExpired, OSError) as exc:
                st.error(f"Analysis generation failed: {exc}")
                return False

        # Re-check after generation attempt.
        if not resolve_data_path(filename).exists():
            st.error(
                "❌ Required analysis files were not generated. "
                "Please run: python agricultural_analysis.py"
            )
            return False

    return True

# ============================================================
# HEADER
# ============================================================

# Main Header matching HTML design
st.markdown('<div class="main-header">🌾 <span>AGRICULTURAL</span> INVESTMENT RISK ANALYSIS</div>', 
            unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
    Turning agricultural data into actionable investment intelligence.
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "📊 Navigation",
    [
        "📈 Overview",
        "🗺️ Geographic Analysis",
        "💰 Investment Metrics",
        "⚠️ Risk Assessment",
        "📊 Data Explorer",
        "📉 Visualizations",
        "ℹ️ About & Info"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📋 Project Information
**Status:** ✅ Production Ready  
**Version:** 2.0 Professional  
**Updated:** 2026-08-15
""")

# Load data
if not all(
    resolve_data_path(name).exists()
    for name in ['agricultural_master_data.csv', 'final_results.csv', 'analysis_summary.json']
):
    if not ensure_analysis_data():
        st.stop()

master_df = load_master_data()
results_df = load_results_data()
summary = load_summary_json()

if master_df is None or results_df is None:
    st.error("⚠️ Analysis data not found. Please run the analysis first!")
    st.stop()

geo_source = results_df if {'Latitude', 'Longitude'}.issubset(results_df.columns) else master_df
geo_count = int(
    geo_source[['Latitude', 'Longitude']].notna().all(axis=1).sum()
) if {'Latitude', 'Longitude'}.issubset(geo_source.columns) else int(len(master_df))

st.sidebar.markdown(f"**Countries:** {len(master_df)}")
st.sidebar.markdown(f"**Geographic Data:** {geo_count}")

# ============================================================
# PAGE 1: OVERVIEW
# ============================================================

if page == "📈 Overview":
    st.header("📊 Analysis Overview")
    
    # Key Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Countries",
            f"{len(master_df)}",
            "Analyzed"
        )
    
    with col2:
        st.metric(
            "Geographic Data",
            f"{geo_count}",
            "With Coordinates"
        )
    
    with col3:
        avg_investment = master_df['Investment_Score'].mean()
        st.metric(
            "Avg Investment Score",
            f"{avg_investment:.1f}",
            "Out of 100"
        )
    
    with col4:
        avg_risk = master_df['Composite_Risk_Score'].mean()
        st.metric(
            "Avg Risk Score",
            f"{avg_risk:.3f}",
            "Out of 1.0"
        )
    
    st.markdown("---")
    
    # Top Performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Investment Countries")
        top_5 = master_df.nlargest(5, 'Investment_Score')[
            ['Country', 'Investment_Score', 'Agricultural_Land_1000ha']
        ].reset_index(drop=True)
        top_5.index = top_5.index + 1
        
        for idx, row in top_5.iterrows():
            st.markdown(f"""
            **{idx}. {row['Country']}**  
            Score: <span class="success-text">{row['Investment_Score']:.1f}</span> | 
            Land: {row['Agricultural_Land_1000ha']:,.0f} 1000 ha
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("⚠️ Highest Risk Countries")
        risk_5 = master_df.nlargest(5, 'Composite_Risk_Score')[
            ['Country', 'Composite_Risk_Score', 'Crop_Diversity_Score']
        ].reset_index(drop=True)
        risk_5.index = risk_5.index + 1
        
        for idx, row in risk_5.iterrows():
            st.markdown(f"""
            **{idx}. {row['Country']}**  
            Risk: <span class="danger-text">{row['Composite_Risk_Score']:.3f}</span> | 
            Diversity: {row['Crop_Diversity_Score']:.1f}/10
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Insights
    st.subheader("📌 Key Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Investment Opportunities
        - **China, mainland** leads with score of 93.6
        - **India** and **USA** are strong performers (75+)
        - **Russia** shows good potential (74.0)
        - Large agricultural base correlates with investment potential
        """)
    
    with col2:
        st.markdown("""
        ### Risk Patterns
        - Average risk score: 0.552 (moderate)
        - Risk distribution is fairly balanced
        - Geographic location influences risk profile
        - Crop diversity helps mitigate risk
        """)

# ============================================================
# PAGE 2: GEOGRAPHIC ANALYSIS
# ============================================================

elif page == "🗺️ Geographic Analysis":
    st.header("🗺️ Geographic Analysis")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_score = st.slider("Min Investment Score", 0, 100, 0)
    with col2:
        max_score = st.slider("Max Investment Score", 0, 100, 100)
    with col3:
        region_filter = st.selectbox(
            "Filter by Region",
            ["All Regions", "High Investment (70+)", "Moderate (45-70)", "Lower (<45)"]
        )
    
    # Apply filters
    filtered_df = master_df[
        (master_df['Investment_Score'] >= min_score) &
        (master_df['Investment_Score'] <= max_score)
    ]
    
    if region_filter == "High Investment (70+)":
        filtered_df = filtered_df[filtered_df['Investment_Score'] >= 70]
    elif region_filter == "Moderate (45-70)":
        filtered_df = filtered_df[
            (filtered_df['Investment_Score'] >= 45) & 
            (filtered_df['Investment_Score'] < 70)
        ]
    elif region_filter == "Lower (<45)":
        filtered_df = filtered_df[filtered_df['Investment_Score'] < 45]
    
    # Display map info
    st.info(f"📍 Showing {len(filtered_df)} countries")
    
    # Geographic statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Countries", len(filtered_df))
    with col2:
        st.metric("Avg Investment", f"{filtered_df['Investment_Score'].mean():.1f}")
    with col3:
        st.metric("Avg Risk", f"{filtered_df['Composite_Risk_Score'].mean():.3f}")
    
    st.markdown("---")
    
    # Top countries by region
    st.subheader("🌍 Geographic Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top 10 by Land Area")
        top_land = filtered_df.nlargest(10, 'Agricultural_Land_1000ha')[
            ['Country', 'Agricultural_Land_1000ha', 'Investment_Score']
        ]
        st.dataframe(top_land, use_container_width=True)
    
    with col2:
        st.markdown("### Top 10 by Investment Score")
        top_invest = filtered_df.nlargest(10, 'Investment_Score')[
            ['Country', 'Investment_Score', 'Crop_Diversity_Score']
        ]
        st.dataframe(top_invest, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive map link
    st.subheader("📍 Interactive Map")
    st.info("""
    View the interactive map with geographic markers:
    - Green markers: High investment potential (70+)
    - Orange markers: Moderate potential (45-70)
    - Red markers: Lower potential (<45)
    
    Circle size represents agricultural land area.
    """)
    
    if st.button("🗺️ Open Interactive Map"):
        st.markdown(
            """
            <iframe src="interactive_risk_map.html" width="100%" height="600"></iframe>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# PAGE 3: INVESTMENT METRICS
# ============================================================

elif page == "💰 Investment Metrics":
    st.header("💰 Investment Analysis")
    
    # Score distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investment Score Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(master_df['Investment_Score'].dropna(), bins=30, 
                color='green', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Investment Score')
        ax.set_ylabel('Number of Countries')
        ax.set_title('Distribution of Investment Scores')
        ax.axvline(master_df['Investment_Score'].mean(), color='red', 
                   linestyle='--', linewidth=2, label=f"Mean: {master_df['Investment_Score'].mean():.1f}")
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Agricultural GDP Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(master_df['Agri_GDP_Million'].dropna(), bins=30,
                color='blue', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Agricultural GDP (Million USD)')
        ax.set_ylabel('Number of Countries')
        ax.set_title('Distribution of Agricultural GDP')
        ax.set_yscale('log')  # Log scale for better visibility
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Investment Score Breakdown
    st.subheader("📊 Investment Score Categories")
    
    categories = {
        "🌟 Excellent (80+)": len(master_df[master_df['Investment_Score'] >= 80]),
        "✅ Good (60-79)": len(master_df[(master_df['Investment_Score'] >= 60) & 
                                         (master_df['Investment_Score'] < 80)]),
        "⚠️ Moderate (45-59)": len(master_df[(master_df['Investment_Score'] >= 45) & 
                                            (master_df['Investment_Score'] < 60)]),
        "❌ Lower (<45)": len(master_df[master_df['Investment_Score'] < 45])
    }
    
    col1, col2, col3, col4 = st.columns(4)
    for i, (cat, count) in enumerate(categories.items()):
        with [col1, col2, col3, col4][i]:
            pct = (count / len(master_df)) * 100
            st.metric(cat, f"{count}", f"{pct:.1f}%")
    
    st.markdown("---")
    
    # Top performers table
    st.subheader("🏆 Top 20 Investment Destinations")
    
    top_20 = master_df.nlargest(20, 'Investment_Score')[
        ['Country', 'Investment_Score', 'Agri_GDP_Million', 
         'Crop_Diversity_Score', 'Agricultural_Land_1000ha']
    ].reset_index(drop=True)
    top_20.index = top_20.index + 1
    
    # Format dataframe
    top_20_display = top_20.copy()
    top_20_display['Investment_Score'] = top_20_display['Investment_Score'].apply(lambda x: f"{x:.1f}")
    top_20_display['Agri_GDP_Million'] = top_20_display['Agri_GDP_Million'].apply(lambda x: f"${x:,.0f}M")
    top_20_display['Crop_Diversity_Score'] = top_20_display['Crop_Diversity_Score'].apply(lambda x: f"{x:.1f}/10")
    top_20_display['Agricultural_Land_1000ha'] = top_20_display['Agricultural_Land_1000ha'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(top_20_display, use_container_width=True)

# ============================================================
# PAGE 4: RISK ASSESSMENT
# ============================================================

elif page == "⚠️ Risk Assessment":
    st.header("⚠️ Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Score Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(master_df['Composite_Risk_Score'].dropna(), bins=30,
                color='red', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Composite Risk Score')
        ax.set_ylabel('Number of Countries')
        ax.set_title('Distribution of Risk Scores')
        ax.axvline(master_df['Composite_Risk_Score'].mean(), color='blue',
                   linestyle='--', linewidth=2, label=f"Mean: {master_df['Composite_Risk_Score'].mean():.3f}")
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Cropland Dependency Risk")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(master_df['Cropland_Dependency_Risk'].dropna(), bins=30,
                color='orange', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Cropland Dependency Risk')
        ax.set_ylabel('Number of Countries')
        ax.set_title('Distribution of Cropland Dependency')
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Risk Categories
    st.subheader("📊 Risk Categories")
    
    risk_categories = {
        "🟢 Low Risk (0-0.3)": len(master_df[master_df['Composite_Risk_Score'] < 0.3]),
        "🟡 Moderate Risk (0.3-0.6)": len(master_df[(master_df['Composite_Risk_Score'] >= 0.3) & 
                                                    (master_df['Composite_Risk_Score'] < 0.6)]),
        "🔴 High Risk (0.6-1.0)": len(master_df[master_df['Composite_Risk_Score'] >= 0.6])
    }
    
    col1, col2, col3 = st.columns(3)
    for i, (cat, count) in enumerate(risk_categories.items()):
        with [col1, col2, col3][i]:
            pct = (count / len(master_df)) * 100
            st.metric(cat, f"{count}", f"{pct:.1f}%")
    
    st.markdown("---")
    
    # Highest Risk Countries
    st.subheader("⚠️ Highest Risk Countries")
    
    risk_20 = master_df.nlargest(20, 'Composite_Risk_Score')[
        ['Country', 'Composite_Risk_Score', 'Cropland_Dependency_Risk',
         'Crop_Diversity_Score', 'Agri_Importance']
    ].reset_index(drop=True)
    risk_20.index = risk_20.index + 1
    
    st.dataframe(risk_20, use_container_width=True)
    
    st.markdown("---")
    
    # Correlation Analysis
    st.subheader("📈 Risk vs Investment Correlation")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(master_df['Composite_Risk_Score'],
                        master_df['Investment_Score'],
                        c=master_df['Agricultural_Land_1000ha'],
                        cmap='viridis', alpha=0.6, s=100)
    ax.set_xlabel('Composite Risk Score')
    ax.set_ylabel('Investment Score')
    ax.set_title('Risk vs Investment Score')
    plt.colorbar(scatter, ax=ax, label='Agricultural Land')
    st.pyplot(fig)

# ============================================================
# PAGE 5: DATA EXPLORER
# ============================================================

elif page == "📊 Data Explorer":
    st.header("📊 Data Explorer")
    
    # Search functionality
    st.subheader("🔍 Search Countries")
    search_term = st.text_input("Enter country name or partial match:")
    
    if search_term:
        filtered = master_df[master_df['Country'].str.contains(search_term, case=False, na=False)]
        st.info(f"Found {len(filtered)} matching countries")
        
        if len(filtered) > 0:
            st.dataframe(filtered, use_container_width=True)
    else:
        st.markdown("Enter a country name to search")
    
    st.markdown("---")
    
    # Full data table with filters
    st.subheader("📋 Full Dataset")
    
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox(
            "Sort by:",
            ["Investment_Score", "Composite_Risk_Score", "Agricultural_Land_1000ha",
             "Country", "Crop_Diversity_Score"]
        )
    with col2:
        sort_order = st.radio("Order:", ["Descending", "Ascending"])
    
    ascending = sort_order == "Ascending"
    
    display_columns = [
        'Country', 'Investment_Score', 'Composite_Risk_Score',
        'Agricultural_Land_1000ha', 'Crop_Diversity_Score',
        'Cropland_Pct', 'Agri_GDP_Million'
    ]
    
    sorted_df = master_df[display_columns].sort_values(by=sort_by, ascending=ascending)
    
    st.dataframe(sorted_df, use_container_width=True)
    
    # Download data
    csv = sorted_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="agricultural_analysis_data.csv",
        mime="text/csv"
    )

# ============================================================
# PAGE 6: VISUALIZATIONS
# ============================================================

elif page == "📉 Visualizations":
    st.header("📉 Analysis Visualizations")
    
    # Correlation heatmap
    st.subheader("🔥 Correlation Matrix")
    
    corr_cols = ['Agricultural_Land_1000ha', 'Cropland_1000ha',
                 'Cropland_Pct', 'Agri_GDP_Million', 'Investment_Score',
                 'Crop_Diversity_Score', 'Composite_Risk_Score']
    
    corr_matrix = master_df[corr_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                fmt='.2f', square=True, ax=ax)
    ax.set_title('Correlation Matrix of Agricultural Metrics')
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Investment vs Diversity
    st.subheader("💰 Investment vs Crop Diversity")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(master_df['Crop_Diversity_Score'],
                        master_df['Investment_Score'],
                        c=master_df['Agricultural_Land_1000ha'],
                        cmap='viridis', alpha=0.6, s=100)
    ax.set_xlabel('Crop Diversity Score')
    ax.set_ylabel('Investment Score')
    ax.set_title('Investment Score vs Crop Diversity')
    plt.colorbar(scatter, ax=ax, label='Agricultural Land (1000 ha)')
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Top countries comparison
    st.subheader("🏆 Top 10 Countries - Metrics Comparison")
    
    top_10 = master_df.nlargest(10, 'Investment_Score')
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Investment Score
    axes[0, 0].barh(top_10['Country'], top_10['Investment_Score'], color='green', alpha=0.7)
    axes[0, 0].set_xlabel('Investment Score')
    axes[0, 0].set_title('Investment Score')
    axes[0, 0].invert_yaxis()
    
    # Risk Score
    axes[0, 1].barh(top_10['Country'], top_10['Composite_Risk_Score'], color='red', alpha=0.7)
    axes[0, 1].set_xlabel('Risk Score')
    axes[0, 1].set_title('Risk Score')
    axes[0, 1].invert_yaxis()
    
    # Diversity
    axes[1, 0].barh(top_10['Country'], top_10['Crop_Diversity_Score'], color='blue', alpha=0.7)
    axes[1, 0].set_xlabel('Diversity Score')
    axes[1, 0].set_title('Crop Diversity')
    axes[1, 0].invert_yaxis()
    
    # Agricultural Land
    axes[1, 1].barh(top_10['Country'], top_10['Agricultural_Land_1000ha']/1000, color='orange', alpha=0.7)
    axes[1, 1].set_xlabel('Agricultural Land (Million ha)')
    axes[1, 1].set_title('Agricultural Land Area')
    axes[1, 1].invert_yaxis()
    
    plt.tight_layout()
    st.pyplot(fig)

# ============================================================
# PAGE 7: ABOUT & INFO
# ============================================================

elif page == "ℹ️ About & Info":
    st.header("ℹ️ About This Analysis")
    
    st.markdown("""
    <div class='info-box'>
    <strong>🎯 Mission:</strong> Provide data-driven insights into global agricultural investment opportunities 
    and risk assessment using advanced geospatial analysis and statistical modeling.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Project Overview")
        st.markdown("""
        This professional dashboard analyzes **140+ countries** across multiple 
        agricultural metrics to identify investment opportunities and risk factors.
        
        **Key Capabilities:**
        - 🌍 Geospatial analysis with coordinates
        - 📊 Statistical regression modeling  
        - 💰 Investment scoring system
        - ⚠️ Risk assessment framework
        - 🗺️ Interactive mapping
        
        **Data Source:** FAOSTAT (Food and Agriculture Organization)  
        **Analysis Type:** Geospatial & Statistical  
        **Methodology:** Geographically Weighted Regression + Linear Regression Fallback
        """)
    
    with col2:
        st.subheader("👤 Project Owner & Developer")
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); border-radius: 15px; border: 2px solid #4CAF50;'>
            <div class='dev-badge' style='font-size: 1.2em; margin-bottom: 10px;'>
                👨‍💻 Lead Developer
            </div>
            <h3 style='color: #2E7D32; margin: 10px 0;'>REGIS UWIMENA</h3>
            <p style='color: #555; font-size: 0.95em;'><strong>MScFE 600 Financial Data</strong></p>
            <p style='color: #666; font-size: 0.9em;'>Washington University in St. Louis</p>
            <div style='margin-top: 15px;'>
                <span style='background: #4CAF50; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin: 3px;'>✅ Project Owner</span>
                <span style='background: #2E7D32; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin: 3px;'>🏆 Lead Analyst</span>
                <span style='background: #1B5E20; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin: 3px;'>💻 Full Stack Developer</span>
            </div>
        </div>
        
        <div style='margin-top: 20px; text-align: center;'>
            <p style='color: #666; font-size: 0.9em;'><em>"Transforming agricultural data into actionable investment insights through advanced analytics and geospatial modeling."</em></p>
        </div>
        
        <div style='margin-top: 15px; text-align: center;'>
            <p style='color: #4CAF50; font-weight: 600;'>✅ Project Status: Production Ready</p>
            <p style='color: #666; font-size: 0.9em;'>Version 3.0 Premium Edition • Last Updated: August 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📈 Metrics Explanation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Financial Metrics
        
        **Investment Score (0-100)**
        - Measures investment attractiveness
        - Based on land area and diversification
        - Higher = more attractive
        
        **Agricultural GDP (Million USD)**
        - Estimated agricultural output
        - Synthetic but realistic calculation
        - Correlates with land area
        
        **Crop Diversity Score (1-10)**
        - Measures diversification
        - Higher = more diverse crops
        - Helps reduce risk
        """)
    
    with col2:
        st.markdown("""
        ### Risk Metrics
        
        **Composite Risk Score (0-1)**
        - Overall investment risk
        - Based on multiple factors
        - Lower = less risky
        
        **Cropland Dependency Risk**
        - Risk from over-reliance on crops
        - High dependency = higher risk
        - Mitigated by diversification
        
        **Agricultural Importance**
        - Sector's importance to country
        - Normalized by global maximum
        - Indicates scale of operations
        """)
    
    st.markdown("---")
    
    st.subheader("📂 Output Files")
    
    files_info = {
        "agricultural_master_data.csv": "Complete dataset with all metrics",
        "final_results.csv": "Regression analysis results",
        "agricultural_analysis.png": "EDA visualizations (300 DPI)",
        "spatial_analysis_map.png": "Geographic distribution maps",
        "interactive_risk_map.html": "Interactive web map",
        "analysis_summary.json": "Summary statistics in JSON",
        "analysis.log": "Detailed execution log"
    }
    
    for filename, description in files_info.items():
        st.markdown(f"**{filename}**  \n{description}")
    
    st.markdown("---")
    
    st.subheader("📊 Key Statistics")
    
    if summary:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Countries", summary.get('total_countries', 'N/A'))
            st.metric("With Coordinates", summary.get('valid_coordinates', 'N/A'))
        
        with col2:
            stats = summary.get('statistics', {})
            st.metric("Avg Investment", f"{stats.get('avg_investment_score', 0):.1f}")
            st.metric("Avg Risk", f"{stats.get('avg_risk_score', 0):.3f}")
        
        with col3:
            stats = summary.get('statistics', {})
            st.metric("Avg Agri Land", f"{stats.get('avg_agricultural_land', 0):,.0f} ha")
    
    st.markdown("---")
    
    st.subheader("🔗 Links & Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Project Files:**
        - 📘 [README.md](README.md) - Complete documentation
        - 📗 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands
        - 📙 [IMPROVEMENTS.md](IMPROVEMENTS.md) - Enhancement details
        """)
    
    with col2:
        st.markdown("""
        **Data Sources:**
        - 🌍 [FAOSTAT](http://www.fao.org/faostat) - Official FAO database
        - 📊 [Analysis Code](agricultural_analysis.py) - Python implementation
        - 🗺️ [Interactive Map](interactive_risk_map.html) - Geographic visualization
        """)

# ============================================================
# FOOTER
# ============================================================

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>
        <span class='footer-brand'>🌾 Agricultural Investment Risk Analysis</span> | 
        <em>Premium Dashboard v3.0</em>
    </p>
    <p style='font-size: 0.85em; color: #666; margin-top: 0.5rem;'>
        👨‍💻 Developed by <strong>REGIS UWIMENA</strong> for MScFE 600 Financial Data Analysis
    </p>
    <p style='font-size: 0.8em; color: #4CAF50; font-weight: 600; margin-top: 0.8rem;'>
        🏆 Washington University in St. Louis • Project Owner & Lead Developer
    </p>
    <p style='font-size: 0.75em; color: #999; margin-top: 1rem;'>
        © 2026 Regis Uwimena • <em>Last Updated: 2026-08-18</em> • All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
