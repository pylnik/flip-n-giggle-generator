import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  // Only use proxy in development when VITE_API_BASE_URL is not set
  const apiBaseUrl = process.env.VITE_API_BASE_URL
  
  const config = {
    plugins: [vue()],
    server: {
      port: 3000,
      host: true
    }
  }

  // Only add proxy if we're in development and no API base URL is configured
  if (mode === 'development' && !apiBaseUrl) {
    const proxyConfig = {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true
      }
    }
    
    config.server.proxy = proxyConfig
    config.preview = {
      proxy: proxyConfig
    }
  }

  return config
})
