<template>
  <div class="app-container">
    <header class="header">
      <div class="container header-content">
        <div class="header-text">
          <h1>🎪 {{ t('title') }}</h1>
          <p class="subtitle">{{ t('subtitle') }}</p>
        </div>
        <div class="language-switcher">
          <button 
            v-for="lang in availableLanguages" 
            :key="lang"
            @click="setLanguage(lang)"
            :class="['lang-btn', { active: locale === lang }]"
            type="button"
            :title="getLanguageName(lang)"
          >
            {{ getLanguageFlag(lang) }}
          </button>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="container">
        <div class="card">
          <!-- Main Configuration -->
          <section class="config-section">
            <h2>📚 {{ t('bookConfig') }}</h2>
            
            <div class="form-group">
              <label for="pageSize">{{ t('pageSize') }}</label>
              <select id="pageSize" v-model="config.pageSize" class="form-control">
                <option value="A4">A4</option>
                <option value="LETTER">Letter</option>
              </select>
            </div>

            <div class="form-group">
              <label for="phrasesPerPage">{{ t('phrasesPerPage') }}</label>
              <select id="phrasesPerPage" v-model="config.phrasesPerPage" class="form-control">
                <option :value="1">{{ tp('phrasesPerPageOption', 1) }}</option>
                <option :value="2">{{ tp('phrasesPerPageOption', 2) }}</option>
                <option :value="4">{{ tp('phrasesPerPageOption', 4) }}</option>
              </select>
            </div>

            <div class="form-group">
              <label for="cutGuides">{{ t('cutGuides') }}</label>
              <select id="cutGuides" v-model="config.cutGuides" class="form-control">
                <option value="internal">{{ t('cutGuidesInternal') }}</option>
                <option value="box">{{ t('cutGuidesBox') }}</option>
                <option value="all">{{ t('cutGuidesAll') }}</option>
                <option value="none">{{ t('cutGuidesNone') }}</option>
              </select>
            </div>

            <!-- Advanced Settings Expander -->
            <div class="expander">
              <button 
                class="expander-toggle" 
                @click="showAdvanced = !showAdvanced"
                type="button"
              >
                ⚙️ {{ t('advancedSettings') }}
                <span class="toggle-icon">{{ showAdvanced ? '▼' : '▶' }}</span>
              </button>
              
              <div v-if="showAdvanced" class="expander-content">
                <div class="form-group">
                  <label for="textCase">{{ t('textCase') }}</label>
                  <select id="textCase" v-model="config.textCase" class="form-control">
                    <option value="none">{{ t('textCaseOriginal') }}</option>
                    <option value="upper">{{ t('textCaseUpper') }}</option>
                    <option value="lower">{{ t('textCaseLower') }}</option>
                    <option value="sentence">{{ t('textCaseSentence') }}</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="maxFont">{{ t('maxFontSize') }}</label>
                  <input 
                    type="number" 
                    id="maxFont" 
                    v-model.number="config.maxFont" 
                    min="20" 
                    max="200" 
                    class="form-control"
                  >
                </div>

                <div class="form-group">
                  <label for="minFont">{{ t('minFontSize') }}</label>
                  <input 
                    type="number" 
                    id="minFont" 
                    v-model.number="config.minFont" 
                    min="10" 
                    max="100" 
                    class="form-control"
                  >
                </div>

                <div class="form-group">
                  <label for="margin">{{ t('pageMargin') }}</label>
                  <input 
                    type="number" 
                    id="margin" 
                    v-model.number="config.margin" 
                    min="0" 
                    max="100" 
                    class="form-control"
                  >
                </div>
              </div>
            </div>
          </section>

          <!-- Phrases Section -->
          <section class="phrases-section">
            <h2>✏️ {{ t('phrasesTitle') }}</h2>
            
            <div class="preset-buttons">
              <button 
                v-for="preset in presets" 
                :key="preset.id"
                @click="loadPreset(preset.id)"
                :disabled="loading"
                class="btn btn-secondary"
                type="button"
              >
                {{ t(preset.labelKey) }}
              </button>
            </div>

            <div class="form-group">
              <label for="phrasesInput">{{ t('phrasesInputLabel') }}</label>
              <textarea 
                id="phrasesInput"
                v-model="phrasesText"
                rows="10"
                class="form-control textarea"
                :placeholder="t('phrasesPlaceholder')"
              ></textarea>
              <small class="form-hint">
                {{ t('phrasesHint') }}
              </small>
            </div>
          </section>

          <!-- Generate Button -->
          <div class="action-section">
            <button 
              @click="generatePDF" 
              :disabled="loading || !phrasesText.trim()"
              class="btn btn-primary btn-large"
              type="button"
            >
              {{ loading ? '⏳ ' + t('generating') : '🎨 ' + t('generatePDF') }}
            </button>
          </div>

          <!-- Status Messages -->
          <div v-if="error" class="alert alert-error">
            ❌ {{ error }}
          </div>
          <div v-if="success" class="alert alert-success">
            ✅ {{ success }}
          </div>
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="container">
        <p>{{ t('madeWith') }} | <a href="https://github.com/pylnik/flip-n-giggle-generator" target="_blank">{{ t('github') }}</a></p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { generateFlipBookPDF } from './utils/pdfGenerator'
import { useI18n } from './i18n/useI18n'

export default {
  name: 'App',
  setup() {
    const { t, tp, setLanguage, availableLanguages, locale } = useI18n()
    
    const config = reactive({
      pageSize: 'A4',
      phrasesPerPage: 1,
      cutGuides: 'internal',
      textCase: 'none',
      maxFont: 110,
      minFont: 26,
      margin: 48,
      padding: 18,
      gutter: 18
    })

    const showAdvanced = ref(false)
    const phrasesText = ref('')
    const loading = ref(false)
    const error = ref('')
    const success = ref('')

    const presets = [
      { id: 'en', labelKey: 'presetEnglish' },
      { id: 'de', labelKey: 'presetGerman' },
      { id: 'ru', labelKey: 'presetRussian' }
    ]

    // Language helper functions
    const getLanguageFlag = (lang) => {
      const flags = {
        en: '🇬🇧',
        de: '🇩🇪',
        ru: '🇷🇺'
      }
      return flags[lang] || '🌐'
    }

    const getLanguageName = (lang) => {
      const names = {
        en: 'English',
        de: 'Deutsch',
        ru: 'Русский'
      }
      return names[lang] || lang
    }

    const loadPreset = async (presetId) => {
      loading.value = true
      error.value = ''
      success.value = ''
      
      try {
        const response = await fetch(`/api/phrases/${presetId}`)
        if (!response.ok) throw new Error('Failed to load preset')
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type')
        if (!contentType || !contentType.startsWith('application/json')) {
          throw new Error('Server returned an error response. Please ensure the API server is running.')
        }
        
        const data = await response.json()
        phrasesText.value = data.phrases.join('\n')
        success.value = t('loadedPhrases', { count: data.phrases.length })
        
        setTimeout(() => {
          success.value = ''
        }, 3000)
      } catch (err) {
        error.value = t('presetLoadError')
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const generatePDF = async () => {
      loading.value = true
      error.value = ''
      success.value = ''

      try {
        // Parse phrases
        const lines = phrasesText.value
          .split('\n')
          .map(line => line.trim())
          .filter(line => line && !line.startsWith('#'))

        if (lines.length === 0) {
          throw new Error(t('enterAtLeastOne'))
        }

        const phrases = lines.map(line => {
          // Support multiple delimiters
          for (const delim of [' / ', ' | ', ' ; ', '/', '|', ';']) {
            if (line.includes(delim)) {
              const parts = line.split(delim).map(p => p.trim()).filter(p => p)
              if (parts.length === 3) {
                return { a: parts[0], b: parts[1], c: parts[2] }
              }
            }
          }
          throw new Error(t('invalidPhraseFormat', { phrase: line }))
        })

        // Generate PDF
        await generateFlipBookPDF(phrases, config)
        
        success.value = t('pdfGeneratedSuccess', { count: phrases.length })
        
        setTimeout(() => {
          success.value = ''
        }, 5000)
      } catch (err) {
        error.value = err.message
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    return {
      t,
      tp,
      setLanguage,
      availableLanguages,
      locale,
      config,
      showAdvanced,
      phrasesText,
      loading,
      error,
      success,
      presets,
      loadPreset,
      generatePDF,
      getLanguageFlag,
      getLanguageName
    }
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 2rem 1rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.header-text {
  flex: 1;
  text-align: center;
}

.header h1 {
  font-size: 2.5rem;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.language-switcher {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.lang-btn {
  width: 48px;
  height: 48px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.lang-btn:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.lang-btn.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.lang-btn.active:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.main-content {
  flex: 1;
  padding: 2rem 1rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.config-section,
.phrases-section {
  margin-bottom: 2rem;
}

.config-section h2,
.phrases-section h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #555;
  font-size: 0.95rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
}

.textarea {
  font-family: 'Courier New', monospace;
  resize: vertical;
  min-height: 150px;
}

.form-hint {
  display: block;
  margin-top: 0.5rem;
  color: #888;
  font-size: 0.85rem;
}

.expander {
  margin-top: 1.5rem;
}

.expander-toggle {
  width: 100%;
  padding: 1rem;
  background: #f8f9fa;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
}

.expander-toggle:hover {
  background: #e9ecef;
  border-color: #667eea;
}

.toggle-icon {
  font-size: 0.8rem;
}

.expander-content {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.preset-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f8f9fa;
  color: #555;
  border: 2px solid #e0e0e0;
}

.btn-secondary:hover:not(:disabled) {
  background: #e9ecef;
  border-color: #667eea;
}

.btn-large {
  width: 100%;
  padding: 1.25rem;
  font-size: 1.25rem;
}

.action-section {
  margin: 2rem 0;
}

.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-weight: 500;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.footer {
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem 1rem;
  text-align: center;
  color: #666;
  margin-top: 2rem;
}

.footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.footer a:hover {
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .header-text {
    text-align: center;
  }

  .language-switcher {
    justify-content: center;
  }

  .header h1 {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .card {
    padding: 1.5rem;
  }

  .preset-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 1.5rem 0.5rem;
  }

  .main-content {
    padding: 1rem 0.5rem;
  }

  .card {
    padding: 1rem;
    border-radius: 8px;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .lang-btn {
    width: 44px;
    height: 44px;
    font-size: 1.25rem;
  }
}
</style>
