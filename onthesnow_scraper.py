#!/usr/bin/env python3
"""
OnTheSnow Colorado Scraper
Scrapes snow conditions for ALL Colorado ski resorts from OnTheSnow
Primary data source - uses embedded JSON for robustness and detail
"""

import os
import pandas as pd
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("onthesnow_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OnTheSnowScraper:
    """Scrapes snow conditions from OnTheSnow.com for Colorado using embedded JSON"""
    
    def __init__(self, headless=True):
        self.url = "https://www.onthesnow.com/colorado/skireport.html"
        self.headless = headless
        self.driver = None
    
    def setup_driver(self):
        """Configure Chrome driver for Selenium"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Essential options for CI/cloud environments
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        # Initialize driver
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def fetch_page(self, url=None):
        """Load the page and wait for data to render"""
        target_url = url or self.url
        try:
            logger.info(f"Loading {target_url}")
            self.driver.get(target_url)
            
            # Wait for the page to load
            logger.info("Waiting for page to load...")
            wait = WebDriverWait(self.driver, 30)
            
            # Wait for body
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("Page body loaded")
            
            # Give extra time for dynamic content
            time.sleep(5)
            
            # Get the rendered HTML
            html = self.driver.page_source
            logger.info(f"Retrieved {len(html)} bytes of HTML")
            
            return html
            
        except Exception as e:
            logger.error(f"Error fetching page {target_url}: {e}")
            raise
    
    def parse_json_data(self, html):
        """Extract resort data from __NEXT_DATA__ JSON"""
        try:
            # Find the __NEXT_DATA__ script tag
            match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
            
            if not match:
                logger.error("Could not find __NEXT_DATA__ in HTML")
                return []
            
            # Parse JSON
            data = json.loads(match.group(1))
            
            # Navigate to resorts data
            try:
                resorts_data = data['props']['pageProps']['resorts']
            except KeyError:
                logger.warning("Could not find resorts data in JSON structure, checking alternative paths")
                # Fallback paths if needed
                return []

            all_resorts = []
            
            # Loop through different status categories (1, 2, etc.)
            for category_key, category_data in resorts_data.items():
                resorts_list = category_data.get('data', [])
                for resort_json in resorts_list:
                    resort = self._parse_resort_json(resort_json)
                    if resort:
                        all_resorts.append(resort)
            
            logger.info(f"Extracted {len(all_resorts)} resorts from JSON")
            return all_resorts
            
        except Exception as e:
            logger.error(f"Error parsing JSON data: {e}")
            return []

    def _parse_resort_json(self, resort_json):
        """Parse individual resort from JSON structure"""
        try:
            name = resort_json.get('title', '')
            if not name:
                return None

            # Status: openFlag values: 1=Open, 2=Closed, 5=Weekends Only
            open_flag = resort_json.get('status', {}).get('openFlag', 2)
            if open_flag in [1, 5]:
                status = 'Open'
            else:
                status = 'Closed'

            # Snow data (values are in cm in the JSON)
            snow = resort_json.get('snow', {})
            
            def cm_to_in(cm):
                if cm is None: return 0
                return round(float(cm) / 2.54)

            base_depth = cm_to_in(snow.get('base') or snow.get('middle') or 0)
            new_snow_24h = cm_to_in(snow.get('last24', 0))
            new_snow_48h = cm_to_in(snow.get('last48', 0))

            # Lifts data
            lifts = resort_json.get('lifts', {})
            open_lifts = lifts.get('open', 0) or 0
            total_lifts = lifts.get('total', 0) or 0
            
            # Trails/Runs data
            runs = resort_json.get('runs', {})
            open_trails = runs.get('open', 0) or 0
            total_trails = runs.get('total', 0) or 0

            resort = {
                'name': name,
                'status': status,
                'new_snow_24h': int(new_snow_24h),
                'new_snow_48h': int(new_snow_48h),
                'base_depth': int(base_depth),
                'open_lifts': int(open_lifts),
                'total_lifts': int(total_lifts),
                'open_trails': int(open_trails),
                'total_trails': int(total_trails),
                'lifts_open': f"{open_lifts}/{total_lifts}",
                'trails_open': f"{open_trails}/{total_trails}",
                'slug': resort_json.get('slug', ''),
            }

            return resort

        except Exception as e:
            logger.warning(f"Error parsing resort JSON: {e}")
            return None

    def scrape(self):
        """Main scraping method"""
        try:
            self.setup_driver()
            html = self.fetch_page()
            
            # Save HTML for debugging
            with open('onthesnow_page_rendered.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            resorts = self.parse_json_data(html)
            
            if not resorts:
                logger.warning("No resort data found!")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(resorts)
            
            # Add metadata
            df['data_fetched_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['source'] = 'OnTheSnow'
            
            # --- IMPROVEMENT: Visit individual pages for extra detail ---
            # We do this for all resorts to get "Surface Conditions" and other specifics
            # To save time, we'll only do it for "Open" resorts
            open_resorts = df[df['status'] == 'Open'].copy()
            logger.info(f"Visiting individual pages for {len(open_resorts)} open resorts for extra detail...")
            
            for idx, row in open_resorts.iterrows():
                if row['slug']:
                    try:
                        detail_url = f"https://www.onthesnow.com/colorado/{row['slug']}/skireport"
                        logger.info(f"  -> Detail: {row['name']} ({detail_url})")
                        
                        self.driver.get(detail_url)
                        time.sleep(2) # Reduced sleep for faster execution
                        
                        detail_html = self.driver.page_source
                        
                        # Look for Surface Conditions text
                        # It often appears in a cell with "Machine Groomed", "Powder", etc.
                        # We'll use a simple regex search in the HTML for common condition words
                        conditions = ["Machine Groomed", "Packed Powder", "Powder", "Variable Conditions", "Spring Conditions", "Icy", "Hard Pack"]
                        found_condition = "-"
                        for cond in conditions:
                            if cond in detail_html:
                                found_condition = cond
                                break
                        
                        df.at[idx, 'surface_conditions'] = found_condition
                        
                        # Also look for Mid-Mountain Depth if available
                        # This is harder to find with simple regex, but let's try
                        match = re.search(r'Mid-Mt Depth.*?([0-9]+)"', detail_html, re.DOTALL | re.IGNORECASE)
                        if match:
                            df.at[idx, 'mid_mtn_depth'] = int(match.group(1))
                        
                    except Exception as e:
                        logger.warning(f"Failed to get details for {row['name']}: {e}")
            
            # Sort by name
            df = df.sort_values('name').reset_index(drop=True)
            
            logger.info(f"Scraped data for {len(df)} resorts")
            return df
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome driver closed")
            except Exception as e:
                logger.warning(f"Error closing driver: {e}")


def main():
    """Test the scraper"""
    logger.info("="*70)
    logger.info("ONTHESNOW SCRAPER - TEST RUN")
    logger.info("="*70)
    
    scraper = OnTheSnowScraper(headless=True)
    
    try:
        df = scraper.scrape()
        
        if df.empty:
            logger.error("No data scraped")
            return
        
        # Save results
        output_file = "onthesnow_resorts.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Saved data to {output_file}")
        
        # Display summary
        print(df[['name', 'new_snow_24h', 'base_depth', 'status']].head().to_string())
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
