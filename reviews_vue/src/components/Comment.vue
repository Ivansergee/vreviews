<template>
  <article class="media">
    <figure class="media-left">
      <p class="image is-64x64">
        <img src="http://localhost:8000/media/placeholder.jpg" />
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <p>
          <strong>{{ author }}</strong> <small>{{ formatTime(created_at) }}</small>
          <br />
          {{ text }}
          <br />
        </p>
      </div>
    </div>
  </article>
</template>

<script>
import moment from 'moment';


export default {
  props: ["author", "text", "created_at"],
  methods: {
    formatTime(time) {
      return moment(time).format('DD.MM.YYYY HH:mm')
    }
  }
};
</script>