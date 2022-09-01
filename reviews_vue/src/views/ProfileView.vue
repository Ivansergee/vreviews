<template>
  <div class="container">
    <div class="tabs is-medium">
      <ul>
        <li :class="[activeTab === 'profile' ? 'is-active' : '']">
          <a @click="activeTab = 'profile'">Профиль</a>
        </li>
        <li :class="[activeTab === 'reviews' ? 'is-active' : '']">
          <a @click="activeTab = 'reviews'">Отзывы и оценки</a>
        </li>
        <li :class="[activeTab === 'bookmarks' ? 'is-active' : '']" v-if="$store.state.username === $route.params.username">
          <a @click="activeTab = 'bookmarks'"
            >Закладки ({{ bookmarksCount }})</a
          >
        </li>
      </ul>
    </div>
    <div class="columns profile" v-if="activeTab == 'profile' && userInfo">
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
    <div class="reviews" v-if="activeTab == 'reviews'">
      <p v-if="!reviews.length">Нет ни одного отзыва</p>
      <ProfileReview
        v-for="review in reviews"
        :key="review.id"
        :id="review.id"
        :product="review.product.name"
        :productSlug="review.product.slug"
        :productImage="review.product.thumbnail_url"
        :score="review.score"
        :text="review.text"
        :created_at="review.created_at"
        :likesCount="review.likes_count"
        :dislikesCount="review.dislikes_count"
        :comments="review.comments"
      />
    </div>
    <div class="bookmarks" v-if="activeTab == 'bookmarks' && $store.state.username === $route.params.username">
      <p v-if="!bookmarks.length">Нет закладок</p>
      <Bookmark
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        :id="bookmark.id"
        :name="bookmark.name"
        :image="bookmark.thumbnail_url"
        :slug="bookmark.slug"
        :avg_score="bookmark.avg_score"
        :flavors="bookmark.flavors"
        :reviews_amount="bookmark.reviews_count"
        :score_amount="bookmark.score_count"
        @deleted="deleteBookmark"
      />
      <a
        class="button is-success"
        @click="getNextBookmarks()"
        v-if="nextBookmarks && bookmarksCount > 10"
        >Показать ещё</a>
    </div>

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
          <div class="field">
            <label><span class="subtitle">Аватар</span></label>
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

          <div class="file has-name">
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
        <button
          class="modal-close is-large"
          aria-label="close"
          @click="showEditAvatar = false"
        ></button>
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

import Bookmark from "../components/Bookmark.vue";
import ProfileReview from "../components/ProfileReview.vue";
import UserInfoForm from "../components/UserInfoForm.vue";
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";

export default {
  components: {
    Bookmark,
    ProfileReview,
    UserInfoForm,
    Cropper,
  },
  data() {
    return {
      activeTab: "profile",
      showEditUserInfo: false,
      showEditAvatar: false,
      avatar: {
        src: null,
        type: null,
        name: null,
        file: null,
      },
      reviews: null,
      userInfo: null,
      bookmarks: [],
      bookmarksCount: null,
      nextBookmarks: null,
      changeAvatarLoading: false,
    };
  },
  mounted() {
    this.getReviews();
    this.getUserInfo();
    this.getBookmarks();
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

    async getReviews() {
      this.$store.commit("setIsLoading", true);

      const username = this.$route.params.username;

      await axios
        .get(`/reviews/?author=${username}`)
        .then((response) => {
          this.reviews = response.data.results;
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    async getUserInfo() {
      this.$store.commit("setIsLoading", true);

      const username = this.$route.params.username;

      await axios
        .get(`/user/${username}/`)
        .then((response) => {
          this.userInfo = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    async getBookmarks() {
      if (this.$store.state.username === this.$route.params.username){
        this.$store.commit("setIsLoading", true);

        const username = this.$store.state.username;
        await axios
          .get(
            `/products/?bookmarks_author=${username}&ordering=-bookmarks__created_at`
          )
          .then((response) => {
            this.bookmarks.push(...response.data.results);
            this.nextBookmarks = response.data.next;
            this.bookmarksCount = response.data.count;
          })
          .catch((error) => {
            console.log(error);
          });

        this.$store.commit("setIsLoading", false);
      }
    },

    async getNextBookmarks() {
      await axios
        .get(this.nextBookmarks)
        .then((response) => {
          this.bookmarks.push(...response.data.results);
          this.nextBookmarks = response.data.next;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    deleteBookmark(id) {
      for (var i in this.bookmarks) {
        if (this.bookmarks[i].id == id) {
          this.bookmarks.splice(i, 1);
          this.bookmarksCount -= 1;
        }
      }
    },
  },
};
</script>