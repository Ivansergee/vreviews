<template>
      <div class="columns box is-vcentered mt-2 mb-5">
        
        <div class="column">
          <figure class="image">
            <img :src="image" />
          </figure>
        </div>

        <div class="column">
          <p class="title is-5 mb-1">
            <router-link :to="{ name: 'product-detail', params: {product_slug: product_slug} }"
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
            <i class="bi bi-star-fill"></i> {{ avg_score  > 0 ? avg_score : '-' }}
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
    "brand_slug",
    "brand_name",
    "nic_content",
    "image",
    "product_slug",
    "description",
    "reviews_count",
    "score_count",
    "flavors",
    "avg_score"
  ],
};
</script>