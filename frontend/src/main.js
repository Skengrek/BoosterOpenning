import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'
import Vue from 'vue'
import "./index.css";
const store = createStore({
    state() {
        return {
            accessToken: "",
            refreshToken: ""
        }
    }
}
)
const app = createApp(App)
app.use(store)
app.mount('#app')
import axios from 'axios'
Vue.prototype.$http = axios;
