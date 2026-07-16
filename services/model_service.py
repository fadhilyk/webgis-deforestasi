"""
Model evaluation service for WebGIS Monitoring Deforestasi Kerinci.

Provides confusion matrix, performance metrics, and clinical
interpretation for the Random Forest classifier.
"""


class ModelService:
    """Service for ML model evaluation — metrics, matrix, interpretation."""

    @staticmethod
    def get_confusion_matrix() -> dict:
        """Return confusion matrix values from the trained model.

        Values reflect the Random Forest classifier performance on
        hold-out test data.

        Returns:
            dict with TP, TN, FP, FN counts and interpretation.
        """
        return {
            'TP': 30,
            'TN': 38,
            'FP': 7,
            'FN': 15,
            'interpretation': {
                'TP': 'Correctly predicted deforestation (True Positive)',
                'TN': 'Correctly predicted non-deforestation (True Negative)',
                'FP': 'False alarm — predicted deforestation, '
                       'actual non-deforestation (False Positive)',
                'FN': 'Missed deforestation — predicted non-deforestation, '
                       'actual deforestation (False Negative)',
            },
        }

    @staticmethod
    def get_metrics() -> dict:
        """Return model performance metrics.

        Metrics calculated from the confusion matrix values.

        Returns:
            dict with accuracy, precision, recall, f1_score,
            and sample counts.
        """
        return {
            'accuracy': 75.6,
            'precision': 81.1,
            'recall': 66.7,
            'f1_score': 73.3,
            'training_samples': 210,
            'testing_samples': 90,
        }

    @staticmethod
    def get_interpretation() -> dict:
        """Return clinical interpretation of model predictions.

        Explains FP (false alarms) and FN (missed detections)
        in the context of deforestation monitoring, along with
        known limitations.

        Returns:
            dict with fp_interpretation, fn_interpretation,
            limitations, and caveats.
        """
        return {
            'fp_interpretation': (
                'False Positives (FP=7) indicate areas the model '
                'predicted as deforestation but were actually unchanged. '
                'These are often caused by spectral confusion between '
                'bare soil and cleared land, or seasonal vegetation changes.'
            ),
            'fn_interpretation': (
                'False Negatives (FN=15) indicate actual deforestation '
                'that the model failed to detect. These are more '
                'consequential for monitoring — caused by small-patch '
                'clearing, cloud cover, or regeneration masking the '
                'disturbance signal.'
            ),
            'limitations': [
                'Model trained on limited sample size (300 total pixels)',
                'Single-temporal snapshot — no time-series trend analysis',
                'Binary classification only (forest/non-forest)',
                'Does not capture degradation, only complete loss',
            ],
            'caveats': [
                'Results are based on Landsat 8 OLI imagery (30m resolution)',
                'Accuracy may vary at class boundaries and heterogeneous areas',
                'Model should be re-validated annually with new reference data',
            ],
        }