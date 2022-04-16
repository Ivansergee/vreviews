<template>
  <div class="container" v-if="product">
    <div class="level">
      <div class="level-left">
        <h1 class="title level-item">{{ product.brand.name}} {{ product.name }}</h1>
      </div>
    </div>
    <div class="columns">
      <div class="column is-4">
        <figure class="image is-1by1">
          <img
            :src=product.get_image
          />
        </figure>
      </div>
      <div class="column is-4">
        <div class="content">
          <p><strong>Бренд:</strong> <router-link :to="{name: 'brand-list'}">{{ product.brand.name }}</router-link></p>
          <p><strong>Название:</strong> {{ product.name }}</p>
          <p><strong>Страна:</strong> {{ product.brand.producer.country }}</p>
          <p><strong>Производитель:</strong> {{ product.brand.producer.name }}</p>
          <p><strong>Вкусы:</strong></p>
          <p class="tags">
            <a class="tag is-info" v-for="flavor in product.flavors" :key="flavor.id">{{ flavor.name }}</a>
          </p>
          <p><strong>Содержание никотина:</strong></p>
          <p class="tags">
            <span class="tag is-warning">12</span>
            <span class="tag is-warning">20</span>
            <span class="tag is-warning">20 HYBRID</span>
          </p>
          <p>{{ product.description }}</p>
        </div>
      </div>
      <div class="column is-4">
        <div class="content">
          <p class="title is-4">Оценка:</p>
          <div class="tags are-large has-addons">
            <span class="tag"><i class="bi bi-star-fill"></i></span>
            <span class="tag is-primary">7.4</span>
          </div>
          <p><strong>Отзывов:</strong> 15</p>
          <p><strong>Оценок:</strong> 25</p>
          <p><strong>Место в рейтинге:</strong> 10</p>
        </div>
      </div>
    </div>

    <section class="section user-review">
        <p class="title is-4">Ваша оценка</p>
        <div class="tags has-addons">
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star-fill"></i></a>
            <a class="tag"><i class="bi bi-star"></i></a>
            <a class="tag"><i class="bi bi-star"></i></a>
            <span class="tag is-primary">8</span>
        </div>
        <article class="media">
        <div class="media-content">
            <div class="field">
                <p class="control">
                    <textarea class="textarea" placeholder="Ваш отзыв..."></textarea>
                </p>
            </div>
            <div class="field">
                <p class="control">
                    <button class="button">Отправить</button>
                </p>
            </div>
        </div>
        </article>
    </section>
    <section class="section reviews">
        <p class="title is-3">Все отзывы</p>
        <article class="media">
        <figure class="media-left">
            <p class="image is-64x64">
            <img src="https://bulma.io/images/placeholders/128x128.png" />
            </p>
        </figure>
        <div class="media-content">
            <div class="content">
            <p>
                <strong>Barbara Middleton</strong>
                <br />
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis porta
                eros lacus, nec ultricies elit blandit non. Suspendisse pellentesque
                mauris sit amet dolor blandit rutrum. Nunc in tempus turpis.
                <br />
                <small><a>Like</a> · <a>Dislike</a> · <a>Reply</a> · 04.04.22 11:45</small>
            </p>
            </div>

            <article class="media">
            <figure class="media-left">
                <p class="image is-64x64">
                <img src="https://bulma.io/images/placeholders/96x96.png" />
                </p>
            </figure>
            <div class="media-content">
                <div class="content">
                <p>
                    <strong>Kayli Eunice </strong> <small>05.04.22 15:32</small>
                    <br />
                    Sed convallis scelerisque mauris, non pulvinar nunc mattis vel.
                    Maecenas varius felis sit amet magna vestibulum euismod
                    malesuada cursus libero. Vestibulum ante ipsum primis in
                    faucibus orci luctus et ultrices posuere cubilia Curae;
                    Phasellus lacinia non nisl id feugiat.
                    <br />
                    
                </p>
                </div>
            </div>
            </article>
        </div>
        </article>

        <article class="media">
        <div class="media-content">
            <div class="field">
            <p class="control">
                <textarea
                class="textarea"
                placeholder="Add a comment..."
                ></textarea>
            </p>
            </div>
            <div class="field">
            <p class="control">
                <button class="button">Post comment</button>
            </p>
            </div>
        </div>
        </article>
    </section>
  </div>
</template>

<style scoped>
img {
  max-width: 300px;
  max-height: 300px;
}
.user-review {
    border-top: 2px solid rgb(90, 90, 90);
    padding-top: 1em;
}
.reviews {
    margin-top: 2em;
}
.columns {
  max-width: 80%;
  margin: auto;
}
</style>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      product: null,
    }
  },
  mounted() {
    this.getProductData()
  },
  methods: {
    async getProductData(){
      this.$store.commit('setIsLoading', true)

      const brand_slug = this.$route.params.brand_slug
      const product_slug = this.$route.params.product_slug

      await axios
        .get(`/products/${brand_slug}/${product_slug}`)
        .then(response => {
          this.product = response.data
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    }
  },
}
</script>