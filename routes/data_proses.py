"""
routes/data_proses.py - Tab 2: Data & Proses
===============================================
WebGIS Monitoring Deforestasi Kerinci

Blueprint untuk endpoint Tab 2 (Data & Proses):
- GET /data                    → Render halaman Data & Proses
- GET /api/data/statistics     → Statistik luas gain & loss (hektar & %)
- GET /api/data/metadata       → Informasi sumber data Sentinel-2

Endpoint ini menghitung dan menyajikan:
1. Luas area gain dan loss dalam hektar
2. Persentase perubahan dan net change
3. Metadata citra satelit yang digunakan

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template

from config import DATA_METADATA
from services.geo_service import GeoService
from services.stats_service import StatsService

# ---------------------------------------------------------------------------
# LOGGER & BLUEPRINT
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# Blueprint Tab 2: Data & Proses
data_bp = Blueprint("data_proses", __name__)


# ---------------------------------------------------------------------------
# HELPER: Error Response
# ---------------------------------------------------------------------------

def _error_response(message: str, status_code: int) -> tuple:
    """
    Buat JSON error response yang konsisten.

    Args:
        message (str)    : Pesan error yang deskriptif.
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
# ENDPOINT 1: GET /data — Halaman HTML Tab 2
# ---------------------------------------------------------------------------

@data_bp.route("/data")
def data_page():
    """
    Render halaman Data & Proses (Tab 2).

    Menampilkan statistik perubahan tutupan hutan, grafik distribusi,
    dan metadata sumber data Sentinel-2.

    Returns:
        HTML: Render template 'data_proses.html'.
        JSON: Fallback 200 jika template belum tersedia.

    HTTP Status:
        200 → Halaman berhasil dirender.

    Example:
        GET /data
        → Menampilkan halaman statistik & proses data
    """
    try:
        logger.info("Rendering data_proses page.")
        return render_template("data_proses.html", page_title="Data & Proses")
    except Exception as exc:
        logger.warning("Template 'data_proses.html' belum tersedia: %s", exc)
        return jsonify({
            "message":   "Data & Proses — template belum tersedia",
            "endpoints": {
                "statistics": "/api/data/statistics",
                "metadata":   "/api/data/metadata",
            },
        }), 200


# ---------------------------------------------------------------------------
# ENDPOINT 2: GET /api/data/statistics — Statistik Gain & Loss
# ---------------------------------------------------------------------------

@data_bp.route("/api/data/statistics")
def get_statistics():
    """
    Hitung dan kembalikan statistik luas perubahan tutupan hutan Kerinci.

    Memuat data GeoJSON gain dan loss, menghitung luas masing-masing
    dalam hektar, lalu mengembalikan statistik lengkap termasuk
    persentase dan net change.

    Returns:
        JSON: Statistik perubahan dengan struktur:
              {
                  "gain_ha"            : float,  # Luas gain dalam hektar
                  "loss_ha"            : float,  # Luas loss dalam hektar
                  "total_change_ha"    : float,  # Total perubahan (gain+loss)
                  "net_change_ha"      : float,  # Net change (gain-loss)
                  "percentage_gain"    : float,  # % gain dari total perubahan
                  "percentage_loss"    : float,  # % loss dari total perubahan
                  "net_change_percent" : float,  # % net change dari total
                  "status"             : str,    # 'net_gain' atau 'net_loss'
                  "gain_feature_count" : int,    # Jumlah polygon gain
                  "loss_feature_count" : int,    # Jumlah polygon loss
                  "timestamp"          : str,    # Waktu kalkulasi (ISO 8601)
              }

    HTTP Status:
        200 → Statistik berhasil dihitung dan dikembalikan.
        500 → Gagal memuat GeoJSON atau menghitung statistik.

    Example:
        GET /api/data/statistics
        → {
              "gain_ha": 247172.75,
              "loss_ha": 242638.92,
              "net_change_ha": 4533.83,
              "status": "net_gain",
              ...
          }
    """
    # Load GeoDataFrame gain
    try:
        logger.info("Loading GeoJSON 'gain' untuk kalkulasi statistik ...")
        gain_gdf = GeoService.load_geojson("gain")
    except FileNotFoundError:
        logger.error("File GeoJSON 'gain' tidak ditemukan.")
        return _error_response(
            "File data 'gain' tidak ditemukan di server. "
            "Pastikan UAS_Kerinci_Gain.geojson ada di folder /data/.",
            500,
        )
    except Exception as exc:
        logger.exception("Gagal load GeoJSON 'gain': %s", exc)
        return _error_response(f"Gagal memuat data gain: {str(exc)}", 500)

    # Load GeoDataFrame loss
    try:
        logger.info("Loading GeoJSON 'loss' untuk kalkulasi statistik ...")
        loss_gdf = GeoService.load_geojson("loss")
    except FileNotFoundError:
        logger.error("File GeoJSON 'loss' tidak ditemukan.")
        return _error_response(
            "File data 'loss' tidak ditemukan di server. "
            "Pastikan UAS_Kerinci_Loss.geojson ada di folder /data/.",
            500,
        )
    except Exception as exc:
        logger.exception("Gagal load GeoJSON 'loss': %s", exc)
        return _error_response(f"Gagal memuat data loss: {str(exc)}", 500)

    # Hitung statistik via StatsService
    try:
        logger.info("Menghitung statistik gain vs loss ...")
        stats = StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)
    except (ValueError, RuntimeError) as exc:
        logger.exception("Gagal menghitung statistik: %s", exc)
        return _error_response(f"Gagal menghitung statistik: {str(exc)}", 500)

    # Tambahkan timestamp kalkulasi
    stats["timestamp"] = datetime.now(timezone.utc).isoformat()

    logger.info(
        "Statistik berhasil dihitung: gain=%.2f ha, loss=%.2f ha, status=%s",
        stats["gain_ha"], stats["loss_ha"], stats["status"],
    )
    return jsonify(stats), 200


# ---------------------------------------------------------------------------
# ENDPOINT 3: GET /api/data/metadata — Informasi Sumber Data
# ---------------------------------------------------------------------------

@data_bp.route("/api/data/metadata")
def get_metadata():
    """
    Kembalikan metadata sumber data citra satelit yang digunakan.

    Memberikan informasi tentang spesifikasi data Sentinel-2 yang
    digunakan sebagai input klasifikasi tutupan hutan Kerinci.

    Returns:
        JSON: Metadata sumber data dengan struktur:
              {
                  "satellite"    : str,   # Nama & koleksi satelit
                  "period_2024"  : str,   # Periode akuisisi 2024
                  "period_2025"  : str,   # Periode akuisisi 2025
                  "cloud_masking": str,   # Metode cloud masking
                  "composite"    : str,   # Metode komposit citra
                  "bands"        : list,  # Band spektral yang digunakan
                  "indexes"      : list,  # Indeks vegetasi/lahan yang dihitung
                  "crs"          : str,   # Sistem koordinat (EPSG)
                  "provider"     : str,   # Penyedia data
                  "platform"     : str,   # Platform pemrosesan
              }

    HTTP Status:
        200 → Metadata selalu tersedia (data statis dari config).

    Example:
        GET /api/data/metadata
        → {
              "satellite": "Sentinel-2 COPERNICUS/S2_SR_HARMONIZED",
              "period_2024": "01 Jan - 31 Des 2024",
              "bands": ["B2", "B3", "B4", "B8", "B11", "B12"],
              ...
          }
    """
    # Metadata statis dari config.py + informasi tambahan
    metadata = {
        **DATA_METADATA,
        "provider":      "European Space Agency (ESA) via Google Earth Engine",
        "platform":      "Google Earth Engine (GEE)",
        "spatial_resolution": {
            "B2_B3_B4_B8":  "10 meter",
            "B11_B12":      "20 meter (resampled ke 10m)",
        },
        "classification": {
            "algorithm":        "Random Forest (100 Trees)",
            "training_samples": "Otomatis dari GEE (Dinamis)",
            "testing_samples":  "Otomatis dari GEE (Dinamis)",
            "split_ratio":      "70:30 (Seed: 42)",
        },
        "output_layers": {
            "gain":         "Area pertambahan tutupan hutan 2024→2025",
            "loss":         "Area kehilangan tutupan hutan 2024→2025",
            "target_2024":  "Prediksi model untuk tahun 2024",
            "target_2025":  "Prediksi model untuk tahun 2025",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    logger.debug("Metadata endpoint dipanggil.")
    return jsonify(metadata), 200


# ---------------------------------------------------------------------------
# ENDPOINT 4: GET /api/data/summary — Ringkasan Lengkap (bonus)
# ---------------------------------------------------------------------------

@data_bp.route("/api/data/summary")
def get_summary():
    """
    Kembalikan ringkasan lengkap: statistik + metadata dalam satu response.

    Menggabungkan hasil /api/data/statistics dan /api/data/metadata
    agar frontend bisa fetch sekali untuk mendapatkan semua data Tab 2.

    Returns:
        JSON: Gabungan statistik dan metadata:
              {
                  "statistics": { ... },  # Hasil dari get_statistics()
                  "metadata":   { ... },  # Hasil dari get_metadata()
                  "timestamp":  str,
              }

    HTTP Status:
        200 → Data berhasil dimuat.
        500 → Gagal memuat data statistik.

    Example:
        GET /api/data/summary
        → { "statistics": {...}, "metadata": {...} }
    """
    # Load dan hitung statistik
    try:
        gain_gdf = GeoService.load_geojson("gain")
        loss_gdf = GeoService.load_geojson("loss")
        stats    = StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)
    except Exception as exc:
        logger.exception("Gagal menghitung statistik di summary: %s", exc)
        return _error_response(f"Gagal memuat data statistik: {str(exc)}", 500)

    # Metadata statis
    metadata = {
        **DATA_METADATA,
        "provider": "European Space Agency (ESA) via Google Earth Engine",
        "platform": "Google Earth Engine (GEE)",
    }

    response = {
        "statistics": stats,
        "metadata":   metadata,
        "timestamp":  datetime.now(timezone.utc).isoformat(),
    }

    logger.info("Summary endpoint berhasil dipanggil.")
    return jsonify(response), 200
