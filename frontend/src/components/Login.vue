<template>
    <div v-if="!mode.login">
        <form name="login-form" class="glass-box" v-if="!mode.register">
            <div class="mb-3">
                <label for="username">Username: </label>
                <input id="username" type="text" v-model="login_data.username" />
            </div>
            <div class="mb-3">
                <label for="password">Password: </label>
                <input id="password" type="password" v-model="login_data.password" />
            </div>
            <button class="btn btn-outline-dark" type="submit" v-on:click.prevent="login()">
                Login
            </button>
            <div>
                <button class="btn btn-outline-dark" type="submit" v-on:click.prevent="switch_mode()">
                    You do not have an account ? let's register then !
                </button>
            </div>
        </form>
        <form name="register-form" class="glass-box" v-if="mode.register">
            <div class="mb-3">
                <label for="email">Email: </label>
                <input id="email" type="text" v-model="register_data.email" />
            </div>
            <div class="mb-3">
                <label for="username">Username: </label>
                <input id="username-register" type="text" v-model="register_data.username" />
            </div>
            <div class="mb-3">
                <label for="password">Password: </label>
                <input id="password-register" type="password" v-model="register_data.password" />
            </div>
            <button class="btn btn-outline-dark" type="submit" v-on:click.prevent="register()">
                Register
            </button>
            <div>
                <button class="btn btn-outline-dark" type="submit" v-on:click.prevent="switch_mode()">
                    You have an account ? let's go to the login then !
                </button>
            </div>
        </form>
    </div>
</template>

<style lang="css">
@import '../assets/styles/login.css';
</style>

<script>
const axios = require('axios').default

// Set up store:
import { loginStore } from '@/stores/login'

export default {
    name: 'LoginView',
    data() {
        return {
            store: loginStore(),
            login_data: {
                username: "",
                password: ""
            },
            register_data: {
                email: "",
                username: "",
                password: "",
                password2: "",
            },
            mode: {
                register: false,
                login: false,
            }
        }
    },
    methods: {
        switch_mode() {
            this.mode.register = !this.mode.register
        },
        async login() {
            if (this.login_data.username != "" || this.login_data.password != "") {
                try {
                    let response = await axios({
                        method: 'post',
                        url: 'http://localhost:8000/api/token/',
                        data: { username: this.login_data.username, password: this.login_data.password },
                        headers: { "content-type": "application/json" }
                    })
                    this.store.updateTokens(response.data.access, response.data.refresh)
                    this.mode.login = true
                    console.log(this.store)
                } catch (error) {
                    console.log(error)
                }
            } else {
                console.log("Username and Password can not be empty")
            }
        },
        async register() {
            if (this.register_data.username != "" || this.register_data.password != "") {
                try {
                    axios.defaults.xsrfHeaderName = 'x-csrftoken'
                    axios.defaults.xsrfCookieName = 'csrftoken'
                    axios.defaults.withCredentials = true
                    let response = await axios({
                        method: 'post',
                        url: 'http://localhost:8000/api/users/',
                        data: { username: this.register_data.username, password: this.register_data.password, email: this.register_data.email },
                        headers: { "content-type": "application/json" }
                    })
                    console.log(response)
                } catch (error) {
                    console.log(error)
                }
            } else {
                console.log("Username and Password can not be empty")
            }
        }
    },
}

</script>