import { useState } from 'react'
import { getRecommendations } from '../services/api'
import './ChatInterface.css'

function ChatInterface({ onRecommendation, onError, onLoading }) {
  const [message, setMessage] = useState('')
  const [conversationHistory, setConversationHistory] = useState([])
  const [messages, setMessages] = useState([])

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!message.trim()) return

    // 添加用户消息到显示列表
    const userMessage = { role: 'user', content: message }
    setMessages((prev) => [...prev, userMessage])

    // 清空输入框
    const userInput = message
    setMessage('')

    // 开始加载
    onLoading(true)

    try {
      // 调用API
      const data = await getRecommendations(userInput, conversationHistory)

      // 添加助手响应到对话历史
      const assistantMessage = {
        role: 'assistant',
        content: data.message,
      }
      setMessages((prev) => [...prev, assistantMessage])

      // 更新对话历史（供下次请求使用）
      setConversationHistory((prev) => [
        ...prev,
        { role: 'user', content: userInput },
        { role: 'assistant', content: data.message },
      ])

      // 传递推荐结果
      onRecommendation(data)
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || '请求失败'
      onError(errorMessage)
    } finally {
      onLoading(false)
    }
  }

  const handleReset = () => {
    setMessages([])
    setConversationHistory([])
    setMessage('')
  }

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>👋 欢迎使用AI图书推荐系统</h2>
            <p>告诉我您的阅读需求，我会为您推荐最合适的书籍</p>
            <div className="example-prompts">
              <p className="example-label">试试这些：</p>
              <button
                className="example-btn"
                onClick={() =>
                  setMessage('我想读一些科幻小说，最近读完了《三体》')
                }
              >
                科幻小说推荐
              </button>
              <button
                className="example-btn"
                onClick={() => setMessage('推荐一些轻松的文学作品')}
              >
                轻松文学
              </button>
              <button
                className="example-btn"
                onClick={() => setMessage('我想学习历史，推荐一些明清历史书籍')}
              >
                历史书籍
              </button>
            </div>
          </div>
        ) : (
          <div className="message-list">
            {messages.map((msg, index) => (
              <div key={index} className={`message message-${msg.role}`}>
                <div className="message-icon">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    {msg.role === 'user' ? '您' : 'AI助手'}
                  </div>
                  <div className="message-text">{msg.content}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <textarea
            className="chat-input"
            placeholder="描述您的阅读需求，比如：我想读一些科幻小说..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
            rows="3"
          />
        </div>
        <div className="input-actions">
          {messages.length > 0 && (
            <button type="button" className="btn-reset" onClick={handleReset}>
              🔄 重新开始
            </button>
          )}
          <button type="submit" className="btn-send" disabled={!message.trim()}>
            📤 发送
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatInterface
