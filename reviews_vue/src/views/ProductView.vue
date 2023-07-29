<template>
  <div class="container" v-if="product">
    <div class="level">
      <div class="level-left">
        <h1 class="title level-item">
          {{ product.brand.name }} {{ product.name }}
        </h1>
      </div>
      <div class="level-right" v-if="$store.state.isAdmin">
        <button class="button is-success level-item" @click="showEdit = true">Редактировать</button>
      </div>
    </div>
    <div class="columns">
      <div class="column is-4">
        <figure class="image is-1by1">
          <img id="product-image" :src="product.thumbnail_url" @click="showImage=true"/>
        </figure>
        <a
          class="button mt-3"
          @click="toggleBookmark()"
          v-if="!product.user_bookmark"
        >
          <span class="icon">
            <i class="fa-regular fa-bookmark"></i>
          </span>
          <span>В закладки</span>
        </a>
        <a class="button mt-3" @click="toggleBookmark()" v-else>
          <span class="icon">
            <i class="fa-solid fa-bookmark"></i>
          </span>
          <span>Добавлено</span>
        </a>
      </div>
      <div class="column is-4">
        <div class="content">
          <p>
            <strong>Бренд: </strong>
            <router-link
              :to="{
                name: 'brand-detail',
                params: { brand_slug: product.brand.slug },
              }"
              >{{ product.brand.name }}</router-link>
          </p>
          <p><strong>Название: </strong> {{ product.name }}</p>
          <p><strong>Страна: </strong> {{ product.brand.producer.country }}</p>
          <p>
            <strong>Производитель: </strong> 
            <router-link
              :to="{
                name: 'producer-detail',
                params: { producer_slug: product.brand.producer.slug },
              }"
              >{{ product.brand.producer.name }}</router-link>
          </p>
          <p><strong>Вкусы:</strong></p>
          <p class="tags">
            <a
              class="tag is-info"
              v-for="flavor in product.flavors"
              :key="flavor.id"
              >{{ flavor.name }}</a
            >
          </p>
          <p><strong>Содержание никотина:</strong></p>
          <p class="tags">
            <span
              class="tag is-warning"
              v-for="amount in product.nic_content"
              :key="amount.id"
              >{{ amount.amount }}</span
            >
          </p>
          <p><strong>VG/PG: </strong>{{ product.vg }}/{{ 100 - product.vg }}</p>
          <p><strong>Объем: </strong></p>
          <p class="tags">
            <span
              class="tag is-warning"
              v-for="volume in product.volume"
              :key="volume.id"
              >{{ volume.volume }} мл</span
            >
          </p>
          <p><strong>Описание:</strong></p>
          <p>{{ product.description }}</p>
        </div>
      </div>
      <div class="column is-4">
        <div class="content">
          <p class="title is-4">Оценка:</p>
          <div class="tags are-large has-addons">
            <span class="tag"><i class="bi bi-star-fill"></i></span>
            <span class="tag is-primary">{{
              product.avg_score > 0 ? product.avg_score : '-'
            }}</span>
          </div>
          <p>
            <strong>Отзывов: </strong
            >{{ product.reviews_count ? product.reviews_count : 0 }}
          </p>
          <p>
            <strong>Оценок: </strong
            >{{ product.score_count ? product.score_count : 0 }}
          </p>
        </div>
      </div>
    </div>

    <section class="user-review">
      <div v-if="$store.state.isAuthenticated">
        <p class="title is-4">Ваш отзыв</p>
        <div v-if="!user_review">
          <p class="subtitle">Оценка</p>
          <div class="tags has-addons"
            @mouseleave="score = user_score"
            @click="setScore()"
          >
            <a class="tag" v-for="i in 10" :key="i" @mouseover="score = i">
              <i
                class="bi"
                :class="[score >= i ? 'bi-star-fill' : 'bi-star']"
              ></i>
            </a>
            <span class="tag is-primary">{{ score }}</span>
          </div>
          <div class="field" v-if="user_score">
            <p class="subtitle">Отзыв</p>
            <div class="control">
                <textarea
                  class="textarea"
                  v-model="new_user_review"
                ></textarea>
            </div>
            <p class="help">Опишите свои впечатления от вкуса (не обязательно).</p>
          </div>
          <div class="field" v-if="user_score">
            <p class="subtitle mb-2">Устройства</p>
            <p class="mb-2" v-if="!devices">Вы ещё не добавили ни одного устройства</p>
            <p class="subtitle">
              <button class="button is-success is-small">
                <span>Добавить уcтройство</span>
              </button>
            </p>
            <div class="control select is-multiple" v-if="devices">
              <select multiple size="3" v-model="selectedDevices">
                <option v-for="device in devices" :key="device.id" :value="device.id">{{ device.name }}</option>
              </select>
            </div>
            <p class="help" v-if="devices">Выберите устройства, на которых вы использовали жидкость. Удерживайте Ctrl для выбора нескольких.</p>
          </div>
          <div class="control mt-2">
              <button
                class="button"
                :class="{ 'is-loading': isLoading }"
                :disabled="!new_user_review"
                @click="addReview()"
              >
                Отправить
              </button>
          </div>
        </div>
        <div v-else>
          <p><strong>Оценка: </strong>{{ user_score }}</p>
          <p><strong>Отзыв: </strong><br />{{ user_review }}</p>
          <div class="mt-5">
            <button
              class="button is-info mr-2"
              @click="
                new_user_review = user_review;
                user_review = '';
              "
            >
              Редактировать
            </button>
            <button class="button is-danger" @click="showDeleteConfirm = true">
              Удалить
            </button>
          </div>
        </div>
      </div>
      <div v-else>
        <p class="title is-5"><a @click="$root.showLogIn=true">Войдите</a> чтобы оставить отзыв.</p>
      </div>
    </section>

    <section class="reviews">
      <p class="title is-3">Отзывы</p>
      <p v-if="!reviews">Отзывов пока нет</p>
      <Review
        v-for="review in reviews"
        :key="review.id"
        :id="review.id"
        :author="review.author"
        :authorAvatar="review.author_avatar"
        :score="review.score"
        :text="review.text"
        :created_at="review.created_at"
        :likesCount="review.likes_count"
        :dislikesCount="review.dislikes_count"
        :userReaction="review.user_reaction"
        :comments="review.comments"
        :devices="review.devices"
        :commentingPostId="commentingPostId"
        @commenting="setCommentingPostId"
        @commented="getReviews"
        @rated="setRated"
        @deleted="removeReview"
      />
    </section>

    <div class="modal" :class="{ 'is-active': showImage }">
      <div class="modal-background" @click="showImage = false"></div>
      <div class="modal-content">
        <p class="image">
          <img :src="product.image_url">
        </p>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="showImage = false"></button>
    </div>

    <div class="modal" :class="{ 'is-active': showEdit }" v-if="showEdit">
      <div class="modal-background" @click="showEdit = false"></div>
      <div class="modal-content">
        <div class="box">
        <EditLiquid
          :name="product.name"
          :description="product.description"
          :brand="{name: product.brand.name, id: product.brand.id}"
          :image="product.image_url"
          :flavors="product.flavors"
          :vg="product.vg"
          @added="updateInfo"
        />
        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="showEdit = false"></button>
    </div>

    <div class="modal" :class="{ 'is-active': showDeleteConfirm }">
      <div class="modal-background" @click="showDeleteConfirm = false"></div>
      <div class="modal-content">
        <div class="box">
          <div class="level">
            <div class="level-left">
              <h1 class="title">Вы уверены?</h1>
            </div>
            <div class="level-right">
              <button
                class="delete is-medium"
                aria-label="close"
                @click="showDeleteConfirm = false"
              ></button>
            </div>
          </div>

          <div class="controls">
            <button
              class="button is-danger mr-3"
              @click="deleteReview()"
              :class="{ 'is-loading': isLoadingDelete }"
            >
              Удалить
            </button>
            <button class="button is-info" @click="showDeleteConfirm = false">
              Отмена
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#product-image {
  max-width: 300px;
  max-height: 300px;
}
#product-image:hover {
  cursor: pointer;
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
  max-width: 100%;
  margin: auto;
}
.fa-bookmark {
  color: red;
}
</style>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

import Review from "../components/Review.vue";
import EditLiquid from "../components/EditLiquid.vue";

export default {
  components: {
    Review,
    EditLiquid
  },
  data() {
    return {
      product: null,
      reviews: null,
      score: 0,
      user_score: 0,
      user_review: "",
      selectedDevices: [],
      new_user_review: null,
      user_review_id: null,
      commentingPostId: 0,
      activeModal: false,
      isLoading: false,
      showDeleteConfirm: false,
      isLoadingDelete: false,
      showImage: false,
      showEdit: false
    };
  },
  mounted() {
    this.getProductData();
    this.getReviews();
  },
  computed: {
    listVolumes() {
      return this.product.volume.join(", ");
    },
    devices() {
      return this.$store.state.devices;
    },
  },
  methods: {
    updateInfo(slug) {
      if (slug != this.$route.params.product_slug) {
        this.$router.replace({ name: 'product-detail', params: { product_slug: slug } });
        this.getProductData(slug);
      } else {
        this.getProductData();
      }
      this.showEdit = false;
    },

    setCommentingPostId(id) {
      this.commentingPostId = id;
    },

    async toggleBookmark() {
      if (this.$store.state.isAuthenticated) {
        const data = { product: this.product.id };
        if (!this.product.user_bookmark) {
          await axios
            .post("/bookmarks/", data)
            .then((this.product.user_bookmark = true))
            .catch((error) => {
              console.log(error);
            });
        } else {
          await axios
            .delete("/bookmarks/", { data: data })
            .then(() => {
              this.product.user_bookmark = null;
            })
            .catch((error) => {
              console.log(error);
            });
        }
      } else {
        this.$root.showLogIn = true;
      }
    },

    setRated(data) {
      for (var i in this.reviews) {
        if (this.reviews[i].id == data.id) {
          if (this.reviews[i].user_reaction === null) {
            this.reviews[i].user_reaction = data.like;
            data.like
              ? (this.reviews[i].likes_count += 1)
              : (this.reviews[i].dislikes_count += 1);
          } else if (this.reviews[i].user_reaction === true) {
            if (data.like) {
              this.reviews[i].user_reaction = null;
              this.reviews[i].likes_count -= 1;
            } else {
              this.reviews[i].user_reaction = data.like;
              this.reviews[i].likes_count -= 1;
              this.reviews[i].dislikes_count += 1;
            }
          } else {
            if (!data.like) {
              this.reviews[i].user_reaction = null;
              this.reviews[i].dislikes_count -= 1;
            } else {
              this.reviews[i].user_reaction = data.like;
              this.reviews[i].likes_count += 1;
              this.reviews[i].dislikes_count -= 1;
            }
          }
        }
      }
    },

    async getProductData(slug=this.$route.params.product_slug) {
      this.$store.commit("setIsLoading", true);

      await axios
        .get(`/products/${slug}/`)
        .then((response) => {
          this.product = response.data;
          this.setTitle(this.product.name);
        })
        .catch((error) => {
          if (error.response.status == 404) {
            this.$router.push({name: "not-found"});
          }
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    async getReviews() {
      this.$store.commit("setIsLoading", true);

      const product_slug = this.$route.params.product_slug;

      await axios
        .get(`/reviews/?product=${product_slug}`)
        .then((response) => {
          this.reviews = [];
          let results = response.data.results;
          for (var i in results) {
            if (results[i].author == this.$store.state.username) {
              this.user_review_id = results[i].id;
              this.user_score = results[i].score;
              this.score = results[i].score;
              this.user_review = results[i].text;
            }
            if (results[i].text) {
              this.reviews.push(results[i]);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    async addReview() {
      if (!this.$store.state.isAuthenticated) {
        this.$root.showLogIn = true;
        return;
      }

      const formData = new FormData();

      formData.append('product_id', this.product.id);
      if (this.review_id) {
        formData.append('score', this.user_score);
      } else {
        formData.append('score', this.score);
      }
      formData.append('text', this.new_user_review);
      for (var i of this.selectedDevices) {
        formData.append("device_id", i );
      }

      if (formData.get('score') < 1) {
        toast({
              message: 'Вы не поставили оценку!',
              type: "is-danger",
              dismissible: true,
              duration: 5000,
              pauseOnHover: true,
              position: "top-center",
            });
        return;
      }

      this.isLoading = true;
      if (!this.user_review_id) {
        await axios
          .post("reviews/", formData)
          .then((response) => {
            this.user_score = response.data.score;
            this.user_review = response.data.review;
            this.user_review_id = response.data.id;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        await axios
          .patch(`reviews/${this.user_review_id}/edit/`, formData)
          .then((response) => {
            this.user_score = response.data.score;
            this.user_review = response.data.review;
          })
          .catch((error) => {
            toast({
              message: error.response.data.detail,
              type: "is-danger",
              dismissible: true,
              duration: 5000,
              pauseOnHover: true,
              position: "top-center",
            });
          });
      }
      this.isLoading = false;

      this.getReviews();
    },

    removeReview(id) {
      for (var i in this.reviews) {
        if (this.reviews[i].id == id) {
          this.reviews.splice(i, 1);
        }
      }
    },

    async deleteReview() {
      if (this.user_review_id) {
        this.isLoadingDelete = true;
        await axios
          .delete(`reviews/${this.user_review_id}/delete/`)
          .then(() => {
            this.user_score = null;
            this.score = 0;
            this.user_review = "";
            this.new_user_review = "";
            this.showDeleteConfirm = false;
            this.removeReview(this.user_review_id);
          })
          .catch((error) => {
            console.log(error.response.message);
          });
        this.isLoadingDelete = false;
      }
    },

    async setScore() {
      if (!this.$store.state.isAuthenticated) {
        this.$root.showLogIn = true;
        return null;
      }

      this.user_score = this.score;

      const formData = {
        product_id: this.product.id,
        score: this.review_id ? this.user_score : this.score,
      };

      if (!this.user_review_id) {
        await axios
          .post("reviews/", formData)
          .then((response) => {
            this.user_score = response.data.score;
            this.user_review_id = response.data.id;
          })
          .catch((error) => {
            console.log(error.response.message);
          });
      } else {
        await axios
          .patch(`reviews/${this.user_review_id}/edit/`, formData)
          .then((response) => {
            this.user_score = response.data.score;
          })
          .catch((error) => {
            console.log(error.response.message);
          });
      }
    },

    setTitle(title) {
      document.title = `${title} | VapeRate`;
    }
  },
};
</script>