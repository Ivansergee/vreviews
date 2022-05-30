import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: null,
    isLoading: false,
    username: null,
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.username = localStorage.getItem('username')
        state.isAuthenticated = true
      } else {
        state.token = null
        state.isAuthenticated = false
      }
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    setUsername(state, username) {
      state.username = username
    },
    removeToken(state) {
      state.token = null
      state.isAuthenticated = false
      state.username = null
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    showLoginRequired() {
      state.loginRequired = true
    }
  },
  actions: {
  },
  modules: {
  }
})
