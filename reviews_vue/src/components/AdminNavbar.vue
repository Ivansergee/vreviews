<template>
    <nav class="navbar">
      <div class="navbar-start">
          <router-link class="navbar-item" :to="{ name: 'admin-suggestions' }"
            >Предложенные отзывы</router-link>
          <router-link class="navbar-item" :to="{ name: 'admin-liquids' }"
            >Жидкости</router-link>
          <router-link class="navbar-item" :to="{ name: 'contacts' }"
            >Бренды</router-link>
            <router-link class="navbar-item" :to="{ name: 'contacts' }"
            >Производители</router-link>
        </div>
    </nav>
</template>