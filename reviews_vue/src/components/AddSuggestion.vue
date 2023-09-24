<template>
  <div class="columns add-liquid">
    <div class="column is-6 is-offset-3">
      <h1 class="title is-4">Добавление отзыва</h1>

      <p>Если вы не нашли свою жидкость на сайте, вы все равно можете оценить её здесь. Наша администрация добавит её на
        сайт и опубликует вместе с вашей оценкой!</p>
      <br>

        <div class="field">
          <label><span class="subtitle">Название</span></label>
          <div class="control">
            <input type="text" class="input" :class="{ 'is-danger': errors.name }" v-model="suggestionData.name" />
          </div>
          <p class="help" v-if="!errors.name">Название жидкости с названием бренда</p>
          <p class="help is-danger" v-if="errors.name">{{ errors.name[0] }}</p>
        </div>

        <div class="field">
          <label><span class="subtitle">Тип никотина</span></label>
          <div class="control">
            <label class="radio">
              <input type="radio" name="nictype" value="salt" v-model="suggestionData.nicType">
              Солевой
            </label>
            <label class="radio">
              <input type="radio" name="nictype" value="classic" v-model="suggestionData.nicType">
              Классический
            </label>
          </div>
          <p class="help is-danger" v-if="errors.nicType">{{ errors.nicType[0] }}</p>
        </div>

        <div class="field">
          <label><span class="subtitle">Оценка</span></label>
          <div class="tags has-addons" @mouseleave="hover_score = suggestionData.score"
            @click="suggestionData.score = hover_score">
            <a class="tag" v-for="i in 10" :key="i" @mouseover="hover_score = i">
              <i class="bi" :class="[hover_score >= i ? 'bi-star-fill' : 'bi-star']"></i>
            </a>
            <span class="tag is-primary">{{ hover_score }}</span>
          </div>
          <p class="help is-danger" v-if="errors.score">{{ errors.score[0] }}</p>
        </div>

        <div class="field">
          <label><span class="subtitle">Отзыв</span></label>
          <div class="control">
            <textarea class="textarea" cols="100" rows="5" v-model="suggestionData.review">
              </textarea>
          </div>
          <p class="help">Ваш отзыв (не обязательно)</p>
        </div>

        <div class="field">
            <p class="subtitle mb-2">Устройства</p>
            <p class="mb-2" v-if="!devices">Вы ещё не добавили ни одного устройства</p>
            <div class="control select is-multiple" v-if="devices">
              <select multiple size="3" v-model="suggestionData.selectedDevices">
                <option v-for="device in devices" :key="device.id" :value="device.id">{{ device.name }}</option>
              </select>
            </div>
            <p class="subtitle mt-2">
              <button class="button is-success is-small" @click="showCreateModal = true">
                <span>Добавить уcтройство</span>
              </button>
            </p>
            <p class="help" v-if="devices">Выберите устройства, на которых вы использовали жидкость. Удерживайте Ctrl для выбора нескольких.</p>
          </div>


        <div class="field">
          <label><span class="subtitle">Комментарий</span></label>
          <div class="control">
            <textarea class="textarea" cols="100" rows="5" v-model="suggestionData.comment">
              </textarea>
          </div>
          <p class="help">Комментарий для модератора (ссылка на жидкость итд). Этот текст не будет опубликован.</p>
        </div>

        <div class="field mt-4">
          <div class="control">
            <button
              class="button is-dark"
              :class="{'is-loading': btnLoading}"
              @click="submitForm">Отправить</button>
          </div>
        </div>
    </div>
    <AddDeviceModal
      :showModal="showCreateModal"
      @close="showCreateModal = false"
      @added="showCreateModal = false"
    />
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


<script>
import axios from "axios";
import { toast } from "bulma-toast";

import AddDeviceModal from './Devices/AddDeviceModal.vue';

export default {
  components: {
    AddDeviceModal
  },
  data() {
    return {
      btnLoading: false,
      errors: {},
      hover_score: 0,
      showCreateModal: false,
      suggestionData: {
        name: "",
        nicType: "",
        review: "",
        selectedDevices: [],
        comment: "",
        score: 0
      },
    };
  },
  computed: {
    devices() {
      return this.$store.state.devices;
    },
  },
  methods: {

    async submitForm() {
      if (!this.$store.state.isAuthenticated) {
        toast({
          message: "Для отправки формы необходимо выполнить вход в свой аккаунт!",
          type: "is-danger",
          dismissible: true,
          duration: 10000,
          pauseOnHover: true,
          position: "top-center",
        });
        return
      }

      this.errors = {};

      if (!this.suggestionData.name) {
        this.errors.name = ['Это поле обязательно'];
      }

      if (!this.suggestionData.nicType) {
        this.errors.nicType = ['Выберите тип никотина'];
      }

      if (Object.keys(this.errors).length !== 0) {
        toast({
          message: "Есть ошибки",
          type: "is-danger",
          dismissible: true,
          duration: 10000,
          pauseOnHover: true,
          position: "top-center",
        });
        return
      }

      const formData = new FormData();

      formData.append("name", this.suggestionData.name);
      formData.append("nic_type", this.suggestionData.nicType);
      formData.append("text", this.suggestionData.review);
      formData.append("score", this.suggestionData.score);
      formData.append("comment", this.suggestionData.comment);
      for (var i of this.suggestionData.selectedDevices) {
        formData.append("device_id", i );
      }

      this.btnLoading = true;
      await axios
        .post("suggestions/", formData)
        .then(() => {
          this.showSuccess();
          this.suggestionData = {
            name: "",
            nicType: "",
            selectedDevices: [],
            review: "",
            comment: "",
            score: 0
          };
        })
        .catch((error) => {
          this.errors = error.response.data;
        });
      this.btnLoading = false;
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