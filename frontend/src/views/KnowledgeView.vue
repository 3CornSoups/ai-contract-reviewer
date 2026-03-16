<!--
=============================================================================
文件作用：知识库管理页面，提供PDF法律法规文件的上传入口
创建时间：2026-03-15
修改日志：
  2026-03-15: 初始创建
=============================================================================
-->
<template>
  <div class="knowledge-view">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>📚 法律知识库管理</span>
        </div>
      </template>
      
      <div class="upload-section">
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          accept=".pdf"
          :show-file-list="true"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将 PDF 文件拖到此处，或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              请上传法律法规原件 (仅支持 PDF 格式)
            </div>
          </template>
        </el-upload>
        
        <el-button 
          type="primary" 
          @click="submitUpload" 
          :loading="loading"
          style="margin-top: 20px;"
          :disabled="!selectedFile"
        >
          {{ loading ? '正在解析入库中...' : '开始解析并入库' }}
        </el-button>
      </div>
      
      <div v-if="result" class="result-section">
        <el-alert
          :title="result.message"
          type="success"
          show-icon
          :closable="false"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const selectedFile = ref(null)
const loading = ref(false)
const result = ref(null)

/**
 * 处理文件选择，拦截默认上传行为
 * @param {Object} file - 包含文件信息的对象
 */
const handleFileChange = (file) => {
  if (file.raw.type !== 'application/pdf') {
    ElMessage.error('只能上传 PDF 文件!')
    selectedFile.value = null
    return
  }
  selectedFile.value = file.raw
}

/**
 * 提交文件至后端接口进行向量化入库
 */
const submitUpload = async () => {
  if (!selectedFile.value) return
  
  loading.value = true
  result.value = null
  
  try {
    const res = await api.uploadKnowledgeFile(selectedFile.value)
    result.value = res
    ElMessage.success('文档入库成功')
  } catch (error) {
    // 错误在 api 拦截器中已提示
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.upload-section {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}
.result-section {
  margin-top: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
</style>