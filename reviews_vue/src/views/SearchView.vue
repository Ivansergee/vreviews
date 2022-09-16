<template>
  <div class="container">
    <h1 class="title is-3">Результаты поиска по запросу "{{ $route.params.query }}"</h1>
    <div class="tabs is-medium">
      <ul>
        <li :class="[activeTab === 'products' ? 'is-active' : '']">
          <a @click="activeTab = 'products'">Жидкости ({{ products.length }})</a>
        </li>
        <li :class="[activeTab === 'brands' ? 'is-active' : '']">
          <a @click="activeTab = 'brands'">Бренды ({{ brands.length }})</a>
        </li>
        <li :class="[activeTab === 'producers' ? 'is-active' : '']">
          <a @click="activeTab = 'producers'">Производители ({{ producers.length }})</a>
        </li>
      </ul>
    </div>
    <div class="products" v-if="activeTab == 'products'">
      <p v-if="products.length === 0">Нет совпадений</p>
      <Product
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :image="product.thumbnail_url"
        :product_slug="product.slug"
        :brand_slug="product.brand.slug"
        :avg_score="product.avg_score ? product.avg_score : '-'"
        :flavors="product.flavors"
        :reviews_count="product.reviews_count ? product.reviews_count : '0'"
        :score_count="product.score_count ? product.score_count : '0'"
      />
      <!-- <a
        class="button is-success"
        @click="getNextBookmarks()"
        v-if="nextBookmarks && bookmarksCount > 10"
      >Показать ещё</a> -->
    </div>

    <div class="brands" v-if="activeTab == 'brands'">
      <p v-if="brands.length === 0">Нет совпадений</p>
      <Brand
        v-for="brand in brands"
        :key="brand.id"
        :name="brand.name"
        :image="brand.thumbnail_url"
        :slug="brand.slug"
        :avg_score="brand.avg_score ? brand.avg_score : '-'"
        :reviews_count="brand.reviews_count ? brand.reviews_count : '0'"
        :score_count="brand.score_count ? brand.score_count : '0'"
      />
      <!-- <a
        class="button is-success"
        @click="getNextBookmarks()"
        v-if="nextBookmarks && bookmarksCount > 10"
      >Показать ещё</a> -->
    </div>

    <div class="producers" v-if="activeTab == 'producers'">
      <p v-if="producers.length === 0">Нет совпадений</p>
      <Producer
        v-for="producer in producers"
        :key="producer.id"
        :name="producer.name"
        :image="producer.thumbnail_url"
        :slug="producer.slug"
        :avg_score="producer.avg_score ? producer.avg_score : '-'"
        :reviews_count="producer.reviews_count ? producer.reviews_count : '0'"
        :score_count="producer.score_count ? producer.score_count : '0'"
      />
      <!-- <a
        class="button is-success"
        @click="getNextBookmarks()"
        v-if="nextBookmarks && bookmarksCount > 10"
      >Показать ещё</a> -->
    </div>
  </div>
</template>

<style scoped>  

</style>

<script>
import axios from 'axios';

import Product from '../components/Product.vue';
import Brand from '../components/Brand.vue';
import Producer from '../components/Producer.vue';


export default {
  components: {
    Product,
    Brand,
    Producer,
  },
  data() {
    return {
      activeTab: 'products',
      products: [],
      brands: [],
      producers: [],
    }
  },
  watch: { 
      '$route.params.query': {
          handler: function() {
            this.getProducts();
            this.getBrands();
            this.getProducers();
          },
          deep: true,
          immediate: true
        }
  },
  mounted() {
    this.getProducts();
    this.getBrands();
    this.getProducers();
  },
  methods: {
    async getProducts(){
      this.$store.commit('setIsLoading', true)

      const query = this.$route.params.query;

      await axios
        .get(`/products/?search=${query}`)
        .then(response => {
          this.products = response.data.results;
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },

    async getBrands(){
      this.$store.commit('setIsLoading', true)

      const query = this.$route.params.query;

      await axios
        .get(`/brands/?search=${query}`)
        .then(response => {
          this.brands = response.data.results;
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },

    async getProducers(){
      this.$store.commit('setIsLoading', true)

      const query = this.$route.params.query;

      await axios
        .get(`/producers/?search=${query}`)
        .then(response => {
          this.producers = response.data.results;
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },
  },
}
</script>