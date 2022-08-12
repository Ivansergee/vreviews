<template>
  <div>
    <div class="box">
        <div class="level">
          <div class="level-left">
            <h1 class="title">Изменение пароля</h1>
          </div>
        </div>

        <div>

          <div class="field">
            <label>Новый пароль</label>
            <div class="control">
              <input
                type="password"
                class="input"
                v-model="new_password"
              />
            </div>
          </div>

          <div class="field">
            <label>Подтвердите пароль</label>
            <div class="control">
              <input
                type="password"
                class="input"
                v-model="re_new_password"
              />
            </div>
          </div>

          <div class="level">
            <div class="level-left">
              <button
                class="button is-dark"
                :class="{ 'is-loading': isLoading }"
                @click="setPassword()"
              >
                Сохранить
              </button>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { toast } from "bulma-toast";

export default {
  data() {
    return {
      new_password: '',
      re_new_password: '',
      isLoading: false,
    }
  },
  methods:{
    async setPassword() {
      this.isLoading = true;
      const data = {
        uid: this.$route.params.uid,
        token: this.$route.params.token,
        new_password: this.new_password,
        re_new_password: this.re_new_password,
      };

      await axios
      .post('users/reset_password_confirm/', data)
      .then(() => {
        toast({
          message: "Пароль изменен. Теперь вы можете войти с новым паролем.",
          type: "is-success",
          dismissible: true,
          pauseOnHover: true,
          duration: 10000,
          position: "top-center",
        });
        this.$router.replace('/');
      })
      .catch(error => {
        toast({
          message: "Что-то пошло не так!",
          type: "is-danger",
          dismissible: true,
          pauseOnHover: true,
          duration: 10000,
          position: "top-center",
        });
        this.$router.replace('/');
        console.log(error.response.data);
      });
      this.isLoading = false;
    },
  },
}
</script>