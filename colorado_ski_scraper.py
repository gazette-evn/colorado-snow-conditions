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
        
        # Find all resort cards - they use class "one-snow-card"
        resort_cards = soup.find_all('div', class_='one-snow-card')
        logger.info(f"Found {len(resort_cards)} resort cards")
        
        for card in resort_cards:
            try:
                resort_data = self._extract_resort_from_card(card)
                if resort_data:
                    resorts.append(resort_data)
            except Exception as e:
                logger.warning(f"Error parsing resort card: {e}")
                continue
        
        logger.info(f"Extracted {len(resorts)} resorts")
        
        return resorts
    
    def _extract_resort_from_card(self, card):
        """Extract resort data from a one-snow-card div"""
        try:
            resort = {}
            
            # Get resort name from h3 with class "h5 text-left"
            name_elem = card.find('h3', class_='h5 text-left')
            if not name_elem:
                name_elem = card.find('h3', class_='h5')
            
            if name_elem:
                resort['name'] = name_elem.get_text(strip=True)
            else:
                return None
            
            # Get 24hr snow
            twentyfour = card.find('span', class_='answer twentyfour')
            resort['new_snow_24h'] = self._parse_snow(twentyfour.get_text(strip=True)) if twentyfour else 0
            
            # Get 48hr snow
            fortyeight = card.find('span', class_='answer fortyeight')
            resort['new_snow_48h'] = self._parse_snow(fortyeight.get_text(strip=True)) if fortyeight else 0
            
            # Get mid-mountain depth
            mid_mtn = card.find('span', class_='answer mid-mtn')
            resort['mid_mtn_depth'] = self._parse_snow(mid_mtn.get_text(strip=True)) if mid_mtn else 0
            
            # Get surface conditions
            surface = card.find('p', class_='surface')
            if surface:
                surface_span = surface.find('span')
                resort['surface_conditions'] = surface_span.get_text(strip=True) if surface_span else ''
            else:
                resort['surface_conditions'] = ''
            
            # Get lifts open/total
            lifts_elem = card.find('p', class_='lifts-open')
            if lifts_elem:
                open_span = lifts_elem.find('span', class_='open')
                total_span = lifts_elem.find('span', class_='total')
                if open_span and total_span:
                    resort['lifts_open'] = f"{open_span.get_text(strip=True)}/{total_span.get_text(strip=True)}"
                else:
                    resort['lifts_open'] = '0/0'
            else:
                resort['lifts_open'] = '0/0'
            
            # Get status (Open/Closed)
            status_open = card.find('span', class_='open')
            status_closed = card.find('span', class_='closed')
            if status_open and 'mt-3' in status_open.get('class', []):
                resort['status'] = 'Open'
            elif status_closed:
                resort['status'] = 'Closed'
            else:
                resort['status'] = 'Unknown'
            
            return resort
            
        except Exception as e:
            logger.warning(f"Error extracting resort card: {e}")
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
        required_cols = ['name', 'surface_conditions', 'new_snow_24h', 'new_snow_48h', 'mid_mtn_depth', 'lifts_open', 'status']
        for col in required_cols:
            if col not in df.columns:
                if col in ['name', 'surface_conditions', 'lifts_open', 'status']:
                    df[col] = ''
                else:
                    df[col] = 0
        
        # Parse lifts into separate columns
        if 'lifts_open' in df.columns:
            df[['open_lifts', 'total_lifts']] = df['lifts_open'].str.extract(r'(\d+)/(\d+)')
            df['open_lifts'] = pd.to_numeric(df['open_lifts'], errors='coerce').fillna(0).astype(int)
            df['total_lifts'] = pd.to_numeric(df['total_lifts'], errors='coerce').fillna(0).astype(int)
        
        # Ensure snow fields are numeric
        for col in ['new_snow_24h', 'new_snow_48h', 'mid_mtn_depth']:
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
        
        # Use columns that actually exist
        display_cols = []
        for col in ['name', 'new_snow_24h', 'open_lifts', 'total_lifts', 'surface_conditions']:
            if col in df.columns:
                display_cols.append(col)
        
        if display_cols:
            print(df[display_cols].head(10).to_string())
        else:
            print(df.head(10).to_string())
        
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

