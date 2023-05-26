import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import BrandView from '../views/BrandView.vue';
import ProducerView from '../views/ProducerView.vue';
import LiquidsView from '../views/LiquidsView.vue';
import BrandsView from '../views/BrandsView.vue';
import ProductView from '../views/ProductView.vue';
import AddView from '../views/AddView.vue';
import AddReviewView from '../views/AddReviewView.vue';
import AdminView from '../views/AdminView.vue';
import ProfileView from '../views/ProfileView.vue';
import ActivateView from '../views/ActivateView.vue';
import ResetPasswordView from '../views/ResetPasswordView.vue';
import SearchView from '../views/SearchView.vue';
import ContactsView from '../views/ContactsView.vue';
import DisposablesView from '../views/DisposablesView.vue';
import NotFoundView from '../views/NotFoundView.vue';

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
    path: '/top-brands',
    name: 'brands-list',
    meta: {
      title: 'Топ брендов'
    },
    component: BrandsView
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
    path: '/add/:type?',
    name: 'add',
    meta: {
      title: 'Добавить'
    },
    component: AddView
  },
  {
    path: '/add-review',
    name: 'add-review',
    meta: {
      title: 'Добавить отзыв'
    },
    component: AddReviewView
  },
  {
    path: '/dashboard',
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
  {
    path: '/contacts',
    name: 'contacts',
    meta: {
      title: 'Контакты'
    },
    component: ContactsView
  },
  {
    path: '/disposables',
    name: 'disposables',
    meta: {
      title: 'Топ одноразок'
    },
    component: DisposablesView
  },
  {
    path: '/:pathMatch(.*)*',
    meta: {
      title: 'Страница не найдена'
    },
    name: 'not-found',
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} | VapeRate`;
  }
  next();
})

export default router
