"""
app.py - Flask Main Application
================================
WebGIS Monitoring Deforestasi Kerinci
Entry point utama untuk Flask application.

Menginisialisasi Flask app, mendaftarkan blueprints (routes),
mengkonfigurasi error handlers, dan menyiapkan server.

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import os
import logging
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from config import (
    TEMPLATE_FOLDER,
    STATIC_FOLDER,
    DATA_FOLDER,
    MODELS_FOLDER,
    GEOJSON_FILES,
    config_by_name,
)

# ---------------------------------------------------------------------------
# LOGGING SETUP
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# APP FACTORY
# ---------------------------------------------------------------------------

def create_app(env: str = "development") -> Flask:
    """
    Factory function untuk membuat dan mengkonfigurasi Flask application.

    Args:
        env (str): Nama environment ('development' atau 'production').
                   Default: 'development'.

    Returns:
        Flask: Instance Flask yang sudah dikonfigurasi.

    Example:
        >>> app = create_app('development')
        >>> app.run()
    """
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_FOLDER),
        static_folder=str(STATIC_FOLDER),
    )

    # Load konfigurasi berdasarkan environment
    cfg = config_by_name.get(env, config_by_name["default"])
    app.config.from_object(cfg)

    # Aktifkan CORS agar frontend dapat mengakses API
    CORS(app)

    # Register blueprints (route modules)
    _register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    logger.info("Flask app created in '%s' mode.", env)
    return app


def _register_blueprints(app: Flask) -> None:
    """
    Mendaftarkan semua blueprint (route modules) ke Flask application.

    Setiap blueprint merepresentasikan satu tab pada WebGIS dashboard:
    - peta_bp    → Tab 1: Peta Hasil
    - data_bp    → Tab 2: Data & Proses
    - model_bp   → Tab 3: Evaluasi Model
    - insights_bp→ Tab 4: Insight Hasil

    Args:
        app (Flask): Flask application instance.
    """
    try:
        from routes.peta import peta_bp
        app.register_blueprint(peta_bp)
        logger.info("Blueprint 'peta' registered.")
    except Exception as exc:
        logger.error("Blueprint 'peta' GAGAL didaftarkan: %s", exc, exc_info=True)

    try:
        from routes.data_proses import data_bp
        app.register_blueprint(data_bp)
        logger.info("Blueprint 'data_proses' registered.")
    except Exception as exc:
        logger.error("Blueprint 'data_proses' GAGAL didaftarkan: %s", exc, exc_info=True)

    try:
        from routes.model import model_bp
        app.register_blueprint(model_bp)
        logger.info("Blueprint 'model' registered.")
    except Exception as exc:
        logger.error("Blueprint 'model' GAGAL didaftarkan: %s", exc, exc_info=True)

    try:
        from routes.insights import insights_bp
        app.register_blueprint(insights_bp)
        logger.info("Blueprint 'insights' registered.")
    except Exception as exc:
        logger.error("Blueprint 'insights' GAGAL didaftarkan: %s", exc, exc_info=True)


def _register_error_handlers(app: Flask) -> None:
    """
    Mendaftarkan custom error handlers untuk HTTP error codes.

    Args:
        app (Flask): Flask application instance.
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request."""
        logger.warning("400 Bad Request: %s", error)
        return jsonify({
            "error": "Bad Request - Parameter tidak valid",
            "status": 400,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found."""
        logger.warning("404 Not Found: %s", error)
        return jsonify({
            "error": "Endpoint atau resource tidak ditemukan",
            "status": 404,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        logger.error("500 Internal Server Error: %s", error)
        return jsonify({
            "error": "Terjadi kesalahan pada server",
            "status": 500,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), 500


# ---------------------------------------------------------------------------
# CREATE APP INSTANCE
# ---------------------------------------------------------------------------

# Baca environment dari variabel lingkungan, default ke 'development'
_env = os.getenv("FLASK_ENV", "development")
app = create_app(env=_env)


# ---------------------------------------------------------------------------
# ROOT & UTILITY ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """
    Root endpoint — halaman beranda WebGIS.

    Returns:
        HTML: Render halaman index, atau JSON welcome message
              jika template belum tersedia.
    """
    try:
        return render_template("index.html")
    except Exception as exc:
        logger.error("Template render GAGAL: %s", exc, exc_info=True)
        # Fallback jika templates belum dibuat
        return jsonify({
            "message": "Selamat datang di WebGIS Monitoring Deforestasi Kerinci",
            "version": "1.0",
            "status": "running",
            "docs": "/api/health",
            "tabs": {
                "peta":        "/map",
                "data_proses": "/data",
                "model":       "/model",
                "insights":    "/insights",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })


@app.route("/api/health")
def health_check():
    """
    Health check endpoint — digunakan Render.com untuk memverifikasi
    bahwa aplikasi berjalan dengan baik.

    Returns:
        JSON: Status aplikasi dan ketersediaan file GeoJSON.
    """
    data_status = {}
    for layer_name, filename in GEOJSON_FILES.items():
        filepath = DATA_FOLDER / filename
        data_status[layer_name] = filepath.exists()

    all_data_ok = all(data_status.values())

    return jsonify({
        "status": "healthy" if all_data_ok else "degraded",
        "app": "WebGIS Monitoring Deforestasi Kerinci",
        "version": "1.0",
        "environment": _env,
        "data_files": data_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200 if all_data_ok else 206


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Baca port dari environment (Render.com menyediakan variabel PORT)
    port = int(os.getenv("PORT", 5000))

    logger.info("Starting WebGIS Deforestasi server on port %d ...", port)

    app.run(
        host="0.0.0.0",   # Accessible dari semua network interfaces
        port=port,
        debug=app.config.get("DEBUG", True),
    )
