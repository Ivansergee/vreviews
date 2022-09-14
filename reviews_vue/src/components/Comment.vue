<template>
  <article class="media">
    <figure class="media-left">
      <p class="image">
        <img :src="authorAvatar" />
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <p>
          <strong><router-link :to="{ name: 'profile', params: {username: author} }">{{ author }}</router-link></strong> <small>{{ formatTime(created_at) }}</small>
          <br />
          {{ text }}
          <br />
        </p>
      </div>
    </div>
  </article>
</template>

<style scoped>
.image>img {
  max-width: 64px;
  max-height: 64px;
}
</style>

<script>
import moment from 'moment';


export default {
  props: ["author", "authorAvatar", "text", "created_at"],
  methods: {
    formatTime(time) {
      return moment(time).format('DD.MM.YYYY HH:mm')
    }
  }
};
</script>