import express from 'express'
import cors from 'cors'
import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const app = express()
const PORT = 3001

// Enable CORS for frontend
app.use(cors())
app.use(express.json())

// API endpoint to fetch phrases
app.get('/api/phrases/:language', (req, res) => {
  const { language } = req.params
  
  const languageMap = {
    'en': 'phrases_en.txt',
    'de': 'phrases_de.txt',
    'ru': 'phrases_ru.txt'
  }
  
  const filename = languageMap[language]
  
  if (!filename) {
    return res.status(400).json({ error: 'Invalid language' })
  }
  
  try {
    const filePath = join(__dirname, 'phrases', filename)
    const content = readFileSync(filePath, 'utf-8')
    
    // Parse phrases (one per line in format "A / B / C")
    const phrases = content
      .split('\n')
      .map(line => line.trim())
      .filter(line => line && !line.startsWith('#'))
    
    res.json({
      language,
      count: phrases.length,
      phrases
    })
  } catch (error) {
    console.error(`Error reading phrases file: ${error.message}`)
    res.status(500).json({ error: 'Failed to load phrases' })
  }
})

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Flip-n-Giggle API is running' })
})

app.listen(PORT, () => {
  console.log(`🚀 Flip-n-Giggle API server running on http://localhost:${PORT}`)
  console.log(`📚 Available endpoints:`)
  console.log(`   GET /api/phrases/en - English phrases`)
  console.log(`   GET /api/phrases/de - German phrases`)
  console.log(`   GET /api/phrases/ru - Russian phrases`)
})
