// =========================================================================
// 文件作用：Vite 打包和开发服务器配置文件
// 创建时间：2026-03-15
// 修改日志：
//   2026-03-15: 初始创建，配置代理解决开发环境跨域问题
// =========================================================================

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      // 开发环境代理配置，将 /api 请求转发至后端的 FastAPI (8000端口)
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})