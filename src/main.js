import { createApp } from 'vue'
import App from './App.vue'
import { useI18n } from './i18n/useI18n'

const app = createApp(App)

// Set HTML lang attribute based on detected language
const { locale } = useI18n()
const htmlRoot = document.getElementById('html-root')
if (htmlRoot) {
  htmlRoot.setAttribute('lang', locale.value)
}

app.mount('#app')
