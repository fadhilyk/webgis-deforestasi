"""
routes/peta.py - Tab 1: Peta Hasil
=====================================
WebGIS Monitoring Deforestasi Kerinci

Blueprint untuk endpoint Tab 1 (Peta Hasil):
- GET /map                       → Render halaman peta interaktif
- GET /api/layers/<layer_name>   → Serve GeoJSON layer untuk Leaflet

Endpoint ini melayani:
1. Halaman HTML peta (Leaflet.js)
2. Data GeoJSON untuk 5 layer: batas-wilayah, gain, loss, target-2024, target-2025

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request

from config import GEOJSON_FILES, MAP_CENTER, MAP_ZOOM
from services.geo_service import GeoService

# ---------------------------------------------------------------------------
# LOGGER & BLUEPRINT
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# Blueprint dengan prefix URL /  (endpoint langsung di root)
peta_bp = Blueprint("peta", __name__)


# ---------------------------------------------------------------------------
# HELPER: Error Response
# ---------------------------------------------------------------------------

def _error_response(message: str, status_code: int) -> tuple:
    """
    Buat JSON error response yang konsisten.

    Args:
        message (str)   : Pesan error yang deskriptif.
        status_code (int): HTTP status code (400, 404, 500, dll.)

    Returns:
        tuple: (Response, status_code) siap di-return dari endpoint.
    """
    return jsonify({
        "error":     message,
        "status":    status_code,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), status_code


# ---------------------------------------------------------------------------
# ENDPOINT 1: GET /map — Halaman Peta HTML
# ---------------------------------------------------------------------------

@peta_bp.route("/map")
def map_page():
    """
    Render halaman peta interaktif Leaflet.js (Tab 1: Peta Hasil).

    Mengirimkan data konfigurasi peta ke template Jinja2:
    - map_center  : Koordinat pusat peta Kerinci [lat, lng]
    - map_zoom    : Zoom level default
    - layer_names : Daftar nama layer yang tersedia

    Returns:
        HTML: Render template 'peta.html' dengan konteks konfigurasi peta.
        JSON: Fallback 200 jika template belum dibuat (fase development).

    HTTP Status:
        200 → Halaman berhasil dirender.
        500 → Template error atau server error.

    Example:
        GET /map
        → Menampilkan halaman peta Kerinci dengan Leaflet.js
    """
    try:
        context = {
            "map_center":   MAP_CENTER,          # [-0.42, 101.27]
            "map_zoom":     MAP_ZOOM,            # 11
            "layer_names":  list(GEOJSON_FILES.keys()),  # Daftar 5 layer
            "page_title":   "Peta Hasil Deforestasi Kerinci",
        }
        logger.info("Rendering map page.")
        return render_template("peta.html", **context)

    except Exception as exc:
        # Fallback jika template belum dibuat
        logger.warning("Template 'peta.html' belum tersedia: %s", exc)
        return jsonify({
            "message":    "Peta Hasil — template belum tersedia",
            "map_center": MAP_CENTER,
            "map_zoom":   MAP_ZOOM,
            "layers":     list(GEOJSON_FILES.keys()),
        }), 200


# ---------------------------------------------------------------------------
# ENDPOINT 2: GET /api/layers/<layer_name> — Serve GeoJSON
# ---------------------------------------------------------------------------

@peta_bp.route("/api/layers/<string:layer_name>")
def get_layer(layer_name: str):
    """
    Serve data GeoJSON layer untuk ditampilkan di peta Leaflet.

    Menerima nama layer sebagai URL parameter, memuat file GeoJSON
    dari folder /data/ menggunakan GeoService, dan mengembalikan
    GeoJSON FeatureCollection sebagai JSON response.

    Args (URL Parameter):
        layer_name (str): Nama layer yang diminta. Nilai yang valid:
                          - 'batas-wilayah' → UAS_Kerinci_BatasWilayah.geojson
                          - 'gain'          → UAS_Kerinci_Gain.geojson
                          - 'loss'          → UAS_Kerinci_Loss.geojson
                          - 'target-2024'   → UAS_Kerinci_Target2024.geojson
                          - 'target-2025'   → UAS_Kerinci_Target2025.geojson

    Returns:
        JSON: GeoJSON FeatureCollection dengan struktur:
              {
                  "type": "FeatureCollection",
                  "features": [...],
                  "bbox": [...]
              }

    HTTP Status:
        200 → GeoJSON berhasil dimuat dan dikembalikan.
        400 → layer_name kosong atau format tidak valid.
        404 → layer_name tidak dikenali atau file tidak ditemukan.
        500 → Gagal membaca atau memproses file GeoJSON.

    Example:
        GET /api/layers/gain
        → Response: GeoJSON FeatureCollection area gain Kerinci

        GET /api/layers/invalid
        → Response: {"error": "Layer 'invalid' tidak dikenali", "status": 404}
    """
    # Sanitasi input
    layer_name = layer_name.strip().lower()

    if not layer_name:
        return _error_response("Nama layer tidak boleh kosong.", 400)

    # Validasi layer_name terhadap daftar yang diizinkan
    if layer_name not in GEOJSON_FILES:
        valid_layers = list(GEOJSON_FILES.keys())
        logger.warning("Layer tidak dikenali: '%s'", layer_name)
        return _error_response(
            f"Layer '{layer_name}' tidak dikenali. "
            f"Layer yang tersedia: {valid_layers}",
            404,
        )

    # Load GeoJSON via GeoService (dengan caching otomatis)
    try:
        logger.info("Request layer: '%s' dari %s", layer_name, request.remote_addr)
        gdf = GeoService.load_geojson(layer_name)

    except FileNotFoundError as exc:
        logger.error("File GeoJSON tidak ditemukan: %s", exc)
        return _error_response(
            f"File GeoJSON untuk layer '{layer_name}' tidak ditemukan di server. "
            "Pastikan file ada di folder /data/.",
            404,
        )

    except ValueError as exc:
        logger.error("Layer tidak valid: %s", exc)
        return _error_response(str(exc), 404)

    except Exception as exc:
        logger.exception("Gagal load layer '%s': %s", layer_name, exc)
        return _error_response(
            f"Gagal memuat layer '{layer_name}': {str(exc)}",
            500,
        )

    # Konversi GeoDataFrame → GeoJSON dict
    try:
        geojson_dict = GeoService.geojson_to_json(gdf)

    except (ValueError, RuntimeError) as exc:
        logger.exception("Gagal konversi GeoDataFrame ke JSON: %s", exc)
        return _error_response(
            f"Gagal memproses data layer '{layer_name}': {str(exc)}",
            500,
        )

    logger.info(
        "Layer '%s' berhasil dikirim: %d features.",
        layer_name,
        len(geojson_dict.get("features", [])),
    )
    return jsonify(geojson_dict), 200


# ---------------------------------------------------------------------------
# ENDPOINT 3: GET /api/layers — Daftar Layer Tersedia
# ---------------------------------------------------------------------------

@peta_bp.route("/api/layers")
def list_layers():
    """
    Kembalikan daftar semua layer GeoJSON yang tersedia beserta statusnya.

    Berguna untuk frontend agar tahu layer apa saja yang bisa diminta,
    dan apakah file fisiknya benar-benar ada di server.

    Returns:
        JSON: Daftar layer dengan status ketersediaan file:
              {
                  "layers": [
                      {
                          "name": "gain",
                          "filename": "UAS_Kerinci_Gain.geojson",
                          "url": "/api/layers/gain",
                          "available": true
                      },
                      ...
                  ],
                  "total": 5
              }

    HTTP Status:
        200 → Selalu berhasil (daftar layer adalah data statis).

    Example:
        GET /api/layers
        → Daftar 5 layer beserta status file di server
    """
    from config import DATA_FOLDER

    layers_info = []
    for name, filename in GEOJSON_FILES.items():
        filepath = DATA_FOLDER / filename
        layers_info.append({
            "name":      name,
            "filename":  filename,
            "url":       f"/api/layers/{name}",
            "available": filepath.exists(),
        })

    logger.debug("Layer list requested: %d layers.", len(layers_info))
    return jsonify({
        "layers": layers_info,
        "total":  len(layers_info),
    }), 200
