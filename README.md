# Colorado Snow Conditions - Live Data Pipeline

🎿 **Automated data visualization pipeline that updates live snow conditions for all Colorado ski resorts**

This project automatically scrapes snow conditions from OnTheSnow and Colorado Ski Country USA, updates a Google Sheet, and powers a Datawrapper map every 2 hours:
- **Live Map**: Interactive symbol map showing all 23 Colorado resorts with current conditions
- **Google Sheets**: Central data source that Datawrapper reads from
- **Automated**: Runs every 2 hours via GitHub Actions - completely hands-off!

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd snow-conditions-data

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Google Sheets API

**Follow the complete guide:** [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)

Quick summary:
1. Create Google Cloud project
2. Enable Google Sheets API
3. Create service account & download JSON key
4. Create new Google Sheet
5. Share sheet with service account email

**You'll get:**
- Service account JSON credentials file
- Google Sheet ID (from the sheet URL)

### 3. Create Environment File

Create a `.env` file in the project root:

```bash
# .env

# Google Sheets Configuration (REQUIRED)
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS='{"type":"service_account","project_id":"...","private_key":"..."}}'

# Datawrapper (Optional - for future table view)
DATAWRAPPER_API_KEY=EFDvH4jTgfczR76PhJuwlzH625xzLs7OIKGv9WYNfuRo7VWb3Kb1A1YlXGL2UinA
```

**Note:** The `GOOGLE_CREDENTIALS` value should be the entire JSON from the service account key file (from Step 2).

### 4. Create Datawrapper Visualizations

**Map:**
1. Go to https://app.datawrapper.de/
2. Create New → Locator map
3. Select Colorado region
4. Upload sample data with columns: `lat`, `lng`, `resort_name` (at minimum)
5. Style as desired (colors, zoom level, etc.)
6. Note the Chart ID from the URL (e.g., `AbC12`)
7. Add to your `.env` as `SNOW_MAP_CHART_ID`

**Table:**
1. Create New → Table
2. Upload sample data with your desired columns
3. Enable sorting on column headers
4. Style as desired
5. Note the Chart ID
6. Add to your `.env` as `SNOW_TABLE_CHART_ID`

### 5. Test the RapidAPI Connection

First, test the RapidAPI connection to understand the data structure:

```bash
python test_skiapi.py
```

This will:
- Test the RapidAPI endpoints
- Show you the data structure returned
- Display sample Colorado resort data
- Help identify which fields to use

Review the output and verify the data looks correct. The script will automatically test multiple endpoints to find the right one.

### 6. Test Individual Scripts

```bash
# Test data fetching
python ski_api_fetcher.py

# Test map update
python snow_map.py

# Test table update
python snow_table.py

# Run all updates
python run_all_updates.py
```

Check Datawrapper to verify your visualizations updated correctly!

---

## 📊 Data Points Tracked

For each Colorado ski resort, we track:

- **Location**: Latitude/longitude for map display
- **Snow Depth**: Base and summit depth (inches)
- **New Snowfall**: 24-hour, 48-hour, and 7-day totals
- **Lift Status**: Number of lifts open vs. total lifts
- **Run Status**: Number of runs open vs. total runs
- **Operating Status**: Open, Closed, or Limited operation
- **Conditions**: Current snow conditions description

---

## 🤖 Automated Updates with GitHub Actions

### Setup Automation

1. **Push your code to GitHub**

```bash
git add .
git commit -m "Initial setup of Colorado snow conditions pipeline"
git push origin main
```

2. **Add Secrets to GitHub Repository**

Go to your repository → Settings → Secrets and variables → Actions

Add these secrets:
- `DATAWRAPPER_API_KEY`
- `SKIAPI_KEY`
- `SNOW_MAP_CHART_ID`
- `SNOW_TABLE_CHART_ID`

3. **Enable GitHub Actions**

The workflow is already configured in `.github/workflows/update-snow-data.yml`

It will run:
- **Every 2 hours** automatically (during ski season)
- **On manual trigger** (Actions tab → Update Colorado Snow Conditions → Run workflow)
- **On push to main** (for testing)

### Monitor Updates

View update status:
1. Go to the Actions tab in your GitHub repository
2. Click on "Update Colorado Snow Conditions"
3. View recent runs and logs
4. Download log artifacts if needed

---

## 📁 Project Structure

```
snow-conditions-data/
├── ski_api_fetcher.py          # Fetches data from skiapi.com
├── snow_map.py                 # Updates Datawrapper map
├── snow_table.py               # Updates Datawrapper table
├── run_all_updates.py          # Master orchestration script
├── test_skiapi.py              # API testing/exploration script
│
├── requirements.txt            # Python dependencies
├── .env                        # API keys (DO NOT COMMIT)
├── .gitignore                  # Git ignore rules
│
├── .github/workflows/
│   └── update-snow-data.yml    # GitHub Actions automation
│
└── README.md                   # This file
```

---

## 🔧 Configuration & Customization

### Adjust Update Frequency

Edit `.github/workflows/update-snow-data.yml`:

```yaml
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
  # Change to:
  - cron: '0 */4 * * *'  # Every 4 hours
  - cron: '0 */1 * * *'  # Every 1 hour
  - cron: '0 6,14,22 * * *'  # 3 times daily (6am, 2pm, 10pm)
```

### Customize Map Tooltip

Edit the `create_tooltip_template()` function in `snow_map.py` to change what information appears when hovering over resort markers.

### Customize Table Columns

Edit the `prepare_table_data()` function in `snow_table.py` to add/remove/reorder columns.

### Filter Resorts

To show only major resorts, add filtering logic in `ski_api_fetcher.py`:

```python
# Example: Only show resorts with 10+ lifts
df = df[df['lifts_total'] >= 10]
```

---

## 🐛 Troubleshooting

### "API key not found" error

Make sure your `.env` file exists and contains the required keys. The `.env` file should be in the same directory as your Python scripts.

### "Chart ID not found" error

Verify your Datawrapper chart IDs are correct in the `.env` file. The IDs are 5-character codes from the chart URLs.

### Data not updating

1. Check GitHub Actions logs for errors
2. Verify API keys are set correctly in repository secrets
3. Check that skiapi.com API is responding (run `test_skiapi.py`)
4. Review log files (`*.log`) for detailed error messages

### Column mapping errors

If the skiapi.com API structure differs from expected, update the `column_mapping` dictionary in `ski_api_fetcher.py` based on the output from `test_skiapi.py`.

---

## 📝 Logs

All scripts generate log files:
- `ski_api_fetcher.log` - Data fetching logs
- `snow_map.log` - Map update logs
- `snow_table.log` - Table update logs
- `master_update.log` - Overall pipeline logs

View recent errors:
```bash
grep ERROR *.log
```

View today's activity:
```bash
grep "$(date +%Y-%m-%d)" master_update.log
```

---

## 🌟 Features

✅ **Fully Automated**: Zero manual intervention after setup  
✅ **Reliable**: Runs on GitHub's infrastructure  
✅ **Observable**: Comprehensive logging and monitoring  
✅ **Maintainable**: Modular, well-documented code  
✅ **Scalable**: Easy to add more visualizations  
✅ **Free**: Uses free tiers of GitHub Actions and Datawrapper  

---

## 📚 Tech Stack

- **Python 3.11+**: Core scripting language
- **Pandas**: Data processing and transformation
- **Datawrapper**: Visualization platform
- **skiapi.com**: Snow conditions data source
- **GitHub Actions**: Automated scheduling and execution

---

## 🤝 Contributing

To add new features:

1. Create a new branch: `git checkout -b feature-name`
2. Make your changes and test thoroughly
3. Commit: `git commit -m "Description of changes"`
4. Push: `git push origin feature-name`
5. Create a Pull Request

---

## 📄 License

This project is open source and available for anyone to use and modify.

---

## 🎿 Credits

Built using the [Datawrapper Automation Pipeline Blueprint](PROJECT_BLUEPRINT.md) - a proven pattern from the SF Examiner production system.

Data provided by [RapidAPI - Ski Resorts and Conditions](https://rapidapi.com)

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review log files for detailed error messages
3. Test individual components (`test_skiapi.py`, `ski_api_fetcher.py`, etc.)
4. Verify all API credentials and chart IDs are correct

---

**Happy skiing! 🎿⛷️**

