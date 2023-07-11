<template>
      <div class="columns box is-vcentered my-5">

        <div class="column">
          <figure class="image">
            <img :src="image" />
          </figure>
        </div>

        <div class="column">
          <p class="title is-5">
            <router-link :to="{ name: 'brand-detail', params: {brand_slug: slug} }"
            >{{ name }}</router-link>
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
              class="tag is-warning"
              v-for="nic in nic_content"
              :key="nic.id"
              >{{ nic.amount }}</span>
          </p>
        </div>

        <div class="column">
          <p class="tag is-primary is-large">
            <i class="bi bi-star-fill"></i> {{ avg_score  < 0 ? '-' : avg_score }}
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
    "image",
    "slug",
    "description",
    "nic_content",
    "reviews_count",
    "score_count",
    "avg_score",
  ],
};
</script>