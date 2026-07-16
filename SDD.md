# SDD: WebGIS Monitoring Deforestasi Kerinci
**Software Design Document**  
**Version**: 1.0  
**Created**: July 2026  
**Status**: In Development

---

## **1. SYSTEM ARCHITECTURE**

### **1.1 High-Level Architecture**

```
┌─────────────────────────────────────────────────────┐
│         CLIENT TIER (Browser)                       │
│  HTML5 + Bootstrap 5 + Leaflet.js + Plotly.js     │
│  - Peta Hasil (Tab 1)                              │
│  - Data & Proses (Tab 2)                           │
│  - Evaluasi Model (Tab 3)                          │
│  - Insight Hasil (Tab 4)                           │
└────────────────┬────────────────────────────────────┘
                 │ HTTP/HTTPS
                 ↓
┌─────────────────────────────────────────────────────┐
│    APPLICATION TIER (Render.com)                   │
│         Flask 2.3 + Gunicorn                       │
│                                                     │
│  ┌─────────────────────────────────────┐           │
│  │  routes/                            │           │
│  │  ├─ peta.py (Tab 1 endpoints)      │           │
│  │  ├─ data_proses.py (Tab 2)         │           │
│  │  ├─ model.py (Tab 3)               │           │
│  │  └─ insights.py (Tab 4)            │           │
│  └─────────────────────────────────────┘           │
│                                                     │
│  ┌─────────────────────────────────────┐           │
│  │  services/                          │           │
│  │  ├─ geo_service.py (GeoJSON ops)   │           │
│  │  ├─ stats_service.py (Calculations)│           │
│  │  └─ model_service.py (Model inferv)│           │
│  └─────────────────────────────────────┘           │
└────────────────┬────────────────────────────────────┘
                 │
         ┌───────┴─────────┐
         ↓                 ↓
┌──────────────────┐  ┌──────────────────┐
│   DATA TIER      │  │  MODEL TIER      │
│   (/data/)       │  │  (/models/)      │
│                  │  │                  │
│ GeoJSON Files:   │  │ Trained Models:  │
│ - BatasWilayah   │  │ - RF_2024.pkl    │
│ - Gain           │  │ - RF_2025.pkl    │
│ - Loss           │  │                  │
│ - Target2024     │  │                  │
│ - Target2025     │  │                  │
└──────────────────┘  └──────────────────┘
```

### **1.2 Technology Stack**

| **Layer** | **Technology** | **Version** |
|---|---|---|
| **Frontend** | HTML5, CSS3 (Bootstrap 5), JavaScript (ES6) | Latest |
| **Map Library** | Leaflet.js + GeoJSON support | v1.9.4 |
| **Chart Library** | Plotly.js | v2.26.0 |
| **Backend** | Flask | v2.3.0 |
| **WSGI Server** | Gunicorn | v21.0.0 |
| **Geospatial** | GeoPandas, Shapely | v0.12.0, v2.0.0 |
| **Data Processing** | Pandas, NumPy | v2.0.0, v1.24.0 |
| **ML** | scikit-learn | v1.3.0 |
| **Server** | Render.com (Free) | Python 3.11 |
| **Version Control** | Git + GitHub | Latest |

---

## **2. SYSTEM COMPONENTS**

### **2.1 Directory Structure**

```
webgis-deforestasi/                    ← Root (GitHub repo)
│
├── .gitignore                         ← Exclude sensitive files
├── .env.example                       ← Config template (no secrets)
├── requirements.txt                   ← Python dependencies
├── Procfile                           ← Gunicorn startup
├── render.yaml                        ← Render deployment config
├── config.py                          ← App configuration
├── app.py                             ← Flask main application
│
├── data/                              ← ⭐ ALL GEOJSON FILES
│   ├── UAS_Kerinci_BatasWilayah.geojson
│   ├── UAS_Kerinci_Gain.geojson
│   ├── UAS_Kerinci_Loss.geojson
│   ├── UAS_Kerinci_Target2024.geojson
│   ├── UAS_Kerinci_Target2025.geojson
│   └── config.json                    ← Metadata (optional)
│
├── models/                            ← ⭐ PRE-TRAINED MODELS
│   ├── random_forest_2024.pkl
│   └── random_forest_2025.pkl
│
├── routes/                            ← Backend API endpoints
│   ├── __init__.py
│   ├── peta.py                       # Tab 1: Peta Hasil
│   ├── data_proses.py                # Tab 2: Data & Proses
│   ├── model.py                      # Tab 3: Evaluasi Model
│   └── insights.py                   # Tab 4: Insight Hasil
│
├── services/                          ← Business logic
│   ├── __init__.py
│   ├── geo_service.py                # GeoJSON operations
│   ├── stats_service.py              # Statistical calculations
│   └── model_service.py              # Model inference
│
├── templates/                         ← Frontend HTML (Jinja2)
│   ├── base.html                     # Base layout + navbar
│   ├── index.html                    # Home/landing page
│   ├── peta.html                     # Tab 1 template
│   ├── data_proses.html              # Tab 2 template
│   ├── model.html                    # Tab 3 template
│   └── insights.html                 # Tab 4 template
│
├── static/                            ← Frontend assets
│   ├── css/
│   │   ├── bootstrap.min.css         # Bootstrap CSS (CDN alternative)
│   │   └── style.css                 # Custom styling
│   └── js/
│       ├── leaflet.min.js            # Leaflet library (CDN alternative)
│       ├── plotly.min.js             # Plotly library (CDN alternative)
│       ├── map.js                    # Map initialization & control
│       ├── charts.js                 # Chart rendering logic
│       └── api-client.js             # Fetch API wrapper
│
├── tests/                             ← Unit tests (optional Phase 2)
│   ├── test_geo_service.py
│   └── test_stats_service.py
│
└── docs/                              ← Documentation
    ├── API.md                        # API endpoint documentation
    ├── SETUP.md                      # Local development setup
    └── DEPLOYMENT.md                 # Deployment guide
```

### **2.2 Component Descriptions**

#### **A. app.py (Flask Application)**
```python
"""
Main Flask application
- Initialize Flask app
- Register blueprints (routes)
- Configure static/template paths
- Error handlers
"""
```

#### **B. config.py (Configuration)**
```python
"""
Environment-specific configuration
- Development/Production settings
- File paths (data/, models/, templates/)
- Constants (map center, zoom level, etc)
"""
```

#### **C. routes/ (API Endpoints)**

**peta.py** (Tab 1: Peta Hasil)
```python
@app.route('/api/layers/<layer_name>')           # Get GeoJSON layer
@app.route('/map')                               # Map page
```

**data_proses.py** (Tab 2: Data & Proses)
```python
@app.route('/api/data/statistics')               # Luas gain/loss
@app.route('/api/data/metadata')                 # Data source info
@app.route('/data')                              # Data page
```

**model.py** (Tab 3: Evaluasi Model)
```python
@app.route('/api/model/metrics')                 # Accuracy, Precision, etc
@app.route('/api/model/confusion-matrix')        # Confusion matrix values
@app.route('/model')                             # Model evaluation page
```

**insights.py** (Tab 4: Insight Hasil)
```python
@app.route('/api/insights/summary')              # Summary statistics
@app.route('/api/insights/spatial')              # Spatial analysis
@app.route('/insights')                          # Insights page
```

#### **D. services/ (Business Logic)**

**geo_service.py**
```python
"""
Geospatial operations
- load_geojson(filename) → Load from /data/ folder
- calculate_area(gdf) → Calculate area in hectares
- get_feature_properties(gdf, feature_id) → Get feature details
"""
```

**stats_service.py**
```python
"""
Statistical calculations
- calculate_gain_loss_stats() → Total gain/loss areas
- calculate_percentages() → Percentage changes
- calculate_spatial_distribution() → Where changes occur
"""
```

**model_service.py**
```python
"""
ML model operations
- load_model(model_path) → Load pre-trained RF model
- get_confusion_matrix() → Return CM values
- get_metrics() → Return accuracy, precision, recall, f1
"""
```

#### **E. templates/ (Frontend HTML)**

All templates extend **base.html** with Bootstrap tab structure:

```html
<!-- base.html -->
<nav class="navbar">
  <h1>WebGIS Monitoring Deforestasi Kerinci</h1>
</nav>

<ul class="nav nav-tabs">
  <li><a href="#tab1" class="nav-link">Peta Hasil</a></li>
  <li><a href="#tab2" class="nav-link">Data & Proses</a></li>
  <li><a href="#tab3" class="nav-link">Evaluasi Model</a></li>
  <li><a href="#tab4" class="nav-link">Insight Hasil</a></li>
</ul>

<div class="tab-content">
  {% include 'peta.html' %}
  {% include 'data_proses.html' %}
  {% include 'model.html' %}
  {% include 'insights.html' %}
</div>
```

#### **F. static/ (Frontend Assets)**

**map.js** - Leaflet initialization
```javascript
// Initialize map
// Load GeoJSON layers
// Setup layer controls (toggle gain/loss)
// Add popups on feature click
// Add legend
```

**charts.js** - Plotly visualization
```javascript
// Render confusion matrix as heatmap
// Render metrics as bar/gauge charts
// Render statistics as cards/tables
```

**api-client.js** - HTTP wrapper
```javascript
// Wrapper functions for fetch API
// async getLayer(name)
// async getStatistics()
// async getMetrics()
// Error handling
```

---

## **3. API DESIGN**

### **3.1 API Endpoints**

#### **TAB 1: Peta Hasil**

| **Method** | **Endpoint** | **Description** | **Response** |
|---|---|---|---|
| GET | `/api/layers/<layer_name>` | Get GeoJSON layer | GeoJSON FeatureCollection |
| GET | `/map` | Map HTML page | HTML |

**Supported layer_name values:**
- `batas-wilayah` → UAS_Kerinci_BatasWilayah.geojson
- `gain` → UAS_Kerinci_Gain.geojson
- `loss` → UAS_Kerinci_Loss.geojson
- `target-2024` → UAS_Kerinci_Target2024.geojson
- `target-2025` → UAS_Kerinci_Target2025.geojson

**Example Request/Response:**
```bash
GET /api/layers/gain

# Response
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Polygon", "coordinates": [...]},
      "properties": {
        "area_ha": 1234.5,
        "percentage": 2.34
      }
    }
  ]
}
```

---

#### **TAB 2: Data & Proses**

| **Method** | **Endpoint** | **Description** | **Response** |
|---|---|---|---|
| GET | `/api/data/statistics` | Luas gain/loss & percentages | JSON |
| GET | `/api/data/metadata` | Data source info | JSON |
| GET | `/data` | Data page HTML | HTML |

**Example Response (statistics):**
```json
{
  "gain_ha": 540.25,
  "loss_ha": 810.75,
  "total_area": 1351.0,
  "percentage_gain": 39.94,
  "percentage_loss": 60.06,
  "net_change_ha": -270.5,
  "net_change_percent": -6.35
}
```

**Example Response (metadata):**
```json
{
  "satellite": "Sentinel-2 COPERNICUS/S2_SR_HARMONIZED",
  "period_2024": "01 Jan - 31 Des 2024",
  "period_2025": "01 Jan - 31 Des 2025",
  "cloud_masking": "S2 Cloud Probability + SCL",
  "composite": "Median Composite",
  "bands": ["B2", "B3", "B4", "B8", "B11", "B12"],
  "indexes": ["NDVI", "NDMI", "NDBI"]
}
```

---

#### **TAB 3: Evaluasi Model**

| **Method** | **Endpoint** | **Description** | **Response** |
|---|---|---|---|
| GET | `/api/model/metrics` | Accuracy, Precision, Recall, F1 | JSON |
| GET | `/api/model/confusion-matrix` | TP, TN, FP, FN values | JSON |
| GET | `/model` | Model evaluation page HTML | HTML |

**Example Response (metrics):**
```json
{
  "accuracy": 75.6,
  "precision": 81.1,
  "recall": 66.7,
  "f1_score": 73.3,
  "training_samples": 210,
  "testing_samples": 90
}
```

**Example Response (confusion-matrix):**
```json
{
  "TP": 30,
  "TN": 38,
  "FP": 7,
  "FN": 15,
  "interpretation": {
    "true_positive": "Model correctly identified target",
    "false_positive": "Model incorrectly predicted target (overprediction)",
    "false_negative": "Model missed actual target (underprediction)"
  }
}
```

---

#### **TAB 4: Insight Hasil**

| **Method** | **Endpoint** | **Description** | **Response** |
|---|---|---|---|
| GET | `/api/insights/summary` | Summary statistics | JSON |
| GET | `/api/insights/spatial` | Spatial distribution analysis | JSON |
| GET | `/insights` | Insights page HTML | HTML |

**Example Response (summary):**
```json
{
  "target_2024_ha": 4250.0,
  "target_2025_ha": 3980.0,
  "gain_ha": 540.0,
  "loss_ha": 810.0,
  "net_change_ha": -270.0,
  "net_change_percent": -6.35,
  "largest_change_area": "Eastern part of city"
}
```

**Example Response (spatial):**
```json
{
  "gain_distribution": {
    "location": "Timur",
    "percentage": 60,
    "possible_causes": ["Reforestation", "Land recovery"]
  },
  "loss_distribution": {
    "location": "Barat & Tengah",
    "percentage": 40,
    "possible_causes": ["Urban expansion", "Agricultural conversion"]
  }
}
```

---

### **3.2 Error Handling**

```python
# All endpoints return proper HTTP status codes

200 OK          # Success
400 Bad Request # Invalid parameters
404 Not Found   # Layer/endpoint not found
500 Internal Server Error # Server error

# Example error response:
{
  "error": "Layer 'invalid_layer' not found",
  "status": 404,
  "timestamp": "2026-07-16T10:30:00Z"
}
```

---

## **4. DATA FLOW**

### **4.1 Layer Loading Flow**

```
User clicks "Map" tab
    ↓
JavaScript: loadLayers()
    ↓
fetch('/api/layers/batas-wilayah')
    ↓
Backend: get_layer('batas-wilayah')
    ↓
GeoService: load_geojson('batas-wilayah')
    ↓
GeoPandas: read_file('data/UAS_Kerinci_BatasWilayah.geojson')
    ↓
Convert to JSON: gdf.to_json()
    ↓
Response: GeoJSON FeatureCollection
    ↓
JavaScript: L.geoJSON(data).addTo(map)
    ↓
Leaflet renders layer on map
```

### **4.2 Statistics Calculation Flow**

```
User views Tab 2
    ↓
fetch('/api/data/statistics')
    ↓
Backend: get_statistics()
    ↓
GeoService: load_geojson('gain') & load_geojson('loss')
    ↓
Calculate: gdf.geometry.area.sum() / 10000 (convert to hectares)
    ↓
StatsService: calculate_percentages(gain_area, loss_area)
    ↓
Response: JSON with all calculated values
    ↓
JavaScript: Render in HTML cards/tables
```

---

## **5. DATABASE DESIGN**

### **5.1 Data Storage (MVP - No Database)**

For Phase 1 (MVP), data is stored as static GeoJSON files:

```
/data/
├── UAS_Kerinci_BatasWilayah.geojson  (Binary spatial geometry)
├── UAS_Kerinci_Gain.geojson
├── UAS_Kerinci_Loss.geojson
├── UAS_Kerinci_Target2024.geojson
├── UAS_Kerinci_Target2025.geojson
└── config.json                       (Metadata)
```

**Advantages:**
- ✅ No database setup needed
- ✅ Fast loading (GeoJSON cached in memory)
- ✅ Easy version control with Git

**Disadvantages:**
- ❌ Not suitable for real-time data updates
- ❌ Limited query capabilities
- ❌ All data loaded into memory

### **5.2 Optional Phase 2: PostgreSQL + PostGIS**

For future enhancement (if needed):

```sql
-- GIS-enabled database schema
CREATE TABLE boundaries (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  geom GEOMETRY(Polygon, 4326)
);

CREATE TABLE forest_changes (
  id SERIAL PRIMARY KEY,
  change_type VARCHAR(50),  -- 'gain' or 'loss'
  area_ha DECIMAL(10, 2),
  year INTEGER,
  geom GEOMETRY(Polygon, 4326)
);

CREATE INDEX idx_forest_geom ON forest_changes USING GIST(geom);
```

---

## **6. SECURITY DESIGN**

### **6.1 Current Security (MVP)**

- ✅ HTTPS enforced by Render.com
- ✅ No sensitive data in GeoJSON files
- ✅ Read-only access (no POST/PUT/DELETE endpoints)
- ✅ No authentication needed (public dashboard)

### **6.2 Potential Future Enhancements**

- Add user authentication (if editing allowed)
- API rate limiting (prevent abuse)
- Input validation on all endpoints
- CSRF protection if forms added

---

## **7. PERFORMANCE DESIGN**

### **7.1 Frontend Optimization**

```javascript
// Lazy loading
<script defer src="static/js/map.js"></script>

// GeoJSON caching
const cache = {};
if (!cache['gain']) {
  cache['gain'] = await fetch('/api/layers/gain').then(r => r.json());
}

// Layer toggling (not reload)
gainLayer.setOpacity(show ? 0.5 : 0);
```

### **7.2 Backend Optimization**

```python
# Load GeoJSON at app startup (not per request)
geojson_cache = {
    'batas-wilayah': load_geojson('batas-wilayah'),
    'gain': load_geojson('gain'),
    # ...
}

# Return cached data (fast)
@app.route('/api/layers/<layer>')
def get_layer(layer):
    return jsonify(geojson_cache[layer])
```

### **7.3 Target Performance Metrics**

| **Metric** | **Target** | **Method** |
|---|---|---|
| Page Load | < 3s | CDN for libraries + cached GeoJSON |
| API Response | < 500ms | Cached data, no DB queries |
| Map Rendering | < 1s | Leaflet optimization |
| Memory Usage | < 100MB | Static files only |

---

## **8. DEPLOYMENT ARCHITECTURE**

### **8.1 Render.com Deployment**

```yaml
# render.yaml
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
    
    repo: https://github.com/username/webgis-deforestasi
    branch: main
    
    healthCheckPath: /
    autoDeploy: true
```

### **8.2 Deployment Flow**

```
1. Developer pushes to GitHub
   git push origin main

2. GitHub webhook triggers Render

3. Render executes:
   - Pull latest code
   - pip install -r requirements.txt
   - gunicorn app:app

4. Application live at:
   https://webgis-deforestasi.onrender.com

5. Auto-HTTPS & monitoring enabled
```

---

## **9. SYSTEM REQUIREMENTS**

### **9.1 Client (Browser)**

- Chrome, Firefox, Safari (latest 2 versions)
- JavaScript enabled
- Min. 2GB RAM (for map rendering)
- Internet connection

### **9.2 Development Environment**

- Python 3.11+
- Git 2.25+
- VS Code / PyCharm
- ~500MB disk space

### **9.3 Production (Render.com)**

- Provided by Render (Python 3.11, Gunicorn, HTTPS)
- Automatic load balancing
- 512MB RAM (free tier)

---

## **10. TESTING STRATEGY**

### **10.1 Unit Tests (Phase 2 - Optional)**

```python
# tests/test_geo_service.py
def test_load_geojson():
    gdf = load_geojson('gain')
    assert gdf is not None
    assert 'geometry' in gdf.columns

def test_calculate_area():
    gdf = load_geojson('loss')
    area = calculate_area(gdf)
    assert area > 0

# tests/test_stats_service.py
def test_statistics_endpoint(client):
    response = client.get('/api/data/statistics')
    assert response.status_code == 200
    assert 'gain_ha' in response.json
```

### **10.2 Manual Testing Checklist**

- [ ] Map loads all layers without errors
- [ ] Layer toggle works (Gain/Loss)
- [ ] Popup shows on feature click
- [ ] Tab navigation works smoothly
- [ ] Statistics calculated correctly
- [ ] Model metrics displayed
- [ ] Responsive on mobile
- [ ] No console errors

---

## **11. MAINTAINABILITY & SCALABILITY**

### **11.1 Code Organization**

- Modular routes (one file per tab)
- Separated business logic (services/)
- Reusable components (templates/)
- Clear naming conventions (snake_case)

### **11.2 Future Enhancements (Phase 2+)**

- Add PostgreSQL + PostGIS for spatial queries
- Implement real-time Sentinel-2 data updates
- Add user authentication & multi-user support
- Advanced GIS tools (buffer, clip, merge)
- Mobile app (React Native)

---

## **12. REVISION HISTORY**

| **Version** | **Date** | **Author** | **Changes** |
|---|---|---|---|
| 1.0 | 16 July 2026 | Hans | Initial SDD creation |

---

**Document Owner**: Hans  
**Last Updated**: 16 July 2026  
**Status**: APPROVED FOR IMPLEMENTATION
