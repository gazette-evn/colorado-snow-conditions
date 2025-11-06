# Testing the Scraper on GitHub Actions

## 🚀 Quick Test Steps

### Step 1: Initialize Git (if not done)

```bash
cd /Users/evanwyloge/snow-conditions-data
git init
git add .
git commit -m "Initial commit - Colorado ski conditions scraper"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Name it: `colorado-snow-conditions` (or whatever you prefer)
3. **Don't** initialize with README (we already have files)
4. Create repository

### Step 3: Push Code to GitHub

```bash
# Link to your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/colorado-snow-conditions.git
git branch -M main
git push -u origin main
```

### Step 4: Run Test Workflow

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Find **"Test Colorado Ski Scraper"** in the left sidebar
4. Click **"Run workflow"** dropdown (top right)
5. Click green **"Run workflow"** button

### Step 5: Watch It Run (2-3 minutes)

You'll see:
- ⏳ Orange dot = Running
- ✅ Green check = Success!
- ❌ Red X = Failed

Click on the run to see detailed logs!

### Step 6: Check Results

1. Click on the completed run
2. Scroll down to **"Artifacts"**
3. Download `scraper-test-results-XXX.zip`
4. Unzip and review:
   - `colorado_resorts_scraped.csv` - Raw scraper output
   - `colorado_resorts_final.csv` - Processed with coordinates
   - Log files - Detailed execution logs

---

## ✅ What Success Looks Like

**In the logs, you should see:**
```
✅ Chrome driver initialized successfully
✅ Page body loaded
✅ Extracted 28 resorts
✅ Saved data to colorado_resorts_scraped.csv
✅ Processed data for 28 resorts
```

**In the CSV files:**
- 28 Colorado resorts
- Columns: name, new_snow_24h, trails_open, conditions, lat/lng
- Current data (today's date)

---

## 🐛 If It Fails

### Common Issues:

**"No resort data found"**
- Colorado Ski Country USA changed their page structure
- Need to adjust parsing logic
- Check `colorado_ski_page_rendered.html` artifact to see actual HTML

**"Chrome driver failed"**
- Usually auto-fixed by GitHub Actions setup
- Check if Chrome installation step succeeded

**"Timeout"**
- Page took too long to load
- Can increase wait time in `colorado_ski_scraper.py`

---

## 📝 What to Look For

Download the artifacts and check:

1. **`colorado_resorts_scraped.csv`** - Should have ~28 rows
2. **Row format:** Resort name, snow, trails, conditions
3. **`colorado_resorts_final.csv`** - Should have lat/lng added
4. **Logs** - Any warnings about missing data

---

## 🎯 After Successful Test

Once the scraper works on GitHub:

1. ✅ **Scraper is production-ready!**
2. 📊 **Create Datawrapper charts** (map & table)
3. 🔗 **Integrate with Datawrapper** (update snow_map.py & snow_table.py)
4. ⚙️ **Switch to main workflow** (update-snow-data.yml)
5. 🎉 **Go live with automated updates!**

---

## 💡 Quick Start

```bash
# 1. Create GitHub repo
# 2. Run these commands:

cd /Users/evanwyloge/snow-conditions-data
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main

# 3. Go to GitHub → Actions → "Test Colorado Ski Scraper" → Run workflow
# 4. Wait 2-3 minutes
# 5. Download artifacts and review!
```

---

**Ready to push to GitHub?** Let me know your GitHub username and I can help with the exact commands! 🚀

