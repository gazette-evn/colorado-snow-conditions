#!/usr/bin/env python3
"""
Google Sheets Forecast Updater
Uploads Colorado snowfall forecast CSV to Google Sheets for Datawrapper.
"""

import os
import json
import logging
import pandas as pd
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
        logging.FileHandler("google_sheets_forecast_updater.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
FORECAST_SPREADSHEET_ID = os.environ.get("GOOGLE_SHEETS_FORECAST_ID")
CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS")

# Google Sheets API scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsForecastUpdater:
    """Handles updating Google Sheets with Colorado forecast data"""

    def __init__(self, spreadsheet_id=None, credentials_json=None):
        self.spreadsheet_id = spreadsheet_id or FORECAST_SPREADSHEET_ID
        self.credentials_json = credentials_json or CREDENTIALS_JSON
        self.service = None

        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_FORECAST_ID not set")

        if not self.credentials_json:
            raise ValueError("GOOGLE_CREDENTIALS not set")

    def authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        try:
            logger.info("Authenticating with Google Sheets API...")

            if isinstance(self.credentials_json, str):
                cleaned = self.credentials_json.strip()
                if cleaned.startswith("'") and cleaned.endswith("'"):
                    cleaned = cleaned[1:-1]
                if cleaned.startswith('"') and cleaned.endswith('"'):
                    cleaned = cleaned[1:-1]
                credentials_dict = json.loads(cleaned)
            else:
                credentials_dict = self.credentials_json

            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=SCOPES
            )

            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("✅ Successfully authenticated with Google Sheets API")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to authenticate: {e}")
            raise

    def prepare_data(self, csv_file):
        """Read forecast CSV and return values for Sheets API."""
        try:
            logger.info(f"Reading data from {csv_file}...")
            df = pd.read_csv(csv_file)

            values = [df.columns.tolist()] + df.fillna('').values.tolist()
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
            range_name = f'{sheet_name}!A:Z'
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            body = {'values': values}
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


def main():
    logger.info("="*70)
    logger.info("GOOGLE SHEETS FORECAST UPDATER - Colorado")
    logger.info("="*70)

    updater = GoogleSheetsForecastUpdater()
    updater.authenticate()

    csv_file = 'colorado_snow_forecast.csv'
    if not os.path.exists(csv_file):
        logger.error(f"❌ CSV file not found: {csv_file}")
        logger.info("Run open_meteo_forecast_export.py first to generate the data")
        return

    values = updater.prepare_data(csv_file)
    updater.update_sheet(values)

    logger.info("="*70)
    logger.info("✅ GOOGLE SHEETS FORECAST UPDATE COMPLETE!")
    logger.info("="*70)
    logger.info(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{updater.spreadsheet_id}")


if __name__ == "__main__":
    main()
