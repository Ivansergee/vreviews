<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Регистрация</h1>
                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Имя пользователя</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="email" class="input" v-model="email">
                        </div>
                    </div>

                    <div class="field">
                        <label>Пароль</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password1">
                        </div>
                    </div>

                    <div class="field">
                        <label>Подтвердите пароль</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password2">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Регистрация</button>
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
    name: 'Sign Up',
    data() {
        return {
            username: '',
            email: '',
            password1: '',
            password2: '',
            errors: []
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.username === ''){
                this.errors.push('Заполните имя пользователя')
            }

            if (this.email === ''){
                this.errors.push('Введите email')
            }

            if (this.password1 === ''){
                this.errors.push('Пароль должен содержать не менее 4 символов')
            }

            if (this.password1 !== this.password2){
                this.errors.push('Пароли не совпадают')
            }

            if (!this.errors.length){
                const formData = {
                    username: this.username,
                    email: this.email,
                    password: this.password1,
                }

                axios
                .post('/users/', formData)
                .then(response => {
                    toast({
                        message: 'Вы успешно зарегистрированы!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'top-center',
                    })

                    this.$router.push('/login')
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        this.errors.push('Что-то пошло не так. Попробуйте ещё раз.')
                            
                        console.log(JSON.stringify(error))
                    }
                })
            }
        }
    }
}
</script>
