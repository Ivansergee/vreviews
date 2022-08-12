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
          <a @click="activeTab = 'bookmarks'">Закладки ({{ bookmarksCount }})</a>
        </li>
      </ul>
    </div>
    <div class="columns profile" v-if="activeTab == 'profile' && userInfo">
      <div class="column is-4">
        <figure class="avatar image is-1by1">
          <img :src="userInfo.profile.avatar">
        </figure>
        <a class="button" @click="showEditUserInfo = true">Редактировать</a>
      </div>
      <div class="column is-8">
        <p><strong class="title is-6">Имя </strong><span>{{ userInfo.username }}</span></p>
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
      :birthday=userInfo.profile.birthday
      :city=userInfo.profile.city
      :tg=userInfo.profile.tg
      :vk=userInfo.profile.vk
      :yt=userInfo.profile.yt
      :about=userInfo.profile.about
      @changedUserInfo="getUserInfo(); showEditUserInfo=false"
      @close="showEditUserInfo=false"
    />

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
import UserInfoForm from '../components/UserInfoForm.vue';


export default {
  components: {
    Bookmark,
    ProfileReview,
    UserInfoForm,
  },
  data() {
    return {
      activeTab: 'profile',
      showEditUserInfo: false,
      reviews: null,
      userInfo: null,
      bookmarks: [],
      bookmarksCount: null,
      nextBookmarks: null,
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
        })
        .catch(error => {
          console.log(error)
        })
      
      this.$store.commit('setIsLoading', false)
    },

    async getBookmarks() {
      this.$store.commit('setIsLoading', true)

      const username = this.$store.state.username

      await axios
        .get(`/products/?bookmarks_author=${username}&ordering=-bookmarks__created_at`)
        .then(response => {
            this.bookmarks.push(...response.data.results);
            this.nextBookmarks = response.data.next;
            this.bookmarksCount = response.data.count;
        })
        .catch(error => {
          console.log(error)
        })
      
      this.$store.commit('setIsLoading', false)
    },

    async getNextBookmarks() {
      await axios
        .get(this.nextBookmarks)
        .then(response => {
            this.bookmarks.push(...response.data.results);
            this.nextBookmarks = response.data.next;
        })
        .catch(error => {
          console.log(error)
        })
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
}
</script>