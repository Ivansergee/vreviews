<template>
    <nav class="navbar">
      <div class="navbar-start">
          <router-link class="navbar-item" :to="{ name: 'liquids-list' }"
            >Профиль</router-link>
          <router-link class="navbar-item" :to="{ name: 'brands-list' }"
            >Отзывы и оценки</router-link>
          <router-link class="navbar-item" :to="{ name: 'contacts' }"
            >Закладки</router-link>
        </div>
    </nav>
</template>