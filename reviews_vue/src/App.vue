<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link class="navbar-item" to="/"
          ><strong>VapeRate</strong></router-link
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
            >Жидкости</router-link
          >
          <router-link class="navbar-item" to="/">Одноразки</router-link>
          <router-link class="navbar-item" :to="{ name: 'add-liquid' }"
            >Добавить</router-link
          >
          <a
            class="navbar-item"
            @click="showSearch = !showSearch"
            :class="{ active: showSearch }"
          >
            <i
              class="fa-solid fa-magnifying-glass fa-lg"
              :class="{ active: showSearch }"
            ></i>
          </a>
        </div>

        <div class="navbar-end" v-if="$store.state.isAuthenticated">
          <router-link
            class="navbar-item"
            :to="{ name: 'admin' }"
            v-if="$store.state.isAdmin"
          >
            Администрирование
          </router-link>
          <router-link class="navbar-item profile" :to="{ name: 'profile', params: {username: $store.state.username} }">
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
              <a class="button is-blue" @click="showLogIn = true">Вход</a>
              <a class="button is-success" @click="showSignUp = true"
                >Регистрация</a
              >
            </div>
          </div>
        </div>
      </div>
    </nav>
    <nav class="navbar is-dark" v-if="showSearch">
      <div class="navbar-item is-flex-grow-1">
        <div class="field has-addons is-flex-grow-1 mx-6">
          <p class="control is-flex-grow-1">
            <input
              class="input"
              type="text"
              placeholder="Название продукта, бренда или производителя"
              v-model="searchQuery"
            />
          </p>
          <p class="control is-flex-grow-0">
            <button class="button" @click="search()">Найти</button>
          </p>
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
      <div class="modal-background" @click="showLogIn = false"></div>
      <div class="modal-content">
        <LogIn
          @logged="showLogIn = false"
          @showRegister="showSignUp = true"
          @showResetPassword="showResetPassword = true"
        />
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showSignUp }">
      <div class="modal-background" @click="showSignUp = false"></div>
      <div class="modal-content">
        <SignUp @signed="showSignUp = false" @showLogin="showLogIn = true" />
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showResetPassword }">
      <div class="modal-background" @click="showResetPassword=false"></div>
      <div class="modal-content">
        <div class="box">
          <div class="level">
            <div class="level-left">
              <h1 class="title">Сбросить пароль</h1>
            </div>
            <div class="level-right">
              <button
                class="delete is-medium"
                aria-label="close"
                @click="showResetPassword=false"
              ></button>
            </div>
          </div>

          <form @submit.prevent="resetPassword()">
            <div class="field">
              <label>Email</label>
              <div class="control">
                <input type="email" class="input" v-model="email">
              </div>
              <p class="help">
                Введите email, указанный при регистрации. На него будет отправлена ссылка для сброса пароля.
              </p>
            </div>

            <div class="level">
              <div class="level-left">
                <button class="button is-dark">Отправить</button>
              </div>
            </div>

          </form>
        </div>
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

import LogIn from "./components/LogIn.vue";
import SignUp from "./components/SignUp.vue";

export default {
  components: {
    LogIn,
    SignUp,
  },
  data() {
    return {
      showMobileMenu: false,
      showLogIn: false,
      showSignUp: false,
      showSearch: false,
      showResetPassword: false,
      email:'',
      searchQuery: '',
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

    async resetPassword() {
      await axios
      .post('users/reset_password/', {'email': this.email})
      .then(()=>{
        toast({
          message: 'На указанную почту направлена ссылка для сброса пароля.',
          type: 'is-success',
          dismissible: true,
          pauseOnHover: true,
          position: 'top-center',
        });
        this.email = '';
        this.showResetPassword = false;
      })
      .catch((error)=>{
        console.log(error.response.data);
      });
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

    search() {
      if (this.searchQuery) {
        this.$router.push({name: 'search', params: {'query': this.searchQuery} });
      }
    }
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

.search {
  flex-grow: 1;
}

p.control {
  display: flex;
}

.active {
  color: #00d1b2;
  background-color: #292929;
}
</style>
