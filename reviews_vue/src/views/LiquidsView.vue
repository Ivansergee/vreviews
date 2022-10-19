<template>
    <div class="products container" v-if="products">
      <p class="title">Топ жидкостей</p>
      <div class="columns is-vcentered is-hidden-mobile list-header">
        <div class="column">
          <p>Изображение</p>
        </div>

        <div class="column">
          <p>Название/Бренд</p>
        </div>

        <div class="column">
          <p>Описание</p>
        </div>

        <div class="column">
          <p>Вкусы</p>
        </div>

        <div class="column">
          <p>Никотин</p>
        </div>

        <div class="column">
          <p>Рейтинг</p>
        </div>
      </div>
      <Product
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :brand="product.brand"
        :image="product.thumbnail_url"
        :product_slug="product.slug"
        :description="product.description"
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
.list-header {
  margin-bottom: 0;
  font-weight: 500;
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
        .get('/products/?ordering=-avg_score,-created_at')
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