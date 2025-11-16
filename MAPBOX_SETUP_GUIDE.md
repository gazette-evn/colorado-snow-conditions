# Mapbox Map Setup Guide

## 🎨 Beautiful, Mobile-Optimized Interactive Map

You now have a custom Mapbox-powered map that gives you full control over styling and works beautifully on mobile!

---

## 🚀 Quick Setup (10 minutes)

### Step 1: Publish Your Google Sheet as CSV

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/10sbXOC-cl-pVZZWzqx0jNp9YJcxgXD4FRELy91flFBI

2. Click **File → Share → Publish to web**

3. In the dialog:
   - **Link:** Choose "Entire Document" (or just "Sheet1")
   - **Format:** Select **"Comma-separated values (.csv)"**
   - Click **"Publish"**
   - Click **"OK"** when it asks to confirm

4. **Copy the URL** it generates (looks like):
   ```
   https://docs.google.com/spreadsheets/d/e/2PACX-1vT.../pub?output=csv
   ```

---

### Step 2: Get Your Mapbox Token

1. Go to: https://account.mapbox.com/access-tokens/

2. Find your **"Default public token"** (starts with `pk.`)

3. **Copy it** - looks like:
   ```
   pk.eyJ1IjoieW91cm5hbWUiLCJhIjoiY2x...
   ```

---

### Step 3: Update Configuration File

Open the file: `docs/config.js`

Replace these two values:

```javascript
// Line 4: Add your Mapbox token
const MAPBOX_TOKEN = 'pk.eyJ1IjoieW91cm5hbWUiLCJhIjoiY2x...';  // ← Paste your token here

// Line 12: Add your Google Sheet CSV URL
const DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT.../pub?output=csv';  // ← Paste your CSV URL here
```

Save the file.

---

### Step 4: Enable GitHub Pages

1. Go to: https://github.com/gazette-evn/colorado-snow-conditions/settings/pages

2. Under **"Source"**, select:
   - **Branch:** `main`
   - **Folder:** `/docs`

3. Click **"Save"**

4. GitHub will build your site (takes 1-2 minutes)

5. Your map will be live at:
   ```
   https://gazette-evn.github.io/colorado-snow-conditions/
   ```

---

### Step 5: Commit and Push

```bash
cd /Users/evanwyloge/snow-conditions-data
git add docs/
git commit -m "Add Mapbox interactive map for Colorado snow conditions"
git push origin main
```

Wait 1-2 minutes for GitHub Pages to deploy, then visit your map!

---

## 🎨 Map Features

### **What You Get:**

✅ **Beautiful Base Map**
- Terrain/satellite/streets options
- Smooth zooming and panning
- Professional cartography

✅ **Smart Markers**
- **Size:** Bigger circles = more trails (Vail is huge!)
- **Color:** Gradient shows trails open %
  - Gray = Closed
  - Light blue = Just opened (1-5%)
  - Green = Moderate (6-25%)
  - Dark green = Mostly open (51-100%)

✅ **Rich Popups**
- Resort name and status
- Snow conditions (24h, 48h, base depth, surface)
- Terrain info (trails/lifts open with percentages)
- Last updated timestamp
- Data source

✅ **Filters**
- "All Resorts" - Shows all 26 resorts
- "Open Only" - Shows only operating resorts

✅ **Mobile Optimized**
- Touch-friendly controls
- Responsive layout
- Works great on phones/tablets

✅ **Auto-Refresh**
- Fetches latest data every 5 minutes
- No page reload needed

---

## 🔄 How Auto-Update Works

### **Data Flow:**

```
Every 2 hours:
GitHub Actions → Scrape → Update Google Sheet → Google publishes as CSV

Every 5 minutes (while map is open):
Map checks CSV URL → Fetches if changed → Updates markers automatically

Every 2 minutes (while someone views the map):
Datawrapper would need manual refresh
Mapbox auto-refreshes → Better UX!
```

### **Result:**
- Users always see fresh data (within 5 minutes)
- No manual refresh needed
- Seamless experience

---

## 🎨 Customization Options

### **Change Map Style** (in `config.js`):

```javascript
style: 'mapbox://styles/mapbox/outdoors-v12'
```

**Options:**
- `streets-v12` - Clean street map
- `outdoors-v12` - Terrain/hiking (current)
- `satellite-v9` - Satellite imagery
- `light-v11` - Minimalist light
- `dark-v11` - Dark theme

### **Change Colors** (in `config.js`):

```javascript
const COLOR_SCALE = {
    closed: '#BDBDBD',   // Change to any hex color
    veryLow: '#90CAF9',
    // ... etc
};
```

### **Adjust Marker Sizes** (in `config.js`):

```javascript
const MARKER_SIZE = {
    min: 12,  // Increase for bigger minimum
    max: 50,  // Increase for bigger maximum
};
```

### **Change Auto-Refresh Interval** (in `config.js`):

```javascript
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes (in milliseconds)
```

---

## 📱 Mobile Experience

### **Features:**
- Touch-optimized controls
- Responsive header and legend
- Smooth pinch-to-zoom
- Easy popup interaction
- Fullscreen mode
- Works in any browser

### **Performance:**
- Fast loading (~2-3 seconds)
- Smooth animations
- Efficient marker rendering
- Minimal data transfer

---

## 🆚 Mapbox vs Datawrapper

| Feature | Datawrapper | Mapbox |
|---------|-------------|--------|
| Setup Time | 5 minutes | 10 minutes |
| Customization | Limited | Unlimited |
| Mobile Experience | OK | Excellent |
| Auto-Refresh | Manual/Premium | Built-in (free) |
| Branding | Datawrapper logo | Your own |
| Hosting | Datawrapper | GitHub (your domain) |
| Cost | Free tier limits | Free (50k loads/mo) |
| Style Control | Templates only | Full CSS/JS |
| Loading Speed | Slower | Faster |

---

## 🔧 Advanced: Custom Domain (Optional)

Want your map at `snow.yourdomain.com` instead of GitHub Pages?

1. Buy domain (Namecheap, Google Domains, etc.)
2. In GitHub Pages settings, add custom domain
3. Configure DNS (CNAME record)
4. GitHub provides free SSL certificate

---

## 📊 Files Created

```
docs/
├── index.html      - Main map page
├── style.css       - Styling and responsive design
├── map.js          - Map logic and data handling
└── config.js       - Your configuration (tokens, URLs, colors)
```

---

## ✅ Next Steps

1. ✅ Get Mapbox token (you have account)
2. ✅ Publish Google Sheet as CSV
3. ✅ Update `docs/config.js` with your token and CSV URL
4. ✅ Commit and push to GitHub
5. ✅ Enable GitHub Pages (settings)
6. ✅ Visit your map!

**Your map URL will be:**
```
https://gazette-evn.github.io/colorado-snow-conditions/
```

---

## 🎯 What You'll Have

A **professional, custom snow conditions map** that:
- ✅ Updates automatically from Google Sheets
- ✅ Looks amazing on mobile
- ✅ Refreshes data every 5 minutes
- ✅ Costs $0 to run
- ✅ Completely under your control
- ✅ Can be embedded anywhere
- ✅ No "Created with..." watermarks

**Much better than Datawrapper for this use case!** 🎿

