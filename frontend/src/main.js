import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import Vue from 'vue'
import "./index.css";

const pinia = createPinia()
const app = createApp(App).use(createPinia())
app.use(pinia)
app.mount('#app')
import axios from 'axios'
Vue.prototype.$http = axios;
