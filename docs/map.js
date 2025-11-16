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
        style: 'mapbox://styles/mapbox/outdoors-v12', // Terrain style
        center: [-106.5, 39.0], // Center of Colorado
        zoom: 6.5,
        pitch: 0
    });
    
    // Add navigation controls
    map.addControl(new mapboxgl.NavigationControl(), 'top-left');
    
    // Add fullscreen control
    map.addControl(new mapboxgl.FullscreenControl(), 'top-left');
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
            document.getElementById('lastUpdate').textContent = `Updated: ${lastUpdate}`;
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
        
        // Create marker element
        const el = document.createElement('div');
        el.className = 'marker';
        el.style.width = `${size}px`;
        el.style.height = `${size}px`;
        el.style.borderRadius = '50%';
        el.style.backgroundColor = color;
        el.style.border = '2px solid white';
        el.style.boxShadow = '0 2px 8px rgba(0,0,0,0.3)';
        el.style.cursor = 'pointer';
        el.style.transition = 'transform 0.2s';
        
        // Hover effect
        el.addEventListener('mouseenter', () => {
            el.style.transform = 'scale(1.15)';
        });
        el.addEventListener('mouseleave', () => {
            el.style.transform = 'scale(1)';
        });
        
        // Create popup
        const popup = new mapboxgl.Popup({
            offset: size / 2 + 10,
            closeButton: true,
            closeOnClick: false
        }).setHTML(createPopupHTML(resort));
        
        // Create and add marker
        const marker = new mapboxgl.Marker(el)
            .setLngLat([lng, lat])
            .setPopup(popup)
            .addTo(map);
        
        markers.push(marker);
    });
    
    console.log(`Rendered ${markers.length} markers`);
}

function calculateMarkerSize(totalTrails) {
    // Size markers based on resort size (total trails)
    // Range: 10px (tiny resorts) to 50px (huge resorts like Vail)
    const minSize = 12;
    const maxSize = 50;
    const minTrails = 7;  // Echo Mountain
    const maxTrails = 277; // Vail
    
    if (totalTrails <= 0) return minSize;
    
    const normalized = (totalTrails - minTrails) / (maxTrails - minTrails);
    const size = minSize + (normalized * (maxSize - minSize));
    
    return Math.max(minSize, Math.min(maxSize, size));
}

function getColorForPercentage(percent, status) {
    // Color scale for trails open percentage
    if (status === 'Closed' || percent === 0) {
        return '#BDBDBD'; // Gray for closed
    } else if (percent < 5) {
        return '#90CAF9'; // Light blue (just opened)
    } else if (percent < 25) {
        return '#66BB6A'; // Light green
    } else if (percent < 50) {
        return '#43A047'; // Medium green
    } else {
        return '#2E7D32'; // Dark green (mostly open)
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

