<template>
    <div class="box">
        <div class="level">
            <div class="level-left">
                <h1 class="title">Регистрация</h1>
            </div>
            <div class="level-right">
                <button class="delete is-medium" aria-label="close" @click="close()"></button>
            </div>
        </div>

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

            <div class="level">
                <div class="level-left">
                    <button
                      class="button is-dark"
                      :class="{ 'is-loading': isLoading }"
                    >Регистрация</button>
                </div>
                <div class="level-right">
                    <span>Уже зарегистрированы?&nbsp;&nbsp;</span><a @click="close(); $emit('showLogin')">Войти</a>
                </div>
            </div>
        </form>
    </div>
</template>

<style scoped>
.modal-background {
    background-color: rgb(10 10 10 / 60%);
}
</style>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'Sign Up',
    emits: ['signed', 'showLogin'],
    data() {
        return {
            username: '',
            email: '',
            password1: '',
            password2: '',
            errors: [],
            isLoading: false,
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

                this.isLoading = true;
                axios
                .post('/users/', formData)
                .then(() => {
                    toast({
                        message: 'Вы успешно зарегистрированы!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'top-center',
                    })

                    this.close();
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
                this.isLoading = false;
            }
        },

        close(){
            this.username = '';
            this.email = '';
            this.password1 = '';
            this.password2 = '';
            this.$emit('signed');
        }
    }
}
</script>
