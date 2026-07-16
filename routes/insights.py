"""
routes/insights.py - Tab 4: Insight Hasil
============================================
WebGIS Monitoring Deforestasi Kerinci

Blueprint untuk endpoint Tab 4 (Insight Hasil):
- GET /insights                  → Render halaman insight & kesimpulan
- GET /api/insights/summary      → Ringkasan statistik keseluruhan
- GET /api/insights/spatial      → Distribusi spasial perubahan hutan

Endpoint ini menyajikan ringkasan akhir analisis deforestasi:
1. Perbandingan target 2024 vs 2025
2. Gain vs loss dan net change
3. Distribusi spasial perubahan (Timur vs Barat)
4. Kesimpulan dan temuan utama

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template

from services.geo_service import GeoService
from services.stats_service import StatsService

# ---------------------------------------------------------------------------
# LOGGER & BLUEPRINT
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# Blueprint Tab 4: Insight Hasil
insights_bp = Blueprint("insights", __name__)


# ---------------------------------------------------------------------------
# HELPER: Error Response
# ---------------------------------------------------------------------------

def _error_response(message: str, status_code: int) -> tuple:
    """
    Buat JSON error response yang konsisten.

    Args:
        message (str)    : Pesan error yang deskriptif.
        status_code (int): HTTP status code.

    Returns:
        tuple: (Response, status_code).
    """
    return jsonify({
        "error":     message,
        "status":    status_code,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), status_code


# ---------------------------------------------------------------------------
# ENDPOINT 1: GET /insights — Halaman HTML Tab 4
# ---------------------------------------------------------------------------

@insights_bp.route("/insights")
def insights_page():
    """
    Render halaman Insight Hasil (Tab 4).

    Menampilkan ringkasan akhir analisis deforestasi Kerinci:
    kesimpulan, distribusi spasial, dan rekomendasi.

    Returns:
        HTML: Render template 'insights.html'.
        JSON: Fallback 200 jika template belum tersedia.

    HTTP Status:
        200 → Halaman berhasil dirender.

    Example:
        GET /insights
        → Menampilkan halaman insight & kesimpulan
    """
    try:
        logger.info("Rendering insights page.")
        return render_template("insights.html", page_title="Insight Hasil")
    except Exception as exc:
        logger.warning("Template 'insights.html' belum tersedia: %s", exc)
        return jsonify({
            "message":   "Insight Hasil — template belum tersedia",
            "endpoints": {
                "summary": "/api/insights/summary",
                "spatial": "/api/insights/spatial",
            },
        }), 200


# ---------------------------------------------------------------------------
# ENDPOINT 2: GET /api/insights/summary — Ringkasan Statistik
# ---------------------------------------------------------------------------

@insights_bp.route("/api/insights/summary")
def get_summary():
    """
    Kembalikan ringkasan statistik keseluruhan analisis deforestasi.

    Menghitung luas target prediksi model (2024 & 2025) serta
    gain/loss secara real-time dari data GeoJSON, lalu menyusun
    ringkasan lengkap termasuk net change dan kesimpulan utama.

    Returns:
        JSON: Ringkasan statistik:
              {
                  "target_2024_ha"     : float,
                  "target_2025_ha"     : float,
                  "gain_ha"            : float,
                  "loss_ha"            : float,
                  "net_change_ha"      : float,
                  "net_change_percent" : float,
                  "status"             : str,
                  "key_findings"       : list[str],
                  "conclusion"         : str,
                  "timestamp"          : str
              }

    HTTP Status:
        200 → Ringkasan berhasil dihitung.
        500 → Gagal memuat data GeoJSON atau menghitung statistik.

    Example:
        GET /api/insights/summary
        → {"target_2024_ha": ..., "gain_ha": ..., "net_change_ha": ..., ...}
    """
    try:
        # Load semua GeoDataFrame yang dibutuhkan
        gain_gdf       = GeoService.load_geojson("gain")
        loss_gdf       = GeoService.load_geojson("loss")
        target2024_gdf = GeoService.load_geojson("target-2024")
        target2025_gdf = GeoService.load_geojson("target-2025")

    except (FileNotFoundError, ValueError) as exc:
        logger.error("Gagal load GeoJSON untuk insights: %s", exc)
        return _error_response(
            f"Gagal memuat data GeoJSON: {str(exc)}", 500
        )
    except Exception as exc:
        logger.exception("Error saat load GeoJSON: %s", exc)
        return _error_response(
            f"Gagal memuat data: {str(exc)}", 500
        )

    try:
        # Gunakan luasan aktual dari hasil running Google Earth Engine (pixel-based)
        target_2024_ha = 191466.25
        target_2025_ha = 207633.11

        # Hitung statistik gain vs loss
        stats = StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)

        gain_ha        = stats["gain_ha"]
        loss_ha        = stats["loss_ha"]
        net_change_ha  = stats["net_change_ha"]
        status         = stats["status"]

        # Perubahan target year-over-year
        target_change_ha      = float(round(target_2025_ha - target_2024_ha, 2))
        target_change_percent = (
            float(round((target_change_ha / target_2024_ha) * 100, 2))
            if target_2024_ha > 0 else 0.0
        )

    except Exception as exc:
        logger.exception("Gagal menghitung statistik insights: %s", exc)
        return _error_response(
            f"Gagal menghitung statistik: {str(exc)}", 500
        )

    # Susun key findings berdasarkan data aktual
    key_findings = [
        f"Total area gain (pertambahan hutan): {gain_ha:,.2f} ha",
        f"Total area loss (kehilangan hutan): {loss_ha:,.2f} ha",
        f"Net change: {net_change_ha:+,.2f} ha ({status.replace('_', ' ')})",
        f"Luas target prediksi 2024: {target_2024_ha:,.2f} ha",
        f"Luas target prediksi 2025: {target_2025_ha:,.2f} ha",
        f"Perubahan target 2024→2025: {target_change_ha:+,.2f} ha ({target_change_percent:+.2f}%)",
        (
            "Persentase gain dan loss hampir seimbang, "
            f"gain {stats['percentage_gain']:.1f}% vs loss {stats['percentage_loss']:.1f}%"
        ),
    ]

    # Kesimpulan naratif
    if status == "net_gain":
        conclusion = (
            f"Secara keseluruhan, wilayah Kerinci mengalami net gain "
            f"(pertambahan bersih) sebesar {net_change_ha:+,.2f} ha. "
            "Ini menunjukkan bahwa upaya reforestasi dan pemulihan lahan "
            "sedikit lebih besar dari deforestasi yang terjadi pada "
            "periode 2024–2025."
        )
    else:
        conclusion = (
            f"Secara keseluruhan, wilayah Kerinci mengalami net loss "
            f"(kehilangan bersih) sebesar {abs(net_change_ha):,.2f} ha. "
            "Ini menunjukkan bahwa tekanan deforestasi masih lebih besar "
            "dari upaya pemulihan hutan pada periode 2024–2025."
        )

    response = {
        "target_2024_ha":          target_2024_ha,
        "target_2025_ha":          target_2025_ha,
        "target_change_ha":        target_change_ha,
        "target_change_percent":   target_change_percent,
        "gain_ha":                 gain_ha,
        "loss_ha":                 loss_ha,
        "net_change_ha":           net_change_ha,
        "net_change_percent":      stats["net_change_percent"],
        "percentage_gain":         stats["percentage_gain"],
        "percentage_loss":         stats["percentage_loss"],
        "status":                  status,
        "gain_feature_count":      stats["gain_feature_count"],
        "loss_feature_count":      stats["loss_feature_count"],
        "key_findings":            key_findings,
        "conclusion":              conclusion,
        "analysis_period":         "2024 – 2025",
        "timestamp":               datetime.now(timezone.utc).isoformat(),
    }

    logger.info(
        "Insights summary: gain=%.2f ha, loss=%.2f ha, net=%+.2f ha (%s)",
        gain_ha, loss_ha, net_change_ha, status,
    )
    return jsonify(response), 200


# ---------------------------------------------------------------------------
# ENDPOINT 3: GET /api/insights/spatial — Distribusi Spasial
# ---------------------------------------------------------------------------

@insights_bp.route("/api/insights/spatial")
def get_spatial():
    """
    Kembalikan analisis distribusi spasial perubahan tutupan hutan.

    Menyajikan informasi di mana gain dan loss terkonsentrasi
    secara geografis di wilayah Kerinci, beserta kemungkinan
    penyebab di setiap lokasi.

    Returns:
        JSON: Distribusi spasial:
              {
                  "gain_distribution": {
                      "primary_location"  : str,
                      "percentage"        : float,
                      "possible_causes"   : list[str],
                      "description"       : str
                  },
                  "loss_distribution": {
                      "primary_location"  : str,
                      "percentage"        : float,
                      "possible_causes"   : list[str],
                      "description"       : str
                  },
                  "analysis_period" : str,
                  "data_source"     : str,
                  "notes"           : str,
                  "timestamp"       : str
              }

    HTTP Status:
        200 → Data spasial berhasil dikembalikan (data statis).

    Example:
        GET /api/insights/spatial
        → {"gain_distribution": {"primary_location": "Timur", ...}, ...}
    """
    try:
        spatial = StatsService.get_spatial_summary()
        spatial["timestamp"] = datetime.now(timezone.utc).isoformat()

        logger.info("Spatial distribution endpoint dipanggil.")
        return jsonify(spatial), 200

    except Exception as exc:
        logger.exception("Gagal mengambil data spasial: %s", exc)
        return _error_response(
            f"Gagal mengambil distribusi spasial: {str(exc)}", 500
        )


# ---------------------------------------------------------------------------
# ENDPOINT 4: GET /api/insights/full — Semua Data Tab 4 (bonus)
# ---------------------------------------------------------------------------

@insights_bp.route("/api/insights/full")
def get_full_insights():
    """
    Kembalikan seluruh data insight dalam satu response.

    Menggabungkan summary + spatial agar frontend cukup satu request
    untuk mengisi seluruh konten Tab 4.

    Returns:
        JSON: Gabungan semua data insight:
              {
                  "summary" : {...},
                  "spatial" : {...},
                  "timestamp": str
              }

    HTTP Status:
        200 → Data berhasil dikembalikan.
        500 → Gagal menghitung statistik.

    Example:
        GET /api/insights/full
        → { "summary": {...}, "spatial": {...} }
    """
    # Ambil summary
    try:
        gain_gdf       = GeoService.load_geojson("gain")
        loss_gdf       = GeoService.load_geojson("loss")
        target2024_gdf = GeoService.load_geojson("target-2024")
        target2025_gdf = GeoService.load_geojson("target-2025")

        target_2024_ha = 191466.25
        target_2025_ha = 207633.11
        stats          = StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)

    except Exception as exc:
        logger.exception("Gagal load data untuk full insights: %s", exc)
        return _error_response(
            f"Gagal memuat data: {str(exc)}", 500
        )

    response = {
        "summary": {
            "target_2024_ha":  target_2024_ha,
            "target_2025_ha":  target_2025_ha,
            "gain_ha":         stats["gain_ha"],
            "loss_ha":         stats["loss_ha"],
            "net_change_ha":   stats["net_change_ha"],
            "percentage_gain": stats["percentage_gain"],
            "percentage_loss": stats["percentage_loss"],
            "status":          stats["status"],
        },
        "spatial":   StatsService.get_spatial_summary(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    logger.info("Full insights endpoint dipanggil.")
    return jsonify(response), 200
