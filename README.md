# Colorado Snow Conditions

**Live interactive map showing real-time snow conditions for all Colorado ski resorts**

🔗 **Live Map:** https://gazette-evn.github.io/colorado-snow-conditions/

---

## What It Does

Automatically scrapes snow conditions from OnTheSnow and Colorado Ski Country USA every 2 hours and displays them on an interactive map with 28 Colorado ski resorts.

### Features

- 🗺️ **Interactive Map** - Click any resort for detailed conditions
- 🎨 **Visual Encoding** - Marker color shows % terrain open, size shows resort size
- 🔄 **Auto-Updates** - Fresh data every 2 hours via GitHub Actions
- 📱 **Mobile Friendly** - Responsive design for on-the-go planning
- 🆓 **Completely Free** - Open source, no API costs

### Data Tracked

For each resort:
- Current operating status (Open/Closed)
- 24-hour snowfall
- Base & mid-mountain depth
- Surface conditions
- Trails open (e.g., 147/277)
- Lifts operating (e.g., 21/31)
- Last update timestamp

---

## Colorado Resorts Covered

**I-70 Corridor:** Vail, Beaver Creek, Breckenridge, Keystone, Copper Mountain, Arapahoe Basin, Loveland, Winter Park

**Aspen Area:** Aspen Mountain, Aspen Highlands, Snowmass, Buttermilk

**Summit County:** Breckenridge, Keystone, Copper, A-Basin

**Southern Colorado:** Telluride, Purgatory, Crested Butte, Wolf Creek, Monarch

**Other:** Steamboat, Eldora, Powderhorn, and more

---

## How It Works

```
OnTheSnow + Colorado Ski Country → Scrapers → Google Sheets → Map
                     ↑                                              
        GitHub Actions runs every 2 hours (Mountain Time)
```

1. **Dual scrapers** fetch data from OnTheSnow and Colorado Ski Country USA
2. **Combined scraper** merges data and adds coordinates
3. **Google Sheets** stores and publishes data as CSV
4. **GitHub Pages** serves the interactive map
5. **GitHub Actions** automates the entire pipeline

---

## Tech Stack

- **Frontend:** Mapbox GL JS, Vanilla JavaScript
- **Backend:** Python 3.11, Selenium, BeautifulSoup, Pandas
- **Data Sources:** OnTheSnow, Colorado Ski Country USA
- **Storage:** Google Sheets API
- **Hosting:** GitHub Pages
- **Automation:** GitHub Actions (every 2 hours)

---

## Development

**Local testing:**
```bash
python combined_scraper.py       # Scrape both sources
python google_sheets_updater.py  # Upload to Google Sheets
open docs/index.html             # View map locally
```

**Project Structure:**
```
├── combined_scraper.py          # Main data aggregator
├── onthesnow_scraper.py         # OnTheSnow scraper
├── colorado_ski_scraper.py      # Colorado Ski Country scraper
├── google_sheets_updater.py     # Google Sheets integration
├── docs/                        # GitHub Pages website
│   ├── index.html
│   ├── map.js
│   ├── config.js
│   └── style.css
└── .github/workflows/           # Automation
    └── update-snow-data.yml
```

---

## License

Open source - feel free to fork and adapt for other regions!

---

**Built with ⛷️ by Evan Wyloge**
