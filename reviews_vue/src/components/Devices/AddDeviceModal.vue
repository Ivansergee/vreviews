<template>
    <div class="modal" :class="{'is-active': showModal}">
      <div class="modal-background" @click="$emit('close'); deviceName = null"></div>
      <div class="modal-content">
        <div class="box">
          <div class="level">
            <div class="level-left">
              <p class="title is-4">Добавление устройства</p>
            </div>
            <div class="level-right">
              <button class="delete is-medium" aria-label="close" @click="$emit('close'); deviceName = null"></button>
            </div>
          </div>

            <div class="field">
              <div class="control">
                <input type="text" class="input" v-model="deviceName">
              </div>
            </div>

            <div class="level">
              <div class="level-left">
                <button class="button is-success"
                  @click="addDevice">Сохранить</button>
              </div>
            </div>

          </div>
        </div>
      </div>
</template>

<script>
import axios from 'axios';


export default {
  props: ['showModal'],
  emits: ['close', 'added'],
  data() {
    return {
      deviceName: null
    }
  },
  methods: {
    async addDevice() {
      await axios
        .post(`devices/`, { name: this.deviceName })
        .then((response) => {
          this.$store.commit('addDevice', response.data);
          this.deviceName = null;
          this.$emit('added');
        })
        .catch((error) => {
          console.log(error);
        });
    },
  }
};
</script>