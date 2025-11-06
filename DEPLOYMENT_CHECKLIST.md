# Deployment Checklist

Quick reference for deploying the Colorado Snow Conditions pipeline.

## Pre-Deployment

- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] GitHub account created
- [ ] Datawrapper account created
- [ ] skiapi.com account and API key obtained

## Local Setup

- [ ] Clone repository
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file with all keys
- [ ] Test skiapi.com connection: `python test_skiapi.py`
- [ ] Update API endpoints in `ski_api_fetcher.py` if needed

## Datawrapper Setup

- [ ] Create locator map in Datawrapper
- [ ] Copy map Chart ID to `.env`
- [ ] Create table in Datawrapper
- [ ] Copy table Chart ID to `.env`

## Local Testing

- [ ] Run `python ski_api_fetcher.py` - should create CSV
- [ ] Run `python snow_map.py` - should update map
- [ ] Run `python snow_table.py` - should update table
- [ ] Run `python run_all_updates.py` - should update both
- [ ] Verify visualizations look correct in Datawrapper

## GitHub Deployment

- [ ] Create GitHub repository
- [ ] Push code: `git push origin main`
- [ ] Add GitHub secrets:
  - `DATAWRAPPER_API_KEY`
  - `SKIAPI_KEY`
  - `SNOW_MAP_CHART_ID`
  - `SNOW_TABLE_CHART_ID`
- [ ] Test manual workflow run
- [ ] Verify automated schedule is active
- [ ] Check logs in GitHub Actions

## Post-Deployment

- [ ] Monitor first few automated runs
- [ ] Verify data accuracy
- [ ] Adjust update frequency if needed
- [ ] Embed visualizations on website (optional)
- [ ] Set up notifications for failures (optional)

## Maintenance

### Weekly
- [ ] Check GitHub Actions for any failures
- [ ] Review logs for warnings

### Monthly  
- [ ] Verify data accuracy
- [ ] Check for API changes
- [ ] Update dependencies if needed: `pip install --upgrade -r requirements.txt`

### Seasonal (Start/End of Ski Season)
- [ ] Adjust update frequency as needed
- [ ] Verify all resorts are reporting correctly
- [ ] Update visualization titles/descriptions

---

## Quick Commands Reference

```bash
# Activate environment
source venv/bin/activate

# Test API
python test_skiapi.py

# Run updates locally
python run_all_updates.py

# View logs
grep ERROR *.log
tail -f master_update.log

# Update dependencies
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

---

## Troubleshooting Quick Fixes

**Map not updating?**
```bash
python snow_map.py
# Check output for specific error
```

**Table not updating?**
```bash
python snow_table.py
# Check output for specific error
```

**API connection issues?**
```bash
python test_skiapi.py
# Verify API key and endpoints
```

**GitHub Actions failing?**
- Check repository Secrets are set correctly
- Review workflow run logs in Actions tab
- Download log artifacts for details

---

## Emergency Shutdown

To temporarily stop automated updates:

1. Go to GitHub repository → Settings → Actions
2. Disable Actions for this repository
3. Re-enable when ready to resume

Or delete the workflow file:
```bash
git rm .github/workflows/update-snow-data.yml
git commit -m "Temporarily disable automation"
git push
```

---

✅ **Once all items are checked, your pipeline is production-ready!**

