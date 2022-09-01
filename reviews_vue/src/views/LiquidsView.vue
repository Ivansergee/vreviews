<template>
    <div class="products" v-if="products">
      <p class="title">Топ жидкостей</p>
      <Product
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :image="product.thumbnail_url"
        :slug="product.slug"
        :avg_score="product.avg_score ? product.avg_score : '-'"
        :flavors="product.flavors"
        :reviews_count="product.reviews_count ? product.reviews_count : '0'"
        :score_count="product.score_count ? product.score_count : '0'"
      />
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
      products: null,
    }
  },
  mounted() {
    this.getProducts()
  },
  methods: {
    async getProducts(){
      this.$store.commit('setIsLoading', true)

      await axios
        .get('/products/?ordering=-avg_score')
        .then(response => {
          this.products = response.data.results;
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    }
  },
}
</script>