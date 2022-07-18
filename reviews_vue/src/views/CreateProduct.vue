<template>
  <div class="add-product">
    <div class="columns">
      <div class="column is-6 is-offset-3">
        <h1 class="title">Добавление жидкости</h1>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label><span class="subtitle">Название</span></label>
            <div class="control">
              <input type="text" class="input" v-model="productData.name" />
            </div>
          </div>

          <div class="field" v-if="options">
            <label><span class="subtitle">Бренд</span></label>
            <br />
            <div class="select">
              <select v-model="productData.brand">
                <option
                  v-for="brand in options.brands"
                  :key="brand.id"
                  :value="brand.id"
                >
                  {{ brand.name }}
                </option>
              </select>
            </div>
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
          </div>

          <div class="field" v-if="options">
            <label><span class="subtitle">Вкусы</span></label>
            <br />
            <div class="select is-multiple">
              <select multiple size="5" v-model="productData.flavors">
                <option
                  v-for="flavor in options.flavors"
                  :key="flavor.id"
                  :value="flavor.id"
                >
                  {{ flavor.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="field" v-if="options">
            <label><span class="subtitle">Содержание никотина</span></label>
            <br />
            <div class="select is-multiple">
              <select multiple size="5" v-model="productData.nic_content">
                <option
                  v-for="amount in options.nic_content"
                  :key="amount.id"
                  :value="amount.id"
                >
                  {{ amount.amount }}
                </option>
              </select>
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
                image-restriction="stencil"
              />
            </div>
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

          <div class="field">
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
.cropper {
  height: 400px;
  width: 400px;
  background: #ddd;
}
.cropper:hover {
  cursor: move;
}
</style>

<script>
import axios from "axios";
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";
import { toast } from "bulma-toast";

export default {
  components: {
    Cropper,
  },
  data() {
    return {
      options: null,
      image: {
        src: null,
        type: null,
        name: null,
      },
      errors: [],
      productData: {
        name: "",
        description: "",
        nic_content: [],
        flavors: [],
        brand: "",
        is_salt: false,
      },
    };
  },
  mounted() {
    this.getOptions();
  },
  methods: {
    submitForm() {
      const formData = new FormData();

      const result = this.$refs.cropper.getResult();
      result.canvas.toBlob((blob) => {
        for (var i of this.productData.flavors) {
          formData.append("flavor_id", i);
        }
        for (var i of this.productData.nic_content) {
          formData.append("nic_content_id", i);
        }
        formData.append("image", blob, this.image.name);
        formData.append("name", this.productData.name);
        formData.append("description", this.productData.description);
        formData.append("brand_id", this.productData.brand);
        formData.append("is_salt", this.productData.is_salt);

        axios
          .post("products/", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          })
          .then((response) => {
            this.showSuccess();
            this.productData = {
              name: "",
              description: "",
              nic_content: [],
              flavors: [],
              brand: "",
              is_salt: false,
            };
            this.image = {
              src: null,
              type: null,
              name: null,
            };
          })
          .catch((error) => {
            console.log(error);
          });
      }, this.image.type);
    },

    uploadImage(event) {
      const { files } = event.target;
      if (files && files[0]) {
        if (this.image.src) {
          URL.revokeObjectURL(this.image.src);
        }
        const src = URL.createObjectURL(files[0]);
        this.image = {
          src: src,
          type: files[0].type,
          name: files[0].name,
        };
      }
    },

    cropImage() {
      const result = this.$refs.cropper.getResult();
      result.canvas.toBlob((blob) => {
        console.log(blob);
      }, this.image.type);
    },

    async getOptions() {
      await axios
        .get("product-options/")
        .then((response) => {
          this.options = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
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