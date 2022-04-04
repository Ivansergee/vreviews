import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BrandView from '../views/BrandView.vue'
import LiquidsView from '../views/LiquidsView.vue'
import ProductView from '../views/ProductView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/liqs',
    name: 'liquids-list',
    component: LiquidsView
  },
  {
    path: '/liqs/brand',
    name: 'brand-list',
    component: BrandView
  },
  {
    path: '/liqs/brand/liq_id',
    name: 'liquid-detail',
    component: ProductView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
