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
        <Review
          v-for="review in reviews"
          :key="review.id"
          :id="review.id"
          :author="review.author"
          :score="review.score"
          :text="review.text"
          :created_at="review.created_at"
          :likesCount="review.likes_count"
          :dislikesCount="review.dislikes_count"
          :userReaction="review.user_reaction"
          :comments="review.comments"
          :commentingPostId="commentingPostId"
          @commenting="setCommentingPostId"
          @commented="getReviews"
          @rated="setRated"
        />
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
import Review from '../components/Review.vue'

export default {
  components: {
    Review
  },
  data() {
    return {
      product: null,
      reviews: null,
      score: 0,
      user_score: 0,
      user_review: '',
      user_review_id: null,
      commentingPostId: 0,
    }
  },
  mounted() {
    this.getProductData()
    this.getReviews()
  },
  methods: {
    setCommentingPostId(id) {
      this.commentingPostId = id
    },

    setRated(data) {
      for (var i in this.reviews) {
        if (this.reviews[i].id == data.id) {
          this.reviews[i].user_reaction = data.like
          if (data.like) {
            this.reviews[i].likes_count += 1
          } else {
            this.reviews[i].dislikes_count += 1
          }
        }
      }
    },

    unsetRated(id) {
      for (var i in this.reviews) {
        if (this.reviews[i].id == id) {
          this.reviews[i].user_reaction = null
        }
      }
    },

    async getProductData(){
      this.$store.commit('setIsLoading', true)

      const product_slug = this.$route.params.product_slug

      await axios
        .get(`/products/${product_slug}`)
        .then(response => {
          this.product = response.data
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    },

    async getReviews() {
      this.$store.commit('setIsLoading', true)

      const product_slug = this.$route.params.product_slug

      await axios
        .get(`/products/${product_slug}/reviews/`)
        .then(response => {
          this.reviews = []

          for (var i in response.data) {
            if (response.data[i].author == this.$store.state.username) {
              this.user_review_id = response.data[i].id
              this.user_score = response.data[i].score
              this.score = response.data[i].score
              this.user_review = response.data[i].text
            }
            if (response.data[i].text){
              this.reviews.push(response.data[i])
            }
          }
        })
        .catch(error => {
          console.log(error)
        })
      
      this.$store.commit('setIsLoading', false)
    },

    async createReview() {
      const formData = {
        product: this.product.id,
        score: this.review_id ? this.user_score : this.score,
        text: this.user_review
      }

      if (!this.user_review_id) {
        await axios
        .post('review/create/', formData)
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
        .patch(`review/${this.user_review_id}/edit/`, formData)
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