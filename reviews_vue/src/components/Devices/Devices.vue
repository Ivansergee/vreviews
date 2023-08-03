<template>
  <div>
    <div class="level is-mobile">
      <div class="level-left">
        <div class="level-item">
          <p class="title is-4" v-if="$store.state.username === $route.params.username">Мои устройства</p>
          <p class="title is-4" v-else>Устройства {{ $route.params.username }}</p>
        </div>
        <div class="level-item" v-if="$store.state.username === $route.params.username">
          <button class="button is-success" @click="showCreateModal = true">
            <span class="icon">
              <i class="fa-solid fa-plus"></i>
            </span>
            <span>Добавить</span>
          </button>
        </div>
      </div>
    </div>

    <div v-for="device in devices" :key="device.id">
      <Device
        :device="device"
        @showEdit="showEdit"
        @showDelete="showDelete"
      />
    </div>
    
    <AddDeviceModal
      :showModal="showCreateModal"
      @close="showCreateModal = false"
      @added="getUserInfo(); showCreateModal = false"
    />
    <EditDeviceModal 
      :showModal="showEditModal"
      :name="deviceName"
      :id="deviceId"
      @close="showEditModal = false"
      @edited="getUserInfo(); showEditModal = false"
    />
    <DeleteDeviceModal
      :showModal="showDeleteModal"
      :name="deviceName"
      :deviceId="deviceId"
      @close="showDeleteModal = false"
      @deleted="getUserInfo(); showDeleteModal = false"
    />

    </div>
</template>

<style scoped></style>

<script>
import Device from './Device.vue';
import AddDeviceModal from './AddDeviceModal.vue';
import EditDeviceModal from './EditDeviceModal.vue';
import DeleteDeviceModal from './DeleteDeviceModal.vue';

export default {
  components: {
    Device,
    AddDeviceModal,
    EditDeviceModal,
    DeleteDeviceModal
  },
  props: ['devices', 'getUserInfo'],
  data() {
    return {
      showCreateModal: false,
      showEditModal: false,
      showDeleteModal: false,
      deviceName: null,
      deviceId: null
    }
  },
  methods: {
    showEdit(id, name) {
      this.showEditModal = true;
      this.deviceName = name;
      this.deviceId = id;
    },
    showDelete(id, name) {
      this.showDeleteModal = true;
      this.deviceName = name;
      this.deviceId = id;
    }
  }
};
</script>