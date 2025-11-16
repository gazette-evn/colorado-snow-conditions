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
    // Using full HTTPS URL to bypass protocol-based caching
    style: 'https://api.mapbox.com/styles/v1/evnwlg/cmi25lrgp00nf01sug74vg0pt?fresh=20241116',
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
    open: '#F5F5F5',        // Almost white - clean, modern
    closed: '#424242',      // Dark grey - strong contrast
};

// Marker sizing (based on total trails)
const MARKER_SIZE = {
    min: 8,     // Smallest resorts (7 trails)
    max: 32,    // Largest resorts (277 trails) - smaller for cleaner look
};

// Marker opacity
const MARKER_OPACITY = 0.85;  // 85% opacity for fills (allows map to show through)

// Auto-refresh interval (milliseconds)
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes

