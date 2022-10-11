<template>
      <div class="columns box is-vcentered my-5">
        
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
            <router-link :to="{ name: 'brand-detail', params: {brand_slug: brand.slug} }"
            >{{ brand.name }}</router-link>
          </p>
        </div>

        <div class="column">
          <p>
            {{ description }}
          </p>
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
          <p class="tags is-warning">
            <span
              class="tag is-warning"
              v-for="nic in brand.nic_content"
              :key="nic.id"
              >{{ nic }}</span
            >
          </p>
        </div>

        <div class="column mr-2">
          <button class="button is-info" @click="publish()">Опубликовать</button>
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
import axios from 'axios';

export default {
  props: [
    "name",
    "brand",
    "image",
    "product_slug",
    "description",
    "flavors",
    "nic_content"
  ],
  emits: ['approved'],
  methods: {
    async publish() {
      const data = {
        is_published: true
      }

      await axios
      .patch(`admin/${this.product_slug}/`, data)
      .then(() => {
        this.$emit('approved', this.product_slug);
      })
      .catch((error) => {
          console.log(error);
      });
    }
  },
};
</script>