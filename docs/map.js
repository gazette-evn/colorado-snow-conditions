// Colorado Snow Conditions - Mapbox Map
// Loads data from Google Sheets and renders interactive resort markers

// Configuration
mapboxgl.accessToken = MAPBOX_TOKEN;

// State
let map;
let resortData = [];
let markers = [];
let currentFilter = 'all'; // 'all' or 'open'

// Initialize map on page load
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadData();
    setupEventListeners();
    
    // Auto-refresh data every 5 minutes
    setInterval(loadData, 5 * 60 * 1000);
});

function initMap() {
    map = new mapboxgl.Map({
        container: 'map',
        style: MAP_CONFIG.style,
        center: MAP_CONFIG.center,
        zoom: MAP_CONFIG.zoom,
        minZoom: MAP_CONFIG.minZoom,
        maxZoom: MAP_CONFIG.maxZoom,
        pitch: 0
    });
    
    // Add navigation controls
    map.addControl(new mapboxgl.NavigationControl(), 'top-left');
    
    // Add fullscreen control
    map.addControl(new mapboxgl.FullscreenControl(), 'top-left');
    
    // Use light-v11 as-is - it's already clean and roads are visible enough
    // Focus on making the resort markers stand out instead of fighting with the basemap
}

function setupEventListeners() {
    document.getElementById('filterOpen').addEventListener('click', () => {
        setFilter('all');
    });
    
    document.getElementById('filterClosed').addEventListener('click', () => {
        setFilter('open');
    });
}

function setFilter(filter) {
    currentFilter = filter;
    
    // Update button states
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (filter === 'all') {
        document.getElementById('filterOpen').classList.add('active');
    } else {
        document.getElementById('filterClosed').classList.add('active');
    }
    
    // Re-render markers with filter
    renderMarkers();
}

async function loadData() {
    try {
        console.log('Fetching data from Google Sheets...');
        
        const response = await fetch(DATA_URL);
        const csvText = await response.text();
        
        // Parse CSV
        resortData = parseCSV(csvText);
        console.log(`Loaded ${resortData.length} resorts`);
        
        // Update last update time
        if (resortData.length > 0) {
            const lastUpdate = resortData[0]['Last Updated'] || 'Unknown';
            // Format: "2025-11-16 11:46" → "Nov 16, 11:46am"
            const formatted = formatTimestamp(lastUpdate);
            document.getElementById('lastUpdate').textContent = `Updated ${formatted}`;
        }
        
        // Render markers
        renderMarkers();
        
        // Hide loading indicator
        document.getElementById('loading').classList.add('hidden');
        
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('loading').innerHTML = 
            '<p style="color: #D32F2F;">Error loading resort data. Please try again later.</p>';
    }
}

function parseCSV(csv) {
    const lines = csv.trim().split('\n');
    const headers = lines[0].split(',');
    
    const data = [];
    for (let i = 1; i < lines.length; i++) {
        const values = parseCSVLine(lines[i]);
        const resort = {};
        
        headers.forEach((header, index) => {
            resort[header.trim()] = values[index] ? values[index].trim() : '';
        });
        
        data.push(resort);
    }
    
    return data;
}

function parseCSVLine(line) {
    // Handle CSV with quoted fields
    const result = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        
        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            result.push(current);
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current);
    
    return result;
}

function renderMarkers() {
    // Clear existing markers
    markers.forEach(marker => marker.remove());
    markers = [];
    
    // Filter resorts based on current filter
    let filteredResorts = resortData;
    if (currentFilter === 'open') {
        filteredResorts = resortData.filter(r => r.Status === 'Open');
    }
    
    // Create markers for each resort
    filteredResorts.forEach(resort => {
        const lat = parseFloat(resort.Latitude);
        const lng = parseFloat(resort.Longitude);
        
        if (isNaN(lat) || isNaN(lng)) {
            console.warn(`Invalid coordinates for ${resort['Resort Name']}`);
            return;
        }
        
        // Calculate marker size based on total trails
        const totalTrails = parseFloat(resort['Total Trails']) || 0;
        const size = calculateMarkerSize(totalTrails);
        
        // Calculate marker color based on trails open percentage
        const trailsOpenPct = parseFloat(resort['Trails Open %']) || 0;
        const color = getColorForPercentage(trailsOpenPct, resort.Status);
        
        // Calculate stroke color based on status
        const isOpen = resort.Status === 'Open';
        const strokeColor = isOpen ? STROKE_COLORS.open : STROKE_COLORS.closed;
        
        // Create marker element with fixed positioning
        const el = document.createElement('div');
        el.className = 'custom-marker';
        
        // Convert hex color to rgba for opacity
        const rgbaColor = hexToRgba(color, MARKER_OPACITY);
        
        el.style.width = `${size}px`;
        el.style.height = `${size}px`;
        el.style.borderRadius = '50%';
        el.style.backgroundColor = rgbaColor;  // Use rgba for opacity
        el.style.border = `2px solid ${strokeColor}`;
        el.style.boxShadow = '0 2px 8px rgba(0,0,0,0.3)';
        el.style.cursor = 'pointer';
        
        // Store original size for hover effect
        el.dataset.originalSize = size;
        
        // Create popup first (before event listeners reference it)
        const popup = new mapboxgl.Popup({
            offset: 25,
            closeButton: true,
            closeOnClick: false,
            maxWidth: '320px'
        }).setHTML(createPopupHTML(resort));
        
        // Track if popup is pinned (clicked)
        let isPinned = false;
        
        // Hover effects - show popup on hover
        el.addEventListener('mouseenter', () => {
            const newSize = size * 1.2;
            el.style.width = `${newSize}px`;
            el.style.height = `${newSize}px`;
            el.style.boxShadow = '0 4px 16px rgba(0,0,0,0.5)';
            
            // Show popup on hover if not already pinned
            if (!isPinned) {
                popup.addTo(map);
            }
        });
        
        el.addEventListener('mouseleave', () => {
            el.style.width = `${size}px`;
            el.style.height = `${size}px`;
            el.style.boxShadow = '0 3px 12px rgba(0,0,0,0.4)';
            
            // Hide popup on mouse leave if not pinned
            if (!isPinned) {
                popup.remove();
            }
        });
        
        // Click to pin/unpin popup
        el.addEventListener('click', (e) => {
            e.stopPropagation();
            
            // Close all other popups and unpin them
            markers.forEach(m => {
                if (m !== marker) {
                    m.getPopup().remove();
                    const markerEl = m.getElement();
                    markerEl._isPinned = false;
                }
            });
            
            // Toggle this popup's pinned state
            isPinned = !isPinned;
            el._isPinned = isPinned;
            
            if (isPinned) {
                popup.addTo(map);
            }
        });
        
        // Create and add marker with anchor set to center
        const marker = new mapboxgl.Marker({
            element: el,
            anchor: 'center'  // This prevents the diagonal movement!
        })
            .setLngLat([lng, lat])
            .setPopup(popup)
            .addTo(map);
        
        markers.push(marker);
    });
    
    console.log(`Rendered ${markers.length} markers`);
}

function calculateMarkerSize(totalTrails) {
    // Size markers based on resort size (total trails)
    const minSize = MARKER_SIZE.min;
    const maxSize = MARKER_SIZE.max;
    const minTrails = 7;  // Echo Mountain
    const maxTrails = 277; // Vail
    
    if (totalTrails <= 0) return minSize;
    
    const normalized = (totalTrails - minTrails) / (maxTrails - minTrails);
    const size = minSize + (normalized * (maxSize - minSize));
    
    return Math.max(minSize, Math.min(maxSize, size));
}

function hexToRgba(hex, alpha) {
    // Convert hex color to rgba with opacity
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function formatTimestamp(timestamp) {
    // Format "2025-11-16 11:46" to "Nov 16, 11:46am"
    try {
        const date = new Date(timestamp);
        const month = date.toLocaleDateString('en-US', { month: 'short' });
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const ampm = hours >= 12 ? 'pm' : 'am';
        const displayHours = hours % 12 || 12;
        
        return `${month} ${day}, ${displayHours}:${minutes}${ampm}`;
    } catch (e) {
        return timestamp;
    }
}

function getColorForPercentage(percent, status) {
    // Modern color scale - uses Google Material colors for sharp, contemporary look
    if (status === 'Closed' || percent === 0) {
        return COLOR_SCALE.closed;  // Very light grey
    } else if (percent < 5) {
        return COLOR_SCALE.veryLow;  // Blue (early season)
    } else if (percent < 25) {
        return COLOR_SCALE.low;  // Green (building)
    } else if (percent < 50) {
        return COLOR_SCALE.medium;  // Yellow (moderate)
    } else {
        return COLOR_SCALE.high;  // Red/orange (peak)
    }
}

function createPopupHTML(resort) {
    const status = resort.Status || 'Unknown';
    const statusClass = status.toLowerCase();
    
    // Snow data
    const snow24h = resort['24h Snowfall (in)'] || '0';
    const snow48h = resort['48h Snowfall (in)'] || '0';
    const baseDepth = resort['Base Depth (in)'] || '0';
    const midDepth = resort['Mid-Mtn Depth (in)'] || '0';
    const surface = resort['Surface Conditions'] || 'N/A';
    
    // Terrain data
    const openTrails = resort['Open Trails'] || '0';
    const totalTrails = resort['Total Trails'] || '0';
    const trailsPct = resort['Trails Open %'] || '0';
    const openLifts = resort['Open Lifts'] || '0';
    const totalLifts = resort['Total Lifts'] || '0';
    const liftsPct = resort['Lifts Open %'] || '0';
    
    // Metadata
    const source = resort['Data Source'] || '';
    const updated = resort['Last Updated'] || '';
    
    return `
        <div class="popup-header">${resort['Resort Name']}</div>
        <div class="popup-status ${statusClass}">${status}</div>
        
        <div class="popup-section">
            <div class="popup-label">Snow Conditions</div>
            <div class="popup-data">
                <span class="popup-data-label">24h Snowfall:</span>
                <span class="popup-data-value">${snow24h}"</span>
            </div>
            <div class="popup-data">
                <span class="popup-data-label">48h Snowfall:</span>
                <span class="popup-data-value">${snow48h}"</span>
            </div>
            <div class="popup-data">
                <span class="popup-data-label">Base Depth:</span>
                <span class="popup-data-value">${baseDepth}"</span>
            </div>
            ${midDepth !== '0' ? `
            <div class="popup-data">
                <span class="popup-data-label">Mid-Mtn Depth:</span>
                <span class="popup-data-value">${midDepth}"</span>
            </div>` : ''}
            ${surface !== 'N/A' && surface !== '' ? `
            <div class="popup-data">
                <span class="popup-data-label">Surface:</span>
                <span class="popup-data-value">${surface}</span>
            </div>` : ''}
        </div>
        
        <div class="popup-section">
            <div class="popup-label">Terrain</div>
            <div class="popup-data">
                <span class="popup-data-label">Trails:</span>
                <span class="popup-data-value">${openTrails}/${totalTrails} (${trailsPct}%)</span>
            </div>
            <div class="popup-data">
                <span class="popup-data-label">Lifts:</span>
                <span class="popup-data-value">${openLifts}/${totalLifts} (${liftsPct}%)</span>
            </div>
        </div>
        
        <div class="popup-footer">
            ${updated ? `Updated: ${updated}<br>` : ''}
            Source: ${source}
        </div>
    `;
}

// Handle errors
window.addEventListener('error', (event) => {
    console.error('JavaScript error:', event.error);
});

