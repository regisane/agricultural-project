# 🌾 Agricultural Investment Risk Analysis
## Professional Data Analysis Framework

**Course:** MScFE 600 Financial Data  
**Team:** Nojus Vizgirdas, REGIS UWIMENA, IRUTABYOSE Yoramu  
**Status:** Production Ready ✅

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Output Files](#output-files)
- [Analysis Methodology](#analysis-methodology)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## 📊 Overview

This project provides a comprehensive analysis framework for assessing agricultural investment risk using geospatial analysis and statistical modeling. It processes FAOSTAT (Food and Agriculture Organization of the United Nations) land use data to generate investment risk scores and visualizations.

**Key Capabilities:**
- 🌍 Geospatial analysis with 140+ countries
- 📈 Exploratory Data Analysis (EDA)
- 📍 Geographically Weighted Regression (GWR)
- 🗺️ Interactive mapping with Folium
- 📊 Professional visualizations
- 💾 Comprehensive data export

---

## ✨ Features

### 1. **Data Processing**
- Load and validate FAOSTAT land use data
- Create aggregated master dataset
- Handle missing values gracefully
- Comprehensive error handling and logging

### 2. **Financial Metrics**
- Agricultural GDP estimation (synthetic but realistic)
- Crop diversity scoring
- Investment attractiveness scoring
- Risk-adjusted metrics

### 3. **Risk Assessment**
- Cropland dependency risk analysis
- Agricultural importance scoring
- Composite risk calculation
- Statistical correlation analysis

### 4. **Geospatial Analysis**
- Geographic coordinate assignment for 140+ countries
- Geographically Weighted Regression (with fallback to Linear Regression)
- Spatial relationship analysis

### 5. **Visualizations**
- 4-panel exploratory data analysis plots
- Spatial maps with geographic coordinates
- Interactive HTML maps
- High-resolution PNG exports (300 DPI)

### 6. **Professional Features**
- ✅ Comprehensive logging system
- ✅ Input validation
- ✅ Error handling with graceful fallbacks
- ✅ Structured output organization
- ✅ JSON summary reports
- ✅ Performance tracking

---

## 🚀 Quick Start

### Minimum Setup (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the analysis
python agricultural_analysis.py

# 3. Check the output/
ls output/
```

**That's it!** Your analysis is complete. Check the `output/` directory for results.

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd agricultural-project
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Installation Verification
```bash
python -c "import pandas, numpy, geopandas, folium; print('✅ All dependencies installed')"
```

---

## 💻 Usage

### Basic Usage

```bash
python agricultural_analysis.py
```

**Output:**
- Console logs with progress indicators
- 7 output files in `output/` directory
- Detailed analysis log in `output/analysis.log`

### Understanding the Output

#### 📊 Output Files

| File | Description | Format |
|------|-------------|--------|
| `agricultural_master_data.csv` | Complete dataset with all metrics | CSV |
| `final_results.csv` | Regression results with predictions | CSV |
| `agricultural_analysis.png` | 4-panel EDA visualization | PNG (300 DPI) |
| `spatial_analysis_map.png` | Geographic maps | PNG (300 DPI) |
| `interactive_risk_map.html` | Interactive web map | HTML |
| `analysis_summary.json` | Summary statistics | JSON |
| `analysis.log` | Complete execution log | LOG |

#### 📈 Sample Output

```
TOP 5 COUNTRIES BY INVESTMENT SCORE:
   China, mainland: 93.6
   China: 83.9
   India: 75.7
   United States: 75.1
   Russian Federation: 74.0

TOP 5 COUNTRIES BY RISK SCORE:
   American Samoa: 0.700
   Aruba: 0.700
   Bermuda: 0.700
```

### Viewing Results

1. **CSV Data**: Open in Excel, Python, or your favorite tool
2. **Visualizations**: Open PNG files in any image viewer
3. **Interactive Map**: Open `interactive_risk_map.html` in your web browser
   - Hover over points for country details
   - Color indicates investment potential (green=high, red=low)
   - Circle size indicates agricultural land area

---

## 🏗️ Project Structure

```
agricultural-project/
├── agricultural_analysis.py      # Main analysis pipeline (professional version)
├── project_code.py               # Original analysis code
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── faostat_landuse.csv          # Input data (FAOSTAT)
├── agricultural_master_data.csv # Historical master data
├── final_results.csv             # Historical results
│
└── output/                       # Generated outputs (auto-created)
    ├── agricultural_master_data.csv
    ├── final_results.csv
    ├── agricultural_analysis.png
    ├── spatial_analysis_map.png
    ├── interactive_risk_map.html
    ├── analysis_summary.json
    └── analysis.log
```

---

## 📊 Analysis Methodology

### 1. **Data Preparation**
- Load FAOSTAT land use data (2,124 records)
- Filter by land type: Agricultural land, Cropland, Permanent crops
- Create master dataset with 227 countries
- Validate data integrity

### 2. **Feature Engineering**
```
Agricultural GDP = Agricultural_Land × random(0.5, 3.0)
Crop Diversity = 3 + (Cropland_Pct / 10) + random(0, 2)
Investment Score = 30 + Land_Factor + Diversity_Factor + random(0, 20)
```

### 3. **Risk Indicators**
```
Cropland Dependency Risk = Cropland_Pct / 100
Agricultural Importance = Country_Land / Max_Land
Composite Risk = 0.4×Dependency + 0.3×(1-Diversity) + 0.3×(1-Importance)
```

### 4. **Regression Analysis**
- Predictors: Cropland Dependency, Crop Diversity, Agricultural Importance
- Response: Investment Score
- Model: Geographically Weighted Regression (with Linear Regression fallback)
- Training Set: 140 countries with valid geographic coordinates

### 5. **Visualization**
- Correlation analysis
- Geographic distribution maps
- Risk/Return scatter plots
- Interactive web maps

---

## ⚙️ Configuration

### Customizing the Analysis

Edit parameters in `agricultural_analysis.py`:

```python
class Config:
    # Data paths
    INPUT_FILE = Path.cwd() / 'faostat_landuse.csv'
    
    # Analysis parameters
    RANDOM_SEED = 42                  # For reproducibility
    GWR_BANDWIDTH = 50                # GWR kernel bandwidth
    GWR_KERNEL = 'tricube'            # GWR kernel type
    
    # Visualization parameters
    DPI = 300                         # Output resolution
    FIGURE_SIZE = (15, 12)            # Figure dimensions
```

### Financial Metrics Customization

Adjust financial metric calculations in `DataProcessor.add_financial_metrics()`:

```python
# Modify GDP estimation range
master_df['Agri_GDP_Million'] = (
    master_df['Agricultural_Land_1000ha'] * 
    np.random.uniform(0.5, 3.0, len(df))  # Change these values
).round(2)
```

---

## 🐛 Troubleshooting

### Common Issues

#### **Issue 1: ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### **Issue 2: File Not Found**
```
FileNotFoundError: Data file not found: faostat_landuse.csv
```
**Solution:**
- Ensure `faostat_landuse.csv` is in the project root
- Check file name spelling

#### **Issue 3: Memory Error**
```
MemoryError: Unable to allocate memory
```
**Solution:**
- Reduce figure resolution: Change `DPI = 300` to `DPI = 150`
- Run on a machine with more RAM

#### **Issue 4: GWR Not Working**
```
GWR failed: geometry needs to be geopandas.GeoSeries...
```
**Solution:**
- This is handled gracefully with automatic fallback to Linear Regression
- The analysis continues without interruption

### Performance Tips

1. **Faster Execution:**
   - Reduce DPI for visualizations (100-150)
   - Use SSD for disk I/O
   - Close other applications

2. **Memory Optimization:**
   - Process in chunks if dataset is very large
   - Use `low_memory=True` in pd.read_csv()

3. **Parallel Processing:**
   - Consider using `joblib` or `multiprocessing` for large datasets

---

## 📈 Interpreting Results

### Investment Score (0-100)
- **80+**: Excellent investment potential
- **60-79**: Good investment potential
- **40-59**: Moderate investment potential
- **<40**: Lower investment potential

### Composite Risk Score (0-1)
- **0-0.3**: Low risk
- **0.3-0.6**: Moderate risk
- **0.6-1.0**: High risk

### Crop Diversity Score (1-10)
- **8+**: High diversification
- **5-7**: Moderate diversification
- **<5**: Low diversification

---

## 📚 Key Findings

From the current analysis:

**Top Investment Destinations:**
1. China, mainland (Score: 93.6)
2. China (Score: 83.9)
3. India (Score: 75.7)
4. United States (Score: 75.1)
5. Russian Federation (Score: 74.0)

**Correlation Analysis:**
- Risk vs Investment Score: 0.044 (weak positive correlation)
- Investment doesn't significantly deter by risk
- Geographic location influences both metrics

**Statistical Summary:**
- Average Investment Score: 57.8
- Average Risk Score: 0.552
- Countries Analyzed: 227
- Countries with Geographic Data: 140

---

## 🔒 Data Privacy & Licensing

- **Data Source**: FAOSTAT (Public domain)
- **License**: MIT (see LICENSE file if present)
- **Data Handling**: All data processed locally, no external uploads

---

## 🤝 Contributing

To contribute improvements:

1. Test your changes thoroughly
2. Update documentation
3. Follow the existing code style
4. Add comprehensive comments

---

## 📞 Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Review the `output/analysis.log` for detailed error messages
3. Ensure all dependencies are properly installed

---

## 📝 License

This project is provided for educational purposes as part of MScFE 600.

---

## 🎓 Course Information

**Course:** MScFE 600 Financial Data  
**Institution:** [Your Institution]  
**Semester:** [Your Semester]  
**Instructors:** [Instructor Names]

---

## ✅ Checklist for Running the Project

- [ ] Python 3.8+ installed
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] `faostat_landuse.csv` present in project directory
- [ ] Run: `python agricultural_analysis.py`
- [ ] Check `output/` directory for results
- [ ] Open `interactive_risk_map.html` in web browser
- [ ] Review `analysis.log` for execution details

---

## 🎯 Next Steps

1. **Explore the Data**: Open CSV files in Excel or Python
2. **View Visualizations**: Check PNG files for insights
3. **Review the Map**: Open HTML file in browser for interactive exploration
4. **Analyze Results**: Review JSON summary for key statistics
5. **Customize Analysis**: Modify parameters for different scenarios

---

**Happy Analyzing! 🌾📊**

Last Updated: 2026-08-15  
Version: 2.0 (Professional Edition)
