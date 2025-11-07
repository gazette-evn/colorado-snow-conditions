# Colorado Snow Conditions - Complete Deployment Guide

This guide walks you through deploying the complete automated pipeline:
**Scrapers → Google Sheets → Datawrapper Map**

---

## 🎯 Architecture Overview

```
┌─────────────────────┐
│  GitHub Actions     │
│  (Every 2 hours)    │
└──────────┬──────────┘
           │
           ├─► 1. Run combined_scraper.py
           │   └─► Scrapes OnTheSnow + CSCUSA
           │       Gets 23 Colorado resorts
           │
           ├─► 2. Run google_sheets_updater.py
           │   └─► Updates Google Sheet with new data
           │
           └─► 3. Datawrapper reads from Sheet
               └─► Symbol Map auto-updates
```

---

## 📋 Prerequisites Checklist

- [ ] GitHub account (you have: gazette-evn)
- [ ] Google account for Sheets
- [ ] Datawrapper account (you have API key)
- [ ] Google Cloud account (create in Step 1)

---

## 🚀 Deployment Steps

### Step 1: Set Up Google Sheets API (15 minutes)

Follow the detailed guide: **[GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)**

This will give you:
- ✅ Service account JSON credentials
- ✅ Google Sheet ID
- ✅ Shared sheet with bot access

### Step 2: Add Secrets to GitHub (5 minutes)

Go to: https://github.com/gazette-evn/colorado-snow-conditions/settings/secrets/actions

Click "New repository secret" and add:

**Secret 1:**
- Name: `GOOGLE_SHEETS_SPREADSHEET_ID`
- Value: `YOUR_SHEET_ID` (from Step 1)

**Secret 2:**
- Name: `GOOGLE_CREDENTIALS`
- Value: Paste entire JSON from service account key file

### Step 3: Test the Integration (10 minutes)

#### Option A: Test Locally (Recommended First)

```bash
cd /Users/evanwyloge/snow-conditions-data

# Add credentials to .env
cat >> .env << 'EOF'

# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS='paste_entire_json_here'
EOF

# Install new dependencies
pip install -r requirements.txt

# Test the scraper → Sheets pipeline
python combined_scraper.py
python google_sheets_updater.py
```

**Check your Google Sheet** - should have 23 resorts!

#### Option B: Test on GitHub Actions

1. Go to: https://github.com/gazette-evn/colorado-snow-conditions/actions
2. Click "Update Colorado Snow Conditions"
3. Click "Run workflow"
4. Wait ~5-7 minutes
5. Check your Google Sheet for data

### Step 4: Set Up Datawrapper Map (10 minutes)

1. **Go to Datawrapper:** https://app.datawrapper.de/
2. **Create → New Chart → Map**
3. **Choose map type:** "Symbol Map"
4. **Select region:** United States → Colorado
5. **Upload data:**
   - **Option A:** Publish your Google Sheet (File → Share → Publish to web)
     - Copy the published URL
     - Paste into Datawrapper "Link external dataset"
   - **Option B:** Export as CSV and upload directly
6. **Configure columns:**
   - **Latitude:** Latitude
   - **Longitude:** Longitude
   - **Size:** Base Depth or 24h Snowfall
   - **Color:** Status (Open = green, Closed = gray)
7. **Customize tooltips:**
   - Show: Resort Name, Status, Snow Data, Lifts
8. **Annotate & Design:**
   - Add title: "Colorado Ski Resort Conditions"
   - Add description
   - Choose colors
9. **Publish!**
   - Copy the Chart ID from the URL
   - Save for future reference

### Step 5: Set Up Auto-Refresh (Optional)

If you want Datawrapper to auto-update:

1. In Datawrapper chart settings
2. Go to "Publish & Embed"
3. Enable "Automatic data updates"
4. Set refresh interval (e.g., every 2 hours)
5. Connect to your published Google Sheet URL

---

## 🔄 How It Works (Once Deployed)

### Automated Updates (Every 2 Hours)

1. **GitHub Actions triggers** (schedule: `0 */2 * * *`)
2. **Scrapers run:**
   - OnTheSnow: Gets 5 open resorts with full data
   - CSCUSA: Gets 20 resorts (supplements OnTheSnow)
   - Combined: Merges to 23 unique resorts
3. **Google Sheets updates:**
   - Clears old data
   - Writes new data
   - Applies formatting
4. **Datawrapper refreshes:**
   - Reads from Google Sheet
   - Updates map visualization
   - Shows latest conditions

### Manual Trigger

Anytime you want to force an update:
1. Go to GitHub Actions
2. "Run workflow" button
3. Wait 5-7 minutes
4. Map updates automatically

---

## 📊 Data Flow

```
Colorado Ski Country USA          OnTheSnow
       (20 resorts)                (5 resorts)
              │                         │
              └────────┬────────────────┘
                       │
              ┌────────▼────────┐
              │ combined_scraper│
              │  (23 resorts)   │
              └────────┬────────┘
                       │
                       │ colorado_resorts_combined.csv
                       │
              ┌────────▼────────────────┐
              │ google_sheets_updater   │
              │  (Google Sheets API)    │
              └────────┬────────────────┘
                       │
              ┌────────▼────────┐
              │  Google Sheet   │
              │  (23 rows)      │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  Datawrapper    │
              │  Symbol Map     │
              └─────────────────┘
```

---

## 🐛 Troubleshooting

### "Permission denied" on Google Sheets
- Verify you shared the sheet with the service account email
- Check the email matches the JSON credentials

### Workflow fails on GitHub
- Check GitHub Secrets are set correctly
- View logs in Actions → Failed run → Artifacts

### Datawrapper not updating
- Verify published Sheet URL is correct
- Check "Automatic updates" is enabled in Datawrapper
- Try manual refresh in Datawrapper

### No data showing up
- Verify scrapers ran successfully (check logs)
- Confirm Google Sheet has data
- Check column mappings in Datawrapper

---

## 📈 Monitoring

**Check these regularly:**

1. **GitHub Actions:** https://github.com/gazette-evn/colorado-snow-conditions/actions
   - Should show green checkmarks every 2 hours
   
2. **Google Sheet:** Your sheet URL
   - Should update every 2 hours
   - Check "Last Updated" column
   
3. **Datawrapper Map:** Your chart URL
   - Should reflect latest Google Sheet data

---

## 🎿 Next Steps After Deployment

Once the map is working:
1. Embed the map on your website
2. Share the public URL
3. Monitor throughout ski season
4. Consider adding the table view (same data, sortable format)

---

## 💡 Cost Breakdown

- **GitHub Actions:** FREE (within free tier limits)
- **Google Sheets API:** FREE
- **Google Cloud:** FREE (no API usage charges)
- **Datawrapper:** Your current plan
- **Total:** $0/month for scraping & data pipeline! 🎉

