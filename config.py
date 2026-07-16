"""
config.py - Application Configuration
======================================
WebGIS Monitoring Deforestasi Kerinci
Berisi semua konstanta dan konfigurasi path untuk aplikasi.

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# FOLDER PATHS
# ---------------------------------------------------------------------------

# Root direktori proyek (lokasi config.py berada)
BASE_DIR = Path(__file__).resolve().parent

# Folder data: menyimpan semua file GeoJSON
DATA_FOLDER = BASE_DIR / "data"

# Folder models: menyimpan file model Random Forest (.pkl)
MODELS_FOLDER = BASE_DIR / "models"

# Folder templates: menyimpan file HTML Jinja2
TEMPLATE_FOLDER = BASE_DIR / "templates"

# Folder static: menyimpan file CSS, JS, dan aset lainnya
STATIC_FOLDER = BASE_DIR / "static"

# ---------------------------------------------------------------------------
# MAP CONFIGURATION
# ---------------------------------------------------------------------------

# Koordinat pusat peta Kerinci [latitude, longitude]
MAP_CENTER = [-0.42, 101.27]

# Zoom level default saat peta pertama kali dibuka
MAP_ZOOM = 11

# Tile layer URL untuk basemap OpenStreetMap
TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

# Attribution untuk basemap
TILE_ATTRIBUTION = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">'
    "OpenStreetMap</a> contributors"
)

# ---------------------------------------------------------------------------
# GEOJSON FILES
# ---------------------------------------------------------------------------

# Mapping nama layer → nama file GeoJSON di folder /data/
# Key digunakan sebagai parameter URL endpoint API
GEOJSON_FILES = {
    "batas-wilayah": "UAS_Kerinci_BatasWilayah.geojson",  # Batas wilayah Kerinci
    "gain":          "UAS_Kerinci_Gain.geojson",           # Area pertambahan hutan
    "loss":          "UAS_Kerinci_Loss.geojson",           # Area kehilangan hutan
    "target-2024":   "UAS_Kerinci_Target2024.geojson",     # Target tahun 2024
    "target-2025":   "UAS_Kerinci_Target2025.geojson",     # Target tahun 2025
}

# ---------------------------------------------------------------------------
# MODEL FILES
# ---------------------------------------------------------------------------

# Mapping tahun → nama file model Random Forest (.pkl)
MODEL_FILES = {
    2024: "random_forest_2024.pkl",
    2025: "random_forest_2025.pkl",
}

# ---------------------------------------------------------------------------
# DATA METADATA (Sentinel-2)
# ---------------------------------------------------------------------------

# Informasi sumber data satelit yang digunakan
DATA_METADATA = {
    "satellite":    "Sentinel-2 COPERNICUS/S2_SR_HARMONIZED",
    "period_2024":  "01 Juni - 30 September 2024",
    "period_2025":  "01 Juni - 30 September 2025",
    "cloud_masking": "QA60 Bitmask + Cloud < 20%",
    "composite":    "Median Composite",
    "bands":        ["B2", "B3", "B4", "B8", "B11", "B12", "NDVI"],
    "indexes":      ["NDVI"],
    "crs":          "EPSG:4326",
}

# ---------------------------------------------------------------------------
# FLASK CONFIGURATION
# ---------------------------------------------------------------------------

class Config:
    """Base configuration class untuk Flask application."""

    # Secret key untuk session Flask (ganti di production via .env)
    SECRET_KEY = "webgis-deforestasi-kerinci-secret-key"

    # Mode debug (dimatikan di production)
    DEBUG = False

    # Mode testing
    TESTING = False

    # Maksimum request size (50 MB untuk file GeoJSON besar)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    # JSON response akan di-sort by key
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Konfigurasi untuk environment development (local)."""

    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    """Konfigurasi untuk environment production (Render.com)."""

    DEBUG = False
    ENV = "production"


# Mapping nama environment → class konfigurasi
config_by_name = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}
