<template>
  <div class="columns box is-vcentered my-5">
    
    <div class="column ml-2">
      <p class="title is-5">
        <router-link :to=" {name: 'profile', params: { username: author } }">
          {{ author }}
        </router-link>
      </p>
    </div>

    <div class="column">
      <p class="title is-5">
        {{ name }}
      </p>
    </div>

    <div class="column">
      <p>
        {{ text }}
      </p>
    </div>

    <div class="column">
      <p>
        {{ comment }}
      </p>
    </div>

    <div class="column mr-2">
      <p class="tag is-primary is-large">
        <i class="bi bi-star-fill"></i> {{ score }}
      </p>
    </div>

    <div class="column mr-2">
      <button class="button is-info" @click="process(id)" v-if="!processed">Обработать</button>
      <router-link :to="{ name: 'product-detail', params: {product_slug: product_slug} }" class="button is-success" v-if="processed && product_slug">Обработано </router-link>
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
    "id",
    "name",
    "text",
    "comment",
    "author",
    "score",
    "product_slug",
    "processed"
  ],
  emits: ['process'],
  methods: {
    process() {
      this.$emit("process", this.id);
    }
  },
};
</script>