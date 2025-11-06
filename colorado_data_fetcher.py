#!/usr/bin/env python3
"""
Colorado Resort Data Fetcher
Integrates the Selenium scraper with the existing Datawrapper pipeline
"""

import pandas as pd
import logging
from datetime import datetime
from colorado_ski_scraper import ColoradoSkiScraper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_fetcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Known Colorado resort coordinates (from your manual data)
RESORT_COORDINATES = {
    'Arapahoe Basin': {'lat': 39.634108, 'lng': -105.87147},
    'Aspen Highlands': {'lat': 39.1820055, 'lng': -106.8564},
    'Aspen Mountain': {'lat': 39.1862685, 'lng': -106.81821},
    'Beaver Creek': {'lat': 39.6016505, 'lng': -106.53161},
    'Breckenridge': {'lat': 39.4782643, 'lng': -106.07232},
    'Buttermilk': {'lat': 39.2058029, 'lng': -106.86107},
    'Cooper': {'lat': 39.3601951, 'lng': -106.30145},
    'Copper Mountain': {'lat': 39.5004501, 'lng': -106.15578},
    'Crested Butte': {'lat': 38.8991036, 'lng': -106.96576},
    'Echo Mountain': {'lat': 39.6845817, 'lng': -105.51939},
    'Eldora': {'lat': 39.9372203, 'lng': -105.58268},
    'Granby Ranch': {'lat': 40.0446489, 'lng': -105.90633},
    'Hesperus': {'lat': 37.2991673, 'lng': -108.05513},
    'Howelsen Hill': {'lat': 40.4833683, 'lng': -106.83797},
    'Kendall Mountain': {'lat': 37.8111854, 'lng': -107.65682},
    'Keystone': {'lat': 39.5816989, 'lng': -105.94367},
    'Loveland': {'lat': 39.6775332, 'lng': -105.90536},
    'Monarch': {'lat': 38.5120635, 'lng': -106.33197},
    'Powderhorn': {'lat': 39.0693741, 'lng': -108.15071},
    'Purgatory': {'lat': 37.6276821, 'lng': -107.83761},
    'Silverton': {'lat': 37.884608, 'lng': -107.66592},
    'Snowmass': {'lat': 39.2130418, 'lng': -106.93782},
    'Steamboat': {'lat': 40.4537983, 'lng': -106.77088},
    'Sunlight': {'lat': 39.3997821, 'lng': -107.33876},
    'Telluride': {'lat': 37.9166674, 'lng': -107.83748},
    'Vail': {'lat': 39.6061444, 'lng': -106.35497},
    'Winter Park': {'lat': 39.8627761, 'lng': -105.77874},
    'Wolf Creek': {'lat': 37.4717059, 'lng': -106.78829},
}


class ColoradoDataFetcher:
    """Fetches and processes Colorado resort data"""
    
    def __init__(self):
        self.scraper = ColoradoSkiScraper(headless=True)
    
    def fetch_all_resorts(self):
        """
        Fetch current conditions for all Colorado resorts
        
        Returns:
            pandas.DataFrame: Standardized resort data with coordinates
        """
        try:
            logger.info("Fetching Colorado resort data...")
            
            # Scrape the data
            df = self.scraper.scrape()
            
            if df.empty:
                logger.error("No data scraped!")
                return pd.DataFrame()
            
            # Add coordinates
            df = self._add_coordinates(df)
            
            # Standardize column names for Datawrapper
            df = self._standardize_columns(df)
            
            # Add derived fields
            df = self._add_derived_fields(df)
            
            logger.info(f"✅ Processed data for {len(df)} resorts")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching resort data: {e}")
            raise
    
    def _add_coordinates(self, df):
        """Add latitude/longitude to resorts"""
        
        def find_coordinates(name):
            """Match resort name to known coordinates"""
            name_clean = name.lower().strip()
            
            for resort_name, coords in RESORT_COORDINATES.items():
                if resort_name.lower() in name_clean or name_clean in resort_name.lower():
                    return pd.Series([coords['lat'], coords['lng']])
            
            # No match found
            logger.warning(f"No coordinates found for: {name}")
            return pd.Series([None, None])
        
        df[['latitude', 'longitude']] = df['name'].apply(find_coordinates)
        
        # Log resorts without coordinates
        missing = df[df['latitude'].isna()]
        if len(missing) > 0:
            logger.warning(f"Missing coordinates for {len(missing)} resorts:")
            for name in missing['name']:
                logger.warning(f"  - {name}")
        
        return df
    
    def _standardize_columns(self, df):
        """Standardize column names"""
        
        # Rename to match existing structure
        column_mapping = {
            'name': 'resort_name',
            'new_snow_24h': 'new_snow_24h',
            'open_trails': 'runs_open',
            'total_trails': 'runs_total',
            'conditions': 'conditions',
            'latitude': 'latitude',
            'longitude': 'longitude',
        }
        
        df = df.rename(columns=column_mapping)
        
        # Ensure all required columns exist
        required = ['resort_name', 'new_snow_24h', 'runs_open', 'runs_total', 
                   'latitude', 'longitude', 'conditions']
        
        for col in required:
            if col not in df.columns:
                if col in ['resort_name', 'conditions']:
                    df[col] = ''
                elif col in ['latitude', 'longitude']:
                    df[col] = None
                else:
                    df[col] = 0
        
        return df
    
    def _add_derived_fields(self, df):
        """Add calculated fields"""
        
        # Calculate percentage of runs open
        df['runs_open_pct'] = (df['runs_open'] / df['runs_total'] * 100).round(0)
        df['runs_open_pct'] = df['runs_open_pct'].replace([float('inf'), -float('inf')], 0)
        
        # Determine operating status
        df['status'] = df.apply(self._determine_status, axis=1)
        
        # Add timestamp
        df['data_fetched_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return df
    
    def _determine_status(self, row):
        """Determine if resort is Open, Closed, or Limited"""
        conditions = str(row['conditions']).lower()
        
        if 'closed' in conditions:
            return 'Closed'
        elif row['runs_open'] > 0:
            if row['runs_open_pct'] < 25:
                return 'Limited'
            else:
                return 'Open'
        else:
            return 'Closed'
    
    def get_summary_stats(self, df):
        """Calculate summary statistics"""
        stats = {
            'total_resorts': len(df),
            'resorts_open': len(df[df['status'] != 'Closed']),
            'avg_runs_open_pct': df[df['runs_open'] > 0]['runs_open_pct'].mean(),
            'resorts_with_new_snow': len(df[df['new_snow_24h'] > 0]),
            'max_new_snow': df['new_snow_24h'].max(),
        }
        
        logger.info("="*60)
        logger.info("SUMMARY STATISTICS")
        logger.info("="*60)
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        logger.info("="*60)
        
        return stats


def main():
    """Test the data fetcher"""
    logger.info("="*70)
    logger.info("COLORADO DATA FETCHER - TEST RUN")
    logger.info("="*70)
    
    fetcher = ColoradoDataFetcher()
    
    try:
        df = fetcher.fetch_all_resorts()
        
        if df.empty:
            logger.error("No data fetched")
            return
        
        # Get summary
        stats = fetcher.get_summary_stats(df)
        
        # Save to CSV
        output_file = "colorado_resorts_final.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"\n✅ Saved final data to {output_file}")
        
        # Display preview
        print("\n" + "="*70)
        print("DATA PREVIEW")
        print("="*70)
        cols_to_show = ['resort_name', 'new_snow_24h', 'runs_open', 'runs_total', 
                       'status', 'latitude', 'longitude']
        print(df[cols_to_show].head(15).to_string())
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

