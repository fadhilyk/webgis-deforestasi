# AGENTS.md: Team Structure & Coordination Guide
**WebGIS Monitoring Deforestasi Kerinci**  
**Version**: 1.0  
**Created**: 16 July 2026  
**Status**: Active

---

## **1. TEAM COMPOSITION**

### **1.1 Team Members**

| **Role** | **Person** | **Responsibility** | **Tech Stack** |
|---|---|---|---|
| **Project Lead & Coordinator** | Hans | Overall project management, requirements, design decisions | - |
| **Code Agent (Backend)** | Claude (Code) | Flask backend, API development, services layer | Python, Flask, GeoPandas |
| **Code Agent (Frontend)** | Claude (Code) | HTML/CSS/JS templates, Leaflet map, UI/UX | HTML5, Bootstrap 5, Leaflet.js, JavaScript |
| **Advisor & Documentation** | Claude (Chat) | Documentation, PRD/SDD/Prompts, guidance | Markdown |

---

## **2. COMMUNICATION PROTOCOL**

### **2.1 Mode of Operation**

**PLAN MODE** (Design & Strategy)
- When: Before coding starts, for major architectural decisions
- Who: Hans consults with Claude (Chat)
- Output: Documentation, architectural diagrams, step-by-step plans
- Example: "Breakdown the tech stack", "Create a detailed design", "Plan the workflow"

**BUILD MODE** (Actual Development)
- When: Implementing actual code
- Who: Hans instructs Claude (Code) to build specific components
- Output: Code files, unit tests, implementation
- Example: "Build the Flask app", "Create API endpoints", "Build Tab 1 frontend"

**COORDINATE MODE** (Integration)
- When: Combining backend + frontend
- Who: Hans coordinates between backend & frontend agents
- Output: Integrated, tested application
- Example: "Make sure API response matches frontend expectations"

### **2.2 Documentation Exchange**

All critical information stored in GitHub repo:

```
webgis-deforestasi/
├── PRD.md                  ← Requirements
├── SDD.md                  ← Technical design
├── AGENTS.md               ← This file (coordination)
├── WORKFLOW_PROMPTS.md     ← Step-by-step build instructions
├── README.md               ← Setup & usage
└── docs/
    ├── API.md             ← Endpoint documentation
    ├── SETUP.md           ← Dev environment setup
    └── DEPLOYMENT.md      ← Deploy to Render
```

---

## **3. PROJECT PHASES & RESPONSIBILITIES**

### **3.1 PHASE 1: Planning & Documentation (Days 1-2)**

| **Task** | **Owner** | **Deliverable** | **Status** |
|---|---|---|---|
| Create PRD | Hans + Claude (Chat) | PRD.md ✅ | ✅ DONE |
| Create SDD | Hans + Claude (Chat) | SDD.md ✅ | ✅ DONE |
| Create AGENTS.md | Claude (Chat) | AGENTS.md ✅ | ✅ DONE |
| Create WORKFLOW_PROMPTS.md | Claude (Chat) | WORKFLOW_PROMPTS.md | 🟡 IN PROGRESS |

**Entry Criteria:**
- ✅ Requirements finalized (PRD approved)
- ✅ Technical design finalized (SDD approved)

**Exit Criteria:**
- ✅ All documentation reviewed by Hans
- ✅ WORKFLOW_PROMPTS.md ready
- ✅ GitHub repo initialized with all docs

---

### **3.2 PHASE 2: Backend Development (Days 3-5)**

| **Task** | **Agent** | **Files** | **Est. Time** |
|---|---|---|---|
| Setup Flask app structure | Claude (Code) | app.py, config.py | 0.5 day |
| Create services/ layer | Claude (Code) | geo_service.py, stats_service.py, model_service.py | 1 day |
| Create routes/peta.py | Claude (Code) | routes/peta.py | 0.5 day |
| Create routes/data_proses.py | Claude (Code) | routes/data_proses.py | 0.5 day |
| Create routes/model.py | Claude (Code) | routes/model.py | 0.5 day |
| Create routes/insights.py | Claude (Code) | routes/insights.py | 0.5 day |
| Test all endpoints locally | Claude (Code) | Test scripts | 0.5 day |

**Test Endpoints (Before Frontend):**
```bash
curl http://localhost:5000/api/layers/batas-wilayah
curl http://localhost:5000/api/data/statistics
curl http://localhost:5000/api/model/metrics
curl http://localhost:5000/api/insights/summary
```

**Exit Criteria:**
- ✅ All endpoints return valid JSON
- ✅ GeoJSON files load without errors
- ✅ Statistics calculated correctly
- ✅ Error handling implemented
- ✅ Code follows PEP 8

---

### **3.3 PHASE 3: Frontend Development (Days 6-8)**

| **Task** | **Agent** | **Files** | **Est. Time** |
|---|---|---|---|
| Create templates/base.html | Claude (Code) | base.html | 0.5 day |
| Create templates/peta.html | Claude (Code) | peta.html | 1 day |
| Create templates/data_proses.html | Claude (Code) | data_proses.html | 0.5 day |
| Create templates/model.html | Claude (Code) | model.html | 0.5 day |
| Create templates/insights.html | Claude (Code) | insights.html | 0.5 day |
| Create static/css/style.css | Claude (Code) | style.css | 0.5 day |
| Create static/js/map.js | Claude (Code) | map.js | 1 day |
| Create static/js/charts.js | Claude (Code) | charts.js | 0.5 day |
| Create static/js/api-client.js | Claude (Code) | api-client.js | 0.5 day |

**Frontend Requirements:**
- Responsive (mobile-friendly with Bootstrap)
- Accessible (WCAG 2.1 Level AA)
- No hardcoded API URLs (use config)
- Clean, semantic HTML

**Exit Criteria:**
- ✅ All tabs render correctly
- ✅ Map displays all layers
- ✅ Charts/stats display
- ✅ Responsive on mobile
- ✅ No console errors

---

### **3.4 PHASE 4: Integration & Testing (Days 9-10)**

| **Task** | **Owner** | **Actions** |
|---|---|---|
| Integration testing | Hans + Claude (Code) | Verify frontend ↔ backend communication |
| Bug fixes | Claude (Code) | Fix any integration issues |
| Performance testing | Hans | Verify page load < 3s, map smooth |
| Cross-browser testing | Hans | Chrome, Firefox, Safari |
| Mobile testing | Hans | Test on actual mobile devices |

**Test Scenarios:**
1. Load page → all tabs visible ✓
2. Click Map tab → map displays ✓
3. Toggle Gain/Loss layers → visible/hidden correctly ✓
4. Click feature on map → popup shows properties ✓
5. Tab 2: statistics calculated & displayed ✓
6. Tab 3: confusion matrix & metrics shown ✓
7. Tab 4: insights populated ✓
8. Refresh page → no data loss ✓
9. Mobile view → responsive ✓

**Exit Criteria:**
- ✅ All test scenarios pass
- ✅ No critical bugs
- ✅ Code reviewed
- ✅ Ready for deployment

---

### **3.5 PHASE 5: Deployment & Documentation (Days 11-12)**

| **Task** | **Owner** | **Deliverable** |
|---|---|---|
| Deploy to Render | Hans | Live URL + GitHub link |
| Create API.md | Claude (Code) | Endpoint documentation |
| Create README.md | Hans | Setup & usage guide |
| Create DEPLOYMENT.md | Claude (Code) | Deployment steps |
| Final review | Hans | Verify everything works live |

**Deployment Checklist:**
- [ ] Render.yaml configured
- [ ] Requirements.txt up-to-date
- [ ] Procfile correct
- [ ] GitHub repo public
- [ ] Environment variables set (.env)
- [ ] HTTPS working
- [ ] Auto-deploy enabled

**Exit Criteria:**
- ✅ Live at https://webgis-deforestasi.onrender.com
- ✅ All features working on production
- ✅ GitHub repo complete + documented
- ✅ Ready for submission to dosen

---

## **4. FOLDER STRUCTURE (Final)**

```
webgis-deforestasi/                    ← GitHub Repo Root
│
├── README.md                          ← Dosen sees this first
├── PRD.md                             ← Requirements
├── SDD.md                             ← Technical design
├── AGENTS.md                          ← This file
├── WORKFLOW_PROMPTS.md                ← Build instructions
│
├── .gitignore
├── .env.example
├── requirements.txt
├── Procfile
├── render.yaml
├── config.py
├── app.py
│
├── data/                              ⭐ ALL 5 GEOJSON FILES
│   ├── UAS_Kerinci_BatasWilayah.geojson
│   ├── UAS_Kerinci_Gain.geojson
│   ├── UAS_Kerinci_Loss.geojson
│   ├── UAS_Kerinci_Target2024.geojson
│   ├── UAS_Kerinci_Target2025.geojson
│   └── config.json
│
├── models/                            ⭐ PRE-TRAINED MODELS
│   ├── random_forest_2024.pkl
│   └── random_forest_2025.pkl
│
├── routes/                            🔴 BACKEND AGENT
│   ├── __init__.py
│   ├── peta.py
│   ├── data_proses.py
│   ├── model.py
│   └── insights.py
│
├── services/                          🔴 BACKEND AGENT
│   ├── __init__.py
│   ├── geo_service.py
│   ├── stats_service.py
│   └── model_service.py
│
├── templates/                         🟢 FRONTEND AGENT
│   ├── base.html
│   ├── index.html
│   ├── peta.html
│   ├── data_proses.html
│   ├── model.html
│   └── insights.html
│
├── static/                            🟢 FRONTEND AGENT
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── style.css
│   └── js/
│       ├── leaflet.min.js
│       ├── plotly.min.js
│       ├── map.js
│       ├── charts.js
│       └── api-client.js
│
├── tests/                             (Phase 2+)
│   ├── test_geo_service.py
│   └── test_stats_service.py
│
└── docs/                              📚 DOCUMENTATION
    ├── API.md
    ├── SETUP.md
    └── DEPLOYMENT.md
```

**Legend:**
- 🔴 = Backend Agent (Claude Code) builds this
- 🟢 = Frontend Agent (Claude Code) builds this
- ⭐ = Critical data files (Hans provides)
- 📚 = Documentation (Claude Chat helps)

---

## **5. WORKFLOW DETAIL**

### **5.1 How Hans & Agents Work Together**

```
┌─────────────────────────────────────────────┐
│ STEP 1: PLAN MODE                           │
│ Hans asks Claude (Chat):                    │
│ "Break down the tech stack"                 │
│ → Get detailed breakdown                    │
│ → Use for WORKFLOW_PROMPTS.md               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ STEP 2: DOCUMENT MODE                       │
│ Hans gets documentation templates:          │
│ - PRD.md ✅                                  │
│ - SDD.md ✅                                  │
│ - AGENTS.md ✅                               │
│ - WORKFLOW_PROMPTS.md (in progress)         │
│                                             │
│ Hans reviews & approves                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ STEP 3: BUILD MODE - BACKEND                │
│ Hans instructs Claude (Code):               │
│ "Build Phase 2: Backend Development"        │
│ Using WORKFLOW_PROMPTS.md Step 1-10         │
│ → Returns: Flask app + routes + services    │
│ → Hans tests locally                        │
│ → Hans reviews code                         │
│ → Pushes to GitHub                          │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ STEP 4: BUILD MODE - FRONTEND               │
│ Hans instructs Claude (Code):               │
│ "Build Phase 3: Frontend Development"       │
│ Using WORKFLOW_PROMPTS.md Step 11-20        │
│ → Returns: HTML templates + CSS + JS        │
│ → Hans integrates with backend              │
│ → Hans tests locally                        │
│ → Hans pushes to GitHub                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ STEP 5: INTEGRATION & TESTING               │
│ Hans + Claude (Code) collaborate:           │
│ - Test frontend ↔ backend communication     │
│ - Fix bugs                                  │
│ - Performance optimization                  │
│ → All tests pass                            │
│ → Push final code to GitHub                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ STEP 6: DEPLOYMENT                          │
│ Hans deploys to Render:                     │
│ - Connect GitHub repo to Render             │
│ - Configure render.yaml                     │
│ - Push to GitHub                            │
│ → Render auto-deploys                       │
│ → Live URL: https://webgis-...onrender.com  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ STEP 7: DOCUMENTATION & SUBMISSION          │
│ Hans + Claude (Chat) finalize:              │
│ - Create API.md documentation               │
│ - Create README.md                          │
│ - Create DEPLOYMENT.md                      │
│ → Submit to dosen                           │
│ → Provide live URL + GitHub link            │
└─────────────────────────────────────────────┘
```

---

## **6. COMMUNICATION CHANNELS**

### **6.1 For Hans & Claude (Chat)**

**When to use:**
- Planning phase (PLAN MODE)
- Architecture decisions
- Documentation review
- Troubleshooting complex issues
- Explaining concepts

**Format:**
- Chat messages
- Document creation/review
- Detailed explanations with examples

---

### **6.2 For Hans & Claude (Code)**

**When to use:**
- Building phase (BUILD MODE)
- Writing actual code
- Creating files & components
- Testing & debugging
- Code reviews

**Format:**
- Follow WORKFLOW_PROMPTS.md instructions
- Code files created in GitHub
- Comments in code for non-obvious logic
- Unit tests for critical functions

---

## **7. VERSION CONTROL STRATEGY**

### **7.1 GitHub Workflow**

```bash
# Initial setup
git clone https://github.com/username/webgis-deforestasi
cd webgis-deforestasi

# After backend development
git add routes/ services/ app.py config.py
git commit -m "Phase 2: Backend development - Flask app + API endpoints"
git push origin main

# After frontend development
git add templates/ static/
git commit -m "Phase 3: Frontend development - HTML/CSS/JS templates"
git push origin main

# After integration
git add .
git commit -m "Phase 4: Integration & testing - all features integrated"
git push origin main

# After deployment
git add render.yaml
git commit -m "Phase 5: Deployment - Render configuration"
git push origin main
```

### **7.2 Commit Message Convention**

```
[PHASE] [COMPONENT]: Brief description

Example:
[PHASE 2] [BACKEND]: Add Flask app structure + API endpoints
[PHASE 3] [FRONTEND]: Add Tab 1 map visualization
[PHASE 4] [INTEGRATION]: Fix API response format mismatch
[PHASE 5] [DEPLOYMENT]: Configure Render.yaml
```

---

## **8. QUALITY ASSURANCE**

### **8.1 Code Review Checklist**

**Before pushing to GitHub:**
- [ ] Code follows PEP 8 (Python) / ES6 (JavaScript)
- [ ] No hardcoded values (use config.py)
- [ ] Error handling implemented
- [ ] Comments on complex logic
- [ ] No unused imports/variables
- [ ] All endpoints tested locally

**Before submitting to dosen:**
- [ ] Live on Render ✓
- [ ] All features working ✓
- [ ] No console errors ✓
- [ ] Responsive on mobile ✓
- [ ] Documentation complete ✓

---

## **9. TROUBLESHOOTING & ESCALATION**

### **9.1 Common Issues & Solutions**

| **Issue** | **Cause** | **Solution** |
|---|---|---|
| GeoJSON not loading | File path wrong | Check `DATA_FOLDER` in config.py |
| API returns 404 | Endpoint not defined | Check routes/ files |
| Map blank | API response error | Check browser DevTools → Network tab |
| Style not applying | CSS file not linked | Check <link> in base.html |
| Render deployment fails | Missing requirements | Check requirements.txt |

### **9.2 When to Escalate**

- ❌ Major architectural issue → Consult Claude (Chat) for PLAN MODE
- ❌ Persistent bug → Debug with Claude (Code)
- ❌ Performance problem → Review SDD & optimize
- ❌ Dosen question → Refer to PRD/SDD documentation

---

## **10. KEY CONTACTS & RESOURCES**

### **10.1 Internal**

| **Person** | **Role** | **Contact** |
|---|---|---|
| Hans | Project Lead | (Direct communication) |
| Claude (Chat) | Planning & Docs | (Chat interface) |
| Claude (Code) | Backend & Frontend | (Code interface) |

### **10.2 External Resources**

| **Resource** | **URL** |
|---|---|
| Leaflet.js Docs | https://leafletjs.com/ |
| Bootstrap 5 Docs | https://getbootstrap.com/docs/5.0/ |
| Flask Documentation | https://flask.palletsprojects.com/ |
| GeoPandas Docs | https://geopandas.org/ |
| Render Docs | https://render.com/docs |
| Plotly.js Docs | https://plotly.com/javascript/ |

---

## **11. REVISION HISTORY**

| **Version** | **Date** | **Author** | **Changes** |
|---|---|---|---|
| 1.0 | 16 July 2026 | Claude (Chat) | Initial AGENTS.md creation |

---

**Document Owner**: Hans  
**Last Updated**: 16 July 2026  
**Status**: APPROVED FOR EXECUTION

---

## **APPENDIX A: Quick Reference**

### **Project At-A-Glance**

- **Name**: WebGIS Monitoring Deforestasi Kerinci
- **Type**: Web-based Geographic Information System
- **Tech Stack**: Flask + GeoPandas + Leaflet.js + Bootstrap 5
- **Hosting**: Render.com (free tier)
- **Repository**: GitHub (public)
- **Duration**: ~2 weeks (12 days)
- **Team**: 1 Lead (Hans) + 2 Code Agents (Backend/Frontend) + 1 Advisor (Chat)
- **Status**: In Development

### **Critical Dates**

- Day 1-2: Planning & Documentation
- Day 3-5: Backend Development
- Day 6-8: Frontend Development
- Day 9-10: Integration & Testing
- Day 11-12: Deployment & Documentation
- **Submission**: Day 12+

### **Submission Checklist**

- [ ] Live URL: https://webgis-deforestasi.onrender.com
- [ ] GitHub repo: https://github.com/username/webgis-deforestasi
- [ ] PRD.md + SDD.md + README.md
- [ ] All features working
- [ ] Documentation complete
- [ ] Responsive design
- [ ] No critical bugs
