<template>

  <div class="columns add-brand">
    <div class="column is-6 is-offset-3">
      <h1 class="title is-4">Добавление нового бренда</h1>
      <form @submit.prevent="submitForm">

        <div class="field">
          <label><span class="subtitle">Название</span></label>
          <div class="control">
            <input type="text" class="input" v-model="brandData.name" />
          </div>
          <p class="help">Название бренда. Добавляйте к названию "Salt", если у производителя есть аналогичная линейка вкусов на классическом никотине.</p>
        </div>

        <div class="field" v-if="producers">
          <label><span class="subtitle">Производитель</span></label>
          <div class="control">
            <VueMultiselect
              v-model="brandData.producer"
              :options="producers"
              :multiple="false"
              selectLabel="Выбрать"
              selectedLabel="Выбрано"
              deselectLabel="Удалить"
              placeholder="Выберите производителя"
              label="name"
              track-by="id"
            />
          </div>
          <p class="help">Выберите компанию производителя. Для поиска начните набирать название</p>
        </div>

        <div class="field">
          <label><span class="subtitle">Описание</span></label>
          <div class="control">
            <textarea
              class="textarea"
              cols="100"
              rows="5"
              v-model="brandData.description"
            >
            </textarea>
          </div>
          <p class="help">О бренде</p>
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
          <p class="help">Добавьте лого бренда и выберите участок, который будет использован для превью. Для зума используйте колесико мыши или стандартный жест на смартфоне.</p>
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
  props: [
    "producers"
  ],
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
      brandData: {
        name: "",
        description: "",
        producer: "",
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
      formData.append("name", this.brandData.name);
      formData.append("description", this.brandData.description);
      formData.append("producer_id", this.brandData.producer.id);

      axios
        .post("brands/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(() => {
          this.showSuccess();
          this.$emit("added");
          this.brandtData = {
            name: "",
            description: "",
            producer: "",
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
        message: "Бренд успешно создан!",
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