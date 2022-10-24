<template>

  <div class="columns add-brand">
    <div class="column is-6 is-offset-3">
      <h1 class="title is-4">Редактирование бренда</h1>
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

        <div class="field" v-if="options">
          <label><span class="subtitle">Содержание никотина</span></label>
          <br />
          <div class="select is-multiple">
            <select multiple size="5" v-model="brandData.nic_content">
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

        <div class="field" v-if="options">
          <label><span class="subtitle">Объем</span></label>
          <br />
          <div class="select is-multiple">
            <select multiple size="5" v-model="brandData.volumes">
              <option
                v-for="vol in options.volumes"
                :key="vol.id"
                :value="vol.id"
              >
                {{ vol.volume }} мл
              </option>
            </select>
          </div>
        </div>

        <div class="field">
          <div class="control">
            <label class="checkbox">
              <input type="checkbox" v-model="brandData.is_salt" />
              Солевой никотин
            </label>
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
import VueMultiselect from 'vue-multiselect';
import { toast } from "bulma-toast";

export default {
  components: {
    VueMultiselect,
  },
  props: [
    "producers",
    "producer",
    "name",
    "description",
    "nic_content",
    "volume",
    "is_salt",
  ],
  emits: ["added"],
  data() {
    return {
      errors: [],
      options: null,
      brandData: {
        name: null,
        description: null,
        producer: null,
        is_salt: null,
        nic_content: null,
        volumes: null,
      },
    };
  },
  mounted() {
    this.brandData.producer = this.producer;
    this.brandData.name = this.name;
    this.brandData.description = this.description;
    this.brandData.nic_content = this.nic_content;
    this.brandData.volumes = this.volume;
    this.getOptions();
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

      if (this.brandData.name){
        formData.append("name", this.brandData.name);
      }
      if (this.brandData.description){
        formData.append("description", this.brandData.description);
      }
      if (this.brandData.producer){
        formData.append("producer_id", this.brandData.producer.id);
      }

      axios
        .patch(`brands/${this.$route.params.brand_slug}/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(response => {
          this.showSuccess();
          this.$emit("added", response.data.slug);
          this.brandData = {
            name: null,
            description: null,
            producer: null,
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