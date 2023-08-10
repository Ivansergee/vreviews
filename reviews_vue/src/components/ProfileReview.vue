<template>
  <div class="review mb-5">
    <article class="media">
      <figure class="media-left">
        <p class="image is-64x64">
          <img :src="productImage" />
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <p>
            <strong class="mr-2"><router-link :to="{ name: 'product-detail', params: {product_slug: productSlug} }"
            >{{ product }}</router-link></strong>
            <small>{{ formatTime(created_at) }}</small>
            <br />
            <span class="review-score my-2" :class="getScoreColor()">
              <b>{{ score }}</b><i class="fa-solid fa-star ml-2"></i>
            </span>
            <br />
            {{ text }}
            <br />
            <small>
              <span>
                <i class="fa-thumbs-up fa-regular"></i>
              </span>
              <small>{{ likesCount }}</small> ·
              <span>
                <i class="fa-thumbs-down fa-regular"></i>
              </span>
              <small>{{ dislikesCount }}</small> ·
              <span><a @click="showComments=!showComments">Комментарии ({{ comments.length }})</a></span>
            </small>
          </p>
        </div>
        <div class="comments" v-if="showComments">
          <Comment
            v-for="comment in comments"
            :key="comment.id"
            :author="comment.author"
            :text="comment.text"
            :created_at="comment.created_at"
          />
        </div>
      </div>
    </article>

  </div>
</template>

<style scoped>
.reply-form {
  margin-bottom: 2em;
}

.fa-thumbs-up {
  color: green;
}

.fa-thumbs-down {
  color: red;
}

.tag {
  box-shadow: 1px 1px 2px #aaa;
}
</style>

<script>
import moment from 'moment'

import Comment from "./Comment.vue";

export default {
  components: {
    Comment,
  },
  props: [
    "id",
    "product",
    "productSlug",
    "productImage",
    "score",
    "text",
    "created_at",
    "comments",
    "likesCount",
    "dislikesCount",
  ],
  data() {
    return {
      showComments: false,
    }
  },
  methods: {
    formatTime(time) {
      return moment(time).format('DD.MM.YYYY HH:mm')
    },

    getScoreColor(){
      if (this.score > 8){
        return 'tag is-success is-light is-medium';
      } else if (this.score > 6) {
        return 'tag is-success is-light is-medium';
      } else if (this.score > 4) {
        return 'tag is-warning is-light is-medium';
      } else {
        return 'tag is-danger is-light is-medium';
      }
    },
  }

};
</script>