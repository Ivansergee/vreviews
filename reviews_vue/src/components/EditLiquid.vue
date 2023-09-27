<template>
  <div>
    <div class="modal" :class="{ 'is-active': showEditImage }" v-if="showEditImage">
      <div class="modal-background" @click="showEditImage = false"></div>
      <div class="modal-content">
        <div class="box">
          <EditImage :image=image :type="'product'" @changed="showEditImage = false" />
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
              <input type="text" class="input" :class="{ 'is-danger': errors.name }" v-model="productData.name" />
            </div>
            <p class="help">Название жидкости без названия бренда</p>
            <p class="help is-danger" v-if="errors.name">{{ errors.name[0] }}</p>
          </div>

          <div class="field" v-if="options">
            <label><span class="subtitle">Бренд</span></label>
            <div class="control">
              <VueMultiselect v-model="productData.brand" :options="options.brands" :multiple="false" selectLabel="Выбрать"
                selectedLabel="Выбрано" deselectLabel="Удалить" placeholder="Выберите бренд" label="name" track-by="id"
                @select="getBrandData" />
            </div>
            <p class="help">Выберите бренд. Для поиска начните набирать название</p>
            <p class="help is-danger" v-if="errors.brand">{{ errors.brand[0] }}</p>
          </div>

          <div class="field">
            <label><span class="subtitle">Описание</span></label>
            <div class="control">
              <textarea class="textarea" cols="100" rows="5" v-model="productData.description">
      </textarea>
            </div>
            <p class="help">Описание вкуса</p>
            <p class="help is-danger" v-if="errors.description">{{ errors.description[0] }}</p>
          </div>

          <div class="field" v-if="options">
            <label><span class="subtitle">Вкусы</span></label>
            <div class="control">
              <VueMultiselect v-model="productData.flavors" :options="options.flavors" :multiple="true" selectLabel="Выбрать"
                selectedLabel="Выбрано" deselectLabel="Удалить" placeholder="Выберите вкусы" label="name" track-by="id" />
            </div>
            <p class="help">Для поиска начните набирать название</p>
            <p class="help is-danger" v-if="errors.flavors">{{ errors.flavors[0] }}</p>
          </div>

          <div class="field">
            <label><span class="subtitle">Тип никотина</span></label>
            <div class="control">
              <label class="radio">
                <input type="radio" name="nictype" value="salt" v-model="productData.nicType">
                Солевой
              </label>
              <label class="radio">
                <input type="radio" name="nictype" value="classic" v-model="productData.nicType">
                Классический
              </label>
            </div>
            <p class="help is-danger" v-if="errors.nicType">{{ errors.nicType[0] }}</p>
          </div>

          <div class="field">
            <label><span class="subtitle">Содержание никотина</span></label>
            <div class="control" v-for="amount in nic_content" :key="amount.id">
              <label class="checkbox">
                <input type="checkbox" :value="amount.id" v-model="productData.nic_content" />
                {{ amount.amount }} мг
              </label>
            </div>
          </div>

          <div class="field">
            <label><span class="subtitle">Объем</span></label>
            <div class="control" v-for="vol in volumes" :key="vol.id">
              <label class="checkbox">
                <input type="checkbox" :value="vol.id" v-model="productData.volumes" />
                {{ vol.volume }} мг
              </label>
            </div>
          </div>

          <div class="field">
            <label><span class="subtitle">VG/PG</span></label>
            <div class="control">
              <input type="number" class="input vg" v-model="productData.vg" /><span> / </span><input type="number"
                class="input vg" :value="pg" readonly />
            </div>
          </div>

          <div class="field">
            <label><span class="subtitle">Изображение</span></label>
            <div class="control" v-if="image.src">
              <cropper class="cropper" ref="cropper" :src="image.src" :stencil-props="{
                handlers: {},
                movable: false,
                scalable: false,
              }" :stencil-size="{
  width: 300,
  height: 300,
}" image-restriction="none" @change="change" />
            </div>
            <p class="help">Добавьте фото жидкости и выберите участок, который будет использован для превью. Для зума
              используйте колесико мыши или стандартный жест на смартфоне.</p>
          </div>

          <div class="file has-name">
            <label class="file-label">
              <input class="file-input" type="file" accept="image/png, image/jpeg" @change="uploadImage($event)"
                name="image" />
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
                <span class="file-label"> Выберите файл </span>
              </span>
              <span class="file-name">{{ image.name }}</span>
            </label>
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
    "nicType",
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
        name: "",
        description: "",
        flavors: [],
        nic_content: [],
        nicType: null,
        vg: 50,
        volumes: [],
        brand: "",
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
    this.productData.nicType = this.nicType;
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
      if (this.image.file) {
        formData.append("image", this.image.file);
      }
      if (this.image.thumbnail) {
        formData.append("thumbnail", this.image.thumbnail, this.image.name);
      }
      formData.append("name", this.productData.name);
      formData.append("vg", this.productData.vg);
      formData.append("nic_type", this.productData.nicType);
      for (var i of this.productData.nic_content) {
        formData.append("nic_content_id", i);
      }
      for (var i of this.productData.volumes) {
        formData.append("volume_id", i);
      }
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