"""
services/stats_service.py - Statistical Service Layer
======================================================
WebGIS Monitoring Deforestasi Kerinci

Menyediakan kalkulasi statistik untuk analisis perubahan tutupan hutan:
- Luas gain (pertambahan) dan loss (kehilangan) dalam hektar
- Persentase perubahan relatif
- Net change (perubahan bersih)
- Distribusi spasial perubahan

Fungsi utama:
    - calculate_gain_loss_stats() : Statistik lengkap gain vs loss
    - calculate_percentages()     : Helper kalkulasi persentase
    - get_spatial_summary()       : Ringkasan distribusi spasial

Author   : Hans (Project Lead)
Version  : 1.0
Created  : July 2026
"""

import logging

from geopandas import GeoDataFrame

from services.geo_service import GeoService

# ---------------------------------------------------------------------------
# LOGGER
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# STATS SERVICE CLASS
# ---------------------------------------------------------------------------

class StatsService:
    """
    Service class untuk kalkulasi statistik perubahan tutupan hutan Kerinci.

    Menghitung statistik berbasis data GeoJSON gain (pertambahan hutan)
    dan loss (kehilangan hutan) hasil analisis citra Sentinel-2.

    Semua kalkulasi menggunakan proyeksi EPSG:3857 melalui GeoService
    agar hasil luas dalam hektar akurat.

    Example:
        >>> from services.geo_service import GeoService
        >>> gain_gdf = GeoService.load_geojson('gain')
        >>> loss_gdf = GeoService.load_geojson('loss')
        >>> stats = StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)
        >>> print(stats['net_change_ha'])
    """

    # ---------------------------------------------------------------------------
    # CALCULATE GAIN/LOSS STATS
    # ---------------------------------------------------------------------------

    @staticmethod
    def calculate_gain_loss_stats(
        gain_gdf: GeoDataFrame,
        loss_gdf: GeoDataFrame,
    ) -> dict:
        """
        Hitung statistik lengkap gain & loss perubahan tutupan hutan.

        Menerima dua GeoDataFrame (gain dan loss), menghitung luas masing-masing
        dalam hektar, lalu mengkalkulasi persentase dan net change.

        Args:
            gain_gdf (GeoDataFrame): GeoDataFrame area pertambahan hutan
                                     (dari UAS_Kerinci_Gain.geojson).
            loss_gdf (GeoDataFrame): GeoDataFrame area kehilangan hutan
                                     (dari UAS_Kerinci_Loss.geojson).

        Returns:
            dict: Statistik lengkap dengan struktur:
                {
                    "gain_ha"              : float,  # Luas gain dalam hektar
                    "loss_ha"              : float,  # Luas loss dalam hektar
                    "total_change_ha"      : float,  # Total perubahan (gain + loss)
                    "net_change_ha"        : float,  # Net change (gain - loss)
                    "percentage_gain"      : float,  # % gain dari total
                    "percentage_loss"      : float,  # % loss dari total
                    "net_change_percent"   : float,  # % net change dari total
                    "status"               : str,    # 'net_gain' atau 'net_loss'
                    "gain_feature_count"   : int,    # Jumlah polygon gain
                    "loss_feature_count"   : int,    # Jumlah polygon loss
                }

        Raises:
            ValueError: Jika salah satu atau kedua GeoDataFrame kosong/None.
            RuntimeError: Jika kalkulasi gagal.

        Example:
            >>> stats = StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)
            >>> print(f"Gain: {stats['gain_ha']} ha ({stats['percentage_gain']}%)")
            >>> print(f"Loss: {stats['loss_ha']} ha ({stats['percentage_loss']}%)")
            >>> print(f"Net : {stats['net_change_ha']} ha")
        """
        # Validasi input
        if gain_gdf is None or len(gain_gdf) == 0:
            raise ValueError("GeoDataFrame 'gain' kosong atau None.")
        if loss_gdf is None or len(loss_gdf) == 0:
            raise ValueError("GeoDataFrame 'loss' kosong atau None.")

        try:
            # Hitung luas masing-masing layer (via GeoService agar proyeksi benar)
            gain_ha = GeoService.calculate_area_ha(gain_gdf)
            loss_ha = GeoService.calculate_area_ha(loss_gdf)

            logger.info("Gain area: %.2f ha | Loss area: %.2f ha", gain_ha, loss_ha)

            # Kalkulasi turunan
            percentages = StatsService.calculate_percentages(gain_ha, loss_ha)

            net_change_ha = round(gain_ha - loss_ha, 2)
            total_change_ha = round(gain_ha + loss_ha, 2)

            # Net change percentage relatif terhadap total perubahan
            net_change_percent = (
                round((net_change_ha / total_change_ha) * 100, 2)
                if total_change_ha > 0
                else 0.0
            )

            # Status: apakah lebih banyak gain atau loss?
            status = "net_gain" if net_change_ha >= 0 else "net_loss"

            result = {
                "gain_ha":             float(gain_ha),
                "loss_ha":             float(loss_ha),
                "total_change_ha":     float(total_change_ha),
                "net_change_ha":       float(net_change_ha),
                "percentage_gain":     float(percentages["percentage_gain"]),
                "percentage_loss":     float(percentages["percentage_loss"]),
                "net_change_percent":  float(net_change_percent),
                "status":              status,
                "gain_feature_count":  int(len(gain_gdf)),
                "loss_feature_count":  int(len(loss_gdf)),
            }

            logger.info(
                "Statistik berhasil dihitung: net_change=%.2f ha (%s)",
                net_change_ha, status,
            )
            return result

        except (ValueError, TypeError) as exc:
            raise exc
        except Exception as exc:
            raise RuntimeError(
                f"Gagal menghitung statistik gain/loss: {exc}"
            ) from exc

    # ---------------------------------------------------------------------------
    # CALCULATE PERCENTAGES (HELPER)
    # ---------------------------------------------------------------------------

    @staticmethod
    def calculate_percentages(gain_ha: float, loss_ha: float) -> dict:
        """
        Helper function: Hitung persentase gain dan loss dari total perubahan.

        Persentase dihitung relatif terhadap total perubahan (gain + loss),
        bukan terhadap luas total wilayah.

        Formula:
            total         = gain_ha + loss_ha
            percentage_gain = (gain_ha / total) * 100
            percentage_loss = (loss_ha / total) * 100

        Args:
            gain_ha (float): Luas area gain dalam hektar.
            loss_ha (float): Luas area loss dalam hektar.

        Returns:
            dict: Persentase gain dan loss:
                {
                    "gain_ha"         : float,
                    "loss_ha"         : float,
                    "total_ha"        : float,
                    "percentage_gain" : float,  # dalam persen (0–100)
                    "percentage_loss" : float,  # dalam persen (0–100)
                }

        Raises:
            ValueError: Jika gain_ha atau loss_ha negatif.

        Example:
            >>> pct = StatsService.calculate_percentages(540.25, 810.75)
            >>> print(pct['percentage_gain'])   # → 39.97
            >>> print(pct['percentage_loss'])   # → 60.03
        """
        if gain_ha < 0:
            raise ValueError(f"gain_ha tidak boleh negatif: {gain_ha}")
        if loss_ha < 0:
            raise ValueError(f"loss_ha tidak boleh negatif: {loss_ha}")

        total_ha = round(gain_ha + loss_ha, 2)

        if total_ha == 0:
            logger.warning("Total perubahan = 0 ha, semua persentase diset 0.")
            return {
                "gain_ha":         float(round(gain_ha, 2)),
                "loss_ha":         float(round(loss_ha, 2)),
                "total_ha":        float(total_ha),
                "percentage_gain": 0.0,
                "percentage_loss": 0.0,
            }

        percentage_gain = round((gain_ha / total_ha) * 100, 2)
        percentage_loss = round((loss_ha / total_ha) * 100, 2)

        logger.debug(
            "Persentase — Gain: %.2f%%, Loss: %.2f%%",
            percentage_gain, percentage_loss,
        )

        return {
            "gain_ha":         float(round(gain_ha, 2)),
            "loss_ha":         float(round(loss_ha, 2)),
            "total_ha":        float(total_ha),
            "percentage_gain": float(percentage_gain),
            "percentage_loss": float(percentage_loss),
        }

    # ---------------------------------------------------------------------------
    # GET SPATIAL SUMMARY
    # ---------------------------------------------------------------------------

    @staticmethod
    def get_spatial_summary() -> dict:
        """
        Kembalikan ringkasan distribusi spasial perubahan tutupan hutan Kerinci.

        Data spasial ini berdasarkan hasil analisis dan presentasi proyek,
        menggambarkan di mana konsentrasi gain dan loss terjadi di wilayah Kerinci.

        Returns:
            dict: Distribusi spasial gain dan loss:
                {
                    "gain_distribution": {
                        "primary_location"  : str,   # Lokasi utama gain
                        "percentage"        : float, # % gain di lokasi tersebut
                        "possible_causes"   : list,  # Daftar kemungkinan penyebab
                        "description"       : str,
                    },
                    "loss_distribution": {
                        "primary_location"  : str,
                        "percentage"        : float,
                        "possible_causes"   : list,
                        "description"       : str,
                    },
                    "analysis_period"       : str,   # Periode analisis
                    "data_source"           : str,   # Sumber data satelit
                    "notes"                 : str,
                }

        Example:
            >>> spatial = StatsService.get_spatial_summary()
            >>> print(spatial['gain_distribution']['primary_location'])
            'Bagian Timur Wilayah Kerinci'
        """
        spatial_summary = {
            "gain_distribution": {
                "primary_location": "Bagian Timur Wilayah Kerinci",
                "percentage": 60.0,
                "possible_causes": [
                    "Reforestasi dan penghijauan",
                    "Pemulihan lahan pasca kebakaran",
                    "Pertumbuhan vegetasi alami",
                    "Program rehabilitasi hutan",
                ],
                "description": (
                    "Konsentrasi pertambahan tutupan hutan terpusat di "
                    "bagian timur wilayah Kerinci, kemungkinan disebabkan "
                    "oleh program reforestasi dan pemulihan lahan alami."
                ),
            },
            "loss_distribution": {
                "primary_location": "Bagian Barat dan Tengah Wilayah Kerinci",
                "percentage": 40.0,
                "possible_causes": [
                    "Ekspansi area pertanian",
                    "Alih fungsi lahan untuk permukiman",
                    "Aktivitas perambahan hutan",
                    "Kebakaran hutan",
                ],
                "description": (
                    "Kehilangan tutupan hutan terkonsentrasi di bagian barat "
                    "dan tengah wilayah, kemungkinan akibat tekanan alih fungsi "
                    "lahan untuk pertanian dan permukiman."
                ),
            },
            "analysis_period": "Tahun 2024 – 2025",
            "data_source": "Sentinel-2 COPERNICUS/S2_SR_HARMONIZED",
            "notes": (
                "Analisis berbasis klasifikasi citra dengan algoritma "
                "Random Forest menggunakan band B2, B3, B4, B8, B11, B12 "
                "serta indeks NDVI, NDMI, dan NDBI."
            ),
        }

        logger.debug("Spatial summary berhasil dibuat.")
        return spatial_summary

    # ---------------------------------------------------------------------------
    # CALCULATE TARGET COMPARISON
    # ---------------------------------------------------------------------------

    @staticmethod
    def calculate_target_comparison(
        target_gdf: GeoDataFrame,
        actual_gdf: GeoDataFrame,
        year: int,
    ) -> dict:
        """
        Bandingkan luas target prediksi model vs realisasi aktual (gain/loss).

        Berguna untuk evaluasi akurasi model prediksi deforestasi.

        Args:
            target_gdf (GeoDataFrame): GeoDataFrame hasil prediksi model
                                       (target-2024 atau target-2025).
            actual_gdf (GeoDataFrame): GeoDataFrame data aktual (gain atau loss).
            year (int): Tahun analisis (2024 atau 2025).

        Returns:
            dict: Perbandingan target vs aktual:
                {
                    "year"            : int,
                    "target_ha"       : float,
                    "actual_ha"       : float,
                    "difference_ha"   : float,
                    "accuracy_percent": float,
                }

        Raises:
            ValueError: Jika GeoDataFrame kosong atau year tidak valid.

        Example:
            >>> comparison = StatsService.calculate_target_comparison(
            ...     t2024_gdf, loss_gdf, year=2024
            ... )
            >>> print(comparison['accuracy_percent'])
        """
        if year not in (2024, 2025):
            raise ValueError(f"Tahun tidak valid: {year}. Gunakan 2024 atau 2025.")
        if target_gdf is None or len(target_gdf) == 0:
            raise ValueError(f"GeoDataFrame target-{year} kosong atau None.")
        if actual_gdf is None or len(actual_gdf) == 0:
            raise ValueError("GeoDataFrame aktual kosong atau None.")

        target_ha = GeoService.calculate_area_ha(target_gdf)
        actual_ha = GeoService.calculate_area_ha(actual_gdf)

        difference_ha = round(target_ha - actual_ha, 2)

        # Akurasi: seberapa dekat target dengan aktual (100% = sempurna)
        accuracy_percent = (
            round((1 - abs(difference_ha) / target_ha) * 100, 2)
            if target_ha > 0 else 0.0
        )

        result = {
            "year":             year,
            "target_ha":        target_ha,
            "actual_ha":        actual_ha,
            "difference_ha":    difference_ha,
            "accuracy_percent": accuracy_percent,
            "overpredicted":    difference_ha > 0,  # True = model overpredict
        }

        logger.info(
            "Target vs Aktual %d: target=%.2f ha, aktual=%.2f ha, akurasi=%.2f%%",
            year, target_ha, actual_ha, accuracy_percent,
        )
        return result


# ---------------------------------------------------------------------------
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ---------------------------------------------------------------------------

def calculate_gain_loss_stats(gain_gdf: GeoDataFrame, loss_gdf: GeoDataFrame) -> dict:
    """Shorthand untuk StatsService.calculate_gain_loss_stats()."""
    return StatsService.calculate_gain_loss_stats(gain_gdf, loss_gdf)


def calculate_percentages(gain_ha: float, loss_ha: float) -> dict:
    """Shorthand untuk StatsService.calculate_percentages()."""
    return StatsService.calculate_percentages(gain_ha, loss_ha)


def get_spatial_summary() -> dict:
    """Shorthand untuk StatsService.get_spatial_summary()."""
    return StatsService.get_spatial_summary()
