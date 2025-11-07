#!/usr/bin/env python3
"""
Test script to verify Google Sheets API connection
Run this after setting up Google Sheets credentials
"""

import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

def test_connection():
    """Test Google Sheets API connection"""
    print("="*70)
    print("TESTING GOOGLE SHEETS API CONNECTION")
    print("="*70)
    
    # Check environment variables
    spreadsheet_id = os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID")
    credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
    
    print("\n1. Checking environment variables...")
    
    if not spreadsheet_id:
        print("❌ GOOGLE_SHEETS_SPREADSHEET_ID not found in .env")
        return False
    print(f"✅ Spreadsheet ID: {spreadsheet_id}")
    
    if not credentials_json:
        print("❌ GOOGLE_CREDENTIALS not found in .env")
        return False
    print(f"✅ Credentials found ({len(credentials_json)} characters)")
    
    # Parse credentials
    print("\n2. Parsing credentials...")
    try:
        creds_dict = json.loads(credentials_json)
        print(f"✅ Credentials parsed successfully")
        print(f"   Service account: {creds_dict.get('client_email', 'N/A')}")
        print(f"   Project: {creds_dict.get('project_id', 'N/A')}")
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse credentials JSON: {e}")
        return False
    
    # Authenticate
    print("\n3. Authenticating with Google Sheets API...")
    try:
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=credentials)
        print("✅ Authentication successful")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False
    
    # Test reading from sheet
    print("\n4. Testing read access...")
    try:
        result = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()
        
        sheet_title = result.get('properties', {}).get('title', 'Unknown')
        print(f"✅ Successfully connected to sheet: '{sheet_title}'")
        
        # Get sheet properties
        sheets = result.get('sheets', [])
        if sheets:
            sheet_name = sheets[0].get('properties', {}).get('title', 'Sheet1')
            print(f"   First sheet name: {sheet_name}")
    except Exception as e:
        print(f"❌ Failed to read sheet: {e}")
        print(f"\n   Possible issues:")
        print(f"   - Sheet ID is incorrect")
        print(f"   - Sheet hasn't been shared with service account")
        print(f"   - Service account email: {creds_dict.get('client_email')}")
        return False
    
    # Test writing to sheet
    print("\n5. Testing write access...")
    try:
        test_data = [
            ['Test Column 1', 'Test Column 2', 'Test Column 3'],
            ['Test data', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '✅']
        ]
        
        # Write to a test range
        test_range = 'Sheet1!A1:C2'
        body = {'values': test_data}
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=test_range,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        updated_cells = result.get('updatedCells', 0)
        print(f"✅ Successfully wrote {updated_cells} cells")
        print(f"   Check your sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        
    except Exception as e:
        print(f"❌ Failed to write to sheet: {e}")
        print(f"\n   Possible issues:")
        print(f"   - Service account needs 'Editor' access")
        print(f"   - Go to sheet → Share → Add: {creds_dict.get('client_email')}")
        return False
    
    # Success!
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\nYou can now run: python google_sheets_updater.py")
    print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    
    return True


if __name__ == "__main__":
    from datetime import datetime
    success = test_connection()
    exit(0 if success else 1)

