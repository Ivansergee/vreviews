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

    <section class="section user-review" v-if="$store.state.isAuthenticated">
        <p class="title is-4">Ваша оценка</p>
        <div class="tags has-addons" @mouseleave="score=user_score" @click="createReview()">
            <a class="tag" v-for="i in 10" :key="i" @mouseover="score=i">
              <i class="bi" :class="[score >= i ? 'bi-star-fill' : 'bi-star']"></i>
            </a>
            <span class="tag is-primary">{{ score }}</span>
        </div>
        <article class="media">
        <div class="media-content">
            <div class="field">
                <p class="control">
                    <textarea class="textarea" placeholder="Ваш отзыв..." v-model="user_review"></textarea>
                </p>
            </div>
            <div class="field">
                <p class="control">
                    <button class="button" @click="createReview()">Отправить</button>
                </p>
            </div>
        </div>
        </article>
    </section>

    <section class="section reviews">
        <p class="title is-3">Отзывы</p>

        <div class="review" v-for="review in reviews" :key="review.id">
          <article class="media">
          <figure class="media-left">
              <p class="image is-64x64">
              <img src="http://localhost:8000/media/placeholder.jpg" />
              </p>
          </figure>
          <div class="media-content">
              <div class="content">
              <p>
                  <strong>{{ review.author }}</strong> <small>{{ review.created_at }}</small>
                  <br />
                  {{ review.text }}
                  <br />
                  <small><a>Like</a> · <a>Dislike</a> · <a>Reply</a> </small>
              </p>
              </div>

              <article class="media">
              <figure class="media-left">
                  <p class="image is-64x64">
                  <img src="http://localhost:8000/media/placeholder.jpg" />
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
        </div>
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
      reviews: null,
      score: 0,
      user_score: 0,
      user_review: '',
      user_review_id: null,
    }
  },
  mounted() {
    this.getProductData()
    this.getReviews()
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
    },
    async getReviews() {
      const product_slug = this.$route.params.product_slug

      await axios
        .get(`/reviews/${product_slug}/`)
        .then(response => {
          this.reviews = response.data
          
          for (var i in response.data){
            if (response.data[i].author == this.$store.state.username) {
              this.user_review_id = response.data[i].id
              this.user_score = response.data[i].score
              this.score = response.data[i].score
              this.user_review = response.data[i].text
            }
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    async createReview() {
      const formData = {
        product: this.product.id,
        score: this.review_id ? this.user_score : this.score,
        text: this.user_review
      }

      if (!this.user_review_id) {
        await axios
        .post('reviews/create/', formData)
        .then(response => {
          this.user_score = response.data.score
          this.user_review = response.data.review
          this.user_review_id = response.data.id
        })
        .catch(error => {
          console.log(error)
        })
      } else {
        await axios
        .patch(`reviews/${this.user_review_id}/edit/`, formData)
        .then(response => {
          this.user_score = response.data.score
          this.user_review = response.data.review
        })
        .catch(error => {
          console.log(error)
        })
      }

      this.getReviews()
    }
  },
}
</script>