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

    <RouterView />
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
