<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import * as THREE from 'three'

const container = ref(null)
let scene, camera, renderer, particles, torus
let mouseX = 0
let mouseY = 0
let targetX = 0
let targetY = 0

const onMouseMove = (event) => {
  mouseX = (event.clientX - window.innerWidth / 2)
  mouseY = (event.clientY - window.innerHeight / 2)
}

const init = () => {
  scene = new THREE.Scene()
  
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.z = 5

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  container.value.appendChild(renderer.domElement)

  // Subtle Wireframe Sphere (Like an armillary sphere or movement part)
  const geometry = new THREE.SphereGeometry(4, 32, 32)
  const material = new THREE.MeshStandardMaterial({ 
    color: 0xc5a059, 
    wireframe: true,
    transparent: true,
    opacity: 0.1
  })
  torus = new THREE.Mesh(geometry, material) // Keeping variable name 'torus' for compatibility
  scene.add(torus)

  // Champagne Dust Particles
  const particlesGeometry = new THREE.BufferGeometry()
  const particlesCount = 800
  const posArray = new Float32Array(particlesCount * 3)

  for(let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 20
  }

  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
  const particlesMaterial = new THREE.PointsMaterial({
    size: 0.015,
    color: 0xc5a059,
    transparent: true,
    opacity: 0.4,
    blending: THREE.AdditiveBlending
  })

  particles = new THREE.Points(particlesGeometry, particlesMaterial)
  scene.add(particles)

  // Soft Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.2)
  scene.add(ambientLight)

  const light1 = new THREE.PointLight(0xc5a059, 1)
  light1.position.set(10, 10, 10)
  scene.add(light1)

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('resize', onResize)

  animate()
}

const onResize = () => {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

const animate = () => {
  requestAnimationFrame(animate)

  targetX = mouseX * 0.0002
  targetY = mouseY * 0.0002

  // Ultra slow, elegant rotation
  torus.rotation.y += 0.001
  torus.rotation.z += 0.0005
  
  scene.rotation.x += (targetY - scene.rotation.x) * 0.02
  scene.rotation.y += (targetX - scene.rotation.y) * 0.02

  particles.rotation.y += 0.0002

  renderer.render(scene, camera)
}

onMounted(() => {
  init()
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('resize', onResize)
  if (renderer) {
    renderer.dispose()
  }
})
</script>

<template>
  <div ref="container" class="three-container"></div>
</template>

<style scoped>
.three-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1; /* Right behind the content */
  pointer-events: none;
  background: #05050a;
}
</style>
