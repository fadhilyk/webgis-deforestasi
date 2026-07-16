/**
 * map.js - Leaflet Map Controller
 * ===============================
 * Mengatur inisialisasi peta Leaflet dan memuat data GeoJSON
 * dari backend menggunakan api-client.js.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Pastikan container peta ada
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // 1. Inisialisasi Peta (Center di Kerinci, Jambi)
    const map = L.map('map').setView([-1.9333, 101.4833], 10);

    // 2. Base Map (Google Satellite Hybrid style via Esri/Carto)
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        maxZoom: 18
    }).addTo(map);

    // Tambahkan Penanda (Marker) Lokasi Kerinci
    const kerinciMarker = L.marker([-1.9333, 101.4833]).addTo(map)
        .bindPopup('<b>Kabupaten Kerinci</b><br>Area Monitoring Deforestasi');

    // Objek untuk menyimpan referensi layer
    const layerInstances = {};

    // Style konfigurasi untuk tiap layer
    const layerStyles = {
        'batas-wilayah': {
            color: '#3388ff',
            weight: 3,
            opacity: 0.8,
            fillColor: 'transparent',
            fillOpacity: 0
        },
        'gain': {
            color: '#2ecc71',
            weight: 1,
            fillColor: '#2ecc71',
            fillOpacity: 0.6
        },
        'loss': {
            color: '#e74c3c',
            weight: 1,
            fillColor: '#e74c3c',
            fillOpacity: 0.6
        },
        'target-2024': {
            color: '#f39c12',
            weight: 1,
            fillColor: '#f39c12',
            fillOpacity: 0.4
        },
        'target-2025': {
            color: '#9b59b6',
            weight: 1,
            fillColor: '#9b59b6',
            fillOpacity: 0.4
        }
    };

    /**
     * Generate synthetic ground truth points for visualization
     */
    function generateGroundTruthLayer() {
        const points = L.featureGroup();
        // Generate 150 points scattered around Kerinci bbox
        for (let i = 0; i < 150; i++) {
            const lat = -2.2 + Math.random() * 0.6;
            const lng = 101.2 + Math.random() * 0.5;
            
            // 70% Target (1) Green, 30% Nontarget (0) Red
            const isTarget = Math.random() > 0.3;
            
            const color = isTarget ? '#00ff9d' : '#ff4a4a';
            const label = isTarget ? 'Target (1)' : 'Nontarget (0)';
            
            L.circleMarker([lat, lng], {
                radius: 5,
                fillColor: color,
                color: '#ffffff',
                weight: 1,
                opacity: 1,
                fillOpacity: 0.9
            }).bindPopup(`<div class="p-2"><strong>Ground Truth</strong><br/><span class="small">Class: ${label}</span><br/><span class="small">Lat: ${lat.toFixed(4)}</span><br/><span class="small">Lng: ${lng.toFixed(4)}</span></div>`).addTo(points);
        }
        return points;
    }

    /**
     * Memuat layer GeoJSON dari API dan menambahkannya ke peta
     */
    async function loadLayer(layerName) {
        try {
            // Handle synthetic ground truth layer locally
            if (layerName === 'ground-truth') {
                const gtLayer = generateGroundTruthLayer();
                layerInstances[layerName] = gtLayer;
                const toggle = document.querySelector(`input[data-layer="${layerName}"]`);
                if (toggle && toggle.checked) gtLayer.addTo(map);
                return;
            }

            // Tampilkan loading state di UI (opsional)
            const label = document.querySelector(`label[for="layer-${layerName.split('-')[0]}"]`);
            if (label) label.style.opacity = '0.5';

            // Ambil data dari API
            const geojsonData = await API.getLayer(layerName);
            
            // Buat Leaflet GeoJSON layer
            const geojsonLayer = L.geoJSON(geojsonData, {
                style: layerStyles[layerName] || { color: '#ffffff' },
                onEachFeature: (feature, layer) => {
                    // Tambahkan popup interaktif
                    if (feature.properties) {
                        let popupContent = `<div class="p-2"><strong>${layerName.toUpperCase()}</strong><br/>`;
                        for (const [key, val] of Object.entries(feature.properties)) {
                            popupContent += `<span class="small">${key}: ${val}</span><br/>`;
                        }
                        popupContent += `</div>`;
                        layer.bindPopup(popupContent);
                    }
                }
            });

            // Simpan referensi dan tambahkan ke peta
            layerInstances[layerName] = geojsonLayer;
            
            // Cek apakah toggle checkbox-nya aktif
            const toggle = document.querySelector(`input[data-layer="${layerName}"]`);
            if (toggle && toggle.checked) {
                geojsonLayer.addTo(map);
                
                // Fit bounds ke batas wilayah (hanya sekali saat pertama load batas)
                if (layerName === 'batas-wilayah') {
                    map.fitBounds(geojsonLayer.getBounds());
                }
            }

            if (label) label.style.opacity = '1';

        } catch (error) {
            console.error(`Gagal memuat layer ${layerName}:`, error);
            alert(`Gagal memuat layer ${layerName}. Pastikan server berjalan.`);
        }
    }

    // 3. Event Listeners untuk Toggle Switch
    document.querySelectorAll('.form-check-input').forEach(toggle => {
        toggle.addEventListener('change', (e) => {
            const layerName = e.target.getAttribute('data-layer');
            const layer = layerInstances[layerName];
            
            if (!layer) {
                // Jika layer belum diload, load dulu
                if (e.target.checked) loadLayer(layerName);
                return;
            }

            // Tampilkan atau Sembunyikan layer
            if (e.target.checked) {
                layer.addTo(map);
            } else {
                map.removeLayer(layer);
            }
        });
    });

    // 4. Load Initial Layers (Batas, Gain, Loss)
    const initialLayers = ['batas-wilayah', 'gain', 'loss'];
    initialLayers.forEach(layer => loadLayer(layer));

    // Perbaiki rendering map saat tab Peta Hasil di-klik
    const tabPetaBtn = document.getElementById('tab-peta-btn');
    if (tabPetaBtn) {
        tabPetaBtn.addEventListener('shown.bs.tab', () => {
            map.invalidateSize();
        });
    }
});
