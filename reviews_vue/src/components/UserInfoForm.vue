<template>
  <div class="modal is-active">
    <div class="modal-background" @click="$emit('close')"></div>
    <div class="modal-content">
      <div class="box">
      <div class="level">
          <div class="level-left">
              <h1 class="title">Изменение информации профиля</h1>
          </div>
          <div class="level-right">
              <button class="delete is-medium" aria-label="close" @click="$emit('close')"></button>
          </div>
      </div>

      <div>
          <div class="field">
              <label>Дата рождения</label>
              <div class="control">
                  <input type="date" class="input" v-model="birthday">
              </div>
          </div>

          <div class="field">
              <label>Город</label>
              <div class="control">
                  <input type="text" class="input" v-model="city">
              </div>
          </div>

          <div class="field">
              <label>Telegram</label>
              <div class="control">
                  <input type="text" class="input" v-model="tg">
              </div>
          </div>

          <div class="field">
              <label>VK</label>
              <div class="control">
                  <input type="text" class="input" v-model="vk">
              </div>
          </div>

          <div class="field">
              <label>Youtube</label>
              <div class="control">
                  <input type="text" class="input" v-model="yt">
              </div>
          </div>

          <div class="field">
              <label>Обо мне</label>
              <div class="control">
                  <textarea class="textarea" v-model="about"></textarea>
              </div>
          </div>

          <div class="level">
              <div class="level-left">
                  <button
                    class="button is-dark"
                    @click="showEditUsername = true"
                  >Изменить имя</button>
                  <button
                    class="button is-dark mx-2"
                    @click="showEditPassword = true"
                  >Изменить пароль</button>
                  <button
                    class="button is-dark"
                    @click="showEditEmail = true"
                  >Изменить email</button>
              </div>
          </div>
          <div class="level">
              <div class="level-left">
                  <button
                    class="button is-dark"
                    :class="{ 'is-loading': isLoading }"
                    @click="submitForm()"
                  >Сохранить</button>
              </div>
          </div>
      </div>
    </div>
    </div>

    <ChangeUsername
      v-if="showEditUsername"
      @close="showEditUsername=false"
    />
    <ChangePassword
      v-if="showEditPassword"
      @close="showEditPassword=false"
    />

  </div>
</template>

<style scoped>
</style>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

import ChangeUsername from './ChangeUsername.vue';
import ChangePassword from './ChangePassword.vue';
import ChangeEmail from './ChangeEmail.vue';

export default {
  props: [
    'birthday',
    'city',
    'tg',
    'vk',
    'yt',
    'about',
  ],
  emits: ["changedUserInfo", "close"],
  components: {
    ChangeUsername,
    ChangePassword,
    ChangeEmail,
  },
  data() {
    return {
      errors: {},
      isLoading: false,
      showEditUsername: false,
      showEditPassword: false,
      showEditEmail: false,
    };
  },
  methods: {
    async submitForm() {
      this.errors = {};
      if (Object.keys(this.errors).length == 0) {

        const username = this.$store.state.username;

        const formData = new FormData();
        if (this.birthday) formData.append('birthday', this.birthday);
        if (this.about) formData.append('about', this.about);
        if (this.city) formData.append('city', this.city);
        if (this.tg) formData.append('tg', this.tg);
        if (this.vk) formData.append('vk', this.vk);
        if (this.yt) formData.append('yt', this.yt);

        this.isLoading = true;
        await axios
        .patch(`/user/${username}/edit/`, formData)
        .then(() => {
          toast({
            message: "Информация изменена",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "top-center",
          });
          this.$emit('changedUserInfo');
        })
        .catch(error => {
          console.log(error);
          if (error.response) {
            for (const property in error.response.data) {
              this.errors[property] = error.response.data[property];
            }
          } else if (error.message || error.request) {
            this.errors['other'] = "Что-то пошло не так. Попробуйте ещё раз.";
          }
          console.log(this.errors);
        });
        this.isLoading = false;
      }
    },

  },
};
</script>
