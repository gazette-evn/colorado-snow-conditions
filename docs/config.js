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
    // Light style with visible roads - clean and modern
    style: 'mapbox://styles/mapbox/light-v11',
};

// Modern, sharp color scheme inspired by contemporary data viz
const COLOR_SCALE = {
    closed: '#E8EAED',      // Very light grey (almost white) - minimal visual weight
    veryLow: '#4285F4',     // Google blue - vibrant but professional (1-5%)
    low: '#34A853',         // Google green - fresh and modern (6-25%)
    medium: '#FBBC04',      // Google yellow - energetic (26-50%)
    high: '#EA4335',        // Google red/orange - high energy (51-100%)
};

// Stroke colors - contemporary and crisp
const STROKE_COLORS = {
    open: '#1A73E8',        // Bright blue - modern, high contrast
    closed: '#BDC1C6',      // Medium grey - subtle but visible
};

// Marker sizing (based on total trails)
const MARKER_SIZE = {
    min: 12,    // Smallest resorts (7 trails)
    max: 50,    // Largest resorts (277 trails)
};

// Auto-refresh interval (milliseconds)
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes

