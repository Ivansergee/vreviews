<template>
    <div class="container products" v-if="products">
      <p class="title">Неопубликованное</p>
      <AdminProduct
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :brand="product.brand.name"
        :image="product.thumbnail_url"
        :product_slug="product.slug"
        :brand_slug="product.brand.slug"
        :description="product.description"
        :flavors="product.flavors"
        :nic_content="product.nic_content"
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
          console.log(this.products);
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    }
  },
}
</script>