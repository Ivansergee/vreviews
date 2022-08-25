<template>
  <div class="container">
    <!-- <h2></h2>
    <div class="tabs is-medium">
      <ul>
        <li :class="[activeTab === 'products' ? 'is-active' : '']">
          <a @click="activeTab = 'products'">Жидкости</a>
        </li>
        <li :class="[activeTab === 'brands' ? 'is-active' : '']">
          <a @click="activeTab = 'brands'">Бренды</a>
        </li>
        <li :class="[activeTab === 'producers' ? 'is-active' : '']">
          <a @click="activeTab = 'producers'">Производители ({{ bookmarksCount }})</a>
        </li>
      </ul>
    </div>
    <div class="products" v-if="activeTab == 'bookmarks'">
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
      />
      <a
        class="button is-success"
        @click="getNextBookmarks()"
        v-if="nextBookmarks && bookmarksCount > 10"
      >Показать ещё</a>
    </div> -->
    {{ $route.query.q }}
  </div>
</template>

<style scoped>  

</style>

<script>
// import axios from 'axios';
// import moment from 'moment';

// import Product from '../components/Product.vue';


export default {
  components: {
    // Product,
    // Brand,
    // Producer,
  },
  data() {
    return {
      activeTab: 'products',
    }
  },
  mounted() {

  },
  methods: {

  },
}
</script>