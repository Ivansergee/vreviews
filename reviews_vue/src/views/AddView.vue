<template>
  <div class="container">
    <div v-if="!isLoading">
      <div class="tabs is-medium">
        <ul>
          <li :class="[$route.params.type === 'liquid' || !$route.params.type ? 'is-active' : '']">
            <a @click="setActiveTab('liquid')">Добавить жидкость</a>
          </li>
          <li :class="[$route.params.type === 'disposable' ? 'is-active' : '']">
            <a @click="setActiveTab('disposable')">Добавить одноразовое устройство</a>
          </li>
          <li :class="[$route.params.type === 'brand' ? 'is-active' : '']">
            <a @click="setActiveTab('brand')">Добавить бренд</a>
          </li>
          <li :class="[$route.params.type === 'producer' ? 'is-active' : '']">
            <a @click="setActiveTab('producer')">Добавить производителя</a>
          </li>
        </ul>
      </div>
    
      <AddLiquid v-if="($route.params.type === 'liquid' || !$route.params.type) && options"
        :brands=options.brands
        :flavors=options.flavors
        :nic_content=options.nic_content
        :volumes=options.volumes
      />
      <AddDisposable v-if="$route.params.type === 'disposable'"

      />
      <AddBrand v-if="$route.params.type === 'brand' && options"
        :producers=options.producers
        @added="getOptions()"
      />
      <AddProducer v-if="$route.params.type === 'producer' && options"
        :countries=options.countries
        @added="getOptions()"
      />
    </div>

    <div class="loading" v-else>
      <PulseLoader
        :loading="isLoading"
        :size="size"
      />
    </div>
  </div>

</template>

<style scoped>
/* .v-spinner {
  text-align: center;
} */

.loading {
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<script>
import AddLiquid from '../components/AddLiquid.vue';
import AddDisposable from '../components/AddDisposable.vue';
import AddBrand from '../components/AddBrand.vue';
import AddProducer from '../components/AddProducer.vue';
import axios from "axios";

import PulseLoader from 'vue-spinner/src/PulseLoader.vue';


export default {
  components: {
    AddLiquid,
    AddDisposable,
    AddBrand,
    AddProducer,
    PulseLoader
  },
  data() {
    return {
      activeTab: 'addLiquid',
      options: null,
      isLoading: false,
      size: '25px',
    };
  },
  mounted() {
    this.show404();
    this.getOptions();
  },
  methods: {
    show404(){
      const types = ['liquid', 'disposable', 'brand', 'producer'];
      if (this.$route.params.type && !types.includes(this.$route.params.type)){
        this.$router.push({name: 'not-found'});
      }
    },

    setActiveTab(tab){
      this.$router.replace({ name: 'add', params: { type: tab } });
    },

    async getOptions() {
      this.isLoading = true;
      await axios
        .get("create-options/")
        .then((response) => {
          this.options = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
      this.isLoading = false;
    },
  },
};
</script>