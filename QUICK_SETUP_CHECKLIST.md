# Quick Setup Checklist

Use this checklist to get your Colorado Snow Conditions pipeline running!

---

## ✅ What's Already Done

- [x] Scrapers working (23 resorts)
- [x] GitHub repo set up
- [x] GitHub Actions configured
- [x] Code pushed to GitHub

---

## 🔧 What You Need To Do

### Part 1: Google Cloud Setup (15 min)

- [ ] **1.1** Create Google Cloud project at https://console.cloud.google.com/
- [ ] **1.2** Enable Google Sheets API
- [ ] **1.3** Create service account named `colorado-snow-bot`
- [ ] **1.4** Download service account JSON key file
- [ ] **1.5** Copy the `client_email` from JSON (you'll need it next)

### Part 2: Google Sheet Setup (5 min)

- [ ] **2.1** Create new Google Sheet at https://sheets.google.com
- [ ] **2.2** Name it: "Colorado Snow Conditions"
- [ ] **2.3** Copy Sheet ID from URL: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
- [ ] **2.4** Share sheet with service account email (from 1.5)
- [ ] **2.5** Give "Editor" access

### Part 3: GitHub Secrets (5 min)

Go to: https://github.com/gazette-evn/colorado-snow-conditions/settings/secrets/actions

- [ ] **3.1** Add secret `GOOGLE_SHEETS_SPREADSHEET_ID` = your sheet ID
- [ ] **3.2** Add secret `GOOGLE_CREDENTIALS` = entire JSON from service account key

### Part 4: Test It! (5 min)

- [ ] **4.1** Go to https://github.com/gazette-evn/colorado-snow-conditions/actions
- [ ] **4.2** Click "Update Colorado Snow Conditions"
- [ ] **4.3** Click "Run workflow" → "Run workflow"
- [ ] **4.4** Wait ~5-7 minutes
- [ ] **4.5** Check your Google Sheet - should have 23 resorts!

### Part 5: Datawrapper Map (10 min)

- [ ] **5.1** Go to https://app.datawrapper.de/
- [ ] **5.2** Create → Map → Symbol Map
- [ ] **5.3** Select Colorado as region
- [ ] **5.4** Publish your Google Sheet (File → Share → Publish to web)
- [ ] **5.5** Link external dataset in Datawrapper (paste published URL)
- [ ] **5.6** Map columns:
  - Latitude → Latitude
  - Longitude → Longitude
  - Tooltip → Resort Name, Status, Snow Data
- [ ] **5.7** Design and customize
- [ ] **5.8** Publish map!

---

## 🎉 Done!

Your pipeline is now:
```
GitHub Actions (every 2 hours)
    ↓
Scrapes OnTheSnow + CSCUSA
    ↓
Updates Google Sheet
    ↓
Datawrapper Map Auto-Updates
```

**Completely automated!** ❄️

---

## 📞 Need Help?

**Getting errors?** Check:
1. [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) - Detailed setup steps
2. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment walkthrough
3. GitHub Actions logs - Download artifacts to see what failed

**Test locally first:**
```bash
python test_google_sheets.py  # Verify API connection
python combined_scraper.py     # Test scraping
python google_sheets_updater.py # Test Sheets upload
```

