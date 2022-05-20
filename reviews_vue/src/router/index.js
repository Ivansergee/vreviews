import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BrandView from '../views/BrandView.vue'
import LiquidsView from '../views/LiquidsView.vue'
import ProductView from '../views/ProductView.vue'
import LogIn from '../views/LogIn.vue'
import SignUp from '../views/SignUp.vue'
import CreateProduct from '../views/CreateProduct'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/top-liqs',
    name: 'liquids-list',
    component: LiquidsView
  },
  {
    path: '/:brand_slug',
    name: 'brand-list',
    component: BrandView
  },
  {
    path: '/:brand_slug/:product_slug',
    name: 'liquid-detail',
    component: ProductView
  },
  {
    path: '/login',
    name: 'login',
    component: LogIn
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp
  },
  {
    path: '/add-liquid',
    name: 'add-liquid',
    component: CreateProduct
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
