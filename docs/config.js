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
    // Colorado bounds (southwest and northeast corners)
    bounds: [
        [-109.06, 36.99],  // Southwest corner of Colorado
        [-102.04, 41.00]   // Northeast corner of Colorado
    ],
    padding: {
        top: 50,
        bottom: 50,
        left: 50,
        right: 50
    },
    minZoom: 5,
    maxZoom: 12,
    // Custom style with perfect highway visibility and clean grey aesthetic
    style: 'mapbox://styles/evnwlg/cmi2cejel00ni01suefqyfex3',
};

// Cool-toned color scheme: blue → pink-purple gradient
const COLOR_SCALE = {
    closed: '#E8EAED',      // Very light grey - minimal visual weight
    veryLow: '#5BA4E8',     // Medium blue - early season (1-10%)
    low: '#7BB5F5',         // Lighter blue - building (10-35%)
    medium: '#C77DFF',      // Bright purple - moderate (35-75%)
    high: '#B9257A',        // Bold pink-purple - peak season (75%+)
};

// Stroke colors - contemporary and crisp
const STROKE_COLORS = {
    open: '#F5F5F5',        // Almost white - clean, modern
    closed: '#424242',      // Dark grey - strong contrast
};

// Marker sizing (based on total trails)
const MARKER_SIZE = {
    min: 12,    // Smallest resorts - increased for better clickability
    max: 36,    // Largest resorts
};

// Marker opacity
const MARKER_OPACITY = 0.85;  // 85% opacity for fills (allows map to show through)

// Auto-refresh interval (milliseconds)
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes

