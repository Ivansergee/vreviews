<template>
    <div class="box">
        <div class="level">
            <div class="level-left">
                <h1 class="title">Вход</h1>
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
                <label>Пароль</label>
                <div class="control">
                    <input type="password" class="input" v-model="password">
                </div>
            </div>

            <div class="notification is-danger" v-if="errors.length">
                <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>

            <div class="level">
                <div class="level-left">
                    <button
                      class="button is-dark"
                      :class="{'is-loading': isLoading}"
                    >Войти</button>
                </div>
                <div class="level-right">
                    <a @click="close(); $emit('showRegister')">Создать аккаунт</a>
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
    name: 'Log In',
    emits: ['logged', 'showRegister'],
    data() {
        return {
            username: '',
            password: '',
            errors: [],
            isLoading: false,
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

                this.isLoading = true;
                await axios
                .post('token/login/', formData)
                .then(response => {
                    const token = response.data.auth_token

                    this.$store.commit('setToken', token)
                    this.$store.commit('setUsername', this.username)

                    axios.defaults.headers.common['Authorization'] = 'Token ' + token

                    localStorage.setItem('token', token)
                    localStorage.setItem('username', this.username)

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
                            
                        console.log(error.message)
                    }
                }),

                await axios
                .get('users/me/')
                .then(response => {
                    this.$store.commit('setIsAdmin', response.data.is_staff);
                    localStorage.setItem('isAdmin', response.data.is_staff);
                })
                this.isLoading = false
            }
        },

        close(){
            this.password = '';
            this.username = '';
            this.$emit('logged');
        }
    }
}
</script>
