<template>
    <div class="add-product">
        <div class="columns">
            <div class="column is-6 is-offset-3">
                <h1 class="title">Добавление жидкости</h1>
                <form @submit.prevent="submitForm">

                    <div class="field">
                        <label><span class="subtitle">Название</span></label>
                        <div class="control">
                            <input type="text" class="input" v-model="productData.name">
                        </div>
                    </div>

                    <div class="field">
                        <label><span class="subtitle">Бренд</span></label>
                        <br>
                        <div class="select">
                            <select v-model="productData.brand">
                                <option v-for="brand in brands" :key="brand.id" :value="brand.id" >{{ brand.name }}</option>
                            </select>
                        </div>
                    </div>

                    <div class="field">
                        <label><span class="subtitle">Вкусы</span></label>
                        <br>
                        <div class="select is-multiple">
                            <select multiple size="8" v-model="productData.flavors">
                                <option v-for="flavor in flavors" :key="flavor.id" :value="flavor.id" >{{ flavor.name }}</option>
                            </select>
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
                                    height: 300
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
                            <span class="file-label">
                                Выберите файл
                            </span>
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
    background: #DDD;
}
.cropper:hover {
    cursor: move;
}
</style>

<script>
import axios from 'axios'
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'


export default {
  components: {
    Cropper,
  },
  data() {
    return {
      brands: [],
      flavors: [],
      nic_content: [],
      image: {
        src: null,
        type: null,
        name: null
      },
      errors: [],
      productData: {
          name: '',
          description: '',
          nic_content: [],
          flavors: [],
          brand: '',
      },
    }
  },
  mounted() {
    this.getFlavors()
    this.getBrands()
  },
  methods: {
      submitForm() {
        const formData = new FormData()

        const result = this.$refs.cropper.getResult()
        result.canvas.toBlob((blob) => {
            formData.append('thumbnail', blob, this.image.name)
            formData.append('image', this.image.src)
            formData.append('name', this.productData.name)
            formData.append('description', this.productData.description)
            formData.append('nic_content', this.productData.nic_content)
            formData.append('flavors', this.productData.flavors)
            formData.append('brand', this.productData.brand)

            axios
            .post('add-product/', formData, {headers:{'Content-Type': 'multipart/form-data'}})
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                console.log(error)
            })

            // for(var pair of formData.entries()) {
            // console.log(pair[0]+ ': '+ pair[1])
            // }

            }, this.image.type)
        

        // for(var pair of formData.entries()) {
        //     console.log(pair[0]+ ': '+ pair[1])
        // }

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
            name: files[0].name
            };
        }
      },

      cropImage() {
        const result = this.$refs.cropper.getResult()
        result.canvas.toBlob((blob) => {console.log(blob)}, this.image.type)
      },

      async getFlavors() {
          await axios
          .get('flavors/')
          .then(response => {
              this.flavors = response.data
          })
          .catch(error => {
                console.log(error)
          })
      },
      async getBrands() {
          await axios
          .get('brands/')
          .then(response => {
              this.brands = response.data
          })
          .catch(error => {
                console.log(error)
          })
      },
  },
}
</script>