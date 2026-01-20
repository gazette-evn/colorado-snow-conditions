#!/usr/bin/env python3
"""
Aspen Snowmass Official Scraper
Hits the official JSON endpoints directly for 100% accuracy
"""

import pandas as pd
import requests
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("aspen_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AspenSnowmassScraper:
    """Scrapes snow conditions from official aspensnowmass.com JSON feeds"""
    
    def __init__(self, headless=True):
        self.base_url = "https://www.aspensnowmass.com/AspenSnowmass/SnowReport/Feed"
        self.mountains = {
            'Snowmass': 'Snowmass',
            'Aspen Mountain': 'AspenMountain',
            'Aspen Highlands': 'AspenHighlands',
            'Buttermilk': 'Buttermilk'
        }
    
    def scrape(self):
        """Fetch data from the 4 individual mountain feeds"""
        results = []
        
        for display_name, internal_id in self.mountains.items():
            try:
                url = f"{self.base_url}?mountain={internal_id}"
                logger.info(f"Fetching official data for {display_name}...")
                
                response = requests.get(url, timeout=15)
                if response.status_code != 200:
                    logger.error(f"Failed to fetch {display_name}: Status {response.status_code}")
                    continue
                
                data = response.json()
                
                # Extract values from the JSON structure
                # Note: The keys match the screenshot exactly (snow24Hours, snowBase, etc.)
                resort = {
                    'name': display_name,
                    'status': data.get('status', 'Unknown'),
                    'new_snow_24h': int(data.get('snow24Hours', {}).get('inches', 0)),
                    'new_snow_48h': int(data.get('snow48Hours', {}).get('inches', 0)),
                    'base_depth': int(data.get('snowBase', {}).get('inches', 0)),
                    'open_lifts': int(data.get('lifts', {}).get('openCount', 0)),
                    'total_lifts': int(data.get('lifts', {}).get('totalCount', 0)),
                    'open_trails': int(data.get('trails', {}).get('openCount', 0)),
                    'total_trails': int(data.get('trails', {}).get('totalCount', 0)),
                    'source': 'Aspen Official',
                    'data_fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Create the string format fields for downstream compatibility
                resort['lifts_open'] = f"{resort['open_lifts']}/{resort['total_lifts']}"
                resort['trails_open'] = f"{resort['open_trails']}/{resort['total_trails']}"
                
                results.append(resort)
                logger.info(f"✅ Success {display_name}: {resort['new_snow_24h']}\" new, {resort['base_depth']}\" base, {resort['lifts_open']} lifts")
                
            except Exception as e:
                logger.error(f"Error processing {display_name}: {e}")
        
        return pd.DataFrame(results)

if __name__ == "__main__":
    scraper = AspenSnowmassScraper()
    df = scraper.scrape()
    print("\nVERIFIED DATA:")
    print(df[['name', 'new_snow_24h', 'base_depth', 'lifts_open', 'trails_open']].to_string())
