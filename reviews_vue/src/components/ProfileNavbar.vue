<template>
    <nav class="navbar">
      <div class="navbar-start">
          <router-link class="navbar-item" :to="{ name: 'profile', params: { username: $store.state.username } }"
            >Профиль</router-link>
          <router-link class="navbar-item" :to="{ name: 'profile-reviews' }"
            >Отзывы и оценки</router-link>
          <router-link class="navbar-item" :to="{ name: 'profile-bookmarks' }"
            >Закладки</router-link>
        </div>
    </nav>
</template>