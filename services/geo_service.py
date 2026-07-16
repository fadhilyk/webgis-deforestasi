"""
GeoJSON data service for WebGIS Monitoring Deforestasi Kerinci.

Handles loading, converting, and analyzing GeoJSON files
for deforestation monitoring layers.
"""

from pathlib import Path

import geopandas as gpd

from config import DATA_FOLDER, GEOJSON_FILES


class GeoService:
    """Service for GeoJSON file operations — load, convert, calculate."""

    # User-facing name → GeoJSON filename mapping
    FILE_MAP = {
        'batas-wilayah': GEOJSON_FILES['batas_wilayah'],
        'gain': GEOJSON_FILES['gain'],
        'loss': GEOJSON_FILES['loss'],
        'target-2024': GEOJSON_FILES['target_2024'],
        'target-2025': GEOJSON_FILES['target_2025'],
    }

    @staticmethod
    def load_geojson(name: str) -> gpd.GeoDataFrame:
        """Load a GeoJSON layer by short name into a GeoDataFrame.

        Args:
            name: One of 'batas-wilayah', 'gain', 'loss',
                  'target-2024', 'target-2025'.

        Returns:
            GeoDataFrame with the layer data.

        Raises:
            ValueError: If *name* is unknown.
            FileNotFoundError: If the underlying GeoJSON file is missing.
        """
        filename = GeoService.FILE_MAP.get(name)
        if filename is None:
            valid = ', '.join(GeoService.FILE_MAP)
            raise ValueError(f"Unknown layer '{name}'. Valid: {valid}")

        path = DATA_FOLDER / filename
        if not path.exists():
            raise FileNotFoundError(f"GeoJSON not found: {path}")

        return gpd.read_file(path)

    @staticmethod
    def geojson_to_json(gdf: gpd.GeoDataFrame) -> dict:
        """Convert a GeoDataFrame to a JSON-serialisable GeoJSON dict.

        Args:
            gdf: Input GeoDataFrame.

        Returns:
            GeoJSON FeatureCollection as a plain dict.
        """
        return gdf.__geo_interface__

    @staticmethod
    def calculate_area_ha(gdf: gpd.GeoDataFrame) -> float:
        """Calculate total area of all geometries in hectares.

        Auto-reprojects to UTM 47S (EPSG:32747) if CRS is geographic.

        Args:
            gdf: GeoDataFrame with valid geometries.

        Returns:
            Total area in hectares, rounded to 2 decimal places.
        """
        gdf_proj = gdf
        if gdf.crs and gdf.crs.is_geographic:
            gdf_proj = gdf.to_crs('EPSG:32747')
        area_m2 = float(gdf_proj.geometry.area.sum())
        area_ha = area_m2 / 10000
        return round(area_ha, 2)
