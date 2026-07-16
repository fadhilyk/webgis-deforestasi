"""Route blueprints for WebGIS Monitoring Deforestasi Kerinci."""

from routes.peta import peta_bp
from routes.data_proses import data_bp
from routes.model import model_bp
from routes.insights import insights_bp

__all__ = ['peta_bp', 'data_bp', 'model_bp', 'insights_bp']
