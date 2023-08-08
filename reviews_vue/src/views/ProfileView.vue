<template>
  <div class="container">
    <div class="columns profile" v-if="userInfo">
      <div class="column is-4">
        <figure class="avatar image is-1by1">
          <img :src="userInfo.profile.avatar" />
        </figure>
        <div class="edit-info" v-if="$store.state.username === $route.params.username">
          <a class="button" @click="showEditAvatar = true">Сменить фото</a>
          <a class="button" @click="showEditUserInfo = true">Редактировать</a>
        </div>
      </div>
      <div class="column is-8">
        <p>
          <strong class="title is-6">Имя </strong
          ><span>{{ userInfo.username }}</span>
        </p>
        <p>
          <strong class="title is-6">Возраст </strong
          ><span>{{ getAge(userInfo.profile.birthday) || "-" }}</span>
        </p>
        <p>
          <strong class="title is-6">Город </strong
          ><span>{{ userInfo.profile.city || "-" }}</span>
        </p>
        <p>
          <strong class="title is-6">Telegram </strong
          ><span>{{ userInfo.profile.tg || "-" }}</span>
        </p>
        <p>
          <strong class="title is-6">VK </strong
          ><span>{{ userInfo.profile.vk || "-" }}</span>
        </p>
        <p>
          <strong class="title is-6">Youtube </strong
          ><span>{{ userInfo.profile.yt || "-" }}</span>
        </p>
        <p class="mt-5"><strong class="title is-6">Обо мне </strong></p>
        <p>{{ userInfo.profile.about || "-" }}</p>
      </div>
    </div>

    <Devices v-if="userInfo" :devices="userInfo.devices" :getUserInfo="getUserInfo"/>

    <UserInfoForm
      v-if="showEditUserInfo && userInfo"
      :birthday="userInfo.profile.birthday"
      :city="userInfo.profile.city"
      :tg="userInfo.profile.tg"
      :vk="userInfo.profile.vk"
      :yt="userInfo.profile.yt"
      :about="userInfo.profile.about"
      @changedUserInfo="
        getUserInfo();
        showEditUserInfo = false;
      "
      @close="showEditUserInfo = false"
    />
    <div class="modal" :class="{ 'is-active': showEditAvatar }" v-if="avatar">
      <div class="modal-background" @click="showEditAvatar = false"></div>
      <div class="modal-content">
        <div class="box">
          <div class="level is-mobile">
            <div class="level-left">
              <p class="title is-4">Изменение фото профиля</p>
            </div>
            <div class="level-right">
              <button class="delete is-medium" aria-label="close" @click="showEditAvatar = false"></button>
            </div>
          </div>
          <div class="field">
            <div class="control" v-if="avatar">
              <cropper
                class="cropper"
                ref="cropper"
                :src="avatar.src"
                :stencil-props="{
                  handlers: {},
                  movable: false,
                  scalable: false,
                }"
                :stencil-size="{
                  width: 300,
                  height: 300,
                }"
                image-restriction="stencil"
                @change="change"
              />
            </div>
          </div>

          <div class="file has-name mb-2">
            <label class="file-label">
              <input
                class="file-input"
                type="file"
                accept="image/png, image/jpeg"
                @change="uploadImage($event)"
                name="image"
              />
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
                <span class="file-label"> Выберите файл </span>
              </span>
              <span class="file-name">{{ avatar.name }}</span>
            </label>
          </div>

          <div class="field">
            <div class="control">
              <button
                class="button is-dark"
                @click="editAvatar()"
                :class="{ 'is-loading': changeAvatarLoading }"
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
.avatar > img {
  background-color: white;
  max-width: 250px;
  max-height: 250px;
}
</style>

<script>
import axios from "axios";
import moment from "moment";

import UserInfoForm from "../components/UserInfoForm.vue";
import Devices from "../components/Devices/Devices.vue";
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";

export default {
  components: {
    UserInfoForm,
    Devices,
    Cropper,
  },
  data() {
    return {
      showEditUserInfo: false,
      showEditAvatar: false,
      showDeviceForm: false,
      avatar: {
        src: null,
        type: null,
        name: null,
        file: null,
      },
      userInfo: null,
      changeAvatarLoading: false,
    };
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    change({ canvas }) {
      canvas.toBlob((blob) => {
        this.avatar.file = blob;
      }, this.avatar.type);
    },

    uploadImage(event) {
      const { files } = event.target;
      if (files && files[0]) {
        if (this.avatar.src) {
          URL.revokeObjectURL(this.avatar.src);
        }
        const src = URL.createObjectURL(files[0]);

        this.avatar.src = src;
        this.avatar.type = files[0].type;
        this.avatar.name = files[0].name;
      }
    },

    async editAvatar() {
      const username = this.$store.state.username;

      const formData = new FormData();
      formData.append('avatar', this.avatar.file, this.avatar.name);

      this.changeAvatarLoading = true;
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
      })
      .catch((error) => {
        console.log(error);
      });
      this.changeAvatarLoading = false;
      this.showEditAvatar = false;
      this.avatar = {
        src: null,
        type: null,
        name: null,
        file: null,
      },
      this.getUserInfo();
    },

    getAge(date) {
      return moment().diff(date, "years");
    },

    async getUserInfo() {
      this.$store.commit("setIsLoading", true);

      const username = this.$route.params.username;

      await axios
        .get(`/user/${username}/`)
        .then((response) => {
          this.userInfo = response.data;
          this.setTitle(this.userInfo.username);
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    setTitle(title) {
      document.title = `Профиль ${title} | VapeRate`;
    }
  },
};
</script>