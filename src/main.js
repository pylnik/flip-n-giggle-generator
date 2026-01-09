import { createApp } from 'vue'
import App from './App.vue'
import './i18n/useI18n' // Import to initialize i18n and set up language detection

const app = createApp(App)
app.mount('#app')
