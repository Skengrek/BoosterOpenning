import { createApp } from 'vue';
import { createPinia } from 'pinia';
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';
import App from './App.vue';
import axios from 'axios';
import './index.css';

// basic import of Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// import icons for Vuetify
import "@mdi/font/css/materialdesignicons.css";
import "@fortawesome/fontawesome-free/css/all.css";

const vuetify = createVuetify({
    components,
    directives,
})

const pinia = createPinia();
const app = createApp(App).use(pinia);
app.use(ToastPlugin)
app.use(vuetify)
app.mount('#app');
app.config.globalProperties.$http = axios;
