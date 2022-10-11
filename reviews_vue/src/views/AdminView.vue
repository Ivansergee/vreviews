<template>
    <div class="container products" v-if="products">
      <p class="title">Неопубликованное</p>
      <AdminProduct
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :brand="product.brand"
        :image="product.thumbnail_url"
        :product_slug="product.slug"
        :description="product.description"
        :flavors="product.flavors"
        @approved="approve"
      />
    </div>
</template>

<style scoped>

</style>

<script>
import axios from 'axios'
import AdminProduct from '../components/AdminProduct.vue'

export default {
  components: {
    AdminProduct
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
        .get('/admin/')
        .then(response => {
          this.products = response.data.results;
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    },

    approve(e) {
      for (var i in this.products) {
        if (this.products[i].slug == e) {
          this.products.splice(i, 1);
        }
      }
    }
  },
}
</script>