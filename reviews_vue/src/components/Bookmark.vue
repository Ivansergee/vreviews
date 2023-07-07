<template>
      <div class="columns box is-vcentered my-5">
        <div class="column">
          <figure class="image">
            <img :src="image" />
          </figure>
        </div>

        <div class="column">
          <p class="title is-5 mb-1">
            <router-link :to="{ name: 'product-detail', params: {product_slug: slug} }"
            >{{ name }}</router-link>
          </p>
          <p class="mb-1">
            <router-link :to="{ name: 'brand-detail', params: {brand_slug: brand_slug} }"
            >{{ brand_name }}</router-link>
          </p>
        </div>

        <div class="column">
          <p v-if="description.length < 150">
            {{ description }}
          </p>
          <p v-else>
            {{ description.substring(0,150)+"..." }}
          </p>
        </div>

        <div class="column">
          <p class="tags">
            <span
              class="tag is-info"
              v-for="flavor in flavors"
              :key="flavor.id"
              >{{ flavor.name }}</span
            >
          </p>
        </div>

        <div class="column">
          <p class="tags">
            <span
              class="tag is-warning"
              v-for="item in nic_content"
              :key="item.id"
              >{{ item.amount }}</span>
          </p>
        </div>

        <div class="column mr-2">
          <p class="tag is-primary is-large">
            <i class="bi bi-star-fill"></i> {{ avg_score || '-' }}
          </p>
          <p class="mt-1">
            <span>
              <i class="bi bi-chat-left-text"></i> {{ reviews_count || 0 }}
            </span>
            <span>
              <i class="bi bi-star-fill"></i> {{ score_count || 0 }}
            </span>
          </p>
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
    "brand_slug",
    "brand_name",
    "nic_content",
    "image",
    "slug",
    "description",
    "reviews_count",
    "score_count",
    "flavors",
    "avg_score"
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