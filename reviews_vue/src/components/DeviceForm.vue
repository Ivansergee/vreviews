<template>
  <div class="modal is-active">
    <div class="modal-background" @click="$emit('close')"></div>
    <div class="modal-content">
      <div class="box">
            <div class="level">
                <div class="level-left">
                    <h1 class="title">Добавление устройства</h1>
                </div>
                <div class="level-right">
                    <button class="delete is-medium" aria-label="close" @click="$emit('close')"></button>
                </div>
            </div>

            <div>
                <div class="field">
                    <label>Название</label>
                    <div class="control">
                        <input type="text" class="input" v-model="city">
                    </div>
                </div>

                
                <div class="level">
                    <div class="level-left">
                        <button
                            class="button is-dark"
                            :class="{ 'is-loading': isLoading }"
                            @click="submitForm()"
                        >Сохранить</button>
                    </div>
                </div>
            </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
</style>

<script>
import axios from "axios";

export default {
  props: [
    
  ],
  emits: ["changedDevice", "addDevice", "close"],
  data() {
    return {
      errors: {},
      isLoading: false,
    };
  },
  methods: {
    async submitForm() {

      }
    },
};
</script>
