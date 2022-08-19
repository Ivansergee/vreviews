import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'


// axios.defaults.baseURL = 'http://188.68.223.142/api'
axios.defaults.baseURL = 'http://localhost:8000/api'

createApp(App).use(store).use(router).mount('#app')
