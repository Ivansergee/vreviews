<template>
    <div class="reviews">
      <p v-if="!reviews.length">Нет ни одного отзыва</p>
      <p class="title is-5" v-else>Отзывы {{ $route.params.username }}</p>
      <ProfileReview
        v-for="review in reviews"
        :key="review.id"
        :id="review.id"
        :product="review.product.name"
        :productSlug="review.product.slug"
        :productImage="review.product.thumbnail_url"
        :score="review.score"
        :text="review.text"
        :created_at="review.created_at"
        :likesCount="review.likes_count"
        :dislikesCount="review.dislikes_count"
        :comments="review.comments"
      />
      <a
        class="button is-success"
        @click="getNextReviews"
        v-if="nextReviews && reviewsCount > 10"
        >Показать ещё</a>
    </div>
</template>
<script>
import axios from "axios";
import ProfileReview from "../components/ProfileReview.vue";


export default {
  components: {
    ProfileReview,
  },
  data() {
    return {
      reviews: [],
      reviewsCount: null,
      nextReviews: null,
    };
  },
  mounted() {
    this.getReviews();
  },
  methods: {
    async getReviews() {
      this.$store.commit("setIsLoading", true);

      const username = this.$route.params.username;

      await axios
        .get(`/reviews/?author=${username}`)
        .then((response) => {
          this.reviews = response.data.results;
          this.nextReviews = response.data.next;
          this.reviewsCount = response.data.count;
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    async getNextReviews() {
      await axios
        .get(this.nextReviews)
        .then((response) => {
          this.reviews.push(...response.data.results);
          this.nextReviews = response.data.next;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>