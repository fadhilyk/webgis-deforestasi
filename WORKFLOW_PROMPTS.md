# WORKFLOW_PROMPTS.md: Step-by-Step Build Instructions
**WebGIS Monitoring Deforestasi Kerinci**  
**Version**: 1.0  
**Created**: 16 July 2026  
**Status**: Ready for Implementation

---

## **TABLE OF CONTENTS**

1. [Overview: Plan Mode vs Build Mode](#overview)
2. [Phase 1: Planning & Documentation](#phase1)
3. [Phase 2: Backend Development](#phase2)
4. [Phase 3: Frontend Development](#phase3)
5. [Phase 4: Integration & Testing](#phase4)
6. [Phase 5: Deployment](#phase5)
7. [Mode Decision Tree](#decision-tree)

---

## **OVERVIEW: PLAN MODE vs BUILD MODE**

### **What is Plan Mode?**

**Plan Mode** adalah saat Anda meminta Claude untuk **merencanakan, merancang, dan menjelaskan** sesuatu sebelum menulis kode.

**Gunakan Plan Mode ketika:**
- ✅ Ingin breakdown teknologi kompleks
- ✅ Perlu arsitektur sistem yang detail
- ✅ Meminta penjelasan konsep mendalam
- ✅ Merancang workflow/process
- ✅ Merencanakan testing strategy
- ✅ Membuat dokumentasi

**Output Plan Mode:**
- Detailed explanations
- Diagrams & flowcharts
- Step-by-step instructions
- Design documents
- Strategy & recommendations

**Contoh Prompt Plan Mode:**
```
"Breakdown the full tech stack untuk project ini dengan detail.
Jelaskan:
1. Tiap component
2. Mengapa dipilih
3. Bagaimana integrate
4. Potential issues
Sertakan diagram architecture."
```

---

### **What is Build Mode?**

**Build Mode** adalah saat Anda meminta Claude untuk **membuat file kode actual** yang langsung bisa dijalankan.

**Gunakan Build Mode ketika:**
- ✅ Siap implementasi (design sudah final)
- ✅ Butuh code file yang actionable
- ✅ Mengikuti detailed specification (dari SDD)
- ✅ Integrating components
- ✅ Testing & debugging
- ✅ Refactoring existing code

**Output Build Mode:**
- Actual code files
- Functions & classes
- Unit tests
- Error handling
- Comments & docstrings

**Contoh Prompt Build Mode:**
```
"Build the Flask app structure sesuai SDD:
1. Create app.py dengan Flask initialization
2. Konfigurasi folder paths (templates, static, data, models)
3. Import semua libraries yang dibutuhkan
4. Setup error handlers
5. Provide ready-to-run code

Ikuti PEP 8 conventions dan include comments."
```

---

### **Plan vs Build: Perbandingan**

| **Aspek** | **Plan Mode** | **Build Mode** |
|---|---|---|
| **Purpose** | Design & strategy | Implementation |
| **When** | Sebelum coding | Saat ready to code |
| **Output** | Documentation, explanations | Actual code files |
| **Detail Level** | High-level + detailed explanations | Low-level implementation details |
| **Code Quality** | N/A | Production-ready |
| **Testing** | Strategy & approach | Unit tests included |
| **Example** | "Explain the architecture" | "Create app.py file" |

---

### **Decision Tree: When to Use What?**

```
┌─ Pertanyaan: "Apa langkah berikutnya?"
│
├─ Apakah sudah ada design/specification detail?
│  ├─ TIDAK → PLAN MODE
│  │         "Jelaskan & design dulu"
│  │
│  └─ YA → NEXT QUESTION
│
├─ Apakah sudah siap mengimplementasikan?
│  ├─ TIDAK → PLAN MODE
│  │         "Jelaskan langkah-langkah implementasi"
│  │
│  └─ YA → BUILD MODE
│          "Create the code files"
│
└─ Apakah sudah ada code yang perlu dimodifikasi?
   ├─ TIDAK → BUILD MODE (create new)
   │
   └─ YA → BUILD MODE (modify existing)
```

---

## **PHASE 1: PLANNING & DOCUMENTATION**

### **Status: ✅ COMPLETE**

Fase ini sudah selesai dengan dokumentasi:
- ✅ PRD.md - Requirements
- ✅ SDD.md - Technical Design
- ✅ AGENTS.md - Team Coordination
- ✅ WORKFLOW_PROMPTS.md - This file

**Next Step:** Proceed to Phase 2

---

## **PHASE 2: BACKEND DEVELOPMENT**

### **Duration**: Days 3-5 (3 days)

### **Mode: BUILD MODE**

Pada fase ini Anda membuat Flask backend. Gunakan **BUILD MODE** dengan detailed specifications dari SDD.

---

### **STEP 2.1: Setup Flask App Structure**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build the Flask app structure untuk WebGIS Deforestasi sesuai SDD section 2.1:

Requirements:
1. Create app.py file:
   - Initialize Flask app
   - Configure template & static folder paths
   - Import all necessary libraries (Flask, geopandas, pandas, scikit-learn, json, etc)
   - Create a @app.route('/') endpoint yang returns 'Welcome' message
   - Include error handler untuk 404
   - Setup if __name__ == '__main__' block with debug=True

2. Create config.py file:
   - Define DATA_FOLDER = Path('data')
   - Define MODELS_FOLDER = Path('models')
   - Define TEMPLATE_FOLDER = Path('templates')
   - Define STATIC_FOLDER = Path('static')
   - Define MAP_CENTER = [-0.42, 101.27]
   - Define GEOJSON_FILES dict dengan semua 5 file names
   - Include comments explaining tiap config

3. Create requirements.txt dengan semua dependencies:
   - Flask==2.3.3
   - GunicornFlask-CORS==4.0.0
   - pandas==2.0.3
   - geopandas==0.12.2
   - shapely==2.0.1
   - scikit-learn==1.3.0
   - python-dotenv==1.0.0

Follow PEP 8 conventions.
Include docstrings pada functions.
Make code production-ready.
Provide semua 3 files lengkap siap copy-paste.
```

**Expected Output:**
- app.py (Flask initialization + basic routing)
- config.py (Configuration constants)
- requirements.txt (All dependencies)

**Testing After:**
```bash
pip install -r requirements.txt
python app.py
# Navigate to http://localhost:5000
# Should see "Welcome" message
```

---

### **STEP 2.2: Create Services Layer (Geo Service)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build geo_service.py sesuai SDD section 2.2:

Requirements:
1. Create services/geo_service.py dengan class GeoService:

2. Implement functions:
   a) load_geojson(filename: str) → GeoDataFrame
      - Load GeoJSON from /data/ folder
      - Accept: 'batas-wilayah', 'gain', 'loss', 'target-2024', 'target-2025'
      - Map filename ke actual file: e.g., 'gain' → 'UAS_Kerinci_Gain.geojson'
      - Return GeoDataFrame
      - Include error handling untuk file not found
      
   b) geojson_to_json(gdf: GeoDataFrame) → dict
      - Convert GeoDataFrame to GeoJSON dict
      - Include all properties & geometry
      - Return JSON-serializable dict
      
   c) calculate_area_ha(gdf: GeoDataFrame) → float
      - Calculate total area dari semua geometries dalam hectares
      - Formula: gdf.geometry.area.sum() / 10000
      - Return rounded to 2 decimals

3. Include docstrings explaining tiap function
4. Include error handling (file not found, invalid geometry)
5. Follow PEP 8

Provide lengkap ready-to-use code.
```

**Expected Output:**
- services/geo_service.py (GeoService class)

**Testing After:**
```python
from services.geo_service import GeoService
geo = GeoService()
gain_gdf = geo.load_geojson('gain')
area = geo.calculate_area_ha(gain_gdf)
print(f"Gain area: {area} ha")
```

---

### **STEP 2.3: Create Services Layer (Stats Service)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build stats_service.py sesuai SDD section 2.2:

Requirements:
1. Create services/stats_service.py dengan class StatsService:

2. Implement functions:
   a) calculate_gain_loss_stats(gain_gdf, loss_gdf) → dict
      - Input: 2 GeoDataFrames (gain & loss)
      - Calculate:
        * gain_area_ha = total gain area
        * loss_area_ha = total loss area
        * net_change_ha = gain - loss
        * percentage_gain = (gain / total) * 100
        * percentage_loss = (loss / total) * 100
        * net_change_percent = (net_change / total) * 100
      - Return dict dengan semua values (rounded to 2 decimals)
      
   b) calculate_percentages(gain_ha, loss_ha) → dict
      - Helper function untuk percentage calculations
      - Return dict dengan percentage values
      
   c) get_spatial_summary() → dict
      - Return spatial distribution information
      - Include: location, percentage, possible_causes (list)
      - Values berdasarkan dari presentation (East vs West, etc)

3. Include docstrings & error handling
4. Follow PEP 8

Provide lengkap ready-to-use code.
```

**Expected Output:**
- services/stats_service.py (StatsService class)

**Testing After:**
```python
from services.geo_service import GeoService
from services.stats_service import StatsService

geo = GeoService()
gain = geo.load_geojson('gain')
loss = geo.load_geojson('loss')

stats = StatsService()
result = stats.calculate_gain_loss_stats(gain, loss)
print(result)
# Output: {'gain_ha': 540.25, 'loss_ha': 810.75, ...}
```

---

### **STEP 2.4: Create Services Layer (Model Service)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build model_service.py sesuai SDD section 2.2:

Requirements:
1. Create services/model_service.py dengan class ModelService:

2. Implement functions:
   a) get_confusion_matrix() → dict
      - Return hardcoded confusion matrix values dari presentation:
      {
        'TP': 30,
        'TN': 38,
        'FP': 7,
        'FN': 15
      }
      - Include interpretation untuk tiap value
      
   b) get_metrics() → dict
      - Return model metrics dari presentation:
      {
        'accuracy': 75.6,
        'precision': 81.1,
        'recall': 66.7,
        'f1_score': 73.3,
        'training_samples': 210,
        'testing_samples': 90
      }
      
   c) get_interpretation() → dict
      - Return interpretation text untuk FP & FN
      - Include limitations & caveats

3. Include docstrings
4. Follow PEP 8

Provide lengkap ready-to-use code.
```

**Expected Output:**
- services/model_service.py (ModelService class)

**Testing After:**
```python
from services.model_service import ModelService
model = ModelService()
cm = model.get_confusion_matrix()
metrics = model.get_metrics()
print(cm)
print(metrics)
```

---

### **STEP 2.5: Create Routes - Tab 1 (Peta)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build routes/peta.py sesuai SDD section 3.1:

Requirements:
1. Create routes/peta.py with Flask blueprint atau routes:

2. Implement endpoints:
   a) GET /api/layers/<layer_name>
      - Accept layer_name: 'batas-wilayah', 'gain', 'loss', 'target-2024', 'target-2025'
      - Use GeoService.load_geojson(layer_name)
      - Return response: jsonify(geojson_dict)
      - Error handling: 404 jika layer tidak found
      
   b) GET /map (atau /peta)
      - Return rendered HTML template: 'peta.html'
      - Pass map config: center, zoom_level
      
3. Include docstrings explaining tiap endpoint
4. Include error handling dengan proper HTTP status codes (200, 404, 500)
5. Follow PEP 8

Provide lengkap ready-to-use code.
```

**Expected Output:**
- routes/peta.py (Peta routes)

**Testing After:**
```bash
curl http://localhost:5000/api/layers/gain
# Should return GeoJSON

curl http://localhost:5000/map
# Should return HTML
```

---

### **STEP 2.6: Create Routes - Tab 2 (Data & Proses)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build routes/data_proses.py sesuai SDD section 3.2:

Requirements:
1. Create routes/data_proses.py:

2. Implement endpoints:
   a) GET /api/data/statistics
      - Use GeoService & StatsService
      - Load gain & loss GeoJSON
      - Calculate statistics
      - Return JSON: {gain_ha, loss_ha, percentage_gain, percentage_loss, net_change_ha, net_change_percent}
      
   b) GET /api/data/metadata
      - Return metadata about data sources
      - Include: satellite, period_2024, period_2025, cloud_masking, composite, bands, indexes
      - Values dari SDD section 4.2
      
   c) GET /data (atau /data-proses)
      - Return rendered HTML template: 'data_proses.html'
      
3. Include error handling
4. Include docstrings
5. Follow PEP 8

Provide lengkap ready-to-use code.
```

**Expected Output:**
- routes/data_proses.py (Data & Proses routes)

**Testing After:**
```bash
curl http://localhost:5000/api/data/statistics
# Should return statistics JSON

curl http://localhost:5000/api/data/metadata
# Should return metadata JSON
```

---

### **STEP 2.7: Create Routes - Tab 3 (Evaluasi Model)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build routes/model.py sesuai SDD section 3.3:

Requirements:
1. Create routes/model.py:

2. Implement endpoints:
   a) GET /api/model/metrics
      - Use ModelService.get_metrics()
      - Return JSON: {accuracy, precision, recall, f1_score, training_samples, testing_samples}
      
   b) GET /api/model/confusion-matrix
      - Use ModelService.get_confusion_matrix()
      - Return JSON: {TP, TN, FP, FN, interpretation}
      
   c) GET /model
      - Return rendered HTML template: 'model.html'
      
3. Include error handling
4. Include docstrings
5. Follow PEP 8

Provide lengkap ready-to-use code.
```

**Expected Output:**
- routes/model.py (Model evaluation routes)

**Testing After:**
```bash
curl http://localhost:5000/api/model/metrics
curl http://localhost:5000/api/model/confusion-matrix
```

---

### **STEP 2.8: Create Routes - Tab 4 (Insight Hasil)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build routes/insights.py sesuai SDD section 3.4:

Requirements:
1. Create routes/insights.py:

2. Implement endpoints:
   a) GET /api/insights/summary
      - Calculate summary dari semua data
      - Return JSON: {target_2024_ha, target_2025_ha, gain_ha, loss_ha, net_change_ha, net_change_percent}
      - Values: Target2024=4250, Target2025=3980, Gain=540, Loss=810 (dari presentation)
      
   b) GET /api/insights/spatial
      - Return spatial distribution analysis
      - Include: gain_distribution, loss_distribution
      - Return JSON dengan location, percentage, possible_causes
      
   c) GET /insights
      - Return rendered HTML template: 'insights.html'
      
3. Include error handling
4. Include docstrings
5. Follow PEP 8

Provide lengkap ready-to-use code.
```

**Expected Output:**
- routes/insights.py (Insights routes)

**Testing After:**
```bash
curl http://localhost:5000/api/insights/summary
curl http://localhost:5000/api/insights/spatial
```

---

### **STEP 2.9: Integrate All Routes into app.py**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Update app.py untuk mengintegrasikan semua routes:

Requirements:
1. Import semua routes:
   - from routes.peta import *
   - from routes.data_proses import *
   - from routes.model import *
   - from routes.insights import *

2. Register routes di Flask app:
   - Use app.add_url_rule() atau Blueprint registration
   - Ensure semua endpoints accessible

3. Create __init__.py di routes/ folder untuk organization

4. Test semua endpoints accessible dari app.py

Provide updated app.py lengkap.
```

**Expected Output:**
- Updated app.py dengan all routes integrated

**Testing After (Full Backend Test):**
```bash
python app.py
# Verify all endpoints work:
curl http://localhost:5000/api/layers/batas-wilayah
curl http://localhost:5000/api/data/statistics
curl http://localhost:5000/api/model/metrics
curl http://localhost:5000/api/insights/summary
# All should return valid JSON
```

---

### **STEP 2.10: Backend Code Review & Testing**

**Mode**: PLAN MODE (konsultasi)

**Prompt untuk Claude (Chat):**

```
Review the backend code yang sudah dibangun:

Checklist:
1. ✓ Semua GeoJSON files load tanpa error?
2. ✓ Semua API endpoints return valid JSON?
3. ✓ Error handling implemented?
4. ✓ PEP 8 compliance?
5. ✓ No hardcoded values (menggunakan config.py)?
6. ✓ Docstrings pada semua functions?

Jika ada issues, identify & provide fixes.
Provide final checklist apakah ready for Phase 3.
```

**Expected Outcome:**
- ✅ All backend endpoints working
- ✅ Code review passed
- ✅ Ready to proceed to Phase 3

---

## **PHASE 3: FRONTEND DEVELOPMENT**

### **Duration**: Days 6-8 (3 days)

### **Mode: BUILD MODE**

Pada fase ini Anda membuat HTML/CSS/JavaScript frontend. Gunakan **BUILD MODE** dengan detailed specifications dari SDD.

---

### **STEP 3.1: Create Base Template**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build templates/base.html sesuai SDD section 2.2 - Templates:

Requirements:
1. Create templates/base.html:
   - DOCTYPE HTML5
   - Include Bootstrap 5 CDN
   - Include Leaflet.js CDN
   - Include Plotly.js CDN
   - Navigation bar dengan title "WebGIS Monitoring Deforestasi Kerinci"
   
2. Create tab structure dengan 4 tabs:
   - Tab 1: Peta Hasil
   - Tab 2: Data & Proses
   - Tab 3: Evaluasi Model
   - Tab 4: Insight Hasil
   
3. Use Bootstrap tabs component:
   <ul class="nav nav-tabs">
     <li><a href="#tab1">Tab 1</a></li>
     ...
   </ul>
   <div class="tab-content">
     <div id="tab1" class="tab-pane">...</div>
     ...
   </div>

4. Link to static CSS: /static/css/style.css
5. Include footer dengan credits
6. Make responsive dengan Bootstrap grid
7. Use Jinja2 template syntax

Provide lengkap base.html file.
```

**Expected Output:**
- templates/base.html (Base layout)

---

### **STEP 3.2: Create Tab 1 Template (Peta Hasil)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build templates/peta.html untuk Tab 1:

Requirements:
1. Create templates/peta.html (extend base.html):

2. Include:
   a) Leaflet map container:
      <div id="map" style="height: 600px;"></div>
      
   b) Layer controls:
      - Checkbox untuk "Vegetasi Bertambah (Gain)" - green
      - Checkbox untuk "Vegetasi Berkurang (Loss)" - red
      - Info bahwa Boundary, Target2024, Target2025 always visible
      
   c) Legend:
      - Gray = Batas Wilayah
      - Green = Gain
      - Red = Loss
      - Purple (dashed) = Target 2024
      - Orange (dashed) = Target 2025
      
   d) Info panel untuk feature properties (onclick popup)

3. Include script:
   <script src="/static/js/map.js"></script>

4. Make responsive with Bootstrap

Provide lengkap templates/peta.html file.
```

**Expected Output:**
- templates/peta.html (Map visualization)

---

### **STEP 3.3: Create Tab 2 Template (Data & Proses)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build templates/data_proses.html untuk Tab 2:

Requirements:
1. Create templates/data_proses.html (extend base.html):

2. Include sections:
   a) Data Metadata:
      - Display dari /api/data/metadata
      - Show: Satellite, Period, Cloud Masking, Composite
      
   b) Statistics Section:
      - Display dari /api/data/statistics
      - Show: Luas Gain, Luas Loss, Percentage changes
      - Format dalam cards atau table
      
   c) Processing Workflow Diagram:
      - Visual diagram showing:
        Sentinel-2 → Preprocessing → Ground Truth
        ↓
        Random Forest → Classification → Change Analysis
      - Use SVG atau ASCII art atau text description

3. Use Bootstrap cards untuk layout
4. Include loading spinner (while fetching data)
5. Include error handling (if API fails)
6. Use JavaScript untuk fetch data dari /api/data/*

Provide lengkap templates/data_proses.html file.
```

**Expected Output:**
- templates/data_proses.html (Data & processing info)

---

### **STEP 3.4: Create Tab 3 Template (Evaluasi Model)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build templates/model.html untuk Tab 3:

Requirements:
1. Create templates/model.html (extend base.html):

2. Include sections:
   a) Confusion Matrix (heatmap):
      - Display 2x2 matrix: TP, TN, FP, FN
      - Use Plotly untuk visual heatmap
      - Fetch dari /api/model/confusion-matrix
      
   b) Metrics Display:
      - Show: Accuracy, Precision, Recall, F1-score
      - Format dalam cards dengan large numbers
      - Fetch dari /api/model/metrics
      
   c) Interpretation Section:
      - Explain apa itu True Positive, False Positive, etc
      - Include model limitations (resolution, cloud masking, etc)
      
3. Use Plotly.js untuk visualization
4. Use Bootstrap grid untuk layout
5. Include loading spinner
6. Include error handling

Provide lengkap templates/model.html file.
```

**Expected Output:**
- templates/model.html (Model evaluation)

---

### **STEP 3.5: Create Tab 4 Template (Insight Hasil)**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build templates/insights.html untuk Tab 4:

Requirements:
1. Create templates/insights.html (extend base.html):

2. Include sections:
   a) Summary Statistics (fetch dari /api/insights/summary):
      - Luas Target 2024: 4,250 ha
      - Luas Target 2025: 3,980 ha
      - Gain: 540 ha (+1.27%)
      - Loss: -810 ha (-1.91%)
      - Net Change: -270 ha (-6.35%)
      - Format dalam cards
      
   b) Spatial Distribution (fetch dari /api/insights/spatial):
      - Gain location & percentage
      - Loss location & percentage
      - Possible causes
      
   c) Key Insights:
      - Largest changes area
      - Trends & patterns
      
   d) Recommendations:
      - Multi-tahun analysis suggestions
      - Sosial-ekonomi integration ideas
      - Monitoring framework

3. Use Bootstrap for layout
4. Use icons untuk visual appeal
5. Include loading spinner
6. Include error handling

Provide lengkap templates/insights.html file.
```

**Expected Output:**
- templates/insights.html (Insights & recommendations)

---

### **STEP 3.6: Create Custom CSS**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build static/css/style.css dengan custom styling:

Requirements:
1. Create static/css/style.css:

2. Include styles untuk:
   a) Navbar:
      - Dark background, white text
      - Padding & spacing
      
   b) Tab styling:
      - Active tab highlighted
      - Nice transition effects
      
   c) Map container:
      - Full width, proper height
      - Border & shadow
      
   d) Cards:
      - Consistent spacing
      - Nice hover effects
      
   e) Statistics display:
      - Large font for numbers
      - Color-coded (gain=green, loss=red, etc)
      
   f) Responsive design:
      - Mobile-first approach
      - Adjust font sizes untuk mobile
      
   g) Legend:
      - Color swatches
      - Clear labels

3. Use CSS variables untuk colors
4. Make it visually appealing tapi professional
5. Ensure accessibility (good contrast, readable fonts)

Provide lengkap static/css/style.css file.
```

**Expected Output:**
- static/css/style.css (Custom styling)

---

### **STEP 3.7: Create Leaflet Map JavaScript**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build static/js/map.js untuk Leaflet map initialization:

Requirements:
1. Create static/js/map.js:

2. Implement functions:
   a) initializeMap():
      - Create Leaflet map dengan center [-0.42, 101.27]
      - Zoom level 10
      - Add OpenStreetMap tile layer
      - Store map reference globally
      
   b) loadLayers():
      - Fetch '/api/layers/batas-wilayah' & add to map
      - Fetch & add Target2024 (purple dashed)
      - Fetch & add Target2025 (orange dashed)
      - Create toggleable layers (Gain/Loss)
      - Add layer control untuk user to toggle
      
   c) setupLayerControls():
      - Add checkbox untuk Gain (green)
      - Add checkbox untuk Loss (red)
      - Toggle visibility on checkbox change
      
   d) addPopups():
      - On feature click, show properties
      - Include: area_ha, periode, etc
      
   e) addLegend():
      - Create legend showing colors
      - Explain tiap color meaning

3. Include error handling (API failure, invalid GeoJSON)
4. Include docstrings
5. Use vanilla JavaScript atau minimal jQuery

Provide lengkap static/js/map.js file.
```

**Expected Output:**
- static/js/map.js (Map functionality)

---

### **STEP 3.8: Create Charts JavaScript**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build static/js/charts.js untuk Plotly chart visualization:

Requirements:
1. Create static/js/charts.js:

2. Implement functions:
   a) renderConfusionMatrix(data):
      - Create 2x2 heatmap using Plotly
      - Data format: {TP, TN, FP, FN}
      - Render in element: #confusion-matrix
      
   b) renderMetricsCards(data):
      - Display metrics dalam cards
      - Data format: {accuracy, precision, recall, f1_score}
      - Large font numbers
      
   c) renderStatistics(data):
      - Display summary stats
      - Data format: {target_2024_ha, target_2025_ha, gain_ha, loss_ha, ...}
      - Color code: gain=green, loss=red
      
   d) renderBarChart(label, value):
      - Generic bar chart function
      - Used for metrics display

3. Include error handling
4. Include docstrings
5. Use Plotly.js CDN (already in base.html)

Provide lengkap static/js/charts.js file.
```

**Expected Output:**
- static/js/charts.js (Chart rendering)

---

### **STEP 3.9: Create API Client JavaScript**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build static/js/api-client.js untuk HTTP API calls:

Requirements:
1. Create static/js/api-client.js:

2. Implement fetch wrapper functions:
   a) getLayer(layerName):
      - Fetch '/api/layers/{layerName}'
      - Return JSON
      
   b) getStatistics():
      - Fetch '/api/data/statistics'
      - Return JSON
      
   c) getMetadata():
      - Fetch '/api/data/metadata'
      - Return JSON
      
   d) getMetrics():
      - Fetch '/api/model/metrics'
      - Return JSON
      
   e) getConfusionMatrix():
      - Fetch '/api/model/confusion-matrix'
      - Return JSON
      
   f) getInsightsSummary():
      - Fetch '/api/insights/summary'
      - Return JSON
      
   g) getInsightsSpatial():
      - Fetch '/api/insights/spatial'
      - Return JSON

3. Include error handling:
   - Log errors to console
   - Return error message to caller
   - Show user-friendly error dialog

4. Include docstrings explaining tiap function
5. Use async/await syntax
6. Follow ES6 conventions

Provide lengkap static/js/api-client.js file.
```

**Expected Output:**
- static/js/api-client.js (API client wrapper)

---

### **STEP 3.10: Create Index/Landing Page**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Build templates/index.html sebagai landing page:

Requirements:
1. Create templates/index.html:
   - Simple landing page
   - Title: "WebGIS Monitoring Deforestasi Kerinci"
   - Brief description
   - Button to go to main app
   - Links to documentation (GitHub, etc)

2. Or create single-page app:
   - index.html redirect ke /map
   - OR merge all tabs dalam single page

Choose option yang lebih sederhana.

Provide templates/index.html file.
```

**Expected Output:**
- templates/index.html (Landing page)

---

## **PHASE 4: INTEGRATION & TESTING**

### **Duration**: Days 9-10 (2 days)

### **Mode: BUILD MODE + Manual Testing**

---

### **STEP 4.1: Full Integration Testing**

**Mode**: PLAN MODE

**Prompt untuk Claude (Chat):**

```
Create testing checklist untuk memastikan frontend ↔ backend integration:

Provide checklist untuk:
1. Page load & rendering
2. Map functionality
3. Layer toggles
4. Statistics display
5. Model metrics display
6. Insights display
7. API error handling
8. Mobile responsiveness
9. Cross-browser compatibility

Format sebagai markdown checklist yang bisa dijalankan.
```

**Expected Output:**
- Detailed testing checklist

**Manual Testing:**
```bash
# 1. Start backend
python app.py

# 2. Open browser
http://localhost:5000/

# 3. Run through checklist
# ... (validate each point)

# 4. Check browser console
# - No JavaScript errors
# - No CORS issues
# - API calls successful
```

---

### **STEP 4.2: Debug & Fix Issues**

**Mode**: BUILD MODE (as needed)

**Prompt untuk Claude (Code) if issues found:**

```
Debug the issue:

Error: [describe the error]
Location: [where it occurs]
Steps to reproduce: [steps]

Expected behavior: [what should happen]
Actual behavior: [what's happening]

Provide fix code immediately.
```

**Common Issues & Solutions:**

| **Issue** | **Cause** | **Fix** |
|---|---|---|
| Map not showing | API endpoint 404 | Check route is defined in app.py |
| CORS error | Backend not allowing origin | Add Flask-CORS to app |
| GeoJSON not rendering | Invalid GeoJSON format | Validate GeoJSON with geojsonlint.com |
| Chart not showing | API response error | Check API endpoint returns valid JSON |
| Statistics wrong | Calculation error | Verify geo_service.calculate_area_ha() |

---

### **STEP 4.3: Performance Optimization**

**Mode**: PLAN MODE

**Prompt untuk Claude (Chat):**

```
Review performance & provide optimization suggestions:

Analyze:
1. Page load time (target < 3s)
2. API response time (target < 500ms)
3. Map rendering time (target < 1s)
4. JavaScript bundle size

Provide recommendations untuk improvement (if needed).
```

---

## **PHASE 5: DEPLOYMENT**

### **Duration**: Day 11 (1 day)

### **Mode: BUILD MODE + Manual Configuration**

---

### **STEP 5.1: Prepare Deployment Files**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Create deployment configuration files:

Requirements:
1. Create Procfile:
   web: gunicorn app:app

2. Create render.yaml:
   services:
     - type: web
       name: webgis-deforestasi
       env: python
       plan: free
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app:app
       envVars:
         - key: PYTHON_VERSION
           value: 3.11
         - key: FLASK_ENV
           value: production
         - key: PORT
           value: 10000

3. Create .gitignore:
   __pycache__/
   *.pyc
   venv/
   .env
   .DS_Store

4. Create .env.example:
   FLASK_ENV=development
   DEBUG=True

Provide semua files lengkap.
```

**Expected Output:**
- Procfile
- render.yaml
- .gitignore
- .env.example

---

### **STEP 5.2: GitHub Setup & Push**

**Mode**: Manual

**Steps:**
```bash
# 1. Initialize Git (if not already)
git init
git add .
git commit -m "Initial commit - WebGIS Deforestasi"

# 2. Create GitHub repo:
# Visit github.com → New Repository
# Name: webgis-deforestasi
# Description: WebGIS Monitoring Deforestasi Kerinci
# Public
# Create repository

# 3. Connect local repo to GitHub
git remote add origin https://github.com/username/webgis-deforestasi
git branch -M main
git push -u origin main

# 4. Verify
# Visit https://github.com/username/webgis-deforestasi
# Should see all files
```

---

### **STEP 5.3: Render Deployment**

**Mode**: Manual

**Steps:**
```
1. Visit render.com → Login/Create account

2. Click "New +" → "Web Service"

3. Connect GitHub:
   - Click "Connect a repository"
   - Authorize GitHub
   - Select "webgis-deforestasi" repo
   - Click "Connect"

4. Configure service:
   - Name: webgis-deforestasi
   - Environment: Python 3
   - Build command: pip install -r requirements.txt
   - Start command: gunicorn app:app
   - Plan: Free

5. Click "Create Web Service"

6. Wait for deployment:
   - Build process will start automatically
   - Check logs for errors
   - Once deployed, get live URL

7. Visit live URL:
   https://webgis-deforestasi.onrender.com
   
   Should see:
   - Home page loads
   - All tabs accessible
   - Map displays
   - No errors
```

---

### **STEP 5.4: Post-Deployment Verification**

**Mode**: Manual Testing

**Verification Checklist:**
- [ ] Website loads (no 404)
- [ ] All tabs accessible
- [ ] Map displays with all layers
- [ ] Gain/Loss toggle works
- [ ] Statistics display correctly
- [ ] Model metrics show
- [ ] Insights populated
- [ ] No console errors
- [ ] HTTPS working
- [ ] Responsive on mobile

---

### **STEP 5.5: Documentation**

**Mode**: BUILD MODE

**Prompt untuk Claude (Code):**

```
Create documentation files:

1. Create README.md:
   - Project title & description
   - Features list
   - Tech stack
   - Setup instructions (for local dev)
   - Deployment instructions
   - API documentation
   - Screenshots (optional)
   - Author & credits

2. Create docs/API.md:
   - All API endpoints
   - Request/response examples
   - Error codes

3. Create docs/SETUP.md:
   - Development environment setup
   - Running locally
   - Testing instructions

4. Create docs/DEPLOYMENT.md:
   - Render deployment steps
   - Environment variables
   - Monitoring & logs

Provide lengkap all documentation files.
```

**Expected Output:**
- README.md
- docs/API.md
- docs/SETUP.md
- docs/DEPLOYMENT.md

---

## **MODE DECISION TREE**

```
                        START
                          ↓
                    [NEW TASK?]
                      /       \
                    NO         YES
                    ↓           ↓
              [CLEAR SPEC?]    [NEED DESIGN?]
                /     \          /     \
              NO       YES       YES     NO
              ↓         ↓        ↓       ↓
         [PLAN MODE] [BUILD?]  [PLAN]  [BUILD]
              ↓         ↓       MODE    MODE
           Design   [BUILD          ↓
           &        MODE]      Explain &
           Detail      ↓       Design
              ↓      Code
           Return   Ready
           to       ↓
           BUILD   Done
           MODE


SUMMARY:
========

🟡 PLAN MODE:
   - Before you know WHAT to build
   - Answer: "What?" & "How?" (conceptual)
   - Output: Design, explanation, strategy
   
🟢 BUILD MODE:
   - When you know WHAT to build
   - Answer: "Build it!" (implementation)
   - Output: Actual code files
```

---

## **QUICK REFERENCE: WHEN TO USE WHAT?**

| **Situation** | **Use** | **Example** |
|---|---|---|
| "Explain the tech stack" | PLAN | Getting overview |
| "Break down the architecture" | PLAN | Understanding design |
| "Create app.py" | BUILD | Ready to implement |
| "Fix the bug" | BUILD | Debugging |
| "How do I deploy?" | PLAN | Understanding process |
| "Deploy to Render" | Manual | Hands-on action |
| "Review the code" | PLAN | Quality assurance |
| "Optimize the map" | BUILD | Performance tuning |

---

## **REVISION HISTORY**

| **Version** | **Date** | **Author** | **Changes** |
|---|---|---|---|
| 1.0 | 16 July 2026 | Claude | Initial WORKFLOW_PROMPTS creation |

---

**Document Owner**: Hans  
**Last Updated**: 16 July 2026  
**Status**: READY FOR EXECUTION
