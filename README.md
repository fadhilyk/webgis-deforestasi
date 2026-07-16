# WebGIS Monitoring Deforestasi - Kabupaten Kerinci 🌲

Repositori ini berisi seluruh kode, data, dan hasil analisis untuk proyek akhir/skripsi WebGIS Monitoring Deforestasi menggunakan citra satelit Sentinel-2 dan algoritma Random Forest Classifier.

## 📋 Informasi Proyek

- **Topik Proyek**: WebGIS Monitoring Deforestasi Hutan
- **Objek Penelitian**: Tutupan Hutan (Forest Cover)
- **Wilayah Studi**: Kabupaten Kerinci, Provinsi Jambi
- **Anggota Tim**: 
  - Fadhil Y. K. (NIM: [Isi NIM])
  - [Nama Anggota 2] (NIM: [Isi NIM]) *(Hapus jika tidak ada)*

## 🔗 Tautan Penting

- **Aplikasi WebGIS Live**: [https://fadhilyk.pythonanywhere.com](https://fadhilyk.pythonanywhere.com)
- **Laporan Proyek (PDF)**: [Tautan Google Drive / Link Download Laporan] *(Silakan isi link laporan di sini)*
- **Dataset Besar**: [Tautan Google Drive] *(Jika ada file model/data yang melebihi batas GitHub)*

## 📂 Struktur Folder (Sesuai Ketentuan)

Repositori ini diatur dengan struktur minimum sebagai berikut:

```text
📦 webgis-deforestasi
 ┣ 📂 gee/          # Skrip kode Google Earth Engine (GEE) javascript
 ┣ 📂 webgis/       # Kode sumber aplikasi WebGIS (Flask Backend & HTML/JS/CSS Frontend)
 ┣ 📂 data/         # File GeoJSON hasil ekspor GEE (Batas Wilayah, Gain, Loss, Target)
 ┣ 📂 results/      # File output/hasil (misal: visualisasi matriks, grafik, model .pkl)
 ┣ 📂 report/       # File laporan dokumen proyek (PDF/Word)
 ┗ 📜 README.md     # Penjelasan repositori (file ini)
```

*(Catatan: Saat ini sistem WebGIS Flask berada di direktori utama (root). Anda dapat merapikannya dengan memindahkannya ke dalam folder `webgis/` jika diperlukan).*

## 💻 Cara Membuka & Menjalankan WebGIS

### Opsi 1: Akses Langsung (Online)
Cara termudah adalah dengan mengakses tautan WebGIS yang sudah di-deploy secara publik:
👉 **[Buka Aplikasi WebGIS Kerinci](https://fadhilyk.pythonanywhere.com)**

### Opsi 2: Menjalankan Secara Lokal (Offline)
Jika Anda ingin menjalankan aplikasi ini di komputer/laptop Anda secara lokal:

1. **Clone Repositori**
   ```bash
   git clone https://github.com/fadhilyk/webgis-deforestasi.git
   cd webgis-deforestasi
   ```

2. **Buat Virtual Environment (Opsional namun disarankan)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi Flask**
   ```bash
   python app.py
   ```

5. **Buka di Browser**
   Buka peramban (browser) web Anda dan akses: `http://localhost:5000`

## 🛠️ Teknologi yang Digunakan
- **Pemrosesan Data Spasial**: Google Earth Engine (JavaScript API)
- **Machine Learning**: Scikit-Learn (Random Forest) & GeoPandas
- **Backend WebGIS**: Python (Flask)
- **Frontend & Peta**: HTML5, CSS3, Bootstrap 5, Leaflet.js
- **Deployment**: PythonAnywhere
