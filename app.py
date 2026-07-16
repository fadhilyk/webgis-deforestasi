"""
Main Flask application for WebGIS Monitoring Deforestasi Kerinci.

Initialises Flask app, registers blueprints, configures
template/static paths, and attaches error handlers.
"""

from flask import Flask, jsonify

from config import TEMPLATE_FOLDER, STATIC_FOLDER
from routes.peta import peta_bp
from routes.data_proses import data_bp
from routes.model import model_bp
from routes.insights import insights_bp


def create_app():
    """Application factory: build and return a configured Flask instance."""
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_FOLDER),
        static_folder=str(STATIC_FOLDER),
    )

    # ── Blueprint registration ──────────────────────────────
    app.register_blueprint(peta_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(model_bp)
    app.register_blueprint(insights_bp)

    # ── Root endpoint ───────────────────────────────────────
    @app.route('/')
    def index():
        """Landing page and health check."""
        return jsonify({
            'message': 'Welcome to WebGIS Monitoring Deforestasi Kerinci',
        })

    # ── Error handlers ──────────────────────────────────────
    @app.errorhandler(404)
    def not_found(error):
        """Return JSON for unmatched routes."""
        return jsonify({'error': 'Not found', 'message': str(error)}), 404

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
