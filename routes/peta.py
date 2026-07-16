"""
Route blueprint for Tab 1 — Peta Hasil (Map View).

Endpoints:
  GET /api/layers/<layer_name>  — GeoJSON layer data
  GET /map                      — Map page template
"""

from flask import Blueprint, jsonify, render_template

from config import MAP_CENTER, MAP_ZOOM
from services.geo_service import GeoService

__all__ = ['peta_bp']

peta_bp = Blueprint('peta', __name__)


@peta_bp.route('/api/layers/<layer_name>')
def get_layer(layer_name: str):
    """Return a GeoJSON layer as JSON.

    Args:
        layer_name: One of 'batas-wilayah', 'gain', 'loss',
                    'target-2024', 'target-2025'.

    Returns:
        JSON response with GeoJSON FeatureCollection (200),
        or error message (404/500).
    """
    try:
        gdf = GeoService.load_geojson(layer_name)
        geojson = GeoService.geojson_to_json(gdf)
        return jsonify(geojson)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error',
                        'message': str(e)}), 500


@peta_bp.route('/map')
def map_page():
    """Render the Peta Hasil (map) page."""
    return render_template('peta.html',
                           center=MAP_CENTER,
                           zoom_level=MAP_ZOOM)
