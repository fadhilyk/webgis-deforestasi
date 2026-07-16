"""
routes/model.py - Tab 3: Evaluasi Model
==========================================
WebGIS Monitoring Deforestasi Kerinci

Blueprint untuk endpoint Tab 3 (Evaluasi Model):
- GET /model                         → Render halaman evaluasi model
- GET /api/model/metrics             → Accuracy, Precision, Recall, F1
- GET /api/model/confusion-matrix    → TP, TN, FP, FN + interpretasi
- GET /api/model/interpretation      → Teks interpretasi & limitasi model

Endpoint ini menyajikan hasil evaluasi model Random Forest
yang digunakan untuk klasifikasi tutupan hutan Kerinci.

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template

from services.model_service import ModelService

# ---------------------------------------------------------------------------
# LOGGER & BLUEPRINT
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# Blueprint Tab 3: Evaluasi Model
model_bp = Blueprint("model", __name__)


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
# ENDPOINT 1: GET /model — Halaman HTML Tab 3
# ---------------------------------------------------------------------------

@model_bp.route("/model")
def model_page():
    """
    Render halaman Evaluasi Model (Tab 3).

    Menampilkan metrik evaluasi model Random Forest, confusion matrix,
    dan interpretasi hasil klasifikasi tutupan hutan.

    Returns:
        HTML: Render template 'model.html'.
        JSON: Fallback 200 jika template belum tersedia.

    HTTP Status:
        200 → Halaman berhasil dirender.

    Example:
        GET /model
        → Menampilkan halaman evaluasi model RF
    """
    try:
        logger.info("Rendering model evaluation page.")
        return render_template("model.html", page_title="Evaluasi Model")
    except Exception as exc:
        logger.warning("Template 'model.html' belum tersedia: %s", exc)
        return jsonify({
            "message":   "Evaluasi Model — template belum tersedia",
            "endpoints": {
                "metrics":          "/api/model/metrics",
                "confusion_matrix": "/api/model/confusion-matrix",
                "interpretation":   "/api/model/interpretation",
            },
        }), 200


# ---------------------------------------------------------------------------
# ENDPOINT 2: GET /api/model/metrics — Metrik Evaluasi Model
# ---------------------------------------------------------------------------

@model_bp.route("/api/model/metrics")
def get_metrics():
    """
    Kembalikan metrik evaluasi model Random Forest.

    Menyajikan accuracy, precision, recall, dan F1 score dari hasil
    evaluasi model pada data testing (90 sampel).

    Returns:
        JSON: Metrik evaluasi lengkap:
              {
                  "accuracy"         : 75.6,
                  "precision"        : 81.1,
                  "recall"           : 66.7,
                  "f1_score"         : 73.3,
                  "training_samples" : 210,
                  "testing_samples"  : 90,
                  "total_samples"    : 300,
                  "train_test_split" : "70% : 30%",
                  "algorithm"        : "Random Forest Classifier",
                  "features_used"    : [...],
                  "target_classes"   : [...],
                  "formulas"         : {...},
                  "timestamp"        : str
              }

    HTTP Status:
        200 → Metrik berhasil dikembalikan.
        500 → Gagal mengambil metrik.

    Example:
        GET /api/model/metrics
        → {"accuracy": 75.6, "precision": 81.1, ...}
    """
    try:
        metrics = ModelService.get_metrics()
        metrics["timestamp"] = datetime.now(timezone.utc).isoformat()

        logger.info(
            "Metrics endpoint: accuracy=%.1f%%, F1=%.1f%%",
            metrics["accuracy"], metrics["f1_score"],
        )
        return jsonify(metrics), 200

    except Exception as exc:
        logger.exception("Gagal mengambil metrik model: %s", exc)
        return _error_response(f"Gagal mengambil metrik model: {str(exc)}", 500)


# ---------------------------------------------------------------------------
# ENDPOINT 3: GET /api/model/confusion-matrix — Confusion Matrix
# ---------------------------------------------------------------------------

@model_bp.route("/api/model/confusion-matrix")
def get_confusion_matrix():
    """
    Kembalikan confusion matrix model beserta interpretasi tiap sel.

    Menyajikan nilai TP, TN, FP, FN dari evaluasi klasifikasi biner
    (hutan vs non-hutan) pada data testing, termasuk format 2D
    untuk visualisasi heatmap di frontend (Plotly.js).

    Returns:
        JSON: Confusion matrix lengkap:
              {
                  "TP": 30,
                  "TN": 38,
                  "FP": 7,
                  "FN": 15,
                  "total_samples"      : 90,
                  "correct_predictions" : 68,
                  "wrong_predictions"   : 22,
                  "matrix_2d"          : [[30,15],[7,38]],
                  "axis_labels"        : {...},
                  "interpretation"     : {
                      "TP": "...",
                      "TN": "...",
                      "FP": "...",
                      "FN": "..."
                  },
                  "timestamp": str
              }

    HTTP Status:
        200 → Confusion matrix berhasil dikembalikan.
        500 → Gagal mengambil data confusion matrix.

    Example:
        GET /api/model/confusion-matrix
        → {"TP": 30, "TN": 38, "FP": 7, "FN": 15, ...}
    """
    try:
        cm = ModelService.get_confusion_matrix()
        cm["timestamp"] = datetime.now(timezone.utc).isoformat()

        logger.info(
            "Confusion matrix endpoint: TP=%d, TN=%d, FP=%d, FN=%d",
            cm["TP"], cm["TN"], cm["FP"], cm["FN"],
        )
        return jsonify(cm), 200

    except Exception as exc:
        logger.exception("Gagal mengambil confusion matrix: %s", exc)
        return _error_response(
            f"Gagal mengambil confusion matrix: {str(exc)}", 500
        )


# ---------------------------------------------------------------------------
# ENDPOINT 4: GET /api/model/interpretation — Interpretasi Hasil
# ---------------------------------------------------------------------------

@model_bp.route("/api/model/interpretation")
def get_interpretation():
    """
    Kembalikan interpretasi naratif hasil evaluasi model dan limitasinya.

    Memberikan konteks untuk memahami angka-angka metrik,
    implikasi dari false positive/negative, serta saran perbaikan model.

    Returns:
        JSON: Interpretasi lengkap:
              {
                  "overall_assessment"  : str,
                  "accuracy_context"    : str,
                  "fp_implication"      : str,
                  "fn_implication"      : str,
                  "precision_vs_recall" : str,
                  "limitations"         : list[str],
                  "recommendations"     : list[str],
                  "data_source"         : str,
                  "timestamp"           : str
              }

    HTTP Status:
        200 → Interpretasi berhasil dikembalikan.
        500 → Gagal mengambil interpretasi.

    Example:
        GET /api/model/interpretation
        → {"overall_assessment": "Model RF menunjukkan akurasi 75.6% ...", ...}
    """
    try:
        interpretation = ModelService.get_interpretation()
        interpretation["timestamp"] = datetime.now(timezone.utc).isoformat()

        logger.info("Interpretation endpoint dipanggil.")
        return jsonify(interpretation), 200

    except Exception as exc:
        logger.exception("Gagal mengambil interpretasi model: %s", exc)
        return _error_response(
            f"Gagal mengambil interpretasi model: {str(exc)}", 500
        )


# ---------------------------------------------------------------------------
# ENDPOINT 5: GET /api/model/summary — Semua Data Model (bonus)
# ---------------------------------------------------------------------------

@model_bp.route("/api/model/summary")
def get_model_summary():
    """
    Kembalikan ringkasan lengkap evaluasi model dalam satu response.

    Menggabungkan metrics, confusion matrix, dan interpretation
    agar frontend bisa fetch sekali untuk semua data Tab 3.

    Returns:
        JSON: Gabungan semua data model:
              {
                  "metrics"         : {...},
                  "confusion_matrix": {...},
                  "interpretation"  : {...},
                  "model_files"     : {...},
                  "timestamp"       : str
              }

    HTTP Status:
        200 → Summary berhasil dikembalikan.
        500 → Gagal mengambil data.

    Example:
        GET /api/model/summary
        → { "metrics": {...}, "confusion_matrix": {...}, ... }
    """
    try:
        response = {
            "metrics":          ModelService.get_metrics(),
            "confusion_matrix": ModelService.get_confusion_matrix(),
            "interpretation":   ModelService.get_interpretation(),
            "model_files":      ModelService.get_available_models(),
            "timestamp":        datetime.now(timezone.utc).isoformat(),
        }

        logger.info("Model summary endpoint dipanggil.")
        return jsonify(response), 200

    except Exception as exc:
        logger.exception("Gagal mengambil model summary: %s", exc)
        return _error_response(
            f"Gagal mengambil model summary: {str(exc)}", 500
        )
