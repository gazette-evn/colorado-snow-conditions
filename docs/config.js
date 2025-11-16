// Configuration for Colorado Snow Conditions Map
// Replace these values with your actual credentials

const MAPBOX_TOKEN = 'pk.eyJ1IjoiZXZud2xnIiwiYSI6ImNtaTIzYTFnYzFneG8yaXB4NDg3M3RsaWwifQ.p3vhcRK8BQ22w5i9fdiM5w';  // Get from https://account.mapbox.com/access-tokens/

// Your Google Sheet published as CSV
// To get this URL:
// 1. Open your Google Sheet
// 2. File → Share → Publish to web
// 3. Choose "Entire Document" and "Comma-separated values (.csv)"
// 4. Click Publish and copy the URL
const DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRre-sQPQqn1VAhLoDgTOwOOTUdKnT688YjHZXQpxN0ArMwt4j9zPQYirvzQX1TxiSUJOXk8ma_AyYl/pub?output=csv';

// Map configuration
const MAP_CONFIG = {
    center: [-106.5, 39.0],  // Center of Colorado
    zoom: 6.5,
    minZoom: 5,
    maxZoom: 12,
    style: 'mapbox://styles/mapbox/outdoors-v12', // Options: streets-v12, satellite-v9, outdoors-v12
};

// Color scheme (trails open percentage)
const COLOR_SCALE = {
    closed: '#BDBDBD',      // Gray
    veryLow: '#90CAF9',     // Light blue (1-5%)
    low: '#66BB6A',         // Light green (6-25%)
    medium: '#43A047',      // Medium green (26-50%)
    high: '#2E7D32',        // Dark green (51-100%)
};

// Marker sizing (based on total trails)
const MARKER_SIZE = {
    min: 12,    // Smallest resorts (7 trails)
    max: 50,    // Largest resorts (277 trails)
};

// Auto-refresh interval (milliseconds)
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes

