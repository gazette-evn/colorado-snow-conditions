#!/usr/bin/env python3
"""
Combined Colorado Ski Resort Scraper
Uses OnTheSnow as primary source, supplements with CSCUSA for any missing resorts
Adds coordinates from known resort locations
"""

import pandas as pd
import logging
from datetime import datetime
from onthesnow_scraper import OnTheSnowScraper
from colorado_ski_scraper import ColoradoSkiScraper

# Colorado resort coordinates (from original manual data + additions)
RESORT_COORDINATES = {
    'Arapahoe Basin': {'lat': 39.634108, 'lng': -105.87147},
    'Arapahoe Basin Ski Area': {'lat': 39.634108, 'lng': -105.87147},  # Same as A-Basin
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
    'Loveland Ski Area': {'lat': 39.6775332, 'lng': -105.90536},  # Same as Loveland
    'Monarch': {'lat': 38.5120635, 'lng': -106.33197},
    'Powderhorn': {'lat': 39.0693741, 'lng': -108.15071},
    'Purgatory': {'lat': 37.6276821, 'lng': -107.83761},
    'Purgatory Resort': {'lat': 37.6276821, 'lng': -107.83761},  # Same as Purgatory
    'Silverton': {'lat': 37.884608, 'lng': -107.66592},
    'Snowmass': {'lat': 39.2130418, 'lng': -106.93782},
    'Steamboat': {'lat': 40.4537983, 'lng': -106.77088},
    'Sunlight': {'lat': 39.3997821, 'lng': -107.33876},
    'Telluride': {'lat': 37.9166674, 'lng': -107.83748},
    'Vail': {'lat': 39.6061444, 'lng': -106.35497},
    'Winter Park': {'lat': 39.8627761, 'lng': -105.77874},
    'Wolf Creek': {'lat': 37.4717059, 'lng': -106.78829},
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("combined_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def add_coordinates(df):
    """Add latitude and longitude to resorts based on name matching"""
    
    def find_coordinates(name):
        """Find coordinates for a resort by name"""
        name_clean = name.strip().lower()
        
        # Try exact match first
        if name in RESORT_COORDINATES:
            coords = RESORT_COORDINATES[name]
            return pd.Series([coords['lat'], coords['lng']])
        
        # Try partial matching
        for resort_name, coords in RESORT_COORDINATES.items():
            if resort_name.lower() in name_clean or name_clean in resort_name.lower():
                return pd.Series([coords['lat'], coords['lng']])
        
        # No match found
        logger.warning(f"⚠️ No coordinates found for: {name}")
        return pd.Series([None, None])
    
    df[['latitude', 'longitude']] = df['name'].apply(find_coordinates)
    
    # Log resorts without coordinates
    missing = df[df['latitude'].isna()]
    if len(missing) > 0:
        logger.warning(f"Missing coordinates for {len(missing)} resorts:")
        for name in missing['name']:
            logger.warning(f"  - {name}")
    else:
        logger.info(f"✅ Added coordinates to all {len(df)} resorts")
    
    return df


def combine_resort_data():
    """
    Scrape from both sources and combine
    OnTheSnow is primary, CSCUSA supplements
    """
    logger.info("="*70)
    logger.info("COMBINED SCRAPER - OnTheSnow + CSCUSA")
    logger.info("="*70)
    
    all_resorts = []
    
    # 1. Get OnTheSnow data (primary source)
    logger.info("\n📊 Step 1: Scraping OnTheSnow (primary source)...")
    try:
        ots_scraper = OnTheSnowScraper(headless=True)
        ots_df = ots_scraper.scrape()
        
        if not ots_df.empty:
            logger.info(f"✅ OnTheSnow: Found {len(ots_df)} resorts")
            all_resorts.append(ots_df)
            ots_resort_names = set(ots_df['name'].str.lower())
        else:
            logger.warning("⚠️ OnTheSnow returned no data")
            ots_resort_names = set()
            
    except Exception as e:
        logger.error(f"❌ OnTheSnow scraper failed: {e}")
        ots_resort_names = set()
    
    # 2. Get CSCUSA data (supplement)
    logger.info("\n📊 Step 2: Scraping CSCUSA (supplement)...")
    try:
        cscusa_scraper = ColoradoSkiScraper(headless=True)
        cscusa_df = cscusa_scraper.scrape()
        
        if not cscusa_df.empty:
            logger.info(f"✅ CSCUSA: Found {len(cscusa_df)} resorts")
            
            # Only add resorts NOT in OnTheSnow
            cscusa_df['name_lower'] = cscusa_df['name'].str.lower()
            new_resorts = cscusa_df[~cscusa_df['name_lower'].isin(ots_resort_names)]
            
            if len(new_resorts) > 0:
                logger.info(f"📝 CSCUSA adds {len(new_resorts)} new resorts:")
                for name in new_resorts['name']:
                    logger.info(f"  + {name}")
                
                # Standardize columns to match OnTheSnow
                new_resorts = new_resorts.copy()
                new_resorts['source'] = 'CSCUSA'
                all_resorts.append(new_resorts)
            else:
                logger.info("ℹ️ CSCUSA had no additional resorts (all already in OnTheSnow)")
        else:
            logger.warning("⚠️ CSCUSA returned no data")
            
    except Exception as e:
        logger.error(f"❌ CSCUSA scraper failed: {e}")
    
    # 3. Combine all data
    if not all_resorts:
        logger.error("❌ No data from any source!")
        return pd.DataFrame()
    
    combined_df = pd.concat(all_resorts, ignore_index=True)
    
    # Remove duplicate resorts (keep first occurrence = OnTheSnow priority)
    combined_df = combined_df.drop_duplicates(subset=['name'], keep='first')
    
    # 4. Add coordinates
    logger.info("\n📍 Adding resort coordinates...")
    combined_df = add_coordinates(combined_df)
    
    # Sort by name
    combined_df = combined_df.sort_values('name').reset_index(drop=True)
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("FINAL COMBINED RESULTS")
    logger.info("="*70)
    logger.info(f"Total unique resorts: {len(combined_df)}")
    logger.info(f"From OnTheSnow: {len(combined_df[combined_df['source'] == 'OnTheSnow'])}")
    logger.info(f"From CSCUSA: {len(combined_df[combined_df['source'] == 'CSCUSA'])}")
    
    return combined_df


def main():
    """Test the combined scraper"""
    df = combine_resort_data()
    
    if df.empty:
        logger.error("No data collected")
        return
    
    # Save combined data
    output_file = "colorado_resorts_combined.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"\n✅ Saved combined data to {output_file}")
    
    # Display results
    print("\n" + "="*70)
    print("ALL COLORADO RESORTS")
    print("="*70)
    for idx, row in df.iterrows():
        status_emoji = "🟢" if row['status'] == 'Open' else "🔴"
        source = f"({row['source']})"
        print(f"{idx+1:2d}. {status_emoji} {row['name']:30s} {source}")
    print("="*70)
    print(f"Total: {len(df)} resorts")


if __name__ == "__main__":
    main()

