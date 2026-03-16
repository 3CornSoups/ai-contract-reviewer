// =========================================================================
// 文件作用：封装前端 API 请求工具类
// 创建时间：2026-03-15
// 依赖项：axios
// 修改日志：
//   2026-03-15: 初始创建
// =========================================================================

import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 Axios 实例，复用通用配置
const apiClient = axios.create({
  baseURL: '/api', // Vite 配置了 proxy，实际将转发到后端
  timeout: 120000, // 合同审核可能较慢，设置2分钟超时
})

// 添加响应拦截器处理错误
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const errorMsg = error.response?.data?.detail || error.message || '请求发生错误'
    ElMessage.error(errorMsg)
    return Promise.reject(error)
  }
)

export default {
  /**
   * 上传法律文件至知识库
   * @param {File} file - PDF文件对象
   * @returns {Promise} 返回入库结果
   */
  uploadKnowledgeFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/knowledge/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * 上传待审核合同
   * @param {File} file - PDF合同文件对象
   * @returns {Promise} 返回大模型审核JSON结果
   */
  auditContractFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/contract/audit', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}