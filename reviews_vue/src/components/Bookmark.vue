<template>
      <div class="columns box is-vcentered my-5">
        <div class="column is-2">
          <figure class="image is-1by1">
            <img :src="image" />
          </figure>
        </div>
        <div class="column is-3">
          <p class="title is-5">
            <router-link :to="{ name: 'product-detail', params: {product_slug: slug} }"
            >{{ name }}</router-link>
          </p>
        </div>
        <div class="column is-2">
          <span
            ><i class="bi bi-chat-left-text"></i> {{ reviews_amount }}
          </span>
          <span><i class="bi bi-star-fill"></i> {{ score_amount }}</span>
        </div>
        <div class="column">
          <p class="tags">
            <span
              class="tag is-info"
              v-for="flavor in flavors"
              :key="flavor.id"
              >{{ flavor }}</span
            >
          </p>
        </div>
        <div class="column">
          <span class="tag is-primary is-large"
            ><i class="bi bi-star-fill"></i> {{ avg_score }}</span
          >
        </div>
        <div class="column">
          <a class="button is-danger" @click="removeBookmark()">
            <span>Удалить</span>
          </a>
        </div>
      </div>
</template>

<style scoped>
.box {
  padding: 0;
}
</style>

<script>
import axios from 'axios';


export default {
  props: [
    "id",
    "name",
    "image",
    "slug",
    "reviews_amount",
    "score_amount",
    "flavors",
    "avg_score",
  ],
  emits: ['deleted'],
  methods: {
    async removeBookmark() {
      const data = {product: this.id};
        await axios
        .delete('/bookmarks/', {data: data})
        .then(() => {
            this.$emit("deleted", this.id);
          })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>