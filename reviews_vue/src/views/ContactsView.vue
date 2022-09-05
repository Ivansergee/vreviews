<template>
  <div>
    <p class='title'>Контакты</p>
  </div>
</template>

<script>


export default {
  mounted() {
    this.activate();
  },
  methods:{
    async activate() {
        const data = {
          uid: this.$route.params.uid,
          token: this.$route.params.token,
        };

        await axios
        .post('users/activation/', data)
        .then(() => {
          toast({
            message: "Email подтвержден! Теперь вы можете войти на сайт.",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 10000,
            position: "top-center",
          });
          this.$router.replace('/');
        })
        .catch(error => {
          toast({
            message: "Что-то пошло не так!",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 10000,
            position: "top-center",
          });
          this.$router.replace('/');
          console.log(error.response.data);
        })
    },
  },
}
</script>