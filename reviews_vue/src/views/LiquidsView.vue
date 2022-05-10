<template>
    <div class="products" v-if="products">
      <p class="title">Топ жидкостей</p>
      <Product
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :image="product.get_image"
        :absolute_url="product.get_absolute_url"
        :avg_score="product.get_avg_score"
        :flavors="product.flavors"
        :reviews_amount="product.get_reviews_amount"
        :score_amount="product.get_score_amount"
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
        .get('/products/')
        .then(response => {
          this.products = response.data
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    }
  },
}
</script>