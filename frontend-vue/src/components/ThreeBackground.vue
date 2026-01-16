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

  // Torus Knot Geometry (More complex and impressive)
  const geometry = new THREE.TorusKnotGeometry(10, 0.1, 100, 16)
  const material = new THREE.MeshStandardMaterial({ 
    color: 0xd4af37, 
    metalness: 1,
    roughness: 0.2,
  })
  torus = new THREE.Mesh(geometry, material)
  scene.add(torus)

  // Particles
  const particlesGeometry = new THREE.BufferGeometry()
  const particlesCount = 2000
  const posArray = new Float32Array(particlesCount * 3)

  for(let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 40
  }

  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
  const particlesMaterial = new THREE.PointsMaterial({
    size: 0.02,
    color: 0xd4af37,
    transparent: true,
    opacity: 0.6
  })

  particles = new THREE.Points(particlesGeometry, particlesMaterial)
  scene.add(particles)

  // Lighting
  const mainLight = new THREE.DirectionalLight(0xffffff, 2)
  mainLight.position.set(1, 1, 2)
  scene.add(mainLight)
  
  const ambientLight = new THREE.AmbientLight(0x404040, 1)
  scene.add(ambientLight)

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

  targetX = mouseX * 0.0005
  targetY = mouseY * 0.0005

  torus.rotation.y += 0.005
  torus.rotation.z += 0.002
  
  // Smooth mouse follow
  scene.rotation.x += (targetY - scene.rotation.x) * 0.05
  scene.rotation.y += (targetX - scene.rotation.y) * 0.05

  particles.rotation.y += 0.0005

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
