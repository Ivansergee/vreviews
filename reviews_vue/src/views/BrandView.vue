<template>
  <div class="container">
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
          <p><strong>Страна:</strong> {{brand?.producer?.country}} </p>
          <p><strong>Производитель:</strong> {{brand?.producer?.name}}  </p>

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

    <section class="section products">
      <p class="title">Все вкусы {{ brand.name }}</p>
          <div class="columns is-vcentered">
            <div class="column is-1">
              <p class="title is-5">1</p>
            </div>
            <div class="column is-2">
              <figure class="image is-1by1">
                <img
                  src="https://www.parzo.ru/media/catalog/product/cache/1/image/363x/040ec09b1e35df139433887a97daa66f/m/a/maxwells_salt_red.jpg"
                />
              </figure>
            </div>
            <div class="column is-3">
                <p class="title is-5">Red</p>
                <p class="is-italic is-size-6">Клубничный лимонад</p>
            </div>
            <div class="column is-2">
                <span><i class="bi bi-chat-left-text"></i> 10   </span>
                <span><i class="bi bi-star-fill"></i> 15</span>
            </div>
            <div class="column">
                <p class="tags">
                    <a class="tag is-info">Клубника</a>
                    <a class="tag is-info">Лимонад</a>
                </p>
            </div>
            <div class="column">
                    <span class="tag is-primary is-large"><i class="bi bi-star-fill"></i> 7.4</span>

            </div>
          </div>
    </section>
  </div>
</template>

<style scoped>
img {
  max-width: 300px;
  max-height: 300px;
}

.head {
  max-width: 80%;
  margin: auto;
}
.is-vcentered {
  max-width: 100% !important;
  margin: auto !important;
  height: 100%;
}
</style>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      brand: {},
      products: {}
    }
  },
  mounted() {
    this.getBrandData()
  },
  methods: {
    getBrandData(){
      const brand_slug = this.$route.params.brand_slug

      axios
        .get(`/brand/${brand_slug}`)
        .then(response => {
          this.brand = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
}
</script>