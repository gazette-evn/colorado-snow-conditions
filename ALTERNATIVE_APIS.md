# Alternative APIs for Colorado Snow Conditions

Since the current RapidAPI "Ski Resorts and Conditions" lacks snow depth/conditions data, here are alternatives:

## 🆓 Free Government Data (Recommended)

### 1. NOAA Weather.gov API
- **URL:** https://www.weather.gov/documentation/services-web-api
- **Cost:** FREE
- **Data:** Weather, precipitation, forecasts
- **Coverage:** All US locations
- **How:** Query by lat/lng from our resort list
- **Rate Limit:** Reasonable for our needs

**Pros:**
- ✅ Completely free
- ✅ Reliable (government)
- ✅ Good documentation
- ✅ Covers all Colorado

**Cons:**
- ❌ Not ski-specific
- ❌ No lift status
- ❌ Requires more data processing

### 2. SNOTEL (Snow Telemetry)
- **URL:** https://www.nrcs.usda.gov/wps/portal/wcc/home/dataAccessHelp/webService/
- **Cost:** FREE
- **Data:** Snow depth, SWE (snow water equivalent), temperature
- **Coverage:** Mountain sites across Colorado
- **How:** SOAP/REST API

**Pros:**
- ✅ Free
- ✅ Accurate automated sensors
- ✅ Historical data available
- ✅ Ski-area relevant

**Cons:**
- ❌ Sensors not at every resort
- ❌ SOAP API (older format)
- ❌ Requires mapping sensors to resorts

## 💰 Commercial APIs

### 3. OpenSnow
- **URL:** https://opensnow.com/
- **Cost:** Unknown (need to inquire)
- **Data:** Snow depth, forecasts, conditions
- **Coverage:** Major ski resorts

**Pros:**
- ✅ Ski-specific
- ✅ Accurate resort data
- ✅ Well-maintained

**Cons:**
- ❌ May require paid plan
- ❌ Need to check API availability

### 4. WeatherAPI.com
- **URL:** https://www.weatherapi.com/
- **Cost:** Free tier available (1M calls/month)
- **Data:** Weather, forecasts, snow alerts
- **Coverage:** Worldwide

**Pros:**
- ✅ Free tier
- ✅ Easy to use
- ✅ Good documentation

**Cons:**
- ❌ Not ski-specific
- ❌ May lack resort-specific data

### 5. Visual Crossing Weather
- **URL:** https://www.visualcrossing.com/
- **Cost:** Free tier (1000 records/day)
- **Data:** Historical + forecast weather
- **Coverage:** Worldwide

## 🔄 Hybrid Solution (Recommended)

### Best Approach:
1. **Use RapidAPI** for:
   - Resort list (16 CO resorts)
   - Locations (lat/lng)
   - Lift status
   - Links to official pages

2. **Add Weather.gov** for:
   - Current weather by location
   - Precipitation data
   - Temperature
   - Snow alerts

3. **Add SNOTEL** (optional) for:
   - Actual snow depth measurements
   - More accurate than estimates

### Implementation:
```python
# For each resort:
# 1. Get basic info from RapidAPI
# 2. Query Weather.gov by lat/lng
# 3. Query nearby SNOTEL station (if available)
# 4. Combine data into comprehensive view
```

## 🛠️ Quick Implementation Guide

### Weather.gov Example:
```python
import requests

# Get grid point for location
lat, lng = 39.605026, -106.356155  # Vail
response = requests.get(
    f"https://api.weather.gov/points/{lat},{lng}"
)
grid_data = response.json()

# Get forecast
forecast_url = grid_data['properties']['forecast']
forecast = requests.get(forecast_url).json()

# Get observations
stations_url = grid_data['properties']['observationStations']
stations = requests.get(stations_url).json()
latest_obs = requests.get(
    f"{stations['features'][0]['id']}/observations/latest"
).json()
```

## 🎯 Recommendation

**Best Path Forward:**

1. **Keep RapidAPI** - Already working, provides resort list + lifts
2. **Add Weather.gov** - Free, reliable, covers all locations
3. **Consider SNOTEL** - Add later for enhanced accuracy

This gives us:
- ✅ 16 Colorado resorts
- ✅ Locations + map markers
- ✅ Lift status
- ✅ Weather data
- ✅ Precipitation (proxy for new snow)
- ✅ All FREE except RapidAPI ($10/mo you already have)

---

**Would you like me to implement the hybrid solution with Weather.gov?**

