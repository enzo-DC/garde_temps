<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const props = defineProps({
  formatPrice: Function,
  currency: String
})

const router = useRouter()
const watches = ref([])
const loading = ref(true)
const wishlist = ref(JSON.parse(localStorage.getItem('wishlist') || '[]'))

const totalValue = computed(() => {
  return watches.value.reduce((acc, w) => acc + parseFloat(w.price), 0)
})

const loadWishlist = async () => {
  if (wishlist.value.length === 0) {
    watches.value = []
    loading.value = false
    return
  }

  loading.value = true
  try {
    // We fetch all watches and filter them by ID locally (simpler for now as we don't have a bulk-by-id endpoint)
    // In a real app, you'd have a specific endpoint or page by page.
    const response = await api.getWatches({ page_size: 100 })
    watches.value = response.data.results.filter(w => wishlist.value.includes(w.id))
    loading.value = false
  } catch (error) {
    console.error('Error loading wishlist:', error)
    loading.value = false
  }
}

// Local formatPrice removed

const removeFromWishlist = (id, event) => {
  event.stopPropagation()
  wishlist.value = wishlist.value.filter(itemId => itemId !== id)
  localStorage.setItem('wishlist', JSON.stringify(wishlist.value))
  watches.value = watches.value.filter(w => w.id !== id)
}

const goToDetail = (id) => {
  router.push(`/watch/${id}`)
}

const goBack = () => {
  router.push('/')
}

// 3D Tilt Effect
const handleTilt = (e) => {
  const rect = e.currentTarget.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const rotateX = (y - centerY) / 15
  const rotateY = (centerX - x) / 15
  e.currentTarget.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`
}

const resetTilt = (e) => {
  e.currentTarget.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`
}

// PDF Export
const downloadPDF = async () => {
  if (wishlist.value.length === 0) return
  
  try {
    const response = await api.exportWishlistPDF(wishlist.value)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'ma_liste_de_souhaits.pdf')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error downloading PDF:', error)
    alert('Erreur lors de la génération du PDF.')
  }
}

onMounted(() => {
  loadWishlist()
})
</script>

<template>
  <div class="wishlist-page">
    <!-- <div class="animated-bg"></div> -->
    
    <div class="container">
      <header class="wishlist-header">
        <button @click="goBack" class="btn-back">← Retour</button>
        <h1 class="page-title italic">Mes Coups de Cœur</h1>
        
        <div class="wishlist-summary-bar" v-if="watches.length">
          <div class="summary-item">
            <span class="summary-label">Collection</span>
            <span class="summary-value">{{ watches.length }} pièces</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-item">
            <span class="summary-label">Valeur Totale Est.</span>
            <span class="summary-value">{{ props.formatPrice(totalValue) }}</span>
          </div>
        </div>

        <div class="header-actions" v-if="watches.length">
          <button class="btn-export-wishlist" @click="downloadPDF">
            📄 Exporter ma sélection
          </button>
        </div>
      </header>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Récupération de vos trésors...</p>
      </div>

      <div v-else-if="watches.length === 0" class="empty-state">
        <div class="empty-icon">💔</div>
        <h2>Votre liste est vide</h2>
        <p>Explorez notre collection et cliquez sur le cœur pour ajouter des montres ici.</p>
        <button @click="goBack" class="btn-discover">Découvrir la collection</button>
      </div>

      <div v-else class="watches-grid">
        <div v-for="(watch, index) in watches" :key="watch.id" 
             class="watch-card" 
             @click="goToDetail(watch.id)"
             @mousemove="handleTilt($event)"
             @mouseleave="resetTilt($event)"
             :style="{ transitionDelay: index * 0.1 + 's' }">
          <div class="watch-image">
            <img v-if="watch.image_url" :src="watch.image_url" :alt="watch.model_name" class="watch-photo">
            <div v-else class="watch-icon">⌚</div>
            
            <button 
              class="remove-btn" 
              @click="removeFromWishlist(watch.id, $event)"
              title="Retirer des favoris"
            >
              ×
            </button>
          </div>
          <div class="watch-info">
            <div class="watch-brand">{{ watch.brand_name }}</div>
            <h3 class="watch-model">{{ watch.model_name }}</h3>
            <div class="watch-details">
              <div class="watch-detail-item"><span>{{ watch.movement_display }}</span></div>
              <div class="watch-detail-item"><span>{{ watch.case_diameter }}mm</span></div>
            </div>
            <div class="watch-price">{{ props.formatPrice(watch.price) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wishlist-page {
  min-height: 100vh;
  padding: 120px 0 4rem; /* Added top padding to account for fixed navbar */
  position: relative;
}

.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
  z-index: -1;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.wishlist-header {
  text-align: center;
  margin-bottom: 5rem;
}

.btn-back {
  background: none;
  border: 1px solid var(--border);
  color: var(--accent-gold);
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
  font-family: var(--font-body);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-size: 0.8rem;
}

.btn-back:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: var(--accent-gold);
}

.page-title {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5vw, 4rem);
  color: var(--accent-gold);
  margin-bottom: 0.5rem;
}

.page-count {
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.9rem;
  margin-bottom: 0;
}

.wishlist-summary-bar {
  display: inline-flex;
  align-items: center;
  gap: 3rem;
  padding: 1.5rem 4rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  margin-top: 2rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.summary-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.3em;
  color: var(--text-muted);
}

.summary-value {
  font-family: var(--font-display);
  font-size: 1.5rem;
  color: var(--accent-gold);
}

.summary-divider {
  width: 1px;
  height: 30px;
  background: var(--border);
}

.header-actions {
  margin-top: 3rem;
}

.btn-export-wishlist {
  background: transparent;
  border: 1px solid var(--accent-gold);
  color: var(--accent-gold);
  padding: 1.2rem 3rem;
  border-radius: 0;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.8rem;
}

.btn-export-wishlist:hover {
  background: var(--accent-gold);
  color: var(--primary);
  transform: translateY(-2px);
}

/* Grid */
.watches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2.5rem;
}

.watch-card {
  background: var(--bg-card);
  border-radius: 0;
  border: 1px solid var(--border);
  overflow: hidden;
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  position: relative;
}

.watch-card:hover {
  border-color: var(--accent-gold);
  box-shadow: 0 30px 60px rgba(0,0,0,0.5);
}

.watch-image {
  height: 280px;
  background: var(--secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.watch-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.watch-card:hover .watch-photo {
  transform: scale(1.1);
}

.remove-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: rgba(255, 71, 87, 0.8);
  color: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
}

.remove-btn:hover {
  transform: scale(1.2) rotate(90deg);
  background: #ff4757;
}

.watch-info {
  padding: 2rem;
}

.watch-brand {
  color: var(--accent-rose);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 0.5rem;
}

.watch-model {
  font-family: var(--font-display);
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.watch-price {
  font-family: var(--font-display);
  font-size: 1.5rem;
  color: var(--accent-gold);
  font-weight: 400;
  margin-bottom: 0;
}

.watch-details {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.75rem 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.watch-detail-item {
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 5rem 0;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 2rem;
  filter: grayscale(1);
  opacity: 0.5;
}

.empty-state h2 {
  font-family: var(--font-display);
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.empty-state p {
  color: var(--text-muted);
  margin-bottom: 3rem;
}

.btn-discover {
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-rose));
  border: none;
  padding: 1.2rem 3rem;
  border-radius: 50px;
  color: var(--primary);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-discover:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.4);
}

/* Spinner */
.loading {
  text-align: center;
  padding: 5rem 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid var(--border);
  border-top-color: var(--accent-gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .watches-grid {
    grid-template-columns: 1fr;
  }
}
</style>
