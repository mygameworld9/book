import axios from 'axios'

const resolvedBaseURL =
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' ? `${window.location.origin}` : 'http://localhost:8000')

const apiClient = axios.create({
  baseURL: resolvedBaseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000,
})

export async function getRecommendations(
  theme,
  userMessage,
  conversationHistory = []
) {
  if (!theme) {
    throw new Error('缺少推荐主题')
  }
  const endpoint = `/api/${theme}/recommend`
  try {
    const response = await apiClient.post(endpoint, {
      user_message: userMessage,
      conversation_history: conversationHistory,
    })
    return response.data
  } catch (error) {
    console.error('API调用失败:', error)
    throw error
  }
}

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
