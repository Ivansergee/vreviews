<template>
  <div>
    <div class="columns">
      <div class="column is-6 is-offset-3">
        <h1 class="title is-4">Изменение изображения</h1>
          <div class="field">
            <label><span class="subtitle">Текущее изображение</span></label>
            <div class="control">
              <a :href="image" target="_blank">{{ image }}</a>
              {{type}}
            </div>
          </div>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label><span class="subtitle">Изображение</span></label>
            <div class="control" v-if="newImage.src">
              <cropper
                class="cropper"
                ref="cropper"
                :src="newImage.src"
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
              <span class="file-name">{{ newImage.name }}</span>
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
  props: ["image", "type"],
  emits: ["changed"],
  data() {
    return {
      isLoading: true,
      errors: [],
      newImage: {
        src: null,
        type: null,
        name: null,
        file: null,
        thumbnail: null,
      },
    };
  },
  methods: {
    change({ coordinates, canvas }) {
      canvas.toBlob((blob) => {
        this.newImage.thumbnail = blob
      }, this.newImage.type);
    },

    uploadImage(event) {
      const { files } = event.target;
      if (files && files[0]) {
        if (this.newImage.src) {
          URL.revokeObjectURL(this.newImage.src);
        }
        const src = URL.createObjectURL(files[0]);

        this.newImage.src = src;
        this.newImage.type = files[0].type;
        this.newImage.name = files[0].name;
        this.newImage.file = files[0];
      }
    },

    submitForm() {
      const formData = new FormData();

      if (this.newImage.file){
        formData.append("image", this.newImage.file);
      }
      if (this.newImage.thumbnail){
        formData.append("thumbnail", this.newImage.thumbnail, this.newImage.name);
      }

      axios
        .patch(`${this.type}s/${this.$route.params.brand_slug}/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(response => {
          this.showSuccess();
          this.$emit("changed");
          this.newImage = {
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