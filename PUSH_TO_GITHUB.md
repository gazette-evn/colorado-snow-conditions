# Push to GitHub - Quick Guide

## Step 1: Create GitHub Repository

1. **Go to:** https://github.com/new
2. **Repository name:** `colorado-snow-conditions` (or your choice)
3. **Description:** "Automated Colorado ski resort conditions with live map and table"
4. **Visibility:** 
   - Public (recommended - free GitHub Actions)
   - Or Private (if you prefer)
5. **DO NOT check:**
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
   - (We already have these files!)
6. **Click:** "Create repository"

## Step 2: Push Your Code

GitHub will show you commands - use these:

```bash
cd /Users/evanwyloge/snow-conditions-data

# Add GitHub remote
git remote add origin https://github.com/gazette-evn/colorado-snow-conditions.git

# Push to GitHub
git push -u origin main
```

## Step 3: Run Test Workflow

1. Go to: https://github.com/gazette-evn/colorado-snow-conditions
2. Click **"Actions"** tab (top menu)
3. You'll see **"Test Colorado Ski Scraper"** in the left sidebar
4. Click on it
5. Click **"Run workflow"** button (top right)
6. Select branch: `main`
7. Click green **"Run workflow"** button

## Step 4: Watch It Run

- ⏳ Takes 2-3 minutes
- Yellow dot = Running
- ✅ Green check = Success!
- ❌ Red X = Failed

Click on the run to see live logs!

## Step 5: Download Results

1. Scroll down on the run page
2. Find **"Artifacts"** section
3. Download `scraper-test-results-1` (or similar)
4. Unzip and review:
   - `colorado_resorts_scraped.csv` - Raw scraper output
   - `colorado_resorts_final.csv` - With coordinates
   - Logs

---

## ✅ Expected Success

**In the logs:**
```
✅ Chrome driver initialized successfully
✅ Extracted 28 resorts
✅ Saved data to colorado_resorts_scraped.csv
Total resorts: 28
```

**In the CSV:**
- 28 Colorado ski resorts
- Current snow conditions
- Trails open/closed
- Coordinates for mapping

---

## 🎯 After Success

Once the test works:
1. ✅ Scraper is production-ready!
2. Create Datawrapper charts
3. Integrate with Datawrapper
4. Enable automated updates

---

**Ready? Create the repo and run these commands!** 🚀

