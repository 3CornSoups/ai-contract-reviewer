<!--
=============================================================================
文件作用：合同智能审核页面，提供合同上传及AI审核结果(风险点/建议)的可视化展示
创建时间：2026-03-15
修改日志：
  2026-03-15: 初始创建
=============================================================================
-->
<template>
  <div class="audit-view">
    <el-row :gutter="20">
      <!-- 左侧：上传区 -->
      <el-col :span="8">
        <el-card shadow="never" class="upload-card">
          <template #header>
            <div class="card-header">
              <span>📄 待审合同上传</span>
            </div>
          </template>
          
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            accept=".pdf"
            :show-file-list="true"
            :limit="1"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将合同 PDF 拖到此处，或 <em>点击上传</em>
            </div>
          </el-upload>
          
          <el-button 
            type="primary" 
            style="width: 100%; margin-top: 20px;" 
            @click="startAudit"
            :loading="loading"
            :disabled="!selectedFile"
          >
            {{ loading ? 'AI正在深度审核中...' : '开始智能审核' }}
          </el-button>
        </el-card>
      </el-col>
      
      <!-- 右侧：审核结果区 -->
      <el-col :span="16">
        <el-card shadow="never" class="result-card" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>🔍 审核报告</span>
              <el-tag v-if="result" :type="statusType" style="margin-left: 10px;">
                {{ result.status === 'PASS' ? '审核通过' : '发现风险' }}
              </el-tag>
            </div>
          </template>
          
          <div v-if="!result && !loading" class="empty-state">
            请在左侧上传合同并点击开始审核
          </div>
          
          <div v-if="result" class="report-content">
            <div class="summary-section">
              <h3>总体概述 (风险等级: <span :class="riskClass">{{ result.risk_level }}</span>)</h3>
              <p>{{ result.summary }}</p>
            </div>
            
            <el-divider v-if="result.violations && result.violations.length > 0" />
            
            <div v-if="result.violations && result.violations.length > 0" class="violations-section">
              <h3>具体违规点与建议</h3>
              <el-collapse v-model="activeViolation">
                <el-collapse-item 
                  v-for="(item, index) in result.violations" 
                  :key="index" 
                  :name="index"
                >
                  <template #title>
                    <span class="violation-title">⚠️ {{ item.issue }}</span>
                  </template>
                  <div class="violation-detail">
                    <p><strong>⚖️ 法律依据：</strong> {{ item.basis }}</p>
                    <p><strong>💡 修改建议：</strong> {{ item.suggestion }}</p>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const selectedFile = ref(null)
const loading = ref(false)
const result = ref(null)
const activeViolation = ref([0])

const handleFileChange = (file) => {
  if (file.raw.type !== 'application/pdf') {
    ElMessage.error('只能上传 PDF 文件!')
    selectedFile.value = null
    return
  }
  selectedFile.value = file.raw
}

const startAudit = async () => {
  if (!selectedFile.value) return
  
  loading.value = true
  result.value = null
  
  try {
    const res = await api.auditContractFile(selectedFile.value)
    result.value = res
  } catch (error) {
    // 错误在拦截器中处理
  } finally {
    loading.value = false
  }
}

// 计算标签类型
const statusType = computed(() => {
  if (!result.value) return 'info'
  return result.value.status === 'PASS' ? 'success' : 'danger'
})

// 计算风险等级样式类
const riskClass = computed(() => {
  if (!result.value) return ''
  const level = result.value.risk_level.toLowerCase()
  if (level === 'high') return 'text-danger'
  if (level === 'medium') return 'text-warning'
  if (level === 'low') return 'text-primary'
  return 'text-success'
})
</script>

<style scoped>
.upload-card, .result-card {
  min-height: 500px;
}
.empty-state {
  text-align: center;
  color: #909399;
  padding: 100px 0;
}
.summary-section h3 {
  margin-top: 0;
}
.text-danger { color: #F56C6C; }
.text-warning { color: #E6A23C; }
.text-primary { color: #409EFF; }
.text-success { color: #67C23A; }
.violation-title {
  font-weight: bold;
  color: #F56C6C;
}
.violation-detail {
  background-color: #f8f8f8;
  padding: 15px;
  border-radius: 4px;
}
.violation-detail p {
  margin: 8px 0;
  line-height: 1.6;
}
</style>