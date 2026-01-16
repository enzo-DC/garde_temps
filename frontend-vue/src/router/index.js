import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import WatchDetail from '../views/WatchDetail.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/watch/:id',
            name: 'watch-detail',
            component: WatchDetail
        },
        {
            path: '/wishlist',
            name: 'wishlist',
            component: () => import('../views/Wishlist.vue')
        }
    ]
})

export default router
