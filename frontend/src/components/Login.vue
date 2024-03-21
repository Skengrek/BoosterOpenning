<template>
    <div v-if="!user.api.isLogged">
        <form name="login-form" class="glass-box" v-if="!mode.register">
            <div class="mb-3">
                <label for="username">Username </label>
                <input id="username" type="text" v-model="login_data.username" />
            </div>
            <div class="mb-3">
                <label for="password">Password: </label>
                <input id="password" type="password" v-model="login_data.password" />
            </div>
            <hr class="solid">
            <div class="horizontaldiv">
                <button class="loginbtn" type="submit" v-on:click.prevent="login()">
                    Login
                </button>
                <button class="loginbtn" type="submit" v-on:click.prevent="switch_mode()">
                    Register
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
            <hr class="solid">
            <div class="horizontaldiv">
                <button class="loginbtn" type="submit" v-on:click.prevent="register()">
                    Register
                </button>
                <button class="loginbtn" type="submit" v-on:click.prevent="switch_mode()">
                    Login
                </button>
            </div>
            
            <div>
                
            </div>
        </form>
    </div>
</template>

<style lang="css">
@import '../assets/styles/login.css';
</style>

<script>

// Set up store:
import { UserStore } from '@/stores/user'

export default {
    name: 'LoginView',
    data() {
        return {
            user: UserStore(),
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
                this.mode.login = await this.user.login(
                    this.login_data.username,
                    this.login_data.password
                )
                if (this.mode.login){
                    this.$toast.success('Connected', {
                        position: 'top',
                    })
                }
                else {
                    this.$toast.error('Wrong Username / Password', {
                        position: 'top',
                    })
                }
            } else {
                console.log("Username and Password can not be empty")
            }
        },
        async register() {
            if (this.register_data.username != "" || this.register_data.password != "") {
                this.mode.login = await this.user.register(
                    this.register_data.username,
                    this.register_data.password,
                    this.register_data.email,
                )
            } else {
                console.log("Username and Password can not be empty")
            }
            if (this.mode.login){
                this.$toast.success('Connected', {
                    position: 'top',
                })
            }
            else {
                this.$toast.error('Something went wrong', {
                    position: 'top',
                })
            }
        }
    },
}

</script>