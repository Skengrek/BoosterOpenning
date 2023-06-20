<template>
    <form name="login-form">
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
    </form>
    <form name="register-form">
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
        <div class="mb-3">
            <label for="password">Password 2: </label>
            <input id="password-register2" type="password" v-model="register_data.password2" />
        </div>
        <button class="btn btn-outline-dark" type="submit" v-on:click.prevent="register()">
            Register
        </button>
    </form>
</template>

<style lang="css">
@import '../assets/styles/base.css';
</style>

<script>
const axios = require('axios').default
export default {
    name: 'LoginView',
    data() {
        return {
            login_data: {
                username: "",
                password: ""
            },
            register_data: {
                email: "",
                username: "",
                password: "",
                password2: "",
            }
        }
    },
    methods: {
        async login() {
            if (this.login_data.username != "" || this.login_data.password != "") {
                try {

                    let response = await axios({
                        method: 'post',
                        url: 'http://localhost:8000/api/token/',
                        data: { username: this.login_data.username, password: this.login_data.password },
                        headers: { "content-type": "application/json" }
                    })
                    console.log(response)
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