<template>
  <div>
    <div class="modal" :class="{ 'is-active': showEditImage }" v-if="showEditImage">
      <div class="modal-background" @click="showEditImage = false"></div>
      <div class="modal-content">
        <div class="box">
          <EditImage
          :image=image
          :type="'product'"
          @changed="showEditImage = false"
          />
        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="showEditImage = false"></button>
    </div>

    <div class="columns add-liquid">
      <div class="column is-6 is-offset-3">
        <h1 class="title is-4">Редактирование жидкости</h1>
        <form @submit.prevent="submitForm">

          <div class="field">
            <label><span class="subtitle">Название</span></label>
            <div class="control">
              <input type="text" class="input" v-model="productData.name" />
            </div>
            <p class="help">Название жидкости без названия бренда</p>
          </div>

          <div class="field" v-if="options">
            <label><span class="subtitle">Бренд</span></label>
            <div class="control">
              <VueMultiselect
                v-model="productData.brand"
                :options="options.brands"
                :multiple="false"
                selectLabel="Выбрать"
                selectedLabel="Выбрано"
                deselectLabel="Удалить"
                placeholder="Выберите бренд"
                label="name"
                track-by="id"
              />
            </div>
            <p class="help">Выберите бренд. Для поиска начните набирать название</p>
          </div>

          <div class="field">
            <label><span class="subtitle">Описание</span></label>
            <div class="control">
              <textarea
                class="textarea"
                cols="100"
                rows="5"
                v-model="productData.description"
              >
              </textarea>
            </div>
            <p class="help">Описание вкуса</p>
          </div>

          <div class="field" v-if="options">
            <label><span class="subtitle">Вкусы</span></label>
            <div class="control">
              <VueMultiselect
                v-model="productData.flavors"
                :options="options.flavors"
                :multiple="true"
                selectLabel="Выбрать"
                selectedLabel="Выбрано"
                deselectLabel="Удалить"
                placeholder="Выберите вкусы"
                label="name"
                track-by="id"
              />
            </div>
            <p class="help">Для поиска начните набирать название</p>
          </div>

          <div class="field">
            <label><span class="subtitle">VG/PG</span></label>
            <div class="control">
              <input type="number" class="input vg" v-model="productData.vg" /><span>   /   </span><input type="number" class="input vg" :value="pg" readonly/>
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </div>

          <div class="field mt-4">
            <div class="control">
              <button class="button is-dark">Отправить</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vg {
  width: 8ch;
}
</style>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>

<script>
import axios from "axios";
import VueMultiselect from 'vue-multiselect';
import { toast } from "bulma-toast";

import EditImage from './EditImage.vue';

export default {
  components: {
    VueMultiselect,
    EditImage
  },
  props: [
    "brand",
    "flavors",
    "name",
    "description",
    "vg",
    "image"
  ],
  data() {
    return {
      showEditImage: false,
      isLoading: true,
      errors: [],
      options: null,
      productData: {
        name: null,
        description: null,
        flavors: [],
        vg: 50,
        brand: null,
      },
    };
  },
  computed: {
    pg() {
      return 100 - this.productData.vg
    }
  },
  mounted() {
    this.getOptions();
    this.productData.name = this.name;
    this.productData.description = this.description;
    this.productData.vg = this.vg;
    this.productData.brand = this.brand;
    this.productData.flavors = this.flavors;
  },
  methods: {
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

    submitForm() {
      const formData = new FormData();

      for (var i of this.productData.flavors) {
        formData.append("flavor_id", i.id);
      }
      formData.append("name", this.productData.name);
      formData.append("vg", this.productData.vg);
      formData.append("description", this.productData.description);
      formData.append("brand_id", this.productData.brand.id);

      axios
        .patch(`products/${this.$route.params.product_slug}`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(() => {
          this.showSuccess();
          this.productData = {
            name: null,
            description: null,
            flavors: [],
            brand: null,
            vg: 50,
          };
        })
        .catch((error) => {
          console.log(error);
        });
    },

    showSuccess() {
      toast({
        message: "Информация обновлена",
        type: "is-success",
        dismissible: true,
        duration: 10000,
        pauseOnHover: true,
        position: "top-center",
      });
    },
  },
};
</script>