import { createApp } from 'vue'
import App from './App.vue'
import Vue from 'vue'
import "./index.css";

createApp(App).mount('#app')

import axios from 'axios'
Vue.prototype.$http = axios;
