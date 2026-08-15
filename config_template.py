"""
Configuration Template for Agricultural Investment Risk Analysis

This file provides a template for creating custom configurations
for different analysis scenarios.

To use:
1. Copy this file as config_custom.py
2. Modify the parameters as needed
3. Import in your analysis scripts
"""

from pathlib import Path
from typing import Optional

class AnalysisConfig:
    """Custom analysis configuration."""
    
    # ============================================================
    # INPUT/OUTPUT CONFIGURATION
    # ============================================================
    
    # Input data file
    INPUT_FILE: Path = Path('faostat_landuse.csv')
    
    # Output directory
    OUTPUT_DIR: Path = Path('output')
    
    # Create output directory automatically
    AUTO_CREATE_OUTPUT_DIR: bool = True
    
    # ============================================================
    # ANALYSIS PARAMETERS
    # ============================================================
    
    # Random seed for reproducibility
    RANDOM_SEED: int = 42
    
    # GWR (Geographically Weighted Regression) parameters
    GWR_BANDWIDTH: float = 50.0
    GWR_KERNEL: str = 'tricube'  # Options: 'tricube', 'gaussian', 'uniform'
    GWR_FIXED: bool = False  # Fixed or adaptive bandwidth
    
    # Financial metrics configuration
    FINANCIAL_CONFIG = {
        'agri_gdp_multiplier_min': 0.5,
        'agri_gdp_multiplier_max': 3.0,
        'crop_diversity_base': 3,
        'crop_diversity_random_max': 2,
        'investment_score_components': {
            'base': 30,
            'land_factor': 30,
            'diversity_factor': 20,
            'random_max': 20
        }
    }
    
    # Risk scoring weights
    RISK_WEIGHTS = {
        'cropland_dependency': 0.4,
        'crop_diversity': 0.3,
        'agricultural_importance': 0.3
    }
    
    # ============================================================
    # VISUALIZATION CONFIGURATION
    # ============================================================
    
    # Image export resolution (DPI)
    DPI: int = 300
    
    # Figure dimensions (width, height)
    FIGURE_SIZE: tuple = (15, 12)
    
    # Color maps for visualizations
    COLORMAP_POSITIVE: str = 'RdYlGn'  # For investment scores
    COLORMAP_RISK: str = 'RdYlGn_r'    # For risk scores
    COLORMAP_DATA: str = 'viridis'     # For data scatter plots
    
    # Figure style
    PLOT_STYLE: str = 'seaborn-v0_8-darkgrid'
    
    # ============================================================
    # FOLIUM MAP CONFIGURATION
    # ============================================================
    
    # Initial map location (latitude, longitude)
    FOLIUM_INITIAL_LOCATION: tuple = (20, 10)
    
    # Initial zoom level
    FOLIUM_INITIAL_ZOOM: int = 2
    
    # Color mapping for investment scores
    FOLIUM_COLOR_MAPPING = {
        'high': 'green',      # > 70
        'moderate': 'orange',  # 45-70
        'low': 'red'          # < 45
    }
    
    # ============================================================
    # LOGGING CONFIGURATION
    # ============================================================
    
    # Enable logging to file
    ENABLE_FILE_LOGGING: bool = True
    
    # Log file location
    LOG_FILE: Optional[Path] = None  # If None, uses output_dir/analysis.log
    
    # Log level
    LOG_LEVEL: str = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # ============================================================
    # DATA PROCESSING CONFIGURATION
    # ============================================================
    
    # Land use types to analyze
    LAND_USE_TYPES = [
        'Agricultural land',
        'Cropland',
        'Permanent crops'
    ]
    
    # Regression variables
    REGRESSION_PREDICTORS = [
        'Cropland_Dependency_Risk',
        'Crop_Diversity_Score',
        'Agri_Importance'
    ]
    REGRESSION_RESPONSE = 'Investment_Score'
    
    # ============================================================
    # OUTPUT CONFIGURATION
    # ============================================================
    
    # Generate analysis visualizations
    GENERATE_ANALYSIS_PLOT: bool = True
    ANALYSIS_PLOT_FILENAME: str = 'agricultural_analysis.png'
    
    # Generate spatial analysis plot
    GENERATE_SPATIAL_PLOT: bool = True
    SPATIAL_PLOT_FILENAME: str = 'spatial_analysis_map.png'
    
    # Generate interactive map
    GENERATE_INTERACTIVE_MAP: bool = True
    INTERACTIVE_MAP_FILENAME: str = 'interactive_risk_map.html'
    
    # Generate JSON summary
    GENERATE_SUMMARY_JSON: bool = True
    SUMMARY_JSON_FILENAME: str = 'analysis_summary.json'
    
    # ============================================================
    # PERFORMANCE CONFIGURATION
    # ============================================================
    
    # Number of threads for parallel processing
    NUM_THREADS: int = 1
    
    # Batch size for large dataset processing
    BATCH_SIZE: int = 1000
    
    # ============================================================
    # VALIDATION CONFIGURATION
    # ============================================================
    
    # Strict data validation
    STRICT_VALIDATION: bool = True
    
    # Remove rows with missing critical values
    REMOVE_MISSING_CRITICAL: bool = True
    
    # Minimum countries required for analysis
    MIN_COUNTRIES_REQUIRED: int = 10
    
    # ============================================================
    # SCENARIO CONFIGURATION
    # ============================================================
    
    # Scenario name for output organization
    SCENARIO_NAME: str = 'default'
    
    # Save scenario configuration
    SAVE_SCENARIO_CONFIG: bool = True
    
    @classmethod
    def to_dict(cls) -> dict:
        """Convert configuration to dictionary."""
        return {
            key: getattr(cls, key) for key in dir(cls)
            if not key.startswith('_') and not callable(getattr(cls, key))
        }
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> None:
        """Load configuration from dictionary."""
        for key, value in config_dict.items():
            if hasattr(cls, key):
                setattr(cls, key, value)


# ============================================================
# PREDEFINED SCENARIOS
# ============================================================

class QuickAnalysisConfig(AnalysisConfig):
    """Fast analysis with reduced quality."""
    DPI = 150
    GWR_BANDWIDTH = 100
    FIGURE_SIZE = (10, 8)


class HighQualityConfig(AnalysisConfig):
    """High-quality analysis with best results."""
    DPI = 600
    GWR_BANDWIDTH = 25
    FIGURE_SIZE = (20, 16)


class ProductionConfig(AnalysisConfig):
    """Production-ready configuration."""
    DPI = 300
    ENABLE_FILE_LOGGING = True
    STRICT_VALIDATION = True
    GENERATE_ANALYSIS_PLOT = True
    GENERATE_SPATIAL_PLOT = True
    GENERATE_INTERACTIVE_MAP = True
    GENERATE_SUMMARY_JSON = True


# ============================================================
# USAGE EXAMPLES
# ============================================================

if __name__ == '__main__':
    # Print default configuration
    print("Default Configuration:")
    for key, value in AnalysisConfig.to_dict().items():
        print(f"  {key}: {value}")
    
    # Use quick analysis
    print("\nUsing QuickAnalysisConfig:")
    print(f"  DPI: {QuickAnalysisConfig.DPI}")
    print(f"  FIGURE_SIZE: {QuickAnalysisConfig.FIGURE_SIZE}")
