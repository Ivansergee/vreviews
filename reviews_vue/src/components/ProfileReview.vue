<template>
  <div class="review">
    <article class="media">
      <figure class="media-left">
        <p class="image is-64x64">
          <img :src="productImage" />
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <p>
            <router-link :to="{ name: 'product-detail', params: {product_slug: productSlug} }"
            >{{ product }}</router-link>
            <small>{{ created_at }}</small>
            <br />
            <strong>Оценка:</strong> {{ score }}
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
              <small>{{ dislikesCount }}</small>
            </small>
          </p>
        </div>

        <Comment
          v-for="comment in comments"
          :key="comment.id"
          :author="comment.author"
          :text="comment.text"
          :created_at="comment.created_at"
        />
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
</style>

<script>
import axios from "axios";
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

};
</script>