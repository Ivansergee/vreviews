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
    <div class="columns profile" v-if="activeTab == 'profile'">
      <div class="column is-one-third">
        <figure class="avatar image is-square">
          <img src="https://bulma.io/images/placeholders/256x256.png">
        </figure>
      </div>
      <div class="column is-two-thirds">
        <p><strong class="title is-6">Имя </strong><span>Foobar</span></p>
        <p><strong class="title is-6">Email </strong><span>Foobar</span></p>
        <p><strong class="title is-6">Возраст </strong><span>Foobar</span></p>
        <p><strong class="title is-6">Город </strong><span>Foobar</span></p>
        <p><strong class="title is-6">Telegram </strong><span>Foobar</span></p>
        <p><strong class="title is-6">VK </strong><span>Foobar</span></p>
        <p><strong class="title is-6">Youtube </strong><span>Foobar</span></p>
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
      <p>Bookmarks</p>
    </div>
  </div>
</template>

<style scoped>
  .avatar {
    margin: auto;
  }
  
  .avatar>img {
    max-width: 250px;
    max-height: 250px;
  }
</style>

<script>
import axios from 'axios'
import Product from '../components/Product.vue'
import ProfileReview from '../components/ProfileReview.vue'

export default {
  components: {
    Product,
    ProfileReview
  },
  data() {
    return {
      activeTab: 'profile',
      reviews: null,
    }
  },
  mounted() {
    this.getReviews();
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async getReviews() {
      this.$store.commit('setIsLoading', true)

      const username = this.$store.state.username

      await axios
        .get(`/reviews/?author__username=${username}`)
        .then(response => {
            this.reviews = response.data;
            console.log(this.reviews);
        })
        .catch(error => {
          console.log(error)
        })
      
      this.$store.commit('setIsLoading', false)
    },
    async getUserInfo() {

    },
    async getBookmarks() {

    },
  },
}
</script>