
"""
============================================================
M6 GROUP WORK PROJECT: AGRICULTURAL INVESTMENT RISK ANALYSIS
Using FAOSTAT Land Use Data & Geographically Weighted Regression
============================================================
Team: Nojus Vizgirdas, REGIS UWIMENA, IRUTABYOSE Yoramu
Course: MScFE 600 Financial Data
============================================================
"""

# ============================================================
# PART 1: INSTALL REQUIRED PACKAGES (Run this ONCE)
# ============================================================
# In VS Code, open TERMINAL (View → Terminal or Ctrl+`)
# Then type: pip install pandas numpy geopandas matplotlib seaborn
# Then type: pip install gwlearn scikit-learn shapely folium

# ============================================================
# PART 2: IMPORT LIBRARIES
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# For geospatial analysis
import geopandas as gpd
from shapely.geometry import Point
import folium

# For GWR
try:
    from gwlearn.linear_model import GWLinearRegression
    print("✅ GWLearn imported successfully!")
except ImportError:
    print("❌ GWLearn not installed. Run: pip install gwlearn")
    print("⚠️  We'll use standard regression instead.")

print("="*60)
print("📊 AGRICULTURAL INVESTMENT RISK ANALYSIS")
print("="*60)

# ============================================================
# PART 3: LOAD YOUR FAOSTAT DATA
# ============================================================
print("\n📁 Loading FAOSTAT data...")

# Load the CSV file
df = pd.read_csv('faostat_landuse.csv')

print(f"✅ Loaded {len(df)} rows")
print(f"📋 Columns: {list(df.columns)}")
print("\n📊 First 5 rows:")
print(df.head())

# ============================================================
# PART 4: UNDERSTAND THE DATA STRUCTURE
# ============================================================
print("\n" + "="*60)
print("🔍 UNDERSTANDING YOUR DATA")
print("="*60)

# Check unique values in key columns
print("\n📌 Unique Areas (Countries):")
print(df['Area'].unique()[:10])  # Show first 10 countries

print("\n📌 Unique Items (Land Use Types):")
print(df['Item'].unique())

print("\n📌 Unique Elements:")
print(df['Element'].unique())

# ============================================================
# PART 5: FILTER AGRICULTURAL LAND DATA
# ============================================================
print("\n" + "="*60)
print("🌾 FILTERING AGRICULTURAL LAND DATA")
print("="*60)

# Filter for Agricultural Land
agri_df = df[df['Item'] == 'Agricultural land'].copy()
print(f"✅ Found {len(agri_df)} records for Agricultural land")

# Filter for Cropland
crop_df = df[df['Item'] == 'Cropland'].copy()
print(f"✅ Found {len(crop_df)} records for Cropland")

# Filter for Permanent crops
perm_crop_df = df[df['Item'] == 'Permanent crops'].copy()
print(f"✅ Found {len(perm_crop_df)} records for Permanent crops")

# ============================================================
# PART 6: CREATE A COMPREHENSIVE DATASET
# ============================================================
print("\n" + "="*60)
print("📊 CREATING MASTER DATASET")
print("="*60)

# Select key columns
master_df = agri_df[['Area', 'Area Code (M49)', 'Value', 'Unit']].copy()
master_df = master_df.rename(columns={
    'Area': 'Country',
    'Area Code (M49)': 'Country_Code',
    'Value': 'Agricultural_Land_1000ha',
    'Unit': 'Unit'
})

print(f"✅ Master dataset has {len(master_df)} countries")

# Add Cropland data
crop_values = crop_df.set_index('Area Code (M49)')['Value']
master_df['Cropland_1000ha'] = master_df['Country_Code'].map(crop_values)

# Add Permanent crops data
perm_values = perm_crop_df.set_index('Area Code (M49)')['Value']
master_df['Permanent_Crops_1000ha'] = master_df['Country_Code'].map(perm_values)

# Calculate Cropland percentage
master_df['Cropland_Pct'] = (master_df['Cropland_1000ha'] / master_df['Agricultural_Land_1000ha']) * 100

print("\n📊 Master Dataset Preview:")
print(master_df.head())

# Save the master dataset
master_df.to_csv('agricultural_master_data.csv', index=False)
print("\n✅ Saved master dataset to 'agricultural_master_data.csv'")

# ============================================================
# PART 7: ADD FINANCIAL METRICS (Synthetic but Realistic)
# ============================================================
print("\n" + "="*60)
print("💰 ADDING FINANCIAL METRICS")
print("="*60)

# Create realistic financial metrics based on agricultural land
np.random.seed(42)

# 1. Estimated Agricultural GDP (million USD)
# Based on land area - more land = more agricultural output
master_df['Agri_GDP_Million'] = (
    master_df['Agricultural_Land_1000ha'] * 
    np.random.uniform(0.5, 3.0, len(master_df))
).round(2)

# 2. Crop Diversity Score (1-10) - more cropland = more diversity
master_df['Crop_Diversity_Score'] = (
    3 + (master_df['Cropland_Pct'] / 10) + 
    np.random.uniform(0, 2, len(master_df))
).clip(1, 10).round(1)

# 3. Investment Attractiveness Score (1-100)
master_df['Investment_Score'] = (
    30 + 
    (master_df['Agricultural_Land_1000ha'] / master_df['Agricultural_Land_1000ha'].max()) * 30 +
    (master_df['Crop_Diversity_Score'] / 10) * 20 +
    np.random.uniform(0, 20, len(master_df))
).clip(1, 100).round(1)

print("\n📊 Financial Metrics Added:")
print(master_df[['Country', 'Agricultural_Land_1000ha', 'Agri_GDP_Million', 
                 'Crop_Diversity_Score', 'Investment_Score']].head())

# ============================================================
# PART 8: CREATE RISK INDICATORS
# ============================================================
print("\n" + "="*60)
print("⚠️  CREATING RISK INDICATORS")
print("="*60)

# Use the data to create meaningful risk indicators

# 1. Cropland Dependency Risk (too much cropland = less diversification)
master_df['Cropland_Dependency_Risk'] = (master_df['Cropland_Pct'] / 100).round(3)

# 2. Agricultural Importance (high land = high importance)
master_df['Agri_Importance'] = (
    master_df['Agricultural_Land_1000ha'] / master_df['Agricultural_Land_1000ha'].max()
).round(3)

# 3. Composite Risk Score (higher = more risky for investment)
# Risk = high cropland dependency + low diversity
master_df['Composite_Risk_Score'] = (
    master_df['Cropland_Dependency_Risk'] * 0.4 + 
    (1 - master_df['Crop_Diversity_Score']/10) * 0.3 +
    (1 - master_df['Agri_Importance']) * 0.3
).round(3)

print("\n📊 Risk Indicators Added:")
print(master_df[['Country', 'Cropland_Dependency_Risk', 
                 'Agri_Importance', 'Composite_Risk_Score']].head())

# ============================================================
# PART 9: EXPLORATORY DATA ANALYSIS
# ============================================================
print("\n" + "="*60)
print("📈 EXPLORATORY DATA ANALYSIS")
print("="*60)

# Statistical summary
print("\n📊 Statistical Summary:")
print(master_df.describe())

# Find Top 10 Countries by Agricultural Land
print("\n🌍 Top 10 Countries by Agricultural Land (1000 ha):")
top_10 = master_df.nlargest(10, 'Agricultural_Land_1000ha')
print(top_10[['Country', 'Agricultural_Land_1000ha', 'Cropland_Pct']])

# Find Countries with Highest Risk
print("\n⚠️  Top 10 Countries with Highest Investment Risk:")
risky_10 = master_df.nlargest(10, 'Composite_Risk_Score')
print(risky_10[['Country', 'Composite_Risk_Score', 'Crop_Diversity_Score']])

# ============================================================
# PART 10: VISUALIZATIONS
# ============================================================
print("\n" + "="*60)
print("🎨 CREATING VISUALIZATIONS")
print("="*60)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Top 10 Countries by Agricultural Land
ax1 = axes[0, 0]
top_10 = master_df.nlargest(10, 'Agricultural_Land_1000ha')
bars1 = ax1.barh(top_10['Country'], top_10['Agricultural_Land_1000ha'], 
                 color='green', alpha=0.7)
ax1.set_xlabel('Agricultural Land (1000 ha)')
ax1.set_title('Top 10 Countries by Agricultural Land')
ax1.invert_yaxis()

# 2. Investment Score vs Crop Diversity
ax2 = axes[0, 1]
scatter = ax2.scatter(master_df['Crop_Diversity_Score'], 
                     master_df['Investment_Score'],
                     c=master_df['Agricultural_Land_1000ha'],
                     cmap='viridis', alpha=0.6, s=50)
ax2.set_xlabel('Crop Diversity Score')
ax2.set_ylabel('Investment Score')
ax2.set_title('Investment Score vs Crop Diversity')
plt.colorbar(scatter, ax=ax2, label='Agricultural Land (1000 ha)')

# 3. Risk Score Distribution
ax3 = axes[1, 0]
ax3.hist(master_df['Composite_Risk_Score'], bins=20, 
         color='red', alpha=0.7, edgecolor='black')
ax3.set_xlabel('Composite Risk Score')
ax3.set_ylabel('Number of Countries')
ax3.set_title('Distribution of Investment Risk Scores')

# 4. Correlation Heatmap
ax4 = axes[1, 1]
corr_cols = ['Agricultural_Land_1000ha', 'Cropland_1000ha', 
             'Cropland_Pct', 'Agri_GDP_Million', 'Investment_Score',
             'Crop_Diversity_Score', 'Composite_Risk_Score']
corr_matrix = master_df[corr_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            fmt='.2f', square=True, ax=ax4)
ax4.set_title('Correlation Matrix of Agricultural Metrics')

plt.tight_layout()
plt.savefig('agricultural_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Visualization saved as 'agricultural_analysis.png'")

# ============================================================
# PART 11: GEOSPATIAL ANALYSIS (Using Lat/Lon for Countries)
# ============================================================
print("\n" + "="*60)
print("🌍 GEOSPATIAL ANALYSIS")
print("="*60)

# Create approximate coordinates for countries (centroid)
# We'll map countries to approximate lat/lon
country_coords = {
    'Afghanistan': (33.9391, 67.7100),
    'Albania': (41.1533, 20.1683),
    'Algeria': (28.0339, 1.6596),
    'Angola': (-11.2027, 17.8739),
    'Argentina': (-38.4161, -63.6167),
    'Armenia': (40.0691, 45.0382),
    'Australia': (-25.2744, 133.7751),
    'Austria': (47.5162, 14.5501),
    'Azerbaijan': (40.1431, 47.5769),
    'Bangladesh': (23.6850, 90.3563),
    'Belarus': (53.7098, 27.9534),
    'Belgium': (50.5039, 4.4699),
    'Bolivia (Plurinational State of)': (-16.2902, -63.5887),
    'Brazil': (-14.2350, -51.9253),
    'Bulgaria': (42.7339, 25.4858),
    'Burkina Faso': (12.2383, -1.5616),
    'Burundi': (-3.3731, 29.9189),
    'Cambodia': (12.5657, 104.9910),
    'Cameroon': (7.3697, 12.3547),
    'Canada': (56.1304, -106.3468),
    'Central African Republic': (6.6111, 20.9394),
    'Chad': (15.4542, 18.7322),
    'Chile': (-35.6751, -71.5430),
    'China': (35.8617, 104.1954),
    'Colombia': (4.5709, -74.2973),
    'Congo': (-0.2280, 15.8277),
    'Costa Rica': (9.7489, -83.7534),
    'Côte d\'Ivoire': (7.5400, -5.5471),
    'Croatia': (45.1000, 15.2000),
    'Cuba': (21.5218, -77.7812),
    'Czechia': (49.8175, 15.4730),
    'Democratic Republic of the Congo': (-4.0383, 21.7587),
    'Denmark': (56.2639, 9.5018),
    'Ecuador': (-1.8312, -78.1834),
    'Egypt': (26.8206, 30.8025),
    'El Salvador': (13.7942, -88.8965),
    'Eritrea': (15.1794, 39.7823),
    'Estonia': (58.5953, 25.0136),
    'Ethiopia': (9.1450, 40.4897),
    'Finland': (61.9241, 25.7482),
    'France': (46.6034, 1.8883),
    'Gabon': (-0.8037, 11.6094),
    'Gambia': (13.4432, -15.3101),
    'Georgia': (42.3154, 43.3569),
    'Germany': (51.1657, 10.4515),
    'Ghana': (7.9465, -1.0232),
    'Greece': (39.0742, 21.8243),
    'Guatemala': (15.7835, -90.2308),
    'Guinea': (9.9456, -9.6966),
    'Guyana': (4.8604, -58.9302),
    'Haiti': (18.9712, -72.2852),
    'Honduras': (15.2000, -86.2419),
    'Hungary': (47.1625, 19.5033),
    'Iceland': (64.9631, -19.0208),
    'India': (20.5937, 78.9629),
    'Indonesia': (-0.7893, 113.9213),
    'Iran (Islamic Republic of)': (32.4279, 53.6880),
    'Iraq': (33.2232, 43.6793),
    'Ireland': (53.4129, -8.2439),
    'Israel': (31.0461, 34.8516),
    'Italy': (41.8719, 12.5674),
    'Jamaica': (18.1096, -77.2975),
    'Japan': (36.2048, 138.2529),
    'Jordan': (30.5852, 36.2384),
    'Kazakhstan': (48.0196, 66.9237),
    'Kenya': (-1.2864, 36.8172),
    'Kuwait': (29.3117, 47.4818),
    'Kyrgyzstan': (41.2044, 74.7661),
    'Latvia': (56.8796, 24.6032),
    'Lebanon': (33.8547, 35.8623),
    'Lesotho': (-29.6096, 28.2336),
    'Liberia': (6.4281, -9.4295),
    'Libya': (26.3351, 17.2283),
    'Lithuania': (55.1694, 23.8813),
    'Luxembourg': (49.8153, 6.1296),
    'Madagascar': (-18.7669, 46.8691),
    'Malawi': (-13.2543, 34.3015),
    'Malaysia': (4.2105, 101.9758),
    'Mali': (17.5707, -3.9962),
    'Mauritania': (21.0079, -10.9408),
    'Mauritius': (-20.3484, 57.5522),
    'Mexico': (23.6345, -102.5528),
    'Mongolia': (46.8625, 103.8467),
    'Morocco': (31.7917, -7.0926),
    'Mozambique': (-18.6657, 35.5296),
    'Myanmar': (21.9162, 95.9560),
    'Namibia': (-22.9576, 18.4904),
    'Nepal': (28.3949, 84.1240),
    'Netherlands (Kingdom of the)': (52.1326, 5.2913),
    'New Zealand': (-40.9006, 174.8860),
    'Nicaragua': (12.8654, -85.2072),
    'Niger': (17.6078, 8.0817),
    'Nigeria': (9.0820, 8.6753),
    'Norway': (60.4720, 8.4689),
    'Pakistan': (30.3753, 69.3451),
    'Panama': (8.5380, -80.7821),
    'Paraguay': (-23.4425, -58.4438),
    'Peru': (-9.1900, -75.0152),
    'Philippines': (12.8797, 121.7740),
    'Poland': (51.9194, 19.1451),
    'Portugal': (39.3999, -8.2245),
    'Republic of Moldova': (47.4116, 28.3699),
    'Romania': (45.9432, 24.9668),
    'Russian Federation': (61.5240, 105.3188),
    'Rwanda': (-1.9403, 29.8739),
    'Saudi Arabia': (23.8859, 45.0792),
    'Senegal': (14.4974, -14.4524),
    'Serbia': (44.0165, 21.0059),
    'Sierra Leone': (8.4606, -11.7799),
    'Slovakia': (48.6690, 19.6990),
    'Slovenia': (46.1512, 14.9955),
    'Somalia': (5.1521, 46.1996),
    'South Africa': (-30.5595, 22.9375),
    'South Sudan': (6.8770, 31.3070),
    'Spain': (40.4637, -3.7492),
    'Sri Lanka': (7.8731, 80.7718),
    'Sudan': (12.8628, 30.2176),
    'Suriname': (3.9193, -56.0278),
    'Sweden': (60.1282, 18.6435),
    'Switzerland': (46.8182, 8.2275),
    'Syrian Arab Republic': (34.8021, 38.9968),
    'Tajikistan': (38.8610, 71.2761),
    'Thailand': (15.8700, 100.9925),
    'Togo': (8.6195, 0.8248),
    'Tunisia': (33.8869, 9.5375),
    'Türkiye': (38.9637, 35.2433),
    'Turkmenistan': (38.9697, 59.5563),
    'Uganda': (1.3733, 32.2903),
    'Ukraine': (48.3794, 31.1656),
    'United Arab Emirates': (23.4241, 53.8478),
    'United Kingdom of Great Britain and Northern Ireland': (55.3781, -3.4360),
    'United Republic of Tanzania': (-6.3690, 34.8888),
    'United States of America': (37.0902, -95.7129),
    'Uruguay': (-32.5228, -55.7658),
    'Uzbekistan': (41.3775, 64.5853),
    'Venezuela (Bolivarian Republic of)': (6.4238, -66.5897),
    'Viet Nam': (14.0583, 108.2772),
    'Yemen': (15.5527, 48.5164),
    'Zambia': (-13.1339, 27.8493),
    'Zimbabwe': (-19.0154, 29.1549),
}

# Add coordinates to master dataset
master_df['Latitude'] = master_df['Country'].map(lambda x: country_coords.get(x, (None, None))[0])
master_df['Longitude'] = master_df['Country'].map(lambda x: country_coords.get(x, (None, None))[1])

# Drop rows with missing coordinates
geo_df = master_df.dropna(subset=['Latitude', 'Longitude']).copy()
print(f"✅ {len(geo_df)} countries with valid coordinates")

# ============================================================
# PART 12: PERFORM GWR ANALYSIS
# ============================================================
print("\n" + "="*60)
print("📍 GEOGRAPHICALLY WEIGHTED REGRESSION (GWR)")
print("="*60)

# Prepare data for GWR
# X = predictors (risk factors)
# y = response (investment score)

X_vars = ['Cropland_Dependency_Risk', 'Crop_Diversity_Score', 'Agri_Importance']
y_var = 'Investment_Score'

# Standardize predictors
scaler = StandardScaler()
X_scaled = scaler.fit_transform(geo_df[X_vars])
X_scaled_df = pd.DataFrame(X_scaled, columns=X_vars)

y = geo_df[y_var].values
coords = geo_df[['Longitude', 'Latitude']].values

# Try GWR
try:
    print("\n🔄 Running GWR with adaptive bandwidth...")
    
    # Fit GWR
    gwr = GWLinearRegression(bandwidth=50, fixed=False, kernel='tricube')
    gwr.fit(X_scaled_df, y, coords)
    
    # Get results
    geo_df['Predicted_Score'] = gwr.predict(X_scaled_df, coords)
    geo_df['Residual'] = y - geo_df['Predicted_Score']
    geo_df['Local_R2'] = gwr.local_r2_
    
    # Extract coefficients
    for i, var in enumerate(X_vars):
        geo_df[f'Coef_{var}'] = gwr.local_coef_[:, i]
    
    print(f"✅ GWR R²: {gwr.r2_:.3f}")
    print(f"✅ Mean Local R²: {geo_df['Local_R2'].mean():.3f}")
    
except Exception as e:
    print(f"⚠️  GWR failed: {e}")
    print("🔄 Using Standard Linear Regression instead...")
    
    # Fallback to standard regression
    model = LinearRegression()
    model.fit(X_scaled, y)
    y_pred = model.predict(X_scaled)
    
    geo_df['Predicted_Score'] = y_pred
    geo_df['Residual'] = y - y_pred
    geo_df['Local_R2'] = r2_score(y, y_pred)
    
    print(f"✅ Linear Regression R²: {r2_score(y, y_pred):.3f}")
    
    # Store coefficients
    for i, var in enumerate(X_vars):
        geo_df[f'Coef_{var}'] = model.coef_[i]
    
    print("📌 Coefficients:")
    for var, coef in zip(X_vars, model.coef_):
        print(f"   {var}: {coef:.3f}")

# ============================================================
# PART 13: SPATIAL VISUALIZATION
# ============================================================
print("\n" + "="*60)
print("🗺️  SPATIAL VISUALIZATIONS")
print("="*60)

# 1. Create a map showing Investment Scores
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# Plot 1: Investment Score by Country
ax1 = axes[0, 0]
scatter1 = ax1.scatter(geo_df['Longitude'], geo_df['Latitude'],
                       c=geo_df['Investment_Score'], cmap='RdYlGn',
                       s=geo_df['Agricultural_Land_1000ha'] / 1000 + 20,
                       alpha=0.7, edgecolor='black', linewidth=0.5)
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax1.set_title('Investment Score by Country\n(Color = Score, Size = Agricultural Land)')
plt.colorbar(scatter1, ax=ax1, label='Investment Score')

# Plot 2: Composite Risk Score
ax2 = axes[0, 1]
scatter2 = ax2.scatter(geo_df['Longitude'], geo_df['Latitude'],
                       c=geo_df['Composite_Risk_Score'], cmap='RdYlGn_r',
                       s=geo_df['Cropland_Dependency_Risk'] * 100 + 20,
                       alpha=0.7, edgecolor='black', linewidth=0.5)
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
ax2.set_title('Investment Risk Score\n(Color = Risk, Size = Cropland Dependency)')
plt.colorbar(scatter2, ax=ax2, label='Risk Score')

# Plot 3: Local R² from GWR
ax3 = axes[1, 0]
scatter3 = ax3.scatter(geo_df['Longitude'], geo_df['Latitude'],
                       c=geo_df['Local_R2'], cmap='Blues',
                       s=50, alpha=0.7, edgecolor='black', linewidth=0.5)
ax3.set_xlabel('Longitude')
ax3.set_ylabel('Latitude')
ax3.set_title('GWR Local R² (Model Fit)')
plt.colorbar(scatter3, ax=ax3, label='Local R²')

# Plot 4: Cropland Dependency Risk
ax4 = axes[1, 1]
scatter4 = ax4.scatter(geo_df['Longitude'], geo_df['Latitude'],
                       c=geo_df['Cropland_Dependency_Risk'], cmap='OrRd',
                       s=50, alpha=0.7, edgecolor='black', linewidth=0.5)
ax4.set_xlabel('Longitude')
ax4.set_ylabel('Latitude')
ax4.set_title('Cropland Dependency Risk\n(Higher = More Risky)')
plt.colorbar(scatter4, ax=ax4, label='Cropland Risk')

plt.tight_layout()
plt.savefig('spatial_analysis_map.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Spatial map saved as 'spatial_analysis_map.png'")

# ============================================================
# PART 14: INTERACTIVE MAP (HTML)
# ============================================================
print("\n" + "="*60)
print("🌐 CREATING INTERACTIVE MAP")
print("="*60)

# Create interactive map with folium
m = folium.Map(location=[20, 10], zoom_start=2)

# Add markers for each country
for idx, row in geo_df.iterrows():
    popup_text = f"""
    <b>Country:</b> {row['Country']}<br>
    <b>Agricultural Land:</b> {row['Agricultural_Land_1000ha']:,.0f} 1000 ha<br>
    <b>Investment Score:</b> {row['Investment_Score']:.1f}<br>
    <b>Risk Score:</b> {row['Composite_Risk_Score']:.3f}<br>
    <b>Local R²:</b> {row['Local_R2']:.3f}<br>
    <b>Cropland:</b> {row['Cropland_1000ha']:,.0f} 1000 ha
    """
    
    # Color based on investment score
    if row['Investment_Score'] > 70:
        color = 'green'
    elif row['Investment_Score'] > 45:
        color = 'orange'
    else:
        color = 'red'
    
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5 + (row['Agricultural_Land_1000ha'] / 50000),
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6
    ).add_to(m)

m.save('interactive_risk_map.html')
print("✅ Interactive map saved as 'interactive_risk_map.html'")
print("   → Open this file in your browser to explore!")

# ============================================================
# PART 15: SAVE FINAL RESULTS
# ============================================================
print("\n" + "="*60)
print("💾 SAVING FINAL RESULTS")
print("="*60)

# Save the final dataset with all results
final_columns = ['Country', 'Agricultural_Land_1000ha', 'Cropland_1000ha',
                 'Investment_Score', 'Composite_Risk_Score', 'Local_R2',
                 'Latitude', 'Longitude', 'Predicted_Score', 'Residual']

final_df = geo_df[final_columns].copy()
final_df.to_csv('final_results.csv', index=False)
print("✅ Final results saved to 'final_results.csv'")

# ============================================================
# PART 16: INSIGHTS SUMMARY
# ============================================================
print("\n" + "="*60)
print("📊 KEY INSIGHTS SUMMARY")
print("="*60)

print("\n📌 TOP 5 COUNTRIES BY INVESTMENT SCORE:")
print(geo_df.nlargest(5, 'Investment_Score')[['Country', 'Investment_Score']])

print("\n📌 TOP 5 COUNTRIES BY RISK SCORE:")
print(geo_df.nlargest(5, 'Composite_Risk_Score')[['Country', 'Composite_Risk_Score']])

print("\n📌 TOP 5 COUNTRIES BY AGRICULTURAL LAND:")
print(geo_df.nlargest(5, 'Agricultural_Land_1000ha')[['Country', 'Agricultural_Land_1000ha']])

print("\n📌 CORRELATION BETWEEN RISK AND INVESTMENT:")
corr_risk_invest = geo_df['Composite_Risk_Score'].corr(geo_df['Investment_Score'])
print(f"   Correlation: {corr_risk_invest:.3f}")

if corr_risk_invest < -0.5:
    print("   → Strong negative correlation: Higher risk = Lower investment")
elif corr_risk_invest < 0:
    print("   → Moderate negative correlation: Risk reduces investment")
else:
    print("   → Positive or weak correlation: Risk doesn't deter investment")

print("\n" + "="*60)
print("✅ ANALYSIS COMPLETE!")
print("="*60)
print("\n📁 FILES GENERATED:")
print("   1. agricultural_master_data.csv - Main dataset")
print("   2. final_results.csv - Results with predictions")
print("   3. agricultural_analysis.png - EDA visualizations")
print("   4. spatial_analysis_map.png - Spatial maps")
print("   5. interactive_risk_map.html - Interactive map (open in browser)")
print("   6. project_code.py - This complete code file")