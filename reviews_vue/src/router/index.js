import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import BrandView from '../views/BrandView.vue';
import LiquidsView from '../views/LiquidsView.vue';
import ProductView from '../views/ProductView.vue';
import CreateProduct from '../views/CreateProduct.vue';
import AdminView from '../views/AdminView.vue';
import ProfileView from '../views/ProfileView.vue';
import ActivateView from '../views/ActivateView.vue';
import ResetPasswordView from '../views/ResetPasswordView.vue';

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
    path: '/profile/:username',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/activate/:uid/:token',
    name: 'activate',
    component: ActivateView
  },
  {
    path: '/password-reset/:uid/:token',
    name: 'reset-password',
    component: ResetPasswordView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
