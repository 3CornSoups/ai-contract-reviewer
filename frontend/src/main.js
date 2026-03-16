// =========================================================================
// 文件作用：前端项目入口文件，初始化 Vue 实例并挂载全局组件库
// 创建时间：2026-03-15
// 依赖项：vue, element-plus
// 修改日志：
//   2026-03-15: 初始创建
// =========================================================================

import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// Element-Plus中文语言包
import zhCn from 'element-plus/es/locale/lang/zh-cn'

const app = createApp(App)

app.use(ElementPlus, {
  locale: zhCn,
})

app.mount('#app')