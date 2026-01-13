import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    // Optimisations de build (esbuild est plus rapide que terser)
    minify: 'esbuild',
    rollupOptions: {
      output: {
        // Code splitting manuel pour meilleur caching
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
        },
      },
    },
    // Augmente la limite de warning pour les gros chunks (si nécessaire)
    chunkSizeWarningLimit: 1000,
  },
  // Optimisation des assets
  assetsInclude: ['**/*.webp', '**/*.jpg', '**/*.png'],
})

