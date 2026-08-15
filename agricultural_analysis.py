"""
============================================================
AGRICULTURAL INVESTMENT RISK ANALYSIS - PROFESSIONAL VERSION
Using FAOSTAT Land Use Data & Geographically Weighted Regression
============================================================
Team: Nojus Vizgirdas, REGIS UWIMENA, IRUTABYOSE Yoramu
Course: MScFE 600 Financial Data
============================================================

This module provides a complete analysis framework for agricultural
investment risk assessment using geospatial and statistical analysis.
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Dict, Tuple, Optional, Any
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import geopandas as gpd
from shapely.geometry import Point
import folium

# ============================================================
# CONFIGURATION AND LOGGING SETUP
# ============================================================

class Config:
    """Configuration management for the analysis."""
    
    # Data paths
    DATA_DIR = Path.cwd()
    INPUT_FILE = DATA_DIR / 'faostat_landuse.csv'
    
    # Output paths
    OUTPUT_DIR = DATA_DIR / 'output'
    
    # Analysis parameters
    RANDOM_SEED = 42
    GWR_BANDWIDTH = 50
    GWR_KERNEL = 'tricube'
    
    # Visualization parameters
    DPI = 300
    FIGURE_SIZE = (15, 12)
    COLORMAP_POSITIVE = 'RdYlGn'
    COLORMAP_RISK = 'RdYlGn_r'
    
    @classmethod
    def setup_output_directory(cls) -> None:
        """Create output directory if it doesn't exist."""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_output_path(cls, filename: str) -> Path:
        """Get full path for output file."""
        return cls.OUTPUT_DIR / filename


def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup comprehensive logging system.
    
    Args:
        log_file: Optional path to log file. If None, logs to console only.
    
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger('AgriculturalAnalysis')
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


# Initialize output directory first
Config.setup_output_directory()
logger = setup_logging(log_file=Config.get_output_path('analysis.log'))

# ============================================================
# DATA LOADING AND VALIDATION
# ============================================================

class DataLoader:
    """Handle data loading and validation."""
    
    @staticmethod
    def load_faostat_data(filepath: Path) -> pd.DataFrame:
        """
        Load FAOSTAT land use data with error handling.
        
        Args:
            filepath: Path to CSV file
        
        Returns:
            DataFrame with FAOSTAT data
        
        Raises:
            FileNotFoundError: If file doesn't exist
            pd.errors.ParserError: If file cannot be parsed
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        try:
            logger.info(f"Loading FAOSTAT data from {filepath}")
            df = pd.read_csv(filepath)
            logger.info(f"✅ Loaded {len(df)} rows with columns: {list(df.columns)}")
            return df
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing CSV file: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            raise
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> bool:
        """Validate data structure and required columns."""
        required_cols = ['Area', 'Area Code (M49)', 'Item', 'Value', 'Unit']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            logger.error(f"Missing required columns: {missing}")
            return False
        
        if df.empty:
            logger.error("Data is empty")
            return False
        
        if df[['Area', 'Area Code (M49)', 'Value']].isnull().any().any():
            logger.warning("Data contains null values in critical columns")
        
        return True

# ============================================================
# DATA PROCESSING AND FEATURE ENGINEERING
# ============================================================

class DataProcessor:
    """Handle data processing and feature engineering."""
    
    @staticmethod
    def filter_land_use_data(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Filter data by land use type."""
        land_types = ['Agricultural land', 'Cropland', 'Permanent crops']
        filtered = {}
        
        for land_type in land_types:
            subset = df[df['Item'] == land_type].copy()
            logger.info(f"Found {len(subset)} records for {land_type}")
            filtered[land_type] = subset
        
        return filtered
    
    @staticmethod
    def create_master_dataset(agri_df: pd.DataFrame, crop_df: pd.DataFrame, 
                            perm_crop_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create master dataset with aggregated metrics.
        
        Args:
            agri_df: Agricultural land data
            crop_df: Cropland data
            perm_crop_df: Permanent crops data
        
        Returns:
            Master dataset with all metrics
        """
        logger.info("Creating master dataset...")
        
        master_df = agri_df[['Area', 'Area Code (M49)', 'Value', 'Unit']].copy()
        master_df = master_df.rename(columns={
            'Area': 'Country',
            'Area Code (M49)': 'Country_Code',
            'Value': 'Agricultural_Land_1000ha',
            'Unit': 'Unit'
        })
        
        # Add cropland data
        crop_values = crop_df.set_index('Area Code (M49)')['Value']
        master_df['Cropland_1000ha'] = master_df['Country_Code'].map(crop_values)
        
        # Add permanent crops data
        perm_values = perm_crop_df.set_index('Area Code (M49)')['Value']
        master_df['Permanent_Crops_1000ha'] = master_df['Country_Code'].map(perm_values)
        
        # Calculate cropland percentage
        master_df['Cropland_Pct'] = (
            master_df['Cropland_1000ha'] / master_df['Agricultural_Land_1000ha']
        ) * 100
        
        logger.info(f"✅ Master dataset created with {len(master_df)} countries")
        return master_df
    
    @staticmethod
    def add_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Add synthetic but realistic financial metrics."""
        logger.info("Adding financial metrics...")
        
        np.random.seed(Config.RANDOM_SEED)
        
        # Estimated Agricultural GDP
        df['Agri_GDP_Million'] = (
            df['Agricultural_Land_1000ha'] * 
            np.random.uniform(0.5, 3.0, len(df))
        ).round(2)
        
        # Crop Diversity Score
        df['Crop_Diversity_Score'] = (
            3 + (df['Cropland_Pct'] / 10) + 
            np.random.uniform(0, 2, len(df))
        ).clip(1, 10).round(1)
        
        # Investment Attractiveness Score
        df['Investment_Score'] = (
            30 + 
            (df['Agricultural_Land_1000ha'] / df['Agricultural_Land_1000ha'].max()) * 30 +
            (df['Crop_Diversity_Score'] / 10) * 20 +
            np.random.uniform(0, 20, len(df))
        ).clip(1, 100).round(1)
        
        logger.info("✅ Financial metrics added")
        return df
    
    @staticmethod
    def add_risk_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Create risk indicators for investment analysis."""
        logger.info("Adding risk indicators...")
        
        # Cropland Dependency Risk
        df['Cropland_Dependency_Risk'] = (df['Cropland_Pct'] / 100).round(3)
        
        # Agricultural Importance
        df['Agri_Importance'] = (
            df['Agricultural_Land_1000ha'] / df['Agricultural_Land_1000ha'].max()
        ).round(3)
        
        # Composite Risk Score
        df['Composite_Risk_Score'] = (
            df['Cropland_Dependency_Risk'] * 0.4 + 
            (1 - df['Crop_Diversity_Score'] / 10) * 0.3 +
            (1 - df['Agri_Importance']) * 0.3
        ).round(3)
        
        logger.info("✅ Risk indicators added")
        return df

# ============================================================
# REGRESSION ANALYSIS
# ============================================================

class RegressionAnalyzer:
    """Handle regression analysis including GWR."""
    
    @staticmethod
    def prepare_regression_data(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare data for regression analysis.
        
        Args:
            df: Input dataframe
        
        Returns:
            Tuple of (X_scaled, y, coords)
        """
        X_vars = ['Cropland_Dependency_Risk', 'Crop_Diversity_Score', 'Agri_Importance']
        y_var = 'Investment_Score'
        
        # Remove rows with missing values
        analysis_df = df[X_vars + [y_var] + ['Longitude', 'Latitude']].dropna()
        logger.info(f"Regression analysis dataset: {len(analysis_df)} countries")
        
        scaler = StandardScaler()
        X = analysis_df[X_vars].values
        X_scaled = scaler.fit_transform(X)
        y = analysis_df[y_var].values
        coords = analysis_df[['Longitude', 'Latitude']].values
        
        return X_scaled, y, coords, analysis_df, X_vars, y_var
    
    @staticmethod
    def perform_gwr_analysis(X_scaled: np.ndarray, y: np.ndarray, 
                            coords: np.ndarray, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform Geographically Weighted Regression analysis.
        
        Args:
            X_scaled: Scaled predictor variables
            y: Response variable
            coords: Geographic coordinates
            df: Analysis dataframe
        
        Returns:
            Dictionary with GWR results
        """
        logger.info("Attempting GWR analysis...")
        
        try:
            # Import GWR
            from gwlearn.linear_model import GWLinearRegression
            
            # Convert to GeoDataFrame
            geometry = [Point(xy) for xy in coords]
            geo_df = gpd.GeoDataFrame(
                df[['Country']],
                geometry=geometry,
                crs='EPSG:4326'
            )
            
            # Fit GWR
            gwr = GWLinearRegression(
                bandwidth=Config.GWR_BANDWIDTH,
                fixed=False,
                kernel=Config.GWR_KERNEL
            )
            
            gwr.fit(X_scaled, y, geo_df.geometry)
            
            predictions = gwr.predict(X_scaled, geo_df.geometry)
            r2 = gwr.r2_
            
            logger.info(f"✅ GWR analysis successful (R² = {r2:.3f})")
            
            return {
                'success': True,
                'predictions': predictions,
                'r2': r2,
                'model': gwr,
                'type': 'GWR'
            }
        
        except ImportError:
            logger.warning("GWLearn not available, using LinearRegression")
            return None
        except Exception as e:
            logger.warning(f"GWR failed: {e}, using LinearRegression instead")
            return None
    
    @staticmethod
    def perform_linear_regression(X_scaled: np.ndarray, y: np.ndarray, 
                                 X_vars: list) -> Dict[str, Any]:
        """
        Perform standard linear regression as fallback.
        
        Args:
            X_scaled: Scaled predictor variables
            y: Response variable
            X_vars: Names of predictor variables
        
        Returns:
            Dictionary with regression results
        """
        logger.info("Performing Linear Regression analysis...")
        
        model = LinearRegression()
        model.fit(X_scaled, y)
        predictions = model.predict(X_scaled)
        r2 = r2_score(y, predictions)
        
        logger.info(f"✅ Linear Regression complete (R² = {r2:.3f})")
        logger.info("Coefficients:")
        for var, coef in zip(X_vars, model.coef_):
            logger.info(f"   {var}: {coef:.4f}")
        
        return {
            'success': True,
            'predictions': predictions,
            'r2': r2,
            'model': model,
            'type': 'Linear'
        }

# ============================================================
# GEOSPATIAL ANALYSIS
# ============================================================

class GeospatialAnalyzer:
    """Handle geospatial analysis and mapping."""
    
    COUNTRY_COORDINATES = {
        'Afghanistan': (33.9391, 67.7100), 'Albania': (41.1533, 20.1683),
        'Algeria': (28.0339, 1.6596), 'Angola': (-11.2027, 17.8739),
        'Argentina': (-38.4161, -63.6167), 'Armenia': (40.0691, 45.0382),
        'Australia': (-25.2744, 133.7751), 'Austria': (47.5162, 14.5501),
        'Azerbaijan': (40.1431, 47.5769), 'Bangladesh': (23.6850, 90.3563),
        'Belarus': (53.7098, 27.9534), 'Belgium': (50.5039, 4.4699),
        'Bolivia (Plurinational State of)': (-16.2902, -63.5887),
        'Brazil': (-14.2350, -51.9253), 'Bulgaria': (42.7339, 25.4858),
        'Burkina Faso': (12.2383, -1.5616), 'Burundi': (-3.3731, 29.9189),
        'Cambodia': (12.5657, 104.9910), 'Cameroon': (7.3697, 12.3547),
        'Canada': (56.1304, -106.3468), 'Central African Republic': (6.6111, 20.9394),
        'Chad': (15.4542, 18.7322), 'Chile': (-35.6751, -71.5430),
        'China': (35.8617, 104.1954), 'Colombia': (4.5709, -74.2973),
        'Congo': (-0.2280, 15.8277), 'Costa Rica': (9.7489, -83.7534),
        'Côte d\'Ivoire': (7.5400, -5.5471), 'Croatia': (45.1000, 15.2000),
        'Cuba': (21.5218, -77.7812), 'Czechia': (49.8175, 15.4730),
        'Democratic Republic of the Congo': (-4.0383, 21.7587),
        'Denmark': (56.2639, 9.5018), 'Ecuador': (-1.8312, -78.1834),
        'Egypt': (26.8206, 30.8025), 'El Salvador': (13.7942, -88.8965),
        'Eritrea': (15.1794, 39.7823), 'Estonia': (58.5953, 25.0136),
        'Ethiopia': (9.1450, 40.4897), 'Finland': (61.9241, 25.7482),
        'France': (46.6034, 1.8883), 'Gabon': (-0.8037, 11.6094),
        'Gambia': (13.4432, -15.3101), 'Georgia': (42.3154, 43.3569),
        'Germany': (51.1657, 10.4515), 'Ghana': (7.9465, -1.0232),
        'Greece': (39.0742, 21.8243), 'Guatemala': (15.7835, -90.2308),
        'Guinea': (9.9456, -9.6966), 'Guyana': (4.8604, -58.9302),
        'Haiti': (18.9712, -72.2852), 'Honduras': (15.2000, -86.2419),
        'Hungary': (47.1625, 19.5033), 'Iceland': (64.9631, -19.0208),
        'India': (20.5937, 78.9629), 'Indonesia': (-0.7893, 113.9213),
        'Iran (Islamic Republic of)': (32.4279, 53.6880), 'Iraq': (33.2232, 43.6793),
        'Ireland': (53.4129, -8.2439), 'Israel': (31.0461, 34.8516),
        'Italy': (41.8719, 12.5674), 'Jamaica': (18.1096, -77.2975),
        'Japan': (36.2048, 138.2529), 'Jordan': (30.5852, 36.2384),
        'Kazakhstan': (48.0196, 66.9237), 'Kenya': (-1.2864, 36.8172),
        'Kuwait': (29.3117, 47.4818), 'Kyrgyzstan': (41.2044, 74.7661),
        'Latvia': (56.8796, 24.6032), 'Lebanon': (33.8547, 35.8623),
        'Lesotho': (-29.6096, 28.2336), 'Liberia': (6.4281, -9.4295),
        'Libya': (26.3351, 17.2283), 'Lithuania': (55.1694, 23.8813),
        'Luxembourg': (49.8153, 6.1296), 'Madagascar': (-18.7669, 46.8691),
        'Malawi': (-13.2543, 34.3015), 'Malaysia': (4.2105, 101.9758),
        'Mali': (17.5707, -3.9962), 'Mauritania': (21.0079, -10.9408),
        'Mauritius': (-20.3484, 57.5522), 'Mexico': (23.6345, -102.5528),
        'Mongolia': (46.8625, 103.8467), 'Morocco': (31.7917, -7.0926),
        'Mozambique': (-18.6657, 35.5296), 'Myanmar': (21.9162, 95.9560),
        'Namibia': (-22.9576, 18.4904), 'Nepal': (28.3949, 84.1240),
        'Netherlands (Kingdom of the)': (52.1326, 5.2913),
        'New Zealand': (-40.9006, 174.8860), 'Nicaragua': (12.8654, -85.2072),
        'Niger': (17.6078, 8.0817), 'Nigeria': (9.0820, 8.6753),
        'Norway': (60.4720, 8.4689), 'Pakistan': (30.3753, 69.3451),
        'Panama': (8.5380, -80.7821), 'Paraguay': (-23.4425, -58.4438),
        'Peru': (-9.1900, -75.0152), 'Philippines': (12.8797, 121.7740),
        'Poland': (51.9194, 19.1451), 'Portugal': (39.3999, -8.2245),
        'Republic of Moldova': (47.4116, 28.3699), 'Romania': (45.9432, 24.9668),
        'Russian Federation': (61.5240, 105.3188), 'Rwanda': (-1.9403, 29.8739),
        'Saudi Arabia': (23.8859, 45.0792), 'Senegal': (14.4974, -14.4524),
        'Serbia': (44.0165, 21.0059), 'Sierra Leone': (8.4606, -11.7799),
        'Slovakia': (48.6690, 19.6990), 'Slovenia': (46.1512, 14.9955),
        'Somalia': (5.1521, 46.1996), 'South Africa': (-30.5595, 22.9375),
        'South Sudan': (6.8770, 31.3070), 'Spain': (40.4637, -3.7492),
        'Sri Lanka': (7.8731, 80.7718), 'Sudan': (12.8628, 30.2176),
        'Suriname': (3.9193, -56.0278), 'Sweden': (60.1282, 18.6435),
        'Switzerland': (46.8182, 8.2275), 'Syrian Arab Republic': (34.8021, 38.9968),
        'Tajikistan': (38.8610, 71.2761), 'Thailand': (15.8700, 100.9925),
        'Togo': (8.6195, 0.8248), 'Tunisia': (33.8869, 9.5375),
        'Türkiye': (38.9637, 35.2433), 'Turkmenistan': (38.9697, 59.5563),
        'Uganda': (1.3733, 32.2903), 'Ukraine': (48.3794, 31.1656),
        'United Arab Emirates': (23.4241, 53.8478),
        'United Kingdom of Great Britain and Northern Ireland': (55.3781, -3.4360),
        'United Republic of Tanzania': (-6.3690, 34.8888),
        'United States of America': (37.0902, -95.7129), 'Uruguay': (-32.5228, -55.7658),
        'Uzbekistan': (41.3775, 64.5853),
        'Venezuela (Bolivarian Republic of)': (6.4238, -66.5897),
        'Viet Nam': (14.0583, 108.2772), 'Yemen': (15.5527, 48.5164),
        'Zambia': (-13.1339, 27.8493), 'Zimbabwe': (-19.0154, 29.1549),
    }
    
    @staticmethod
    def add_coordinates(df: pd.DataFrame) -> pd.DataFrame:
        """Add geographic coordinates to dataframe."""
        logger.info("Adding geographic coordinates...")
        
        df['Latitude'] = df['Country'].map(
            lambda x: GeospatialAnalyzer.COUNTRY_COORDINATES.get(x, (None, None))[0]
        )
        df['Longitude'] = df['Country'].map(
            lambda x: GeospatialAnalyzer.COUNTRY_COORDINATES.get(x, (None, None))[1]
        )
        
        valid_coords = df.dropna(subset=['Latitude', 'Longitude'])
        logger.info(f"✅ {len(valid_coords)} countries with valid coordinates")
        
        return df
    
    @staticmethod
    def create_interactive_map(df: pd.DataFrame, output_path: Path) -> None:
        """Create interactive folium map."""
        logger.info("Creating interactive map...")
        
        m = folium.Map(location=[20, 10], zoom_start=2)
        
        valid_df = df.dropna(subset=['Latitude', 'Longitude'])
        
        for idx, row in valid_df.iterrows():
            popup_text = f"""
            <b>Country:</b> {row['Country']}<br>
            <b>Agricultural Land:</b> {row['Agricultural_Land_1000ha']:,.0f} 1000 ha<br>
            <b>Investment Score:</b> {row['Investment_Score']:.1f}<br>
            <b>Risk Score:</b> {row['Composite_Risk_Score']:.3f}<br>
            <b>Cropland:</b> {row['Cropland_1000ha']:,.0f} 1000 ha
            """
            
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
        
        m.save(str(output_path))
        logger.info(f"✅ Interactive map saved to {output_path}")

# ============================================================
# VISUALIZATION
# ============================================================

class Visualizer:
    """Handle all visualization tasks."""
    
    @staticmethod
    def plot_analysis(df: pd.DataFrame, output_path: Path) -> None:
        """Create comprehensive analysis visualizations."""
        logger.info("Creating analysis visualizations...")
        
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        fig, axes = plt.subplots(2, 2, figsize=Config.FIGURE_SIZE)
        
        # Top 10 countries by agricultural land
        top_10 = df.nlargest(10, 'Agricultural_Land_1000ha')
        axes[0, 0].barh(top_10['Country'], top_10['Agricultural_Land_1000ha'],
                        color='green', alpha=0.7)
        axes[0, 0].set_xlabel('Agricultural Land (1000 ha)')
        axes[0, 0].set_title('Top 10 Countries by Agricultural Land')
        axes[0, 0].invert_yaxis()
        
        # Investment vs Crop Diversity
        scatter = axes[0, 1].scatter(df['Crop_Diversity_Score'],
                                     df['Investment_Score'],
                                     c=df['Agricultural_Land_1000ha'],
                                     cmap='viridis', alpha=0.6, s=50)
        axes[0, 1].set_xlabel('Crop Diversity Score')
        axes[0, 1].set_ylabel('Investment Score')
        axes[0, 1].set_title('Investment Score vs Crop Diversity')
        plt.colorbar(scatter, ax=axes[0, 1], label='Agricultural Land (1000 ha)')
        
        # Risk distribution
        axes[1, 0].hist(df['Composite_Risk_Score'], bins=20,
                        color='red', alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Composite Risk Score')
        axes[1, 0].set_ylabel('Number of Countries')
        axes[1, 0].set_title('Distribution of Investment Risk Scores')
        
        # Correlation heatmap
        corr_cols = ['Agricultural_Land_1000ha', 'Cropland_1000ha',
                     'Cropland_Pct', 'Agri_GDP_Million', 'Investment_Score',
                     'Crop_Diversity_Score', 'Composite_Risk_Score']
        
        valid_df = df[corr_cols].dropna()
        corr_matrix = valid_df.corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                    fmt='.2f', square=True, ax=axes[1, 1])
        axes[1, 1].set_title('Correlation Matrix')
        
        plt.tight_layout()
        plt.savefig(str(output_path), dpi=Config.DPI, bbox_inches='tight')
        logger.info(f"✅ Analysis visualization saved to {output_path}")
        plt.close()
    
    @staticmethod
    def plot_spatial_analysis(df: pd.DataFrame, output_path: Path) -> None:
        """Create spatial analysis visualizations."""
        logger.info("Creating spatial visualizations...")
        
        valid_df = df.dropna(subset=['Latitude', 'Longitude'])
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))
        
        # Investment Score
        scatter1 = axes[0, 0].scatter(valid_df['Longitude'], valid_df['Latitude'],
                                      c=valid_df['Investment_Score'],
                                      cmap=Config.COLORMAP_POSITIVE,
                                      s=valid_df['Agricultural_Land_1000ha'] / 1000 + 20,
                                      alpha=0.7, edgecolor='black', linewidth=0.5)
        axes[0, 0].set_xlabel('Longitude')
        axes[0, 0].set_ylabel('Latitude')
        axes[0, 0].set_title('Investment Score by Country\n(Size = Agricultural Land)')
        plt.colorbar(scatter1, ax=axes[0, 0], label='Investment Score')
        
        # Risk Score
        scatter2 = axes[0, 1].scatter(valid_df['Longitude'], valid_df['Latitude'],
                                      c=valid_df['Composite_Risk_Score'],
                                      cmap=Config.COLORMAP_RISK,
                                      s=valid_df['Cropland_Dependency_Risk'] * 100 + 20,
                                      alpha=0.7, edgecolor='black', linewidth=0.5)
        axes[0, 1].set_xlabel('Longitude')
        axes[0, 1].set_ylabel('Latitude')
        axes[0, 1].set_title('Investment Risk Score\n(Size = Cropland Dependency)')
        plt.colorbar(scatter2, ax=axes[0, 1], label='Risk Score')
        
        # Cropland Dependency
        scatter3 = axes[1, 0].scatter(valid_df['Longitude'], valid_df['Latitude'],
                                      c=valid_df['Cropland_Dependency_Risk'],
                                      cmap='OrRd', s=50, alpha=0.7,
                                      edgecolor='black', linewidth=0.5)
        axes[1, 0].set_xlabel('Longitude')
        axes[1, 0].set_ylabel('Latitude')
        axes[1, 0].set_title('Cropland Dependency Risk')
        plt.colorbar(scatter3, ax=axes[1, 0], label='Cropland Risk')
        
        # Diversity Score
        scatter4 = axes[1, 1].scatter(valid_df['Longitude'], valid_df['Latitude'],
                                      c=valid_df['Crop_Diversity_Score'],
                                      cmap='Blues', s=50, alpha=0.7,
                                      edgecolor='black', linewidth=0.5)
        axes[1, 1].set_xlabel('Longitude')
        axes[1, 1].set_ylabel('Latitude')
        axes[1, 1].set_title('Crop Diversity Score')
        plt.colorbar(scatter4, ax=axes[1, 1], label='Diversity')
        
        plt.tight_layout()
        plt.savefig(str(output_path), dpi=Config.DPI, bbox_inches='tight')
        logger.info(f"✅ Spatial visualization saved to {output_path}")
        plt.close()

# ============================================================
# ANALYSIS REPORTING
# ============================================================

class AnalysisReporter:
    """Generate analysis reports and summaries."""
    
    @staticmethod
    def generate_summary_stats(df: pd.DataFrame) -> None:
        """Generate and log summary statistics."""
        logger.info("=" * 60)
        logger.info("KEY INSIGHTS SUMMARY")
        logger.info("=" * 60)
        
        logger.info("\n📌 TOP 5 COUNTRIES BY INVESTMENT SCORE:")
        top_5 = df.nlargest(5, 'Investment_Score')[['Country', 'Investment_Score']]
        for idx, row in top_5.iterrows():
            logger.info(f"   {row['Country']}: {row['Investment_Score']:.1f}")
        
        logger.info("\n📌 TOP 5 COUNTRIES BY RISK SCORE:")
        risky_5 = df.nlargest(5, 'Composite_Risk_Score')[
            ['Country', 'Composite_Risk_Score']
        ]
        for idx, row in risky_5.iterrows():
            logger.info(f"   {row['Country']}: {row['Composite_Risk_Score']:.3f}")
        
        logger.info("\n📌 TOP 5 COUNTRIES BY AGRICULTURAL LAND:")
        large_5 = df.nlargest(5, 'Agricultural_Land_1000ha')[
            ['Country', 'Agricultural_Land_1000ha']
        ]
        for idx, row in large_5.iterrows():
            logger.info(f"   {row['Country']}: {row['Agricultural_Land_1000ha']:,.0f} 1000 ha")
        
        logger.info("\n📌 STATISTICAL SUMMARY:")
        stats = df[['Agricultural_Land_1000ha', 'Investment_Score',
                    'Composite_Risk_Score']].describe()
        logger.info(f"\n{stats}")
        
        # Correlation analysis
        corr = df['Composite_Risk_Score'].corr(df['Investment_Score'])
        logger.info(f"\n📌 CORRELATION BETWEEN RISK AND INVESTMENT: {corr:.3f}")
    
    @staticmethod
    def save_summary_json(df: pd.DataFrame, output_path: Path) -> None:
        """Save summary statistics as JSON."""
        summary = {
            'analysis_date': datetime.now().isoformat(),
            'total_countries': len(df),
            'valid_coordinates': len(df.dropna(subset=['Latitude', 'Longitude'])),
            'top_investment_countries': df.nlargest(5, 'Investment_Score')[
                ['Country', 'Investment_Score']
            ].to_dict(orient='records'),
            'top_risk_countries': df.nlargest(5, 'Composite_Risk_Score')[
                ['Country', 'Composite_Risk_Score']
            ].to_dict(orient='records'),
            'statistics': {
                'avg_investment_score': float(df['Investment_Score'].mean()),
                'avg_risk_score': float(df['Composite_Risk_Score'].mean()),
                'avg_agricultural_land': float(df['Agricultural_Land_1000ha'].mean())
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"✅ Summary saved to {output_path}")

# ============================================================
# MAIN ANALYSIS PIPELINE
# ============================================================

class AgriculturalAnalysisPipeline:
    """Main analysis pipeline orchestrator."""
    
    def __init__(self):
        """Initialize the pipeline."""
        # Config already initialized at module level
        self.loader = DataLoader()
        self.processor = DataProcessor()
        self.analyzer = RegressionAnalyzer()
        self.geo_analyzer = GeospatialAnalyzer()
        self.visualizer = Visualizer()
        self.reporter = AnalysisReporter()
    
    def run(self) -> None:
        """Execute the complete analysis pipeline."""
        try:
            logger.info("=" * 60)
            logger.info("STARTING AGRICULTURAL INVESTMENT ANALYSIS")
            logger.info("=" * 60)
            
            # Load and validate data
            raw_df = self.loader.load_faostat_data(Config.INPUT_FILE)
            if not self.loader.validate_data(raw_df):
                raise ValueError("Data validation failed")
            
            # Process data
            filtered = self.processor.filter_land_use_data(raw_df)
            master_df = self.processor.create_master_dataset(
                filtered['Agricultural land'],
                filtered['Cropland'],
                filtered['Permanent crops']
            )
            master_df = self.processor.add_financial_metrics(master_df)
            master_df = self.processor.add_risk_indicators(master_df)
            
            # Save master dataset
            master_output = Config.get_output_path('agricultural_master_data.csv')
            master_df.to_csv(master_output, index=False)
            logger.info(f"✅ Master dataset saved to {master_output}")
            
            # Add coordinates
            master_df = self.geo_analyzer.add_coordinates(master_df)
            
            # Perform regression analysis
            X_scaled, y, coords, analysis_df, X_vars, y_var = \
                self.analyzer.prepare_regression_data(master_df)
            
            # Try GWR, fallback to Linear Regression
            gwr_result = self.analyzer.perform_gwr_analysis(X_scaled, y, coords, analysis_df)
            if gwr_result:
                regression_result = gwr_result
            else:
                regression_result = self.analyzer.perform_linear_regression(X_scaled, y, X_vars)
            
            # Add regression results
            analysis_df['Predicted_Score'] = regression_result['predictions']
            analysis_df['Residual'] = y - regression_result['predictions']
            
            # Save results
            final_output = Config.get_output_path('final_results.csv')
            analysis_df.to_csv(final_output, index=False)
            logger.info(f"✅ Final results saved to {final_output}")
            
            # Generate visualizations
            self.visualizer.plot_analysis(
                master_df,
                Config.get_output_path('agricultural_analysis.png')
            )
            self.visualizer.plot_spatial_analysis(
                master_df,
                Config.get_output_path('spatial_analysis_map.png')
            )
            
            # Create interactive map
            self.geo_analyzer.create_interactive_map(
                master_df,
                Config.get_output_path('interactive_risk_map.html')
            )
            
            # Generate reports
            self.reporter.generate_summary_stats(master_df)
            self.reporter.save_summary_json(
                master_df,
                Config.get_output_path('analysis_summary.json')
            )
            
            logger.info("\n" + "=" * 60)
            logger.info("✅ ANALYSIS COMPLETE!")
            logger.info("=" * 60)
            logger.info("\n📁 OUTPUT FILES GENERATED:")
            logger.info("   1. agricultural_master_data.csv - Main dataset")
            logger.info("   2. final_results.csv - Results with predictions")
            logger.info("   3. agricultural_analysis.png - EDA visualizations")
            logger.info("   4. spatial_analysis_map.png - Spatial maps")
            logger.info("   5. interactive_risk_map.html - Interactive map")
            logger.info("   6. analysis_summary.json - Summary statistics")
            logger.info("   7. analysis.log - Complete log file")
            logger.info("\nAll outputs saved to: output/")
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            sys.exit(1)

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    pipeline = AgriculturalAnalysisPipeline()
    pipeline.run()
