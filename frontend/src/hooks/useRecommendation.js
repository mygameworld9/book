import { useCallback, useEffect, useRef, useState } from 'react'
import { getRecommendations } from '../services/api'

export default function useRecommendation(theme) {
  const [messages, setMessages] = useState([])
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const conversationRef = useRef([])

  useEffect(() => {
    // Reset state when theme changes
    conversationRef.current = []
    setMessages([])
    setRecommendations(null)
    setError(null)
    setLoading(false)
  }, [theme])

  const sendMessage = useCallback(
    async (text) => {
      const trimmed = text.trim()
      if (!trimmed) return

      const userMessage = { role: 'user', content: trimmed }
      setMessages((prev) => [...prev, userMessage])
      setLoading(true)
      setError(null)

      try {
        const history = conversationRef.current
        const data = await getRecommendations(theme, trimmed, history)
        const assistantMessage = { role: 'assistant', content: data.message }

        const nextHistory = [
          ...history,
          { role: 'user', content: trimmed },
          { role: 'assistant', content: data.message },
        ]
        conversationRef.current = nextHistory

        setMessages((prev) => [...prev, assistantMessage])
        setRecommendations(data)
      } catch (err) {
        const errorMessage =
          err?.response?.data?.error?.message ||
          err?.message ||
          '请求失败，请稍后再试'
        setError(errorMessage)
      } finally {
        setLoading(false)
      }
    },
    [theme]
  )

  const resetSession = useCallback(() => {
    conversationRef.current = []
    setMessages([])
    setRecommendations(null)
    setError(null)
  }, [])

  return {
    messages,
    recommendations,
    loading,
    error,
    sendMessage,
    resetSession,
  }
}
