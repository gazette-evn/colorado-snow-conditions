# Colorado Snow Conditions - Setup Guide

## Step-by-Step Setup Instructions

### Step 1: Initial Environment Setup (5 minutes)

```bash
# Navigate to project directory
cd snow-conditions-data

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get skiapi.com API Key

1. Visit https://skiapi.com
2. Sign up for an account or log in
3. Navigate to API section / Developer Dashboard
4. Generate or copy your API key
5. Save it for the next step

### Step 3: Get Datawrapper API Token

1. Visit https://app.datawrapper.de/
2. Create account or log in
3. Go to Settings → API Tokens: https://app.datawrapper.de/account/api-tokens
4. Click "Create new token"
5. Give it a name like "Colorado Snow Conditions"
6. Copy the token (you won't be able to see it again!)

### Step 4: Create .env File

Create a file named `.env` in the project root:

```bash
# Copy the example (if it exists) or create from scratch
cat > .env << 'EOF'
# API Credentials
DATAWRAPPER_API_KEY=paste_your_datawrapper_token_here
SKIAPI_KEY=paste_your_skiapi_key_here

# Datawrapper Chart IDs (leave blank for now, will fill in step 6)
SNOW_MAP_CHART_ID=
SNOW_TABLE_CHART_ID=
EOF
```

⚠️ **IMPORTANT**: Never commit your `.env` file to git. It's already in `.gitignore`.

### Step 5: Test the skiapi.com Connection

```bash
python test_skiapi.py
```

**What to look for:**
- ✅ "API Key loaded: Yes"
- ✅ Response with status code 200
- ✅ JSON data showing resort information

**If it fails:**
- Check your SKIAPI_KEY is correct
- Review the API documentation for correct endpoint URLs
- Update `ski_api_fetcher.py` with correct endpoints based on test output

**Action Required:**
Based on the test output, you may need to update the API endpoints and column mappings in `ski_api_fetcher.py`:
- Update `SKIAPI_BASE_URL`
- Update endpoint paths in `fetch_colorado_resorts()`
- Update `column_mapping` dictionary to match actual API field names

### Step 6: Create Datawrapper Visualizations

#### Create the Map

1. Go to https://app.datawrapper.de/
2. Click **"New Chart"** → **"New Map"**
3. Choose **"Locator Map"** (symbol map)
4. Search for "Colorado" and select the Colorado region
5. Click **"Proceed"**
6. In the data step, you can upload sample data or just proceed
   - Sample CSV format:
   ```csv
   lat,lng,resort_name
   39.6403,-106.3742,Vail
   39.4817,-106.0384,Breckenridge
   ```
7. Click **"Proceed"** to the visualize step
8. Customize as desired:
   - Set zoom level to show all of Colorado
   - Choose marker color
   - Set title: "Colorado Ski Resort Conditions"
9. Click **"Proceed"** to publish
10. Copy the Chart ID from the URL
    - URL looks like: `https://app.datawrapper.de/chart/AbC12/visualize`
    - Chart ID is: `AbC12`
11. Add to your `.env` file as `SNOW_MAP_CHART_ID=AbC12`

#### Create the Table

1. In Datawrapper, click **"New Chart"** → **"New Table"**
2. Upload sample data or paste:
   ```csv
   Resort,24h Snow (in),Base Depth (in),Lifts Open,Status
   Vail,2,45,15,Open
   Breckenridge,3,38,12,Open
   ```
3. Click **"Proceed"**
4. In visualize step:
   - Enable "Make columns sortable"
   - Customize styling (colors, fonts, etc.)
   - Set title: "Colorado Ski Resorts - Conditions Table"
5. Click **"Proceed"** to publish
6. Copy the Chart ID from the URL
7. Add to your `.env` file as `SNOW_TABLE_CHART_ID=XyZ78`

Your `.env` should now look like:
```bash
DATAWRAPPER_API_KEY=your_actual_token
SKIAPI_KEY=your_actual_key
SNOW_MAP_CHART_ID=AbC12
SNOW_TABLE_CHART_ID=XyZ78
```

### Step 7: Test Each Script Individually

```bash
# Test data fetching
python ski_api_fetcher.py
# Should create colorado_resorts_current.csv

# Test map update
python snow_map.py
# Check your Datawrapper map - should show all CO resorts

# Test table update  
python snow_table.py
# Check your Datawrapper table - should show resort data

# Test master script
python run_all_updates.py
# Should run both map and table updates
```

### Step 8: Set Up GitHub Actions (Optional but Recommended)

#### Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial setup of Colorado snow conditions pipeline"

# Create GitHub repository and push
# (Follow GitHub's instructions for your new repo)
git branch -M main
git remote add origin https://github.com/yourusername/snow-conditions-data.git
git push -u origin main
```

#### Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add each of these secrets:
   - Name: `DATAWRAPPER_API_KEY`, Value: your token
   - Name: `SKIAPI_KEY`, Value: your API key
   - Name: `SNOW_MAP_CHART_ID`, Value: your map chart ID
   - Name: `SNOW_TABLE_CHART_ID`, Value: your table chart ID

#### Test GitHub Actions

1. Go to **Actions** tab in your repository
2. Click **"Update Colorado Snow Conditions"** workflow
3. Click **"Run workflow"** → **"Run workflow"** (manual trigger)
4. Wait for it to complete (usually 1-2 minutes)
5. Check your Datawrapper visualizations - they should be updated!
6. Click on the completed run → **Artifacts** → Download logs to review

### Step 9: Verify Automated Schedule

The workflow is configured to run every 2 hours automatically. You can:
- Check the Actions tab to see scheduled runs
- Modify the schedule in `.github/workflows/update-snow-data.yml` if needed
- View logs for each run

---

## Verification Checklist

- [ ] Python virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] skiapi.com API key obtained and added to .env
- [ ] Datawrapper API token obtained and added to .env
- [ ] test_skiapi.py runs successfully and shows data
- [ ] ski_api_fetcher.py updated with correct API endpoints (if needed)
- [ ] Datawrapper map created and chart ID added to .env
- [ ] Datawrapper table created and chart ID added to .env
- [ ] snow_map.py runs and updates the map successfully
- [ ] snow_table.py runs and updates the table successfully
- [ ] run_all_updates.py executes both updates successfully
- [ ] Code pushed to GitHub repository
- [ ] GitHub secrets configured
- [ ] GitHub Actions workflow tested manually
- [ ] Automated schedule verified

---

## Common Issues and Solutions

### Issue: "No module named 'dotenv'"
**Solution:** Make sure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "DATAWRAPPER_API_KEY not set in .env"
**Solution:** 
1. Verify `.env` file exists in project root
2. Check that it contains `DATAWRAPPER_API_KEY=your_token`
3. No spaces around the `=`
4. Token should not be in quotes

### Issue: "Unauthorized" error from skiapi.com
**Solution:**
1. Verify your API key is correct
2. Check if API requires different authentication (Bearer token vs API key)
3. Review skiapi.com documentation for auth requirements

### Issue: Charts not updating
**Solution:**
1. Verify chart IDs are correct (check Datawrapper URLs)
2. Make sure charts are published (not just saved)
3. Check logs for specific error messages
4. Verify API rate limits aren't exceeded

### Issue: Column mapping errors
**Solution:**
After running `test_skiapi.py`, update the `column_mapping` in `ski_api_fetcher.py` to match the actual field names from the API.

---

## Next Steps

Once everything is working:

1. **Customize visualizations** in Datawrapper (colors, fonts, layout)
2. **Embed visualizations** on your website using Datawrapper embed codes
3. **Adjust update frequency** in GitHub Actions workflow
4. **Add filtering** for specific resorts (edit `ski_api_fetcher.py`)
5. **Monitor logs** to ensure reliable operation

---

## Support Resources

- **Datawrapper Documentation**: https://developer.datawrapper.de/
- **Python Datawrapper Library**: https://github.com/chekos/datawrapper
- **GitHub Actions Documentation**: https://docs.github.com/en/actions

---

**You're all set! Your Colorado snow conditions pipeline should now be running automatically.** 🎿

