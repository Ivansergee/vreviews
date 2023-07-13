<template>
    <nav class="navbar">
      <div class="navbar-start">
          <router-link class="navbar-item" :to="{ name: 'profile', params: { username: $route.params.username } }"
            >Профиль</router-link>
          <router-link class="navbar-item" :to="{ name: 'profile-reviews' }"
            >Отзывы и оценки</router-link>
          <router-link class="navbar-item" :to="{ name: 'profile-bookmarks' }" v-if="$store.state.isAuthenticated && $store.state.username === $route.params.username"
            >Закладки</router-link>
        </div>
    </nav>
</template>