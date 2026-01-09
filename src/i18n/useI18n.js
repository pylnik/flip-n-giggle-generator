import { ref, computed } from 'vue'
import { translations } from './translations'

// Detect user's system language
function detectLanguage() {
  // Get browser language
  const browserLang = navigator.language || navigator.userLanguage
  
  // Extract language code (e.g., 'en' from 'en-US')
  const langCode = browserLang.split('-')[0].toLowerCase()
  
  // Check if we have translations for this language
  if (translations[langCode]) {
    return langCode
  }
  
  // Fallback to English
  return 'en'
}

// Global state for current language
const currentLanguage = ref(detectLanguage())

// Save language preference to localStorage
function saveLanguagePreference(lang) {
  try {
    localStorage.setItem('flip-n-giggle-lang', lang)
  } catch (e) {
    // Ignore localStorage errors
  }
}

// Load language preference from localStorage
function loadLanguagePreference() {
  try {
    const saved = localStorage.getItem('flip-n-giggle-lang')
    if (saved && translations[saved]) {
      return saved
    }
  } catch (e) {
    // Ignore localStorage errors
  }
  return null
}

// Initialize language from localStorage or system
const savedLang = loadLanguagePreference()
if (savedLang) {
  currentLanguage.value = savedLang
}

export function useI18n() {
  // Get translation by key with optional placeholder replacement
  const t = (key, params = {}) => {
    const lang = currentLanguage.value
    const translation = translations[lang]?.[key] || translations['en']?.[key] || key
    
    // Replace placeholders like {count} with actual values
    return translation.replace(/\{(\w+)\}/g, (match, param) => {
      return params[param] !== undefined ? params[param] : match
    })
  }
  
  // Get plural form based on count
  const tp = (key, count) => {
    const lang = currentLanguage.value
    const translation = translations[lang]?.[key] || translations['en']?.[key] || key
    
    // Split by | for plural forms
    const forms = translation.split('|').map(s => s.trim())
    
    // English and German: singular (1) or plural (other)
    if (lang === 'en' || lang === 'de') {
      const form = count === 1 ? forms[0] : (forms[1] || forms[0])
      return form.replace('{count}', count)
    }
    
    // Russian: complex plural rules
    if (lang === 'ru') {
      const mod10 = count % 10
      const mod100 = count % 100
      
      let form
      if (mod10 === 1 && mod100 !== 11) {
        form = forms[0] // 1, 21, 31...
      } else if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) {
        form = forms[1] || forms[0] // 2-4, 22-24...
      } else {
        form = forms[2] || forms[1] || forms[0] // 0, 5-20, 25-30...
      }
      return form.replace('{count}', count)
    }
    
    // Fallback
    return translation.replace('{count}', count)
  }
  
  // Set current language
  const setLanguage = (lang) => {
    if (translations[lang]) {
      currentLanguage.value = lang
      saveLanguagePreference(lang)
    }
  }
  
  // Get available languages
  const availableLanguages = computed(() => Object.keys(translations))
  
  // Get current language code
  const locale = computed(() => currentLanguage.value)
  
  return {
    t,
    tp,
    setLanguage,
    availableLanguages,
    locale
  }
}
