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
            :src=product.image_url
          />
        </figure>
      </div>
      <div class="column is-4">
        <div class="content">
          <p><strong>Бренд:</strong> <router-link :to="{name: 'brand-list', params: {brand_slug: product.brand.slug}}">{{ product.brand.name }}</router-link></p>
          <p><strong>Название:</strong> {{ product.name }}</p>
          <p><strong>Страна:</strong> {{ product.brand.producer.country }}</p>
          <p><strong>Производитель:</strong> {{ product.brand.producer.name }}</p>
          <p><strong>Вкусы:</strong></p>
          <p class="tags">
            <a class="tag is-info" v-for="flavor in product.flavors" :key="flavor.id">{{ flavor }}</a>
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
            <span class="tag is-primary">{{ product.get_avg_score }}</span>
          </div>
          <p><strong>Отзывов: </strong>{{ product.get_reviews_amount }}</p>
          <p><strong>Оценок: </strong>{{ product.get_score_amount }}</p>
        </div>
      </div>
    </div>

    <section class="user-review" v-if="$store.state.isAuthenticated">
      <p class="title is-4">Ваша оценка</p>
      <div v-if="!user_review">
        <div class="tags has-addons" @mouseleave="score=user_score" @click="setScore()">
            <a class="tag" v-for="i in 10" :key="i" @mouseover="score=i">
              <i class="bi" :class="[score >= i ? 'bi-star-fill' : 'bi-star']"></i>
            </a>
            <span class="tag is-primary">{{ score }}</span>
        </div>
        <article class="media">
          <div class="media-content">
              <div class="field">
                  <p class="control">
                      <textarea class="textarea" placeholder="Ваш отзыв..." v-model="new_user_review"></textarea>
                  </p>
              </div>
              <div class="field">
                  <p class="control">
                      <button class="button" @click="addReview()">Отправить</button>
                  </p>
              </div>
          </div>
        </article>
      </div>
      <div v-else>
        <p><strong>Оценка: </strong>{{ user_score }}</p>
        <p><strong>Отзыв: </strong><br>{{ user_review }}</p>
        <div class="mt-5">
          <button class="button is-info mr-2" @click="new_user_review=user_review; user_review=''">Редактировать</button>
          <button class="button is-danger ml-2" @click="activeModal=true">Удалить</button>
        </div>
      </div>
    </section>

    <div class="modal is-align-items-center" :class="{'is-active': activeModal}">
        <div class="modal-background"></div>
        <div class="modal-content">
          <div class="box">
            <p class="mb-5">Вы уверены?</p>
            <div class="controls">
              <button class="button is-danger mr-2" @click="deleteReview()">Удалить</button>
              <button class="button is-light ml-2" @click="activeModal=false">Отмена</button>
            </div>
          </div>
        </div>
    </div>

    <section class="reviews">
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
    border-bottom: 2px solid rgb(90, 90, 90);
    padding-top: 1em;
    padding-bottom: 1em;
}
.reviews {
    margin-top: 2em;
}
.columns {
  max-width: 80%;
  margin: auto;
}
.controls {
  display: flex;
  justify-content: center;
}
.box p {
  text-align: center;
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
      new_user_review: null,
      user_review_id: null,
      commentingPostId: 0,
      activeModal: false,
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

          if (this.reviews[i].user_reaction === null){
            this.reviews[i].user_reaction = data.like
            data.like ? this.reviews[i].likes_count += 1 : this.reviews[i].dislikes_count += 1
          } else if (this.reviews[i].user_reaction === true) {
            if (data.like) {
              this.reviews[i].user_reaction = null
              this.reviews[i].likes_count -= 1
            } else {
              this.reviews[i].user_reaction = data.like
              this.reviews[i].likes_count -= 1
              this.reviews[i].dislikes_count += 1
            }
          } else {
            if (!data.like) {
              this.reviews[i].user_reaction = null
              this.reviews[i].dislikes_count -= 1
            } else {
              this.reviews[i].user_reaction = data.like
              this.reviews[i].likes_count += 1
              this.reviews[i].dislikes_count -= 1
            }
          }

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
        .get(`/reviews/?product__slug=${product_slug}`)
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

    async addReview() {
      const formData = {
        product: this.product.id,
        score: this.review_id ? this.user_score : this.score,
        text: this.new_user_review
      }

      if (!this.user_review_id) {
        await axios
        .post('reviews/', formData)
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
    },

    async deleteReview() {
      await axios
        .delete(`reviews/${this.user_review_id}/delete/`)
        .then(response => {
          this.user_score = 0
          this.score = 0
          this.user_review = ''
          this.new_user_review = ''
          this.user_review_id = null
          this.activeModal = false
        })
        .catch(error => {
          console.log(error)
        })
      this.getReviews()
    },

    async setScore() {
      const formData = {
        product: this.product.id,
        score: this.review_id ? this.user_score : this.score,
      }

      if (!this.user_review_id) {
        await axios
        .post('reviews/', formData)
        .then(response => {
          this.user_score = response.data.score
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
        })
        .catch(error => {
          console.log(error)
        })
      }

    },

  },
}
</script>