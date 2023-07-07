<template>
  <div class="container" v-if="brand">
    <div class="level">
      <div class="level-left">
        <h1 class="title level-item">{{ brand.name }}</h1>
      </div>
      <div class="level-right" v-if="$store.state.isAdmin">
        <button class="button is-success level-item" @click="showEdit = true">Редактировать</button>
      </div>
    </div>
    <div class="columns head">
      <div class="column is-4">
        <figure class="image is-1by1">
          <img id="brand-image" :src="brand.thumbnail_url" @click="showImage=true" />
        </figure>
      </div>
      <div class="column is-4">
        <div class="content">
          <p><strong>Страна:</strong> {{brand.producer.country}} </p>
          <p><strong>Производитель:  </strong>   
          <router-link
              :to="{
                name: 'producer-detail',
                params: { producer_slug: brand.producer.slug },
              }"
              >{{ brand.producer.name }}</router-link> </p>
          <p><strong>Содержание никотина:</strong></p>
          <p class="tags">
            <span
              class="tag is-warning"
              v-for="nic in brand.nic_content"
              :key="nic.id"
              >{{ nic.amount }}</span
            >
          </p>
          <p>
            <strong>Объем: </strong>
            <span>{{ listVolumes }}</span>
          </p>
          <p><strong>Описание:</strong></p>
          <p>{{ brand.description }}</p>
        </div>
      </div>
      <div class="column is-4">
        <div class="content">
          <p class="title is-4">Средняя оценка:</p>
          <div class="tags are-large has-addons">
            <span class="tag"><i class="bi bi-star-fill"></i></span>
            <span class="tag is-primary">{{ brand.avg_score }}</span>
          </div>
          <p><strong>Отзывов:</strong> {{ brand.reviews_count || 0 }}</p>
          <p><strong>Оценок:</strong> {{ brand.score_count || 0 }}</p>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': showImage }">
      <div class="modal-background" @click="showImage = false"></div>
      <div class="modal-content">
        <p class="image">
          <img :src="brand.image_url">
        </p>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="showImage = false"></button>
    </div>

    <div class="modal" :class="{ 'is-active': showEdit }" v-if="brand.producer && showEdit">
      <div class="modal-background" @click="showEdit = false"></div>
      <div class="modal-content">
        <div class="box">
        <EditBrand
          :name="brand.name"
          :description="brand.description"
          :producer="{name: brand.producer.name, id: brand.producer.id}"
          :nic_content="brand.nic_content"
          :volumes="brand.volume ? brand.volume : null"
          :is_salt="brand.is_salt"
          :image="brand.image_url"
          @added="updateInfo"
        />
        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="showEdit = false"></button>
    </div>

    <div class="products" v-if="products">
      <p class="title">Все вкусы {{ brand.name }} ({{ productsCount }})
        <router-link :to="{ name: 'add', params: {type: 'liquid'}, query:{brandId: brand.id} }" class="add button is-success">
          Добавить новый вкус
        </router-link>
      </p>
      <Product
        v-for="product in products"
        :key="product.id"
        :name="product.name"
        :brand_name="product.brand.name"
        :brand_slug="product.brand.slug"
        :nic_content="product.nic_content"
        :image="product.thumbnail_url"
        :product_slug="product.slug"
        :description="product.description"
        :avg_score="product.avg_score"
        :flavors="product.flavors"
        :reviews_count="product.reviews_count"
        :score_count="product.score_count"
      />
      <div class="loadButton">
        <a
        class="button is-success"
        @click="getNextProducts"
        v-if="nextProducts"
        >Показать ещё</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
#brand-image {
  max-width: 300px;
  max-height: 300px;
}
#brand-image:hover {
  cursor: pointer;
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
.loadButton {
  display: flex;
  justify-content: center;
}

.add {
  float: right;
}

</style>

<script>
import axios from 'axios';
import Product from '../components/Product.vue';
import EditBrand from '../components/EditBrand.vue';


export default {
  components: {
    Product,
    EditBrand,

  },
  data() {
    return {
      brand: null,
      products: null,
      productsCount: null,
      nextProducts: null,
      showImage: false,
      showEdit: false,
    }
  },
  computed: {
    listVolumes() {
      const volList = [];
      for (var vol of this.brand.volume) {
        volList.push(vol.volume + ' мл');
      }
      return volList.join(", ");
    },
  },
  mounted() {
    this.getBrandData();
    this.getProducts();
  },
  methods: {
    updateInfo(slug) {
      if (slug != this.$route.params.brand_slug) {
        this.$router.replace({ name: 'brand-detail', params: { brand_slug: slug } });
        this.getBrandData(slug);
      } else {
        this.getBrandData();
      }
      this.showEdit = false;
    },

    async getBrandData(slug=this.$route.params.brand_slug){
      this.$store.commit('setIsLoading', true)

      await axios
        .get(`/brands/${slug}/`)
        .then(response => {
          this.brand = response.data;
          this.setTitle(this.brand.name);
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },

    async getProducts(){
      this.$store.commit('setIsLoading', true);

      const brand_slug = this.$route.params.brand_slug;

      await axios
        .get(`/products/?brand=${brand_slug}&ordering=-avg_score,-created_at`)
        .then(response => {
          this.products = response.data.results;
          this.nextProducts = response.data.next;
          this.productsCount = response.data.count;
        })
        .catch(error => {
          console.log(error);
        });

      this.$store.commit('setIsLoading', false);
    },

    async getNextProducts() {
      await axios
        .get(this.nextProducts)
        .then((response) => {
          this.products.push(...response.data.results);
          this.nextProducts = response.data.next;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    setTitle(title) {
      document.title = `${title} | VapeRate`;
    }
  },
}
</script>