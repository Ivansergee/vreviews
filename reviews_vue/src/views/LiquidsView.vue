<template>
  <div class="products container" v-if="products">
    <p class="title mb-2">Жидкости</p>
    <div class="level is-mobile mb-3">
      <div class="level-left is-mobile">
        
        <div class="level-item mr-3">
          <a class="button has-text-grey-darker" :class="{'is-focused': showFilter}" @click="showFilter = !showFilter">
            <span class="icon">
              <i class="fa-solid fa-filter"></i>
            </span>
            <span>Фильтр</span>
          </a>
        </div>
        
        <div class="dropdown level-item" :class="{'is-active': sortDropdown}">
          <div class="dropdown-trigger">
            <a class="button has-text-grey-darker" @click="sortDropdown = !sortDropdown">
              <i class="fa-solid fa-arrow-down-wide-short mr-1"></i>
              <span>{{ sortBy }}</span>
              <span class="icon is-small" v-if="sortDropdown">
                <i class="fas fa-angle-up" aria-hidden="true"></i>
              </span>
              <span class="icon is-small" v-if="!sortDropdown">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </a>
          </div>
          <div class="dropdown-menu" id="dropdown-menu3" role="menu">
            <div class="dropdown-content">
              <a href="#" class="dropdown-item" @click="sortByRating">
                По оценке
              </a>
              <a href="#" class="dropdown-item" @click="sortByPop">
                По популярности
              </a>
              <a href="#" class="dropdown-item" @click="sortByDate">
                По дате добавления
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="box" v-if="showFilter">
      <p>{{ filter.nic_type }}</p>
      <div class="control">
        <label class="radio">
          <input type="radio" name="nic-type" value="salt" v-model="filter.nic_type">
          Солевой
        </label>
      </div>
      <div class="control">
        <label class="radio">
          <input type="radio" name="nic-type" value="classic" v-model="filter.nic_type">
          Классический
        </label>
      </div>
      <a class="button is-success">Применить</a>
      <a class="button is-danger">Сбросить фильтр</a>
    </div>
    
    <div class="columns is-vcentered is-hidden-mobile list-header">
      <div class="column">
        <p>Изображение</p>
      </div>

      <div class="column">
        <p>Название/Бренд</p>
      </div>

      <div class="column">
        <p>Описание</p>
      </div>

      <div class="column">
        <p>Вкусы</p>
      </div>

      <div class="column">
        <p>Никотин</p>
      </div>

      <div class="column">
        <p>Рейтинг</p>
      </div>
    </div>
    <Product v-for="product in products" :key="product.id" :name="product.name" :brand_name="product.brand.name"
      :brand_slug="product.brand.slug" :nic_content="product.nic_content" :image="product.thumbnail_url"
      :product_slug="product.slug" :description="product.description" :avg_score="product.avg_score"
      :flavors="product.flavors" :reviews_count="product.reviews_count" :score_count="product.score_count" />
    <div class="loadNext">
      <a class="button is-success" @click="getNextLiquids" v-if="nextLiquids">Показать ещё</a>
    </div>
  </div>
</template>

<style scoped>
.loadNext {
  display: flex;
  justify-content: center;
}

.list-header {
  margin-bottom: 0;
  font-weight: 500;
}
</style>

<script>
import axios from 'axios';
import Product from '../components/Product.vue';


export default {
  components: {
    Product
  },
  data() {
    return {
      products: null,
      nextLiquids: null,
      sortBy: 'По оценке',
      sortDropdown: false,
      showFilter: false,
      filter: {
        nic_type: '',
      }
    }
  },
  mounted() {
    this.getProducts()
  },
  methods: {
    async getProducts(ordering='-avg_score,-created_at', filter='') {
      this.$store.commit('setIsLoading', true)

      await axios
        .get(`/products/?${filter}ordering=${ordering}`)
        .then(response => {
          this.products = response.data.results;
          this.nextLiquids = response.data.next;
        })
        .catch(error => {
          console.log(error);
        })

      this.$store.commit('setIsLoading', false)
    },

    async getNextLiquids() {
      await axios
        .get(this.nextLiquids)
        .then((response) => {
          this.products.push(...response.data.results);
          this.nextLiquids = response.data.next;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    sortByRating() {
      this.sortBy = 'По оценке';
      this.sortDropdown = false;
      this.getProducts();
    },

    sortByPop() {
      this.sortBy = 'По популярности';
      this.sortDropdown = false;
      this.getProducts('-score_count');
    },

    sortByDate() {
      this.sortBy = 'По дате добавления';
      this.sortDropdown = false;
      this.getProducts('-created_at');
    },

  },

}
</script>