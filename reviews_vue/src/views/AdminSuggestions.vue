<template>
    <div>
      <p class="title is-4">Предложенные отзывы</p>
      <Suggestion
        v-for="suggestion in suggestions"
        :key="suggestion.id"
        :id="suggestion.id"
        :name="suggestion.name"
        :nic_type="suggestion.nic_type"
        :text="suggestion.text"
        :comment="suggestion.comment"
        :author="suggestion.author_name"
        :score="suggestion.score"
        :product_slug="suggestion.product_slug"
        :processed="suggestion.processed"
        @process="showCreateLiquid(suggestion.name, suggestion.comment, suggestion.text, suggestion.author, suggestion.score, suggestion.id, suggestion.nic_type)"
      />

      <div class="modal" :class="{ 'is-active': showCreate }" v-if="showCreate">
      <div class="modal-background" @click="showCreate = false"></div>
      <div class="modal-content">
        <div class="box">
        <AdminAddLiquid v-if="options && showCreate"
            :brands=options.brands
            :flavors=options.flavors
            :nic_content=options.nic_content
            :nic_type="modalNicType"
            :volumes=options.volumes
            :name=modalName
            :comment=modalComment
            :review=modalReview
            :authorId=modalAuthorId
            :score=modalScore
            :suggestion_id=modalSuggestionId
            :devices="modalDevices"
            @processed="processSuggestion"
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
      modalNicType: null,
      modalComment: null,
      modalDevices: null,
      modalReview: null,
      modalAuthorId: null,
      modalScore: null,
      modalSuggestionId: null,
      modalDevices: null
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

    async processSuggestion(id, slug){
      await axios
      .patch(`suggestions/${id}/`, {'processed': true, 'product_slug': slug})
      .then(() => {
        this.getSuggestions();
        this.showCreate = false;
      })
      .catch((error) => {
        console.log(error.response.data);
      })
    },

    showCreateLiquid(name, comment, review, authorId, score, suggestion_id, nic_type) {
      this.showCreate = true;
      this.modalName = name;
      this.modalComment = comment;
      this.modalReview = review;
      this.modalAuthorId = authorId;
      this.modalScore = score;
      this.modalSuggestionId = suggestion_id;
      this.modalNicType = nic_type;
      this.modalDevices = devices;
    }
  }
}
</script>