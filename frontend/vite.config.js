import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue2'
import { resolve } from 'path'
const projectRootDir = resolve(__dirname);

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": resolve(projectRootDir, "src")
    }
  },
  build: {
    outDir: "dist",
    copyPublicDir: false,
    assetsDir: "static/assets",
    manifest: true,
    rollupOptions: {
      input: "src/main.js",
    }
  },
  server: {

  }
})
