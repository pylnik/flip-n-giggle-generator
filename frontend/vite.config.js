import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const apiProxy = {
  '/api': {
    target: 'http://localhost:3001',
    changeOrigin: true
  }
}

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: true,
    proxy: apiProxy
  },
  preview: {
    proxy: apiProxy
  }
})
