# PRD: WebGIS Monitoring Deforestasi Kerinci
**Project**: WebGIS Empat Tab: Jelaskan Hasil, Proses, dan Kepercayaannya  
**Version**: 1.0  
**Created**: July 2026  
**Status**: In Development

---

## **1. EXECUTIVE SUMMARY**

Aplikasi web interaktif berbasis Geographic Information System (WebGIS) untuk memantau perubahan tutupan hutan di Kabupaten Kerinci menggunakan data Sentinel-2 dan machine learning (Random Forest). Sistem ini menyajikan analisis deforestasi dalam 4 tab interaktif: visualisasi peta, data & proses, evaluasi model, dan insight hasil.

**Target Users:**
- Dinas Kehutanan / Stakeholder Pemerintah
- Peneliti & Akademisi
- Environmental Monitor
- Dosen & Mahasiswa (untuk evaluasi submission)

**Platform**: Web-based, cloud-hosted (Render.com), accessible via GitHub

---

## **2. PRODUCT VISION**

Menyediakan dashboard WebGIS yang **interaktif**, **informatif**, dan **transparan** untuk memudahkan stakeholder memahami:
- ✅ Perubahan vegetasi (gain/loss) di Kerinci tahun 2024-2025
- ✅ Akurasi & kepercayaan model machine learning
- ✅ Insight spatial dan rekomendasi kebijakan

---

## **3. SCOPE & DELIVERABLES**

### **3.1 IN-SCOPE**

| **Feature** | **Description** | **Priority** |
|---|---|---|
| **TAB 1: Peta Hasil** | Visualisasi interaktif 5 layer GeoJSON dengan Leaflet | P0 |
| **TAB 2: Data & Proses** | Info data source, statistik luas, workflow diagram | P0 |
| **TAB 3: Evaluasi Model** | Confusion matrix, accuracy/precision/recall/F1, interpretasi | P0 |
| **TAB 4: Insight Hasil** | Summary stats, spatial analysis, recommendations | P0 |
| **Responsive Design** | Mobile-friendly UI dengan Bootstrap 5 | P1 |
| **GitHub Integration** | Push-deploy otomatis ke Render | P0 |
| **Documentation** | README, API docs, deployment guide | P1 |

### **3.2 OUT-OF-SCOPE**

- ❌ Real-time Sentinel-2 data ingestion (static GeoJSON files)
- ❌ User authentication/authorization
- ❌ Advanced GIS tools (buffer, clip, merge)
- ❌ Multi-user collaboration features
- ❌ Database persistence (PostgreSQL) - optional for Phase 2

---

## **4. DATA SPECIFICATIONS**

### **4.1 Input Data**

5 GeoJSON files (semua ada di `/data/` folder):

| **File** | **Description** | **Purpose** | **Layer Name** |
|---|---|---|---|
| `UAS_Kerinci_BatasWilayah.geojson` | Batas administrasi kota | Base map / reference boundary | `batas-wilayah` |
| `UAS_Kerinci_Gain.geojson` | Area dengan vegetasi bertambah | Monitoring gain 2024-2025 | `gain` |
| `UAS_Kerinci_Loss.geojson` | Area dengan vegetasi berkurang | Monitoring loss 2024-2025 | `loss` |
| `UAS_Kerinci_Target2024.geojson` | Target area tahun 2024 | Reference target 2024 | `target-2024` |
| `UAS_Kerinci_Target2025.geojson` | Target area tahun 2025 | Reference target 2025 | `target-2025` |

### **4.2 Data Properties**

Setiap GeoJSON feature minimal memiliki:
```json
{
  "type": "Feature",
  "geometry": { "type": "Polygon", "coordinates": [...] },
  "properties": {
    "area_ha": 1234.5,
    "percentage": 2.34,
    "periode": "2024-2025"
  }
}
```

### **4.3 Model Data**

Pre-trained Random Forest model (2024 & 2025):
- Format: `.pkl` (Python pickle)
- Location: `/models/`
- Used for: Tab 3 confusion matrix reference

---

## **5. FUNCTIONAL REQUIREMENTS**

### **5.1 TAB 1: PETA HASIL**

**FR1.1** | Render peta interaktif dengan Leaflet
- Input: 5 GeoJSON layers
- Output: Map dengan zoom/pan/popup
- Behavior: Base layer (BatasWilayah) always visible, Gain/Loss togglable

**FR1.2** | Layer toggle controls
- Checkbox untuk Gain (green, opacity 0.5)
- Checkbox untuk Loss (red, opacity 0.5)
- Always visible: Target2024 (purple dashed), Target2025 (orange dashed)

**FR1.3** | Interactive popups
- Click feature → show properties (area_ha, periode, etc)

**FR1.4** | Legend
- Explain colors: gray=boundary, green=gain, red=loss, purple=target2024, orange=target2025

**FR1.5** | Zoom to extent
- Default zoom level: 10 (Kerinci area)
- Center: [-0.42, 101.27]

---

### **5.2 TAB 2: DATA & PROSES**

**FR2.1** | Display data metadata
- Sumber data: Sentinel-2 COPERNICUS/S2_SR_HARMONIZED
- Periode: 01 Jan - 31 Des (2024 & 2025)
- Cloud masking: S2 Cloud Probability + SCL
- Composite: Median Composite

**FR2.2** | Show processing workflow diagram
```
Sentinel-2 
  → Preprocessing (cloud masking, composite)
  → Ground Truth (labeled data)
  → Random Forest (classification)
  → Change Analysis (gain/loss detection)
```

**FR2.3** | Calculate & display statistics
- Luas Gain: X ha (calculated from UAS_Kerinci_Gain.geojson)
- Luas Loss: Y ha (calculated from UAS_Kerinci_Loss.geojson)
- Persentase perubahan: Z%

**FR2.4** | Layer information table
- Layer name, data type (Polygon), feature count, CRS

---

### **5.3 TAB 3: EVALUASI MODEL**

**FR3.1** | Display confusion matrix
```
                Predicted (0)    Predicted (1)
Actual (0)      TN = 38          FP = 7
Actual (1)      FN = 15          TP = 30
```

**FR3.2** | Calculate & show metrics
- Accuracy: 75.6%
- Precision: 81.1%
- Recall: 66.7%
- F1-score: 73.3%

**FR3.3** | Interpretasi hasil
- Model accuracy explanation
- False Positive (FP) interpretation & implications
- False Negative (FN) interpretation & implications

**FR3.4** | Keterbatasan model
- Sentinel-2 spatial resolution (10-20m)
- Cloud masking limitations
- Ground truth coverage limitations

---

### **5.4 TAB 4: INSIGHT HASIL**

**FR4.1** | Summary statistics
- Luas Target 2024: 4,250 ha
- Luas Target 2025: 3,980 ha
- Pertambahan (gain): 540 ha (+1.27%)
- Pengurangan (loss): -810 ha (-1.91%)
- Perubahan bersih: -270 ha (-6.35%)

**FR4.2** | Spatial insights
- Lokasi perubahan terbesar (Bagian timur kota)
- Pola distribusi gain/loss
- Kemungkinan penyebab (ekspansi permukiman, pembangunan, konversi lahan)

**FR4.3** | Potensi penggunaan hasil
- Perencanaan ruang hijau dan monitoring
- Lingkungan, kebijakan tata ruang
- Potential implementation strategies

**FR4.4** | Rekomendasi lanjutan
- Multi-tahun analysis
- Integrasi data sosial-ekonomi
- Continuous monitoring framework

---

## **6. NON-FUNCTIONAL REQUIREMENTS**

| **NFR** | **Requirement** | **Target** |
|---|---|---|
| **Performance** | Page load time | < 3 seconds |
| **Availability** | Uptime | 99% |
| **Responsiveness** | Mobile support | iOS + Android |
| **Security** | HTTPS | Enforced via Render |
| **Scalability** | Concurrent users | 100+ users |
| **Accessibility** | WCAG 2.1 | Level AA |
| **Browser Support** | Chrome, Firefox, Safari | Latest 2 versions |

---

## **7. TECHNICAL CONSTRAINTS**

- **Language**: Python (backend) + JavaScript (frontend)
- **Backend Framework**: Flask 2.3+
- **Frontend**: HTML5 + Bootstrap 5 + Leaflet.js + Plotly.js
- **Database**: GeoJSON files (no database required for MVP)
- **Hosting**: Render.com (free tier)
- **Deployment**: GitHub push → Render auto-deploy
- **Python Version**: 3.11+

---

## **8. ACCEPTANCE CRITERIA**

✅ **MVP Acceptance (Phase 1):**
- [ ] All 5 GeoJSON files load without errors
- [ ] Map displays all layers correctly (colors, opacity, toggles work)
- [ ] Tab 2 statistics calculated & displayed accurately
- [ ] Tab 3 confusion matrix & metrics shown
- [ ] Tab 4 insights populated from actual data
- [ ] Responsive on mobile (Bootstrap layout)
- [ ] Deployed to Render with GitHub integration
- [ ] All API endpoints return valid JSON

✅ **Code Quality:**
- [ ] Code follows PEP 8 (Python) + ES6 (JavaScript)
- [ ] Comments on complex logic
- [ ] No hardcoded values (use config.py)
- [ ] Error handling on API endpoints

✅ **Documentation:**
- [ ] README.md with setup & deployment instructions
- [ ] API documentation (endpoints, params, responses)
- [ ] Code comments for non-obvious logic

---

## **9. SUCCESS METRICS**

| **Metric** | **Target** | **Measurement** |
|---|---|---|
| **Functionality** | 100% Features implemented | Feature checklist |
| **Performance** | Page load < 3s | Browser DevTools |
| **User Experience** | Intuitive navigation | Dosen feedback |
| **Code Quality** | No critical bugs | Testing results |
| **Deployment** | Auto-deploy working | GitHub push → live |

---

## **10. TIMELINE & MILESTONES**

| **Phase** | **Duration** | **Deliverables** |
|---|---|---|
| **Phase 1: Setup & Planning** | Days 1-2 | PRD, SDD, Agents.md, Prompts.md |
| **Phase 2: Backend Development** | Days 3-5 | Flask app + API endpoints + GeoJSON loading |
| **Phase 3: Frontend Development** | Days 6-8 | HTML/CSS/JS + Leaflet map + Tabs |
| **Phase 4: Integration & Testing** | Days 9-10 | Full integration, testing, bug fixes |
| **Phase 5: Deployment** | Day 11 | Deploy to Render, verify live |
| **Phase 6: Documentation & Review** | Day 12 | README, API docs, dosen submission |

---

## **11. ASSUMPTIONS & DEPENDENCIES**

### **Assumptions**
- GeoJSON files sudah valid & properly formatted
- Random Forest model sudah trained & available as .pkl
- Dosen access melalui URL live (tidak local install)
- Data tidak akan berubah frequently (static GeoJSON)

### **Dependencies**
- GitHub repository with write access
- Render.com free account
- Python 3.11+ local environment for development
- Modern web browser (Chrome, Firefox, Safari)

---

## **12. GLOSSARY**

| **Term** | **Definition** |
|---|---|
| **Gain** | Area dimana vegetasi bertambah (dari non-forest menjadi forest) |
| **Loss** | Area dimana vegetasi berkurang (dari forest menjadi non-forest) |
| **Sentinel-2** | Satellite imagery dari European Space Agency (ESA) |
| **GeoJSON** | Format JSON untuk geographic data (polygons, points, lines) |
| **Random Forest** | Machine learning ensemble method untuk classification |
| **Confusion Matrix** | Table untuk evaluasi model classification (TP, TN, FP, FN) |
| **WebGIS** | Web-based Geographic Information System |

---

## **13. REVISION HISTORY**

| **Version** | **Date** | **Author** | **Changes** |
|---|---|---|---|
| 1.0 | 16 July 2026 | Hans | Initial PRD creation |

---

**Document Owner**: Hans  
**Last Updated**: 16 July 2026  
**Status**: APPROVED FOR DEVELOPMENT
