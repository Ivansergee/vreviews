<template>
    <div class="bookmarks" v-if="$store.state.username === $route.params.username">
      <p v-if="!bookmarks.length">Нет закладок</p>
      <p class="title is-5" v-else>Закладки {{ $route.params.username }}</p>
      <Bookmark
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        :id="bookmark.id"
        :name="bookmark.name"
        :description="bookmark.description"
        :image="bookmark.thumbnail_url"
        :slug="bookmark.slug"
        :brand_name="bookmark.brand.name"
        :brand_slug="bookmark.brand.slug"
        :nic_content="bookmark.nic_content"
        :avg_score="bookmark.avg_score"
        :flavors="bookmark.flavors"
        :reviews_amount="bookmark.reviews_count"
        :score_amount="bookmark.score_count"
        @deleted="deleteBookmark"
      />
      <a
        class="button is-success"
        @click="getNextBookmarks"
        v-if="nextBookmarks && bookmarksCount > 10"
        >Показать ещё</a>
    </div>
</template>
<script>
import axios from "axios";

import Bookmark from "../components/Bookmark.vue";


export default {
  components: {
    Bookmark
  },
  data() {
    return {
      bookmarks: [],
      bookmarksCount: null,
      nextBookmarks: null,
    };
  },
  mounted() {
    this.getBookmarks();
  },
  methods: {
    async getBookmarks() {
      if (this.$store.state.username === this.$route.params.username){
        this.$store.commit("setIsLoading", true);

        const username = this.$store.state.username;
        await axios
          .get(
            `/products/?bookmarks_author=${username}&ordering=-bookmarks__created_at`
          )
          .then((response) => {
            this.bookmarks.push(...response.data.results);
            this.nextBookmarks = response.data.next;
            this.bookmarksCount = response.data.count;
          })
          .catch((error) => {
            console.log(error);
          });

        this.$store.commit("setIsLoading", false);
      }
    },

    async getNextBookmarks() {
      await axios
        .get(this.nextBookmarks)
        .then((response) => {
          this.bookmarks.push(...response.data.results);
          this.nextBookmarks = response.data.next;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    deleteBookmark(id) {
      for (var i in this.bookmarks) {
        if (this.bookmarks[i].id == id) {
          this.bookmarks.splice(i, 1);
          this.bookmarksCount -= 1;
        }
      }
    },
  },
};
</script>