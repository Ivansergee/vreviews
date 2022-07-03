<template>
  <div>
    <div class="tabs is-medium">
      <ul>
        <li :class="[activeTab === 'profile' ? 'is-active' : '']">
          <a @click="setActiveTab('profile')">Профиль</a>
        </li>
        <li :class="[activeTab === 'reviews' ? 'is-active' : '']">
          <a @click="setActiveTab('reviews')">Отзывы</a>
        </li>
        <li :class="[activeTab === 'bookmarks' ? 'is-active' : '']">
          <a @click="setActiveTab('bookmarks')">Закладки</a>
        </li>
      </ul>
    </div>
    <div class="columns profile" v-if="activeTab == 'profile'">
      <div class="column is-one-third">
        image
      </div>
      <div class="column is-two-thirds">
        info
      </div>
    </div>
    <div class="reviews" v-if="activeTab == 'reviews'">
      <p>Reviews</p>
    </div>
    <div class="bookmarks" v-if="activeTab == 'bookmarks'">
      <p>Bookmarks</p>
    </div>
  </div>
</template>

<style scoped>

</style>

<script>
import axios from 'axios'
import Product from '../components/Product.vue'

export default {
  components: {
    Product
  },
  data() {
    return {
      activeTab: 'profile',
    }
  },
  mounted() {
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    }
  },
}
</script>