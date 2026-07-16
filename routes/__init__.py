"""
routes/__init__.py
===================
Package inisialisasi untuk routes layer.

Setiap file route merepresentasikan satu tab di WebGIS dashboard:
- peta.py        → Tab 1: Peta Hasil      (/map, /api/layers/<name>)
- data_proses.py → Tab 2: Data & Proses   (/data, /api/data/...)
- model.py       → Tab 3: Evaluasi Model  (/model, /api/model/...)
- insights.py    → Tab 4: Insight Hasil   (/insights, /api/insights/...)
"""
