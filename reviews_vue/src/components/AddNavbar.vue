<template>
    <nav class="navbar">
      <div class="navbar-start">
          <a class="navbar-item" @click="setActiveTab('suggestion')"
            ><strong>Добавить отзыв</strong></a>
          <a class="navbar-item" @click="setActiveTab('liquid')"
            >Добавить жидкость</a>
          <a class="navbar-item" @click="setActiveTab('brand')"
            >Добавить бренд</a>
          <a class="navbar-item" @click="setActiveTab('producer')"
            >Добавить производителя</a>
        </div>
    </nav>
</template>
<script>
export default {
  methods: {
    setActiveTab(tab){
      this.$router.replace({ name: 'add', params: { type: tab } });
    }
  },
};
</script>