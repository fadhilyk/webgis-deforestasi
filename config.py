"""
Application configuration for WebGIS Monitoring Deforestasi Kerinci.

Defines paths, constants, and GeoJSON file mappings used across the app.
"""

from pathlib import Path

# ── Base directories ────────────────────────────────────────
DATA_FOLDER = Path('data')          # GeoJSON data files
MODELS_FOLDER = Path('models')      # Pre-trained ML models (.pkl)
TEMPLATE_FOLDER = Path('templates') # Jinja2 HTML templates
STATIC_FOLDER = Path('static')      # CSS, JS, images

# ── Map defaults ────────────────────────────────────────────
# Center coordinates for Kerinci Regency, Jambi, Indonesia
MAP_CENTER = [-0.42, 101.27]        # [latitude, longitude]
MAP_ZOOM = 11                       # Default zoom level

# ── GeoJSON file key -> filename mapping ────────────────────
GEOJSON_FILES = {
    'batas_wilayah': 'UAS_Kerinci_BatasWilayah.geojson',
    'gain': 'UAS_Kerinci_Gain.geojson',
    'loss': 'UAS_Kerinci_Loss.geojson',
    'target_2024': 'UAS_Kerinci_Target2024.geojson',
    'target_2025': 'UAS_Kerinci_Target2025.geojson',
}
