<template>
    <nav class="navbar">
      <div class="navbar-start">
          <router-link class="navbar-item" :to="{ name: 'liquids-list' }"
            ><strong>Добавить отзыв</strong></router-link>
          <router-link class="navbar-item" :to="{ name: 'liquids-list' }"
            >Добавить жидкость</router-link>
          <router-link class="navbar-item" :to="{ name: 'brands-list' }"
            >Добавить бренд</router-link>
          <router-link class="navbar-item" :to="{ name: 'contacts' }"
            >Добавить производителя</router-link>
        </div>
    </nav>
</template>