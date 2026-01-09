import { createApp } from 'vue'
import App from './App.vue'
import { useI18n } from './i18n/useI18n'

// Initialize i18n to set up language detection and HTML lang attribute
const { locale } = useI18n()

// Set initial HTML lang attribute
document.documentElement.setAttribute('lang', locale.value)

const app = createApp(App)
app.mount('#app')
