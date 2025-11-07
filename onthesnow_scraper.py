#!/usr/bin/env python3
"""
OnTheSnow Colorado Scraper
Scrapes snow conditions for ALL Colorado ski resorts from OnTheSnow
Primary data source - covers 23+ resorts including all major ones
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
from bs4 import BeautifulSoup
import time
import re

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
    """Scrapes snow conditions from OnTheSnow.com for Colorado"""
    
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
    
    def fetch_page(self):
        """Load the page and wait for data to render"""
        try:
            logger.info(f"Loading {self.url}")
            self.driver.get(self.url)
            
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
            logger.error(f"Error fetching page: {e}")
            raise
    
    def parse_snow_data(self, html):
        """Parse the HTML to extract resort data"""
        soup = BeautifulSoup(html, 'html.parser')
        
        resorts = []
        
        # OnTheSnow typically uses tables for resort data
        # Look for table rows with resort information
        
        # Strategy 1: Find table with resort data
        tables = soup.find_all('table')
        logger.info(f"Found {len(tables)} tables")
        
        for table in tables:
            rows = table.find_all('tr')
            logger.info(f"Table has {len(rows)} rows")
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:  # Enough data for a resort
                    resort_data = self._extract_resort_from_row(cells, row)
                    if resort_data:
                        resorts.append(resort_data)
        
        # Strategy 2: Look for div-based layout (if no tables)
        if not resorts:
            logger.info("No table data found, looking for div structure")
            # OnTheSnow might use divs with specific classes
            resort_divs = soup.find_all('div', class_=lambda x: x and 'resort' in x.lower())
            
            for div in resort_divs:
                resort_data = self._extract_resort_from_div(div)
                if resort_data:
                    resorts.append(resort_data)
        
        logger.info(f"Extracted {len(resorts)} resorts")
        
        return resorts
    
    def _extract_resort_from_row(self, cells, row):
        """Extract resort data from table row"""
        try:
            # Get resort name - usually first cell or contains a link
            name = None
            for cell in cells[:2]:  # Check first 2 cells for name
                text = cell.get_text(strip=True)
                link = cell.find('a')
                if link:
                    name = link.get_text(strip=True)
                    break
                elif text and len(text) > 3 and not text.isdigit():
                    name = text
                    break
            
            if not name or len(name) < 3:
                return None
            
            # Filter out header rows
            if name.lower() in ['resort', 'name', 'location', 'open', 'closed']:
                return None
            
            resort = {'name': name}
            
            # Extract numeric data from remaining cells
            data_cells = [cell.get_text(strip=True) for cell in cells]
            
            # Try to find snow/depth/lift data
            for cell_text in data_cells:
                # Look for snow amounts (e.g., "5\"", "0-1\"", "18\"")
                if '"' in cell_text or 'in' in cell_text.lower():
                    inches = self._parse_measurement(cell_text)
                    if 'new_snow_24h' not in resort:
                        resort['new_snow_24h'] = inches
                    elif 'new_snow_48h' not in resort:
                        resort['new_snow_48h'] = inches
                    elif 'base_depth' not in resort:
                        resort['base_depth'] = inches
                
                # Look for lift/trail counts (e.g., "4/140", "5/23")
                if '/' in cell_text and re.match(r'\d+/\d+', cell_text):
                    if 'lifts_open' not in resort:
                        resort['lifts_open'] = cell_text
                    elif 'trails_open' not in resort:
                        resort['trails_open'] = cell_text
            
            # Get status from row or cells
            status_text = row.get_text().lower()
            if 'open' in status_text and 'opens' not in status_text:
                resort['status'] = 'Open'
            elif 'closed' in status_text or 'opens' in status_text:
                resort['status'] = 'Closed'
            else:
                resort['status'] = 'Unknown'
            
            # Set defaults for missing fields
            resort.setdefault('new_snow_24h', 0)
            resort.setdefault('new_snow_48h', 0)
            resort.setdefault('base_depth', 0)
            resort.setdefault('lifts_open', '0/0')
            resort.setdefault('trails_open', '0/0')
            
            return resort
            
        except Exception as e:
            logger.debug(f"Error parsing row: {e}")
            return None
    
    def _extract_resort_from_div(self, div):
        """Extract resort data from div container"""
        try:
            name_elem = div.find(['h2', 'h3', 'h4', 'a'])
            if not name_elem:
                return None
            
            name = name_elem.get_text(strip=True)
            if len(name) < 3:
                return None
            
            resort = {
                'name': name,
                'new_snow_24h': 0,
                'new_snow_48h': 0,
                'base_depth': 0,
                'lifts_open': '0/0',
                'trails_open': '0/0',
                'status': 'Unknown'
            }
            
            # Extract data from div text
            div_text = div.get_text()
            
            # Look for measurements
            measurements = re.findall(r'(\d+)"', div_text)
            if len(measurements) >= 1:
                resort['new_snow_24h'] = int(measurements[0])
            if len(measurements) >= 2:
                resort['base_depth'] = int(measurements[1])
            
            # Look for lift/trail data
            counts = re.findall(r'(\d+/\d+)', div_text)
            if len(counts) >= 1:
                resort['lifts_open'] = counts[0]
            
            return resort
            
        except Exception as e:
            logger.debug(f"Error parsing div: {e}")
            return None
    
    def _parse_measurement(self, text):
        """Extract measurement in inches from text like '5\"' or '0-1\"' or '18 in'"""
        # Handle ranges like "0-1\""
        range_match = re.search(r'(\d+)-(\d+)', text)
        if range_match:
            # Take the higher number
            return int(range_match.group(2))
        
        # Handle simple numbers like "5\"" or "18 in"
        num_match = re.search(r'(\d+)', text)
        if num_match:
            return int(num_match.group(1))
        
        return 0
    
    def scrape(self):
        """Main scraping method"""
        try:
            self.setup_driver()
            html = self.fetch_page()
            
            # Save HTML for debugging
            with open('onthesnow_page_rendered.html', 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info("Saved rendered HTML to onthesnow_page_rendered.html")
            
            resorts = self.parse_snow_data(html)
            
            if not resorts:
                logger.warning("No resort data found! Check HTML file for structure")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(resorts)
            
            # Add metadata
            df['data_fetched_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['source'] = 'OnTheSnow'
            
            # Clean up data
            df = self._clean_data(df)
            
            return df
            
        finally:
            self.cleanup()
    
    def _clean_data(self, df):
        """Clean and standardize the data"""
        # Ensure required columns exist
        required_cols = ['name', 'new_snow_24h', 'new_snow_48h', 'base_depth', 'lifts_open', 'trails_open', 'status']
        for col in required_cols:
            if col not in df.columns:
                if col in ['name', 'lifts_open', 'trails_open', 'status']:
                    df[col] = '' if col == 'name' else '0/0' if 'open' in col else 'Unknown'
                else:
                    df[col] = 0
        
        # Parse lifts and trails into separate columns
        for field in ['lifts_open', 'trails_open']:
            if field in df.columns:
                col_prefix = field.replace('_open', '')
                df[[f'open_{col_prefix}', f'total_{col_prefix}']] = df[field].str.extract(r'(\d+)/(\d+)')
                df[f'open_{col_prefix}'] = pd.to_numeric(df[f'open_{col_prefix}'], errors='coerce').fillna(0).astype(int)
                df[f'total_{col_prefix}'] = pd.to_numeric(df[f'total_{col_prefix}'], errors='coerce').fillna(0).astype(int)
        
        # Ensure numeric fields
        for col in ['new_snow_24h', 'new_snow_48h', 'base_depth']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # Sort by name
        df = df.sort_values('name').reset_index(drop=True)
        
        logger.info(f"Cleaned data for {len(df)} resorts")
        
        return df
    
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
            logger.error("No data scraped - check the HTML file for page structure")
            return
        
        # Save results
        output_file = "onthesnow_resorts.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Saved data to {output_file}")
        
        # Display summary
        logger.info(f"\n{'='*70}")
        logger.info("SCRAPING RESULTS")
        logger.info(f"{'='*70}")
        logger.info(f"Total resorts: {len(df)}")
        logger.info(f"\nAll resorts found:")
        for idx, name in enumerate(df['name'].tolist(), 1):
            logger.info(f"  {idx}. {name}")
        
        # Show sample data
        logger.info(f"\nSample data (first 5 resorts):")
        cols = ['name', 'new_snow_24h', 'base_depth', 'lifts_open', 'status']
        print(df[cols].head().to_string())
        
        # Check for open resorts
        open_resorts = df[df['status'] == 'Open']
        if len(open_resorts) > 0:
            logger.info(f"\n🎿 {len(open_resorts)} resorts currently OPEN:")
            for _, resort in open_resorts.iterrows():
                logger.info(f"  - {resort['name']}: {resort['lifts_open']} lifts")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

