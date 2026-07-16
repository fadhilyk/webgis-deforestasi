/**
 * api-client.js - API Client
 * ===========================
 * WebGIS Monitoring Deforestasi Kerinci
 *
 * Helper functions untuk fetch data dari Flask API endpoints.
 */

const API_BASE = '';  // Same-origin, no prefix needed

/**
 * Generic fetch wrapper with error handling.
 * @param {string} url - API endpoint path
 * @returns {Promise<Object>} - Parsed JSON response
 */
async function apiFetch(url) {
    try {
        const response = await fetch(`${API_BASE}${url}`);
        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.error || `HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`API Error [${url}]:`, error.message);
        throw error;
    }
}

// Convenience functions per endpoint
const API = {
    // Tab 1: Peta
    getLayers:          ()     => apiFetch('/api/layers'),
    getLayer:          (name) => apiFetch(`/api/layers/${name}`),

    // Tab 2: Data & Proses
    getStatistics:     ()     => apiFetch('/api/data/statistics'),
    getMetadata:       ()     => apiFetch('/api/data/metadata'),

    // Tab 3: Model
    getMetrics:        ()     => apiFetch('/api/model/metrics'),
    getConfusionMatrix:()     => apiFetch('/api/model/confusion-matrix'),
    getInterpretation: ()     => apiFetch('/api/model/interpretation'),

    // Tab 4: Insights
    getSummary:        ()     => apiFetch('/api/insights/summary'),
    getSpatial:        ()     => apiFetch('/api/insights/spatial'),
};
