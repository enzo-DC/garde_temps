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
  --primary: #0a0a0f;
  --secondary: #1a1a2e;
  --accent-gold: #d4af37;
  --accent-rose: #b76e79;
  --text-primary: #ffffff;
  --text-secondary: #c4c4c4;
  --text-muted: #808080;
  --bg-card: rgba(26, 26, 46, 0.6);
  --border: rgba(212, 175, 55, 0.2);
  --font-display: 'Cormorant Garamond', serif;
  --font-body: 'Montserrat', sans-serif;
  --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Montserrat:wght@200;300;400;500;600;700&display=swap');

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
  background: linear-gradient(var(--accent-gold), var(--accent-rose));
  border-radius: 5px;
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
