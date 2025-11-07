#!/usr/bin/env python3
"""
Combined Colorado Ski Resort Scraper
Uses OnTheSnow as primary source, supplements with CSCUSA for any missing resorts
"""

import pandas as pd
import logging
from datetime import datetime
from onthesnow_scraper import OnTheSnowScraper
from colorado_ski_scraper import ColoradoSkiScraper

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

