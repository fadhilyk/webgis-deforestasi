"""
Route blueprint for Tab 3 — Evaluasi Model.

Endpoints:
  GET /api/model/metrics          — Model performance metrics
  GET /api/model/confusion-matrix — Confusion matrix values
  GET /model                      — Model evaluation page
"""

from flask import Blueprint, jsonify, render_template

from services.model_service import ModelService

__all__ = ['model_bp']

model_bp = Blueprint('model', __name__)


@model_bp.route('/api/model/metrics')
def get_metrics():
    """Return model performance metrics.

    Returns:
        JSON with accuracy, precision, recall, f1_score,
        training_samples, testing_samples (200),
        or error message (500).
    """
    try:
        metrics = ModelService.get_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve model metrics',
                        'message': str(e)}), 500


@model_bp.route('/api/model/confusion-matrix')
def get_confusion_matrix():
    """Return confusion matrix values.

    Returns:
        JSON with TP, TN, FP, FN counts and interpretation (200),
        or error message (500).
    """
    try:
        matrix = ModelService.get_confusion_matrix()
        return jsonify(matrix)
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve confusion matrix',
                        'message': str(e)}), 500


@model_bp.route('/model')
def model_page():
    """Render the Evaluasi Model page."""
    return render_template('model.html')
