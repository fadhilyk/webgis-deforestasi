/**
 * charts.js - Charts & Data Controller
 * =====================================
 * Memuat data dari backend API dan meng-update DOM:
 * Tab 2 (Statistik & Metadata), Tab 3 (Evaluasi Model), Tab 4 (Insights)
 */

document.addEventListener('DOMContentLoaded', () => {

    // =====================================================================
    // TAB 2: DATA & PROSES (Statistics & Metadata)
    // =====================================================================
    async function loadDataProses() {
        try {
            // 1. Fetch data
            const [stats, meta] = await Promise.all([
                API.getStatistics(),
                API.getMetadata()
            ]);

            // 2. Hide loading, show content
            document.getElementById('data-loading').style.display = 'none';
            document.getElementById('data-content').style.display = 'block';

            // 3. Update Stat Cards
            document.getElementById('stat-gain-ha').innerText = `${stats.gain_ha.toLocaleString()} ha`;
            document.getElementById('stat-gain-pct').innerText = stats.percentage_gain;
            
            document.getElementById('stat-loss-ha').innerText = `${stats.loss_ha.toLocaleString()} ha`;
            document.getElementById('stat-loss-pct').innerText = stats.percentage_loss;
            
            document.getElementById('stat-net-ha').innerText = `${Math.abs(stats.net_change_ha).toLocaleString()} ha`;
            const statusBadge = document.getElementById('stat-status-badge');
            if (stats.status === 'net_gain') {
                statusBadge.innerText = `+${stats.net_change_percent}% (Net Gain)`;
                statusBadge.className = 'badge bg-gain';
            } else {
                statusBadge.innerText = `-${stats.net_change_percent}% (Net Loss)`;
                statusBadge.className = 'badge bg-loss';
            }

            document.getElementById('stat-total-ha').innerText = `${stats.total_change_ha.toLocaleString()} ha`;
            document.getElementById('stat-features').innerText = (stats.gain_feature_count + stats.loss_feature_count).toLocaleString();

            // 4. Render Pie Chart (Gain vs Loss)
            const pieData = [{
                values: [stats.gain_ha, stats.loss_ha],
                labels: ['Area Gain', 'Area Loss'],
                type: 'pie',
                hole: 0.4,
                marker: { colors: ['#2ecc71', '#e74c3c'] },
                textinfo: 'label+percent',
                hoverinfo: 'label+value+percent'
            }];
            const pieLayout = {
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: { color: '#e8f5e9' },
                margin: { t: 10, b: 10, l: 10, r: 10 },
                showlegend: true,
                legend: { orientation: 'h', y: -0.1 }
            };
            Plotly.newPlot('chart-gain-loss', pieData, pieLayout, {responsive: true});

            // 5. Render Bar Chart (Features count)
            const barData = [{
                x: ['Polygon Gain', 'Polygon Loss'],
                y: [stats.gain_feature_count, stats.loss_feature_count],
                type: 'bar',
                marker: { color: ['#52b788', '#e74c3c'] },
                text: [stats.gain_feature_count, stats.loss_feature_count],
                textposition: 'auto',
            }];
            const barLayout = {
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: { color: '#e8f5e9' },
                margin: { t: 20, b: 30, l: 40, r: 10 },
                yaxis: { gridcolor: 'rgba(255,255,255,0.1)' }
            };
            Plotly.newPlot('chart-features', barData, barLayout, {responsive: true});

            // 6. Update Metadata Table
            const tbody = document.getElementById('metadata-table').querySelector('tbody');
            tbody.innerHTML = `
                <tr><td class="text-muted" width="150">Provider</td><td>${meta.provider}</td></tr>
                <tr><td class="text-muted">Satelit</td><td>${meta.satellite}</td></tr>
                <tr><td class="text-muted">Platform</td><td>${meta.platform}</td></tr>
                <tr><td class="text-muted">Cloud Masking</td><td>${meta.cloud_masking}</td></tr>
                <tr><td class="text-muted">Algoritma</td><td>${meta.classification.algorithm}</td></tr>
                <tr><td class="text-muted">Band Sentinel-2</td><td>${meta.bands.join(', ')}</td></tr>
            `;

        } catch (error) {
            console.error('Error loading Tab 2 data:', error);
            document.getElementById('data-loading').innerHTML = `<div class="alert alert-danger">Gagal memuat data statistik: ${error.message}</div>`;
        }
    }


    // =====================================================================
    // TAB 3: EVALUASI MODEL
    // =====================================================================
    async function loadModelData() {
        try {
            const [metrics, matrix, interp] = await Promise.all([
                API.getMetrics(),
                API.getConfusionMatrix(),
                API.getInterpretation()
            ]);

            // Hide loading, show content
            document.getElementById('model-loading').style.display = 'none';
            document.getElementById('model-content').style.display = 'block';

            // Update Metrics Cards
            const updateMetricCard = (id, val, textId) => {
                const percent = val.toFixed(1);
                document.getElementById(`metric-${id}`).innerText = `${percent}%`;
                document.getElementById(`bar-${id}`).style.width = `${percent}%`;
            };

            updateMetricCard('accuracy', metrics.accuracy);
            updateMetricCard('precision', metrics.precision);
            updateMetricCard('recall', metrics.recall);
            updateMetricCard('f1', metrics.f1_score);
            
            document.getElementById('model-samples').innerText = metrics.training_samples + metrics.testing_samples;

            // Render Confusion Matrix Heatmap
            const cm = matrix;
            const zValues = [
                [cm.TP, cm.FP],
                [cm.FN, cm.TN]
            ];
            const hmData = [{
                z: zValues,
                x: ['Prediksi Hutan', 'Prediksi Non-Hutan'],
                y: ['Aktual Hutan', 'Aktual Non-Hutan'],
                type: 'heatmap',
                colorscale: 'Greens',
                showscale: true,
                text: [
                    [`True Positive (TP): ${cm.TP}`, `False Positive (FP): ${cm.FP}`],
                    [`False Negative (FN): ${cm.FN}`, `True Negative (TN): ${cm.TN}`]
                ],
                hoverinfo: 'text'
            }];
            
            const hmLayout = {
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: { color: '#e8f5e9' },
                margin: { t: 20, b: 40, l: 120, r: 20 },
                annotations: []
            };
            
            // Add text annotations to heatmap squares
            for (let i = 0; i < 2; i++) {
                for (let j = 0; j < 2; j++) {
                    hmLayout.annotations.push({
                        x: ['Prediksi Hutan', 'Prediksi Non-Hutan'][j],
                        y: ['Aktual Hutan', 'Aktual Non-Hutan'][i],
                        text: zValues[i][j].toString(),
                        font: { size: 20, color: (zValues[i][j] > 40) ? '#fff' : '#000' },
                        showarrow: false
                    });
                }
            }
            
            Plotly.newPlot('chart-confusion-matrix', hmData, hmLayout, {responsive: true});

            // Update Interpretation Text
            document.getElementById('model-interpretation').innerHTML = `
                <p><strong>Akurasi Model:</strong> ${interp.accuracy_context}</p>
                <p class="text-danger mb-1"><strong>False Positive (FP):</strong> ${interp.fp_implication}</p>
                <p class="text-warning"><strong>False Negative (FN):</strong> ${interp.fn_implication}</p>
            `;

            const limsHtml = interp.limitations.map(l => `<li>${l}</li>`).join('');
            document.getElementById('model-limitations').innerHTML = limsHtml;
            
            const recsHtml = interp.recommendations.map(r => `<li>${r}</li>`).join('');
            document.getElementById('model-recommendations').innerHTML = recsHtml;

        } catch (error) {
            console.error('Error loading Tab 3 data:', error);
            document.getElementById('model-loading').innerHTML = `<div class="alert alert-danger">Gagal memuat evaluasi model: ${error.message}</div>`;
        }
    }


    // =====================================================================
    // TAB 4: INSIGHT HASIL
    // =====================================================================
    async function loadInsightsData() {
        try {
            const [summary, spatial] = await Promise.all([
                API.getSummary(),
                API.getSpatial()
            ]);

            // Hide loading, show content
            document.getElementById('insights-loading').style.display = 'none';
            document.getElementById('insights-content').style.display = 'block';

            // Update Summary Stats
            document.getElementById('insight-t2024').innerText = `${summary.target_2024_ha.toLocaleString()} ha`;
            document.getElementById('insight-t2025').innerText = `${summary.target_2025_ha.toLocaleString()} ha`;
            document.getElementById('insight-gain').innerText = `${summary.gain_ha.toLocaleString()} ha`;
            document.getElementById('insight-loss').innerText = `${summary.loss_ha.toLocaleString()} ha`;

            // Update Spatial Distribution
            const sGain = spatial.gain_distribution;
            document.getElementById('spatial-gain-location').innerHTML = `<strong>Lokasi Utama:</strong> ${sGain.primary_location} (${sGain.percentage}%)`;
            document.getElementById('spatial-gain-desc').innerText = sGain.description;
            document.getElementById('spatial-gain-causes').innerHTML = sGain.possible_causes.map(c => `<li>${c}</li>`).join('');

            const sLoss = spatial.loss_distribution;
            document.getElementById('spatial-loss-location').innerHTML = `<strong>Lokasi Utama:</strong> ${sLoss.primary_location} (${sLoss.percentage}%)`;
            document.getElementById('spatial-loss-desc').innerText = sLoss.description;
            document.getElementById('spatial-loss-causes').innerHTML = sLoss.possible_causes.map(c => `<li>${c}</li>`).join('');

            // Set static Key Findings & Conclusion
            document.getElementById('key-findings').innerHTML = `
                <li>Luas target deforestasi 2024 adalah <strong>${summary.target_2024_ha.toLocaleString()} ha</strong>.</li>
                <li>Realisasi Loss (kehilangan hutan) mencapai <strong>${summary.loss_ha.toLocaleString()} ha</strong>.</li>
                <li>Terjadi penambahan area hijau (Gain) sebesar <strong>${summary.gain_ha.toLocaleString()} ha</strong>.</li>
                <li>Net Change tutupan hutan menunjukkan <strong>${Math.abs(summary.net_change_ha).toLocaleString()} ha</strong> (${summary.net_change_percent}% dari total perubahan).</li>
            `;
            
            const netStatus = summary.net_change_ha >= 0 ? "peningkatan" : "penurunan";
            document.getElementById('conclusion-text').innerText = `Berdasarkan analisis citra Sentinel-2 pada tahun 2024–2025, wilayah Kerinci mengalami dinamika perubahan tutupan lahan yang aktif. Meskipun terdapat upaya reforestasi, tekanan kehilangan lahan masih tinggi, menghasilkan tren netto (net change) berupa ${netStatus} tutupan hutan secara keseluruhan.`;

            // Render Comparison Chart
            const compData = [
                {
                    name: 'Target (Prediksi)',
                    x: ['2024', '2025'],
                    y: [summary.target_2024_ha, summary.target_2025_ha],
                    type: 'bar',
                    marker: { color: '#f39c12' }
                },
                {
                    name: 'Realisasi (Aktual)',
                    x: ['2024'],
                    y: [summary.loss_ha],
                    type: 'bar',
                    marker: { color: '#e74c3c' }
                }
            ];
            const compLayout = {
                barmode: 'group',
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: { color: '#e8f5e9' },
                margin: { t: 20, b: 30, l: 50, r: 20 },
                yaxis: { gridcolor: 'rgba(255,255,255,0.1)', title: 'Luas (Hektar)' },
                legend: { orientation: 'h', y: -0.15 }
            };
            Plotly.newPlot('chart-comparison', compData, compLayout, {responsive: true});

        } catch (error) {
            console.error('Error loading Tab 4 data:', error);
            document.getElementById('insights-loading').innerHTML = `<div class="alert alert-danger">Gagal memuat insight: ${error.message}</div>`;
        }
    }


    // =====================================================================
    // TRIGGER LOAD ON TAB CLICK
    // =====================================================================
    // Kita gunakan sistem "Lazy Loading", data hanya difetch saat tab pertama kali diklik
    
    let isDataLoaded = false;
    let isModelLoaded = false;
    let isInsightsLoaded = false;

    // Listener Tab Data
    const tabDataBtn = document.getElementById('tab-data-btn');
    if (tabDataBtn) {
        tabDataBtn.addEventListener('shown.bs.tab', () => {
            if (!isDataLoaded) {
                loadDataProses();
                isDataLoaded = true;
            }
        });
    }

    // Listener Tab Model
    const tabModelBtn = document.getElementById('tab-model-btn');
    if (tabModelBtn) {
        tabModelBtn.addEventListener('shown.bs.tab', () => {
            if (!isModelLoaded) {
                loadModelData();
                isModelLoaded = true;
            }
        });
    }

    // Listener Tab Insights
    const tabInsightsBtn = document.getElementById('tab-insights-btn');
    if (tabInsightsBtn) {
        tabInsightsBtn.addEventListener('shown.bs.tab', () => {
            if (!isInsightsLoaded) {
                loadInsightsData();
                isInsightsLoaded = true;
            }
        });
    }
});
