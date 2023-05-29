<template>
    <nav class="navbar">
      <div class="navbar-start">
          <router-link class="navbar-item" :to="{ name: 'liquids-list' }"
            >Жидкости</router-link>
          <router-link class="navbar-item" :to="{ name: 'brands-list' }"
            >Бренды</router-link>
          <router-link class="navbar-item" :to="{ name: 'contacts' }"
            >Контакты</router-link>
        </div>
    </nav>
</template>