<template>
    <div class="products container" v-if="products">
      <p class="title">Топ жидкостей</p>
      <Product
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :brand="product.brand.name"
        :image="product.thumbnail_url"
        :product_slug="product.slug"
        :description="product.description"
        :brand_slug="product.brand.slug"
        :avg_score="product.avg_score"
        :flavors="product.flavors"
        :reviews_count="product.reviews_count"
        :score_count="product.score_count"
      />
      <div class="loadNext">
        <a
          class="button is-success"
          @click="getNextLiquids"
          v-if="nextLiquids"
          >Показать ещё</a>
      </div>
    </div>
</template>

<style scoped>
.loadNext {
  display: flex;
  justify-content: center;
}

</style>

<script>
import axios from 'axios';
import Product from '../components/Product.vue';


export default {
  components: {
    Product
  },
  data() {
    return {
      products: null,
      nextLiquids: null,
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
          this.nextLiquids = response.data.next;
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },

    async getNextLiquids() {
      await axios
        .get(this.nextLiquids)
        .then((response) => {
          this.products.push(...response.data.results);
          this.nextLiquids = response.data.next;
        })
        .catch((error) => {
          console.log(error);
        });
    },

  },

    
}
</script>