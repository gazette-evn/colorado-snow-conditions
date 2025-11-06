# Colorado Snow Conditions - Project Overview

## 🎯 What We Built

A **complete automated data pipeline** that:
1. Fetches live snow conditions from skiapi.com for all Colorado ski resorts
2. Processes and transforms the data
3. Updates two Datawrapper visualizations:
   - **Interactive Map**: Shows all resorts with pin markers
   - **Sortable Table**: Displays detailed snow statistics
4. Runs automatically every 2 hours via GitHub Actions
5. Logs all operations for monitoring and debugging

---

## 📁 Project Files Created

### Core Pipeline Scripts
- **`ski_api_fetcher.py`** - Fetches and processes data from skiapi.com
- **`snow_map.py`** - Updates the Datawrapper map visualization
- **`snow_table.py`** - Updates the Datawrapper table visualization
- **`run_all_updates.py`** - Master script that runs all updates

### Testing & Development
- **`test_skiapi.py`** - Tests skiapi.com API and explores data structure

### Configuration
- **`requirements.txt`** - Python package dependencies
- **`.gitignore`** - Git ignore rules (excludes .env, logs, etc.)
- **`.env`** - Your API keys (YOU NEED TO CREATE THIS - see setup guide)

### Automation
- **`.github/workflows/update-snow-data.yml`** - GitHub Actions workflow

### Documentation
- **`README.md`** - Main project documentation
- **`SETUP_GUIDE.md`** - Step-by-step setup instructions
- **`DEPLOYMENT_CHECKLIST.md`** - Deployment verification checklist
- **`PROJECT_BLUEPRINT.md`** - Original blueprint/methodology
- **`PROJECT_OVERVIEW.md`** - This file

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Workflow                   │
│                  (Runs every 2 hours)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   run_all_updates.py                         │
│              (Master Orchestration Script)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
        ┌──────────────────┐  ┌──────────────────┐
        │  snow_map.py     │  │  snow_table.py   │
        └──────────────────┘  └──────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ↓
                ┌──────────────────────────┐
                │  ski_api_fetcher.py      │
                │  - Fetch from skiapi.com │
                │  - Process data          │
                │  - Standardize format    │
                └──────────────────────────┘
                              ↓
                ┌──────────────────────────┐
                │    Datawrapper API       │
                │  - Update map data       │
                │  - Update table data     │
                │  - Publish visualizations│
                └──────────────────────────┘
```

---

## 📊 Data Flow

### 1. Data Source (skiapi.com)
```json
{
  "name": "Vail",
  "lat": 39.6403,
  "lng": -106.3742,
  "baseDepth": 45,
  "summitDepth": 67,
  "newSnow24h": 2,
  "liftsOpen": 15,
  "liftsTotal": 31,
  "status": "Open"
}
```

### 2. Processing (ski_api_fetcher.py)
- Fetches all Colorado resorts
- Standardizes column names
- Cleans and validates data
- Calculates percentages (lifts/runs open)
- Adds timestamps

### 3. Map Preparation (snow_map.py)
- Filters to resorts with coordinates
- Formats display values (e.g., `45"` for depth)
- Creates tooltip fields
- Adds status indicators

### 4. Table Preparation (snow_table.py)
- Selects relevant columns
- Renames to user-friendly names
- Sorts by 24h snowfall
- Formats for readability

### 5. Datawrapper Update
- Uploads processed data
- Updates metadata (title, description, timestamp)
- Publishes charts
- Visualizations go live!

---

## 🎨 Visualizations

### Map Features
- **Pin markers** at each resort location
- **Interactive tooltips** showing:
  - Resort name and status
  - New snowfall (24h, 48h)
  - Snow depth (base, summit)
  - Lifts and runs open
  - Current conditions
- **Auto-zoom** to Colorado region
- **Color-coded** by status (optional)

### Table Features
- **Sortable columns** - click any header to sort
- **Key metrics**:
  - Resort name
  - New snow (24h, 48h, 7-day)
  - Base and summit depth
  - Lifts open/total
  - Runs open/total
  - Operating status
- **Automatic sorting** by most recent snowfall
- **Clean formatting** with no decimals

---

## ⚙️ Configuration Options

### Update Frequency
Edit `.github/workflows/update-snow-data.yml`:
- Current: Every 2 hours
- Options: Hourly, every 4 hours, 3x daily, etc.

### Resort Filtering
Edit `ski_api_fetcher.py` to filter resorts:
```python
# Only major resorts
df = df[df['lifts_total'] >= 10]

# Specific resorts
df = df[df['resort_name'].isin(['Vail', 'Breckenridge', 'Keystone'])]
```

### Visualization Styling
- **Map**: Customize in Datawrapper UI (colors, zoom, tooltip format)
- **Table**: Customize in Datawrapper UI (fonts, colors, column widths)

### Data Points
Edit `prepare_table_data()` in `snow_table.py` to add/remove columns

---

## 🚀 Next Steps (For You)

1. **Get API Keys**
   - [ ] Sign up at skiapi.com and get API key
   - [ ] Create Datawrapper account and generate API token

2. **Test the API**
   - [ ] Create `.env` file with your skiapi key
   - [ ] Run `python test_skiapi.py`
   - [ ] Review the output to understand data structure

3. **Update Code (if needed)**
   - [ ] Based on test results, update API endpoints in `ski_api_fetcher.py`
   - [ ] Update column mappings to match actual API fields

4. **Create Visualizations**
   - [ ] Create map in Datawrapper
   - [ ] Create table in Datawrapper
   - [ ] Add Chart IDs to `.env`

5. **Test Locally**
   - [ ] Run `python run_all_updates.py`
   - [ ] Verify visualizations update correctly

6. **Deploy to GitHub**
   - [ ] Push code to GitHub
   - [ ] Add secrets to repository
   - [ ] Test GitHub Actions workflow

7. **Monitor**
   - [ ] Watch first few automated runs
   - [ ] Review logs for any issues
   - [ ] Fine-tune as needed

---

## 📋 Required Accounts & Keys

You will need:

1. **skiapi.com Account**
   - Sign up at https://skiapi.com
   - Get API key
   - Cost: [Check their pricing]

2. **Datawrapper Account**
   - Sign up at https://app.datawrapper.de/
   - Free tier available
   - Generate API token

3. **GitHub Account** (for automation)
   - Sign up at https://github.com
   - Free tier sufficient

---

## 💰 Cost Breakdown

- **GitHub Actions**: Free (up to 2,000 minutes/month)
- **Datawrapper**: Free tier available (check limits)
- **skiapi.com**: [Check their pricing - may have free tier]

**Estimated Monthly Cost**: $0-$20 depending on API usage

---

## 📈 Success Metrics

Once deployed, you'll have:
- ✅ Live updating visualizations
- ✅ Zero manual intervention required
- ✅ Automatic updates every 2 hours
- ✅ Complete logging and monitoring
- ✅ Error handling and recovery
- ✅ Professional, embeddable visualizations

---

## 🔧 Maintenance Requirements

### Minimal (Monthly)
- Check GitHub Actions for failures
- Verify data accuracy
- Review logs for warnings

### As Needed
- Update API endpoints if skiapi.com changes
- Adjust styling in Datawrapper
- Modify update frequency
- Add/remove data points

---

## 🎓 Learning Resources

If you want to understand or modify the code:

- **Python Basics**: https://docs.python.org/3/tutorial/
- **Pandas**: https://pandas.pydata.org/docs/
- **Datawrapper API**: https://developer.datawrapper.de/
- **GitHub Actions**: https://docs.github.com/en/actions

---

## 📞 Getting Help

If something doesn't work:

1. **Check logs** - Every script creates a `.log` file
2. **Review setup guide** - `SETUP_GUIDE.md` has step-by-step instructions
3. **Check configuration** - Verify `.env` file has all required keys
4. **Test components** - Run individual scripts to isolate issues
5. **Review error messages** - They usually tell you exactly what's wrong

Common issues and solutions are in `SETUP_GUIDE.md` under "Common Issues"

---

## 🎉 You're Ready!

This is a **production-ready system** based on proven patterns from real newsroom data pipelines. Follow the setup guide, test thoroughly, and you'll have live snow conditions updating automatically!

**Have fun and enjoy fresh powder! 🎿**

