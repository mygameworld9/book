import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'

function loadSharedViteEnv(mode) {
  const rootDir = path.resolve(__dirname, '..')
  const shared = loadEnv(mode, rootDir, 'VITE_')
  const local = loadEnv(mode, process.cwd(), 'VITE_')
  return { ...shared, ...local }
}

export default ({ mode }) => {
  const env = loadSharedViteEnv(mode)
  Object.entries(env).forEach(([key, value]) => {
    process.env[key] = value
  })

  return defineConfig({
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 3000,
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: './src/test/setup.js',
    },
  })
}
