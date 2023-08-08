<template>
    <div class="modal" :class="{'is-active': showModal}">
      <div class="modal-background" @click="$emit('close')"></div>
      <div class="modal-content">
        <div class="box">
          <div class="level is-mobile">
            <div class="level-left">
              <p class="title is-4">Удаление устройства</p>
            </div>
            <div class="level-right">
              <button class="delete is-medium" aria-label="close" @click="$emit('close')"></button>
            </div>
          </div>

            <div class="field">
              <p>Удалить устройство {{ deviceName }}?</p>
              <p>Оно также будет удалено из всех ваших отзывов!</p>
            </div>

            <div class="level">
              <div class="level-left">
                <button class="button is-danger"
                  @click="deleteDevice">Удалить</button>
              </div>
            </div>

          </div>
        </div>
      </div>
</template>

<script>
import axios from 'axios';


export default {
  props: ['showModal', 'id', 'name'],
  emits: ['close', 'deleted'],
  data() {
    return {
      deviceName: this.name
    }
  },
  methods: {
    async deleteDevice() {
      await axios
        .delete(`devices/${this.id}/`)
        .then(() => {
          this.$store.commit('removeDevice', this.id);
          this.deviceName = null;
          this.$emit('deleted');
        })
        .catch((error) => {
          console.log(error);
        });
    },
  }
};
</script>