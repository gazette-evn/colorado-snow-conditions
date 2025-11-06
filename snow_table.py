#!/usr/bin/env python3
"""
Snow Conditions Table Updater
Updates Datawrapper table with sortable Colorado ski resort data
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
        logging.FileHandler("snow_table.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API credentials
DATAWRAPPER_API_KEY = os.environ.get("DATAWRAPPER_API_KEY")
SNOW_TABLE_CHART_ID = os.environ.get("SNOW_TABLE_CHART_ID")

# Initialize Datawrapper client
dw = datawrapper.Datawrapper(access_token=DATAWRAPPER_API_KEY)

def prepare_table_data(df):
    """
    Prepare resort data for table visualization
    
    Args:
        df: DataFrame from ski_api_fetcher
        
    Returns:
        pandas.DataFrame: Table-ready data with clean column names
    """
    try:
        logger.info("Preparing data for table visualization")
        
        # Create a copy
        table_df = df.copy()
        
        # Select and rename columns for table
        table_df = table_df[[
            'resort_name',
            'new_snow_24h',
            'new_snow_48h', 
            'new_snow_7d',
            'base_depth',
            'summit_depth',
            'lifts_open',
            'lifts_total',
            'lifts_open_pct',
            'runs_open',
            'runs_total',
            'runs_open_pct',
            'status',
            'conditions'
        ]].copy()
        
        # Rename columns to be user-friendly
        table_df = table_df.rename(columns={
            'resort_name': 'Resort',
            'new_snow_24h': '24h Snow (in)',
            'new_snow_48h': '48h Snow (in)',
            'new_snow_7d': '7-Day Snow (in)',
            'base_depth': 'Base Depth (in)',
            'summit_depth': 'Summit Depth (in)',
            'lifts_open': 'Lifts Open',
            'lifts_total': 'Total Lifts',
            'lifts_open_pct': 'Lifts (%)',
            'runs_open': 'Runs Open',
            'runs_total': 'Total Runs',
            'runs_open_pct': 'Runs (%)',
            'status': 'Status',
            'conditions': 'Conditions'
        })
        
        # Convert numeric columns to integers (remove decimals for cleaner display)
        numeric_cols = [
            '24h Snow (in)', '48h Snow (in)', '7-Day Snow (in)',
            'Base Depth (in)', 'Summit Depth (in)',
            'Lifts Open', 'Total Lifts', 'Lifts (%)',
            'Runs Open', 'Total Runs', 'Runs (%)'
        ]
        
        for col in numeric_cols:
            if col in table_df.columns:
                table_df[col] = table_df[col].fillna(0).astype(int)
        
        # Fill NaN in text columns
        table_df['Status'] = table_df['Status'].fillna('Unknown')
        table_df['Conditions'] = table_df['Conditions'].fillna('-')
        
        # Sort by 24h snowfall (descending) - most snow first
        table_df = table_df.sort_values('24h Snow (in)', ascending=False)
        
        logger.info(f"Prepared table data for {len(table_df)} resorts")
        
        return table_df
        
    except Exception as e:
        logger.error(f"Error preparing table data: {e}")
        raise


def update_snow_table():
    """
    Main function to update the Datawrapper snow conditions table
    """
    logger.info("=" * 60)
    logger.info("Starting snow conditions table update")
    logger.info("=" * 60)
    
    try:
        # Check configuration
        if not DATAWRAPPER_API_KEY:
            raise ValueError("DATAWRAPPER_API_KEY not set in .env")
        if not SNOW_TABLE_CHART_ID:
            raise ValueError("SNOW_TABLE_CHART_ID not set in .env")
        
        # Fetch resort data
        logger.info("Fetching resort data...")
        fetcher = SkiAPIFetcher()
        resort_data = fetcher.fetch_colorado_resorts()
        
        # Prepare table data
        table_data = prepare_table_data(resort_data)
        
        # Update table
        logger.info(f"Updating Datawrapper table {SNOW_TABLE_CHART_ID}")
        
        # Upload data
        dw.add_data(SNOW_TABLE_CHART_ID, table_data)
        logger.info(f"✅ Data uploaded: {len(table_data)} resorts")
        
        # Update table metadata
        current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p MT')
        
        dw.update_chart(
            SNOW_TABLE_CHART_ID,
            title="Colorado Ski Resorts - Snow Conditions Table",
            metadata={
                'describe': {
                    'intro': f'Sortable table of current snow conditions for all Colorado ski resorts. Click column headers to sort. Last updated: {current_time}',
                    'source-name': 'skiapi.com',
                    'byline': 'Data updated every 2 hours'
                }
            }
        )
        logger.info("✅ Table metadata updated")
        
        # Republish table
        dw.publish_chart(SNOW_TABLE_CHART_ID)
        logger.info("✅ Table published successfully")
        
        # Summary stats
        top_snow = table_data.nlargest(3, '24h Snow (in)')[['Resort', '24h Snow (in)']]
        
        logger.info("=" * 60)
        logger.info("TABLE UPDATE SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Resorts in table: {len(table_data)}")
        logger.info(f"Chart ID: {SNOW_TABLE_CHART_ID}")
        logger.info(f"Updated: {current_time}")
        logger.info("\nTop 3 Resorts (24h snow):")
        for idx, row in top_snow.iterrows():
            logger.info(f"  {row['Resort']}: {row['24h Snow (in)']}\"")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to update snow table: {e}")
        raise


if __name__ == "__main__":
    update_snow_table()

