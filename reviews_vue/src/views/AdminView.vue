<template>
    <div class="container">
      <router-view></router-view>
    </div>
</template>
<script>
export default {
  name: 'Dashboard',
  created() {
    if (!this.$store.state.isAdmin) {
      this.$router.push('/')
    }
  },
}
</script>

