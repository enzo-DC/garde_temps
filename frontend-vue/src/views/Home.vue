<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// State
const watches = ref([])
const totalWatches = ref(0)
const totalBrands = ref(0)
const avgPrice = ref(0)
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)
const showFilters = ref(false)
const comparisonList = ref([])
const showComparisonModal = ref(false)
const wishlist = ref(JSON.parse(localStorage.getItem('wishlist') || '[]'))
const animatedStats = ref({
  watches: 0,
  brands: 0,
  price: 0
})

// Wishlist logic
const toggleWishlist = (id, event) => {
  event.stopPropagation()
  const index = wishlist.value.indexOf(id)
  if (index === -1) {
    wishlist.value.push(id)
  } else {
    wishlist.value.splice(index, 1)
  }
  localStorage.setItem('wishlist', JSON.stringify(wishlist.value))
}

const isInWishlist = (id) => wishlist.value.includes(id)

// Comparison logic
const toggleComparison = (watch, event) => {
  event.stopPropagation()
  const index = comparisonList.value.findIndex(w => w.id === watch.id)
  if (index === -1) {
    if (comparisonList.value.length >= 4) {
      alert('Vous pouvez comparer jusqu\'à 4 montres maximum.')
      return
    }
    comparisonList.value.push(watch)
  } else {
    comparisonList.value.splice(index, 1)
  }
}

const isCompared = (id) => {
  return comparisonList.value.some(w => w.id === id)
}

const removeFromComparison = (id) => {
  comparisonList.value = comparisonList.value.filter(w => w.id !== id)
}

const clearComparison = () => {
  comparisonList.value = []
  showComparisonModal.value = false
}

// Filters
const filters = ref({
  country: '',
  movement: '',
  diameter: '',
  search: '',
  ordering: '-created_at'
})

// Load watches
const loadWatches = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      ...Object.fromEntries(
        Object.entries({
          brand__country: filters.value.country,
          movement_type: filters.value.movement,
          case_diameter__lte: filters.value.diameter,
          search: filters.value.search,
          ordering: filters.value.ordering
        }).filter(([_, v]) => v)
      )
    }
    
    const response = await api.getWatches(params)
    watches.value = response.data.results
    totalPages.value = Math.ceil(response.data.count / 12)
    loading.value = false
    
    // Initialize reveal animations after data loads
    setTimeout(initReveal, 100)
  } catch (error) {
    console.error('Error loading watches:', error)
    loading.value = false
  }
}

// Load stats with animation
const animateValue = (refKey, start, end, duration) => {
  let startTimestamp = null
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp
    const progress = Math.min((timestamp - startTimestamp) / duration, 1)
    animatedStats.value[refKey] = Math.floor(progress * (end - start) + start)
    if (progress < 1) {
      window.requestAnimationFrame(step)
    }
  }
  window.requestAnimationFrame(step)
}

const loadStats = async () => {
  try {
    const [watchesRes, brandsRes] = await Promise.all([
      api.getWatches(),
      api.getBrands()
    ])
    
    totalWatches.value = watchesRes.data.count
    totalBrands.value = brandsRes.data.count
    
    let targetPrice = 0
    if (watchesRes.data.results.length > 0) {
      const sum = watchesRes.data.results.reduce((acc, w) => acc + parseFloat(w.price), 0)
      targetPrice = Math.round(sum / watchesRes.data.results.length)
      avgPrice.value = targetPrice
    }

    // Animate stats
    animateValue('watches', 0, totalWatches.value, 2000)
    animateValue('brands', 0, totalBrands.value, 2000)
    animateValue('price', 0, targetPrice, 2000)
    
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

// PDF Export
const downloadPDF = async (watchIds) => {
  try {
    const response = await api.exportPDF(watchIds)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'catalogue_garde_temps.pdf')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error downloading PDF:', error)
    alert('Erreur lors de la génération du PDF.')
  }
}

// Format price
const formatPrice = (price) => {
  return new Intl.NumberFormat('fr-FR').format(price)
}

// Reset filters
const resetFilters = () => {
  filters.value = {
    country: '',
    movement: '',
    diameter: '',
    search: '',
    ordering: '-created_at'
  }
  currentPage.value = 1
  loadWatches()
}

// Change page
const changePage = (page) => {
  currentPage.value = page
  loadWatches()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Watch filters
const applyFilters = () => {
  currentPage.value = 1
  loadWatches()
}

// Navigate to detail
const goToDetail = (id) => {
  router.push(`/watch/${id}`)
}

// Scroll reveal
const initReveal = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-active')
      }
    })
  }, { threshold: 0.1 })

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el))
}

// 3D Tilt Effect
const handleTilt = (e, card) => {
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

onMounted(() => {
  loadWatches()
  loadStats()
  initReveal()
})
</script>

<template>
  <div class="home">
    <!-- Animated Background -->
    <!-- <div class="animated-bg"></div> -->
    
    <!-- Particles -->
    <!-- <div class="particles">
      <div v-for="i in 30" :key="i" class="particle" 
           :style="{
             left: Math.random() * 100 + '%',
             top: Math.random() * 100 + '%',
             animationDelay: Math.random() * 20 + 's',
             animationDuration: (15 + Math.random() * 10) + 's'
           }"></div>
    </div> -->

    <!-- Navigation Buttons -->
    <div class="nav-floating">
      <button class="wishlist-toggle" @click="router.push('/wishlist')" title="Ma Liste de Souhaits">
        ♥
        <span v-if="wishlist.length" class="badge">{{ wishlist.length }}</span>
      </button>
      
      <button class="filters-toggle" :class="{ active: showFilters }" @click="showFilters = !showFilters">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <!-- Filters Sidebar -->
    <aside class="filters-sidebar" :class="{ active: showFilters }">
      <h2>Filtres</h2>
      <div class="filters-grid">
        <div class="filter-group">
          <label>Pays de Marque</label>
          <select v-model="filters.country" @change="applyFilters" class="filter-select">
            <option value="">Tous les pays</option>
            <option value="Suisse">Suisse</option>
            <option value="Japon">Japon</option>
            <option value="France">France</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Type de Mouvement</label>
          <select v-model="filters.movement" @change="applyFilters" class="filter-select">
            <option value="">Tous les mouvements</option>
            <option value="AUTO">Automatique</option>
            <option value="MANUAL">Manuel</option>
            <option value="QUARTZ">Quartz</option>
            <option value="SOLAR">Solaire</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Diamètre Maximum</label>
          <select v-model="filters.diameter" @change="applyFilters" class="filter-select">
            <option value="">Tous les diamètres</option>
            <option value="38">≤ 38mm</option>
            <option value="40">≤ 40mm</option>
            <option value="42">≤ 42mm</option>
            <option value="44">≤ 44mm</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Recherche</label>
          <input v-model="filters.search" @input="applyFilters" type="text" class="filter-input" placeholder="Nom, référence...">
        </div>

        <div class="filter-group">
          <label>Trier par</label>
          <select v-model="filters.ordering" @change="applyFilters" class="filter-select">
            <option value="-created_at">Plus récentes</option>
            <option value="price">Prix croissant</option>
            <option value="-price">Prix décroissant</option>
            <option value="model_name">Nom A-Z</option>
          </select>
        </div>

        <div class="filter-group">
          <button @click="resetFilters" class="btn-reset">Réinitialiser</button>
        </div>
      </div>
    </aside>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Garde-Temps</h1>
        <p class="hero-subtitle">Collection Exclusive de Montres de Prestige</p>
        <a href="#collection" class="hero-cta" @click.prevent="$el.querySelector('.stats-section').scrollIntoView({ behavior: 'smooth' })">
          Découvrir la Collection
        </a>
      </div>
      <div class="scroll-indicator"></div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section reveal">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">{{ animatedStats.watches }}</div>
            <div class="stat-label">Montres de Prestige</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ animatedStats.brands }}</div>
            <div class="stat-label">Manufactures</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ formatPrice(animatedStats.price) }} €</div>
            <div class="stat-label">Valeur Moyenne</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Watches Grid -->
    <main class="main-content">
      <div class="container">
        <h2 class="section-title">Notre Collection</h2>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Chargement des garde-temps...</p>
        </div>

        <div v-else class="watches-grid">
          <div v-for="(watch, index) in watches" :key="watch.id" 
               class="watch-card reveal" 
               @click="goToDetail(watch.id)"
               @mousemove="handleTilt($event, watch)"
               @mouseleave="resetTilt($event)"
               :style="{ transitionDelay: index * 0.05 + 's' }">
            <div class="watch-image">
              <img v-if="watch.image_url" :src="watch.image_url" :alt="watch.model_name" class="watch-photo" loading="lazy">
              <div v-else class="watch-icon">⌚</div>
              
              <!-- Comparison Toggle -->
              <button 
                class="compare-btn" 
                :class="{ active: isCompared(watch.id) }"
                @click="toggleComparison(watch, $event)"
                title="Comparer"
              >
                <span v-if="isCompared(watch.id)">✓</span>
                <span v-else>+</span>
              </button>

              <!-- Wishlist Toggle -->
              <button 
                class="wishlist-btn" 
                :class="{ active: isInWishlist(watch.id) }"
                @click="toggleWishlist(watch.id, $event)"
                title="Ajouter aux favoris"
              >
                ♥
              </button>
            </div>
            <div class="watch-info">
              <div class="watch-brand">{{ watch.brand_name }} • {{ watch.brand_country }}</div>
              <h3 class="watch-model">{{ watch.model_name }}</h3>
              <div class="watch-details">
                <div class="watch-detail-item">⚙️ <span>{{ watch.movement_display }}</span></div>
                <div class="watch-detail-item">📏 <span>{{ watch.case_diameter }}mm</span></div>
                <div class="watch-detail-item">💎 <span>{{ watch.material_display }}</span></div>
              </div>
              <div class="watch-price">{{ formatPrice(watch.price) }} €</div>
              <div class="watch-reference">Réf. {{ watch.reference_number }}</div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">← Précédent</button>
          <span class="page-info">Page {{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">Suivant →</button>
        </div>
      </div>
    </main>

    <!-- Comparison Bar -->
    <div v-if="comparisonList.length > 0" class="comparison-bar">
      <div class="comparison-items">
        <div v-for="item in comparisonList" :key="item.id" class="comp-mini-item">
          <div class="comp-mini-img">
            <img v-if="item.image_url" :src="item.image_url" alt="">
            <span v-else>⌚</span>
          </div>
          <button class="comp-mini-remove" @click="removeFromComparison(item.id)">×</button>
        </div>
        <div v-for="i in (4 - comparisonList.length)" :key="'empty'+i" class="comp-mini-empty"></div>
      </div>
      <div class="comparison-actions">
        <button v-if="comparisonList.length >= 2" class="btn-compare-now" @click="showComparisonModal = true">
          Comparer ({{ comparisonList.length }})
        </button>
        <button class="btn-clear-comp" @click="clearComparison">Réinitialiser</button>
      </div>
    </div>

    <!-- Comparison Modal -->
    <div v-if="showComparisonModal" class="comparison-modal" @click="showComparisonModal = false">
      <div class="comparison-content" @click.stopPropagation>
        <button class="modal-close" @click="showComparisonModal = false">×</button>
        <div class="modal-header-flex">
          <h2 class="modal-title">Comparatif Haute Horlogerie</h2>
          <button class="btn-export-pdf" @click="downloadPDF(comparisonList.map(w => w.id))">
            📄 Exporter en PDF
          </button>
        </div>
        
        <div class="comparison-table-wrapper">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>Paramètre</th>
                <th v-for="watch in comparisonList" :key="watch.id">
                  <div class="comp-table-header">
                    <img v-if="watch.image_url" :src="watch.image_url" class="comp-table-img">
                    <div v-else class="comp-table-icon">⌚</div>
                    <h3>{{ watch.model_name }}</h3>
                    <p>{{ watch.brand_name }}</p>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Prix</td>
                <td v-for="watch in comparisonList" :key="watch.id" class="price-val">
                  {{ formatPrice(watch.price) }} €
                </td>
              </tr>
              <tr>
                <td>Origine</td>
                <td v-for="watch in comparisonList" :key="watch.id">{{ watch.brand_country }}</td>
              </tr>
              <tr>
                <td>Mouvement</td>
                <td v-for="watch in comparisonList" :key="watch.id">{{ watch.movement_display }}</td>
              </tr>
              <tr>
                <td>Matériau</td>
                <td v-for="watch in comparisonList" :key="watch.id">{{ watch.material_display }}</td>
              </tr>
              <tr>
                <td>Diamètre</td>
                <td v-for="watch in comparisonList" :key="watch.id">{{ watch.case_diameter }} mm</td>
              </tr>
              <tr>
                <td>Étanchéité</td>
                <td v-for="watch in comparisonList" :key="watch.id">{{ watch.water_resistance }} m</td>
              </tr>
              <tr>
                <td>Référence</td>
                <td v-for="watch in comparisonList" :key="watch.id" class="ref-val">{{ watch.reference_number }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>&copy; 2026 Garde-Temps - Collection Exclusive de Montres de Prestige</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.home {
  position: relative;
  min-height: 100vh;
}

.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%);
  z-index: -2;
}

.animated-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 50%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(183, 110, 121, 0.1) 0%, transparent 50%);
  animation: pulse 15s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: var(--accent-gold);
  border-radius: 50%;
  opacity: 0.3;
  animation: float 20s infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-100px) translateX(50px); }
  50% { transform: translateY(-200px) translateX(-50px); }
  75% { transform: translateY(-100px) translateX(100px); }
}

.container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 2rem;
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

.filters-toggle, .wishlist-toggle {
  background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-rose) 100%);
  border: none;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.4);
  position: relative;
}

.wishlist-toggle {
  background: white;
  color: #ff4757;
  font-size: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.wishlist-toggle .badge {
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

.filters-toggle:hover, .wishlist-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 15px 40px rgba(212, 175, 55, 0.6);
}

.filters-toggle span {
  width: 25px;
  height: 2px;
  background: var(--primary);
  transition: all 0.3s ease;
}

.filters-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(7px, 7px);
}

.filters-toggle.active span:nth-child(2) {
  opacity: 0;
}

.filters-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -7px);
}

/* Filters Sidebar */
.filters-sidebar {
  position: fixed;
  top: 0;
  right: -450px;
  width: 450px;
  height: 100vh;
  background: rgba(10, 10, 15, 0.98);
  backdrop-filter: blur(30px);
  border-left: 1px solid var(--border);
  z-index: 999;
  transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
  padding: 6rem 2rem 2rem;
}

.filters-sidebar.active {
  right: 0;
  box-shadow: -20px 0 60px rgba(0, 0, 0, 0.8);
}

.filters-sidebar h2 {
  font-family: var(--font-display);
  font-size: 2.5rem;
  color: var(--accent-gold);
  margin-bottom: 2rem;
  font-weight: 300;
}

.filters-sidebar .modal-title {
  font-family: var(--font-display);
  font-size: 2.5rem;
  color: var(--accent-gold);
  margin-bottom: 0;
}

.modal-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-right: 3rem;
}

.btn-export-pdf {
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid var(--accent-gold);
  color: var(--accent-gold);
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.8rem;
}

.btn-export-pdf:hover {
  background: var(--accent-gold);
  color: var(--primary);
}

.filters-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.filter-group label {
  display: block;
  font-size: 0.75rem;
  color: var(--accent-gold);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 0.75rem;
}

.filter-select, .filter-input {
  width: 100%;
  padding: 1rem 1.5rem;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid var(--border);
  border-radius: 50px;
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.filter-select:focus, .filter-input:focus {
  outline: none;
  border-color: var(--accent-gold);
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
  background: rgba(26, 26, 46, 1);
}

.btn-reset {
  width: 100%;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-rose) 100%);
  border: none;
  border-radius: 50px;
  color: var(--primary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 1rem;
}

.btn-reset:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.4);
}

/* Hero */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, transparent 0%, rgba(10, 10, 15, 0.8) 100%);
  z-index: 1;
}

.hero-content {
  text-align: center;
  z-index: 2;
  position: relative;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 300;
  color: var(--accent-gold);
  margin-bottom: 1rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  animation: fadeInUp 1s ease-out;
  text-shadow: 0 0 40px rgba(212, 175, 55, 0.5);
}

.hero-subtitle {
  font-size: clamp(1rem, 2vw, 1.5rem);
  font-weight: 200;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  margin-bottom: 3rem;
  animation: fadeInUp 1s ease-out 0.2s both;
  color: var(--text-secondary);
}

.hero-cta {
  display: inline-block;
  padding: 1.5rem 4rem;
  background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-rose) 100%);
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  border-radius: 50px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeInUp 1s ease-out 0.4s both;
  box-shadow: 0 10px 40px rgba(212, 175, 55, 0.3);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.hero-cta::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.hero-cta:hover::before {
  left: 100%;
}

.hero-cta:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(212, 175, 55, 0.5);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  animation: bounce 2s infinite;
}

.scroll-indicator::after {
  content: '↓';
  font-size: 2rem;
  color: var(--accent-gold);
}

@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(10px); }
}

/* Stats */
.stats-section {
  padding: 4rem 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  padding: 3rem 2rem;
  border-radius: 20px;
  text-align: center;
  border: 1px solid var(--border);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.4s;
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card:hover {
  transform: translateY(-10px);
  border-color: var(--accent-gold);
  box-shadow: 0 20px 60px rgba(212, 175, 55, 0.3);
}

.stat-value {
  font-size: 4rem;
  font-weight: 300;
  color: var(--accent-gold);
  font-family: var(--font-display);
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.2em;
}

/* Main Content */
.main-content {
  padding: 4rem 0;
}

.section-title {
  font-family: var(--font-display);
  font-size: 3rem;
  font-weight: 300;
  text-align: center;
  margin-bottom: 3rem;
  color: var(--accent-gold);
  letter-spacing: 0.1em;
}

.watches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 3rem;
  margin-bottom: 4rem;
}

.watch-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--border);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  animation: fadeInUp 0.6s ease-out both;
}

.watch-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(183, 110, 121, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.5s;
  pointer-events: none;
  z-index: 1;
}

.watch-card:hover::before {
  opacity: 1;
}

.watch-card:hover {
  transform: translateY(-15px) scale(1.02);
  border-color: var(--accent-gold);
  box-shadow: 0 30px 80px rgba(212, 175, 55, 0.4);
}

.watch-image {
  width: 100%;
  height: 350px;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(10, 10, 15, 0.9) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 6rem;
  position: relative;
  overflow: hidden;
}

.watch-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.watch-card:hover .watch-photo {
  transform: scale(1.1);
}

.watch-image::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.2) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.5s;
}

.watch-card:hover .watch-image::after {
  opacity: 1;
}

.watch-icon {
  filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.5));
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.watch-card:hover .watch-icon {
  transform: scale(1.1) rotate(5deg);
}

.watch-info {
  padding: 2rem;
  position: relative;
  z-index: 2;
}

.watch-brand {
  font-size: 0.75rem;
  color: var(--accent-rose);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 0.75rem;
}

.watch-model {
  font-family: var(--font-display);
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  line-height: 1.3;
}

.watch-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.watch-detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.watch-detail-item span {
  color: var(--text-secondary);
  font-weight: 500;
}

.watch-price {
  font-size: 2.2rem;
  font-weight: 300;
  color: var(--accent-gold);
  font-family: var(--font-display);
  margin-bottom: 0.5rem;
}

.watch-reference {
  font-size: 0.75rem;
  color: var(--text-muted);
  letter-spacing: 0.1em;
}

/* Loading */
.loading {
  text-align: center;
  padding: 4rem 0;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 3px solid var(--border);
  border-top: 3px solid var(--accent-gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Comparison Button on Card */
.compare-btn {
  position: absolute;
  top: 1rem;
  left: 1rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(10, 10, 15, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  color: var(--accent-gold);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
}

.compare-btn:hover {
  background: var(--accent-gold);
  color: var(--primary);
  transform: scale(1.1);
}

.compare-btn.active {
  background: var(--accent-gold);
  color: var(--primary);
  border-color: var(--accent-gold);
}

/* Comparison Bar */
.comparison-bar {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(10, 10, 15, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 50px;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  z-index: 900;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from { transform: translateX(-50%) translateY(100px); opacity: 0; }
  to { transform: translateX(-50%) translateY(0); opacity: 1; }
}

.comparison-items {
  display: flex;
  gap: 0.75rem;
}

.comp-mini-item, .comp-mini-empty {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.05);
  position: relative;
}

.comp-mini-img {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: 12px;
}

.comp-mini-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.comp-mini-img span {
  font-size: 1.5rem;
}

.comp-mini-remove {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent-rose);
  color: white;
  border: none;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.comp-mini-remove:hover {
  transform: scale(1.2);
}

.comparison-actions {
  display: flex;
  gap: 1rem;
}

.btn-compare-now {
  padding: 0.8rem 2rem;
  background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-rose) 100%);
  border: none;
  border-radius: 50px;
  color: var(--primary);
  font-weight: 700;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transition: all 0.3s;
}

.btn-compare-now:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(212, 175, 55, 0.4);
}

.btn-clear-comp {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-muted);
  border-radius: 50px;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-clear-comp:hover {
  border-color: var(--accent-rose);
  color: var(--accent-rose);
}

/* Comparison Modal */
.comparison-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.95);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

.comparison-content {
  background: var(--bg-card);
  border: 1px solid var(--border);
  width: 100%;
  max-width: 1400px;
  max-height: 90vh;
  border-radius: 30px;
  padding: 4rem;
  position: relative;
  overflow-y: auto;
}

.modal-close {
  position: absolute;
  top: 2rem;
  right: 2rem;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 3rem;
  cursor: pointer;
  line-height: 1;
}

.modal-title {
  font-family: var(--font-display);
  font-size: 3rem;
  color: var(--accent-gold);
  text-align: center;
  margin-bottom: 4rem;
  font-weight: 300;
}

.comparison-table-wrapper {
  overflow-x: auto;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
}

.comparison-table th, .comparison-table td {
  padding: 2rem;
  text-align: center;
  border-bottom: 1px solid var(--border);
}

.comparison-table th:first-child, .comparison-table td:first-child {
  text-align: left;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--accent-rose);
  font-size: 0.8rem;
  width: 200px;
}

.comp-table-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.comp-table-img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 15px;
  border: 1px solid var(--border);
}

.comp-table-icon {
  width: 150px;
  height: 150px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
}

.comp-table-header h3 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0;
}

.comp-table-header p {
  font-size: 0.9rem;
  color: var(--accent-gold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0;
}

.price-val {
  font-size: 1.8rem;
  color: var(--accent-gold);
  font-family: var(--font-display);
}

.ref-val {
  font-family: monospace;
  color: var(--text-muted);
  letter-spacing: 2px;
}

@media (max-width: 1024px) {
  .comparison-content {
    padding: 2rem;
  }
  .modal-title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .comparison-bar {
    width: 90%;
    flex-direction: column;
    border-radius: 20px;
    gap: 1rem;
  }
  .comparison-items {
    justify-content: center;
  }
}
/* Reveal Animation */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.reveal-active {
  opacity: 1;
  transform: translateY(0);
}

/* Wishlist Button */
.wishlist-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(10, 10, 15, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
}

.wishlist-btn:hover {
  transform: scale(1.1);
  color: #ff4757;
}

.wishlist-btn.active {
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
  border-color: #ff4757;
}

/* Card Improvements */
.watch-card {
  transform-style: preserve-3d;
  will-change: transform;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--border);
  transition: border-color 0.5s, box-shadow 0.5s;
  cursor: pointer;
  position: relative;
}

.watch-info {
  transform: translateZ(20px);
}

/* Pagination Improvements */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin: 4rem 0;
}

.pagination button {
  padding: 1rem 2.5rem;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 50px;
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.pagination button:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-rose) 100%);
  color: var(--primary);
  border-color: var(--accent-gold);
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.4);
}

.pagination button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  color: var(--text-secondary);
  font-size: 1rem;
  letter-spacing: 0.1em;
}

/* Footer Improvements */
.footer {
  background: rgba(10, 10, 15, 0.95);
  backdrop-filter: blur(20px);
  padding: 5rem 0;
  text-align: center;
  margin-top: 8rem;
  border-top: 1px solid var(--border);
}

.footer p {
  color: var(--text-muted);
  font-size: 0.9rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 3rem;
  }
  
  .watches-grid {
    grid-template-columns: 1fr;
  }
  
  .filters-sidebar {
    width: 100%;
    right: -100%;
  }

  .watch-card {
    transform: none !important; /* Disable tilt on mobile */
  }
}
</style>
