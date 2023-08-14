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

// Set up store:
import { API } from '@/stores/api'

export default {
    name: 'LoginView',
    data() {
        return {
            api: API(),
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
                console.log("Start login")
                this.mode.login = await this.api.login(
                    this.login_data.username,
                    this.login_data.password
                )
                console.log("End login")
            } else {
                console.log("Username and Password can not be empty")
            }
        },
        async register() {
            if (this.register_data.username != "" || this.register_data.password != "") {
                this.mode.login = await this.api.register(
                    this.register_data.username,
                    this.register_data.password,
                    this.register_data.email,
                )
            } else {
                console.log("Username and Password can not be empty")
            }
        }
    },
}

</script>