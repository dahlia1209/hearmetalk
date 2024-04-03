import { fileURLToPath, URL } from 'node:url'
import { resolve } from 'path'
import { defineConfig, splitVendorChunkPlugin } from 'vite'
import vue from '@vitejs/plugin-vue'

const path = require("path");
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    splitVendorChunkPlugin()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: true
  },
  assetsInclude: ['**/*.mov'],
  build: {
    chunkSizeWarningLimit: 2000,
    rollupOptions: {
      output: {
        manualChunks(id: string) {
          if (id.includes('microsoft-cognitiveservices-speech-sdk')) {
            return 'microsoft-cognitiveservices-speech-sdk';
          }
        },
      },
    },
  },
})