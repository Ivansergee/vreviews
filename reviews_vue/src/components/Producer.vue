<template>
      <div class="columns box is-vcentered my-5">
        <div class="column is-2">
          <figure class="image is-1by1">
            <img :src="image" />
          </figure>
        </div>
        <div class="column is-3">
          <p class="title is-5">
            <router-link :to="{ name: 'producer-detail', params: {producer_slug: slug} }"
            >{{ name }}</router-link>
          </p>
        </div>
        <div class="column is-2">
          <span
            ><i class="bi bi-chat-left-text"></i> {{ reviews_count || 0 }}
          </span>
          <span><i class="bi bi-star-fill"></i> {{ score_count || 0 }}</span>
        </div>
        <div class="column">
          <span class="tag is-primary is-large"
            ><i class="bi bi-star-fill"></i> {{ avg_score  > 0 ? avg_score : '-' }}</span
          >
        </div>
      </div>
</template>

<style scoped>
.box {
  padding: 0;
}
</style>

<script>
export default {
  props: [
    "name",
    "image",
    "slug",
    "reviews_count",
    "score_count",
    "avg_score",
  ],
};
</script>