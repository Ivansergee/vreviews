<template>
    <div class="columns add-liquid">
        <div class="column is-6 is-offset-3">
            <h1 class="title is-4">Добавление отзыва</h1>
            <p>Если вы не нашли свою жидкость на сайте, то все равно можете оставить свою оценку. 
                Наши модераторы добавят жидкость на сайт сразу с вашим отзывом!</p>
            <br>
            <form @submit.prevent="submitForm">

                <div class="field">
                    <label><span class="subtitle">Название</span></label>
                    <div class="control">
                        <input type="text" class="input" v-model="name" />
                    </div>
                    <p class="help">Название жидкости с названием бренда</p>
                </div>

                <div class="field">
                    <label><span class="subtitle">Ваша оценка</span></label>
                    <div class="tags has-addons" @mouseleave="score = user_score" @click="setScore">
                        <a class="tag" v-for="i in 10" :key="i" @mouseover="score = i">
                            <i class="bi" :class="[score >= i ? 'bi-star-fill' : 'bi-star']"></i>
                        </a>
                        <span class="tag is-primary">{{ score }}</span>
                    </div>
                </div>

                <div class="field">
                    <label><span class="subtitle">Ваш отзыв</span></label>
                    <div class="control">
                        <textarea class="textarea" cols="100" rows="5" v-model="review"></textarea>
                    </div>
                    <p class="help">Ваши впечатления от жидкости (не обязательно)</p>
                </div>
                
                <div class="field">
                    <label><span class="subtitle">Комментарий</span></label>
                    <div class="control">
                        <textarea class="textarea" cols="100" rows="5" v-model="comment"></textarea>
                    </div>
                    <p class="help">Дополнительная информация для модератора (ссылка на жидкость и т. п.)</p>
                </div>


                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" :key="error">{{ error }}</p>
                </div>

                <div class="field mt-4">
                    <div class="control">
                        <button class="button is-dark">Отправить</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
</style>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
  data() {
    return {
      errors: [],
      name: "",
      review: null,
      score: 0,
      user_score: 0,
      comment: ""
    };
  },
  methods: {

    submitForm() {
      const formData = new FormData();
      
      formData.append("name", this.name);
      formData.append("comment", this.comment);
      formData.append("score", this.user_score);
      formData.append("text", this.review);

      axios
        .post("suggestions/", formData)
        .then(() => {
            this.showSuccess
        })
        .catch((error) => {
          console.log(error);
        });
    },

    setScore() {
      this.user_score = this.score;
    },

    showSuccess() {
      toast({
        message: "Спасибо! Информация отправлена на проверку и скоро будет опубликована на сайте.",
        type: "is-success",
        dismissible: true,
        duration: 10000,
        pauseOnHover: true,
        position: "top-center",
      });
    },
  },
};
</script>