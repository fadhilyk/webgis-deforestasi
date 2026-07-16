"""
Route blueprint for Tab 2 — Data & Proses.

Endpoints:
  GET /api/data/statistics  — Gain/loss area & percentage stats
  GET /api/data/metadata    — Data source information
  GET /data                 — Data page template
"""

from flask import Blueprint, jsonify, render_template

from services.geo_service import GeoService
from services.stats_service import StatsService

__all__ = ['data_bp']

data_bp = Blueprint('data', __name__)


@data_bp.route('/api/data/statistics')
def get_statistics():
    """Return gain/loss area statistics and percentages.

    Loads gain and loss GeoJSON layers, computes total area,
    net change, and percentage shares.

    Returns:
        JSON with gain_ha, loss_ha, total_area, percentage_gain,
        percentage_loss, net_change_ha, net_change_percent (200),
        or error message (500).
    """
    try:
        gain_gdf = GeoService.load_geojson('gain')
        loss_gdf = GeoService.load_geojson('loss')

        stats = StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)
        total_area = round(stats['gain_area_ha'] + stats['loss_area_ha'], 2)

        return jsonify({
            'gain_ha': stats['gain_area_ha'],
            'loss_ha': stats['loss_area_ha'],
            'total_area': total_area,
            'percentage_gain': stats['percentage_gain'],
            'percentage_loss': stats['percentage_loss'],
            'net_change_ha': stats['net_change_ha'],
            'net_change_percent': stats['net_change_percent'],
        })
    except Exception as e:
        return jsonify({'error': 'Failed to compute statistics',
                        'message': str(e)}), 500


@data_bp.route('/api/data/metadata')
def get_metadata():
    """Return metadata about data sources and preprocessing.

    Describes satellite imagery, time periods, cloud masking,
    composite method, spectral bands, and vegetation indexes used.

    Returns:
        JSON with satellite, period_2024, period_2025, cloud_masking,
        composite, bands, indexes.
    """
    return jsonify({
        'satellite': 'Sentinel-2 COPERNICUS/S2_SR_HARMONIZED',
        'period_2024': '01 Jan - 31 Des 2024',
        'period_2025': '01 Jan - 31 Des 2025',
        'cloud_masking': 'S2 Cloud Probability + SCL',
        'composite': 'Median Composite',
        'bands': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12'],
        'indexes': ['NDVI', 'NDMI', 'NDBI'],
    })


@data_bp.route('/data')
def data_page():
    """Render the Data & Proses page."""
    return render_template('data_proses.html')
