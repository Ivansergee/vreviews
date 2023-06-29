<template>
    <div>
      <p class="title is-4">Предложенные отзывы</p>
      <Suggestion
        v-for="suggestion in suggestions"
        :key="suggestion.id"
        :id="suggestion.id"
        :name="suggestion.name"
        :text="suggestion.text"
        :comment="suggestion.comment"
        :author="suggestion.author_name"
        :score="suggestion.score"
        @process="showCreateLiquid(suggestion.name, suggestion.comment, suggestion.text, suggestion.author)"
      />

      <div class="modal" :class="{ 'is-active': showCreate }" v-if="showCreate">
      <div class="modal-background" @click="showCreate = false"></div>
      <div class="modal-content">
        <div class="box">
        <AdminAddLiquid v-if="options && showCreate"
            :brands=options.brands
            :flavors=options.flavors
            :nic_content=options.nic_content
            :volumes=options.volumes
            :name=modalName
            :comment=modalComment
            :review=modalReview
            :authorId=modalAuthorId
        />
        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="showCreate = false"></button>
    </div>

    </div>
</template>

<style scoped>

</style>

<script>
import axios from 'axios';
import Suggestion from '../components/Suggestion.vue';
import AdminAddLiquid from '../components/AdminAddLiquid.vue';

export default {
  components: {
    Suggestion,
    AdminAddLiquid
  },
  data() {
    return {
      suggestions: null,
      showCreate: false,
      options: null,
      modalName: null,
      modalComment: null,
      modalReview: null,
      modalAuthorId: null
    }
  },
  mounted() {
    this.getSuggestions();
    this.getOptions();
  },
  methods: {
    async getSuggestions(){
      this.$store.commit('setIsLoading', true);

      await axios
        .get('/suggestions/')
        .then(response => {
          this.suggestions = response.data.results;
        })
        .catch(error => {
          console.log(error)
        });

      this.$store.commit('setIsLoading', false);
    },

    async getOptions() {
      await axios
        .get("create-options/")
        .then((response) => {
          this.options = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    showCreateLiquid(name, comment, review, authorId) {
      this.showCreate = true;
      this.modalName = name;
      this.modalComment = comment;
      this.modalReview = review;
      this.modalAuthorId = authorId;
    }
  }
}
</script>