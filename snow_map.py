#!/usr/bin/env python3
"""
Snow Conditions Map Updater
Updates Datawrapper map with current Colorado ski resort conditions
"""

import os
import pandas as pd
import datawrapper
import logging
from datetime import datetime
from dotenv import load_dotenv
from ski_api_fetcher import SkiAPIFetcher

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("snow_map.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API credentials
DATAWRAPPER_API_KEY = os.environ.get("DATAWRAPPER_API_KEY")
SNOW_MAP_CHART_ID = os.environ.get("SNOW_MAP_CHART_ID")

# Initialize Datawrapper client
dw = datawrapper.Datawrapper(access_token=DATAWRAPPER_API_KEY)

def prepare_map_data(df):
    """
    Prepare resort data for map visualization
    
    Args:
        df: DataFrame from ski_api_fetcher
        
    Returns:
        pandas.DataFrame: Map-ready data with lat/lng and tooltip fields
    """
    try:
        logger.info("Preparing data for map visualization")
        
        # Create a copy
        map_df = df.copy()
        
        # Rename coordinates for Datawrapper
        if 'latitude' in map_df.columns and 'longitude' in map_df.columns:
            map_df = map_df.rename(columns={
                'latitude': 'lat',
                'longitude': 'lng'
            })
        
        # Remove resorts without coordinates
        map_df = map_df.dropna(subset=['lat', 'lng'])
        
        # Create human-readable tooltip fields
        
        # Format snow depth
        map_df['base_depth_display'] = map_df['base_depth'].apply(
            lambda x: f"{int(x)}\"" if pd.notna(x) and x > 0 else "N/A"
        )
        
        map_df['summit_depth_display'] = map_df['summit_depth'].apply(
            lambda x: f"{int(x)}\"" if pd.notna(x) and x > 0 else "N/A"
        )
        
        # Format new snow
        map_df['new_snow_24h_display'] = map_df['new_snow_24h'].apply(
            lambda x: f"{int(x)}\"" if pd.notna(x) and x > 0 else "0\""
        )
        
        map_df['new_snow_48h_display'] = map_df['new_snow_48h'].apply(
            lambda x: f"{int(x)}\"" if pd.notna(x) and x > 0 else "0\""
        )
        
        # Format lifts/runs status
        map_df['lifts_status'] = map_df.apply(
            lambda row: f"{int(row['lifts_open'])}/{int(row['lifts_total'])}" 
            if pd.notna(row['lifts_open']) and pd.notna(row['lifts_total']) 
            else "N/A",
            axis=1
        )
        
        map_df['runs_status'] = map_df.apply(
            lambda row: f"{int(row['runs_open'])}/{int(row['runs_total'])}" 
            if pd.notna(row['runs_open']) and pd.notna(row['runs_total']) 
            else "N/A",
            axis=1
        )
        
        # Status emoji/indicator
        status_map = {
            'Open': '🟢 Open',
            'Closed': '🔴 Closed',
            'Limited': '🟡 Limited',
        }
        map_df['status_display'] = map_df['status'].apply(
            lambda x: status_map.get(str(x), str(x)) if pd.notna(x) else 'Unknown'
        )
        
        # Select columns for map
        map_columns = [
            'lat', 'lng', 'resort_name',
            'base_depth_display', 'summit_depth_display',
            'new_snow_24h_display', 'new_snow_48h_display',
            'lifts_status', 'runs_status',
            'status_display', 'conditions'
        ]
        
        # Keep only columns that exist
        map_columns = [col for col in map_columns if col in map_df.columns]
        map_df = map_df[map_columns]
        
        logger.info(f"Prepared map data for {len(map_df)} resorts")
        
        return map_df
        
    except Exception as e:
        logger.error(f"Error preparing map data: {e}")
        raise


def create_tooltip_template():
    """
    Create HTML tooltip template for map markers
    
    Returns:
        str: HTML template string
    """
    template = """
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.4; min-width: 200px;">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: #2c3e50;">
            {{ resort_name }}
        </div>
        
        <div style="margin-bottom: 6px;">
            <span style="font-weight: 600;">Status:</span> {{ status_display }}
        </div>
        
        <div style="border-top: 1px solid #e0e0e0; margin: 8px 0; padding-top: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">New Snow (24h):</span>
                <span style="color: #3498db; font-weight: bold;">{{ new_snow_24h_display }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">New Snow (48h):</span>
                <span style="color: #3498db;">{{ new_snow_48h_display }}</span>
            </div>
        </div>
        
        <div style="border-top: 1px solid #e0e0e0; margin: 8px 0; padding-top: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">Base Depth:</span>
                <span>{{ base_depth_display }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">Summit Depth:</span>
                <span>{{ summit_depth_display }}</span>
            </div>
        </div>
        
        <div style="border-top: 1px solid #e0e0e0; margin: 8px 0; padding-top: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">Lifts Open:</span>
                <span>{{ lifts_status }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">Runs Open:</span>
                <span>{{ runs_status }}</span>
            </div>
        </div>
        
        {{ #if conditions }}
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e0e0e0; font-style: italic; color: #555;">
            {{ conditions }}
        </div>
        {{ /if }}
    </div>
    """
    return template


def update_snow_map():
    """
    Main function to update the Datawrapper snow conditions map
    """
    logger.info("=" * 60)
    logger.info("Starting snow conditions map update")
    logger.info("=" * 60)
    
    try:
        # Check configuration
        if not DATAWRAPPER_API_KEY:
            raise ValueError("DATAWRAPPER_API_KEY not set in .env")
        if not SNOW_MAP_CHART_ID:
            raise ValueError("SNOW_MAP_CHART_ID not set in .env")
        
        # Fetch resort data
        logger.info("Fetching resort data...")
        fetcher = SkiAPIFetcher()
        resort_data = fetcher.fetch_colorado_resorts()
        
        # Prepare map data
        map_data = prepare_map_data(resort_data)
        
        # Update map
        logger.info(f"Updating Datawrapper map {SNOW_MAP_CHART_ID}")
        
        # Upload data
        dw.add_data(SNOW_MAP_CHART_ID, map_data)
        logger.info(f"✅ Data uploaded: {len(map_data)} resort markers")
        
        # Update map metadata
        current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p MT')
        
        dw.update_chart(
            SNOW_MAP_CHART_ID,
            title="Colorado Ski Resort Conditions - Live Snow Report",
            metadata={
                'describe': {
                    'intro': f'Current snow conditions, lift status, and terrain reports for all Colorado ski resorts. Last updated: {current_time}',
                    'source-name': 'skiapi.com',
                    'byline': 'Data updated every 2 hours'
                },
                'visualize': {
                    'tooltip': {
                        'body': create_tooltip_template()
                    }
                }
            }
        )
        logger.info("✅ Map metadata updated")
        
        # Republish map
        dw.publish_chart(SNOW_MAP_CHART_ID)
        logger.info("✅ Map published successfully")
        
        # Summary
        logger.info("=" * 60)
        logger.info("MAP UPDATE SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Resorts displayed: {len(map_data)}")
        logger.info(f"Chart ID: {SNOW_MAP_CHART_ID}")
        logger.info(f"Updated: {current_time}")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to update snow map: {e}")
        raise


if __name__ == "__main__":
    update_snow_map()

