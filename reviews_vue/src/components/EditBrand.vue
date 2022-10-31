<template>

  <div class="columns add-brand" v-if="!isLoading">
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

        <div class="field" v-if="options.producers">
          <label><span class="subtitle">Производитель</span></label>
          <div class="control">
            <VueMultiselect
              v-model="brandData.producer"
              :options="options.producers"
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

        <div class="field" v-if="options.nic_content">
          <label><span class="subtitle">Содержание никотина</span></label>
          <div class="control" v-for="amount in options.nic_content" :key="amount.id">
            <label class="checkbox">
              <input type="checkbox" @click="addNic(amount.id)" :checked="brandData.nic_content.includes(amount.id)"/>
              {{ amount.amount }} мг
            </label>
          </div>
        </div>

        <div class="field" v-if="options.volumes">
          <label><span class="subtitle">Объем</span></label>
          <div class="control" v-for="vol in options.volumes" :key="vol.id">
            <label class="checkbox">
              <input type="checkbox" @click="addVol(vol.id)" :checked="brandData.volumes.includes(vol.id)"/>
              {{ vol.volume }} мл
            </label>
          </div>
        </div>

        <div class="field">
          <label><span class="subtitle">Солевой никотин</span></label>
          <div class="control">
            <label class="checkbox">
              <input type="checkbox" v-model="brandData.is_salt" />
              Да
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
    "producer",
    "name",
    "description",
    "nic_content",
    "volumes",
    "is_salt",
  ],
  emits: ["added"],
  data() {
    return {
      isLoading: true,
      errors: [],
      options: null,
      brandData: {
        name: null,
        description: null,
        producer: null,
        is_salt: null,
        nic_content: [],
        volumes: [],
      },
    };
  },
  mounted() {
    this.getOptions();
    this.brandData.producer = this.producer;
    this.brandData.name = this.name;
    this.brandData.description = this.description;
    if (this.nic_content) {
      this.nic_content.forEach((element) => {this.addNic(element.id)});
    }
    if (this.volumes) {
      this.volumes.forEach((element) => {this.addVol(element.id)});
    }
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
      if (this.brandData.nic_content){
        for (var i of this.brandData.volumes) {
          formData.append("nic_content_id", i);
        }
      }
      if (this.brandData.volumes){
        for (var i of this.brandData.volumes) {
          formData.append("volume_id", i);
        }
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
            is_salt: null,
            nic_content: [],
            volumes: [],
          };
        })
        .catch((error) => {
          console.log(error);
        });
    },

    addNic(id){
      if (this.brandData.nic_content.includes(id)){
        var i = this.brandData.nic_content.indexOf(id);
        this.brandData.nic_content.splice(i, 1);
      } else {
        this.brandData.nic_content.push(id)
      }
    },

    addVol(id){
      if (this.brandData.volumes.includes(id)){
        var i = this.brandData.volumes.indexOf(id);
        this.brandData.volumes.splice(i, 1);
      } else {
        this.brandData.volumes.push(id)
      }
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