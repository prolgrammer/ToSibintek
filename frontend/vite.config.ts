import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import mkcert from 'vite-plugin-mkcert'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    mkcert()
  ],
  resolve: {
    alias: {
      '@pages': path.resolve(__dirname, "src/pages"),
      '@widgets': path.resolve(__dirname, "src/widgets"),
      '@shared': path.resolve(__dirname, "src/shared"),
      '@features': path.resolve(__dirname, "src/features"),
      '@entities': path.resolve(__dirname, "src/entities"),
      '@public': path.resolve(__dirname, "src/public"),
    }
  },
  server: {
    port: 3000,
    host: '0.0.0.0'
  }
})
