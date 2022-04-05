<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link class="navbar-item" to="/"><strong>VReviews</strong></router-link>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>  
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" :class="{ 'is-active': showMobileMenu }">
        <div class="navbar-start">
          <router-link class="navbar-item" :to="{name: 'liquids-list'}">Жидкости</router-link>
          <router-link class="navbar-item" to="/">Одноразки</router-link>
        </div>
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <router-link class="button is-blue" to="/">Вход</router-link>
              <router-link class="button is-success" to="/">Регистрация</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <section class="section">
      <router-view/>
    </section>
    
    <footer class="footer">
      <p class="has-text-centered">
        VReviews 2022
      </p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showMobileMenu: false,
    }
  },
}
</script>


<style lang="scss">
  @import '../node_modules/bulma';
  @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css");


</style>
