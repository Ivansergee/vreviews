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
        <li :class="[activeTab === 'bookmarks' ? 'is-active' : '']">
          <a @click="activeTab = 'bookmarks'">Закладки</a>
        </li>
      </ul>
    </div>
    <div class="columns profile" v-if="activeTab == 'profile' && userInfo">
      <div class="column is-4">
        <figure class="avatar image is-1by1">
          <img :src="userInfo.profile.avatar">
        </figure>
        <a class="button" @click="showEdit = true">Редактировать</a>
      </div>
      <div class="column is-8">
        <p><strong class="title is-6">Имя </strong><span>{{ userInfo.username }}</span></p>
        <p v-if="userInfo.email"><strong class="title is-6">Email </strong><span>{{ userInfo.email }}</span></p>
        <p><strong class="title is-6">Возраст </strong><span>{{ getAge(userInfo.profile.birthday) || '-' }}</span></p>
        <p><strong class="title is-6">Город </strong><span>{{ userInfo.profile.city || '-' }}</span></p>
        <p><strong class="title is-6">Telegram </strong><span>{{ userInfo.profile.tg || '-' }}</span></p>
        <p><strong class="title is-6">VK </strong><span>{{ userInfo.profile.vk || '-' }}</span></p>
        <p><strong class="title is-6">Youtube </strong><span>{{ userInfo.profile.yt || '-' }}</span></p>
        <p class="mt-5"><strong class="title is-6">Обо мне </strong></p>
        <p>{{ userInfo.profile.about || '-' }}</p>
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
          :productImage="review.product.image_url"
          :score="review.score"
          :text="review.text"
          :created_at="review.created_at"
          :likesCount="review.likes_count"
          :dislikesCount="review.dislikes_count"
          :comments="review.comments"
        />
    </div>
    <div class="bookmarks" v-if="activeTab == 'bookmarks'">
      <p v-if="!bookmarks.length">Нет закладок</p>
      <Bookmark
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        :id="bookmark.id"
        :name="bookmark.name"
        :image="bookmark.image_url"
        :slug="bookmark.slug"
        :avg_score="bookmark.avg_score"
        :flavors="bookmark.flavors"
        :reviews_amount="bookmark.get_reviews_amount"
        :score_amount="bookmark.get_score_amount"
        @deleted="deleteBookmark"
      />
      <a class="button is-success" :class="{'disabled': !nextBookmarks}" @click="getBookmarks()">Показать ещё</a>
    </div>

    <div class="modal" :class="{ 'is-active': showEdit }">
      <div class="modal-background" @click="showEdit = false"></div>
      <div class="modal-content">
        <div class="box">
        <div class="level">
            <div class="level-left">
                <h1 class="title">Изменение информации профиля</h1>
            </div>
            <div class="level-right">
                <button class="delete is-medium" aria-label="close" @click="showEdit = false"></button>
            </div>
        </div>

        <div>
            <div class="field">
                <label>Дата рождения</label>
                <div class="control">
                    <input type="date" class="input" v-model="profileData.birthday">
                </div>
            </div>

            <div class="field">
                <label>Город</label>
                <div class="control">
                    <input type="text" class="input" v-model="profileData.city">
                </div>
            </div>

            <div class="field">
                <label>Telegram</label>
                <div class="control">
                    <input type="text" class="input" v-model="profileData.tg">
                </div>
            </div>

            <div class="field">
                <label>VK</label>
                <div class="control">
                    <input type="text" class="input" v-model="profileData.vk">
                </div>
            </div>

            <div class="field">
                <label>Youtube</label>
                <div class="control">
                    <input type="text" class="input" v-model="profileData.yt">
                </div>
            </div>

            <div class="field">
                <label>Обо мне</label>
                <div class="control">
                    <textarea class="textarea" v-model="profileData.about"></textarea>
                </div>
            </div>

            <div class="level">
                <div class="level-left">
                    <button
                      class="button is-dark"
                      :class="{ 'is-loading': isLoading }"
                      @click="editUserInfo()"
                    >Сохранить</button>
                </div>
            </div>
        </div>
    </div>
      </div>
    </div>
  </div>
</template>

<style scoped>  
  .avatar>img {
    background-color: white;
    max-width: 250px;
    max-height: 250px;
  }
</style>

<script>
import axios from 'axios';
import moment from 'moment';

import Bookmark from '../components/Bookmark.vue';
import ProfileReview from '../components/ProfileReview.vue';


export default {
  components: {
    Bookmark,
    ProfileReview,
  },
  data() {
    return {
      activeTab: 'profile',
      showEdit: false,
      reviews: null,
      userInfo: null,
      bookmarks: [],
      bookmarksAmount: null,
      nextBookmarks: null,
      profileData: {
        avatar: null,
        birthday: null,
        city: null,
        tg: null,
        vk: null,
        yt: null,
        about: null,
      },
      isLoading: false,
    }
  },
  mounted() {
    this.getReviews();
    this.getUserInfo();
    this.getBookmarks();
  },
  methods: {
    getAge(date) {
      return moment().diff(date, 'years');
    },

    async getReviews() {
      this.$store.commit('setIsLoading', true)

      const username = this.$store.state.username

      await axios
        .get(`/reviews/?author=${username}`)
        .then(response => {
            this.reviews = response.data.results;
        })
        .catch(error => {
          console.log(error)
        })
      
      this.$store.commit('setIsLoading', false)
    },

    async getUserInfo() {
      this.$store.commit('setIsLoading', true)

      const username = this.$store.state.username

      await axios
        .get(`/user/${username}/`)
        .then(response => {
            this.userInfo = response.data;
            this.profileData.avatar = response.data.profile.avatar;
            this.profileData.birthday = response.data.profile.birthday;
            this.profileData.tg = response.data.profile.tg;
            this.profileData.vk = response.data.profile.vk;
            this.profileData.yt = response.data.profile.yt;
            this.profileData.about = response.data.profile.about;
        })
        .catch(error => {
          console.log(error)
        })
      
      this.$store.commit('setIsLoading', false)
    },

    async editUserInfo(){

      const username = this.$store.state.username;

      const formData = {
        profile__birthday: this.profileData.birthday,
        profile__about: this.profileData.about,
        profile__tg: this.profileData.tg,
        profile__vk: this.profileData.vk,
        profile__yt: this.profileData.yt,
      };

      await axios
        .patch(`/user/${username}/`, formData)
        .then(response => {
            console.log(response);
        })
        .catch(error => {
          console.log(error)
        })
    },

    async getBookmarks() {
      this.$store.commit('setIsLoading', true)
      console.log(this.nextBookmarks);

      const username = this.$store.state.username
      if (!this.nextBookmarks){
        var url = `/products/?bookmarks_author=${username}&ordering=-bookmarks__created_at`
      } else {
        var url = this.nextBookmarks;
      }

      await axios
        .get(url)
        .then(response => {
            this.bookmarks.push(...response.data.results);
            this.nextBookmarks = response.data.next;
            this.bookmarksAmount = response.data.count;
            console.log(this.nextBookmarks);
        })
        .catch(error => {
          console.log(error)
        })
      
      this.$store.commit('setIsLoading', false)
    },

    deleteBookmark(id) {
      for (var i in this.bookmarks) {
        if (this.bookmarks[i].id == id) {
          this.bookmarks.splice(i, 1)
        }
      }
    },
  },
}
</script>