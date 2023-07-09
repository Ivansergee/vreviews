<template>
    <div>
        <div class="level is-mobile">
            <div class="level-left">
                <div class="level-item">
                <p class="title is-4">Мои устройства</p>
                </div>
                <div class="level-item">
                <button class="button is-success" @click="addDevice">
                    <span class="icon">
                    <i class="fa-solid fa-plus"></i>
                    </span>
                    <span>Добавить</span>
                </button>
                </div>
            </div>
        </div>

        <div v-for="device in devices" :key="device.id">
            <Device :device="device" />
        </div>
    </div>
</template>

<style scoped>
</style>

<script>
import Device from '../components/Device.vue'

export default {
  components: {
    Device
  },
  props: ['devices'],
  methods: {
    async addDevice() {
        await axios
          .post(`devices/`, { like: reaction })
          .then(() => {
            this.$emit("rated", { id: this.id, like: reaction });
          })
          .catch((error) => {
            console.log(error);
          });
    }
  }
};
</script>