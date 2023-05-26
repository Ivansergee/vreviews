<template>
      <div class="columns box is-vcentered my-5">

        <div class="column">
          <p class="title is-5 mb-1">
            {{ name }}
          </p>
        </div>

        <div class="column">
          <p>
            {{ description }}
          </p>
        </div>

        <div class="column mr-2">
          <button class="button is-info" @click="process()">Обработать</button>
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
    "id",
    "name",
    "description",
  ],
  emits: ['processed'],
  methods: {
    async process() {
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