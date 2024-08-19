<template>
    <div v-if="!app.api.isLogged">
        <form name="login-form" class="glass-box" v-if="!state_register">


            <v-text-field v-model="login_data.username" label="Username" variant="underlined"></v-text-field>
            <v-text-field 
                v-model="login_data.password"
                label="Password"
                type="password"
                variant="underlined"
                persistent-counter
            ></v-text-field>
            <div class="horizontaldiv">
                <button class="loginbtn" type="submit" v-on:click.prevent="login()">
                    Login
                </button>
                <button class="loginbtn" type="submit" v-on:click.prevent="switch_mode()">
                    Register
                </button>
            </div>
        </form>
        <form name="register-form" class="glass-box" v-if="state_register">
            <v-text-field v-model="register_data.email" label="Mail" variant="underlined"></v-text-field>
            <v-text-field v-model="register_data.username" label="Username" variant="underlined"></v-text-field>
            <v-text-field v-model="register_data.password" label="Password" variant="underlined"></v-text-field>
            <v-text-field v-model="register_data.password2" label="Verify password" variant="underlined"></v-text-field>
            <div class="horizontaldiv">
                <button class="loginbtn" type="submit" v-on:click.prevent="state_register()">
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
*,
*:before,
*:after {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}
form {
    width: 350px;
    background-color: rgba(255, 255, 255, 0.13);
    position: absolute;
    transform: translate(-50%, -50%);
    top: 50%;
    left: 50%;
    border-radius: 10px;
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border: 2px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 40px rgba(8, 7, 16, 0.6);
    padding: 35px;
}

form * {
    font-family: "Poppins", sans-serif;
    color: rgb(223, 223, 223);
    letter-spacing: 0.5px;
    outline: none;
    border: none;
}

@media (prefers-color-scheme: dark) {
    form * {
        color: #ffffff;
    }
}

form h3 {
    font-size: 32px;
    font-weight: 500;
    line-height: 42px;
    text-align: center;
}
button.loginbtn {
    margin: 10px;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.07);
    color:rgb(223, 223, 223);
    padding: 15px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 5px;
    cursor: pointer;
}


/* Solid border */
hr.solid {
    border-top: 3px solid rgba(255, 255, 255, 0.07);
}

div.horizontaldiv{
    display:flex;
}
</style>

<script>

// Set up store:
import { AppStore } from '@/stores/app'
import { useToast } from 'vue-toast-notification';

export default {
    name: 'LoginView',
    data() {
        return {
            app: AppStore(),
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
            state_register: false,
            toast: useToast()
        }
    },
    methods: {
        switch_mode() {
            this.state_register = !this.state_register
        },
        async login() {
            if (this.login_data.username != "" || this.login_data.password != "") {
                const isLogged = await this.app.login(
                    this.login_data.username,
                    this.login_data.password
                )
                if(isLogged){this.toast.success("Logged in!")}
                else {this.toast.error("Username or password are wrong.")}
            } else {
                console.log("Username and Password can not be empty")
            }
        },
        async register() {
            if (this.register_data.username != "" || this.register_data.password != "") {
                if (this.register_data.password === this.register_data.password2){
                    const isLogged = await this.app.register(
                        this.register_data.username,
                        this.register_data.password,
                        this.register_data.email,
                    )
                    if (isLogged){this.toast.success("Logged in!")}
                }
                
            } else {
                console.log("Username and Password can not be empty")
            }
        }
    },
}

</script>