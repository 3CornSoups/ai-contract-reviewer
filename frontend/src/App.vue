<!--
=============================================================================
文件作用：前端根组件，页面整体框架（顶部导航+侧边栏+主体内容）
创建时间：2026-03-15
修改日志：
  2026-03-15: 初始创建，包含两种主要功能页面的切换逻辑
=============================================================================
-->
<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="logo">⚖️ AI合同智能审核系统</div>
    </el-header>
    
    <el-container>
      <!-- 侧边栏菜单 -->
      <el-aside width="200px" class="app-aside">
        <el-menu :default-active="activeMenu" @select="handleSelect" class="el-menu-vertical">
          <el-menu-item index="audit">
            <el-icon><Document /></el-icon>
            <span>合同智能审核</span>
          </el-menu-item>
          <el-menu-item index="knowledge">
            <el-icon><Management /></el-icon>
            <span>法律知识库管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主体内容区 -->
      <el-main class="app-main">
        <!-- 根据菜单动态渲染组件 -->
        <component :is="currentComponent"></component>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Document, Management } from '@element-plus/icons-vue'
import AuditView from './views/AuditView.vue'
import KnowledgeView from './views/KnowledgeView.vue'

// 当前激活的菜单项
const activeMenu = ref('audit')

/**
 * 菜单切换处理函数
 * @param {string} index - 菜单项标识
 */
const handleSelect = (index) => {
  activeMenu.value = index
}

// 动态计算当前应展示的组件
const currentComponent = computed(() => {
  return activeMenu.value === 'audit' ? AuditView : KnowledgeView
})
</script>

<style>
.app-container {
  height: 100vh;
}
.app-header {
  background-color: #2b3a4a;
  color: white;
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
}
.logo {
  margin-left: 20px;
}
.app-aside {
  background-color: #ffffff;
  border-right: 1px solid #dcdfe6;
}
.el-menu-vertical {
  border-right: none;
}
.app-main {
  background-color: #f0f2f5;
  padding: 24px;
}
</style>