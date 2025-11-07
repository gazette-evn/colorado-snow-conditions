# Available Data Fields - Complete Reference

## 📊 All Data We're Collecting

### ✅ Currently in Google Sheets (17 columns):

#### **Location & Identity:**
1. **Resort Name** - Official resort name
2. **Latitude** - Decimal degrees for mapping
3. **Longitude** - Decimal degrees for mapping
4. **Data Source** - OnTheSnow or CSCUSA

#### **Snow Conditions:**
5. **24h Snowfall** - New snow in last 24 hours (inches)
6. **48h Snowfall** - New snow in last 48 hours (inches)  
7. **Base Depth** - Snow depth at base elevation (inches)
8. **Mid-Mtn Depth** - Snow depth at mid-mountain (inches)
9. **Surface Conditions** - Surface type:
   - `MM` = Machine Made/Man Made
   - `PP` = Packed Powder
   - `MG` = Machine Groomed
   - Other descriptors

#### **Terrain Status:**
10. **Status** - Open or Closed
11. **Lifts Open** - Format: "4/21" (4 lifts open out of 21 total)
12. **Open Lifts** - Number of lifts currently operating
13. **Total Lifts** - Total number of lifts at resort
14. **Trails Open** - Format: "1/147" (1 trail open out of 147 total)
15. **Open Trails** - Number of trails currently open
16. **Total Trails** - Total number of trails at resort

#### **Metadata:**
17. **Last Updated** - Timestamp of data fetch

---

## 📋 Data Source Comparison

### OnTheSnow Provides:
- ✅ 24h snowfall
- ✅ 48h snowfall (shown as "3-day forecast")
- ✅ Base depth
- ✅ Trails open (split into open/total)
- ✅ Lifts open (split into open/total)
- ✅ Status (Open/Closed)
- ❌ Mid-mountain depth (not available)
- ❌ Surface conditions (not available)

### CSCUSA Provides:
- ✅ 24h snowfall
- ✅ 48h snowfall
- ✅ Mid-mountain depth
- ✅ Surface conditions
- ✅ Lifts open (format: "1/9")
- ✅ Status (Open/Closed)
- ⚠️ Base depth (sometimes)
- ❌ Trails open (not consistently available)

---

## 🎨 Best Fields for Datawrapper Map

### Essential (Must Have):
1. **Latitude** - For pin placement
2. **Longitude** - For pin placement  
3. **Resort Name** - Label
4. **Status** - Color coding (Green=Open, Red=Closed)

### High Value (Recommended):
5. **24h Snowfall** - Most important for skiers
6. **Base Depth** - Shows overall conditions
7. **Trails Open** - Shows how much terrain available
8. **Lifts Open** - Shows capacity

### Nice to Have (Optional):
9. **48h Snowfall** - Recent trend
10. **Mid-Mtn Depth** - Better snow than base
11. **Surface Conditions** - Quality indicator
12. **Open Trails** - Numeric for filtering
13. **Total Trails** - Context for size

---

## 💡 Datawrapper Symbol Map Suggestions

### Color by Status:
- 🟢 **Green pins** - Open resorts
- 🔴 **Red pins** - Closed resorts

### Size by Metric (Choose one):
- **Option A:** Base Depth (larger pin = more snow)
- **Option B:** Total Trails (larger pin = bigger resort)
- **Option C:** Trails Open % (larger pin = more terrain available)

### Tooltip Display:
When hovering over a pin, show:
```
📍 Breckenridge
Status: Open ✓
24h Snow: 0"
Base Depth: 18"
Trails: 1/188 open (1%)
Lifts: 2/35 open (6%)
Surface: Man Made
Last Updated: 2025-11-07 15:24
```

---

## 🔮 Additional Data We Could Add (Future)

### From External Sources:

#### **Weather API (NOAA):**
- Current temperature
- Wind speed/direction
- Weather conditions
- 7-day forecast

#### **SNOTEL (USDA):**
- Snow water equivalent (SWE)
- Historical snowpack comparison
- Nearby weather station data

#### **Resort Websites (If scraped individually):**
- Terrain park status
- Grooming reports
- Special conditions/closures
- Pass restrictions
- Ticket prices

### Derived Metrics:
- **Terrain Open %** - `(Open Trails / Total Trails) * 100`
- **Lift Capacity %** - `(Open Lifts / Total Lifts) * 100`
- **Snow Trend** - Compare 24h vs 48h vs 7-day
- **Days Since Last Snow** - Calculate from historical data

---

## 📊 Current Data Quality by Resort

### Open Resorts (Full Data):
| Resort | 24h Snow | Base | Trails | Lifts | Surface |
|--------|----------|------|--------|-------|---------|
| Arapahoe Basin (OTS) | ✓ | ✓ | ✓ | ✓ | ❌ |
| Arapahoe Basin (CSCUSA) | ✓ | ❌ | ❌ | ✓ | ✓ |
| Breckenridge | ✓ | ✓ | ✓ | ✓ | ❌ |
| Copper Mountain | ✓ | ✓ | ✓ | ✓ | ❌ |
| Keystone | ✓ | ✓ | ✓ | ✓ | ❌ |
| Loveland | ✓ | ❌ | ❌ | ✓ | ✓ |
| Winter Park | ✓ | ✓ | ✓ | ✓ | ❌ |

### Closed Resorts (Limited Data):
- Status: Closed
- All snow metrics: 0
- Lifts/Trails: 0 open
- Will populate when they open

---

## 🎯 Data Refresh Frequency

### Current (GitHub Actions):
- **Every 2 hours** during ski season
- Runs automatically at: 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00

### Resort Update Frequency:
- **OnTheSnow:** Updates hourly during operating hours
- **CSCUSA:** Updates once daily between 5-7am MST

### Recommendation:
- **Peak season:** Keep 2-hour updates
- **Off-season:** Can reduce to 4-6 hour updates to save GitHub Actions minutes

---

## ✅ Summary

### What We Have:
- ✅ 17 comprehensive data fields
- ✅ All essential metrics for skiers
- ✅ Location data for mapping
- ✅ Both aggregate (1/147) and split (1, 147) formats
- ✅ Multiple data sources for reliability

### What's Missing:
- ❌ Weather forecasts (can add NOAA API)
- ❌ Historical trends (can add if we store data)
- ❌ Terrain parks (need individual resort scraping)
- ❌ Real-time webcams (beyond scope)

### Data Quality:
- **Excellent** for open resorts from OnTheSnow
- **Good** for CSCUSA resorts (missing some fields)
- **Complete** coverage of critical metrics
- **Production-ready** for visualization

