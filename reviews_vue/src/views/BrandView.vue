<template>
  <div class="container" v-if="brand">
    <div class="level">
      <div class="level-left">
        <h1 class="title level-item">{{ brand.name }}</h1>
      </div>
    </div>
    <div class="columns head">
      <div class="column is-4">
        <figure class="image is-1by1">
          <img
            :src=brand.get_image
          />
        </figure>
      </div>
      <div class="column is-4">
        <div class="content">
          <p><strong>Страна:</strong> {{brand.producer.country}} </p>
          <p><strong>Производитель:</strong> {{brand.producer.name}}  </p>

          <p>{{ brand.description }}</p>
        </div>
      </div>
      <div class="column is-4">
        <div class="content">
          <p class="title is-4">Средняя оценка:</p>
          <div class="tags are-large has-addons">
            <span class="tag"><i class="bi bi-star-fill"></i></span>
            <span class="tag is-primary">{{ brand.get_avg_score }}</span>
          </div>
          <p><strong>Отзывов:</strong> {{ brand.get_reviews_amount }}</p>
          <p><strong>Оценок:</strong> {{ brand.get_score_amount }}</p>
        </div>
      </div>
    </div>

    <div class="products">
      <p class="title">Все вкусы {{ brand.name }}</p>
      <Product
        v-for="product in brand.products"
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
  </div>
</template>

<style scoped>
img {
  max-width: 300px;
  max-height: 300px;
}

.head {
  margin: 2em auto;
  padding: 2em;
  background-color: white;
}
.is-vcentered {
  margin: 2em auto !important;
  height: 100%;
  background-color: white;
}

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
      brand: null,
    }
  },
  mounted() {
    this.getBrandData()
  },
  methods: {
    async getBrandData(){
      this.$store.commit('setIsLoading', true)

      const brand_slug = this.$route.params.brand_slug

      await axios
        .get(`/brand/${brand_slug}/`)
        .then(response => {
          this.brand = response.data
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    }
  },
}
</script>