# Datawrapper Symbol Map - Setup Guide

## 🎨 How to Create Your Colorado Snow Conditions Map

### Your Google Sheet:
https://docs.google.com/spreadsheets/d/10sbXOC-cl-pVZZWzqx0jNp9YJcxgXD4FRELy91flFBI

---

## ✅ What's Now Available (Updated!)

All 23 resorts now have complete data:

### **Columns in Google Sheet:**
1. **Resort Name** - Resort name
2. **Latitude** - For positioning pins
3. **Longitude** - For positioning pins
4. **Status** - Open or Closed
5. **24h Snowfall (in)** - New snow in last 24h
6. **48h Snowfall (in)** - New snow in last 48h
7. **Base Depth (in)** - Snow depth at base
8. **Mid-Mtn Depth (in)** - Snow depth mid-mountain
9. **Surface Conditions** - MM, PP, MG, etc.
10. **Total Trails** - Total number of trails ⭐ NEW!
11. **Open Trails** - Number currently open
12. **Trails Open %** - Percentage of trails open ⭐ NEW!
13. **Total Lifts** - Total number of lifts ⭐ NEW!
14. **Open Lifts** - Number currently operating
15. **Lifts Open %** - Percentage of lifts open ⭐ NEW!
16. **Data Source** - OnTheSnow or CSCUSA
17. **Last Updated** - Timestamp

---

## 🗺️ Datawrapper Configuration

### Step 1: Create Symbol Map

1. Go to: https://app.datawrapper.de/
2. Click **"New Chart"**
3. Select **"Symbol Map"**

### Step 2: Link Your Google Sheet

1. Click **"Link external dataset"**
2. Choose **"Google Spreadsheet"**
3. Enter Sheet ID: `10sbXOC-cl-pVZZWzqx0jNp9YJcxgXD4FRELy91flFBI`
4. Or paste full URL
5. Click **"Proceed"**

### Step 3: Configure Location (Check & Describe Tab)

**Locator Type:** Points (symbols)

**Location columns:**
- **Latitude column:** `Latitude`
- **Longitude column:** `Longitude`

**Label column (optional):** `Resort Name`

### Step 4: Design Map (Visualize Tab)

#### **Symbol Size** ⭐ KEY SETTING
**Size by:** `Total Trails`

**Settings:**
- **Min size:** 8 pixels
- **Max size:** 40 pixels
- **Scale:** Linear

**Result:** Larger resorts (more trails) have bigger circles!

---

#### **Symbol Color** 🎨 KEY SETTING  
**Color by:** `Trails Open %`

**Settings:**
- **Color scheme:** Sequential (choose a gradient)
  - **Suggestion:** Blue (closed) → Green (partially open) → Yellow/Orange (fully open)
  - Or: Single hue gradient (light gray → dark green)
- **Custom colors:**
  - 0% = `#E0E0E0` (gray - closed)
  - 1-25% = `#90CAF9` (light blue - just opened)
  - 26-50% = `#4CAF50` (green - moderate)
  - 51-100% = `#2E7D32` (dark green - mostly open)

**Alternative (Simpler):**
**Color by:** `Status`
- **Open** = Green (#4CAF50)
- **Closed** = Gray (#BDBDBD)

---

#### **Tooltip**
Configure what appears when hovering over a resort:

**Title:** `{{ Resort Name }}`

**Body:** 
```
Status: {{ Status }}
---
Snow Conditions:
• 24h Snowfall: {{ 24h Snowfall (in) }}"
• Base Depth: {{ Base Depth (in) }}"
• Surface: {{ Surface Conditions }}
---
Terrain:
• Trails: {{ Open Trails }}/{{ Total Trails }} ({{ Trails Open % }}%)
• Lifts: {{ Open Lifts }}/{{ Total Lifts }} ({{ Lifts Open % }}%)
---
Updated: {{ Last Updated }}
```

**Simplified Version:**
```
{{ Status }}
Trails: {{ Open Trails }}/{{ Total Trails }} open
24h Snow: {{ 24h Snowfall (in) }}"
Base: {{ Base Depth (in) }}"
```

---

### Step 5: Map Settings

**Base map:**
- **Style:** Light gray or terrain
- **Focus:** Colorado (zoom appropriately)
- **Labels:** Show major cities (Denver, Boulder, Colorado Springs, etc.)

**Symbol style:**
- **Border:** 1-2px white border (helps symbols stand out)
- **Opacity:** 80-90% (so map shows through)

---

## 🎨 Recommended Design Options

### **Option A: Size + Color by Trail Percentage** (Most Informative)
- **Size:** Total Trails (shows resort size)
- **Color:** Trails Open % (shows how much is open)
- **Best for:** Understanding which resorts are most operational

### **Option B: Size by Total, Color by Status** (Simplest)
- **Size:** Total Trails
- **Color:** Status (Green=Open, Gray=Closed)
- **Best for:** Quick overview of what's open

### **Option C: Size + Color by Snow** (Snow-Focused)
- **Size:** Total Trails
- **Color:** Base Depth (in) or 24h Snowfall
- **Best for:** Finding the best snow conditions

---

## 📊 Why All Resorts Show Now

**Before:** Only 6 resorts had total_trails data (from OnTheSnow)

**Now:** All 23 resorts have total_trails from:
- OnTheSnow data (when available)
- Manual resort statistics (when scraped data missing)

**Trail Counts Added For:**
- Arapahoe Basin: 147 trails
- Aspen Highlands: 144 trails
- Aspen Mountain: 76 trails
- Buttermilk: 44 trails
- Cooper: 60 trails
- Echo Mountain: 7 trails
- Eldora: 53 trails
- Granby Ranch: 33 trails
- Howelsen Hill: 15 trails
- Monarch: 64 trails
- Powderhorn: 42 trails
- Purgatory Resort: 105 trails
- Silverton: 69 trails
- Snowmass: 98 trails
- Steamboat: 169 trails
- Sunlight: 71 trails
- Telluride: 148 trails

---

## 🔄 Auto-Refresh

**Your sheet updates automatically every 2 hours via GitHub Actions!**

**Datawrapper will auto-refresh from the sheet:**
- No manual work needed
- Map always shows current conditions
- Percentages recalculate automatically

**Schedule (Mountain Time):**
Updates at: 5pm, 7pm, 9pm, 11pm, 1am, 3am, 5am, 7am, 9am, 11am, 1pm, 3pm

---

## 🎯 Next Steps in Datawrapper

1. **Refresh the data** in Datawrapper (it should now show all 23 resorts)
2. **Set size:** Total Trails
3. **Set color:** Trails Open % (gradient) or Status (simple)
4. **Configure tooltip** with resort details
5. **Style the map** (colors, borders, labels)
6. **Publish!** 🎿

---

## 📈 Current Data (Example)

**Open Resorts (Early Season):**
| Resort | Total Trails | Open Trails | % Open |
|--------|--------------|-------------|--------|
| Arapahoe Basin | 147 | 1 | 0.7% |
| Breckenridge | 188 | 2 | 1.1% |
| Copper Mountain | 150 | 3 | 2.0% |
| Keystone | 140 | 4 | 2.9% |
| Loveland | 94 | 0 | 0.0% |
| Winter Park | 171 | 5 | 2.9% |

**Closed Resorts:**
All have 0% open (will show as 0 trails open)

**Visual Result:**
- Closed resorts: Gray circles, sized by total trails
- Open resorts: Colored by % open, sized by total trails
- Easy to see which resorts are biggest AND how much terrain is available!

---

## 💡 Tips

**For Early Season (Now):**
- Most resorts closed (gray)
- Open resorts have <5% of terrain open
- Use gradient that shows small differences (0-5%)

**For Peak Season (Dec-Mar):**
- Most resorts open (colorful)
- Many resorts 80-100% open
- Gradient shows which resorts have the most terrain available

**Color Gradient Suggestion:**
- 0% = Light gray
- 1-10% = Light blue (early season minimal)
- 11-50% = Blue-green (building)
- 51-80% = Green (strong)
- 81-100% = Dark green (full operations)

This way you can see the progression as ski season ramps up!

