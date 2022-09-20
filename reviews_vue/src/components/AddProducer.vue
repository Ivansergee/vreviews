<template>

  <div class="columns add-producer">
    <div class="column is-6 is-offset-3">
      <h1 class="title is-4">Добавление нового производителя</h1>
      <form @submit.prevent="submitForm">

        <div class="field">
          <label><span class="subtitle">Название</span></label>
          <div class="control">
            <input type="text" class="input" v-model="producerData.name" />
          </div>
          <p class="help">Название производителя</p>
        </div>

        <div class="field" v-if="countries">
          <label><span class="subtitle">Страна</span></label>
          <div class="control">
            <VueMultiselect
              v-model="producerData.country"
              :options="countries"
              :multiple="false"
              selectLabel="Выбрать"
              selectedLabel="Выбрано"
              deselectLabel="Удалить"
              placeholder="Выберите страну"
              label="name"
              track-by="id"
            />
          </div>
          <p class="help">Выберите страну. Для поиска начните набирать название</p>
        </div>

        <div class="field">
          <label><span class="subtitle">Описание</span></label>
          <div class="control">
            <textarea
              class="textarea"
              cols="100"
              rows="5"
              v-model="producerData.description"
            >
            </textarea>
          </div>
          <p class="help">О производителе</p>
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
              @change="change"
            />
          </div>
          <p class="help">Добавьте лого производителя и выберите участок, который будет использован для превью. Для зума используйте колесико мыши или стандартный жест на смартфоне.</p>
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
  props: ['countries'],
  emits: ["added"],
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
      producerData: {
        name: "",
        description: "",
        country: "",
      },
    };
  },
  methods: {
    change({ coordinates, canvas }) {
      canvas.toBlob((blob) => {
        this.image.thumbnail = blob
      }, this.image.type);
    },
    submitForm() {
      const formData = new FormData();

      if (this.image.file){
        formData.append("image", this.image.file);
      }
      if (this.image.thumbnail){
        formData.append("thumbnail", this.image.thumbnail, this.image.name);
      }
      formData.append("name", this.producerData.name);
      formData.append("description", this.producerData.description);
      formData.append("country_id", this.producerData.country.id);

      axios
        .post("producers/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(() => {
          this.$emit("added");
          this.showSuccess();
          this.producerData = {
            name: "",
            description: "",
            country: "",
          };
          this.image = {
            src: null,
            type: null,
            name: null,
            file: null,
            thumbnail: null,
          };
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
        message: "Производитель добавлен!",
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