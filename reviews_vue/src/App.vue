<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link class="navbar-item" to="/"
          ><strong>VReviews</strong></router-link
        >

        <a
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div
        class="navbar-menu"
        id="navbar-menu"
        :class="{ 'is-active': showMobileMenu }"
      >
        <div class="navbar-start">
          <router-link class="navbar-item" :to="{ name: 'liquids-list' }"
            >Жидкости</router-link>
          <router-link class="navbar-item" to="/">Одноразки</router-link>
          <router-link class="navbar-item" :to="{ name: 'add-liquid' }"
            >Добавить</router-link>
        </div>

        <div class="navbar-end" v-if="$store.state.isAuthenticated">
          <router-link class="navbar-item" :to="{ name: 'admin' }" v-if="$store.state.isAdmin">
            Администрирование
          </router-link>
          <router-link class="navbar-item profile" :to="{ name: 'profile' }">
            <span class="icon-text">
              <span class="icon">
                <i class="fa-solid fa-user-large fa-lg"></i>
              </span>
              <span>{{ $store.state.username }}</span>
            </span>
          </router-link>
          <a class="navbar-item" @click="logout()">
            <span class="logout">Выход</span>
          </a>
        </div>

        <div class="navbar-end" v-else>
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-blue" @click="showLogIn = true"
                >Вход</a>
              <router-link class="button is-success" :to="{ name: 'signup' }"
                >Регистрация</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div
      class="is-loading-bar has-text-centered"
      :class="{ 'is-loading': $store.state.isLoading }"
    >
      <div class="lds-dual-ring"></div>
    </div>
    
    <div class="modal" :class="{ 'is-active': showLogIn }">
      <div class="modal-background"></div>
      <div class="modal-content">
        <LogIn />
      </div>
    </div>

    <main class="section">
      <router-view />
    </main>

    <footer class="footer">
      <p class="has-text-centered">VReviews 2022</p>
    </footer>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

import LogIn from './components/LogIn.vue'

export default {
  components: {
    LogIn
  },
  data() {
    return {
      showMobileMenu: false,
      showLogIn: false,
    };
  },
  beforeCreate() {
    this.$store.commit("initializeStore");

    const token = this.$store.state.token;

    if (token) {
      axios.defaults.headers.common["Authorization"] = "Token " + token;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  },
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = "";

      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("userid");
      localStorage.removeItem("isAdmin");


      this.$store.commit("removeToken");

      this.$router.push("/");
    },
    showLoginRequired() {
      toast({
        message: "Необходимо авторизоваться!",
        type: "is-danger",
        dismissible: true,
        duration: 3000,
        pauseOnHover: true,
        position: "top-center",
      });
    },
  },
  mounted() {},
};
</script>


<style lang="scss">
@import "../node_modules/bulma";
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css");

html {
  background: #f5f5f5;
}

html,
body,
#app {
  height: 100%;
  margin: 0;
}

.logout .profile {
  text-decoration: underline;
}

.icon .logout {
  margin: auto 1.5em;
}

.icon-text {
  text-decoration: underline;
}

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  &.is-loading {
    height: 80px;
  }
}

</style>
