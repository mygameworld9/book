import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 120秒超时（LLM调用可能较慢）
})

/**
 * 获取图书推荐
 * @param {string} userMessage - 用户消息
 * @param {Array} conversationHistory - 对话历史
 * @returns {Promise<Object>} 推荐结果
 */
export async function getRecommendations(userMessage, conversationHistory = []) {
  try {
    const response = await apiClient.post('/api/v1/recommendations', {
      user_message: userMessage,
      conversation_history: conversationHistory,
    })
    return response.data
  } catch (error) {
    console.error('API调用失败:', error)
    throw error
  }
}

/**
 * 健康检查
 * @returns {Promise<Object>} 健康状态
 */
export async function checkHealth() {
  try {
    const response = await apiClient.get('/health')
    return response.data
  } catch (error) {
    console.error('健康检查失败:', error)
    throw error
  }
}

export default apiClient
