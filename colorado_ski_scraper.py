#!/usr/bin/env python3
"""
Colorado Ski Country USA Scraper
Scrapes live snow conditions for all Colorado ski resorts using Selenium
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("colorado_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ColoradoSkiScraper:
    """Scrapes snow conditions from Colorado Ski Country USA"""
    
    def __init__(self, headless=True):
        self.url = "https://www.coloradoski.com/snow-report"
        self.headless = headless
        self.driver = None
    
    def setup_driver(self):
        """Configure Chrome driver for Selenium"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Essential options for running in CI/cloud environments
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
        """Load the page and wait for JavaScript to render data"""
        try:
            logger.info(f"Loading {self.url}")
            self.driver.get(self.url)
            
            # Wait for the page to load - look for common elements
            # This will need adjustment based on actual page structure
            logger.info("Waiting for page to load...")
            
            # Wait up to 30 seconds for content to appear
            wait = WebDriverWait(self.driver, 30)
            
            # Try to wait for any of these common patterns
            try:
                # Wait for resort data to appear (adjust selector as needed)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                logger.info("Page body loaded")
                
                # Give JavaScript extra time to load data
                time.sleep(5)
                
            except Exception as e:
                logger.warning(f"Timeout waiting for specific elements: {e}")
                # Continue anyway - sometimes data loads without specific markers
            
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
        
        # This is where we need to identify the actual data structure
        # Let's look for common patterns in the HTML
        
        # Strategy 1: Look for table rows
        tables = soup.find_all('table')
        logger.info(f"Found {len(tables)} tables")
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:  # Has enough data
                    resort_data = self._extract_resort_from_row(cells)
                    if resort_data:
                        resorts.append(resort_data)
        
        # Strategy 2: Look for divs/articles with resort data
        if not resorts:
            logger.info("No table data found, looking for div/article structure")
            resort_containers = soup.find_all(['div', 'article'], 
                                             class_=lambda x: x and 'resort' in x.lower())
            
            for container in resort_containers:
                resort_data = self._extract_resort_from_container(container)
                if resort_data:
                    resorts.append(resort_data)
        
        # Strategy 3: Look for specific data attributes
        if not resorts:
            logger.info("Trying data attribute strategy")
            elements = soup.find_all(attrs={'data-resort': True})
            for element in elements:
                resort_data = self._extract_resort_from_element(element)
                if resort_data:
                    resorts.append(resort_data)
        
        logger.info(f"Extracted {len(resorts)} resorts")
        
        return resorts
    
    def _extract_resort_from_row(self, cells):
        """Extract resort data from table row cells"""
        try:
            # Adjust indices based on actual table structure
            resort = {
                'name': cells[0].get_text(strip=True),
                'conditions': cells[1].get_text(strip=True) if len(cells) > 1 else '',
                'new_snow_24h': self._parse_snow(cells[2].get_text(strip=True)) if len(cells) > 2 else 0,
                'trails_open': self._parse_trails(cells[3].get_text(strip=True)) if len(cells) > 3 else '0/0',
            }
            
            # Only return if we got a valid resort name
            if resort['name'] and len(resort['name']) > 2:
                return resort
                
        except Exception as e:
            logger.debug(f"Error parsing row: {e}")
        
        return None
    
    def _extract_resort_from_container(self, container):
        """Extract resort data from div/article container"""
        try:
            resort = {
                'name': '',
                'conditions': '',
                'new_snow_24h': 0,
                'trails_open': '0/0',
            }
            
            # Look for resort name
            name_elem = container.find(['h1', 'h2', 'h3', 'h4', 'a'], 
                                      class_=lambda x: x and ('name' in x.lower() or 'title' in x.lower()))
            if name_elem:
                resort['name'] = name_elem.get_text(strip=True)
            
            # Look for snow data
            snow_elem = container.find(string=lambda x: x and 'snow' in x.lower())
            if snow_elem:
                resort['new_snow_24h'] = self._parse_snow(snow_elem)
            
            # Look for trail data
            trail_elem = container.find(string=lambda x: x and 'trail' in x.lower())
            if trail_elem:
                resort['trails_open'] = self._parse_trails(trail_elem)
            
            if resort['name']:
                return resort
                
        except Exception as e:
            logger.debug(f"Error parsing container: {e}")
        
        return None
    
    def _extract_resort_from_element(self, element):
        """Extract resort data from element with data attributes"""
        try:
            resort = {
                'name': element.get('data-resort', ''),
                'conditions': element.get('data-conditions', ''),
                'new_snow_24h': int(element.get('data-snow', 0)),
                'trails_open': element.get('data-trails', '0/0'),
            }
            
            if resort['name']:
                return resort
                
        except Exception as e:
            logger.debug(f"Error parsing element: {e}")
        
        return None
    
    def _parse_snow(self, text):
        """Extract snow amount from text like '24-hour snow total: 5\"' """
        import re
        match = re.search(r'(\d+)"', text)
        if match:
            return int(match.group(1))
        return 0
    
    def _parse_trails(self, text):
        """Extract trail counts from text like 'Trails open: 5/147' """
        import re
        match = re.search(r'(\d+)/(\d+)', text)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        return "0/0"
    
    def scrape(self):
        """Main scraping method"""
        try:
            self.setup_driver()
            html = self.fetch_page()
            
            # Save HTML for debugging
            with open('colorado_ski_page_rendered.html', 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info("Saved rendered HTML to colorado_ski_page_rendered.html")
            
            resorts = self.parse_snow_data(html)
            
            if not resorts:
                logger.warning("No resort data found! Check HTML file for structure")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(resorts)
            
            # Add metadata
            df['data_fetched_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Clean up data
            df = self._clean_data(df)
            
            return df
            
        finally:
            self.cleanup()
    
    def _clean_data(self, df):
        """Clean and standardize the data"""
        # Ensure required columns exist
        required_cols = ['name', 'conditions', 'new_snow_24h', 'trails_open']
        for col in required_cols:
            if col not in df.columns:
                df[col] = '' if col in ['name', 'conditions', 'trails_open'] else 0
        
        # Parse trails into separate columns
        if 'trails_open' in df.columns:
            df[['open_trails', 'total_trails']] = df['trails_open'].str.extract(r'(\d+)/(\d+)')
            df['open_trails'] = pd.to_numeric(df['open_trails'], errors='coerce').fillna(0).astype(int)
            df['total_trails'] = pd.to_numeric(df['total_trails'], errors='coerce').fillna(0).astype(int)
        
        # Ensure snow is numeric
        df['new_snow_24h'] = pd.to_numeric(df['new_snow_24h'], errors='coerce').fillna(0).astype(int)
        
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
    logger.info("COLORADO SKI SCRAPER - TEST RUN")
    logger.info("="*70)
    
    scraper = ColoradoSkiScraper(headless=True)
    
    try:
        df = scraper.scrape()
        
        if df.empty:
            logger.error("No data scraped - check the HTML file for page structure")
            return
        
        # Save results
        output_file = "colorado_resorts_scraped.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Saved data to {output_file}")
        
        # Display summary
        logger.info(f"\n{'='*70}")
        logger.info("SCRAPING RESULTS")
        logger.info(f"{'='*70}")
        logger.info(f"Total resorts: {len(df)}")
        logger.info(f"\nFirst 10 resorts:")
        print(df[['name', 'new_snow_24h', 'open_trails', 'total_trails', 'conditions']].head(10).to_string())
        
        # Check for resorts with snow
        with_snow = df[df['new_snow_24h'] > 0]
        if len(with_snow) > 0:
            logger.info(f"\n🌨️  Resorts with new snow (24h):")
            print(with_snow[['name', 'new_snow_24h']])
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

