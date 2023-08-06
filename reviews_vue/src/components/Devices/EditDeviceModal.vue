<template>
    <div class="modal" :class="{'is-active': showModal}">
      <div class="modal-background" @click="$emit('close')"></div>
      <div class="modal-content">
        <div class="box">
          <div class="level">
            <div class="level-left">
              <p class="title is-4">Изменение устройства</p>
            </div>
            <div class="level-right">
              <button class="delete is-medium" aria-label="close" @click="$emit('close')"></button>
            </div>
          </div>
            <div class="field" v-if="deviceName">
              <div class="control">
                <input type="text" class="input" v-model="deviceName">
              </div>
            </div>

            <div class="level">
              <div class="level-left">
                <button class="button is-dark"
                  @click="editDevice">Сохранить</button>
              </div>
            </div>
          </div>
        </div>
      </div>
</template>

<style scoped></style>

<script>
import axios from 'axios';

export default {
  props: ['showModal', 'id', 'name'],
  emits: ['close', 'edited'],
  data() {
    return {
      deviceName: this.name
    }
  },
  methods: {
    async editDevice() {
      await axios
        .patch(`devices/${this.id}/`, { name: this.deviceName })
        .then((response) => {
          this.$store.commit('editDevice', response.data);
          this.deviceName = null;
          this.$emit('edited');
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }
};
</script>