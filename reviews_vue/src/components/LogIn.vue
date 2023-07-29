<template>
  <div class="box">
    <div class="level">
      <div class="level-left">
        <h1 class="title">Вход</h1>
      </div>
      <div class="level-right">
        <button
          class="delete is-medium"
          aria-label="close"
          @click="close()"
        ></button>
      </div>
    </div>

    <form @submit.prevent="submitForm">
      <div class="field">
        <label>Имя пользователя</label>
        <div class="control">
          <input type="text" class="input" v-model="username" />
        </div>
      </div>

      <div class="field">
        <label>Пароль</label>
        <div class="control">
          <input type="password" class="input" v-model="password" />
        </div>
      </div>

      <div class="notification is-danger" v-if="errors.length">
        <p v-for="error in errors" :key="error">{{ error }}</p>
      </div>

      <div class="notification is-danger" v-if="resendActivation">
        <p>Аккаунт не активирован. Пройдите по ссылке в письме на вашей почте для активации (проверьте папку "спам").</p>
        <a @click="close(); $emit('showResendActivation');">Отправить повторно</a>
      </div>

      <div class="level">
        <div class="level-left">
          <a
            @click="
              close();
              $emit('showResetPassword');
            "
            >Не помню пароль</a
          >
        </div>
      </div>

      <div class="level">
        <div class="level-left">
          <button class="button is-dark" :class="{ 'is-loading': isLoading }">
            Войти
          </button>
        </div>
        <div class="level-right">
          <a
            @click="
              close();
              $emit('showRegister');
            "
            >Создать аккаунт</a
          >
        </div>
      </div>
    </form>
  </div>
</template>

<style scoped>
.modal-background {
  background-color: rgb(10 10 10 / 60%);
}
</style>

<script>
import axios from "axios";

export default {
  name: "Log In",
  emits: ["logged", "showRegister", "showResendActivation", "showResetPassword"],
  data() {
    return {
      username: "",
      password: "",
      errors: [],
      isLoading: false,
      resendActivation: false,
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];
      if (this.username === "") {
        this.errors.push("Заполните имя пользователя");
      }
      if (this.password === "") {
        this.errors.push("Введите пароль");
      }

      if (!this.errors.length) {
        const formData = {
          username: this.username,
          password: this.password,
        };

        this.isLoading = true;
        await axios
        .post("token/login/", formData)
        .then((response) => {
          const token = response.data.auth_token;

          this.$store.commit("setToken", token);
          this.$store.commit("setUsername", this.username);

          axios.defaults.headers.common["Authorization"] = "Token " + token;

          localStorage.setItem("token", token);
          localStorage.setItem("username", this.username);
          location.reload();

          this.close();
        })
        .catch((error) => {
          if (error.response) {
            for (const property in error.response.data) {
              if (property === "non_field_errors") {
                if (error.response.data[property][0] === 'User is not active') {
                  this.resendActivation = true;
                } else {
                  this.errors.push(error.response.data[property][0]);
                }
              } else {
                this.errors.push(`${property}: ${error.response.data[property][0]}`);
              }
            }
          } else if (error.message) {
            this.errors.push("Что-то пошло не так. Попробуйте ещё раз.");
          }
        }),(this.isLoading = false);

        if (localStorage.getItem('token')){
          await axios.get("users/me/")
          .then((response) => {
            this.$store.commit("setIsAdmin", response.data.is_staff);
            localStorage.setItem("isAdmin", response.data.is_staff);
            this.$store.commit("setDevices", response.data.devices);
            localStorage.setItem("devices", JSON.stringify(this.$store.state.devices));
          });
        }

      }
    },

    close() {
      this.password = "";
      this.username = "";
      this.errors = [];
      this.$emit("logged");
    },
  },
};
</script>
