import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    isAdmin: false,
    token: null,
    isLoading: false,
    username: null,
    devices: []
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token');
        state.username = localStorage.getItem('username');
        state.isAdmin = localStorage.getItem('isAdmin') === 'true';
        state.isAuthenticated = true;
        state.devices = JSON.parse(localStorage.getItem('devices'));
      } else {
        state.token = null;
        state.isAuthenticated = false;
        state.isAdmin = false;
      }
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
    },
    setUsername(state, username) {
      state.username = username;
    },
    setIsAdmin(state, isAdmin) {
      state.isAdmin = isAdmin;
    },
    setDevices(state, devices) {
      state.devices = devices;
    },
    removeToken(state) {
      state.token = null;
      state.isAuthenticated = false;
      state.username = null;
      state.isAdmin = false;
      state.devices = null;
    },
    setIsLoading(state, status) {
      state.isLoading = status;
    },
    showLoginRequired() {
      state.loginRequired = true;
    }
  },
  actions: {
  },
  modules: {
  }
})
