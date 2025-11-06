#!/usr/bin/env python3
"""
Ski API Data Fetcher
Fetches current snow conditions from skiapi.com for Colorado resorts
"""

import os
import pandas as pd
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ski_api_fetcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API Configuration
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_BASE_URL = "https://ski-resorts-and-conditions.p.rapidapi.com"

class SkiAPIFetcher:
    """Handles fetching and processing ski resort data from RapidAPI"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or RAPIDAPI_KEY
        self.headers = {
            "x-rapidapi-host": "ski-resorts-and-conditions.p.rapidapi.com",
            "x-rapidapi-key": self.api_key
        }
    
    def fetch_colorado_resorts(self):
        """
        Fetch all Colorado resort data from RapidAPI
        
        Returns:
            pandas.DataFrame: Resort data with standardized columns
        """
        try:
            logger.info("Fetching Colorado resort data from RapidAPI")
            
            # Try different endpoint patterns
            # Start with the most likely based on RapidAPI documentation
            endpoints_to_try = [
                "/v1/resort",
                "/resort",
                "/resorts",
            ]
            
            data = None
            for endpoint in endpoints_to_try:
                url = f"{RAPIDAPI_BASE_URL}{endpoint}"
                try:
                    logger.info(f"Trying endpoint: {url}")
                    response = requests.get(
                        url,
                        headers=self.headers,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        logger.info(f"✅ Successfully fetched from {endpoint}")
                        break
                    else:
                        logger.warning(f"Endpoint {endpoint} returned status {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Endpoint {endpoint} failed: {e}")
                    continue
            
            if data is None:
                raise ValueError("Could not fetch data from any endpoint")
            
            # Convert to DataFrame based on response structure
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try common keys
                for key in ['resorts', 'data', 'results', 'resort']:
                    if key in data:
                        df = pd.DataFrame(data[key])
                        break
                else:
                    # If no common key found, treat the whole dict as one record
                    df = pd.DataFrame([data])
            else:
                logger.error(f"Unexpected API response structure: {type(data)}")
                raise ValueError("Unexpected API response format")
            
            logger.info(f"Successfully fetched data for {len(df)} resorts")
            
            # Filter for Colorado resorts
            df = self._filter_colorado_resorts(df)
            logger.info(f"Filtered to {len(df)} Colorado resorts")
            
            # Process and standardize the data
            df_processed = self._process_resort_data(df)
            
            return df_processed
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from RapidAPI: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing resort data: {e}")
            raise
    
    def _filter_colorado_resorts(self, df):
        """
        Filter dataframe to only Colorado resorts
        
        Args:
            df: DataFrame with all resorts
            
        Returns:
            DataFrame with only Colorado resorts
        """
        # Check different possible column names for location
        location_columns = ['state', 'region', 'location', 'province', 'country']
        
        for col in location_columns:
            if col in df.columns:
                # Filter for Colorado
                colorado_mask = df[col].astype(str).str.contains('CO|Colorado|colorado', case=False, na=False)
                if colorado_mask.any():
                    logger.info(f"Filtering by column '{col}'")
                    return df[colorado_mask].copy()
        
        # If no location column found, return all (and log warning)
        logger.warning("Could not identify location column - returning all resorts")
        return df
    
    def _process_resort_data(self, df):
        """
        Process raw API data into standardized format
        
        Args:
            df: Raw DataFrame from API
            
        Returns:
            pandas.DataFrame: Processed data with standardized columns
        """
        try:
            # Create a copy to avoid modifying original
            df = df.copy()
            
            # TODO: Adjust column mappings based on actual API response
            # This is a template - update based on test_skiapi.py results
            
            # Standardized column mapping
            column_mapping = {
                # Location info
                'name': 'resort_name',
                'lat': 'latitude',
                'lon': 'longitude',
                'lng': 'longitude',
                
                # Snow conditions
                'baseDepth': 'base_depth',
                'summitDepth': 'summit_depth',
                'newSnow24h': 'new_snow_24h',
                'newSnow48h': 'new_snow_48h',
                'newSnow7d': 'new_snow_7d',
                
                # Lift/Run status
                'liftsOpen': 'lifts_open',
                'liftsTotal': 'lifts_total',
                'runsOpen': 'runs_open',
                'runsTotal': 'runs_total',
                
                # Conditions
                'status': 'status',
                'conditions': 'conditions',
                'lastUpdated': 'last_updated',
            }
            
            # Rename columns that exist
            existing_mappings = {k: v for k, v in column_mapping.items() if k in df.columns}
            df = df.rename(columns=existing_mappings)
            
            # Ensure required columns exist (create with None if missing)
            required_columns = [
                'resort_name', 'latitude', 'longitude',
                'base_depth', 'summit_depth',
                'new_snow_24h', 'new_snow_48h', 'new_snow_7d',
                'lifts_open', 'lifts_total',
                'runs_open', 'runs_total',
                'status', 'conditions'
            ]
            
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
                    logger.warning(f"Column '{col}' not found in API data, setting to None")
            
            # Data cleaning and type conversion
            
            # Remove resorts without coordinates
            df = df.dropna(subset=['latitude', 'longitude'])
            
            # Convert numeric columns
            numeric_cols = [
                'base_depth', 'summit_depth',
                'new_snow_24h', 'new_snow_48h', 'new_snow_7d',
                'lifts_open', 'lifts_total', 'runs_open', 'runs_total'
            ]
            
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Add calculated fields
            df['lifts_open_pct'] = (df['lifts_open'] / df['lifts_total'] * 100).round(0)
            df['runs_open_pct'] = (df['runs_open'] / df['runs_total'] * 100).round(0)
            
            # Handle infinities from division by zero
            df['lifts_open_pct'] = df['lifts_open_pct'].replace([float('inf'), -float('inf')], 0)
            df['runs_open_pct'] = df['runs_open_pct'].replace([float('inf'), -float('inf')], 0)
            
            # Add update timestamp
            df['data_fetched_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Sort by resort name
            df = df.sort_values('resort_name')
            
            logger.info(f"Processed {len(df)} Colorado resorts")
            
            return df
            
        except Exception as e:
            logger.error(f"Error in _process_resort_data: {e}")
            raise
    
    def get_summary_stats(self, df):
        """
        Calculate summary statistics for logging/monitoring
        
        Args:
            df: Processed resort DataFrame
            
        Returns:
            dict: Summary statistics
        """
        stats = {
            'total_resorts': len(df),
            'resorts_open': len(df[df['status'] != 'Closed']),
            'avg_base_depth': df['base_depth'].mean(),
            'max_new_snow_24h': df['new_snow_24h'].max(),
            'total_lifts_open': df['lifts_open'].sum(),
        }
        
        logger.info("Summary Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        
        return stats


def fetch_and_save_data():
    """
    Main function to fetch data and save to CSV (for testing)
    """
    logger.info("=" * 60)
    logger.info("Starting ski resort data fetch")
    logger.info("=" * 60)
    
    try:
        fetcher = SkiAPIFetcher()
        df = fetcher.fetch_colorado_resorts()
        
        # Get summary stats
        fetcher.get_summary_stats(df)
        
        # Save to CSV for inspection
        output_file = "colorado_resorts_current.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Data saved to {output_file}")
        
        # Display preview
        print("\n" + "=" * 60)
        print("DATA PREVIEW")
        print("=" * 60)
        print(df.head())
        print("\n" + "=" * 60)
        print(f"Total resorts: {len(df)}")
        print("=" * 60)
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch data: {e}")
        raise


if __name__ == "__main__":
    fetch_and_save_data()

