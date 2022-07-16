<template>
  <div>
    <div class="tabs is-medium">
      <ul>
        <li :class="[activeTab === 'profile' ? 'is-active' : '']">
          <a @click="setActiveTab('profile')">Профиль</a>
        </li>
        <li :class="[activeTab === 'reviews' ? 'is-active' : '']">
          <a @click="setActiveTab('reviews')">Отзывы и оценки</a>
        </li>
        <li :class="[activeTab === 'bookmarks' ? 'is-active' : '']">
          <a @click="setActiveTab('bookmarks')">Закладки</a>
        </li>
      </ul>
    </div>
    <div class="columns profile" v-if="activeTab == 'profile' && userInfo">
      <div class="column is-one-third">
        <figure class="avatar image is-square">
          <img :src="userInfo.profile.avatar">
        </figure>
      </div>
      <div class="column is-two-thirds">
        <p><strong class="title is-6">Имя </strong><span>{{ userInfo.username }}</span></p>
        <p v-if="userInfo.email"><strong class="title is-6">Email </strong><span>{{ userInfo.email }}</span></p>
        <p><strong class="title is-6">Возраст </strong><span>{{ userInfo.profile.birthday || '-' }}</span></p>
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
        :avg_score="bookmark.get_avg_score"
        :flavors="bookmark.flavors"
        :reviews_amount="bookmark.get_reviews_amount"
        :score_amount="bookmark.get_score_amount"
        @deleted="deleteBookmark"
      />
    </div>
  </div>
</template>

<style scoped>
  .avatar {
    margin: auto;
    background-color: white;
  }
  
  .avatar>img {
    max-width: 250px;
    max-height: 250px;
    margin: auto;
  }
</style>

<script>
import axios from 'axios';
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
      reviews: null,
      userInfo: null,
      bookmarks: null,
    }
  },
  mounted() {
    this.getReviews();
    this.getUserInfo();
    this.getBookmarks();
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },

    async getReviews() {
      this.$store.commit('setIsLoading', true)

      const username = this.$store.state.username

      await axios
        .get(`/reviews/?author=${username}`)
        .then(response => {
            this.reviews = response.data;
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
            this.bookmarks = response.data;
            console.log(this.bookmarks);
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
    }
  },
}
</script>