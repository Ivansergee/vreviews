import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BrandView from '../views/BrandView.vue'
import LiquidsView from '../views/LiquidsView.vue'
import ProductView from '../views/ProductView.vue'
import LogIn from '../views/LogIn.vue'
import SignUp from '../views/SignUp.vue'
import CreateProduct from '../views/CreateProduct'
import AdminView from '../views/AdminView'
import ProfileView from '../views/ProfileView'

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
    path: '/brand/:brand_slug',
    name: 'brand-list',
    component: BrandView
  },
  {
    path: '/product/:product_slug',
    name: 'product-detail',
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
  {
    path: '/admin',
    name: 'admin',
    component: AdminView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
