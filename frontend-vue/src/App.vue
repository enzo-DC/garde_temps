<script setup>
import { RouterView } from 'vue-router'
import { onMounted, onUnmounted, ref } from 'vue'
import ThreeBackground from './components/ThreeBackground.vue'

const cursorX = ref(0)
const cursorY = ref(0)
const cursorOuterX = ref(0)
const cursorOuterY = ref(0)
const isPointer = ref(false)

const updateCursor = (e) => {
  cursorX.value = e.clientX
  cursorY.value = e.clientY
  
  // Custom check for interactive elements
  const target = e.target
  isPointer.value = 
    window.getComputedStyle(target).cursor === 'pointer' || 
    target.tagName === 'A' || 
    target.tagName === 'BUTTON' ||
    target.closest('button') ||
    target.closest('a')
}

let rafId

const animateCursor = () => {
  // Smooth follow for outer circle
  const dx = cursorX.value - cursorOuterX.value
  const dy = cursorY.value - cursorOuterY.value
  
  cursorOuterX.value += dx * 0.15
  cursorOuterY.value += dy * 0.15
  
  rafId = requestAnimationFrame(animateCursor)
}

const currency = ref(localStorage.getItem('currency') || 'EUR')
const exchangeRates = {
  EUR: 1,
  USD: 1.08,
  CHF: 0.94
}
const currencySymbols = {
  EUR: '€',
  USD: '$',
  CHF: 'CHF'
}

const formatPrice = (price) => {
  const rate = exchangeRates[currency.value]
  const converted = price * rate
  const symbol = currencySymbols[currency.value]
  
  if (currency.value === 'CHF') {
    return new Intl.NumberFormat('fr-CH').format(Math.round(converted)) + ' ' + symbol
  }
  return symbol + ' ' + new Intl.NumberFormat(currency.value === 'USD' ? 'en-US' : 'fr-FR').format(Math.round(converted))
}

const changeCurrency = (newCurrency) => {
  currency.value = newCurrency
  localStorage.setItem('currency', newCurrency)
}

onMounted(() => {
  window.addEventListener('mousemove', updateCursor)
  animateCursor()
})

onUnmounted(() => {
  window.removeEventListener('mousemove', updateCursor)
  cancelAnimationFrame(rafId)
})
</script>

<template>
  <div id="app">
    <!-- Custom Cursor -->
    <div 
      class="custom-cursor" 
      :style="{ transform: `translate3d(${cursorX}px, ${cursorY}px, 0)` }"
      :class="{ 'pointer-hover': isPointer }"
    ></div>
    <div 
      class="custom-cursor-outer" 
      :style="{ transform: `translate3d(${cursorOuterX}px, ${cursorOuterY}px, 0)` }"
      :class="{ 'pointer-hover': isPointer }"
    ></div>

    <ThreeBackground />

    <!-- Global Header / Currency Switcher -->
    <header class="global-navbar">
      <div class="nav-left">
        <div class="currency-selector">
          <button 
            v-for="curr in ['EUR', 'USD', 'CHF']" 
            :key="curr"
            :class="{ active: currency === curr }"
            @click="changeCurrency(curr)"
          >
            {{ curr }}
          </button>
        </div>
      </div>
      <div class="nav-brand" @click="router.push('/')">GARDE-TEMPS</div>
      <div class="nav-right">
        <!-- Optional: Account, Searchicon etc -->
      </div>
    </header>

    <RouterView :formatPrice="formatPrice" :currency="currency" />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  cursor: none !important; /* Hide default cursor */
}

:root {
  --primary: #050505;
  --secondary: #0d0d0d;
  --accent-gold: #c5a059; /* Muted Champagne Gold */
  --accent-brass: #8e7341;
  --text-primary: #f5f5f5;
  --text-secondary: #a0a0a0;
  --text-muted: #555555;
  --bg-card: rgba(15, 15, 15, 0.85);
  --border: rgba(197, 160, 89, 0.15);
  --font-display: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@200;300;400;500;600&display=swap');

html {
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-body);
  background: transparent;
  color: var(--text-primary);
  line-height: 1.6;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

#app {
  min-height: 100vh;
}

/* Global Navbar */
.global-navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 4rem;
  z-index: 1000;
  background: rgba(5, 5, 5, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
}

.nav-brand {
  font-family: var(--font-display);
  font-size: 1.5rem;
  letter-spacing: 0.3em;
  color: var(--accent-gold);
  cursor: pointer;
  font-weight: 600;
}

.currency-selector {
  display: flex;
  gap: 1.5rem;
}

.currency-selector button {
  background: none;
  border: none;
  color: var(--text-muted);
  font-family: var(--font-body);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: var(--transition);
  padding: 0.5rem 0;
  border-bottom: 1px solid transparent;
}

.currency-selector button:hover, .currency-selector button.active {
  color: var(--accent-gold);
}

.currency-selector button.active {
  border-bottom: 1px solid var(--accent-gold);
}

/* Custom Cursor Styles */
.custom-cursor {
  position: fixed;
  top: -5px;
  left: -5px;
  width: 10px;
  height: 10px;
  background-color: var(--accent-gold);
  border-radius: 50%;
  pointer-events: none;
  z-index: 10000;
  transition: width 0.3s, height 0.3s, background-color 0.3s;
}

.custom-cursor-outer {
  position: fixed;
  top: -20px;
  left: -20px;
  width: 40px;
  height: 40px;
  border: 1px solid var(--accent-gold);
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  transition: width 0.3s, height 0.3s, top 0.3s, left 0.3s, border-color 0.3s;
}

.custom-cursor.pointer-hover {
  width: 60px;
  height: 60px;
  top: -30px;
  left: -30px;
  background-color: rgba(212, 175, 55, 0.15);
}

.custom-cursor-outer.pointer-hover {
  width: 80px;
  height: 80px;
  top: -40px;
  left: -40px;
  border-color: var(--accent-rose);
}

/* Scrollbar Customization */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--primary);
}

::-webkit-scrollbar-thumb {
  background: var(--accent-gold);
  border-radius: 0;
}

@media (max-width: 1024px) {
  * {
    cursor: auto !important;
  }
  .custom-cursor, .custom-cursor-outer {
    display: none;
  }
}
</style>
