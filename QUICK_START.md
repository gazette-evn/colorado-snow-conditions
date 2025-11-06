# Quick Start - Your API Keys Are Ready!

✅ **Your `.env` file has been created with your API keys!**

## Next Steps (5 minutes to test)

### 1. Install Dependencies

```bash
cd /Users/evanwyloge/snow-conditions-data
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test the RapidAPI Connection

```bash
python test_skiapi.py
```

**This will:**
- Connect to the RapidAPI "Ski Resorts and Conditions" API
- Show you what data is available
- Display Colorado resort information
- Help verify everything is working

**Look for:**
- ✅ "API Key loaded: Yes"
- ✅ Status Code: 200
- ✅ JSON data showing ski resorts

### 3. Review the Output

The test script will show you:
- The data structure from the API
- What fields are available (snow depth, lifts, conditions, etc.)
- Which Colorado resorts are included

**If the column names in the API don't match what we expect**, you may need to update the `column_mapping` in `ski_api_fetcher.py`.

### 4. Create Your Datawrapper Charts

Once you confirm the API works, create two visualizations in Datawrapper:

**A. Create the Map**
1. Go to https://app.datawrapper.de/
2. New Chart → Locator Map
3. Search for "Colorado"
4. Note the Chart ID from the URL (e.g., `AbC12`)
5. Add to `.env`: `SNOW_MAP_CHART_ID=AbC12`

**B. Create the Table**
1. New Chart → Table
2. Upload sample data or create blank
3. Note the Chart ID
4. Add to `.env`: `SNOW_TABLE_CHART_ID=XyZ78`

### 5. Test the Full Pipeline

```bash
# Test map update
python snow_map.py

# Test table update
python snow_table.py

# Run everything
python run_all_updates.py
```

### 6. Check Your Visualizations

Go to Datawrapper and verify:
- Map shows Colorado ski resort markers
- Table shows resort data with snow conditions
- Data looks accurate

---

## Your API Keys

✅ **Datawrapper:** Already configured in `.env`
✅ **RapidAPI:** Already configured in `.env`

Just need to add:
- `SNOW_MAP_CHART_ID` - after creating map
- `SNOW_TABLE_CHART_ID` - after creating table

---

## If Something Goes Wrong

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API Key not found"
Check that `.env` file exists in the project root (it should - we created it!)

### "Unauthorized" or "403"
- Verify your RapidAPI subscription is active
- Check you're subscribed to "Ski Resorts and Conditions" API
- Verify API key is correct in `.env`

### Column mapping errors
After running `test_skiapi.py`, update the `column_mapping` dictionary in `ski_api_fetcher.py` to match the actual API field names.

---

## What Happens Next

Once everything works locally:

1. **Push to GitHub**
2. **Add secrets** to GitHub repository
3. **GitHub Actions** will run automatically every 2 hours
4. **Visualizations** update with fresh data

No more manual work needed! ⛷️

---

**Run `python test_skiapi.py` now to get started!**

