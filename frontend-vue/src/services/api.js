import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

export default {
    // Watches
    getWatches(params = {}) {
        return api.get('/watches/', { params })
    },

    getWatch(id) {
        return api.get(`/watches/${id}/`)
    },

    // Brands
    getBrands() {
        return api.get('/brands/')
    },

    // Complications
    getComplications() {
        return api.get('/complications/')
    },

    // PDF Export
    exportPDF(watchIds) {
        return api.post('/watches/export-pdf/', { watch_ids: watchIds }, {
            responseType: 'blob'
        })
    },

    exportWishlistPDF(watchIds) {
        return api.post('/watches/export-wishlist/', { watch_ids: watchIds }, {
            responseType: 'blob'
        })
    },

    exportComparisonPDF(watchIds) {
        return api.post('/watches/export-comparison/', { watch_ids: watchIds }, {
            responseType: 'blob'
        })
    }
}
