<template>
    <div class="brands container" v-if="brands">
      <p class="title">Топ брендов</p>
      <Brand
        v-for="brand in brands"
        :key="brand.id"
        :name="brand.name"
        :image="brand.thumbnail_url"
        :slug="brand.slug"
        :description="brand.description"
        :avg_score="brand.avg_score"
        :reviews_count="brand.reviews_count"
        :score_count="brand.score_count"
      />
      <div class="loadNext">
        <a
          class="button is-success"
          @click="getNextBrands"
          v-if="nextBrands"
          >Показать ещё</a>
      </div>
    </div>
</template>

<style scoped>
.loadNext {
  display: flex;
  justify-content: center;
}

</style>

<script>
import axios from 'axios';
import Brand from '../components/Brand.vue';


export default {
  components: {
    Brand
  },
  data() {
    return {
      brands: null,
      nextBrands: null,
    }
  },
  mounted() {
    this.getBrands()
  },
  methods: {
    async getBrands(){
      this.$store.commit('setIsLoading', true)

      await axios
        .get('/brands/?ordering=-avg_score')
        .then(response => {
          this.brands = response.data.results;
          this.nextBrands = response.data.next;
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },

    async getNextBrands() {
      await axios
        .get(this.nextBrands)
        .then((response) => {
          this.brands.push(...response.data.results);
          this.nextBrands = response.data.next;
        })
        .catch((error) => {
          console.log(error);
        });
    },

  },

    
}
</script>