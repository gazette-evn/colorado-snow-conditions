# GitHub Actions Troubleshooting Guide

## 🔧 Recent Fixes Applied

### What Was Wrong:

1. **Workflow running on every push** ❌
   - Triggered on every commit to `main` branch
   - Caused unnecessary scraping attempts
   - Potentially hit rate limits

2. **Missing error diagnostics** ❌
   - Hard to tell what was failing
   - No verification of environment variables
   - Logs not shown in workflow output

3. **No timeout protection** ❌
   - Workflows could hang indefinitely
   - Wasted GitHub Actions minutes

### What Was Fixed:

1. **Removed push trigger** ✅
   - Now only runs on schedule (every 2 hours) or manual trigger
   - Prevents excessive scraping

2. **Added environment variable checks** ✅
   - Verifies `GOOGLE_SHEETS_SPREADSHEET_ID` is set
   - Verifies `GOOGLE_CREDENTIALS` is set
   - Fails fast with clear error message if missing

3. **Enhanced logging** ✅
   - Shows last 50 lines of master_update.log in workflow
   - Uploads more debug files (CSV, HTML)
   - Always uploads artifacts, even on failure

4. **Added timeout** ✅
   - 15-minute maximum per workflow run
   - Prevents runaway jobs

---

## 🔍 How to Debug Future Failures

### Step 1: Check the Workflow Run

Go to: https://github.com/gazette-evn/colorado-snow-conditions/actions

Look at the failed run and check:

1. **Which step failed?**
   - "Verify environment variables" → Secrets not configured
   - "Install Chrome" → Ubuntu/Chrome issue
   - "Scrape data" → Scraping or Google Sheets issue

### Step 2: Download Artifacts

1. Scroll to bottom of failed workflow run
2. Click "update-logs-XXXXX" under Artifacts
3. Download and unzip
4. Check the log files:
   - `master_update.log` - Overall pipeline status
   - `combined_scraper.log` - Scraping details
   - `onthesnow_scraper.log` - OnTheSnow scraper
   - `colorado_scraper.log` - CSCUSA scraper
   - `google_sheets_updater.log` - Google Sheets upload

### Step 3: Check Logs for Common Errors

**If you see:** `GOOGLE_SHEETS_SPREADSHEET_ID is not set`
- **Fix:** Add the secret in GitHub repository settings
- Go to: Settings → Secrets and variables → Actions
- Add `GOOGLE_SHEETS_SPREADSHEET_ID` = `10sbXOC-cl-pVZZWzqx0jNp9YJcxgXD4FRELy91flFBI`

**If you see:** `GOOGLE_CREDENTIALS is not set`
- **Fix:** Add the Google service account JSON as a secret
- Go to: Settings → Secrets and variables → Actions
- Add `GOOGLE_CREDENTIALS` = (paste the entire JSON from `.env`)

**If you see:** `403 Forbidden` or `Permission denied`
- **Fix:** Check Google Sheets permissions
- Make sure the service account email has Editor access to the sheet
- Service account: `colorado-snow-bot@colorado-snow-conditions.iam.gserviceaccount.com`

**If you see:** `Chrome not found` or `Selenium error`
- **Fix:** Chrome installation issue in GitHub Actions
- The workflow should handle this automatically
- Try re-running the workflow (sometimes transient)

**If you see:** `No data scraped`
- **Fix:** Website structure may have changed
- Check if OnTheSnow or CSCUSA changed their HTML
- May need to update scraper selectors

**If you see:** `Timeout` errors
- **Fix:** Scrapers taking too long
- Network might be slow from GitHub Actions
- Increase timeout in `run_all_updates.py` (currently 5 min per script)

---

## 🎯 Quick Checks

### Are Secrets Configured?

Go to: https://github.com/gazette-evn/colorado-snow-conditions/settings/secrets/actions

You should see:
- ✅ `GOOGLE_CREDENTIALS`
- ✅ `GOOGLE_SHEETS_SPREADSHEET_ID`

If missing, add them:

```bash
# GOOGLE_SHEETS_SPREADSHEET_ID
10sbXOC-cl-pVZZWzqx0jNp9YJcxgXD4FRELy91flFBI

# GOOGLE_CREDENTIALS (paste entire JSON from .env file)
{"type":"service_account","project_id":"colorado-snow-conditions",...}
```

### Is the Workflow Enabled?

Go to: https://github.com/gazette-evn/colorado-snow-conditions/actions

- Check if the workflow is listed under "All workflows"
- If disabled, click on it and enable

### Is the Sheet Shared?

1. Open: https://docs.google.com/spreadsheets/d/10sbXOC-cl-pVZZWzqx0jNp9YJcxgXD4FRELy91flFBI
2. Click "Share" button
3. Check if `colorado-snow-bot@colorado-snow-conditions.iam.gserviceaccount.com` has Editor access
4. If not, add it

---

## 🔄 Manual Testing

### Test Workflow Manually

1. Go to: https://github.com/gazette-evn/colorado-snow-conditions/actions
2. Click "Update Colorado Snow Conditions" workflow
3. Click "Run workflow" (top right)
4. Select "main" branch
5. Click green "Run workflow" button
6. Wait 5-10 minutes and check results

### Test Locally

```bash
cd /Users/evanwyloge/snow-conditions-data
source venv/bin/activate

# Test the complete pipeline
python run_all_updates.py

# Or test individual components
python combined_scraper.py
python google_sheets_updater.py
```

---

## 📊 Understanding the Workflow

### Schedule

```yaml
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
```

**Runs at (UTC):**
- 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00

**Convert to Mountain Time (MST = UTC-7):**
- 5pm, 7pm, 9pm, 11pm, 1am, 3am, 5am, 7am, 9am, 11am, 1pm, 3pm

### Steps

1. **Checkout repository** - Get latest code
2. **Set up Python** - Install Python 3.11
3. **Install dependencies** - Install all packages from requirements.txt
4. **Install Chrome** - Install headless Chrome for Selenium
5. **Verify environment** - Check secrets are configured
6. **Scrape and update** - Run combined scraper + Google Sheets updater
7. **Upload artifacts** - Save logs for debugging
8. **Notify on failure** - Mark workflow as failed if any step fails

### Timeout

- Workflow will auto-cancel after **15 minutes**
- Individual scripts timeout after **5 minutes**

---

## ⚠️ Common Pitfalls

### 1. Forgetting to Add Secrets

**Symptom:** "GOOGLE_SHEETS_SPREADSHEET_ID is not set!"

**Fix:** Add secrets in GitHub repository settings

### 2. Invalid JSON in GOOGLE_CREDENTIALS

**Symptom:** "Failed to parse credentials" or JSON errors

**Fix:** 
- Copy the ENTIRE JSON from `.env` file
- Make sure it's valid JSON (use jsonlint.com to verify)
- No extra quotes or escape characters

### 3. Sheet Permissions

**Symptom:** "403 Forbidden" when updating sheet

**Fix:** Share sheet with service account email (Editor access)

### 4. Rate Limiting

**Symptom:** Scrapers get 429 or 403 errors

**Fix:** 
- Reduce scraping frequency (change cron to `0 */4 * * *` for every 4 hours)
- OnTheSnow and CSCUSA may block too-frequent requests

### 5. Website Structure Changes

**Symptom:** "Extracted 0 resorts" or "No data found"

**Fix:**
- Websites changed their HTML structure
- Need to update scraper CSS selectors
- Check saved `*_rendered.html` files in artifacts to see current structure

---

## 🚨 Emergency: Stop the Workflow

If something is wrong and you need to stop automated runs:

### Option 1: Disable Workflow
1. Go to: https://github.com/gazette-evn/colorado-snow-conditions/actions
2. Click "Update Colorado Snow Conditions"
3. Click "..." menu (top right)
4. Select "Disable workflow"

### Option 2: Change Schedule
1. Edit `.github/workflows/update-snow-data.yml`
2. Comment out the schedule:
```yaml
# schedule:
#   - cron: '0 */2 * * *'
```
3. Commit and push

### Option 3: Delete Workflow File
1. Delete `.github/workflows/update-snow-data.yml`
2. Commit and push

---

## ✅ Success Indicators

A successful run should show:

```
✅ GOOGLE_SHEETS_SPREADSHEET_ID is set
✅ GOOGLE_CREDENTIALS is set (2354 characters)
✅ Combined Resort Data Scraper completed successfully
✅ Google Sheets Update completed successfully
Completed: 2/2 updates successful
```

And your Google Sheet will be updated with fresh data!

---

## 📞 Getting Help

**If you're still stuck:**

1. Download the artifacts from the failed workflow run
2. Look at all the `.log` files
3. Check which step failed
4. Look for error messages in the logs
5. Common errors are documented above

**The logs will tell you:**
- Which resort data was successfully scraped
- How many resorts were found
- If coordinates were added
- If Google Sheets authentication worked
- What data was uploaded

**Most issues are:**
- Missing secrets (90%)
- Sheet permissions (5%)
- Website structure changes (5%)

