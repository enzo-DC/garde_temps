<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
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
}

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Montserrat:wght@200;300;400;500;600;700&display=swap');

body {
  font-family: var(--font-body);
  background: #000;
  color: var(--text-primary);
  line-height: 1.6;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
}
</style>
