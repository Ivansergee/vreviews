<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Вход</h1>
                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Имя пользователя</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Пароль</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Войти</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'Log In',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    methods: {
        async submitForm() {
            this.errors = []

            if (this.username === ''){
                this.errors.push('Заполните имя пользователя')
            }

            if (this.password === ''){
                this.errors.push('Введите пароль')
            }

            if (!this.errors.length){
                const formData = {
                    username: this.username,
                    password: this.password,
                }

                await axios
                .post('token/login/', formData)
                .then(response => {
                    const token = this.response.data.auth_token

                    this.$store.commit('setToken', token)

                    axios.defaults.headers.common['Authorization'] = 'Token ' + token

                    localStorage.setItem('token', token)

                    const toPath = this.$route.query.to || '/'

                    this.$router.push(toPath)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        this.errors.push('Что-то пошло не так. Попробуйте ещё раз.')
                            
                        console.log(error.message)
                    }
                })
            }
        }
    }
}
</script>
