"""
Route blueprint for Tab 4 — Insight Hasil.

Endpoints:
  GET /api/insights/summary  — Summary statistics from presentation data
  GET /api/insights/spatial  — Spatial distribution analysis
  GET /insights              — Insights page template
"""

from flask import Blueprint, jsonify, render_template

from services.stats_service import StatsService

__all__ = ['insights_bp']

insights_bp = Blueprint('insights', __name__)


@insights_bp.route('/api/insights/summary')
def get_summary():
    """Return summary statistics from deforestation analysis.

    Combines target areas and observed gain/loss from presentation data.

    Returns:
        JSON with target_2024_ha, target_2025_ha, gain_ha, loss_ha,
        net_change_ha, net_change_percent (200), or error (500).
    """
    try:
        gain_ha = 540
        loss_ha = 810
        net_change_ha = round(gain_ha - loss_ha, 2)
        total = gain_ha + loss_ha
        net_change_percent = (
            round(((gain_ha - loss_ha) / total) * 100, 2) if total else 0.0
        )

        return jsonify({
            'target_2024_ha': 4250,
            'target_2025_ha': 3980,
            'gain_ha': gain_ha,
            'loss_ha': loss_ha,
            'net_change_ha': net_change_ha,
            'net_change_percent': net_change_percent,
        })
    except Exception as e:
        return jsonify({'error': 'Failed to compute summary',
                        'message': str(e)}), 500


@insights_bp.route('/api/insights/spatial')
def get_spatial():
    """Return spatial distribution of deforestation.

    Delegates to StatsService for region-level breakdown.

    Returns:
        JSON with gain_distribution and loss_distribution arrays,
        each containing location, percentage, possible_causes.
    """
    try:
        summary = StatsService.get_spatial_summary()
        return jsonify({
            'gain_distribution': summary['regions'],
            'loss_distribution': summary['regions'],
        })
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve spatial data',
                        'message': str(e)}), 500


@insights_bp.route('/insights')
def insights_page():
    """Render the Insight Hasil page."""
    return render_template('insights.html')
