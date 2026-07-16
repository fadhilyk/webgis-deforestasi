"""
services/geo_service.py - Geospatial Service Layer
====================================================
WebGIS Monitoring Deforestasi Kerinci

Menyediakan operasi geospasial untuk membaca, mengkonversi, dan
menghitung data dari file GeoJSON di folder /data/.

Fungsi utama:
    - load_geojson()      : Load GeoJSON file → GeoDataFrame
    - geojson_to_json()   : GeoDataFrame → JSON-serializable dict
    - calculate_area_ha() : Hitung luas total dalam hektar

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import json
import logging
from pathlib import Path

import geopandas as gpd
from geopandas import GeoDataFrame

from config import DATA_FOLDER, GEOJSON_FILES

# ---------------------------------------------------------------------------
# LOGGER
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# GEO SERVICE CLASS
# ---------------------------------------------------------------------------

class GeoService:
    """
    Service class untuk operasi geospasial pada data GeoJSON Kerinci.

    Menyediakan method statis untuk:
    - Memuat file GeoJSON dari folder /data/
    - Mengkonversi GeoDataFrame ke dict JSON-serializable
    - Menghitung luas area dalam hektar

    Attributes:
        _cache (dict): In-memory cache untuk menyimpan GeoDataFrame
                       yang sudah di-load agar tidak reload berulang.

    Example:
        >>> service = GeoService()
        >>> gdf = service.load_geojson('gain')
        >>> luas_ha = service.calculate_area_ha(gdf)
        >>> print(f"Luas gain: {luas_ha} ha")
    """

    # Cache class-level: menyimpan GeoDataFrame per layer_name
    _cache: dict[str, GeoDataFrame] = {}

    # ---------------------------------------------------------------------------
    # LOAD GEOJSON
    # ---------------------------------------------------------------------------

    @classmethod
    def load_geojson(cls, layer_name: str, use_cache: bool = True) -> GeoDataFrame:
        """
        Load file GeoJSON dari folder /data/ berdasarkan nama layer.

        Menerima nama layer (key) dan memetakannya ke nama file GeoJSON
        yang sesuai menggunakan dictionary GEOJSON_FILES dari config.py.

        Args:
            layer_name (str): Nama layer yang ingin dimuat. Nilai yang valid:
                              - 'batas-wilayah' → UAS_Kerinci_BatasWilayah.geojson
                              - 'gain'          → UAS_Kerinci_Gain.geojson
                              - 'loss'          → UAS_Kerinci_Loss.geojson
                              - 'target-2024'   → UAS_Kerinci_Target2024.geojson
                              - 'target-2025'   → UAS_Kerinci_Target2025.geojson
            use_cache (bool): Jika True, gunakan data dari cache jika tersedia.
                              Default: True.

        Returns:
            GeoDataFrame: Data geospasial dalam format GeoDataFrame GeoPandas.

        Raises:
            ValueError: Jika layer_name tidak dikenali (tidak ada di GEOJSON_FILES).
            FileNotFoundError: Jika file GeoJSON tidak ditemukan di folder /data/.
            RuntimeError: Jika file gagal dibaca atau format tidak valid.

        Example:
            >>> gdf = GeoService.load_geojson('gain')
            >>> print(gdf.shape)
            (1234, 5)
        """
        # Validasi layer_name
        if layer_name not in GEOJSON_FILES:
            valid_keys = list(GEOJSON_FILES.keys())
            raise ValueError(
                f"Layer '{layer_name}' tidak dikenali. "
                f"Pilihan valid: {valid_keys}"
            )

        # Return dari cache jika tersedia dan use_cache=True
        if use_cache and layer_name in cls._cache:
            logger.debug("Cache hit untuk layer '%s'.", layer_name)
            return cls._cache[layer_name]

        # Bangun path file
        filename = GEOJSON_FILES[layer_name]
        filepath = DATA_FOLDER / filename

        # Cek keberadaan file
        if not filepath.exists():
            raise FileNotFoundError(
                f"File GeoJSON tidak ditemukan: '{filepath}'. "
                f"Pastikan file '{filename}' ada di folder /data/."
            )

        # Baca file GeoJSON dengan GeoPandas
        try:
            logger.info("Loading GeoJSON: %s ...", filepath)
            gdf = gpd.read_file(str(filepath))
            logger.info(
                "Berhasil load '%s': %d features, CRS=%s",
                layer_name, len(gdf), gdf.crs,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Gagal membaca file GeoJSON '{filepath}': {exc}"
            ) from exc

        # Simpan ke cache
        if use_cache:
            cls._cache[layer_name] = gdf
            logger.debug("Layer '%s' disimpan ke cache.", layer_name)

        return gdf

    # ---------------------------------------------------------------------------
    # GEOJSON TO JSON
    # ---------------------------------------------------------------------------

    @staticmethod
    def geojson_to_json(gdf: GeoDataFrame) -> dict:
        """
        Konversi GeoDataFrame ke GeoJSON dict yang JSON-serializable.

        Menggunakan method bawaan GeoPandas `.to_json()` untuk menghasilkan
        GeoJSON FeatureCollection lengkap dengan geometry dan properties.

        Args:
            gdf (GeoDataFrame): GeoDataFrame yang ingin dikonversi.
                                Harus memiliki kolom 'geometry'.

        Returns:
            dict: GeoJSON FeatureCollection dalam format dict Python.
                  Struktur:
                  {
                      "type": "FeatureCollection",
                      "features": [
                          {
                              "type": "Feature",
                              "geometry": {...},
                              "properties": {...}
                          },
                          ...
                      ]
                  }

        Raises:
            ValueError: Jika GeoDataFrame kosong atau tidak memiliki kolom geometry.
            RuntimeError: Jika konversi gagal.

        Example:
            >>> gdf = GeoService.load_geojson('loss')
            >>> geojson_dict = GeoService.geojson_to_json(gdf)
            >>> print(geojson_dict['type'])
            'FeatureCollection'
        """
        # Validasi input
        if gdf is None or len(gdf) == 0:
            raise ValueError("GeoDataFrame kosong, tidak dapat dikonversi.")

        if "geometry" not in gdf.columns:
            raise ValueError(
                "GeoDataFrame tidak memiliki kolom 'geometry'. "
                "Pastikan data GeoJSON telah dimuat dengan benar."
            )

        # Konversi ke GeoJSON string lalu parse ke dict
        try:
            geojson_str = gdf.to_json(show_bbox=True, drop_id=False)
            geojson_dict = json.loads(geojson_str)
            logger.debug(
                "GeoDataFrame berhasil dikonversi: %d features.",
                len(geojson_dict.get("features", [])),
            )
            return geojson_dict
        except Exception as exc:
            raise RuntimeError(
                f"Gagal mengkonversi GeoDataFrame ke JSON: {exc}"
            ) from exc

    # ---------------------------------------------------------------------------
    # CALCULATE AREA (HEKTAR)
    # ---------------------------------------------------------------------------

    @staticmethod
    def calculate_area_ha(gdf: GeoDataFrame) -> float:
        """
        Hitung total luas semua geometri dalam GeoDataFrame (satuan: hektar).

        Kalkulasi dilakukan dengan menjumlahkan luas semua geometri
        menggunakan `.geometry.area.sum()`. Karena data GeoJSON umumnya
        menggunakan CRS geografis (EPSG:4326, satuan derajat), data
        diproyeksikan ke CRS metrik (EPSG:3857) sebelum menghitung luas.

        Formula:
            area_ha = gdf_projected.geometry.area.sum() / 10_000

        Args:
            gdf (GeoDataFrame): GeoDataFrame yang ingin dihitung luasnya.
                                Harus memiliki kolom 'geometry'.

        Returns:
            float: Total luas dalam hektar, dibulatkan 2 desimal.
                   Contoh: 1234.56

        Raises:
            ValueError: Jika GeoDataFrame kosong atau tidak memiliki geometry.
            RuntimeError: Jika kalkulasi luas gagal.

        Example:
            >>> gdf = GeoService.load_geojson('gain')
            >>> luas = GeoService.calculate_area_ha(gdf)
            >>> print(f"Total luas gain: {luas} ha")
            Total luas gain: 540.25 ha
        """
        # Validasi input
        if gdf is None or len(gdf) == 0:
            raise ValueError(
                "GeoDataFrame kosong, tidak dapat menghitung luas."
            )

        if "geometry" not in gdf.columns:
            raise ValueError(
                "GeoDataFrame tidak memiliki kolom 'geometry'."
            )

        try:
            # Proyeksikan ke CRS metrik (meter) agar area akurat
            # EPSG:3857 = Web Mercator (satuan meter)
            if gdf.crs is None:
                logger.warning(
                    "GeoDataFrame tidak memiliki CRS. "
                    "Menggunakan EPSG:4326 sebagai default."
                )
                gdf = gdf.set_crs("EPSG:4326")

            gdf_projected = gdf.to_crs("EPSG:3857")

            # Hitung luas: m² → hektar (1 ha = 10.000 m²)
            area_m2 = gdf_projected.geometry.area.sum()
            area_ha = round(area_m2 / 10_000, 2)

            logger.debug(
                "Total luas: %.2f m² = %.2f ha", area_m2, area_ha
            )
            return area_ha

        except Exception as exc:
            raise RuntimeError(
                f"Gagal menghitung luas area: {exc}"
            ) from exc

    # ---------------------------------------------------------------------------
    # UTILITY: CLEAR CACHE
    # ---------------------------------------------------------------------------

    @classmethod
    def clear_cache(cls) -> None:
        """
        Hapus semua data dari in-memory cache.

        Berguna saat file GeoJSON diperbarui dan data lama
        perlu di-invalidate.

        Example:
            >>> GeoService.clear_cache()
        """
        cls._cache.clear()
        logger.info("GeoService cache telah dibersihkan.")

    @classmethod
    def get_cached_layers(cls) -> list[str]:
        """
        Kembalikan daftar nama layer yang saat ini tersimpan di cache.

        Returns:
            list[str]: Daftar layer_name yang sudah di-cache.

        Example:
            >>> cached = GeoService.get_cached_layers()
            >>> print(cached)
            ['gain', 'loss']
        """
        return list(cls._cache.keys())


# ---------------------------------------------------------------------------
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ---------------------------------------------------------------------------
# Shorthand agar bisa dipanggil langsung tanpa instantiate class:
# from services.geo_service import load_geojson, calculate_area_ha

def load_geojson(layer_name: str, use_cache: bool = True) -> GeoDataFrame:
    """Shorthand untuk GeoService.load_geojson(). Lihat docstring class."""
    return GeoService.load_geojson(layer_name, use_cache=use_cache)


def geojson_to_json(gdf: GeoDataFrame) -> dict:
    """Shorthand untuk GeoService.geojson_to_json(). Lihat docstring class."""
    return GeoService.geojson_to_json(gdf)


def calculate_area_ha(gdf: GeoDataFrame) -> float:
    """Shorthand untuk GeoService.calculate_area_ha(). Lihat docstring class."""
    return GeoService.calculate_area_ha(gdf)
