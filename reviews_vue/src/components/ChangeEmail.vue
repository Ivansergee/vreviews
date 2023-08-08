<template>
  <div class="modal is-active">
    <div class="modal-background" @click="$emit('close')"></div>
    <div class="modal-content">
      <div class="box">
        <div class="level is-mobile">
          <div class="level-left">
            <p class="title is-4">Изменение почты</p>
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
            <label>Текущий пароль</label>
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

          <div class="field">
            <label>Новый email</label>
            <div class="control">
              <input
                type="email"
                class="input"
                v-model="email"
              />
            </div>
            <p class="help is-danger" v-if="errors.new_email">
              {{ errors.email[0] }}
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
      current_password: '',
      email: '',

      errors: [],
      isLoading: false,
    };
  },
  methods: {
    async submitForm() {
      if (this.errors.length == 0) {
        const username = this.$store.state.username;

        const formData = {
          password: this.current_password,
          email: this.email,
        };

        this.isLoading = true;
        await axios
          .patch(`/user/${username}/edit-email/`, formData)
          .then(() => {
            toast({
              message: "Email изменен.",
              type: "is-success",
              dismissible: true,
              pauseOnHover: true,
              duration: 10000,
              position: "top-center",
            });
          })
          .catch((error) => {
            this.errors = error.response.data;
          });
        this.isLoading = false;
        this.close()
      }
    },
    close(){
      this.email = '';
      this.current_password = '';
      this.errors = [];
      this.$emit('close');
    }
  },
};
</script>