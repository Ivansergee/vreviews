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
                    <a>Like</a> · 
                    <a>Dislike</a> · 
                    <a @click="toggleReplyForm()">{{ commentingPostId === id ? 'Закрыть' : 'Ответить' }}</a>
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
</style>

<script>
import axios from 'axios'
import Comment from '../components/Comment.vue'

export default {
  components: {
      Comment,
  },
  props: ['id', 'author', 'score', 'text', 'created_at', 'comments', 'commentingPostId'],
  emits: ['commenting', 'commented'],
  data() {
      return {
          replyButton: 'Ответить',
          commentText: null,
      }
  },
  methods: {
        toggleReplyForm() {
            if (this.commentingPostId === this.id){
                this.$emit('commenting', 0)
            } else {
                this.$emit('commenting', this.id)
            }
        },

        async addComment() {
            const formData = {
                review: this.id,
                text: this.commentText
            }
            await axios
            .post(`review/${this.id}/comment/`, formData)
            .then(response => {
                this.$emit('commented')
            })
            .catch(error => {
                console.log(error)
            })
        },
  },

}
</script>