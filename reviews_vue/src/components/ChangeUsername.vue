<template>
  <div class="modal is-active">
    <div class="modal-background" @click="$emit('close')"></div>
    <div class="modal-content">
      <div class="box">
        <div class="level">
          <div class="level-left">
            <h1 class="title">Изменение имени пользователя</h1>
          </div>
          <div class="level-right">
            <button
              class="delete is-medium"
              aria-label="close"
              @click="$emit('close')"
            ></button>
          </div>
        </div>

        <div>
          <div class="field">
            <label>Новое имя</label>
            <div class="control">
              <input
                type="text"
                class="input"
                v-model="new_username"
              />
            </div>
            <p class="help is-danger" v-if="errors.new_username">
              {{ errors.new_username[0] }}
            </p>
          </div>

          <div class="field">
            <label>Пароль</label>
            <div class="control">
              <input
                type="password"
                class="input"
                v-model="current_password"
              />
            </div>
            <p class="help is-danger" v-if="errors.current_password">
              {{ errors.current_password[0] }}
            </p>
          </div>

          <div class="level">
            <div class="level-left">
              <button
                class="button is-dark"
                :class="{ 'is-loading': isLoading }"
                @click="submitForm()"
              >
                Сохранить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
  emits: ["close"],
  data() {
    return {
      new_username: '',
      current_password: '',
      errors: {},
      isLoading: false,
    };
  },
  methods: {
    async submitForm() {
      this.errors = {};
      if (Object.keys(this.errors).length == 0) {
        const username = this.$store.state.username;

        const formData = {
          new_username: this.new_username,
          current_password: this.current_password,
        };

        this.isLoading = true;
        await axios
        .post('/users/set_username/', formData)
        .then(() => {
          toast({
            message: "Имя пользователя изменено. Войдите с новыми данными.",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 10000,
            position: "top-center",
          });
          this.$root.logout();
        })
        .catch(error => {
          this.errors = error.response.data;
        })
        this.isLoading = false;
      }
    },
  },
};
</script>
