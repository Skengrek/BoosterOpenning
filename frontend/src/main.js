
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';
import App from './App.vue';
import axios from 'axios';
import './index.css';

const pinia = createPinia();
const app = createApp(App).use(pinia);
app.use(ToastPlugin)
app.mount('#app');
app.config.globalProperties.$http = axios;
