
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import axios from 'axios';
import './index.css';

const pinia = createPinia();
const app = createApp(App).use(pinia);
app.mount('#app');
app.config.globalProperties.$http = axios;
