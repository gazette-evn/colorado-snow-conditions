# API Key Status

## ✅ Configured and Ready

### Datawrapper API
- **Status:** ✅ Configured in `.env`
- **Key:** `EFDvH4j...` (first 7 chars)
- **Location:** `.env` file

### RapidAPI Key  
- **Status:** ✅ Configured in `.env`
- **Key:** `0b51d28...` (first 7 chars)
- **API:** Ski Resorts and Conditions
- **Host:** `ski-resorts-and-conditions.p.rapidapi.com`
- **Location:** `.env` file

## ⏳ Still Needed

### Datawrapper Chart IDs

After creating your charts in Datawrapper, add these to `.env`:

```bash
SNOW_MAP_CHART_ID=xxxxx      # From your locator map URL
SNOW_TABLE_CHART_ID=yyyyy    # From your table chart URL
```

**How to get Chart IDs:**
1. Create chart in Datawrapper
2. Look at the URL: `https://app.datawrapper.de/chart/AbC12/visualize`
3. The ID is: `AbC12`
4. Add to `.env` file

---

## GitHub Secrets (for automation)

When you're ready to deploy, add these as GitHub repository secrets:

- `DATAWRAPPER_API_KEY`
- `RAPIDAPI_KEY`  
- `SNOW_MAP_CHART_ID`
- `SNOW_TABLE_CHART_ID`

**Location:** GitHub repo → Settings → Secrets and variables → Actions

---

## Test Your Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Test API connection
python test_skiapi.py
```

If you see "✅ SUCCESS!" with Colorado resort data, you're all set!

