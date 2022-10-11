<template>
  <div class="home">
    <div class="home-text">
      <h1>VapeRate</h1>
      <p>Отзывы о жидкостях для вейпа</p>
    </div>
  </div>
</template>

<style scoped>
.home {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("https://vaperate.ru/media/background.jpg");
  width: 100%;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  position: relative;
}
.home-text {
  text-align: center;
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
}
.home-text>h1 {
  font-size: 70px;
}
.home-text>p {
  font-size: 20px;
  font-weight: 400;
}
.section {
  margin: 0;
  padding: 0;
}
</style>

<script>

export default {
  name: 'HomeView',
  components: {
  }
}
</script>
