<template>
    <div class="columns add-liquid">
      <div class="column is-6 is-offset-3">
        <h1 class="title is-4">Добавление новой жидкости</h1>
        <form @submit.prevent="submitForm">

          <div class="field">
            <label><span class="subtitle">Название</span></label>
            <div class="control">
              <input type="text" class="input" v-model="productData.name" />
            </div>
            <p class="help">Название жидкости без названия бренда</p>
          </div>

          <div class="field">
            <label><span class="subtitle">Бренд</span></label>
            <div class="control">
              <VueMultiselect
                v-model="productData.brand"
                :options="brands"
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

          <div class="field">
            <label><span class="subtitle">Вкусы</span></label>
            <div class="control">
              <VueMultiselect
                v-model="productData.flavors"
                :options="flavors"
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
            <label><span class="subtitle">Содержание никотина</span></label>
            <br />
            <div class="select is-multiple">
              <select multiple size="5" v-model="productData.nic_content">
                <option
                  v-for="amount in nic_content"
                  :key="amount.id"
                  :value="amount.id"
                >
                  {{ amount.amount }}
                </option>
              </select>
            </div>
          </div>

          <div class="field">
            <label><span class="subtitle">Объем</span></label>
            <br />
            <div class="select is-multiple">
              <select multiple size="5" v-model="productData.volumes">
                <option
                  v-for="vol in volumes"
                  :key="vol.id"
                  :value="vol.id"
                >
                  {{ vol.volume }} мл
                </option>
              </select>
            </div>
          </div>

          <div class="field">
            <label><span class="subtitle">VG/PG</span></label>
            <div class="control">
              <input type="number" class="input vg" v-model="productData.vg" /><span>   /   </span><input type="number" class="input vg" :value="pg" readonly/>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <label class="checkbox">
                <input type="checkbox" v-model="productData.is_salt" />
                Солевой никотин
              </label>
            </div>
          </div>

          <div class="field">
            <label><span class="subtitle">Изображение</span></label>
            <div class="control" v-if="image.src">
              <cropper
                class="cropper"
                ref="cropper"
                :src="image.src"
                :stencil-props="{
                  handlers: {},
                  movable: false,
                  scalable: false,
                }"
                :stencil-size="{
                  width: 300,
                  height: 300,
                }"
                image-restriction="none"
                @change="change"
              />
            </div>
            <p class="help">Добавьте фото жидкости и выберите участок, который будет использован для превью. Для зума используйте колесико мыши или стандартный жест на смартфоне.</p>
          </div>

          <div class="file has-name">
            <label class="file-label">
              <input
                class="file-input"
                type="file"
                accept="image/png, image/jpeg"
                @change="uploadImage($event)"
                name="image"
              />
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
                <span class="file-label"> Выберите файл </span>
              </span>
              <span class="file-name">{{ image.name }}</span>
            </label>
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

</template>

<style scoped>
.cropper {
  height: 400px;
  width: 400px;
  background: #ddd;
}
.cropper:hover {
  cursor: move;
}
.vg {
  width: 8ch;
}
</style>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>

<script>
import axios from "axios";
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";
import VueMultiselect from 'vue-multiselect';
import { toast } from "bulma-toast";

export default {
  components: {
    Cropper,
    VueMultiselect,
  },
  props: {
    brands: {
      type: Array,
      default: []
    },
    flavors: {
      type: Array,
      default: []
    },
    nic_content: {
      type: Array,
      default: []
    },
    volumes: {
      type: Array,
      default: []
    },
  },
  data() {
    return {
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
    this.setBrand();
  },
  computed: {
    pg() {
      return 100 - this.productData.vg
    }
  },
  methods: {
    setBrand() {
      const brandId = this.$route.query.brandId;

      if (brandId) {
        for (const brand of this.brands) {
          if (brand.id == brandId) {
            this.productData.brand = {id: brand.id, name: brand.name}
          }
        }
      }
    },

    change({ coordinates, canvas }) {
      canvas.toBlob((blob) => {
        this.image.thumbnail = blob
      }, this.image.type);
    },

    submitForm() {
      const formData = new FormData();
      for (var i of this.productData.flavors) {
        formData.append("flavor_id", i.id);
      }
      for (var i of this.productData.nic_content) {
        formData.append("nic_content_id", i);
      }
      for (var i of this.productData.volumes) {
        formData.append("volume_id", i);
      }
      if (this.image.file){
        formData.append("image", this.image.file);
      }
      if (this.image.thumbnail){
        formData.append("thumbnail", this.image.thumbnail, this.image.name);
      }
      formData.append("name", this.productData.name);
      formData.append("vg", this.productData.vg);
      formData.append("description", this.productData.description);
      formData.append("brand_id", this.productData.brand.id);
      formData.append("is_salt", this.productData.is_salt);

      axios
        .post("products/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(() => {
          this.showSuccess();
          this.productData = {
            name: "",
            description: "",
            nic_content: [],
            flavors: [],
            volumes: [],
            brand: this.productData.brand,
            vg: 50,
            is_salt: false,
          };
          this.image = {
            src: null,
            type: null,
            name: null,
            file: null,
            thumbnail: null,
          };
          this.setBrand();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    uploadImage(event) {
      const { files } = event.target;
      if (files && files[0]) {
        if (this.image.src) {
          URL.revokeObjectURL(this.image.src);
        }
        const src = URL.createObjectURL(files[0]);

        this.image.src = src;
        this.image.type = files[0].type;
        this.image.name = files[0].name;
        this.image.file = files[0];
      }
    },

    showSuccess() {
      toast({
        message: "Спасибо! Информация отправлена на проверку и скоро будет опубликована на сайте.",
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