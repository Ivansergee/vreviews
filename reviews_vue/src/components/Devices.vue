<template>
  <div>
    <div class="level is-mobile">
      <div class="level-left">
        <div class="level-item">
          <p class="title is-4" v-if="$store.state.username === $route.params.username">Мои устройства</p>
          <p class="title is-4" v-else>Устройства {{ $route.params.username }}</p>
        </div>
        <div class="level-item" v-if="$store.state.username === $route.params.username">
          <button class="button is-success" @click="modalType = 'create'; showModal = true">
            <span class="icon">
              <i class="fa-solid fa-plus"></i>
            </span>
            <span>Добавить</span>
          </button>
        </div>
      </div>
    </div>

    <div v-for="device in devices" :key="device.id">
      <Device :device="device" :openModal="openModal" />
    </div>

    <div class="modal" :class="{'is-active': showModal && modalType}">
      <div class="modal-background" @click="showModal = false; deviceName = null"></div>
      <div class="modal-content">
        <div class="box">
          <div class="level">
            <div class="level-left">
              <p class="title is-4" v-if="modalType==='edit'">Изменение устройства</p>
              <p class="title is-4" v-if="modalType==='delete'">Удаление устройства</p>
              <p class="title is-4" v-if="modalType==='create'">Добавление устройства</p>
            </div>
            <div class="level-right">
              <button class="delete is-medium" aria-label="close" @click="showModal = false; deviceName = null"></button>
            </div>
          </div>

            <div class="field" v-if="modalType==='edit' || modalType==='create'">
              <div class="control">
                <input type="text" class="input" v-model="deviceName">
              </div>
            </div>

            <div class="field" v-if="modalType==='delete'">
              <p>Удалить устройство {{ deviceName }}?</p>
              <p>Оно также будет удалено из всех ваших отзывов!</p>
            </div>

            <div class="level" v-if="modalType==='edit'">
              <div class="level-left">
                <button class="button is-dark"
                  @click="editDevice">Сохранить</button>
              </div>
            </div>

            <div class="level" v-if="modalType==='delete'">
              <div class="level-left">
                <button class="button is-danger"
                  @click="deleteDevice">Удалить</button>
              </div>
            </div>

            <div class="level" v-if="modalType==='create'">
              <div class="level-left">
                <button class="button is-success"
                  @click="addDevice">Сохранить</button>
              </div>
            </div>

          </div>
        </div>
      </div>


    </div>
</template>

<style scoped></style>

<script>
import axios from 'axios';
import Device from '../components/Device.vue'

export default {
  components: {
    Device
  },
  props: ['devices', 'getUserInfo'],
  data() {
    return {
      showModal: false,
      modalType: null,
      deviceName: null,
      deviceId: null
    }
  },
  methods: {
    async addDevice() {
      await axios
        .post(`devices/`, { name: this.deviceName })
        .then((response) => {
          this.getUserInfo();
          this.$store.commit('addDevice', response.data);
          this.deviceName = null;
          this.showModal = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async editDevice() {
      await axios
        .patch(`devices/${this.deviceId}/`, { name: this.deviceName })
        .then((response) => {
          this.getUserInfo();
          this.$store.commit('editDevice', response.data);
          this.deviceName = null;
          this.showModal = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async deleteDevice() {
      await axios
        .delete(`devices/${this.deviceId}/`)
        .then(() => {
          this.getUserInfo();
          this.$store.commit('removeDevice', this.deviceId);
          this.deviceName = null;
          this.showModal = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    openModal(operation, id, name) {
      this.modalType = operation;
      this.deviceName = name;
      this.deviceId = id;
      this.showModal = true;
    },
  }
};
</script>