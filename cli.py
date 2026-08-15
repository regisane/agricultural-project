#!/usr/bin/env python
"""
Command-Line Interface for Agricultural Investment Risk Analysis

This module provides a professional CLI for running the analysis
with various options and configurations.
"""

import argparse
import sys
from pathlib import Path
from agricultural_analysis import (
    Config, logger, AgriculturalAnalysisPipeline,
    DataLoader, DataProcessor, GeospatialAnalyzer
)


class CLI:
    """Command-line interface for the analysis pipeline."""
    
    def __init__(self):
        """Initialize CLI."""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            description='Agricultural Investment Risk Analysis',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python cli.py --run                 # Run full analysis
  python cli.py --validate            # Validate input data only
  python cli.py --info                # Show project information
  python cli.py --run --seed 100      # Run with custom random seed
            """
        )
        
        # Main operation options
        parser.add_argument(
            '--run', action='store_true',
            help='Run the complete analysis pipeline'
        )
        parser.add_argument(
            '--validate', action='store_true',
            help='Validate input data and exit'
        )
        parser.add_argument(
            '--info', action='store_true',
            help='Show project information'
        )
        parser.add_argument(
            '--version', action='version',
            version='Agricultural Analysis 2.0 (Professional Edition)'
        )
        
        # Configuration options
        parser.add_argument(
            '--input', type=str, default=None,
            help='Path to input CSV file (default: faostat_landuse.csv)'
        )
        parser.add_argument(
            '--output-dir', type=str, default='output',
            help='Output directory (default: output)'
        )
        parser.add_argument(
            '--seed', type=int, default=42,
            help='Random seed for reproducibility (default: 42)'
        )
        parser.add_argument(
            '--dpi', type=int, default=300,
            help='Resolution for saved images (default: 300)'
        )
        parser.add_argument(
            '--quiet', action='store_true',
            help='Suppress console output'
        )
        
        # GWR options
        parser.add_argument(
            '--gwr-bandwidth', type=float, default=50,
            help='GWR bandwidth parameter (default: 50)'
        )
        
        return parser
    
    def run(self, args=None):
        """Execute CLI based on arguments."""
        if args is None:
            args = self.parser.parse_args()
        
        # Show help if no arguments
        if len(sys.argv) == 1:
            self.parser.print_help()
            return 0
        
        # Handle --info
        if args.info:
            self._show_info()
            return 0
        
        # Handle --validate
        if args.validate:
            return self._validate_data(args)
        
        # Handle --run
        if args.run:
            return self._run_analysis(args)
        
        self.parser.print_help()
        return 0
    
    def _show_info(self) -> None:
        """Show project information."""
        print("""
╔════════════════════════════════════════════════════════════╗
║   AGRICULTURAL INVESTMENT RISK ANALYSIS                    ║
║   Professional Edition v2.0                                ║
╚════════════════════════════════════════════════════════════╝

📊 PROJECT OVERVIEW
────────────────────────────────────────────────────────────
This framework analyzes agricultural investment risk using:
  • FAOSTAT land use data (227+ countries)
  • Geospatial analysis (140+ countries with coordinates)
  • Geographically Weighted Regression (with fallback)
  • Professional visualizations and interactive maps

📁 INPUT DATA
────────────────────────────────────────────────────────────
Required file: faostat_landuse.csv
  • 2,124 records
  • Land use metrics by country
  • Three land types: Agricultural, Cropland, Permanent crops

📈 OUTPUT FILES
────────────────────────────────────────────────────────────
1. agricultural_master_data.csv - Complete dataset
2. final_results.csv - Regression results
3. agricultural_analysis.png - EDA visualizations
4. spatial_analysis_map.png - Geographic maps
5. interactive_risk_map.html - Interactive map
6. analysis_summary.json - Summary statistics
7. analysis.log - Execution log

🔧 AVAILABLE METRICS
────────────────────────────────────────────────────────────
Financial Metrics:
  • Agri_GDP_Million - Agricultural GDP estimation
  • Crop_Diversity_Score - Crop diversity (1-10)
  • Investment_Score - Investment attractiveness (0-100)

Risk Metrics:
  • Cropland_Dependency_Risk - Dependency on cropland
  • Agri_Importance - Agricultural sector importance
  • Composite_Risk_Score - Overall risk score (0-1)

📊 STATISTICAL RESULTS
────────────────────────────────────────────────────────────
Average Investment Score: 57.8
Average Risk Score: 0.552
Countries Analyzed: 227
Countries with Coordinates: 140
Regression R²: 0.470

🎯 TOP PERFORMERS
────────────────────────────────────────────────────────────
Investment Score Leaders:
  1. China, mainland: 93.6
  2. China: 83.9
  3. India: 75.7
  4. United States: 75.1
  5. Russian Federation: 74.0

Largest Agricultural Areas:
  1. China: 521,395,100 hectares
  2. United States: 423,821,437 hectares
  3. Australia: 355,775,000 hectares
  4. Brazil: 236,806,800 hectares
  5. Russian Federation: 215,494,000 hectares

👥 PROJECT TEAM
────────────────────────────────────────────────────────────
Course: MScFE 600 Financial Data
Team: Nojus Vizgirdas, REGIS UWIMENA, IRUTABYOSE Yoramu

📚 DOCUMENTATION
────────────────────────────────────────────────────────────
Full documentation: See README.md
        """)
    
    def _validate_data(self, args) -> int:
        """Validate input data."""
        logger.info("🔍 VALIDATING INPUT DATA")
        
        try:
            loader = DataLoader()
            
            # Determine input file
            if args.input:
                input_file = Path(args.input)
            else:
                input_file = Config.INPUT_FILE
            
            # Load and validate
            df = loader.load_faostat_data(input_file)
            if loader.validate_data(df):
                logger.info("✅ Data validation passed!")
                logger.info(f"   • {len(df)} records loaded")
                logger.info(f"   • {df['Area'].nunique()} unique areas")
                logger.info(f"   • {df['Item'].nunique()} unique items")
                return 0
            else:
                logger.error("❌ Data validation failed!")
                return 1
        
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return 1
    
    def _run_analysis(self, args) -> int:
        """Run the analysis pipeline."""
        logger.info("🚀 STARTING ANALYSIS")
        
        try:
            # Apply configuration overrides
            if args.input:
                Config.INPUT_FILE = Path(args.input)
            if args.output_dir:
                Config.OUTPUT_DIR = Path(args.output_dir)
            if args.seed:
                Config.RANDOM_SEED = args.seed
            if args.dpi:
                Config.DPI = args.dpi
            if args.gwr_bandwidth:
                Config.GWR_BANDWIDTH = args.gwr_bandwidth
            
            # Re-create output directory with new config
            Config.setup_output_directory()
            
            # Run pipeline
            pipeline = AgriculturalAnalysisPipeline()
            pipeline.run()
            
            logger.info("✅ Analysis completed successfully!")
            logger.info(f"📁 Results saved to: {Config.OUTPUT_DIR}")
            return 0
        
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return 1


def main():
    """Main entry point."""
    cli = CLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
