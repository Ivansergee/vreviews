<template>
  <div class="container">
    <div v-if="!isLoading">
    
      <AddLiquid v-if="($route.params.type === 'liquid') && options"
        :brands=options.brands
        :flavors=options.flavors
        :nic_content=options.nic_content
        :volumes=options.volumes
      />
      <AddBrand v-if="$route.params.type === 'brand' && options"
        :producers=options.producers
        :nic_content=options.nic_content
        :volumes=options.volumes
        @added="getOptions()"
      />
      <AddProducer v-if="$route.params.type === 'producer' && options"
        :countries=options.countries
        @added="getOptions()"
      />
      <AddSuggestion v-if="$route.params.type === 'suggestion' || !$route.params.type" />
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
.tabs {
  overflow: auto;
  white-space: nowrap;
}

.loading {
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<script>
import AddLiquid from '../components/AddLiquid.vue';
import AddBrand from '../components/AddBrand.vue';
import AddProducer from '../components/AddProducer.vue';
import AddSuggestion from '../components/AddSuggestion.vue';
import axios from "axios";

import PulseLoader from 'vue-spinner/src/PulseLoader.vue';


export default {
  components: {
    AddLiquid,
    AddBrand,
    AddProducer,
    AddSuggestion,
    PulseLoader
  },
  data() {
    return {
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
      const types = ['liquid', 'suggestion', 'brand', 'producer'];
      if ((this.$route.params.type === 'brand' || this.$route.params.type === 'producer') && !this.$store.state.isAdmin){
        this.$router.replace({name: 'not-found'});
      }
      if (this.$route.params.type && !types.includes(this.$route.params.type)){
        this.$router.replace({name: 'not-found'});
      }
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