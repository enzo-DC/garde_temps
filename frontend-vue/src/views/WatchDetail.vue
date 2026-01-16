<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const props = defineProps({
  formatPrice: Function,
  currency: String
})

const route = useRoute()
const router = useRouter()
const watch = ref(null)
const loading = ref(true)

const wishlist = ref(JSON.parse(localStorage.getItem('wishlist') || '[]'))

const loadWatch = async () => {
  try {
    const response = await api.getWatch(route.params.id)
    watch.value = response.data
    loading.value = false
  } catch (error) {
    console.error('Error loading watch:', error)
    loading.value = false
  }
}

const toggleWishlist = (id) => {
  const index = wishlist.value.indexOf(id)
  if (index === -1) {
    wishlist.value.push(id)
  } else {
    wishlist.value.splice(index, 1)
  }
  localStorage.setItem('wishlist', JSON.stringify(wishlist.value))
}

const isInWishlist = (id) => wishlist.value.includes(id)

// Local formatPrice removed

const goBack = () => {
  router.push('/')
}

const downloadPDF = async () => {
  if (!watch.value) return
  
  try {
    const response = await api.exportPDF([watch.value.id])
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `fiche_${watch.value.model_name.replace(/\s+/g, '_')}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error downloading PDF:', error)
    alert('Erreur lors de la génération du PDF.')
  }
}

onMounted(() => {
  loadWatch()
})
</script>

<template>
  <div class="watch-detail">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Chargement...</p>
    </div>

    <div v-else-if="watch" class="container">
      <!-- Navigation Buttons -->
      <div class="nav-floating">
        <button class="wishlist-link-btn" @click="router.push('/wishlist')" title="Ma Liste de Souhaits">
          ♥
          <span v-if="wishlist.length" class="badge">{{ wishlist.length }}</span>
        </button>
        
        <button 
          class="wishlist-toggle-btn" 
          :class="{ active: isInWishlist(watch.id) }"
          @click="toggleWishlist(watch.id)"
          title="Ajouter aux favoris"
        >
          {{ isInWishlist(watch.id) ? '❤️' : '🤍' }}
        </button>
      </div>

      <button @click="goBack" class="back-link">← Retour au Catalogue</button>

      <div class="detail-container">
        <div class="watch-showcase">
          <div class="watch-image-large">
            <img v-if="watch.image_url" :src="watch.image_url" :alt="watch.model_name" class="watch-photo-large">
            <div v-else class="watch-icon-large">⌚</div>
          </div>
        </div>

        <div class="watch-details-section">
            <div class="watch-brand">{{ watch.brand_name }}</div>
            <h1 class="watch-title">{{ watch.model_name }}</h1>
            <div class="watch-price">{{ props.formatPrice(watch.price) }}</div>
            
            <p class="watch-description">{{ watch.description }}</p>
          <div class="watch-meta">
            <div class="meta-item">
              Réf. <span>{{ watch.reference_number }}</span>
            </div>
            <div v-if="watch.serial_number" class="meta-item">
              S/N <span>{{ watch.serial_number }}</span>
            </div>
          </div>

          <div class="specs-grid">
            <div class="spec-card">
              <div class="spec-label">Mouvement</div>
              <div class="spec-value">{{ watch.movement_display }}</div>
            </div>
            <div class="spec-card">
              <div class="spec-label">Matériau</div>
              <div class="spec-value">{{ watch.material_display }}</div>
            </div>
            <div class="spec-card">
              <div class="spec-label">Diamètre</div>
              <div class="spec-value">{{ watch.case_diameter }} mm</div>
            </div>
            <div class="spec-card">
              <div class="spec-label">Étanchéité</div>
              <div class="spec-value">{{ watch.water_resistance }} m</div>
            </div>
          </div>

          <div class="description-section">
            <h2 class="section-title">Description</h2>
            <p class="description-text">{{ watch.description }}</p>
          </div>

          <div v-if="watch.complications && watch.complications.length > 0" class="complications-section">
            <h2 class="section-title">Complications</h2>
            <div class="complications-grid">
              <div v-for="complication in watch.complications" :key="complication.id" class="complication-badge">
                {{ complication.name }}
              </div>
            </div>
          </div>
          <div class="watch-actions">
            <button class="btn-primary-luxury" @click="toggleWishlist(watch.id)">
              {{ isInWishlist(watch.id) ? 'Retirer des favoris' : 'Ajouter aux favoris' }}
            </button>
            <button class="btn-secondary-luxury" @click="downloadPDF">
              📥 Télécharger la Fiche PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.watch-detail {
  min-height: 100vh;
  background: transparent;
  padding: 120px 0 2rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--accent-gold);
  background: none;
  border: none;
  font-weight: 600;
  margin-bottom: 3rem;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-size: 0.85rem;
  cursor: pointer;
  font-family: var(--font-body);
}

.back-link:hover {
  color: var(--accent-rose);
  transform: translateX(-10px);
}

.detail-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  margin-bottom: 4rem;
}

.watch-showcase {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.watch-image-large {
  width: 100%;
  aspect-ratio: 1;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(10, 10, 15, 0.9) 100%);
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12rem;
  border: 1px solid var(--border);
  position: relative;
  overflow: hidden;
  animation: fadeIn 1s ease-out;
}

.watch-photo-large {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.watch-image-large:hover .watch-photo-large {
  transform: scale(1.05);
}

.watch-image-large::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.watch-icon-large {
  position: relative;
  z-index: 1;
  filter: drop-shadow(0 0 40px rgba(212, 175, 55, 0.6));
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.watch-details-section {
  animation: slideInRight 1s ease-out;
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(50px); }
  to { opacity: 1; transform: translateX(0); }
}

.brand-badge {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-rose) 100%);
  color: var(--primary);
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 1.5rem;
}

.watch-title {
  font-family: var(--font-display);
  font-size: 4rem;
  font-weight: 300;
  color: var(--accent-gold);
  margin-bottom: 1rem;
  line-height: 1.2;
}

.watch-price-large {
  font-size: 3rem;
  font-weight: 300;
  color: var(--text-primary);
  font-family: var(--font-display);
  margin-bottom: 2rem;
}

.watch-meta {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border);
}

.meta-item {
  font-size: 0.85rem;
  color: var(--text-muted);
  letter-spacing: 0.1em;
}

.meta-item span {
  color: var(--accent-gold);
  font-weight: 600;
}

.specs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-bottom: 3rem;
}

.spec-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  transition: all 0.3s ease;
}

.spec-card:hover {
  border-color: var(--accent-gold);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
}

.spec-label {
  font-size: 0.75rem;
  color: var(--accent-rose);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.spec-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.description-section {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  padding: 3rem;
  border-radius: 30px;
  margin-bottom: 3rem;
  border: 1px solid var(--border);
}

.section-title {
  font-family: var(--font-display);
  font-size: 2rem;
  color: var(--accent-gold);
  margin-bottom: 1.5rem;
  font-weight: 300;
}

.description-text {
  line-height: 1.9;
  color: var(--text-secondary);
  font-size: 1.05rem;
}

.complications-section {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  padding: 3rem;
  border-radius: 30px;
  margin-bottom: 3rem;
  border: 1px solid var(--border);
}

.complications-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.complication-badge {
  background: var(--bg-card);
  padding: 1rem 2rem;
  border-radius: 50px;
  border: 1px solid var(--border);
  font-size: 0.95rem;
  transition: all 0.3s ease;
  color: var(--text-primary);
}

.complication-badge:hover {
  border-color: var(--accent-gold);
  background: var(--secondary);
  transform: translateY(-3px);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  color: var(--text-secondary);
}

.spinner {
  width: 60px;
  height: 60px;
  border: 3px solid var(--border);
  border-top: 3px solid var(--accent-gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 2rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Navigation Floating */
.nav-floating {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.wishlist-link-btn, .wishlist-toggle-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
  border: none;
  font-size: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.wishlist-link-btn {
  background: white;
  color: #ff4757;
}

.wishlist-toggle-btn {
  background: var(--bg-card);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  color: var(--text-primary);
  font-size: 1.2rem;
}

.wishlist-toggle-btn.active {
  background: rgba(255, 71, 87, 0.1);
  border-color: #ff4757;
}

.wishlist-link-btn .badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4757;
  color: white;
  font-size: 0.7rem;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  border: 2px solid white;
}

.wishlist-link-btn:hover, .wishlist-toggle-btn:hover {
  transform: scale(1.1);
}

@media (max-width: 1024px) {
  .detail-container {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .watch-showcase {
    position: relative;
    top: 0;
  }

  .watch-title {
    font-size: 3rem;
  }

  .specs-grid {
    grid-template-columns: 1fr;
  }
}

.watch-actions {
  display: flex;
  gap: 1.5rem;
  margin-top: 3rem;
  padding-top: 3rem;
  border-top: 1px solid var(--border);
}

.btn-primary-luxury {
  background: var(--accent-gold);
  color: var(--primary);
  border: none;
  padding: 1.5rem 2.5rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  cursor: pointer;
  transition: var(--transition);
  flex: 1;
}

.btn-primary-luxury:hover {
  background: #fff;
}

.btn-secondary-luxury {
  background: transparent;
  color: var(--accent-gold);
  border: 1px solid var(--accent-gold);
  padding: 1.5rem 2.5rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  cursor: pointer;
  transition: var(--transition);
  flex: 1;
}

.btn-secondary-luxury:hover {
  background: var(--accent-gold);
  color: var(--primary);
}

@media (max-width: 768px) {
  .watch-actions {
    flex-direction: column;
  }
}
</style>
