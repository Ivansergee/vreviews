import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import BrandView from '../views/BrandView.vue';
import ProducerView from '../views/ProducerView.vue';
import LiquidsView from '../views/LiquidsView.vue';
import ProductView from '../views/ProductView.vue';
import CreateProduct from '../views/CreateProduct.vue';
import AdminView from '../views/AdminView.vue';
import ProfileView from '../views/ProfileView.vue';
import ActivateView from '../views/ActivateView.vue';
import ResetPasswordView from '../views/ResetPasswordView.vue';
import SearchView from '../views/SearchView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    meta: {
      title: 'Главная'
    },
    component: HomeView
  },
  {
    path: '/top-liqs',
    name: 'liquids-list',
    meta: {
      title: 'Топ жидкостей'
    },
    component: LiquidsView
  },
  {
    path: '/producer/:producer_slug',
    name: 'producer-detail',
    component: ProducerView
  },
  {
    path: '/brand/:brand_slug',
    name: 'brand-detail',
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
    meta: {
      title: 'Добавление продукта'
    },
    component: CreateProduct
  },
  {
    path: '/admin',
    name: 'admin',
    meta: {
      title: 'Администрирование'
    },
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
    meta: {
      title: 'Активация аккаунта'
    },
    component: ActivateView
  },
  {
    path: '/password-reset/:uid/:token',
    name: 'reset-password',
    meta: {
      title: 'Сброс пароля'
    },
    component: ResetPasswordView
  },
  {
    path: '/search/:query',
    name: 'search',
    meta: {
      title: 'Поиск'
    },
    component: SearchView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} | VapeRate`;
  }
  next();
})

export default router
