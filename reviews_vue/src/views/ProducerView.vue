<template>
  <div class="container" v-if="producer">
    <div class="level">
      <div class="level-left">
        <h1 class="title level-item">{{ producer.name }}</h1>
      </div>
    </div>
    <div class="columns head">
      <div class="column is-4">
        <figure class="image is-1by1">
          <img
            :src=producer.image_url
          />
        </figure>
      </div>
      <div class="column is-4">
        <div class="content">
          <p><strong>Страна:</strong> {{producer.country}} </p>
          <p v-if="producer.website"><strong>Сайт:</strong> <a :href="producer.website">{{producer.website}}</a></p>
          <p v-if="producer.vk"><strong>VK:</strong> <a :href="producer.vk">{{producer.vk}}</a> </p>
          <p v-if="producer.tg"><strong>Telegram:</strong> <a :href="producer.tg">{{producer.tg}}</a> </p>
          <p v-if="producer.ig"><strong>Instagram:</strong> <a :href="producer.ig">{{producer.ig}}</a> </p>

          <p><strong>Описание:</strong></p>
          <p>{{ producer.description }}</p>
        </div>
      </div>
      <div class="column is-4">
        <div class="content">
          <p class="title is-4">Средняя оценка:</p>
          <div class="tags are-large has-addons">
            <span class="tag"><i class="bi bi-star-fill"></i></span>
            <span class="tag is-primary">{{ producer.avg_score > 0 ? producer.avg_score : '-' }}</span>
          </div>
          <p><strong>Отзывов:</strong> {{ producer.reviews_count || 0 }}</p>
          <p><strong>Оценок:</strong> {{ producer.score_count || 0 }}</p>
        </div>
      </div>
    </div>

    <div class="products" v-if="brands">
      <p class="title">Все линейки {{ producer.name }}</p>
      <Brand
        v-for="brand in brands"
        :key="brand.id"
        :name="brand.name"
        :image="brand.thumbnail_url"
        :slug="brand.slug"
        :nic_content="brand.nic_content"
        :description="brand.description"
        :avg_score="brand.avg_score"
        :reviews_count="brand.reviews_count"
        :score_count="brand.score_count"
      />
    </div>
  </div>
</template>

<style scoped>
img {
  max-width: 300px;
  max-height: 300px;
}

.head {
  margin: 2em auto;
  padding: 2em;
  background-color: white;
}
.is-vcentered {
  margin: 2em auto !important;
  height: 100%;
  background-color: white;
}

</style>

<script>
import axios from 'axios'
import Brand from '../components/Brand.vue'


export default {
  components: {
    Brand
  },
  data() {
    return {
      producer: null,
      brands: null,
    }
  },
  created() {
    this.getProducerData();
    this.getBrands();
  },
  methods: {
    async getProducerData(){
      this.$store.commit('setIsLoading', true)

      const producerSlug = this.$route.params.producer_slug;

      await axios
        .get(`/producers/${producerSlug}/`)
        .then(response => {
          this.producer = response.data;
          this.setTitle(this.producer.name);
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },

    async getBrands(){
      this.$store.commit('setIsLoading', true);

      const producerSlug = this.$route.params.producer_slug;

      await axios
        .get(`/brands/?producer=${producerSlug}&ordering=-avg_score,-created_at`)
        .then(response => {
          this.brands = response.data.results;
        })
        .catch(error => {
          console.log(error);
        });

      this.$store.commit('setIsLoading', false);
    },

    setTitle(title) {
      document.title = `${title} | VapeRate`;
    }
  },
}
</script>