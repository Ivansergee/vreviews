<template>
  <div class="container">
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
  
    <AddLiquid v-if="$route.params.type === 'liquid' || !$route.params.type"/>
    <AddDisposable v-if="$route.params.type === 'disposable'"/>
    <AddBrand v-if="$route.params.type === 'brand'"/>
    <AddProducer v-if="$route.params.type === 'producer'"/>
  </div>

</template>

<script>
import AddLiquid from '../components/AddLiquid.vue';
import AddDisposable from '../components/AddDisposable.vue';
import AddBrand from '../components/AddBrand.vue';
import AddProducer from '../components/AddProducer.vue';

export default {
  components: {
    AddLiquid,
    AddDisposable,
    AddBrand,
    AddProducer
  },
  data() {
    return {
      activeTab: 'addLiquid',
      options: [],
      image: {
        src: null,
        type: null,
        name: null,
        file: null,
        thumbnail: null,
      },
      errors: [],
      productData: {
        name: "",
        description: "",
        nic_content: [],
        flavors: [],
        volumes: [],
        vg: 50,
        brand: "",
        is_salt: false,
      },
    };
  },
  mounted() {
    this.show404();
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
    
  },
};
</script>