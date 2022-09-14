<template>
  <div class="review">
    <article class="media">
      <figure class="media-left">
        <p class="image is-64x64">
          <img :src="authorAvatar" />
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <p>
            <strong><router-link :to="{ name: 'profile', params: {username: author} }">{{ author }}</router-link></strong> <small>{{ formatTime(created_at) }}</small>
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
              }}</a> · 

              <a @click="activeModal = true">{{
                $store.state.isAdmin ? "Удалить" : ""
              }}</a>
            </small>
          </p>
        </div>

        <Comment
          v-for="comment in comments"
          :key="comment.id"
          :author="comment.author"
          :authorAvatar="comment.author_avatar"
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
            <button class="button" :disabled="!commentText" @click="addComment()">Отправить</button>
          </p>
        </div>
      </div>
    </article>

    <div
      class="modal is-align-items-center"
      :class="{ 'is-active': activeModal }"
    >
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="box">
          <p class="mb-5">Вы уверены?</p>
          <div class="controls">
            <button class="button is-danger mr-2" @click="deleteReview()">
              Удалить
            </button>
            <button class="button is-light ml-2" @click="activeModal = false">
              Отмена
            </button>
          </div>
        </div>
      </div>
    </div>
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
.controls {
  display: flex;
  justify-content: center;
}
.box p {
  text-align: center;
}
</style>

<script>
import axios from "axios";
import moment from 'moment';

import Comment from "../components/Comment.vue";

export default {
  components: {
    Comment,
  },
  props: [
    "id",
    "author",
    "authorAvatar",
    "score",
    "text",
    "created_at",
    "comments",
    "commentingPostId",
    "userReaction",
    "likesCount",
    "dislikesCount",
  ],
  emits: ["commenting", "commented", "rated", "deleted"],
  data() {
    return {
      commentText: null,
      activeModal: false,
    };
  },
  methods: {
    formatTime(time) {
      return moment(time).format('DD.MM.YYYY HH:mm')
    },

    toggleReplyForm() {
      if (!this.$store.state.isAuthenticated) {
        this.$root.showLogIn = true;
        return null;
      }

      if (this.commentingPostId === this.id) {
        this.$emit("commenting", 0);
      } else {
        this.$emit("commenting", this.id);
      }
    },

    async deleteReview() {
      await axios
        .delete(`reviews/${this.id}/delete/`)
        .then(() => {
          this.$emit("deleted", this.id);
          this.activeModal = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async addComment() {
      const formData = {
        review: this.id,
        text: this.commentText,
      };
      await axios
        .post(`reviews/${this.id}/comment/`, formData)
        .then(() => {
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
        this.$root.showLogIn = true;
        return null;
      }
      if (this.userReaction === null) {
        await axios
          .post(`reviews/${this.id}/rate/`, { like: reaction })
          .then(() => {
            this.$emit("rated", { id: this.id, like: reaction });
          })
          .catch((error) => {
            console.log(error);
          });
      } else if (this.userReaction !== reaction) {
        await axios
          .patch(`reviews/${this.id}/rate/`, { like: reaction })
          .then(() => {
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