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
            <span class="tag is-primary">8.2</span>
          </div>
          <p><strong>Отзывов:</strong> 15</p>
          <p><strong>Оценок:</strong> 25</p>
        </div>
      </div>
    </div>

    <div class="products">
      <p class="title">Все вкусы {{ brand.name }}</p>
          
          <div class="columns is-vcentered" v-for="product in brand.products" :key="product.id">
            <div class="column is-2">
              <figure class="image is-1by1">
                <img
                  :src=product.get_image
                />
              </figure>
            </div>
            <div class="column is-3">
                <p class="title is-5"><a :href="product.get_absolute_url">{{ product.name }}</a></p>
                <p class="is-italic is-size-6">Клубничный лимонад</p>
            </div>
            <div class="column is-2">
                <span><i class="bi bi-chat-left-text"></i> 10   </span>
                <span><i class="bi bi-star-fill"></i> 15</span>
            </div>
            <div class="column">
                <p class="tags">
                    <span class="tag is-info" v-for="flavor in product.flavors" :key="flavor.id">{{ flavor.name }}</span>
                </p>
            </div>
            <div class="column">
                <span class="tag is-primary is-large"><i class="bi bi-star-fill"></i> 7.4</span>
            </div>
          </div>

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

export default {
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
        .get(`/products/brand/${brand_slug}/`)
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