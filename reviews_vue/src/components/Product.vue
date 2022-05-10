<template>
    <div class="columns is-vcentered">
            <div class="column is-2">
              <figure class="image is-1by1">
                <img
                  :src=image
                />
              </figure>
            </div>
            <div class="column is-3">
                <p class="title is-5"><a :href="absolute_url">{{ name }}</a></p>
                <p class="is-italic is-size-6">Клубничный лимонад</p>
            </div>
            <div class="column is-2">
                <span><i class="bi bi-chat-left-text"></i> {{ reviews_amount }} </span>
                <span><i class="bi bi-star-fill"></i> {{ score_amount }}</span>
            </div>
            <div class="column">
                <p class="tags">
                    <span class="tag is-info" v-for="flavor in flavors" :key="flavor.id">{{ flavor }}</span>
                </p>
            </div>
            <div class="column">
                <span class="tag is-primary is-large"><i class="bi bi-star-fill"></i> {{ avg_score }}</span>
            </div>
          </div>

</template>

<script>
export default {
  props: [
      'name',
      'image',
      'absolute_url',
      'reviews_amount',
      'score_amount',
      'flavors',
      'avg_score'],
}
</script>