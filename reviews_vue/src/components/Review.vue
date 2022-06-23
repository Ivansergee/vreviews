<template>
  <div class="review">
    <article class="media">
      <figure class="media-left">
        <p class="image is-64x64">
          <img src="http://localhost:8000/media/placeholder.jpg" />
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <p>
            <strong>{{ author }}</strong> <small>{{ created_at }}</small>
            <br />
            <strong>Оценка:</strong> {{ score }}
            <br />
            {{ text }}
            <br />
            <small>
              <a @click="manageReaction(true)">
                <i
                  class="fa-thumbs-up"
                  :class="[userReaction === true ? 'fa-solid' : 'fa-regular']"
                ></i>
              </a>
              <small>{{ likesCount }}</small> ·
              <a @click="manageReaction(false)">
                <i
                  class="fa-thumbs-down"
                  :class="[userReaction === false ? 'fa-solid' : 'fa-regular']"
                ></i>
              </a>
              <small>{{ dislikesCount }}</small> ·
              <a @click="toggleReplyForm()">{{
                commentingPostId === id ? "Закрыть" : "Ответить"
              }}</a>
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

    <article class="media reply-form">
      <div class="media-content" v-if="commentingPostId === id">
        <div class="field">
          <p class="control">
            <textarea
              class="textarea"
              placeholder="Ваш комментарий..."
              v-model="commentText"
            ></textarea>
          </p>
        </div>
        <div class="field">
          <p class="control">
            <button class="button" @click="addComment()">Отправить</button>
          </p>
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
</style>

<script>
import axios from "axios";

import Comment from "../components/Comment.vue";

export default {
  components: {
    Comment,
  },
  props: [
    "id",
    "author",
    "score",
    "text",
    "created_at",
    "comments",
    "commentingPostId",
    "userReaction",
    "likesCount",
    "dislikesCount",
  ],
  emits: ["commenting", "commented", "rated"],
  data() {
    return {
      commentText: null,
    };
  },
  methods: {
    toggleReplyForm() {
      if (!this.$store.state.isAuthenticated) {
        this.$root.showLoginRequired();
        return null;
      }

      if (this.commentingPostId === this.id) {
        this.$emit("commenting", 0);
      } else {
        this.$emit("commenting", this.id);
      }
    },

    async addComment() {
      const formData = {
        review: this.id,
        text: this.commentText,
      };
      await axios
        .post(`reviews/${this.id}/comment/`, formData)
        .then((response) => {
          this.$emit("commented");
          this.commentText = null;
          this.toggleReplyForm();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async manageReaction(reaction) {
      if (!this.$store.state.isAuthenticated) {
        this.$root.showLoginRequired();
        return null;
      }
      if (this.userReaction === null) {
        await axios
          .post(`reviews/${this.id}/rate/`, { like: reaction })
          .then((response) => {
            this.$emit("rated", { id: this.id, like: reaction });
          })
          .catch((error) => {
            console.log(error);
          });
      } else if (this.userReaction !== reaction) {
        await axios
          .patch(`reviews/${this.id}/rate/`, { like: reaction })
          .then((response) => {
            this.$emit("rated", { id: this.id, like: reaction });
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        await axios
          .delete(`reviews/${this.id}/rate/`)
          .then((response) => {
            this.$emit("rated", { id: this.id, like: reaction });
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
};
</script>