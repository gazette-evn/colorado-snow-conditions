# Google Sheets API Setup Guide

This guide will help you set up Google Sheets API access for the Colorado Snow Conditions project.

## Step 1: Create Google Cloud Project (5 minutes)

1. Go to: https://console.cloud.google.com/
2. Click "New Project" (top right, next to search bar)
3. Name it: "Colorado Snow Conditions"
4. Click "Create"

## Step 2: Enable Google Sheets API (2 minutes)

1. In your project, go to: https://console.cloud.google.com/apis/library
2. Search for "Google Sheets API"
3. Click on it
4. Click "Enable"

## Step 3: Create Service Account (5 minutes)

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Name: `colorado-snow-bot`
4. Description: "Automated updates for Colorado snow data"
5. Click "Create and Continue"
6. Skip "Grant access" (click Continue)
7. Skip "Grant users access" (click Done)

## Step 4: Create Service Account Key (3 minutes)

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON"
5. Click "Create"
6. **Save the downloaded JSON file** - you'll need it!

The JSON file looks like:
```json
{
  "type": "service_account",
  "project_id": "your-project-123456",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "colorado-snow-bot@your-project.iam.gserviceaccount.com",
  ...
}
```

**Important:** Copy the `client_email` value - you'll need it in Step 5!

## Step 5: Create Google Sheet (3 minutes)

1. Go to: https://sheets.google.com
2. Click "Blank" to create a new sheet
3. Name it: "Colorado Snow Conditions"
4. **Copy the Sheet ID from the URL:**
   - URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
   - Sheet ID is the long string between `/d/` and `/edit`
5. **Share the sheet with your service account:**
   - Click "Share" button (top right)
   - Paste the `client_email` from Step 4
   - Give it "Editor" access
   - Click "Send"

## Step 6: Add to Environment Variables

### For Local Testing:

Edit your `.env` file:

```bash
# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS='paste_entire_json_here'
```

**Note:** The credentials should be the ENTIRE JSON content in single quotes.

### For GitHub Actions:

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"

**Secret 1:**
- Name: `GOOGLE_SHEETS_SPREADSHEET_ID`
- Value: Your sheet ID (from Step 5)

**Secret 2:**
- Name: `GOOGLE_CREDENTIALS`
- Value: Paste the ENTIRE contents of the JSON file from Step 4

## Step 7: Test Locally (Optional)

```bash
cd /Users/evanwyloge/snow-conditions-data
source venv/bin/activate  # If using venv
pip install -r requirements.txt

# Run the combined scraper first
python combined_scraper.py

# Then update Google Sheets
python google_sheets_updater.py
```

You should see:
```
✅ Successfully authenticated with Google Sheets API
✅ Prepared data: 23 resorts
✅ Successfully updated X cells
✅ GOOGLE SHEETS UPDATE COMPLETE!
```

## Step 8: Verify in Google Sheets

Open your sheet: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID`

You should see:
- **Header row** (bold): Resort Name, Latitude, Longitude, Status, etc.
- **23 rows** of resort data
- Clean formatting

---

## Troubleshooting

### "Permission denied" error
- Make sure you shared the sheet with the service account email
- Check that the email in the JSON matches the one you shared with

### "Invalid credentials" error
- Verify the JSON is complete (includes private key)
- Check that quotes are correct in `.env` or GitHub secrets

### "Spreadsheet not found" error
- Verify the spreadsheet ID is correct
- Make sure the sheet exists and wasn't deleted

---

## Next Steps

Once Google Sheets is working:
1. Publish the sheet (File → Share → Publish to web)
2. Connect it to Datawrapper
3. Create your Symbol Map visualization!

