# Colorado Snow Conditions - Interactive Map

Live, auto-updating map showing current snow conditions for all Colorado ski resorts.

## 🗺️ View the Map

**Live URL:** https://gazette-evn.github.io/colorado-snow-conditions/

---

## 📊 Features

- **26 Colorado Ski Resorts** with live conditions
- **Auto-updates** from Google Sheets every 5 minutes
- **Mobile-optimized** responsive design
- **Interactive markers** sized by resort size, colored by terrain availability
- **Detailed popups** with snow depth, trails/lifts open, and more
- **Filters** to show all resorts or only open ones

---

## 🔄 Data Updates

**Data Source:** Automated scrapers (OnTheSnow + Colorado Ski Country USA)

**Update Frequency:** Every 2 hours via GitHub Actions

**Last Update:** Check the map's header or any resort popup

---

## 🛠️ Setup

See: [MAPBOX_SETUP_GUIDE.md](../MAPBOX_SETUP_GUIDE.md)

**Quick steps:**
1. Get Mapbox token
2. Publish Google Sheet as CSV
3. Update `config.js`
4. Enable GitHub Pages
5. Done!

---

## 📱 Mobile Support

The map is fully responsive and optimized for:
- iOS Safari
- Android Chrome
- Desktop browsers
- Touch gestures
- Small screens

---

## 🎨 Customization

All settings in `config.js`:
- Map style (terrain, satellite, streets)
- Color scheme
- Marker sizes
- Auto-refresh interval
- Center point and zoom

---

## 📄 Files

- `index.html` - Map page structure
- `style.css` - Responsive styling
- `map.js` - Map logic and data handling
- `config.js` - Your configuration settings

---

Built with ❄️ for Colorado skiers

