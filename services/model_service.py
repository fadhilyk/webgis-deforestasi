"""
services/model_service.py - Model Service Layer
================================================
WebGIS Monitoring Deforestasi Kerinci

Menyediakan data evaluasi model Random Forest yang digunakan
untuk klasifikasi perubahan tutupan hutan Kerinci berbasis
citra Sentinel-2.

Data bersumber dari hasil training & evaluasi model (hardcoded dari
presentasi proyek), karena model .pkl mungkin tidak selalu tersedia
di server production (Render free tier - disk ephemeral).

Fungsi utama:
    - get_confusion_matrix()  : Nilai TP, TN, FP, FN + interpretasi
    - get_metrics()           : Accuracy, Precision, Recall, F1
    - get_interpretation()    : Teks interpretasi & limitasi model

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import logging
from pathlib import Path

from config import MODELS_FOLDER, MODEL_FILES

# ---------------------------------------------------------------------------
# LOGGER
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# MODEL SERVICE CLASS
# ---------------------------------------------------------------------------

class ModelService:
    """
    Service class untuk data evaluasi model Random Forest Kerinci.

    Menyimpan dan menyajikan hasil evaluasi model klasifikasi
    tutupan hutan yang telah dilatih menggunakan data Sentinel-2.

    Model dilatih dengan:
    - Algoritma  : Random Forest Classifier
    - Data train : 210 sampel (70% dari total)
    - Data test  : 90 sampel (30% dari total)
    - Fitur      : Band B2, B3, B4, B8, B11, B12 + NDVI, NDMI, NDBI
    - Target     : Biner (hutan / non-hutan)

    Note:
        Semua nilai metrik di-hardcode dari hasil presentasi proyek.
        Ini memastikan endpoint tetap berjalan meski file .pkl
        tidak tersedia di environment production.

    Example:
        >>> service = ModelService()
        >>> cm = service.get_confusion_matrix()
        >>> print(cm['TP'])  # → 30
        >>> metrics = service.get_metrics()
        >>> print(metrics['accuracy'])  # → 75.6
    """

    # ---------------------------------------------------------------------------
    # CONFUSION MATRIX CONSTANTS
    # ---------------------------------------------------------------------------

    # Nilai confusion matrix dari hasil evaluasi model (presentasi)
    _CM_TP = 30   # True Positive  : Model prediksi hutan → aktual hutan ✓
    _CM_TN = 38   # True Negative  : Model prediksi non-hutan → aktual non-hutan ✓
    _CM_FP = 7    # False Positive : Model prediksi hutan → aktual non-hutan ✗
    _CM_FN = 15   # False Negative : Model prediksi non-hutan → aktual hutan ✗

    # ---------------------------------------------------------------------------
    # METRICS CONSTANTS
    # ---------------------------------------------------------------------------

    # Metrik evaluasi model dari hasil presentasi proyek
    _ACCURACY          = 75.6   # Persentase prediksi yang benar
    _PRECISION         = 81.1   # Ketepatan prediksi positif
    _RECALL            = 66.7   # Sensitivitas (kemampuan deteksi kelas positif)
    _F1_SCORE          = 73.3   # Harmonic mean of Precision & Recall
    _TRAINING_SAMPLES  = 210    # Jumlah sampel data training (70%)
    _TESTING_SAMPLES   = 90     # Jumlah sampel data testing  (30%)

    # ---------------------------------------------------------------------------
    # GET CONFUSION MATRIX
    # ---------------------------------------------------------------------------

    @classmethod
    def get_confusion_matrix(cls) -> dict:
        """
        Kembalikan nilai confusion matrix model beserta interpretasi tiap sel.

        Confusion matrix merepresentasikan performa klasifikasi biner
        (hutan vs non-hutan) pada data testing (90 sampel).

        Struktur confusion matrix:
            ┌──────────────────────┬──────────────────────┐
            │ TP = 30 (True +)     │ FN = 15 (False -)    │
            ├──────────────────────┼──────────────────────┤
            │ FP = 7  (False +)    │ TN = 38 (True -)     │
            └──────────────────────┴──────────────────────┘

        Returns:
            dict: Confusion matrix lengkap dengan struktur:
                {
                    "TP": int,                  # True Positive
                    "TN": int,                  # True Negative
                    "FP": int,                  # False Positive
                    "FN": int,                  # False Negative
                    "total_samples": int,        # TP+TN+FP+FN
                    "correct_predictions": int,  # TP+TN
                    "wrong_predictions": int,    # FP+FN
                    "interpretation": dict,      # Teks interpretasi tiap sel
                    "matrix_2d": list,           # Format [[TP,FN],[FP,TN]]
                                                 # untuk Plotly heatmap
                }

        Example:
            >>> cm = ModelService.get_confusion_matrix()
            >>> print(f"TP={cm['TP']}, FN={cm['FN']}")
            TP=30, FN=15
            >>> print(cm['interpretation']['FP'])
            'Model salah memprediksi area non-hutan sebagai hutan ...'
        """
        total_samples       = cls._CM_TP + cls._CM_TN + cls._CM_FP + cls._CM_FN
        correct_predictions = cls._CM_TP + cls._CM_TN
        wrong_predictions   = cls._CM_FP + cls._CM_FN

        result = {
            "TP": cls._CM_TP,
            "TN": cls._CM_TN,
            "FP": cls._CM_FP,
            "FN": cls._CM_FN,
            "total_samples":       total_samples,
            "correct_predictions": correct_predictions,
            "wrong_predictions":   wrong_predictions,

            # Format 2D untuk Plotly heatmap [[baris1], [baris2]]
            # Urutan: [[TP, FN], [FP, TN]] — Predicted vs Actual
            "matrix_2d": [
                [cls._CM_TP, cls._CM_FN],
                [cls._CM_FP, cls._CM_TN],
            ],

            # Label sumbu untuk heatmap
            "axis_labels": {
                "x": ["Aktual Positif (Hutan)", "Aktual Negatif (Non-Hutan)"],
                "y": ["Prediksi Positif (Hutan)", "Prediksi Negatif (Non-Hutan)"],
            },

            # Interpretasi tiap sel confusion matrix
            "interpretation": {
                "TP": (
                    f"True Positive ({cls._CM_TP} sampel): "
                    "Model berhasil mengidentifikasi area hutan dengan benar. "
                    "Prediksi 'hutan' sesuai dengan kondisi aktual 'hutan'."
                ),
                "TN": (
                    f"True Negative ({cls._CM_TN} sampel): "
                    "Model berhasil mengidentifikasi area non-hutan dengan benar. "
                    "Prediksi 'non-hutan' sesuai dengan kondisi aktual 'non-hutan'."
                ),
                "FP": (
                    f"False Positive ({cls._CM_FP} sampel): "
                    "Model salah memprediksi area non-hutan sebagai hutan "
                    "(overprediction). Bisa disebabkan oleh area dengan NDVI tinggi "
                    "seperti perkebunan atau semak belukar yang mirip hutan."
                ),
                "FN": (
                    f"False Negative ({cls._CM_FN} sampel): "
                    "Model gagal mendeteksi area hutan yang sebenarnya ada "
                    "(underprediction / missed detection). Bisa terjadi pada hutan "
                    "yang tertutupi awan atau memiliki reflektansi rendah."
                ),
            },
        }

        logger.debug("Confusion matrix berhasil disiapkan: %d total sampel.", total_samples)
        return result

    # ---------------------------------------------------------------------------
    # GET METRICS
    # ---------------------------------------------------------------------------

    @classmethod
    def get_metrics(cls) -> dict:
        """
        Kembalikan metrik evaluasi model Random Forest.

        Metrik dihitung dari confusion matrix pada data testing (90 sampel)
        menggunakan scikit-learn's classification_report.

        Definisi metrik:
            Accuracy  = (TP + TN) / (TP + TN + FP + FN)
            Precision = TP / (TP + FP)   [ketepatan prediksi positif]
            Recall    = TP / (TP + FN)   [kemampuan mendeteksi kelas positif]
            F1 Score  = 2 × (Precision × Recall) / (Precision + Recall)

        Returns:
            dict: Metrik evaluasi lengkap dengan struktur:
                {
                    "accuracy"          : float,  # % akurasi keseluruhan
                    "precision"         : float,  # % ketepatan prediksi hutan
                    "recall"            : float,  # % sensitivitas deteksi hutan
                    "f1_score"          : float,  # F1 harmonic mean
                    "training_samples"  : int,    # Jumlah data training
                    "testing_samples"   : int,    # Jumlah data testing
                    "total_samples"     : int,    # Total data
                    "train_test_split"  : str,    # Rasio train/test
                    "algorithm"         : str,    # Nama algoritma
                    "features_used"     : list,   # Fitur input model
                    "target_classes"    : list,   # Kelas output
                    "formulas"          : dict,   # Rumus tiap metrik
                }

        Example:
            >>> metrics = ModelService.get_metrics()
            >>> print(f"Accuracy: {metrics['accuracy']}%")
            Accuracy: 75.6%
            >>> print(f"F1 Score: {metrics['f1_score']}%")
            F1 Score: 73.3%
        """
        total_samples = cls._TRAINING_SAMPLES + cls._TESTING_SAMPLES

        result = {
            "accuracy":          cls._ACCURACY,
            "precision":         cls._PRECISION,
            "recall":            cls._RECALL,
            "f1_score":          cls._F1_SCORE,
            "training_samples":  cls._TRAINING_SAMPLES,
            "testing_samples":   cls._TESTING_SAMPLES,
            "total_samples":     total_samples,
            "train_test_split":  "70% : 30%",
            "algorithm":         "Random Forest Classifier",

            # Fitur yang digunakan sebagai input model
            "features_used": [
                "B2 (Blue)", "B3 (Green)", "B4 (Red)",
                "B8 (NIR)", "B11 (SWIR-1)", "B12 (SWIR-2)",
                "NDVI", "NDMI", "NDBI",
            ],

            # Kelas output klasifikasi
            "target_classes": ["Hutan", "Non-Hutan"],

            # Rumus matematis tiap metrik (untuk tampilan di frontend)
            "formulas": {
                "accuracy":  "(TP + TN) / (TP + TN + FP + FN) × 100",
                "precision": "TP / (TP + FP) × 100",
                "recall":    "TP / (TP + FN) × 100",
                "f1_score":  "2 × (Precision × Recall) / (Precision + Recall)",
            },
        }

        logger.debug(
            "Metrics disiapkan: accuracy=%.1f%%, F1=%.1f%%",
            cls._ACCURACY, cls._F1_SCORE,
        )
        return result

    # ---------------------------------------------------------------------------
    # GET INTERPRETATION
    # ---------------------------------------------------------------------------

    @classmethod
    def get_interpretation(cls) -> dict:
        """
        Kembalikan teks interpretasi hasil evaluasi model dan limitasinya.

        Memberikan konteks naratif tentang arti dari angka-angka metrik,
        implikasinya terhadap analisis deforestasi, serta keterbatasan model.

        Returns:
            dict: Interpretasi lengkap dengan struktur:
                {
                    "overall_assessment"  : str,   # Penilaian keseluruhan model
                    "accuracy_context"    : str,   # Konteks nilai akurasi
                    "fp_implication"      : str,   # Dampak False Positive
                    "fn_implication"      : str,   # Dampak False Negative
                    "precision_vs_recall" : str,   # Trade-off precision vs recall
                    "limitations"         : list,  # Keterbatasan model
                    "recommendations"     : list,  # Saran peningkatan
                    "data_source"         : str,   # Sumber data
                }

        Example:
            >>> interp = ModelService.get_interpretation()
            >>> print(interp['overall_assessment'])
            'Model Random Forest menunjukkan akurasi 75.6% ...'
            >>> for lim in interp['limitations']:
            ...     print(f"- {lim}")
        """
        result = {
            "overall_assessment": (
                f"Model Random Forest menunjukkan akurasi {cls._ACCURACY}% dalam "
                "mengklasifikasikan tutupan hutan Kerinci berbasis citra Sentinel-2. "
                f"Nilai ini tergolong cukup baik mengingat kompleksitas lanskap "
                "tropis dengan variasi vegetasi yang tinggi."
            ),

            "accuracy_context": (
                f"Akurasi {cls._ACCURACY}% berarti model memprediksi dengan benar "
                f"pada {cls._CM_TP + cls._CM_TN} dari {cls._CM_TP + cls._CM_TN + cls._CM_FP + cls._CM_FN} "
                "sampel uji. Dalam konteks monitoring hutan, angka ini perlu "
                "diimbangi dengan analisis lapangan untuk validasi."
            ),

            "fp_implication": (
                f"False Positive ({cls._CM_FP} kasus): Model 'melihat' hutan di mana "
                "sebenarnya bukan hutan. Implikasinya adalah overestimasi luas hutan — "
                "area seperti perkebunan kelapa sawit, kebun teh, atau semak belukar "
                "dengan NDVI tinggi berpotensi salah diklasifikasikan sebagai hutan."
            ),

            "fn_implication": (
                f"False Negative ({cls._CM_FN} kasus): Model 'melewatkan' area hutan "
                "yang sebenarnya ada. Ini berarti underestimasi kerusakan hutan — "
                "kondisi berbahaya karena deforestasi yang terjadi tidak terdeteksi. "
                "Sering terjadi pada area dengan tutupan awan atau hutan dengan "
                "kerapatan rendah."
            ),

            "precision_vs_recall": (
                f"Precision ({cls._PRECISION}%) lebih tinggi dari Recall ({cls._RECALL}%), "
                "menunjukkan model lebih konservatif — ketika model memprediksi 'hutan', "
                "kemungkinan besar benar. Namun model cenderung melewatkan beberapa area "
                "hutan yang sebenarnya ada (recall lebih rendah)."
            ),

            # Keterbatasan model yang perlu diketahui pengguna
            "limitations": [
                "Akurasi dibatasi oleh kualitas data training (210 sampel relatif kecil).",
                "Citra Sentinel-2 dipengaruhi tutupan awan — area berawan sulit diklasifikasi.",
                "Model tidak membedakan jenis hutan (primer, sekunder, mangrove, dll.).",
                "Perubahan musiman vegetasi bisa mempengaruhi akurasi klasifikasi.",
                "Model dilatih pada data 2024–2025, performa bisa berbeda untuk tahun lain.",
                "Resolusi spasial 10–20 meter Sentinel-2 membatasi deteksi perubahan kecil.",
            ],

            # Rekomendasi untuk meningkatkan model
            "recommendations": [
                "Perbanyak sampel training (minimal 500+ sampel per kelas).",
                "Tambahkan data validasi lapangan (ground truth GPS).",
                "Eksplorasi algoritma lain: XGBoost, SVM, atau Deep Learning (CNN).",
                "Gunakan cloud-free composite yang lebih panjang (6 bulan atau 1 tahun).",
                "Tambahkan fitur tekstur (GLCM) untuk membedakan jenis vegetasi.",
                "Validasi dengan data independen dari sumber lain (LAPAN, KLHK).",
            ],

            "data_source": (
                "Sentinel-2 Level-2A (Surface Reflectance) — "
                "COPERNICUS/S2_SR_HARMONIZED via Google Earth Engine. "
                "Periode: Januari–Desember 2024 & 2025."
            ),
        }

        logger.debug("Interpretasi model berhasil disiapkan.")
        return result

    # ---------------------------------------------------------------------------
    # UTILITY: CHECK MODEL FILE EXISTS
    # ---------------------------------------------------------------------------

    @staticmethod
    def model_file_exists(year: int) -> bool:
        """
        Cek apakah file model .pkl tersedia di folder /models/.

        Args:
            year (int): Tahun model (2024 atau 2025).

        Returns:
            bool: True jika file ada, False jika tidak.

        Example:
            >>> exists = ModelService.model_file_exists(2024)
            >>> print(exists)  # True atau False
        """
        if year not in MODEL_FILES:
            return False
        filepath = MODELS_FOLDER / MODEL_FILES[year]
        exists = filepath.exists()
        logger.debug("Model file %d: %s (%s)", year, filepath, "ada" if exists else "tidak ada")
        return exists

    @staticmethod
    def get_available_models() -> dict:
        """
        Kembalikan status ketersediaan semua file model .pkl.

        Returns:
            dict: Status tiap model:
                {
                    2024: True/False,
                    2025: True/False
                }

        Example:
            >>> status = ModelService.get_available_models()
            >>> print(status)
            {2024: True, 2025: False}
        """
        return {
            year: (MODELS_FOLDER / filename).exists()
            for year, filename in MODEL_FILES.items()
        }


# ---------------------------------------------------------------------------
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ---------------------------------------------------------------------------

def get_confusion_matrix() -> dict:
    """Shorthand untuk ModelService.get_confusion_matrix()."""
    return ModelService.get_confusion_matrix()


def get_metrics() -> dict:
    """Shorthand untuk ModelService.get_metrics()."""
    return ModelService.get_metrics()


def get_interpretation() -> dict:
    """Shorthand untuk ModelService.get_interpretation()."""
    return ModelService.get_interpretation()
