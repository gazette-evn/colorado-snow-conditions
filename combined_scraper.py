#!/usr/bin/env python3
"""
Combined Colorado Ski Resort Scraper
Uses OnTheSnow as primary source, supplements with CSCUSA for any missing resorts
Adds coordinates from known resort locations
"""

import pandas as pd
import logging
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from onthesnow_scraper import OnTheSnowScraper
from colorado_ski_scraper import ColoradoSkiScraper
from aspen_snowmass_scraper import AspenSnowmassScraper

# Set to skip individual page visits for faster execution (e.g., in CI)
SKIP_DETAIL_PAGES = os.environ.get('SKIP_DETAIL_PAGES', 'false').lower() == 'true'

# Colorado resort coordinates and trail counts
# Trail counts from user's manual data CSV (Colorado Ski Area Data - Sheet1.csv)
# Lift counts estimated from resort data
RESORT_DATA = {
    'Arapahoe Basin': {'lat': 39.634108, 'lng': -105.87147, 'total_trails': 147, 'total_lifts': 9},
    'Arapahoe Basin Ski Area': {'lat': 39.634108, 'lng': -105.87147, 'total_trails': 147, 'total_lifts': 9},
    'Aspen Highlands': {'lat': 39.1820055, 'lng': -106.8564, 'total_trails': 116, 'total_lifts': 5},
    'Aspen Mountain': {'lat': 39.1862685, 'lng': -106.81821, 'total_trails': 104, 'total_lifts': 8},
    'Beaver Creek': {'lat': 39.6016505, 'lng': -106.53161, 'total_trails': 176, 'total_lifts': 25},
    'Breckenridge': {'lat': 39.4782643, 'lng': -106.07232, 'total_trails': 193, 'total_lifts': 35},
    'Buttermilk': {'lat': 39.2058029, 'lng': -106.86107, 'total_trails': 44, 'total_lifts': 8},
    'Cooper': {'lat': 39.3601951, 'lng': -106.30145, 'total_trails': 65, 'total_lifts': 5},
    'Copper Mountain': {'lat': 39.5004501, 'lng': -106.15578, 'total_trails': 159, 'total_lifts': 24},
    'Crested Butte': {'lat': 38.8991036, 'lng': -106.96576, 'total_trails': 168, 'total_lifts': 16},
    'Echo Mountain': {'lat': 39.6845817, 'lng': -105.51939, 'total_trails': 7, 'total_lifts': 3},
    'Eldora': {'lat': 39.9372203, 'lng': -105.58268, 'total_trails': 62, 'total_lifts': 12},
    'Granby Ranch': {'lat': 40.0446489, 'lng': -105.90633, 'total_trails': 54, 'total_lifts': 5},
    'Hesperus': {'lat': 37.2991673, 'lng': -108.05513, 'total_trails': 26, 'total_lifts': 2},
    'Howelsen Hill': {'lat': 40.4833683, 'lng': -106.83797, 'total_trails': 17, 'total_lifts': 3},
    'Kendall Mountain': {'lat': 37.8111854, 'lng': -107.65682, 'total_trails': 7, 'total_lifts': 2},
    'Keystone': {'lat': 39.5816989, 'lng': -105.94367, 'total_trails': 142, 'total_lifts': 21},
    'Loveland': {'lat': 39.6775332, 'lng': -105.90536, 'total_trails': 94, 'total_lifts': 10},
    'Loveland Ski Area': {'lat': 39.6775332, 'lng': -105.90536, 'total_trails': 94, 'total_lifts': 10},
    'Monarch': {'lat': 38.5120635, 'lng': -106.33197, 'total_trails': 67, 'total_lifts': 7},
    'Powderhorn': {'lat': 39.0693741, 'lng': -108.15071, 'total_trails': 57, 'total_lifts': 4},
    'Purgatory': {'lat': 37.6276821, 'lng': -107.83761, 'total_trails': 107, 'total_lifts': 11},
    'Purgatory Resort': {'lat': 37.6276821, 'lng': -107.83761, 'total_trails': 107, 'total_lifts': 11},
    'Silverton': {'lat': 37.884608, 'lng': -107.66592, 'total_trails': 0, 'total_lifts': 2},  # No trail count in manual data
    'Snowmass': {'lat': 39.2130418, 'lng': -106.93782, 'total_trails': 98, 'total_lifts': 21},
    'Steamboat': {'lat': 40.4537983, 'lng': -106.77088, 'total_trails': 184, 'total_lifts': 18},
    'Sunlight': {'lat': 39.3997821, 'lng': -107.33876, 'total_trails': 77, 'total_lifts': 4},
    'Telluride': {'lat': 37.9166674, 'lng': -107.83748, 'total_trails': 149, 'total_lifts': 19},
    'Vail': {'lat': 39.6061444, 'lng': -106.35497, 'total_trails': 277, 'total_lifts': 31},
    'Winter Park': {'lat': 39.8627761, 'lng': -105.77874, 'total_trails': 171, 'total_lifts': 24},
    'Wolf Creek': {'lat': 37.4717059, 'lng': -106.78829, 'total_trails': 133, 'total_lifts': 7},
}

# Max snowfall cap to handle data errors (inches)
MAX_24H_SNOWFALL = 12

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


def add_resort_data(df):
    """Add latitude, longitude, trail counts, and lift counts to resorts"""
    
    def find_resort_data(name):
        """Find complete resort data by name"""
        name_clean = name.strip().lower()
        
        # Try exact match first
        if name in RESORT_DATA:
            data = RESORT_DATA[name]
            return pd.Series([data['lat'], data['lng'], data['total_trails'], data['total_lifts']])
        
        # Try partial matching
        for resort_name, data in RESORT_DATA.items():
            if resort_name.lower() in name_clean or name_clean in resort_name.lower():
                return pd.Series([data['lat'], data['lng'], data['total_trails'], data['total_lifts']])
        
        # No match found
        logger.warning(f"⚠️ No resort data found for: {name}")
        return pd.Series([None, None, None, None])
    
    # Add coordinates and trail/lift totals
    df[['latitude', 'longitude', 'total_trails_manual', 'total_lifts_manual']] = df['name'].apply(find_resort_data)
    
    # Fill in missing total_trails and total_lifts from manual data
    df['total_trails'] = df['total_trails'].fillna(df['total_trails_manual'])
    df['total_lifts'] = df['total_lifts'].fillna(df['total_lifts_manual'])
    
    # Drop the temporary manual columns
    df = df.drop(columns=['total_trails_manual', 'total_lifts_manual'], errors='ignore')
    
    # Calculate percentages
    df['trails_open_pct'] = 0.0
    df['lifts_open_pct'] = 0.0
    
    # Calculate trails open percentage
    valid_trails = (df['total_trails'].notna()) & (df['total_trails'] > 0) & (df['open_trails'].notna())
    df.loc[valid_trails, 'trails_open_pct'] = (df.loc[valid_trails, 'open_trails'] / df.loc[valid_trails, 'total_trails'] * 100).round(1)
    
    # Calculate lifts open percentage
    valid_lifts = (df['total_lifts'].notna()) & (df['total_lifts'] > 0) & (df['open_lifts'].notna())
    df.loc[valid_lifts, 'lifts_open_pct'] = (df.loc[valid_lifts, 'open_lifts'] / df.loc[valid_lifts, 'total_lifts'] * 100).round(1)
    
    # Log resorts without coordinates
    missing = df[df['latitude'].isna()]
    if len(missing) > 0:
        logger.warning(f"Missing data for {len(missing)} resorts:")
        for name in missing['name']:
            logger.warning(f"  - {name}")
    else:
        logger.info(f"✅ Added complete data to all {len(df)} resorts")
    
    return df


def add_missing_major_resorts(df):
    """Add major resorts that aren't scraped yet but should appear on the map"""
    
    # Major resorts to always include (even if closed/not scraped)
    must_include = ['Vail', 'Beaver Creek', 'Crested Butte', 'Wolf Creek']
    
    existing_names = df['name'].str.lower().tolist()
    existing_normalized = [name.replace(' ski area', '').replace(' resort', '').replace(' mountain', '').strip() 
                          for name in existing_names]
    
    missing_resorts = []
    
    for resort_name in must_include:
        # Check if resort is already in the data (by normalized name)
        resort_normalized = resort_name.lower()
        if not any(resort_normalized in existing for existing in existing_normalized):
            # Resort is missing - add it as placeholder
            if resort_name in RESORT_DATA:
                data = RESORT_DATA[resort_name]
                missing_resorts.append({
                    'name': resort_name,
                    'status': 'Closed',
                    'new_snow_24h': 0,
                    'new_snow_48h': 0,
                    'base_depth': 0,
                    'trails_open': '0/0',
                    'lifts_open': '0/0',
                    'data_fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'Manual Entry',
                    'open_lifts': 0,
                    'total_lifts': data['total_lifts'],
                    'open_trails': 0,
                    'total_trails': data['total_trails'],
                    'mid_mtn_depth': 0,
                    'surface_conditions': '',
                    'name_lower': resort_name.lower(),
                    'latitude': data['lat'],
                    'longitude': data['lng'],
                    'trails_open_pct': 0.0,
                    'lifts_open_pct': 0.0,
                })
                logger.info(f"  + Added placeholder for {resort_name} ({data['total_trails']} trails)")
    
    if missing_resorts:
        missing_df = pd.DataFrame(missing_resorts)
        df = pd.concat([df, missing_df], ignore_index=True)
        logger.info(f"✅ Added {len(missing_resorts)} missing major resorts")
    else:
        logger.info("✅ All major resorts already present")
    
    return df


def scrape_onthesnow():
    """Scrape OnTheSnow data (runs in parallel)"""
    logger.info("📊 [PARALLEL] Scraping OnTheSnow (primary source)...")
    try:
        ots_scraper = OnTheSnowScraper(headless=True, skip_detail_pages=SKIP_DETAIL_PAGES)
        ots_df = ots_scraper.scrape()

        if not ots_df.empty:
            # Filter out aggregated "Aspen Snowmass" entry to avoid double pins
            aspen_mask = ots_df['name'].str.contains('Aspen Snowmass', case=False, na=False)
            if aspen_mask.any():
                logger.info(f"🗑️ Filtering out aggregated 'Aspen Snowmass' from OnTheSnow")
                ots_df = ots_df[~aspen_mask].copy()

            # Apply snowfall sanity check
            high_snow_mask = ots_df['new_snow_24h'] > MAX_24H_SNOWFALL
            if high_snow_mask.any():
                for idx, row in ots_df[high_snow_mask].iterrows():
                    logger.warning(f"⚠️ High snowfall detected for {row['name']}: {row['new_snow_24h']}\". Capping at {MAX_24H_SNOWFALL}\".")
                ots_df.loc[high_snow_mask, 'new_snow_24h'] = MAX_24H_SNOWFALL

            logger.info(f"✅ OnTheSnow: Found {len(ots_df)} resorts")
            return ('onthesnow', ots_df)
        else:
            logger.warning("⚠️ OnTheSnow returned no data")
            return ('onthesnow', pd.DataFrame())

    except Exception as e:
        logger.error(f"❌ OnTheSnow scraper failed: {e}")
        return ('onthesnow', pd.DataFrame())


def scrape_cscusa():
    """Scrape CSCUSA data (runs in parallel)"""
    logger.info("📊 [PARALLEL] Scraping CSCUSA (supplement)...")
    try:
        cscusa_scraper = ColoradoSkiScraper(headless=True)
        cscusa_df = cscusa_scraper.scrape()

        if not cscusa_df.empty:
            logger.info(f"✅ CSCUSA: Found {len(cscusa_df)} resorts")
            return ('cscusa', cscusa_df)
        else:
            logger.warning("⚠️ CSCUSA returned no data")
            return ('cscusa', pd.DataFrame())

    except Exception as e:
        logger.error(f"❌ CSCUSA scraper failed: {e}")
        return ('cscusa', pd.DataFrame())


def scrape_aspen():
    """Scrape Aspen Official data (runs in parallel)"""
    logger.info("📊 [PARALLEL] Scraping Aspen Official (granular snow supplement)...")
    try:
        aspen_scraper = AspenSnowmassScraper(headless=True)
        aspen_df = aspen_scraper.scrape()
        if not aspen_df.empty:
            logger.info(f"✅ Aspen Official: Found {len(aspen_df)} mountains")
            return ('aspen', aspen_df)
        else:
            logger.warning("⚠️ Aspen Official returned no data")
            return ('aspen', pd.DataFrame())
    except Exception as e:
        logger.error(f"❌ Aspen Official scraper failed: {e}")
        return ('aspen', pd.DataFrame())


def combine_resort_data():
    """
    Scrape from all sources IN PARALLEL and combine
    OnTheSnow is primary, CSCUSA supplements, Aspen provides granular data
    """
    logger.info("="*70)
    logger.info("COMBINED SCRAPER - PARALLEL MODE")
    logger.info("="*70)
    if SKIP_DETAIL_PAGES:
        logger.info("⚡ SKIP_DETAIL_PAGES=true - skipping individual resort page visits for speed")

    all_resorts = []
    ots_df = pd.DataFrame()
    cscusa_df = pd.DataFrame()
    aspen_official_data = {}

    # Run all three scrapers in parallel
    logger.info("\n🚀 Starting parallel scraping of all data sources...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(scrape_onthesnow): 'OnTheSnow',
            executor.submit(scrape_cscusa): 'CSCUSA',
            executor.submit(scrape_aspen): 'Aspen'
        }

        for future in as_completed(futures):
            source_name = futures[future]
            try:
                source_key, df = future.result(timeout=300)  # 5 min timeout per scraper

                if source_key == 'onthesnow' and not df.empty:
                    ots_df = df
                    all_resorts.append(df)
                elif source_key == 'cscusa' and not df.empty:
                    cscusa_df = df
                elif source_key == 'aspen' and not df.empty:
                    for _, row in df.iterrows():
                        aspen_official_data[row['name']] = row.to_dict()

                logger.info(f"✅ {source_name} completed")
            except Exception as e:
                logger.error(f"❌ {source_name} failed: {e}")

    logger.info("\n📊 Processing CSCUSA supplement data...")
    # Now process CSCUSA data - only add resorts NOT in OnTheSnow
    if not cscusa_df.empty:
        ots_resort_names = set(ots_df['name'].str.lower()) if not ots_df.empty else set()
        cscusa_df['name_lower'] = cscusa_df['name'].str.lower()
        new_resorts = cscusa_df[~cscusa_df['name_lower'].isin(ots_resort_names)]

        if len(new_resorts) > 0:
            # Apply snowfall sanity check to CSCUSA data too
            high_snow_mask = new_resorts['new_snow_24h'] > MAX_24H_SNOWFALL
            if high_snow_mask.any():
                for idx, row in new_resorts[high_snow_mask].iterrows():
                    logger.warning(f"⚠️ High snowfall detected for {row['name']} (CSCUSA): {row['new_snow_24h']}\". Capping at {MAX_24H_SNOWFALL}\".")
                new_resorts = new_resorts.copy()
                new_resorts.loc[high_snow_mask, 'new_snow_24h'] = MAX_24H_SNOWFALL

            logger.info(f"📝 CSCUSA adds {len(new_resorts)} new resorts:")
            for name in new_resorts['name']:
                logger.info(f"  + {name}")

            new_resorts = new_resorts.copy()
            new_resorts['source'] = 'CSCUSA'
            all_resorts.append(new_resorts)
        else:
            logger.info("ℹ️ CSCUSA had no additional resorts (all already in OnTheSnow)")

    # 4. Combine all data
    if not all_resorts:
        logger.error("❌ No data from any source!")
        return pd.DataFrame()
    
    combined_df = pd.concat(all_resorts, ignore_index=True)
    
    # Remove duplicate resorts with better deduplication logic
    def normalize_name(name):
        """Normalize resort names for duplicate detection"""
        name = name.lower().strip()
        # Remove common suffixes
        name = name.replace(' ski area', '').replace(' ski resort', '')
        name = name.replace(' resort', '').replace(' mountain resort', '')
        name = name.replace(' mountain', '')
        return name
    
    combined_df['name_normalized'] = combined_df['name'].apply(normalize_name)
    
    # Sort to prioritize OnTheSnow/CSCUSA for terrain data
    combined_df = combined_df.drop_duplicates(subset=['name_normalized'], keep='first')
    
    # 5. PATCH ASPEN DATA: Overwrite all stats with official data if we have it
    for idx, row in combined_df.iterrows():
        name = row['name']
        # Check if this name (or normalized version) is in our official Aspen data
        official_match = None
        if name in aspen_official_data:
            official_match = aspen_official_data[name]
        else:
            # Try matching by normalized name for Aspen resorts
            for a_name, a_data in aspen_official_data.items():
                if normalize_name(a_name) == normalize_name(name):
                    official_match = a_data
                    break
        
        if official_match:
            logger.info(f"💉 Patching {name} with 100% verified official data")
            # Overwrite EVERYTHING from the official source
            for key, value in official_match.items():
                combined_df.at[idx, key] = value
            combined_df.at[idx, 'source'] = "Aspen Official"

    combined_df = combined_df.drop(columns=['name_normalized'])
    
    # 6. Add coordinates, trail counts, and calculate percentages
    logger.info("\n📍 Adding resort data (coordinates, trail counts, percentages)...")
    combined_df = add_resort_data(combined_df)
    
    # 7. Add missing major resorts (not yet scraped but should be shown)
    logger.info("\n➕ Checking for missing major resorts...")
    combined_df = add_missing_major_resorts(combined_df)
    
    # Sort by name
    combined_df = combined_df.sort_values('name').reset_index(drop=True)
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("FINAL COMBINED RESULTS")
    logger.info("="*70)
    logger.info(f"Total unique resorts: {len(combined_df)}")
    
    if 'source' in combined_df.columns:
        ots_count = len(combined_df[combined_df['source'].str.contains('OnTheSnow', na=False)])
        aspen_count = len(combined_df[combined_df['source'].str.contains('Aspen Official', na=False)])
        cscusa_count = len(combined_df[combined_df['source'].str.contains('CSCUSA', na=False)])
        logger.info(f"From OnTheSnow: {ots_count}")
        logger.info(f"From Aspen Official: {aspen_count}")
        logger.info(f"From CSCUSA: {cscusa_count}")
    
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
