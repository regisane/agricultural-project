# 🚀 Streamlit Dashboard Guide

## Agricultural Investment Risk Analysis - Interactive Dashboard

**Status:** ✅ Production Ready  
**Version:** 2.0 Professional Edition  
**Dashboard Version:** Streamlit 1.61.1

---

## 🎯 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Dashboard
```bash
streamlit run app.py
```

### 3️⃣ View in Browser
Dashboard will open automatically at:
- **Local:** http://localhost:8501
- **Network:** http://<your-ip>:8501

---

## 📊 Dashboard Pages

### 📈 Overview
- **Key Statistics:** Total countries, geographic data, average scores
- **Top Performers:** Highest investment opportunities
- **Risk Leaders:** Countries with highest risk
- **Key Insights:** Investment and risk analysis summary

### 🗺️ Geographic Analysis
- **Interactive Filtering:** Filter by investment score range
- **Region Selection:** High/Moderate/Lower categories
- **Geographic Statistics:** Distribution by region
- **Data Tables:** Top countries by land area and investment
- **Interactive Map:** Open full Folium map

### 💰 Investment Metrics
- **Score Distribution:** Histogram of investment scores
- **GDP Analysis:** Agricultural GDP distribution
- **Category Breakdown:** Countries by investment tier
- **Top 20 Table:** Detailed investment ranking
- **Downloadable Data:** Export data as CSV

### ⚠️ Risk Assessment
- **Risk Distribution:** Histogram of risk scores
- **Dependency Analysis:** Cropland dependency risk
- **Risk Categories:** Low/Moderate/High risk breakdown
- **Top Risk Countries:** Ranked by composite risk score
- **Correlation Analysis:** Risk vs Investment scatter plot

### 📊 Data Explorer
- **Search Functionality:** Find countries by name
- **Full Dataset:** Browse complete analysis data
- **Sorting Options:** Sort by any metric
- **Download:** Export filtered data to CSV

### 📉 Visualizations
- **Correlation Heatmap:** Inter-metric relationships
- **Investment vs Diversity:** Scatter plot analysis
- **Top 10 Comparison:** 4-panel metric comparison
- **Professional Charts:** High-quality visualizations

### ℹ️ About & Info
- **Project Overview:** Analysis methodology
- **Team Information:** Project team details
- **Metrics Explanation:** Detailed metric definitions
- **Output Files:** File descriptions and contents
- **Key Statistics:** Summary of analysis results
- **Resources:** Links and data sources

---

## 🎨 Dashboard Features

### ✨ Interactive Elements
- ✅ Sidebar navigation with 7 pages
- ✅ Dynamic filtering and sorting
- ✅ Search functionality
- ✅ Downloadable CSV exports
- ✅ Interactive visualizations
- ✅ Responsive design

### 📊 Visualizations
- ✅ Bar charts and histograms
- ✅ Scatter plots with color mapping
- ✅ Correlation heatmaps
- ✅ Multi-panel comparisons
- ✅ Geographic visualizations
- ✅ High-quality exports (300 DPI)

### 📱 User Experience
- ✅ Clean, professional layout
- ✅ Color-coded metrics (green, orange, red)
- ✅ Intuitive navigation
- ✅ Fast data loading (cached)
- ✅ Responsive to screen size
- ✅ Mobile-friendly

---

## 🔧 Configuration

### Modify Dashboard Settings

Edit `app.py` to customize:

```python
# Change page title
st.set_page_config(
    page_title="Your Title",
    page_icon="🌾",
    layout="wide"
)

# Adjust colors and styling
st.markdown("""
    <style>
    .main-header { color: #your-color; }
    </style>
""", unsafe_allow_html=True)
```

### Data Caching

Dashboard automatically caches data for fast performance:
```python
@st.cache_data
def load_master_data():
    return pd.read_csv('output/agricultural_master_data.csv')
```

---

## 📊 Data Requirements

Dashboard expects the following files in `output/` directory:

```
output/
├── agricultural_master_data.csv    ✅ Required
├── final_results.csv               ✅ Required
├── analysis_summary.json           ✅ Required
├── agricultural_analysis.png       (Optional)
├── spatial_analysis_map.png        (Optional)
├── interactive_risk_map.html       (Optional)
└── analysis.log                    (Optional)
```

**To Generate Data:**
```bash
# Run the main analysis first
python agricultural_analysis.py
```

---

## 🚀 Advanced Usage

### Custom Styling

Add custom CSS to any page:
```python
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)
```

### Performance Optimization

For large datasets, use session state:
```python
if 'master_df' not in st.session_state:
    st.session_state.master_df = load_master_data()
    
df = st.session_state.master_df
```

### Custom Filters

Add filters to any page:
```python
min_score = st.slider("Min Score", 0, 100, 0)
filtered = df[df['Investment_Score'] >= min_score]
```

---

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Clear cache and restart
streamlit run app.py --logger.level=debug

# Or use a different port
streamlit run app.py --server.port 8502
```

### Data not loading
```bash
# Make sure analysis has been run
python agricultural_analysis.py

# Verify output files exist
ls -la output/
```

### Slow performance
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache/

# Restart dashboard
streamlit run app.py --client.caching=true
```

### Memory issues
```bash
# Run with reduced memory footprint
streamlit run app.py --client.maxMessageSize=50
```

---

## 📈 Deployment Options

### Local Machine
```bash
streamlit run app.py
```

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Deploy with one click

### Docker Container
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Run Docker:
```bash
docker build -t ag-dashboard .
docker run -p 8501:8501 ag-dashboard
```

### AWS/Azure/GCP
Use any Python web hosting service:
- AWS EC2 with Streamlit
- Azure App Service
- Google Cloud Run
- DigitalOcean Droplet

---

## 🎯 Use Cases

### For Investors
- Screen investment opportunities
- Compare countries by metrics
- Analyze risk profiles
- Download data for further analysis

### For Researchers
- Explore agricultural patterns
- Study land use distribution
- Analyze crop diversification
- Export data for modeling

### For Policy Makers
- Understand agricultural trends
- Plan development strategies
- Assess regional performance
- Make data-driven decisions

### For Educational Use
- Learn data analysis techniques
- Explore geospatial analysis
- Understand agricultural economics
- Practice Streamlit development

---

## 📊 Metrics Reference

### Investment Score (0-100)
| Range | Category | Recommendation |
|-------|----------|---|
| 80+ | Excellent | Highly recommended |
| 60-79 | Good | Strong opportunity |
| 45-59 | Moderate | Consider with caution |
| <45 | Lower | Lower priority |

### Risk Score (0-1)
| Range | Category | Recommendation |
|-------|----------|---|
| 0-0.3 | Low | Favorable |
| 0.3-0.6 | Moderate | Monitor |
| 0.6-1.0 | High | Higher caution |

### Crop Diversity (1-10)
| Range | Diversification | Benefit |
|-------|---|---|
| 8-10 | High | Good risk mitigation |
| 5-7 | Moderate | Balanced approach |
| 1-4 | Low | Concentrated risk |

---

## 🔗 Related Files

- **agricultural_analysis.py** - Main analysis engine
- **cli.py** - Command-line interface
- **app.py** - Streamlit dashboard (this)
- **requirements.txt** - Dependencies
- **README.md** - Full documentation
- **output/** - Analysis results

---

## 📞 Support

**Issues with Dashboard?**
1. Check [README.md](README.md) for general help
2. Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands
3. Check [IMPROVEMENTS.md](IMPROVEMENTS.md) for technical details
4. Review [analysis.log](output/analysis.log) for errors

**Common Commands:**
```bash
# Run dashboard
streamlit run app.py

# Run with specific port
streamlit run app.py --server.port 8502

# Run in headless mode
streamlit run app.py --logger.level=error

# Clear cache
streamlit cache clear
```

---

## 🎓 Learning Resources

**Streamlit Documentation:**
- 📖 [Official Docs](https://docs.streamlit.io)
- 🎬 [Video Tutorials](https://streamlit.io/gallery)
- 💻 [Community Forum](https://discuss.streamlit.io)

**Data Analysis:**
- 📚 [Pandas Documentation](https://pandas.pydata.org)
- 🔬 [Matplotlib Guide](https://matplotlib.org)
- 🗺️ [Folium Documentation](https://python-visualization.github.io/folium)

---

## ✅ Verification Checklist

- [ ] Streamlit installed (`pip install -r requirements.txt`)
- [ ] Analysis data generated (`python agricultural_analysis.py`)
- [ ] Dashboard starts (`streamlit run app.py`)
- [ ] Browser opens to localhost:8501
- [ ] All pages load without errors
- [ ] Data displays correctly
- [ ] Visualizations render
- [ ] Filters work properly
- [ ] Download functionality works
- [ ] No console errors

---

## 📝 Version History

**v2.0 (Current)**
- ✅ Streamlit dashboard
- ✅ 7-page interface
- ✅ Interactive filtering
- ✅ Professional styling
- ✅ Data export
- ✅ High-performance caching

**v1.0**
- ✅ CLI analysis
- ✅ Python analysis engine
- ✅ Geographic maps
- ✅ Visualizations

---

## 🎉 Summary

The Streamlit dashboard provides a professional, user-friendly interface for exploring agricultural investment risk analysis results. With 7 interactive pages, comprehensive filtering, and beautiful visualizations, it makes data analysis accessible to everyone.

**Status:** ✅ Production Ready  
**Dashboard:** 🌾 Fully Functional  
**Deployment:** 🚀 Ready to Deploy

---

**Happy Analyzing! 🌾📊**

Last Updated: 2026-08-15  
Dashboard Version: v2.0  
Team: Nojus Vizgirdas, REGIS UWIMENA, IRUTABYOSE Yoramu
