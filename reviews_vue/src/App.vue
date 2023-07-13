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
          <router-link class="navbar-item" :to="{ name: 'brands-list' }"
            >Бренды</router-link>
          <router-link
            class="navbar-item"
            :to="{ name: 'add' }"
            >Добавить</router-link
          >
          <router-link class="navbar-item" :to="{ name: 'contacts' }"
            >Контакты</router-link
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
          <router-link
            class="navbar-item profile"
            :to="{
              name: 'profile',
              params: { username: $store.state.username },
            }"
          >
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
              @keydown.enter="search"
              v-model="searchQuery"
            />
          </p>
          <p class="control is-flex-grow-0">
            <button class="button" @click="search">Найти</button>
          </p>
        </div>
      </div>
    </nav>

    <AdminNavbar v-if="adminNavbar"/>
    <AddNavbar v-if="addNavbar"/>
    <ProfileNavbar v-if="profileNavbar"/>

    <div class="loading" v-if="$store.state.isLoading">
      <PulseLoader :loading="$store.state.isLoading" :size="loaderSize" />
    </div>

    <main class="main-content" :class="{ 'section': $route.name != 'home' }">
      <div class="modal" :class="{ 'is-active': showLogIn }">
        <div class="modal-background" @click="showLogIn = false"></div>
        <div class="modal-content">
          <LogIn
            @logged="showLogIn = false"
            @showRegister="showSignUp = true"
            @showResetPassword="showResetPassword = true"
            @showResendActivation="showResendActivation = true"
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
        <div class="modal-background" @click="showResetPassword = false"></div>
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
                  @click="showResetPassword = false"
                ></button>
              </div>
            </div>

            <form @submit.prevent="resetPassword">
              <div class="field">
                <label>Email</label>
                <div class="control">
                  <input type="email" class="input" v-model="email" />
                </div>
                <p class="help">
                  Введите email, указанный при регистрации. На него будет
                  отправлена ссылка для сброса пароля.
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

      <div class="modal" :class="{ 'is-active': showResendActivation }">
        <div
          class="modal-background"
          @click="showResendActivation = false"
        ></div>
        <div class="modal-content">
          <div class="box">
            <div class="level">
              <div class="level-left">
                <h1 class="title">Активация аккаунта</h1>
              </div>
              <div class="level-right">
                <button
                  class="delete is-medium"
                  aria-label="close"
                  @click="showResetPassword = false"
                ></button>
              </div>
            </div>

            <form @submit.prevent="resendActivation">
              <div class="field">
                <label>Email</label>
                <div class="control">
                  <input type="email" class="input" v-model="email" />
                </div>
                <p class="help">Введите email, указанный при регистрации.</p>
              </div>

              <div class="notification is-danger" v-if="errors.length">
                <p v-for="error in errors" :key="error">{{ error }}</p>
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
      <router-view />
    </main>

    <footer class="footer">
      <p class="has-text-centered">VapeRate 2022</p>
    </footer>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

import LogIn from "./components/LogIn.vue";
import SignUp from "./components/SignUp.vue";
import AdminNavbar from "./components/AdminNavbar.vue";
import AddNavbar from "./components/AddNavbar.vue";
import ProfileNavbar from "./components/ProfileNavbar.vue";
import PulseLoader from "vue-spinner/src/PulseLoader.vue";

export default {
  components: {
    LogIn,
    SignUp,
    PulseLoader,
    AdminNavbar,
    AddNavbar,
    ProfileNavbar
  },
  data() {
    return {
      showMobileMenu: false,
      showLogIn: false,
      showSignUp: false,
      showSearch: false,
      showResetPassword: false,
      showResendActivation: false,
      email: "",
      searchQuery: "",
      errors: [],
      loaderSize: "25px",
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
  computed: {
    adminNavbar() {
      if (this.$store.state.isAdmin && this.$route.path.startsWith('/dashboard')) {
        return true
      }
      return null
    },
    addNavbar() {
      if (this.$route.path.startsWith('/add')) {
        return true
      }
      return null
    },
    profileNavbar() {
      if (this.$route.path.startsWith('/profile')) {
        return true
      }
      return null
    },
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
        .post("users/reset_password/", { email: this.email })
        .then(() => {
          toast({
            message: "На указанную почту направлена ссылка для сброса пароля.",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            position: "top-center",
          });
          this.email = "";
          this.showResetPassword = false;
        })
        .catch((error) => {
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

    async resendActivation() {
      this.errors = [];
      await axios
        .post("/users/resend_activation/", { email: this.email })
        .then(() => {
          toast({
            message: "На указанную почту направлена ссылка для активации.",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            position: "top-center",
          });
          this.showResendActivation = false;
          this.email = "";
        })
        .catch((error) => {
          this.errors.push(error.response.data[0]);
        });
    },

    search() {
      if (this.searchQuery) {
        this.$router.push({
          name: "search",
          params: { query: this.searchQuery },
        });
      }
    },
  }
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

#wrapper {
  display: flex;
  flex-direction: column;
}

.loading {
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-content {
  min-height: 100vh;
  display: flex;
}

.footer {
  display: flex;
  align-items: center;
  justify-content: center;
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
