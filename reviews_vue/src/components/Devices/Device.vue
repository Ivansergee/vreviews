<template>
    <div class="box m-3 py-2">
        <div class="level is-mobile">
            <div class="level-left">
                <div class="level-item">
                    <p>{{ device.name }}</p>
                </div>
            </div>
            <div class="level-right" v-if="$store.state.username === $route.params.username"> 
                <div class="level-item">
                    <button
                        class="button is-info is-small mr-3"
                        @click="$emit('showEdit', device.id, device.name)"
                    >
                        <i class="fa-solid fa-pen"></i>
                    </button>
                    <button
                        class="button is-danger is-small"
                        @click="$emit('showDelete', device.id, device.name)"
                    >
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>

<script>
export default {
    props: ['device', 'openModal'],
    emits: ['showEdit', 'showDelete']
};
</script>