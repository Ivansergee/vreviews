<template>
      <div class="columns box is-vcentered my-5">
        <div class="column is-2">
          <img class="image" :src="image" />
        </div>
        <div class="column is-3">
          <p class="title is-5 mb-1">
            <router-link :to="{ name: 'product-detail', params: {product_slug: product_slug} }"
            >{{ name }}</router-link>
          </p>
          <p class="mb-1">
            <router-link :to="{ name: 'brand-detail', params: {brand_slug: brand_slug} }"
            >{{ brand }}</router-link>
          </p>
        </div>
        <div class="column is-2">
          <span
            ><i class="bi bi-chat-left-text"></i> {{ reviews_count }}
          </span>
          <span><i class="bi bi-star-fill"></i> {{ score_count }}</span>
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
      </div>
</template>

<style scoped>
.box {
  padding: 0;
}
.image {
  max-height: 200px;
  max-width: 200px;
}
</style>

<script>
export default {
  props: [
    "name",
    "brand",
    "image",
    "product_slug",
    "brand_slug",
    "reviews_count",
    "score_count",
    "flavors",
    "avg_score",
  ],
};
</script>