# Colorado Ski Resort Data - Available Sources

## 🥇 Best Options (Recommended)

### 1. SnoCountry API ⭐ TOP CHOICE
- **URL:** https://feeds.snocountry.net/
- **Cost:** Free tier available, paid tiers for more features
- **Data:**
  - ✅ New snow (24h, 48h, 7-day)
  - ✅ Base depth (top/bottom)
  - ✅ Open trails & lifts
  - ✅ Operating status
  - ✅ Surface conditions
  - ✅ Updated daily
- **Coverage:** Extensive US ski resort coverage including Colorado
- **Format:** Structured API (JSON/XML)
- **Reliability:** ⭐⭐⭐⭐⭐ Industry standard

**Pros:**
- ✅ Free tier available
- ✅ Well-documented API
- ✅ Data sourced directly from resorts
- ✅ Daily updates during ski season
- ✅ All Colorado major resorts

**Cons:**
- May require registration
- Free tier limits (need to check)

---

### 2. OnTheSnow API (Mountain News)
- **URL:** https://partner.docs.onthesnow.com/
- **Cost:** Commercial partnership (need to inquire)
- **Data:**
  - ✅ Operating status
  - ✅ Snow depths (summit/mid/base)
  - ✅ Recent snowfall
  - ✅ Open lifts
  - ✅ Terrain status
  - ✅ Surface conditions
- **Coverage:** Comprehensive global coverage
- **Format:** REST API
- **Reliability:** ⭐⭐⭐⭐⭐ Very reliable

**Pros:**
- ✅ Direct from resorts
- ✅ Daily updates
- ✅ Very comprehensive data
- ✅ Professional API

**Cons:**
- ❌ Requires commercial partnership
- ❌ Likely costs money
- Need to contact for pricing

---

### 3. OpenSnow API
- **URL:** https://blizzard.opensnow.com/opensnow-api/
- **Cost:** Commercial partnership required
- **Data:**
  - ✅ Current conditions
  - ✅ 5-day snow forecasts
  - ✅ Daily snow reports
  - ✅ Hourly forecasts
  - ✅ Historical data
- **Coverage:** Ski resorts worldwide
- **Format:** REST API with detailed documentation
- **Reliability:** ⭐⭐⭐⭐⭐ Premium service

**Pros:**
- ✅ Very accurate forecasts
- ✅ Beautiful data
- ✅ Well-known in ski community
- ✅ Includes forecasting

**Cons:**
- ❌ Commercial partners only
- ❌ Need to request access
- ❌ Likely expensive

---

## 💰 Budget Options

### 4. Weather Unlocked Ski Resort API
- **URL:** https://developer.weatherunlocked.com/
- **Cost:** Paid tiers
- **Data:**
  - ✅ Weather forecasts
  - ✅ Ski resort specific data
  - ❓ May not include live conditions
- **Coverage:** Global ski resorts
- **Reliability:** ⭐⭐⭐

**Pros:**
- ✅ Includes forecast data
- ✅ Good for planning

**Cons:**
- ❌ Focus on forecasts, not current conditions
- ❌ Paid service

---

## 🆓 Free Government Data

### 5. SNOTEL (USDA)
- **URL:** https://www.nrcs.usda.gov/wps/portal/wcc/home/
- **Cost:** FREE
- **Data:**
  - ✅ Snow depth (measured)
  - ✅ Snow Water Equivalent (SWE)
  - ✅ Temperature
  - ✅ Precipitation
- **Coverage:** Automated stations throughout Colorado mountains
- **Format:** SOAP/REST API, CSV downloads
- **Reliability:** ⭐⭐⭐⭐⭐ Government sensors

**Pros:**
- ✅ Completely free
- ✅ Accurate automated sensors
- ✅ Historical data available
- ✅ Reliable government data

**Cons:**
- ❌ Sensors not AT resorts (nearby)
- ❌ Need to map sensors to resorts
- ❌ SOAP API (older format)
- ❌ No lift/terrain status

---

## 📊 Data Aggregators

### 6. Colorado Ski Country USA
- **URL:** https://www.coloradoski.com/snow-report
- **Cost:** FREE (web scraping needed)
- **Data:**
  - ✅ Daily snow reports
  - ✅ All Colorado resorts
  - ✅ Snowfall totals
  - ✅ Lift info
- **Format:** Website (no public API)
- **Reliability:** ⭐⭐⭐⭐

**Pros:**
- ✅ Free
- ✅ All Colorado resorts
- ✅ Daily updates

**Cons:**
- ❌ No API - requires web scraping
- ❌ Scraping can break
- ❌ Against TOS potentially

---

## 🎯 My Recommendations

### Option A: **SnoCountry API** (BEST)
**Why:**
- Free tier likely exists
- Purpose-built for ski conditions
- All the data we need
- Industry standard

**Action:** Sign up at feeds.snocountry.net and check their free tier

---

### Option B: **Hybrid: SNOTEL + Resort Scraping**
**Why:**
- Completely free
- SNOTEL for snow depth (reliable)
- Scrape resort pages for lifts/terrain
- Total control

**Action:** Build custom scraper using:
1. SNOTEL API for snow data
2. BeautifulSoup/Scrapy for resort websites
3. Map SNOTEL stations to resorts

---

### Option C: **OnTheSnow API** (Premium)
**Why:**
- Most comprehensive
- Professional grade
- Direct from resorts
- Worth it if you have budget

**Action:** Contact OnTheSnow for commercial partnership

---

## 📋 Next Steps

### Immediate:
1. ✅ **Test SnoCountry API** - Check if free tier meets our needs
2. Sign up and test their data structure
3. See if it has Keystone/A-Basin current data

### Backup:
- Build SNOTEL + scraper hybrid if SnoCountry doesn't work

### Budget:
- Contact OnTheSnow if you have budget ($50-200/mo estimate)

---

## 🔍 Quick Comparison

| Source | Cost | Live Data | Easy API | CO Coverage | Forecast |
|--------|------|-----------|----------|-------------|----------|
| **SnoCountry** | Free/Paid | ✅ | ✅ | ✅ | ❌ |
| **OnTheSnow** | Paid | ✅ | ✅ | ✅ | ❌ |
| **OpenSnow** | Paid | ✅ | ✅ | ✅ | ✅ |
| **SNOTEL** | Free | ✅ | ⚠️ | ✅ | ❌ |
| **RapidAPI (current)** | $10/mo | ❌ | ✅ | ✅ | ❌ |

---

## 🎿 Verdict

**Try SnoCountry first!** It's likely free for basic usage and purpose-built for exactly what we need. If that doesn't work, we can build a hybrid SNOTEL + scraper solution.

Want me to test the SnoCountry API to see if it has current Keystone/A-Basin data?

