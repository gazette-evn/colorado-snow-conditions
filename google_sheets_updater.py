#!/usr/bin/env python3
"""
Google Sheets Updater
Uploads Colorado resort data to Google Sheets for Datawrapper integration
"""

import os
import json
import logging
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("google_sheets_updater.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
SPREADSHEET_ID = os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID")
CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS")  # JSON string from GitHub secrets

# Google Sheets API scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsUpdater:
    """Handles updating Google Sheets with Colorado resort data"""
    
    def __init__(self, spreadsheet_id=None, credentials_json=None):
        self.spreadsheet_id = spreadsheet_id or SPREADSHEET_ID
        self.credentials_json = credentials_json or CREDENTIALS_JSON
        self.service = None
        
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID not set")
        
        if not self.credentials_json:
            raise ValueError("GOOGLE_CREDENTIALS not set")
        
        # Debug logging (don't log actual credentials, just metadata)
        logger.info(f"Spreadsheet ID length: {len(str(self.spreadsheet_id))}")
        logger.info(f"Credentials type: {type(self.credentials_json)}")
        logger.info(f"Credentials length: {len(str(self.credentials_json))}")
        
        # Check if credentials is just whitespace
        if isinstance(self.credentials_json, str) and not self.credentials_json.strip():
            raise ValueError("GOOGLE_CREDENTIALS is empty or only whitespace")
    
    def authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        try:
            logger.info("Authenticating with Google Sheets API...")
            
            # Parse credentials JSON
            if isinstance(self.credentials_json, str):
                # Clean up the JSON string (remove extra quotes, whitespace, newlines)
                cleaned = self.credentials_json.strip()
                
                # Remove surrounding quotes if present (common when pasting into GitHub secrets)
                if cleaned.startswith("'") and cleaned.endswith("'"):
                    cleaned = cleaned[1:-1]
                if cleaned.startswith('"') and cleaned.endswith('"'):
                    cleaned = cleaned[1:-1]
                
                # Log the first few characters for debugging (don't log the whole thing!)
                logger.info(f"Parsing credentials JSON (starts with: {cleaned[:50]}...)")
                
                try:
                    credentials_dict = json.loads(cleaned)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON. Length: {len(cleaned)}, First 100 chars: {cleaned[:100]}")
                    logger.error(f"JSON error: {e}")
                    raise
            else:
                credentials_dict = self.credentials_json
            
            # Create credentials
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=SCOPES
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("✅ Successfully authenticated with Google Sheets API")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to authenticate: {e}")
            raise
    
    def prepare_data(self, csv_file):
        """Read and prepare data from CSV file"""
        try:
            logger.info(f"Reading data from {csv_file}...")
            df = pd.read_csv(csv_file)
            
            # Select and rename columns for Google Sheets
            # Include all useful data for Datawrapper Symbol Map
            # Keep numeric values clean (no " symbols) for Datawrapper
            
            # Convert to clean numeric values
            def clean_numeric(x):
                if pd.isna(x) or x == '':
                    return 0
                try:
                    return float(x)
                except:
                    return 0
            
            sheet_data = pd.DataFrame({
                'Resort Name': df['name'],
                'Latitude': df.get('latitude', df.get('lat', '')),
                'Longitude': df.get('longitude', df.get('lng', '')),
                'Status': df.get('status', 'Unknown'),
                '24h Snowfall (in)': df.get('new_snow_24h', 0).apply(clean_numeric),
                '48h Snowfall (in)': df.get('new_snow_48h', 0).apply(clean_numeric),
                'Base Depth (in)': df.get('base_depth', 0).apply(clean_numeric),
                'Mid-Mtn Depth (in)': df.get('mid_mtn_depth', 0).apply(clean_numeric),
                'Surface Conditions': df.get('surface_conditions', ''),
                'Total Trails': df.get('total_trails', 0),
                'Open Trails': df.get('open_trails', 0),
                'Trails Open %': df.get('trails_open_pct', 0),
                'Total Lifts': df.get('total_lifts', 0),
                'Open Lifts': df.get('open_lifts', 0),
                'Lifts Open %': df.get('lifts_open_pct', 0),
                'Data Source': df.get('source', ''),
                'Last Updated': datetime.now(ZoneInfo('America/Denver')).strftime('%Y-%m-%d %H:%M')
            })
            
            # Convert to list of lists for Sheets API
            # First row is headers
            values = [sheet_data.columns.tolist()] + sheet_data.fillna('').values.tolist()
            
            logger.info(f"✅ Prepared data: {len(values)-1} resorts")
            return values
            
        except Exception as e:
            logger.error(f"❌ Failed to prepare data: {e}")
            raise
    
    def update_sheet(self, values, sheet_name='Sheet1'):
        """Update Google Sheet with new data"""
        try:
            if not self.service:
                raise ValueError("Not authenticated. Call authenticate() first.")
            
            logger.info(f"Updating sheet {self.spreadsheet_id}...")
            
            # Clear existing data
            range_name = f'{sheet_name}!A:Z'
            logger.info(f"Clearing range {range_name}...")
            
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            # Write new data
            logger.info(f"Writing {len(values)} rows...")
            
            body = {
                'values': values
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f'{sheet_name}!A1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            updated_cells = result.get('updatedCells', 0)
            logger.info(f"✅ Successfully updated {updated_cells} cells")
            
            return result
            
        except HttpError as e:
            logger.error(f"❌ HTTP Error updating sheet: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to update sheet: {e}")
            raise
    
    def format_sheet(self, sheet_name='Sheet1'):
        """Apply formatting to make the sheet look nice"""
        try:
            logger.info("Applying formatting...")
            
            requests = [
                # Freeze header row
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': 0,
                            'gridProperties': {
                                'frozenRowCount': 1
                            }
                        },
                        'fields': 'gridProperties.frozenRowCount'
                    }
                },
                # Bold header row
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'textFormat': {
                                    'bold': True
                                }
                            }
                        },
                        'fields': 'userEnteredFormat.textFormat.bold'
                    }
                },
                # Auto-resize columns
                {
                    'autoResizeDimensions': {
                        'dimensions': {
                            'sheetId': 0,
                            'dimension': 'COLUMNS',
                            'startIndex': 0,
                            'endIndex': 9
                        }
                    }
                }
            ]
            
            body = {
                'requests': requests
            }
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
            
            logger.info("✅ Formatting applied")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to apply formatting (non-critical): {e}")


def main():
    """Main execution"""
    logger.info("="*70)
    logger.info("GOOGLE SHEETS UPDATER - Colorado Snow Conditions")
    logger.info("="*70)
    
    try:
        # Initialize updater
        updater = GoogleSheetsUpdater()
        
        # Authenticate
        updater.authenticate()
        
        # Read data from combined scraper output
        csv_file = 'colorado_resorts_combined.csv'
        if not os.path.exists(csv_file):
            logger.error(f"❌ CSV file not found: {csv_file}")
            logger.info("Run combined_scraper.py first to generate the data")
            return
        
        # Prepare data
        values = updater.prepare_data(csv_file)
        
        # Update sheet
        updater.update_sheet(values)
        
        # Apply formatting
        updater.format_sheet()
        
        logger.info("="*70)
        logger.info("✅ GOOGLE SHEETS UPDATE COMPLETE!")
        logger.info("="*70)
        logger.info(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{updater.spreadsheet_id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to update Google Sheets: {e}")
        raise


if __name__ == "__main__":
    main()

